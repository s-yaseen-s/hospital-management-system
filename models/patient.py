from models.database import db

class Patient(db.Model):
    __tablename__ = 'patient'
    
    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    age = db.Column(db.Integer)
    previous_conditions = db.Column(db.Text)
    street = db.Column(db.String(100))
    city = db.Column(db.String(100))
    
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    medical_record = db.relationship('MedicalRecord', backref='patient', uselist=False)
    prescriptions = db.relationship('Prescription', backref='patient', lazy=True)
    lab_tests = db.relationship('LabTest', backref='patient', lazy=True)
    invoices = db.relationship('Invoice', backref='patient', lazy=True)