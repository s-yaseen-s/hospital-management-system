from models.database import db
from models.patient import Patient
from models.doctor import Doctor
from models.nurse import Nurse
from models.receptionist import Receptionist
from models.department import Department
from models.appointment import Appointment
from models.medical_record import MedicalRecord
from models.prescription import Prescription
from models.medication import Medication
from models.lab_test import LabTest
from models.invoice import Invoice
from models.payment import Payment
from models.room_bed import RoomBed
from models.patient_bed_assignment import PatientBedAssignment
from models.user import User

prescription_medication = db.Table('prescription_medication',
    db.Column('script_id', db.Integer, db.ForeignKey('prescription.script_id'), primary_key=True),
    db.Column('med_id', db.Integer, db.ForeignKey('medication.med_id'), primary_key=True)
)

doctor_updates_record = db.Table('doctor_updates_record',
    db.Column('doc_id', db.Integer, db.ForeignKey('doctor.doc_id'), primary_key=True),
    db.Column('record_id', db.Integer, db.ForeignKey('medical_record.record_id'), primary_key=True),
    db.Column('notes', db.Text),
    db.Column('date', db.DateTime)
)

nurse_updates_record = db.Table('nurse_updates_record',
    db.Column('nurse_id', db.Integer, db.ForeignKey('nurse.nurse_id'), primary_key=True),
    db.Column('record_id', db.Integer, db.ForeignKey('medical_record.record_id'), primary_key=True),
    db.Column('notes', db.Text),
    db.Column('date', db.DateTime)
)