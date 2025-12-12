from datetime import datetime
from models.database import db

class Payment(db.Model):
    __tablename__ = 'payment'
    
    payment_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    inv_id = db.Column(db.Integer, db.ForeignKey('invoice.inv_id'))