import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mssql+pymssql://sa:YourPassword@localhost/HospitalDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    ROLES = {
        'admin': 'admin',
        'doctor': 'doctor',
        'nurse': 'nurse',
        'receptionist': 'receptionist'
    }