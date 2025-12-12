from models.database import db

class LabTest(db.Model):
    __tablename__ = 'lab_test'
    
    test_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    result = db.Column(db.Text)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    doc_id = db.Column(db.Integer, db.ForeignKey('doctor.doc_id'))