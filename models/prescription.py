from models.database import db

class Prescription(db.Model):
    __tablename__ = 'prescription'
    
    script_id = db.Column(db.Integer, primary_key=True)
    instructions = db.Column(db.Text)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    doc_id = db.Column(db.Integer, db.ForeignKey('doctor.doc_id'))
    appt_id = db.Column(db.Integer, db.ForeignKey('appointment.appt_id'))
    
    medications = db.relationship('Medication', secondary='prescription_medication', backref='prescriptions')