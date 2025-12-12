from models.database import db

class Receptionist(db.Model):
    __tablename__ = 'receptionist'
    
    rec_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.user_id'))
    
    appointments = db.relationship('Appointment', backref='receptionist', lazy=True)
    invoices = db.relationship('Invoice', backref='receptionist', lazy=True)