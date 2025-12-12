from models.database import db
from models.patient import Patient
from models.doctor import Doctor
from models.doctor_updates_record import DoctorUpdatesRecord
from models.nurse import Nurse
from models.nurse_updates_record import NurseUpdatesRecord
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

# Association table for many-to-many relationship between prescriptions and medications
prescription_medication = db.Table('prescription_medication',
    db.Column('script_id', db.Integer, db.ForeignKey('prescription.script_id'), primary_key=True),
    db.Column('med_id', db.Integer, db.ForeignKey('medication.med_id'), primary_key=True)
)
