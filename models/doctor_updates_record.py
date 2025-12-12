from datetime import datetime
from models.database import db

class DoctorUpdatesRecord(db.Model):
    __tablename__ = 'doctor_updates_record'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doc_id'), nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('medical_record.record_id'), nullable=True)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    
    def __init__(self, doctor_id, description, record_id=None):
        self.doctor_id = doctor_id
        self.description = description
        self.record_id = record_id
