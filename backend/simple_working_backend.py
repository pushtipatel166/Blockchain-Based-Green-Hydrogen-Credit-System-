from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return {"status": "healthy", "message": "Simple Backend is running!"}

@app.route('/api/login', methods=['POST'])
def login():
    # Accept any login - bypass authentication
    data = request.get_json()
    username = data.get('username', 'demo_user')
    role = data.get('role', 'buyer')
    
    return jsonify({
        "success": True,
        "message": "Login successful - Bypassed",
        "user": {
            "id": 1,
            "username": username,
            "role": role,
            "email": f"{username}@example.com"
        },
        "token": "bypass_token_12345"
    })

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    return jsonify({
        "success": True,
        "message": "Signup successful - Bypassed",
        "user": {
            "id": 1,
            "username": data.get('username', 'demo_user'),
            "role": data.get('role', 'buyer'),
            "email": data.get('email', 'demo@example.com')
        }
    })

@app.route('/api/profile', methods=['GET'])
def get_profile():
    return jsonify({
        "data": {
            "id": 1,
            "username": "demo_user",
            "role": "buyer",
            "email": "demo@example.com"
        }
    })

@app.route('/api/buyer/credits', methods=['GET'])
def get_buyer_credits():
    # Fake credits with realistic hydrogen credit data
    fake_credits = [
        {
            "id": "H2_CREDIT_001",
            "name": "Wind-Powered Hydrogen Production",
            "description": "Green hydrogen produced using 100% renewable wind energy in North Sea offshore farms",
            "amount": 1500,  # kg of H2
            "price": 0.85,   # ETH per kg
            "total_value": 1275,  # ETH
            "creator": {"username": "NorthSea_Wind", "organization": "NorthSea Wind Farms Ltd"},
            "is_active": True,
            "is_expired": False,
            "secure_url": "https://example.com/docs/wind_h2_001",
            "production_method": "Wind Electrolysis",
            "location": "North Sea, Netherlands",
            "verification_score": 0.98,
            "carbon_footprint": "0.0 kg CO2/kg H2",
            "created_at": "2025-08-15T10:30:00Z",
            "expires_at": "2026-08-15T10:30:00Z",
            "certification": "ISO 14001, Green Hydrogen Standard",
            "blockchain_id": "0x1234567890abcdef1234567890abcdef12345678"
        },
        {
            "id": "H2_CREDIT_002", 
            "name": "Solar Hydrogen from Desert Farms",
            "description": "Hydrogen produced using concentrated solar power in Sahara desert regions",
            "amount": 2200,  # kg of H2
            "price": 0.72,   # ETH per kg
            "total_value": 1584,  # ETH
            "creator": {"username": "Sahara_Solar", "organization": "Sahara Solar Initiative"},
            "is_active": True,
            "is_expired": False,
            "secure_url": "https://example.com/docs/solar_h2_002",
            "production_method": "Solar Thermal Electrolysis",
            "location": "Sahara Desert, Morocco",
            "verification_score": 0.96,
            "carbon_footprint": "0.0 kg CO2/kg H2",
            "created_at": "2025-08-10T14:20:00Z",
            "expires_at": "2026-08-10T14:20:00Z",
            "certification": "ISO 14001, Solar Hydrogen Certified",
            "blockchain_id": "0xabcdef1234567890abcdef1234567890abcdef12"
        },
        {
            "id": "H2_CREDIT_003",
            "name": "Geothermal Hydrogen Production",
            "description": "Hydrogen generated using geothermal energy from Iceland's volcanic activity",
            "amount": 800,   # kg of H2
            "price": 1.15,   # ETH per kg
            "total_value": 920,   # ETH
            "creator": {"username": "Iceland_Geo", "organization": "Iceland Geothermal Energy"},
            "is_active": True,
            "is_expired": False,
            "secure_url": "https://example.com/docs/geo_h2_003",
            "production_method": "Geothermal Electrolysis",
            "location": "Reykjanes, Iceland",
            "verification_score": 0.99,
            "carbon_footprint": "0.0 kg CO2/kg H2",
            "created_at": "2025-08-20T09:15:00Z",
            "expires_at": "2026-08-20T09:15:00Z",
            "certification": "ISO 14001, Geothermal Hydrogen Standard",
            "blockchain_id": "0x7890abcdef1234567890abcdef1234567890abcd"
        },
        {
            "id": "H2_CREDIT_004",
            "name": "Tidal Energy Hydrogen",
            "description": "Hydrogen produced using tidal energy from Scottish coastal waters",
            "amount": 1200,  # kg of H2
            "price": 0.95,   # ETH per kg
            "total_value": 1140,  # ETH
            "creator": {"username": "Scottish_Tides", "organization": "Scottish Marine Energy"},
            "is_active": True,
            "is_expired": False,
            "secure_url": "https://example.com/docs/tidal_h2_004",
            "production_method": "Tidal Electrolysis",
            "location": "Pentland Firth, Scotland",
            "verification_score": 0.94,
            "carbon_footprint": "0.0 kg CO2/kg H2",
            "created_at": "2025-08-05T16:45:00Z",
            "expires_at": "2026-08-05T16:45:00Z",
            "certification": "ISO 14001, Marine Energy Certified",
            "blockchain_id": "0x4567890abcdef1234567890abcdef1234567890ab"
        },
        {
            "id": "H2_CREDIT_005",
            "name": "Biomass Hydrogen from Agricultural Waste",
            "description": "Hydrogen produced from agricultural waste using advanced gasification technology",
            "amount": 3000,  # kg of H2
            "price": 0.65,   # ETH per kg
            "total_value": 1950,  # ETH
            "creator": {"username": "Agri_Waste_H2", "organization": "Agricultural Waste Solutions"},
            "is_active": True,
            "is_expired": False,
            "secure_url": "https://example.com/docs/biomass_h2_005",
            "production_method": "Biomass Gasification",
            "location": "Midwest, USA",
            "verification_score": 0.92,
            "carbon_footprint": "0.1 kg CO2/kg H2",
            "created_at": "2025-08-12T11:30:00Z",
            "expires_at": "2026-08-12T11:30:00Z",
            "certification": "ISO 14001, Biomass Hydrogen Standard",
            "blockchain_id": "0xef1234567890abcdef1234567890abcdef1234567"
        }
    ]
    
    return jsonify({
        "data": fake_credits,
        "total": len(fake_credits),
        "total_value": sum(credit["total_value"] for credit in fake_credits)
    })

@app.route('/api/buyer/portfolio-analytics', methods=['GET'])
def get_portfolio_analytics():
    return jsonify({
        "data": {
            "totalInvested": 150.00,
            "currentValue": 175.50,
            "profitLoss": 25.50,
            "profitLossPercentage": 17.0,
            "hydrogenOffset": 75.5,
            "creditsCount": 3
        }
    })

@app.route('/api/buyer/purchase', methods=['POST'])
def purchase_credit():
    data = request.get_json()
    credit_id = data.get('creditId')
    buyer_address = data.get('buyerAddress')
    amount = data.get('amount')
    price = data.get('price')
    
    # Simulate purchase success
    return jsonify({
        "success": True,
        "message": f"Successfully purchased {amount}kg of hydrogen credit {credit_id}",
        "transaction_hash": "0x" + "a" * 64,  # Fake transaction hash
        "purchase_data": {
            "credit_id": credit_id,
            "buyer_address": buyer_address,
            "amount": amount,
            "price": price,
            "total_cost": amount * price,
            "purchase_date": datetime.now().isoformat()
        }
    })

@app.route('/api/buyer/market-trends', methods=['GET'])
def get_market_trends():
    return jsonify({
        "data": {
            "price_trend": "increasing",
            "volume_24h": 12500,
            "market_cap": 2500000,
            "price_change_24h": 5.2,
            "popular_production_methods": ["Wind", "Solar", "Geothermal"]
        }
    })

@app.route('/api/buyer/notifications', methods=['GET'])
def get_notifications():
    return jsonify({
        "data": [
            {
                "id": 1,
                "type": "price_alert",
                "message": "Wind hydrogen credits dropped 5% in price",
                "timestamp": datetime.now().isoformat(),
                "read": False
            }
        ]
    })

@app.route('/api/NGO/my-credits', methods=['GET'])
def get_ngo_credits():
    return jsonify({
        "data": [
            {
                "id": 1,
                "name": "Wind H₂ Production",
                "amount": 100,
                "price": 0.5,
                "creator": {"username": "wind_ngo"},
                "is_active": True,
                "is_expired": False,
                "secure_url": "https://example.com/docs"
            }
        ]
    })

@app.route('/api/NGO/auto-credits', methods=['GET'])
def get_auto_credits():
    return jsonify({
        "data": [
            {
                "id": 1,
                "name": "Auto-Generated H₂ Credit",
                "amount": 50,
                "price": 0.4,
                "creator": {"username": "ai_system"},
                "is_active": True,
                "is_expired": False,
                "secure_url": "https://example.com/docs"
            }
        ]
    })

@app.route('/api/NGO/transactions', methods=['GET'])
def get_transactions():
    return jsonify({
        "data": [
            {
                "id": 1,
                "type": "credit_created",
                "amount": 100,
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            }
        ]
    })

@app.route('/api/buyer/purchased-credits', methods=['GET'])
def get_purchased_credits():
    return jsonify({
        "data": [
            {
                "id": 1,
                "name": "Purchased H₂ Credit",
                "amount": 50,
                "price": 0.5,
                "purchase_date": datetime.now().isoformat(),
                "status": "active"
            }
        ]
    })

@app.route('/api/verification/submit', methods=['POST'])
def submit_verification():
    return jsonify({
        "success": True,
        "message": "Verification submitted successfully",
        "verification_id": "VER_001"
    })

@app.route('/api/verification/ml-verify', methods=['POST'])
def ml_verify():
    return jsonify({
        "success": True,
        "message": "ML verification completed",
        "verification_score": 0.95,
        "status": "approved"
    })

@app.route('/api/NGO/create-credit', methods=['POST'])
def create_credit():
    data = request.get_json()
    
    # Simulate credit creation success
    return jsonify({
        "success": True,
        "message": "Credit created successfully!",
        "credit_id": f"CREDIT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "data": {
            "name": data.get('name', 'New Hydrogen Credit'),
            "amount": data.get('amount', 100),
            "price": data.get('price', 0.5),
            "created_at": datetime.now().isoformat()
        }
    })

if __name__ == '__main__':
    print("🚀 Starting SIMPLE working backend server...")
    print("✅ No complex dependencies required!")
    print("✅ Authentication bypassed!")
    print("✅ All endpoints working!")
    print("✅ Fake credits added for buyer dashboard!")
    print("✅ Credit creation endpoint added!")
    app.run(debug=True, host='0.0.0.0', port=5000)
