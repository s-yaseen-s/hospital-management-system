from datetime import datetime
from models.database import db

class NurseUpdatesRecord(db.Model):
    __tablename__ = 'nurse_updates_record'
    
    id = db.Column(db.Integer, primary_key=True)
    nurse_id = db.Column(db.Integer, db.ForeignKey('nurse.nurse_id'), nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('medical_record.record_id'), nullable=True)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    
    def __init__(self, nurse_id, description, record_id=None):
        self.nurse_id = nurse_id
        self.description = description
        self.record_id = record_id
