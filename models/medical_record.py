from models.database import db

class MedicalRecord(db.Model):
    __tablename__ = 'medical_record'
    
    record_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), unique=True)
    
    doctor_updates = db.relationship('DoctorUpdatesRecord', backref='medical_record', lazy=True)
    nurse_updates = db.relationship('NurseUpdatesRecord', backref='medical_record', lazy=True)