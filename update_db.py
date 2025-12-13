from app import create_app
from models.database import db

app = create_app()
with app.app_context():
    db.create_all()
    print("Database updated with new schema")
