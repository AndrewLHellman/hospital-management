INSERT INTO DEPARTMENT (deptID, name, location, headDoctor) VALUES
('DEPT001', 'Cardiology', 'Building A, Floor 2', NULL),
('DEPT002', 'Neurology', 'Building B, Floor 1', NULL),
('DEPT003', 'Pediatrics', 'Building C, Floor 3', NULL),
('DEPT004', 'Oncology', 'Building A, Floor 3', NULL),
('DEPT005', 'Emergency', 'Building D, Ground Floor', NULL);

INSERT INTO ROOM (roomNumber, type, capacity, status, departmentID) VALUES
('RM101', 'Examination', 2, 'Available', 'DEPT001'),
('RM102', 'Surgery', 10, 'Available', 'DEPT001'),
('RM201', 'Patient Room', 4, 'Occupied', 'DEPT002'),
('RM301', 'ICU', 1, 'Available', 'DEPT003'),
('RM401', 'Treatment', 3, 'Maintenance', 'DEPT004'),
('RM501', 'Emergency Bay', 6, 'Available', 'DEPT005');

INSERT INTO DOCTOR (doctorID, name, specialization, office_phone, mobile_phone, email, pager_number, emergency_contact, departmentID) VALUES
('DOC001', 'John Smith', 'Cardiologist', '555-1001', '555-2001', 'jsmith@hospital.org', '555-3001', 'Jane Smith 555-4001', 'DEPT001'),
('DOC002', 'Emily Johnson', 'Neurologist', '555-1002', '555-2002', 'ejohnson@hospital.org', '555-3002', 'Michael Johnson 555-4002', 'DEPT002'),
('DOC003', 'Robert Chen', 'Pediatrician', '555-1003', '555-2003', 'rchen@hospital.org', '555-3003', 'Lisa Chen 555-4003', 'DEPT003'),
('DOC004', 'Sarah Williams', 'Oncologist', '555-1004', '555-2004', 'swilliams@hospital.org', '555-3004', 'David Williams 555-4004', 'DEPT004'),
('DOC005', 'James Brown', 'Emergency Medicine', '555-1005', '555-2005', 'jbrown@hospital.org', '555-3005', 'Mary Brown 555-4005', 'DEPT005');
('DOC006', 'Michelle Lee', 'Dermatologist', '555-1006', '555-2006', 'mlee@hospital.org', '555-3006', 'Richard Lee 555-4006', 'DEPT004');

UPDATE DEPARTMENT SET headDoctor = 'DOC001' WHERE deptID = 'DEPT001';
UPDATE DEPARTMENT SET headDoctor = 'DOC002' WHERE deptID = 'DEPT002';
UPDATE DEPARTMENT SET headDoctor = 'DOC003' WHERE deptID = 'DEPT003';
UPDATE DEPARTMENT SET headDoctor = 'DOC004' WHERE deptID = 'DEPT004';
UPDATE DEPARTMENT SET headDoctor = 'DOC005' WHERE deptID = 'DEPT005';

INSERT INTO PATIENT (patientID, name, dateOfBirth, street_number, street_name, apt_number, city, state, zip_code, country, insuranceInfo) VALUES
('PAT001', 'Thomas Anderson', '1975-05-15', '123', 'Main St', '4B', 'Springfield', 'IL', '62701', 'USA', 'BlueCross #12345678'),
('PAT002', 'Maria Garcia', '1988-11-22', '456', 'Oak Ave', NULL, 'Springfield', 'IL', '62702', 'USA', 'Aetna #87654321'),
('PAT003', 'Robert Johnson', '1965-03-10', '789', 'Pine Rd', '102', 'Springfield', 'IL', '62703', 'USA', 'Medicare #ABC123'),
('PAT004', 'Jennifer Lee', '1992-07-30', '101', 'Cedar Ln', NULL, 'Springfield', 'IL', '62704', 'USA', 'United #XYZ789'),
('PAT005', 'Mohammed Ali', '1980-12-18', '202', 'Elm St', '305', 'Springfield', 'IL', '62705', 'USA', 'Cigna #DEF456');

INSERT INTO PATIENT_PHONE_NUMBERS (patientID, patientPhoneNumber) VALUES
('PAT001', '555-0001'),
('PAT001', '555-0002'),
('PAT002', '555-0003'),
('PAT003', '555-0004'),
('PAT004', '555-0005'),
('PAT004', '555-0006'),
('PAT005', '555-0007');

INSERT INTO MEDICAL_RECORD (recordID, date, diagnosis, treatment, note, patientID) VALUES
('REC001', '2024-01-05', 'Hypertension', 'Prescribed medication and lifestyle changes', 'Patient needs to monitor blood pressure daily', 'PAT001'),
('REC002', '2024-01-12', 'Migraine', 'Pain management and trigger avoidance', 'Recurring issue, consider preventative treatment', 'PAT002'),
('REC003', '2024-01-20', 'Type 2 Diabetes', 'Diet control and insulin therapy', 'Scheduled for follow-up in 3 months', 'PAT003'),
('REC004', '2024-02-02', 'Influenza', 'Rest and antiviral medication', 'Patient advised to stay hydrated', 'PAT004'),
('REC005', '2024-02-15', 'Appendicitis', 'Appendectomy performed', 'Surgery successful, recovery progressing well', 'PAT005'),
('REC006', '2024-03-10', 'Annual Check-up', 'No treatment needed', 'All vitals normal', 'PAT001');

INSERT INTO APPOINTMENT (appointmentID, dateTime, duration, status, type, notes, patientID, doctorID, roomNumber) VALUES
('APP001', '2025-05-10 09:00:00', 30, 'Scheduled', 'Follow-up', 'Blood pressure check', 'PAT001', 'DOC001', 'RM101'),
('APP002', '2025-05-11 14:30:00', 45, 'Scheduled', 'Consultation', 'Headache evaluation', 'PAT002', 'DOC002', 'RM201'),
('APP003', '2025-05-12 10:15:00', 60, 'Scheduled', 'Check-up', 'Diabetes management', 'PAT003', 'DOC003', 'RM301'),
('APP004', '2025-04-15 16:00:00', 30, 'Completed', 'Follow-up', 'Post-flu recovery assessment', 'PAT004', 'DOC001', 'RM101'),
('APP005', '2025-04-20 11:00:00', 45, 'Completed', 'Post-op', 'Surgical site examination', 'PAT005', 'DOC004', 'RM401'),
('APP006', '2025-04-25 09:30:00', 30, 'Cancelled', 'Check-up', 'Patient requested reschedule', 'PAT001', 'DOC003', 'RM301');

INSERT INTO MEDICATION (medicationID, name, type, stockLevel, unit) VALUES
('MED001', 'Lisinopril', 'Antihypertensive', 500, 'Tablet'),
('MED002', 'Sumatriptan', 'Antimigraine', 200, 'Tablet'),
('MED003', 'Metformin', 'Antidiabetic', 350, 'Tablet'),
('MED004', 'Oseltamivir', 'Antiviral', 150, 'Capsule'),
('MED005', 'Amoxicillin', 'Antibiotic', 400, 'Capsule'),
('MED006', 'Ibuprofen', 'Analgesic', 600, 'Tablet');

INSERT INTO PRESCRIPTION (recordID, prescriptionNumber, dosage, frequency, startDate, endDate, medicationID) VALUES
('REC001', 'PRE001', '10mg', 'Once daily', '2024-01-05', '2024-07-05', 'MED001'),
('REC002', 'PRE002', '50mg', 'As needed', '2024-01-12', '2024-04-12', 'MED002'),
('REC003', 'PRE003', '500mg', 'Twice daily', '2024-01-20', '2024-07-20', 'MED003'),
('REC004', 'PRE004', '75mg', '12-hourly', '2024-02-02', '2024-02-16', 'MED004'),
('REC005', 'PRE005', '500mg', '8-hourly', '2024-02-15', '2024-02-29', 'MED005'),
('REC001', 'PRE006', '20mg', 'Once daily', '2024-03-10', '2024-09-10', 'MED001');
