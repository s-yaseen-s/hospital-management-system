from datetime import datetime
from models.database import db

class Invoice(db.Model):
    __tablename__ = 'invoice'
    
    inv_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    rec_id = db.Column(db.Integer, db.ForeignKey('receptionist.rec_id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    payments = db.relationship('Payment', backref='invoice', lazy=True)