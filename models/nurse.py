from models.database import db

class Nurse(db.Model):
    __tablename__ = 'nurse'
    
    nurse_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.user_id'))
    
    record_updates = db.relationship('NurseUpdatesRecord', backref='nurse', lazy=True)