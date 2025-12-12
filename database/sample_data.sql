INSERT INTO User_Account (username, password, role) VALUES
('admin', 'pbkdf2:sha256:260000$N73Nk0xI3V4lR6jW$3a9f8c7b6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f', 'admin'),
('drsmith', 'pbkdf2:sha256:260000$N73Nk0xI3V4lR6jW$3a9f8c7b6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f', 'doctor'),
('drjones', 'pbkdf2:sha256:260000$N73Nk0xI3V4lR6jW$3a9f8c7b6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f', 'doctor'),
('drbrown', 'pbkdf2:sha256:260000$N73Nk0xI3V4lR6jW$3a9f8c7b6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f', 'doctor'),
('nursejones', 'pbkdf2:sha256:260000$N73Nk0xI3V4lR6jW$3a9f8c7b6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f', 'nurse'),
('nursebrown', 'pbkdf2:sha256:260000$N73Nk0xI3V4lR6jW$3a9f8c7b6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f', 'nurse'),
('reception', 'pbkdf2:sha256:260000$N73Nk0xI3V4lR6jW$3a9f8c7b6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f', 'receptionist');

INSERT INTO Doctor (name, specialty, dept_id, user_id) VALUES
('Dr. John Smith', 'Cardiologist', 1, 2),
('Dr. Sarah Jones', 'Pediatrician', 2, 3),
('Dr. Robert Brown', 'Orthopedic Surgeon', 3, 4);

INSERT INTO Nurse (name, user_id) VALUES
('Nurse Alice Jones', 5),
('Nurse Bob Brown', 6);

INSERT INTO Receptionist (name, user_id) VALUES
('Receptionist Mary Wilson', 7);

INSERT INTO Patient (name, phone, date_of_birth, age, previous_conditions, street, city) VALUES
('John Doe', '555-0101', '1980-05-15', 43, 'Hypertension, Diabetes', '123 Main St', 'New York'),
('Jane Smith', '555-0102', '1992-08-22', 31, 'Asthma', '456 Oak Ave', 'New York'),
('Robert Johnson', '555-0103', '1975-12-10', 48, 'None', '789 Pine Rd', 'Brooklyn'),
('Emily Davis', '555-0104', '2005-03-30', 18, 'Allergies', '321 Elm St', 'Queens'),
('Michael Wilson', '555-0105', '1988-07-14', 35, 'High Cholesterol', '654 Maple Dr', 'Bronx'),
('Sarah Miller', '555-0106', '1995-11-25', 28, 'Migraine', '987 Birch Ln', 'Manhattan'),
('David Taylor', '555-0107', '1965-02-14', 58, 'Arthritis, Hypertension', '741 Cedar Blvd', 'Staten Island'),
('Lisa Anderson', '555-0108', '1982-09-03', 41, 'Diabetes', '852 Spruce Way', 'New York');

INSERT INTO Appointment (name, status, date, patient_id, doc_id, rec_id) VALUES
('Regular Checkup', 'Completed', '2024-01-15 09:00:00', 1, 1, 1),
('Follow-up Visit', 'Scheduled', '2024-01-20 10:30:00', 2, 2, 1),
('Cardiology Consultation', 'Scheduled', '2024-01-18 14:00:00', 3, 1, 1),
('Pediatric Checkup', 'Completed', '2024-01-10 11:00:00', 4, 2, 1),
('Orthopedic Consultation', 'Cancelled', '2024-01-12 16:00:00', 5, 3, 1),
('Annual Physical', 'Scheduled', '2024-01-22 13:30:00', 6, 1, 1),
('Post-surgery Follow-up', 'Scheduled', '2024-01-19 15:00:00', 7, 3, 1),
('Emergency Visit', 'Completed', '2024-01-14 17:00:00', 8, 2, 1);

INSERT INTO Medical_Record (patient_id) VALUES (1), (2), (3), (4), (5), (6), (7), (8);

INSERT INTO Doctor_Updates_Record (doc_id, record_id, notes, date) VALUES
(1, 1, 'Patient shows improved blood pressure. Continue current medication.', '2024-01-15 10:00:00'),
(1, 3, 'Patient complains of chest pain. Ordered ECG test.', '2024-01-18 14:30:00'),
(2, 2, 'Asthma well-controlled with current inhaler. No changes needed.', '2024-01-20 11:00:00'),
(2, 4, 'Allergy symptoms seasonal. Prescribed antihistamines.', '2024-01-10 12:00:00'),
(3, 7, 'Post-surgery recovery progressing well. Physical therapy recommended.', '2024-01-19 15:30:00');

INSERT INTO Nurse_Updates_Record (nurse_id, record_id, notes, date) VALUES
(1, 1, 'BP: 130/85, Pulse: 72, Temp: 98.6°F', '2024-01-15 09:30:00'),
(1, 2, 'BP: 120/80, Pulse: 68, Temp: 98.4°F', '2024-01-20 10:45:00'),
(2, 3, 'BP: 140/90, Pulse: 76, Temp: 99.1°F', '2024-01-18 14:15:00'),
(2, 4, 'BP: 110/70, Pulse: 70, Temp: 98.2°F', '2024-01-10 11:30:00');

INSERT INTO Medication (name, dosage, frequency, instructions) VALUES
('Lisinopril', '10mg', 'Once daily', 'Take with water in the morning'),
('Metformin', '500mg', 'Twice daily', 'Take with meals'),
('Albuterol', '90mcg', 'As needed', 'Inhale 1-2 puffs every 4-6 hours'),
('Loratadine', '10mg', 'Once daily', 'Take in the morning'),
('Ibuprofen', '400mg', 'Every 6 hours', 'Take with food'),
('Amoxicillin', '500mg', 'Three times daily', 'Complete full course'),
('Atorvastatin', '20mg', 'Once daily', 'Take at bedtime'),
('Levothyroxine', '50mcg', 'Once daily', 'Take on empty stomach');

INSERT INTO Prescription (instructions, patient_id, doc_id, appt_id) VALUES
('Take Lisinopril daily for blood pressure control.', 1, 1, 1),
('Use Albuterol inhaler as needed for asthma symptoms.', 2, 2, 2),
('Take Loratadine daily during allergy season.', 4, 2, 4),
('Take Ibuprofen for pain management as needed.', 7, 3, 7),
('Complete full course of Amoxicillin for infection.', 8, 2, 8);

INSERT INTO Prescription_Medication (script_id, med_id) VALUES
(1, 1), -- Prescription 1 includes Lisinopril
(1, 2), -- Prescription 1 also includes Metformin
(2, 3), -- Prescription 2 includes Albuterol
(3, 4), -- Prescription 3 includes Loratadine
(4, 5), -- Prescription 4 includes Ibuprofen
(5, 6); -- Prescription 5 includes Amoxicillin

INSERT INTO Lab_Test (name, result, patient_id, doc_id) VALUES
('Complete Blood Count', 'Normal ranges', 1, 1),
('ECG', 'Normal sinus rhythm', 3, 1),
('Blood Glucose', 'Fasting: 95 mg/dL', 1, 1),
('Allergy Panel', 'Positive for pollen, dust mites', 4, 2),
('X-Ray Right Knee', 'Healing fracture, no displacement', 7, 3);

INSERT INTO Invoice (amount, status, patient_id, rec_id, date) VALUES
(150.00, 'Paid', 1, 1, '2024-01-15 11:00:00'),
(200.00, 'Pending', 2, 1, '2024-01-20 11:30:00'),
(300.00, 'Pending', 3, 1, '2024-01-18 15:00:00'),
(100.00, 'Paid', 4, 1, '2024-01-10 12:30:00'),
(500.00, 'Pending', 7, 1, '2024-01-19 16:00:00');

INSERT INTO Payment (amount, date, inv_id) VALUES
(150.00, '2024-01-15 12:00:00', 1),
(100.00, '2024-01-10 13:00:00', 4);

INSERT INTO Room_Bed (room_no, status) VALUES
(101, 'Available'),
(101, 'Occupied'),
(102, 'Available'),
(102, 'Available'),
(103, 'Occupied'),
(103, 'Available'),
(201, 'Available'),
(201, 'Available'),
(202, 'Occupied'),
(202, 'Available');

INSERT INTO Patient_Bed_Assignment (patient_id, bed_no, start_date, end_date) VALUES
(1, 2, '2024-01-14', '2024-01-16'),
(7, 5, '2024-01-18', NULL),
(8, 9, '2024-01-14', '2024-01-15');

PRINT 'Sample data inserted successfully!';
PRINT 'Total records inserted:'
PRINT '  - Users: ' + CAST((SELECT COUNT(*) FROM User_Account) AS VARCHAR)
PRINT '  - Patients: ' + CAST((SELECT COUNT(*) FROM Patient) AS VARCHAR)
PRINT '  - Doctors: ' + CAST((SELECT COUNT(*) FROM Doctor) AS VARCHAR)
PRINT '  - Appointments: ' + CAST((SELECT COUNT(*) FROM Appointment) AS VARCHAR)
PRINT '  - Invoices: ' + CAST((SELECT COUNT(*) FROM Invoice) AS VARCHAR)