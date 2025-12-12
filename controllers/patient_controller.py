from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.database import db
from models.patient import Patient
from models.appointment import Appointment
from models.medical_record import MedicalRecord
from models.prescription import Prescription
from models.invoice import Invoice
from models.lab_test import LabTest
from utils.decorators import admin_required, doctor_required, nurse_required, receptionist_required

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/')
@login_required
@admin_required
def list_patients():
    patients = Patient.query.all()
    return render_template('patient/list.html', patients=patients)

@patient_bp.route('/<int:patient_id>')
@login_required
def view_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    if current_user.role == 'doctor':
        doctor = Doctor.query.filter_by(user_id=current_user.user_id).first()
        appointments = Appointment.query.filter_by(patient_id=patient_id, doc_id=doctor.doc_id).all()
    else:
        appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    
    medical_record = MedicalRecord.query.filter_by(patient_id=patient_id).first()
    prescriptions = Prescription.query.filter_by(patient_id=patient_id).all()
    invoices = Invoice.query.filter_by(patient_id=patient_id).all()
    lab_tests = LabTest.query.filter_by(patient_id=patient_id).all()
    
    return render_template('patient/view.html', patient=patient, appointments=appointments, medical_record=medical_record, prescriptions=prescriptions, invoices=invoices, lab_tests=lab_tests)

@patient_bp.route('/add', methods=['GET', 'POST'])
@login_required
@receptionist_required
def add_patient():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        date_of_birth = request.form.get('date_of_birth')
        age = request.form.get('age')
        previous_conditions = request.form.get('previous_conditions')
        street = request.form.get('street')
        city = request.form.get('city')
        
        patient = Patient(
            name=name,
            phone=phone,
            date_of_birth=date_of_birth,
            age=age,
            previous_conditions=previous_conditions,
            street=street,
            city=city
        )
        
        db.session.add(patient)
        db.session.commit()
        
        medical_record = MedicalRecord(patient_id=patient.patient_id)
        db.session.add(medical_record)
        db.session.commit()
        
        flash('Patient added successfully!', 'success')
        return redirect(url_for('patient.view_patient', patient_id=patient.patient_id))
    
    return render_template('patient/add.html')

@patient_bp.route('/<int:patient_id>/edit', methods=['GET', 'POST'])
@login_required
@receptionist_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    if request.method == 'POST':
        patient.name = request.form.get('name')
        patient.phone = request.form.get('phone')
        patient.date_of_birth = request.form.get('date_of_birth')
        patient.age = request.form.get('age')
        patient.previous_conditions = request.form.get('previous_conditions')
        patient.street = request.form.get('street')
        patient.city = request.form.get('city')
        
        db.session.commit()
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('patient.view_patient', patient_id=patient.patient_id))
    
    return render_template('patient/edit.html', patient=patient)