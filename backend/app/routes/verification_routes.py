from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_current_user
from app.models.verification import VerificationRequest, VerificationDocument
from app.models.user import User
from app.models.credit import Credit
from app.ml_models.h2_verification_model import advanced_h2_model
from app import db
from datetime import datetime
import json
import os

verification_bp = Blueprint('verification', __name__)

@verification_bp.route('/api/verification/submit', methods=['POST'])
@jwt_required()
def submit_verification():
    """Submit H₂ production for ML verification"""
    current_user = get_current_user()
    if not current_user:
        return jsonify({"message": "Invalid token"}), 401

    user = User.query.filter_by(username=current_user['username']).first()
    if user.role != 'NGO':
        return jsonify({"message": "Only NGOs can submit verifications"}), 403

    data = request.get_json()
    
    # Extract data
    energy_mwh = float(data.get('energy_mwh', 0))
    h2_kg = float(data.get('h2_kg', 0))
    production_method = data.get('production_method', 'electrolysis')
    production_date = data.get('production_date')
    
    # ML Verification
    ml_result = advanced_h2_model.verify_h2_production(
        energy_mwh, h2_kg, production_method,
        location=data.get('location', 'unknown'),
        timestamp=data.get('production_date'),
        equipment_specs=data.get('equipment_specs'),
        weather_data=data.get('weather_data'),
        historical_data=data.get('historical_data')
    )
    
    # Check if ML verification passed
    if ml_result['is_valid']:
        # 🚀 AUTO-GENERATE CREDIT & TOKEN when ML verification passes
        credit_id = f"CREDIT_{datetime.now().strftime('%Y%m%d')}_{int(datetime.now().timestamp())}"
        token_id = f"TOKEN_{datetime.now().strftime('%Y%m%d')}_{int(datetime.now().timestamp())}"
        
        # Create credit automatically
        credit = Credit(
            id=credit_id,
            name=f"H₂ Credit - {production_method.capitalize()} - {h2_kg}kg",
            description=f"ML-Verified H₂ production using {production_method}",
            amount=h2_kg,
            price=h2_kg * 2.5,  # $2.5 per kg H₂
            creator_id=user.id,
            is_verified=True,
            is_active=True,
            is_expired=False,
            req_status=2,  # Approved status
            score=100  # Perfect ML verification score
        )
        
        db.session.add(credit)
        db.session.commit()
        
        # Create verification request with credit linked
        verification_request = VerificationRequest(
            industry_id=user.id,
            credit_id=credit.id,
            hydrogen_amount=h2_kg,
            production_date=datetime.strptime(production_date, '%Y-%m-%d').date(),
            production_method=production_method,
            energy_source='renewable',
            status='approved'  # Auto-approved by ML
        )
        
        db.session.add(verification_request)
        db.session.commit()
        
        # Auto-generate government documents
        documents = generate_government_documents(verification_request.id, energy_mwh, h2_kg)
        
        return jsonify({
            "success": True,
            "message": "🚀 ML Verification PASSED! Credit & Token automatically generated!",
            "verification_id": verification_request.id,
            "credit_id": credit_id,
            "token_id": token_id,
            "ml_verification": ml_result,
            "documents": documents,
            "status": "approved",
            "auto_generated": True,
            "hydrogen_amount": h2_kg,
            "credit_value": credit.price
        })
    else:
        # ML verification failed
        verification_request = VerificationRequest(
            industry_id=user.id,
            credit_id=None,
            hydrogen_amount=h2_kg,
            production_date=datetime.strptime(production_date, '%Y-%m-%d').date(),
            production_method=production_method,
            energy_source='renewable',
            status='rejected'
        )
        
        db.session.add(verification_request)
        db.session.commit()
        
        return jsonify({
            "success": False,
            "message": "❌ ML Verification FAILED! Credit not generated.",
            "verification_id": verification_request.id,
            "ml_verification": ml_result,
            "status": "rejected"
        })

@verification_bp.route('/api/verification/ml-verify', methods=['POST'])
@jwt_required()
def ml_verify():
    """Direct ML verification endpoint"""
    data = request.get_json()
    energy_mwh = float(data.get('energy_mwh', 0))
    h2_kg = float(data.get('h2_kg', 0))
    production_method = data.get('production_method', 'electrolysis')
    
    result = advanced_h2_model.verify_h2_production(
        energy_mwh, h2_kg, production_method,
        location=data.get('location', 'unknown'),
        timestamp=data.get('timestamp'),
        equipment_specs=data.get('equipment_specs'),
        weather_data=data.get('weather_data'),
        historical_data=data.get('historical_data')
    )
    
    return jsonify({
        "ml_verification": result,
        "recommendation": "APPROVED" if result['is_valid'] else "REJECTED"
    })

@verification_bp.route('/api/verification/pending', methods=['GET'])
@jwt_required()
def get_pending_verifications():
    """Get pending verifications for review"""
    current_user = get_current_user()
    if not current_user:
        return jsonify({"message": "Invalid token"}), 401

    user = User.query.filter_by(username=current_user['username']).first()
    

    pending_verifications = VerificationRequest.query.filter_by(status='pending').all()
    
    verifications = []
    for v in pending_verifications:
        industry = User.query.get(v.industry_id)
        documents = VerificationDocument.query.filter_by(verification_request_id=v.id).all()
        
        # Re-run ML verification
        ml_result = advanced_h2_model.verify_h2_production(
            v.energy_source_mwh if hasattr(v, 'energy_source_mwh') else 1000,
            v.hydrogen_amount,
            v.production_method,
            location='unknown',
            timestamp=v.created_at.isoformat() if v.created_at else None
        )
        
        verifications.append({
            "id": v.id,
            "industry_name": industry.username,
            "hydrogen_amount": v.hydrogen_amount,
            "production_method": v.production_method,
            "production_date": v.production_date.strftime('%Y-%m-%d'),
            "created_at": v.created_at.strftime('%Y-%m-%d %H:%M'),
            "documents_count": len(documents),
            "ml_verification": ml_result
        })
    
    return jsonify(verifications)

@verification_bp.route('/api/verification/<int:verification_id>/approve', methods=['POST'])
@jwt_required()
def approve_verification(verification_id):
    """Approve verification and generate credits"""
    current_user = get_current_user()
    if not current_user:
        return jsonify({"message": "Invalid token"}), 401

    user = User.query.filter_by(username=current_user['username']).first()
    

    verification = VerificationRequest.query.get(verification_id)
    if not verification:
        return jsonify({"message": "Verification not found"}), 404

    data = request.get_json()
    notes = data.get('notes', '')
    
    # Update verification status
    verification.status = 'approved'
    verification.verification_date = datetime.utcnow()
    verification.verification_notes = notes
    
    # Generate credit
    credit = Credit(
        name=f"H₂ Credit - {verification.production_method}",
        description=f"Verified H₂ production using {verification.production_method}",
        amount=verification.hydrogen_amount,
        price=verification.hydrogen_amount * 2.5,  # $2.5 per kg H₂
        creator_id=verification.industry_id,
        is_verified=True
    )
    
    db.session.add(credit)
    db.session.commit()
    
    # Link credit to verification
    verification.credit_id = credit.id
    db.session.commit()
    
    return jsonify({
        "message": "Verification approved and credits generated",
        "credit_id": credit.id,
        "hydrogen_amount": verification.hydrogen_amount,
        "credit_value": credit.price
    })

@verification_bp.route('/api/verification/<int:verification_id>/reject', methods=['POST'])
@jwt_required()
def reject_verification(verification_id):
    """Reject verification"""
    current_user = get_current_user()
    if not current_user:
        return jsonify({"message": "Invalid token"}), 401

    user = User.query.filter_by(username=current_user['username']).first()
    

    verification = VerificationRequest.query.get(verification_id)
    if not verification:
        return jsonify({"message": "Verification not found"}), 404

    data = request.get_json()
    notes = data.get('notes', 'Verification rejected')
    
    verification.status = 'rejected'
    
    verification.verification_date = datetime.utcnow()
    verification.verification_notes = notes
    
    db.session.commit()
    
    return jsonify({
        "message": "Verification rejected",
        "verification_id": verification_id
    })

@verification_bp.route('/api/verification/industry-status', methods=['GET'])
@jwt_required()
def get_industry_verification_status():
    """Get verification status for industry"""
    current_user = get_current_user()
    if not current_user:
        return jsonify({"message": "Invalid token"}), 401

    user = User.query.filter_by(username=current_user['username']).first()
    if user.role != 'NGO':
        return jsonify({"message": "Only NGOs can view their verification status"}), 403

    verifications = VerificationRequest.query.filter_by(industry_id=user.id).all()
    
    status_list = []
    for v in verifications:
        documents = VerificationDocument.query.filter_by(verification_request_id=v.id).all()
        
        status_list.append({
            "id": v.id,
            "hydrogen_amount": v.hydrogen_amount,
            "production_method": v.production_method,
            "status": v.status,
            "created_at": v.created_at.strftime('%Y-%m-%d %H:%M'),
            "documents_count": len(documents),
            "credit_id": v.credit_id
        })
    
    return jsonify(status_list)

def generate_government_documents(verification_id, energy_mwh, h2_kg):
    """Auto-generate realistic government documents"""
    documents = []
    
    # Energy Production Certificate
    energy_doc = {
        "type": "energy_certificate",
        "title": "Renewable Energy Production Certificate",
        "content": f"Certified that {energy_mwh} MWh of renewable energy was produced from wind turbines on {datetime.now().strftime('%Y-%m-%d')}",
        "government_signature": f"gov_sig_{datetime.now().timestamp()}",
        "certificate_number": f"REC-{verification_id:06d}"
    }
    
    # H₂ Production Certificate
    h2_doc = {
        "type": "h2_certificate", 
        "title": "Green Hydrogen Production Certificate",
        "content": f"Certified that {h2_kg} kg of green hydrogen was produced using {energy_mwh} MWh of renewable energy",
        "government_signature": f"gov_sig_{datetime.now().timestamp()}",
        "certificate_number": f"H2C-{verification_id:06d}"
    }
    
    # Efficiency Report
    efficiency = (energy_mwh * 1000) / h2_kg
    efficiency_doc = {
        "type": "efficiency_report",
        "title": "H₂ Production Efficiency Report",
        "content": f"Production efficiency: {efficiency:.2f} kWh/kg H₂ (Industry standard: 45-60 kWh/kg)",
        "efficiency_score": "EXCELLENT" if 45 <= efficiency <= 55 else "GOOD" if 55 < efficiency <= 60 else "POOR"
    }
    
    documents = [energy_doc, h2_doc, efficiency_doc]
    
    # Save documents to database
    for doc in documents:
        verification_doc = VerificationDocument(
            verification_request_id=verification_id,
            document_type=doc["type"],
            file_path=f"/documents/{doc['type']}_{verification_id}.json",
            file_name=f"{doc['title']}.json",
            file_size=len(json.dumps(doc)),
            is_verified=True
        )
        db.session.add(verification_doc)
    
    db.session.commit()
    
    return documents


