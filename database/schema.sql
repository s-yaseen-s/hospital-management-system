-- Hospital Management System Database Schema
-- For Microsoft SQL Server - Based on Updated_Database_Schema_Report.pdf

-- Drop tables if they exist (in reverse order of dependencies)
IF OBJECT_ID('Prescription_Medication', 'U') IS NOT NULL DROP TABLE Prescription_Medication;
IF OBJECT_ID('Medication', 'U') IS NOT NULL DROP TABLE Medication;
IF OBJECT_ID('Prescription', 'U') IS NOT NULL DROP TABLE Prescription;
IF OBJECT_ID('Lab_Test', 'U') IS NOT NULL DROP TABLE Lab_Test;
IF OBJECT_ID('Doctor_Updates_Record', 'U') IS NOT NULL DROP TABLE Doctor_Updates_Record;
IF OBJECT_ID('Nurse_Updates_Record', 'U') IS NOT NULL DROP TABLE Nurse_Updates_Record;
IF OBJECT_ID('Medical_Record', 'U') IS NOT NULL DROP TABLE Medical_Record;
IF OBJECT_ID('Patient_Bed_Assignment', 'U') IS NOT NULL DROP TABLE Patient_Bed_Assignment;
IF OBJECT_ID('Room_Bed', 'U') IS NOT NULL DROP TABLE Room_Bed;
IF OBJECT_ID('Payment', 'U') IS NOT NULL DROP TABLE Payment;
IF OBJECT_ID('Invoice', 'U') IS NOT NULL DROP TABLE Invoice;
IF OBJECT_ID('Appointment', 'U') IS NOT NULL DROP TABLE Appointment;
IF OBJECT_ID('Receptionist', 'U') IS NOT NULL DROP TABLE Receptionist;
IF OBJECT_ID('Nurse', 'U') IS NOT NULL DROP TABLE Nurse;
IF OBJECT_ID('Doctor', 'U') IS NOT NULL DROP TABLE Doctor;
IF OBJECT_ID('User_Account', 'U') IS NOT NULL DROP TABLE User_Account;
IF OBJECT_ID('Department', 'U') IS NOT NULL DROP TABLE Department;
IF OBJECT_ID('Patient', 'U') IS NOT NULL DROP TABLE Patient;

-- Create Patient table (from schema PDF)
CREATE TABLE Patient (
    patient_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    date_of_birth DATE,
    age INT,
    previous_conditions VARCHAR(MAX),
    street VARCHAR(100),
    city VARCHAR(100)
);

-- Create Department table (from schema PDF)
CREATE TABLE Department (
    dept_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Create User_Account table (from schema PDF)
CREATE TABLE User_Account (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('doctor', 'nurse', 'receptionist', 'admin'))
);

-- Create Doctor table (from schema PDF)
CREATE TABLE Doctor (
    doc_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100),
    dept_id INT FOREIGN KEY REFERENCES Department(dept_id),
    user_id INT FOREIGN KEY REFERENCES User_Account(user_id)
);

-- Create Nurse table (from schema PDF)
CREATE TABLE Nurse (
    nurse_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_id INT FOREIGN KEY REFERENCES User_Account(user_id)
);

-- Create Receptionist table (from schema PDF)
CREATE TABLE Receptionist (
    rec_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_id INT FOREIGN KEY REFERENCES User_Account(user_id)
);

-- Create Appointment table (from schema PDF)
CREATE TABLE Appointment (
    appt_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100),
    status VARCHAR(50) DEFAULT 'Scheduled',
    date DATETIME NOT NULL,
    patient_id INT FOREIGN KEY REFERENCES Patient(patient_id),
    doc_id INT FOREIGN KEY REFERENCES Doctor(doc_id),
    rec_id INT FOREIGN KEY REFERENCES Receptionist(rec_id)
);

-- Create Medical_Record table (from schema PDF)
CREATE TABLE Medical_Record (
    record_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id INT UNIQUE FOREIGN KEY REFERENCES Patient(patient_id)
);

-- Create Doctor_Updates_Record table (from schema PDF - M:M relationship)
CREATE TABLE Doctor_Updates_Record (
    doc_id INT FOREIGN KEY REFERENCES Doctor(doc_id),
    record_id INT FOREIGN KEY REFERENCES Medical_Record(record_id),
    notes VARCHAR(MAX),
    date DATETIME DEFAULT GETDATE(),
    PRIMARY KEY (doc_id, record_id)
);

-- Create Nurse_Updates_Record table (from schema PDF - M:M relationship)
CREATE TABLE Nurse_Updates_Record (
    nurse_id INT FOREIGN KEY REFERENCES Nurse(nurse_id),
    record_id INT FOREIGN KEY REFERENCES Medical_Record(record_id),
    notes VARCHAR(MAX),
    date DATETIME DEFAULT GETDATE(),
    PRIMARY KEY (nurse_id, record_id)
);

-- Create Prescription table (from schema PDF)
CREATE TABLE Prescription (
    script_id INT IDENTITY(1,1) PRIMARY KEY,
    instructions VARCHAR(MAX),
    patient_id INT FOREIGN KEY REFERENCES Patient(patient_id),
    doc_id INT FOREIGN KEY REFERENCES Doctor(doc_id),
    appt_id INT FOREIGN KEY REFERENCES Appointment(appt_id)
);

-- Create Medication table (from schema PDF)
CREATE TABLE Medication (
    med_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    dosage VARCHAR(100),
    frequency VARCHAR(100),
    instructions VARCHAR(MAX)
);

-- Create Prescription_Medication table (from schema PDF - M:M relationship)
CREATE TABLE Prescription_Medication (
    script_id INT FOREIGN KEY REFERENCES Prescription(script_id),
    med_id INT FOREIGN KEY REFERENCES Medication(med_id),
    PRIMARY KEY (script_id, med_id)
);

-- Create Lab_Test table (from schema PDF)
CREATE TABLE Lab_Test (
    test_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    result VARCHAR(MAX),
    patient_id INT FOREIGN KEY REFERENCES Patient(patient_id),
    doc_id INT FOREIGN KEY REFERENCES Doctor(doc_id)
);

-- Create Invoice table (from schema PDF)
CREATE TABLE Invoice (
    inv_id INT IDENTITY(1,1) PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    patient_id INT FOREIGN KEY REFERENCES Patient(patient_id),
    rec_id INT FOREIGN KEY REFERENCES Receptionist(rec_id),
    date DATETIME DEFAULT GETDATE()
);

-- Create Payment table (from schema PDF)
CREATE TABLE Payment (
    payment_id INT IDENTITY(1,1) PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    date DATETIME DEFAULT GETDATE(),
    inv_id INT FOREIGN KEY REFERENCES Invoice(inv_id)
);

-- Create Room_Bed table (from schema PDF)
CREATE TABLE Room_Bed (
    bed_no INT IDENTITY(1,1) PRIMARY KEY,
    room_no INT NOT NULL,
    status VARCHAR(50) DEFAULT 'Available'
);

-- Create Patient_Bed_Assignment table (from schema PDF)
CREATE TABLE Patient_Bed_Assignment (
    assign_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id INT FOREIGN KEY REFERENCES Patient(patient_id),
    bed_no INT FOREIGN KEY REFERENCES Room_Bed(bed_no),
    start_date DATE DEFAULT GETDATE(),
    end_date DATE
);

-- Create indexes for better performance
CREATE INDEX idx_appointment_date ON Appointment(date);
CREATE INDEX idx_appointment_patient ON Appointment(patient_id);
CREATE INDEX idx_appointment_doctor ON Appointment(doc_id);
CREATE INDEX idx_invoice_patient ON Invoice(patient_id);
CREATE INDEX idx_invoice_status ON Invoice(status);
CREATE INDEX idx_patient_name ON Patient(name);
CREATE INDEX idx_doctor_name ON Doctor(name);
CREATE INDEX idx_prescription_patient ON Prescription(patient_id);
CREATE INDEX idx_prescription_doctor ON Prescription(doc_id);

-- Insert default departments (based on Design-phaseDB.docx)
INSERT INTO Department (name) VALUES 
('Cardiology'),
('Pediatrics'),
('Orthopedics'),
('Neurology'),
('Emergency'),
('General Surgery'),
('Oncology'),
('Radiology');

PRINT 'Database schema created successfully!';