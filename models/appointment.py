from datetime import datetime
from models.database import db

class Appointment(db.Model):
    __tablename__ = 'appointment'
    
    appt_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(50), default='Scheduled')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    doc_id = db.Column(db.Integer, db.ForeignKey('doctor.doc_id'))
    rec_id = db.Column(db.Integer, db.ForeignKey('receptionist.rec_id'))
    
    prescriptions = db.relationship('Prescription', backref='appointment', lazy=True)