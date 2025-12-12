import sqlite3
import os
from models.database import db
from models.user import User
from app import create_app

def init_database():
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Create default admin user if not exists
        admin = User.query.filter_by(username='admin', role='admin').first()
        if not admin:
            admin = User(username='admin', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Create other default users
            users_data = [
                {'username': 'drsmith', 'role': 'doctor', 'password': 'password123'},
                {'username': 'drjones', 'role': 'doctor', 'password': 'password123'},
                {'username': 'nursejones', 'role': 'nurse', 'password': 'password123'},
                {'username': 'nursebrown', 'role': 'nurse', 'password': 'password123'},
                {'username': 'reception', 'role': 'receptionist', 'password': 'password123'},
            ]
            
            for user_data in users_data:
                user = User(username=user_data['username'], role=user_data['role'])
                user.set_password(user_data['password'])
                db.session.add(user)
            
            db.session.commit()
            print("Default users created successfully!")
        
        print("Database initialization completed!")

if __name__ == '__main__':
    init_database()