from models.database import db

class Department(db.Model):
    __tablename__ = 'department'
    
    dept_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Active')
    head_doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doc_id'))
    
    # Relationships
    doctors = db.relationship('Doctor', back_populates='department', lazy=True, foreign_keys='Doctor.dept_id')
    rooms = db.relationship('RoomBed', back_populates='department', lazy=True)
    head_doctor = db.relationship('Doctor', foreign_keys=[head_doctor_id], backref='headed_departments')