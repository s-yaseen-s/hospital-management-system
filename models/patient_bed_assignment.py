from datetime import datetime
from models.database import db
from models.patient import Patient
from models.room_bed import RoomBed

class PatientBedAssignment(db.Model):
    __tablename__ = 'patient_bed_assignment'
    
    assign_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    bed_no = db.Column(db.Integer, db.ForeignKey('room_bed.bed_no'))
    start_date = db.Column(db.Date, default=datetime.utcnow)
    end_date = db.Column(db.Date)
    
    # Relationships
    patient = db.relationship('Patient', backref='bed_assignments')
    bed = db.relationship('RoomBed', backref='bed_assignments_rel')