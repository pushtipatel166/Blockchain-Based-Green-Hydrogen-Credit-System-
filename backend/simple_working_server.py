from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_PATH = 'carbon_credit_simple.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS credits (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        amount INTEGER NOT NULL,
        price REAL NOT NULL,
        creator_id TEXT NOT NULL,
        is_verified BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS verification_requests (
        id TEXT PRIMARY KEY,
        industry_id TEXT NOT NULL,
        credit_id TEXT,
        hydrogen_amount INTEGER NOT NULL,
        production_method TEXT NOT NULL,
        status TEXT DEFAULT 'pending'
    )
    ''')
    
    # Add test users
    cursor.execute('DELETE FROM users WHERE username IN (?, ?)', ('test_admin', 'test_buyer'))
    cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (str(uuid.uuid4()), 'test_admin', 'sepolia', 'NGO'))
    cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (str(uuid.uuid4()), 'test_buyer', 'sepolia', 'buyer'))
    
    # Add fake credits for testing
    cursor.execute('DELETE FROM credits')
    fake_credits = [
        ('CREDIT_001', 'H₂ Credit - Electrolysis', 150, 375.0, 'test_admin', 1, '2025-08-31 10:00:00'),
        ('CREDIT_002', 'H₂ Credit - Steam Reforming', 200, 500.0, 'test_admin', 1, '2025-08-31 11:00:00'),
        ('CREDIT_003', 'H₂ Credit - Biomass', 100, 250.0, 'test_admin', 1, '2025-08-31 12:00:00'),
        ('CREDIT_004', 'H₂ Credit - Solar', 300, 750.0, 'test_admin', 1, '2025-08-31 13:00:00')
    ]
    
    for credit in fake_credits:
        cursor.execute('''
        INSERT INTO credits (id, name, amount, price, creator_id, is_verified, created_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', credit)
    
    # Add fake verification requests
    cursor.execute('DELETE FROM verification_requests')
    fake_verifications = [
        ('VER_001', 'test_admin', 'CREDIT_001', 150, 'Electrolysis', 'approved'),
        ('VER_002', 'test_admin', 'CREDIT_002', 200, 'Steam Reforming', 'approved'),
        ('VER_003', 'test_admin', 'CREDIT_003', 100, 'Biomass', 'approved'),
        ('VER_004', 'test_admin', 'CREDIT_004', 300, 'Solar', 'approved')
    ]
    
    for ver in fake_verifications:
        cursor.execute('''
        INSERT INTO verification_requests (id, industry_id, credit_id, hydrogen_amount, production_method, status) 
        VALUES (?, ?, ?, ?, ?, ?)
        ''', ver)
    
    conn.commit()
    conn.close()
    print("Database initialized with test users and fake credits!")

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "Simple server running"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ? AND role = ?', (username, password, role))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({
            "access_token": "mock_token_123",
            "role": role
        })
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/api/NGO/auto-credits', methods=['GET'])
def get_auto_credits():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT c.*, v.production_method, v.hydrogen_amount 
    FROM credits c 
    LEFT JOIN verification_requests v ON c.id = v.credit_id 
    WHERE c.is_verified = 1
    ''')
    credits = cursor.fetchall()
    conn.close()
    
    auto_credits = []
    for credit in credits:
        auto_credits.append({
            "id": credit[0],
            "name": credit[1],
            "amount": credit[2],
            "price": credit[3],
            "token_id": f"TOKEN_{credit[0]}",
            "production_method": credit[7] or "Unknown",
            "hydrogen_amount": credit[8] or credit[2],
            "verification_date": credit[6],
            "ml_score": 100,
            "status": "ML-Approved & Token Generated"
        })
    
    return jsonify({
        "auto_credits": auto_credits,
        "total_auto_generated": len(auto_credits)
    })

@app.route('/api/buyer/credits', methods=['GET'])
def get_buyer_credits():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM credits WHERE is_verified = 1')
    credits = cursor.fetchall()
    conn.close()
    
    buyer_credits = []
    for credit in credits:
        buyer_credits.append({
            "id": credit[0],
            "name": credit[1],
            "amount": credit[2],
            "price": credit[3],
            "creator_id": credit[4],
            "is_verified": credit[5],
            "created_at": credit[6]
        })
    
    return jsonify(buyer_credits)

@app.route('/api/verification/submit', methods=['POST'])
def submit_verification():
    data = request.get_json()
    
    # Simulate ML verification - always approve for testing
    ml_result = {"is_valid": True, "confidence": 0.95}
    
    if ml_result['is_valid']:
        # Auto-generate credit
        credit_id = f"CREDIT_{datetime.now().strftime('%Y%m%d')}_{int(datetime.now().timestamp())}"
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create credit
        cursor.execute('''
        INSERT INTO credits (id, name, amount, price, creator_id, is_verified) 
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (credit_id, f"H₂ Credit - {data['production_method']}", data['hydrogen_amount'], 
              data['hydrogen_amount'] * 2.5, data['industry_id'], 1))
        
        # Create verification request
        cursor.execute('''
        INSERT INTO verification_requests (id, industry_id, credit_id, hydrogen_amount, production_method, status) 
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (str(uuid.uuid4()), data['industry_id'], credit_id, data['hydrogen_amount'], 
              data['production_method'], 'approved'))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "🚀 ML Verification PASSED! Credit & Token automatically generated!",
            "credit_id": credit_id,
            "token_id": f"TOKEN_{credit_id}",
            "status": "approved"
        })
    else:
        return jsonify({
            "success": False,
            "message": "ML Verification failed"
        })

if __name__ == '__main__':
    init_db()
    print("Simple working server starting...")
    app.run(host='0.0.0.0', port=5000, debug=True)
