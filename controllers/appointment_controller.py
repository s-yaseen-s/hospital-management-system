from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.database import db
from models.appointment import Appointment
from models.patient import Patient
from models.doctor import Doctor
from models.receptionist import Receptionist
from datetime import datetime, date
from utils.decorators import doctor_required, receptionist_required

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/')
@login_required
def schedule():
    if current_user.role == 'doctor':
        doctor = Doctor.query.filter_by(user_id=current_user.user_id).first()
        appointments = Appointment.query.filter_by(doc_id=doctor.doc_id).order_by(Appointment.date).all()
        return render_template('appointments/schedule.html', appointments=appointments, doctor=doctor)
    
    elif current_user.role == 'receptionist':
        appointments = Appointment.query.order_by(Appointment.date).all()
        patients = Patient.query.all()
        doctors = Doctor.query.all()
        return render_template('appointments/schedule.html', appointments=appointments, patients=patients, doctors=doctors)
    
    else:
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

@appointment_bp.route('/<int:appt_id>')
@login_required
def view_appointment(appt_id):
    appointment = Appointment.query.get_or_404(appt_id)
    
    if current_user.role == 'doctor':
        doctor = Doctor.query.filter_by(user_id=current_user.user_id).first()
        if appointment.doc_id != doctor.doc_id:
            flash('Access denied.', 'danger')
            return redirect(url_for('index'))
    
    return render_template('appointments/view.html', appointment=appointment)

@appointment_bp.route('/add', methods=['GET', 'POST'])
@login_required
@receptionist_required
def add_appointment():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        doc_id = request.form.get('doc_id')
        appointment_date = request.form.get('date')
        name = request.form.get('name')
        
        receptionist = Receptionist.query.filter_by(user_id=current_user.user_id).first()
        
        # Convert string date to datetime object
        if appointment_date:
            try:
                # Handle different date formats
                if 'T' in appointment_date:
                    # Format: 2025-12-13T18:51
                    appointment_datetime = datetime.strptime(appointment_date, '%Y-%m-%dT%H:%M')
                else:
                    # Format: 2025-12-13
                    appointment_datetime = datetime.strptime(appointment_date, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format', 'error')
                return redirect(url_for('appointment.schedule'))
        else:
            flash('Date is required', 'error')
            return redirect(url_for('appointment.schedule'))
        
        appointment = Appointment(
            name=name,
            date=appointment_datetime,
            patient_id=patient_id,
            doc_id=doc_id,
            rec_id=receptionist.rec_id
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        flash('Appointment scheduled successfully!', 'success')
        return redirect(url_for('appointment.schedule'))
    
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('appointments/add.html', patients=patients, doctors=doctors)

@appointment_bp.route('/<int:appt_id>/update_status', methods=['POST'])
@login_required
@doctor_required
def update_status(appt_id):
    appointment = Appointment.query.get_or_404(appt_id)
    status = request.form.get('status')
    
    doctor = Doctor.query.filter_by(user_id=current_user.user_id).first()
    if appointment.doc_id != doctor.doc_id:
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    appointment.status = status
    db.session.commit()
    
    flash('Appointment status updated successfully!', 'success')
    return redirect(url_for('appointment.view_appointment', appt_id=appt_id))

@appointment_bp.route('/today')
@login_required
def today_appointments():
    today = date.today()
    
    if current_user.role == 'doctor':
        doctor = Doctor.query.filter_by(user_id=current_user.user_id).first()
        appointments = Appointment.query.filter_by(doc_id=doctor.doc_id, date=today).all()
    elif current_user.role == 'receptionist':
        appointments = Appointment.query.filter_by(date=today).all()
    else:
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    return render_template('appointments/schedule.html', appointments=appointments, today=today)