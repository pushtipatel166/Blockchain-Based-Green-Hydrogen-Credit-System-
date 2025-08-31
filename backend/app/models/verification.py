from app import db
from datetime import datetime

class VerificationRequest(db.Model):
    __tablename__ = 'verification_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    industry_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    credit_id = db.Column(db.Integer, db.ForeignKey('credits.id'), nullable=True)

    
    hydrogen_amount = db.Column(db.Float, nullable=False)
    production_date = db.Column(db.Date, nullable=False)
    production_method = db.Column(db.String(50), nullable=False)
    energy_source = db.Column(db.String(50), nullable=False)
    energy_source_mwh = db.Column(db.Float, nullable=True)
    
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verification_date = db.Column(db.DateTime, nullable=True)
    verification_notes = db.Column(db.Text, nullable=True)
    
    # Relationships
    industry = db.relationship('User', foreign_keys=[industry_id], backref='verification_requests')

    credit = db.relationship('Credit', backref='verification_request')
    documents = db.relationship('VerificationDocument', backref='verification_request', cascade='all, delete-orphan')


class VerificationDocument(db.Model):
    __tablename__ = 'verification_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    verification_request_id = db.Column(db.Integer, db.ForeignKey('verification_requests.id'), nullable=False)
    
    document_type = db.Column(db.String(50), nullable=False)  # energy_certificate, h2_certificate, efficiency_report
    file_path = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


