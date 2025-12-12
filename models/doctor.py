from models.database import db

class Doctor(db.Model):
    __tablename__ = 'doctor'
    
    doc_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.user_id'))
    
    department = db.relationship('Department', back_populates='doctors')
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    prescriptions = db.relationship('Prescription', backref='doctor', lazy=True)
    lab_tests = db.relationship('LabTest', backref='doctor', lazy=True)
    record_updates = db.relationship('DoctorUpdatesRecord', backref='doctor', lazy=True)