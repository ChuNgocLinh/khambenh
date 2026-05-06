-- ========================================
-- 1. TẠO DATABASE
-- ========================================
CREATE DATABASE HealthcareDB;
GO

USE HealthcareDB;
GO

-- ========================================
-- 2. BẢNG USERS (ĐĂNG NHẬP + PHÂN QUYỀN)
-- ========================================
CREATE TABLE Users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) UNIQUE NOT NULL,
    password NVARCHAR(255) NOT NULL,
    role NVARCHAR(20) CHECK (role IN ('admin','doctor','patient')) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);

-- ========================================
-- 3. BẢNG PATIENTS (BỆNH NHÂN)
-- ========================================
CREATE TABLE Patients (
    patient_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100),
    dob DATE,
    gender NVARCHAR(10),
    phone NVARCHAR(20),
    address NVARCHAR(255),
    created_at DATETIME DEFAULT GETDATE()
);

-- ========================================
-- 4. BẢNG DOCTORS (BÁC SĨ)
-- ========================================
CREATE TABLE Doctors (
    doctor_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100),
    specialty NVARCHAR(100),
    phone NVARCHAR(20),
    email NVARCHAR(100)
);

-- ========================================
-- 🔗 LINK USER - PATIENT / DOCTOR
-- ========================================

ALTER TABLE Patients 
ADD user_id INT UNIQUE;

ALTER TABLE Doctors 
ADD user_id INT UNIQUE;

ALTER TABLE Patients
ADD CONSTRAINT fk_patient_user
FOREIGN KEY (user_id) REFERENCES Users(user_id);

ALTER TABLE Doctors
ADD CONSTRAINT fk_doctor_user
FOREIGN KEY (user_id) REFERENCES Users(user_id);
-- ========================================
-- 5. BẢNG SERVICES (DỊCH VỤ KHÁM)
-- ========================================
CREATE TABLE Services (
    service_id INT IDENTITY(1,1) PRIMARY KEY,
    service_name NVARCHAR(100),
    price DECIMAL(10,2),
    description NVARCHAR(255)
);

-- ========================================
-- 6. BẢNG APPOINTMENTS (LỊCH HẸN)
-- ========================================
CREATE TABLE Appointments (
    appointment_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATETIME,
    status NVARCHAR(20) CHECK (status IN ('pending','confirmed','in_progress','done','cancelled')),
    note NVARCHAR(255),

    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
);

-- ========================================
-- 7. BẢNG MEDICAL RECORD (HỒ SƠ KHÁM)
-- ========================================
CREATE TABLE MedicalRecords (
    record_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    diagnosis NVARCHAR(255),
    treatment NVARCHAR(255),
    created_at DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
);

-- ========================================
-- 🔗 LINK MEDICAL RECORD - APPOINTMENT
-- ========================================

ALTER TABLE MedicalRecords
ADD appointment_id INT;

ALTER TABLE MedicalRecords
ADD CONSTRAINT fk_medical_appointment
FOREIGN KEY (appointment_id) REFERENCES Appointments(appointment_id);
-- ========================================
-- 8. BẢNG MEDICINES (THUỐC)
-- ========================================
CREATE TABLE Medicines (
    medicine_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100),
    quantity INT,
    price DECIMAL(10,2),
    description NVARCHAR(255)
);

-- ========================================
-- 9. BẢNG PRESCRIPTIONS (ĐƠN THUỐC)
-- ========================================
CREATE TABLE Prescriptions (
    prescription_id INT IDENTITY(1,1) PRIMARY KEY,
    record_id INT,
    medicine_id INT,
    quantity INT,

    FOREIGN KEY (record_id) REFERENCES MedicalRecords(record_id),
    FOREIGN KEY (medicine_id) REFERENCES Medicines(medicine_id)
);

-- ========================================
-- 10. BẢNG PAYMENTS (THANH TOÁN)
-- ========================================
CREATE TABLE Payments (
    payment_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id INT,
    total_amount DECIMAL(10,2),
    status NVARCHAR(20) CHECK (status IN ('paid','unpaid')),
    payment_date DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);

-- ========================================
-- 🔗 LINK PAYMENT - APPOINTMENT
-- ========================================

ALTER TABLE Payments
ADD appointment_id INT;

ALTER TABLE Payments
ADD CONSTRAINT fk_payment_appointment
FOREIGN KEY (appointment_id) REFERENCES Appointments(appointment_id);
-- ========================================
-- 11. BẢNG INVOICES (HÓA ĐƠN)
-- ========================================
CREATE TABLE Invoices (
    invoice_id INT IDENTITY(1,1) PRIMARY KEY,
    payment_id INT,
    service_id INT,
    quantity INT,

    FOREIGN KEY (payment_id) REFERENCES Payments(payment_id),
    FOREIGN KEY (service_id) REFERENCES Services(service_id)
);

-- ========================================
-- 💰 NÂNG CẤP INVOICE
-- ========================================

ALTER TABLE Invoices
ADD unit_price DECIMAL(10,2);

ALTER TABLE Invoices
ADD total_price AS (quantity * unit_price);
-- ========================================
-- 12. INSERT DỮ LIỆU MẪU
-- ========================================
-- ========================================
-- ⚡ INDEX (TỐI ƯU)
-- ========================================

CREATE INDEX idx_patient_name ON Patients(name);
CREATE INDEX idx_appointment_date ON Appointments(appointment_date);
-- Users
INSERT INTO Users (username, password, role)
VALUES 
('admin','123456','admin'),
('doctor1','123456','doctor'),
('staff1','123456','staff');

-- Patients
INSERT INTO Patients (name, dob, gender, phone, address)
VALUES
(N'Nguyễn Văn A','2000-01-01',N'Nam','0123456789',N'Hà Nội'),
(N'Trần Thị B','1995-05-10',N'Nữ','0987654321',N'HCM');

-- Doctors
INSERT INTO Doctors (name, specialty, phone, email)
VALUES
(N'Bác sĩ Minh',N'Nội khoa','0900000001','minh@gmail.com'),
(N'Bác sĩ Hùng',N'Ngoại khoa','0900000002','hung@gmail.com');

-- Services
INSERT INTO Services (service_name, price)
VALUES
(N'Khám tổng quát',200000),
(N'Xét nghiệm máu',150000);

-- Medicines
INSERT INTO Medicines (name, quantity, price)
VALUES
(N'Paracetamol',100,5000),
(N'Amoxicillin',50,10000);

-- Appointments
INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status)
VALUES
(1,1,GETDATE(),'pending'),
(2,2,GETDATE(),'pending');

-- MedicalRecords
INSERT INTO MedicalRecords (patient_id, doctor_id, diagnosis, treatment)
VALUES
(1,1,N'Sốt',N'Uống thuốc'),
(2,2,N'Đau bụng',N'Nghỉ ngơi');

-- Payments
INSERT INTO Payments (patient_id, total_amount, status)
VALUES
(1,200000,'paid'),
(2,150000,'unpaid');

GO