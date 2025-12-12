from datetime import datetime
from models.database import db

class PatientBedAssignment(db.Model):
    __tablename__ = 'patient_bed_assignment'
    
    assign_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    bed_no = db.Column(db.Integer, db.ForeignKey('room_bed.bed_no'))
    start_date = db.Column(db.Date, default=datetime.utcnow)
    end_date = db.Column(db.Date)