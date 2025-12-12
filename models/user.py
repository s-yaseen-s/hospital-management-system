from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db

class User(db.Model, UserMixin):
    __tablename__ = 'user_account'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    
    doctor = db.relationship('Doctor', backref='user', uselist=False)
    nurse = db.relationship('Nurse', backref='user', uselist=False)
    receptionist = db.relationship('Receptionist', backref='user', uselist=False)
    
    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_doctor(self):
        return self.role == 'doctor'
    
    @property
    def is_nurse(self):
        return self.role == 'nurse'
    
    @property
    def is_receptionist(self):
        return self.role == 'receptionist'