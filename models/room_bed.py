from models.database import db

class RoomBed(db.Model):
    __tablename__ = 'room_bed'
    
    bed_no = db.Column(db.Integer, primary_key=True)
    room_no = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='Available')
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'))
    
    # Relationships
    department = db.relationship('Department', back_populates='rooms')
    assignments = db.relationship('PatientBedAssignment', backref='bed_assignments', lazy=True)