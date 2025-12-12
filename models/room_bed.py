from models.database import db

class RoomBed(db.Model):
    __tablename__ = 'room_bed'
    
    bed_no = db.Column(db.Integer, primary_key=True)
    room_no = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='Available')
    
    assignments = db.relationship('PatientBedAssignment', backref='bed', lazy=True)