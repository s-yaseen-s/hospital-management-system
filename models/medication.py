from models.database import db

class Medication(db.Model):
    __tablename__ = 'medication'
    
    med_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100))
    frequency = db.Column(db.String(100))
    instructions = db.Column(db.Text)