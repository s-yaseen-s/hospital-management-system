from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.database import db
from models.receptionist import Receptionist
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.invoice import Invoice
from models.payment import Payment
from datetime import datetime, date
from utils.decorators import receptionist_required

receptionist_bp = Blueprint('receptionist', __name__)

@receptionist_bp.route('/dashboard')
@login_required
@receptionist_required
def dashboard():
    receptionist = Receptionist.query.filter_by(user_id=current_user.user_id).first()
    
    today = date.today()
    appointments = Appointment.query.filter_by(date=today).all()
    
    pending_invoices = Invoice.query.filter_by(status='Pending').count()
    total_invoices = Invoice.query.count()
    
    return render_template('receptionist/dashboard.html', receptionist=receptionist, appointments=appointments, pending_invoices=pending_invoices, total_invoices=total_invoices)

@receptionist_bp.route('/appointments')
@login_required
@receptionist_required
def appointments():
    appointments = Appointment.query.order_by(Appointment.date.desc()).all()
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    
    return render_template('receptionist/appointments.html', appointments=appointments, patients=patients, doctors=doctors)

@receptionist_bp.route('/appointment/add', methods=['POST'])
@login_required
@receptionist_required
def add_appointment():
    patient_id = request.form.get('patient_id')
    doc_id = request.form.get('doc_id')
    appointment_date = request.form.get('date')
    name = request.form.get('name')
    
    receptionist = Receptionist.query.filter_by(user_id=current_user.user_id).first()
    
    appointment = Appointment(
        name=name,
        date=appointment_date,
        patient_id=patient_id,
        doc_id=doc_id,
        rec_id=receptionist.rec_id
    )
    
    db.session.add(appointment)
    db.session.commit()
    
    flash('Appointment scheduled successfully!', 'success')
    return redirect(url_for('receptionist.appointments'))

@receptionist_bp.route('/appointment/<int:appt_id>/cancel', methods=['POST'])
@login_required
@receptionist_required
def cancel_appointment(appt_id):
    appointment = Appointment.query.get(appt_id)
    
    if appointment:
        appointment.status = 'Cancelled'
        db.session.commit()
        flash('Appointment cancelled successfully!', 'success')
    else:
        flash('Appointment not found!', 'danger')
    
    return redirect(url_for('receptionist.appointments'))

@receptionist_bp.route('/billing')
@login_required
@receptionist_required
def billing():
    invoices = Invoice.query.order_by(Invoice.date.desc()).all()
    patients = Patient.query.all()
    
    return render_template('receptionist/billing.html', invoices=invoices, patients=patients)

@receptionist_bp.route('/invoice/add', methods=['POST'])
@login_required
@receptionist_required
def add_invoice():
    patient_id = request.form.get('patient_id')
    amount = request.form.get('amount')
    description = request.form.get('description')
    
    receptionist = Receptionist.query.filter_by(user_id=current_user.user_id).first()
    
    invoice = Invoice(
        amount=amount,
        patient_id=patient_id,
        rec_id=receptionist.rec_id,
        date=datetime.utcnow()
    )
    
    db.session.add(invoice)
    db.session.commit()
    
    flash('Invoice created successfully!', 'success')
    return redirect(url_for('receptionist.billing'))

@receptionist_bp.route('/invoice/<int:inv_id>/pay', methods=['POST'])
@login_required
@receptionist_required
def pay_invoice(inv_id):
    amount = request.form.get('amount')
    
    payment = Payment(
        amount=amount,
        inv_id=inv_id,
        date=datetime.utcnow()
    )
    
    invoice = Invoice.query.get(inv_id)
    if invoice:
        total_paid = sum(p.amount for p in invoice.payments) + float(amount)
        if total_paid >= invoice.amount:
            invoice.status = 'Paid'
    
    db.session.add(payment)
    db.session.commit()
    
    flash('Payment recorded successfully!', 'success')
    return redirect(url_for('receptionist.billing'))

@receptionist_bp.route('/admission')
@login_required
@receptionist_required
def admission():
    patients = Patient.query.all()
    return render_template('receptionist/admission.html', patients=patients)