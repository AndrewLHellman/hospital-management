CREATE TABLE DEPARTMENT (
    deptID VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    headDoctor VARCHAR(10)
);

CREATE TABLE ROOM (
    roomNumber VARCHAR(10) PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Available', 'Occupied', 'Maintenance')),
    departmentID VARCHAR(10) NOT NULL,
    FOREIGN KEY (departmentID) REFERENCES DEPARTMENT(deptID)
);

CREATE TABLE DOCTOR (
    doctorID VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    office_phone VARCHAR(15),
    mobile_phone VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL,
    pager_number VARCHAR(15),
    emergency_contact VARCHAR(100) NOT NULL,
    departmentID VARCHAR(10) NOT NULL,
    FOREIGN KEY (departmentID) REFERENCES DEPARTMENT(deptID)
);

ALTER TABLE DEPARTMENT
ADD CONSTRAINT fk_head_doctor
FOREIGN KEY (headDoctor) REFERENCES DOCTOR(doctorID);

CREATE TABLE PATIENT (
    patientID VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    dateOfBirth DATE NOT NULL,
    street_number VARCHAR(10),
    street_name VARCHAR(100),
    apt_number VARCHAR(10),
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    country VARCHAR(50) NOT NULL,
    insuranceInfo VARCHAR(200)
);

CREATE TABLE PATIENT_PHONE_NUMBERS (
    patientID VARCHAR(10),
    patientPhoneNumber VARCHAR(15),
    PRIMARY KEY (patientID, patientPhoneNumber),
    FOREIGN KEY (patientID) REFERENCES PATIENT(patientID) ON DELETE CASCADE
);

CREATE TABLE APPOINTMENT (
    appointmentID VARCHAR(10) PRIMARY KEY,
    dateTime DATETIME NOT NULL,
    duration INT NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Scheduled', 'Completed', 'Cancelled', 'No-show')),
    type VARCHAR(50) NOT NULL,
    notes TEXT,
    patientID VARCHAR(10) NOT NULL,
    doctorID VARCHAR(10) NOT NULL,
    roomNumber VARCHAR(10) NOT NULL,
    FOREIGN KEY (patientID) REFERENCES PATIENT(patientID),
    FOREIGN KEY (doctorID) REFERENCES DOCTOR(doctorID),
    FOREIGN KEY (roomNumber) REFERENCES ROOM(roomNumber)
);

CREATE TABLE MEDICAL_RECORD (
    recordID VARCHAR(10) PRIMARY KEY,
    date DATE NOT NULL,
    diagnosis TEXT NOT NULL,
    treatment TEXT,
    note TEXT,
    patientID VARCHAR(10) NOT NULL,
    FOREIGN KEY (patientID) REFERENCES PATIENT(patientID)
);

CREATE TABLE MEDICATION (
    medicationID VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    stockLevel INT NOT NULL,
    unit VARCHAR(20) NOT NULL
);

CREATE TABLE PRESCRIPTION (
    recordID VARCHAR(10),
    prescriptionNumber VARCHAR(10),
    dosage VARCHAR(50) NOT NULL,
    frequency VARCHAR(50) NOT NULL,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL,
    medicationID VARCHAR(10) NOT NULL,
    PRIMARY KEY (recordID, prescriptionNumber),
    FOREIGN KEY (recordID) REFERENCES MEDICAL_RECORD(recordID) ON DELETE CASCADE,
    FOREIGN KEY (medicationID) REFERENCES MEDICATION(medicationID),
    CONSTRAINT valid_dates CHECK (endDate >= startDate)
);
