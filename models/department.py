from models.database import db

class Department(db.Model):
    __tablename__ = 'department'
    
    dept_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # Relationships
    doctors = db.relationship('Doctor', back_populates='department', lazy=True)
    rooms = db.relationship('RoomBed', back_populates='department', lazy=True)