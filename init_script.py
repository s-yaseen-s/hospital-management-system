import os
from models.database import db
from app import create_app

def init_db():
    # Remove existing database file if it exists
    db_path = os.path.join(os.path.dirname(__file__), 'hospital.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Removed existing database file.")
    
    # Create app and initialize database
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Created database tables.")
        
        # Add some initial data
        from models.user import User
        from models.doctor import Doctor
        from models.department import Department
        from models.patient import Patient
        
        # Add default admin user
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Add a test department
        dept = Department(name='Cardiology')
        db.session.add(dept)
        
        # Add a test doctor
        doctor = Doctor(name='Dr. Smith', specialty='Cardiologist', dept_id=1)
        db.session.add(doctor)
        
        # Add a test patient
        from datetime import date
        patient = Patient(
            name='John Doe',
            phone='123-456-7890',
            date_of_birth=date(1980, 1, 1),
            age=43,
            street='123 Main St',
            city='New York'
        )
        db.session.add(patient)
        
        # Commit changes
        db.session.commit()
        print("Added initial data to the database.")
        
        print("\nDatabase initialization completed successfully!")
        print(f"Admin login: username='admin', password='admin123'")

if __name__ == '__main__':
    init_db()
