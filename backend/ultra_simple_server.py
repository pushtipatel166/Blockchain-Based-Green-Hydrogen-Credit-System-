from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Database file
DB_FILE = 'ultra_simple.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS credits (
        id TEXT PRIMARY KEY,
        name TEXT,
        amount INTEGER,
        price REAL,
        creator_id TEXT,
        is_verified INTEGER,
        created_at TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS verification_requests (
        id TEXT PRIMARY KEY,
        industry_id TEXT,
        credit_id TEXT,
        hydrogen_amount INTEGER,
        production_method TEXT,
        status TEXT
    )
    ''')
    
    # Clear existing data and add test users
    cursor.execute('DELETE FROM users')
    cursor.execute('DELETE FROM credits')
    cursor.execute('DELETE FROM verification_requests')
    
    # Add test users
    test_users = [
        ('test_admin', 'test_admin', 'sepolia', 'NGO'),
        ('test_buyer', 'test_buyer', 'sepolia', 'buyer')
    ]
    
    for user in test_users:
        cursor.execute('INSERT INTO users (id, username, password, role) VALUES (?, ?, ?, ?)', user)
    
    # Add fake credits
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
    return jsonify({"status": "OK", "message": "Ultra Simple Server is running!"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ? AND role = ?', 
                  (username, password, role))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({
            "access_token": "ultra_simple_token_123",
            "user": {
                "id": user[0],
                "username": user[1],
                "role": user[3]
            }
        })
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/api/NGO/auto-credits', methods=['GET'])
def ngo_auto_credits():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT c.*, v.hydrogen_amount, v.production_method 
    FROM credits c 
    LEFT JOIN verification_requests v ON c.id = v.credit_id 
    WHERE c.is_verified = 1
    ''')
    
    credits = []
    for row in cursor.fetchall():
        credits.append({
            "id": row[0],
            "name": row[1],
            "amount": row[2],
            "price": row[3],
            "creator_id": row[4],
            "is_verified": bool(row[5]),
            "created_at": row[6],
            "hydrogen_amount": row[7] or 0,
            "production_method": row[8] or "Unknown"
        })
    
    conn.close()
    return jsonify(credits)

@app.route('/api/buyer/credits', methods=['GET'])
def buyer_credits():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM credits WHERE is_verified = 1')
    
    credits = []
    for row in cursor.fetchall():
        credits.append({
            "id": row[0],
            "name": row[1],
            "amount": row[2],
            "price": row[3],
            "creator_id": row[4],
            "is_verified": bool(row[5]),
            "created_at": row[6]
        })
    
    conn.close()
    return jsonify(credits)

@app.route('/api/verification/submit', methods=['POST'])
def submit_verification():
    data = request.get_json()
    
    # Simulate ML verification - always pass
    is_valid = True
    
    if is_valid:
        # Generate new credit ID
        new_credit_id = f"CREDIT_{len(os.listdir('.')) + 100}"
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Add new credit
        cursor.execute('''
        INSERT INTO credits (id, name, amount, price, creator_id, is_verified, created_at) 
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        ''', (new_credit_id, f'H₂ Credit - {data.get("production_method", "New")}', 
              data.get("hydrogen_amount", 100), 250.0, data.get("industry_id", "test_admin"), 1))
        
        # Add verification request
        cursor.execute('''
        INSERT INTO verification_requests (id, industry_id, credit_id, hydrogen_amount, production_method, status) 
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (f"VER_{new_credit_id}", data.get("industry_id", "test_admin"), 
              new_credit_id, data.get("hydrogen_amount", 100), 
              data.get("production_method", "New"), "approved"))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "message": "Verification successful! Credit generated automatically.",
            "credit_id": new_credit_id,
            "is_valid": True
        })
    
    return jsonify({"message": "Verification failed", "is_valid": False}), 400

if __name__ == '__main__':
    print("Starting Ultra Simple Server...")
    init_db()
    print("Server ready! Starting Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True)
