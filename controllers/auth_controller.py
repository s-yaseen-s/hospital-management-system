from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from models.database import db
from models.doctor import Doctor
from models.nurse import Nurse
from models.receptionist import Receptionist

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        user = User.query.filter_by(username=username, role=role).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            
            if role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif role == 'doctor':
                return redirect(url_for('doctor.dashboard'))
            elif role == 'nurse':
                return redirect(url_for('nurse.dashboard'))
            elif role == 'receptionist':
                return redirect(url_for('receptionist.dashboard'))
        else:
            flash('Invalid username, password, or role', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('auth.login'))