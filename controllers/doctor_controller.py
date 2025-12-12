from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.database import db
from models.doctor import Doctor
from models.patient import Patient
from models.appointment import Appointment
from models.prescription import Prescription
from models.medical_record import MedicalRecord
from models.lab_test import LabTest
from datetime import datetime, date
from utils.decorators import doctor_required

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/dashboard')
@login_required
@doctor_required
def dashboard():
    doctor = Doctor.query.filter_by(user_id=current_user.user_id).first()
    
    today = date.today()
    appointments = Appointment.query.filter_by(doc_id=doctor.doc_id, date=today).all()
    
    recent_prescriptions = Prescription.query.filter_by(doc_id=doctor.doc_id).order_by(Prescription.script_id.desc()).limit(5).all()
    
    return render_template('doctor/dashboard.html', doctor=doctor, appointments=appointments, prescriptions=recent_prescriptions)

@doctor_bp.route('/appointments')
@login_required
@doctor_required
def appointments():
    doctor = Doctor.query.filter_by(user_id=current_user.user_id).first()
    appointments = Appointment.query.filter_by(doc_id=doctor.doc_id).order_by(Appointment.date.desc()).all()
    
    return render_template('doctor/appointments.html', appointments=appointments, doctor=doctor)

@doctor_bp.route('/patients')
@login_required
@doctor_required
def patients():
    doctor = Doctor.query.filter_by(user_id=current_user.user_id).first()
    
    appointments = Appointment.query.filter_by(doc_id=doctor.doc_id).all()
    patient_ids = set([app.patient_id for app in appointments])
    patients = Patient.query.filter(Patient.patient_id.in_(patient_ids)).all()
    
    return render_template('doctor/patients.html', patients=patients, doctor=doctor)

@doctor_bp.route('/patient/<int:patient_id>')
@login_required
@doctor_required
def view_patient(patient_id):
    doctor = Doctor.query.filter_by(user_id=current_user.user_id).first()
    patient = Patient.query.get_or_404(patient_id)
    medical_record = MedicalRecord.query.filter_by(patient_id=patient_id).first()
    
    appointments = Appointment.query.filter_by(patient_id=patient_id, doc_id=doctor.doc_id).all()
    prescriptions = Prescription.query.filter_by(patient_id=patient_id, doc_id=doctor.doc_id).all()
    lab_tests = LabTest.query.filter_by(patient_id=patient_id, doc_id=doctor.doc_id).all()
    
    return render_template('doctor/medical_record.html', patient=patient, medical_record=medical_record, appointments=appointments, prescriptions=prescriptions, lab_tests=lab_tests, doctor=doctor)

@doctor_bp.route('/prescription/new', methods=['GET', 'POST'])
@login_required
@doctor_required
def new_prescription():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        instructions = request.form.get('instructions')
        
        doctor = Doctor.query.filter_by(user_id=current_user.user_id).first()
        
        prescription = Prescription(
            instructions=instructions,
            patient_id=patient_id,
            doc_id=doctor.doc_id,
            appt_id=None
        )
        
        db.session.add(prescription)
        db.session.commit()
        
        flash('Prescription created successfully!', 'success')
        return redirect(url_for('doctor.dashboard'))
    
    patients = Patient.query.all()
    return render_template('doctor/prescription.html', patients=patients)