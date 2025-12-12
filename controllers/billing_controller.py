from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.database import db
from models.invoice import Invoice
from models.payment import Payment
from models.patient import Patient
from models.receptionist import Receptionist
from datetime import datetime
from utils.decorators import receptionist_required, admin_required

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/')
@login_required
def invoices():
    if current_user.role in ['receptionist', 'admin']:
        invoices = Invoice.query.order_by(Invoice.date.desc()).all()
        patients = Patient.query.all()
        
        return render_template('receptionist/invoices.html', invoices=invoices, patients=patients)
    else:
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

@billing_bp.route('/create', methods=['POST'])
@login_required
@receptionist_required
def create_invoice():
    patient_id = request.form.get('patient_id')
    amount = request.form.get('amount')
    description = request.form.get('description', '')
    
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
    return redirect(url_for('billing.invoices'))

@billing_bp.route('/<int:inv_id>')
@login_required
def view_invoice(inv_id):
    invoice = Invoice.query.get_or_404(inv_id)
    
    if current_user.role not in ['receptionist', 'admin']:
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    payments = Payment.query.filter_by(inv_id=inv_id).all()
    total_paid = sum(p.amount for p in payments)
    balance = invoice.amount - total_paid
    
    return render_template('receptionist/invoice_view.html', 
                         invoice=invoice, 
                         payments=payments,
                         total_paid=total_paid,
                         balance=balance)

@billing_bp.route('/<int:inv_id>/payment', methods=['POST'])
@login_required
@receptionist_required
def add_payment(inv_id):
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
        else:
            invoice.status = 'Partial'
    
    db.session.add(payment)
    db.session.commit()
    
    flash('Payment recorded successfully!', 'success')
    return redirect(url_for('billing.view_invoice', inv_id=inv_id))

@billing_bp.route('/report')
@login_required
@admin_required
def billing_report():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    query = Invoice.query
    
    if start_date:
        query = query.filter(Invoice.date >= start_date)
    if end_date:
        query = query.filter(Invoice.date <= end_date)
    
    invoices = query.order_by(Invoice.date.desc()).all()
    
    total_amount = sum(inv.amount for inv in invoices)
    paid_amount = sum(inv.amount for inv in invoices if inv.status == 'Paid')
    pending_amount = sum(inv.amount for inv in invoices if inv.status == 'Pending')
    
    return render_template('admin/billing_report.html',
                         invoices=invoices,
                         total_amount=total_amount,
                         paid_amount=paid_amount,
                         pending_amount=pending_amount,
                         start_date=start_date,
                         end_date=end_date)