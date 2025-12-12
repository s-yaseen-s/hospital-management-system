import os
from pathlib import Path

# Get the base directory
basedir = Path(__file__).parent.absolute()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # SQLite configuration for development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(basedir, "hospital.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    ROLES = {
        'admin': 'admin',
        'doctor': 'doctor',
        'nurse': 'nurse',
        'receptionist': 'receptionist'
    }