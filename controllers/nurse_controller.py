from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.database import db
from models.nurse import Nurse
from models.patient import Patient
from models.room_bed import RoomBed
from models.patient_bed_assignment import PatientBedAssignment
from models.medical_record import MedicalRecord
from datetime import datetime, date
from utils.decorators import nurse_required

nurse_bp = Blueprint('nurse', __name__)

@nurse_bp.route('/dashboard')
@login_required
@nurse_required
def dashboard():
    nurse = Nurse.query.filter_by(user_id=current_user.user_id).first()
    
    patients = Patient.query.all()
    available_beds = RoomBed.query.filter_by(status='Available').count()
    occupied_beds = RoomBed.query.filter_by(status='Occupied').count()
    
    return render_template('nurse/dashboard.html', nurse=nurse, patients=patients, available_beds=available_beds, occupied_beds=occupied_beds)

@nurse_bp.route('/patients')
@login_required
@nurse_required
def patients():
    nurse = Nurse.query.filter_by(user_id=current_user.user_id).first()
    patients = Patient.query.all()
    
    return render_template('nurse/patients.html', patients=patients, nurse=nurse)

@nurse_bp.route('/patient/<int:patient_id>/vitals', methods=['GET', 'POST'])
@login_required
@nurse_required
def patient_vitals(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    medical_record = MedicalRecord.query.filter_by(patient_id=patient_id).first()
    
    if request.method == 'POST':
        notes = request.form.get('notes')
        
        if medical_record:
            nurse = Nurse.query.filter_by(user_id=current_user.user_id).first()
            
            db.session.execute(
                "INSERT INTO nurse_updates_record (nurse_id, record_id, notes, date) VALUES (:nurse_id, :record_id, :notes, :date)",
                {
                    'nurse_id': nurse.nurse_id,
                    'record_id': medical_record.record_id,
                    'notes': notes,
                    'date': datetime.utcnow()
                }
            )
            db.session.commit()
            
            flash('Vitals recorded successfully!', 'success')
            return redirect(url_for('nurse.patients'))
    
    return render_template('nurse/vitals.html', patient=patient)

@nurse_bp.route('/beds')
@login_required
@nurse_required
def beds():
    beds = RoomBed.query.all()
    assignments = PatientBedAssignment.query.filter(PatientBedAssignment.end_date == None).all()
    
    return render_template('nurse/beds.html', beds=beds, assignments=assignments)

@nurse_bp.route('/bed/assign', methods=['POST'])
@login_required
@nurse_required
def assign_bed():
    patient_id = request.form.get('patient_id')
    bed_no = request.form.get('bed_no')
    
    bed = RoomBed.query.get(bed_no)
    if bed and bed.status == 'Available':
        assignment = PatientBedAssignment(
            patient_id=patient_id,
            bed_no=bed_no,
            start_date=date.today()
        )
        
        bed.status = 'Occupied'
        
        db.session.add(assignment)
        db.session.commit()
        
        flash('Bed assigned successfully!', 'success')
    else:
        flash('Bed is not available!', 'danger')
    
    return redirect(url_for('nurse.beds'))

@nurse_bp.route('/bed/<int:bed_no>/vacate', methods=['POST'])
@login_required
@nurse_required
def vacate_bed(bed_no):
    assignment = PatientBedAssignment.query.filter_by(bed_no=bed_no, end_date=None).first()
    
    if assignment:
        assignment.end_date = date.today()
        
        bed = RoomBed.query.get(bed_no)
        bed.status = 'Available'
        
        db.session.commit()
        flash('Bed vacated successfully!', 'success')
    else:
        flash('No active assignment found for this bed!', 'danger')
    
    return redirect(url_for('nurse.beds'))