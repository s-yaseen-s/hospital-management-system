from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.database import db
from models.user import User
from models.doctor import Doctor
from models.nurse import Nurse
from models.receptionist import Receptionist
from models.department import Department
from models.patient import Patient
from models.appointment import Appointment
from models.invoice import Invoice
from datetime import datetime, date
from utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    total_appointments = Appointment.query.count()
    total_invoices = Invoice.query.count()
    
    today = date.today()
    today_appointments = Appointment.query.filter_by(date=today).count()
    
    pending_invoices = Invoice.query.filter_by(status='Pending').count()
    paid_invoices = Invoice.query.filter_by(status='Paid').count()
    
    return render_template('admin/dashboard.html', 
                         total_patients=total_patients,
                         total_doctors=total_doctors,
                         total_appointments=total_appointments,
                         total_invoices=total_invoices,
                         today_appointments=today_appointments,
                         pending_invoices=pending_invoices,
                         paid_invoices=paid_invoices)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    doctors = Doctor.query.all()
    nurses = Nurse.query.all()
    receptionists = Receptionist.query.all()
    
    return render_template('admin/users.html', 
                         users=users, 
                         doctors=doctors, 
                         nurses=nurses, 
                         receptionists=receptionists)

@admin_bp.route('/user/add', methods=['POST'])
@login_required
@admin_required
def add_user():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    name = request.form.get('name')
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Username already exists!', 'danger')
        return redirect(url_for('admin.users'))
    
    user = User(username=username, role=role)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    if role == 'doctor':
        specialty = request.form.get('specialty')
        dept_id = request.form.get('dept_id')
        
        doctor = Doctor(
            name=name,
            specialty=specialty,
            dept_id=dept_id,
            user_id=user.user_id
        )
        db.session.add(doctor)
    
    elif role == 'nurse':
        nurse = Nurse(
            name=name,
            user_id=user.user_id
        )
        db.session.add(nurse)
    
    elif role == 'receptionist':
        receptionist = Receptionist(
            name=name,
            user_id=user.user_id
        )
        db.session.add(receptionist)
    
    db.session.commit()
    flash('User added successfully!', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    
    if user:
        if user.role == 'doctor':
            Doctor.query.filter_by(user_id=user_id).delete()
        elif user.role == 'nurse':
            Nurse.query.filter_by(user_id=user_id).delete()
        elif user.role == 'receptionist':
            Receptionist.query.filter_by(user_id=user_id).delete()
        
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    else:
        flash('User not found!', 'danger')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/departments')
@login_required
@admin_required
def departments():
    departments = Department.query.all()
    return render_template('admin/departments.html', departments=departments)

@admin_bp.route('/department/add', methods=['POST'])
@login_required
@admin_required
def add_department():
    name = request.form.get('name')
    
    department = Department(name=name)
    db.session.add(department)
    db.session.commit()
    
    flash('Department added successfully!', 'success')
    return redirect(url_for('admin.departments'))

@admin_bp.route('/department/<int:dept_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_department_status(dept_id):
    department = Department.query.get_or_404(dept_id)
    
    if department.status == 'Active':
        department.status = 'Inactive'
        flash(f'Department "{department.name}" deactivated successfully!', 'info')
    else:
        department.status = 'Active'
        flash(f'Department "{department.name}" activated successfully!', 'success')
    
    db.session.commit()
    return redirect(url_for('admin.departments'))

@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    start_date = request.args.get('start_date', date.today().replace(day=1))
    end_date = request.args.get('end_date', date.today())
    
    appointments = Appointment.query.filter(
        Appointment.date.between(start_date, end_date)
    ).all()
    
    invoices = Invoice.query.filter(
        Invoice.date.between(start_date, end_date)
    ).all()
    
    total_revenue = sum(inv.amount for inv in invoices if inv.status == 'Paid')
    
    doctors = Doctor.query.all()
    doctor_stats = []
    for doctor in doctors:
        doc_appointments = Appointment.query.filter_by(doc_id=doctor.doc_id).count()
        doctor_stats.append({
            'doctor': doctor,
            'appointments': doc_appointments
        })
    
    return render_template('admin/reports.html', 
                         appointments=appointments,
                         invoices=invoices,
                         total_revenue=total_revenue,
                         doctor_stats=doctor_stats,
                         start_date=start_date,
                         end_date=end_date)