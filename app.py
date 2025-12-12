from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user
from config import Config
from models.database import db
from models.user import User
import controllers

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Force SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from controllers.auth_controller import auth_bp
    from controllers.patient_controller import patient_bp
    from controllers.doctor_controller import doctor_bp
    from controllers.nurse_controller import nurse_bp
    from controllers.receptionist_controller import receptionist_bp
    from controllers.admin_controller import admin_bp
    from controllers.appointment_controller import appointment_bp
    from controllers.billing_controller import billing_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(doctor_bp, url_prefix='/doctor')
    app.register_blueprint(nurse_bp, url_prefix='/nurse')
    app.register_blueprint(receptionist_bp, url_prefix='/receptionist')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(appointment_bp, url_prefix='/appointments')
    app.register_blueprint(billing_bp, url_prefix='/billing')
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('common/error.html', message='Page not found'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('common/error.html', message='Internal server error'), 500
    
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            role = current_user.role
            if role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif role == 'doctor':
                return redirect(url_for('doctor.dashboard'))
            elif role == 'nurse':
                return redirect(url_for('nurse.dashboard'))
            elif role == 'receptionist':
                return redirect(url_for('receptionist.dashboard'))
        return redirect(url_for('auth.login'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)