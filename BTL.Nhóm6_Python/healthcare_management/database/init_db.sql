-- ========================================
-- 1. BẢNG USERS (ĐĂNG NHẬP + PHÂN QUYỀN)
-- ========================================
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    -- Canonical roles phải đồng bộ với migrate.py: admin/doctor/patient/staff
    CHECK (role IN ('admin','doctor','patient','staff'))
);

-- ========================================
-- 2. BẢNG PATIENTS (BỆNH NHÂN)
-- ========================================
CREATE TABLE IF NOT EXISTS Patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    dob DATE,
    gender VARCHAR(10),
    phone VARCHAR(20),
    cccd VARCHAR(20),
    email VARCHAR(100),
    patient_type VARCHAR(30) DEFAULT 'general',
    occupation VARCHAR(100),
    intake_notes VARCHAR(500),
    address VARCHAR(255),
    user_id INT UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- ========================================
-- 3. BẢNG DOCTORS (BÁC SĨ)
-- ========================================
CREATE TABLE IF NOT EXISTS Doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    specialty VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    user_id INT UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- ========================================
-- 3.1 BẢNG USER SETTINGS (CÀI ĐẶT CÁ NHÂN)
-- ========================================
CREATE TABLE IF NOT EXISTS UserSettings (
    user_id INT PRIMARY KEY,
    gender VARCHAR(10) DEFAULT 'Nam',
    dob DATE,
    address VARCHAR(255) DEFAULT '',
    avatar_path VARCHAR(255) DEFAULT '',
    notify_new_appointment BOOLEAN DEFAULT TRUE,
    notify_reminder BOOLEAN DEFAULT TRUE,
    notify_system BOOLEAN DEFAULT TRUE,
    theme_mode VARCHAR(20) DEFAULT 'Sáng',
    font_size VARCHAR(20) DEFAULT 'Trung bình',
    display_density VARCHAR(20) DEFAULT 'Thoải mái',
    language VARCHAR(20) DEFAULT 'Tiếng Việt',
    backup_mode VARCHAR(20) DEFAULT 'cloud',
    last_backup_at DATETIME NULL,
    last_sync_at DATETIME NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- ========================================
-- 4. BẢNG SERVICES (DỊCH VỤ KHÁM)
-- ========================================
CREATE TABLE IF NOT EXISTS Services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(100),
    price DECIMAL(10,2),
    description VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE
);

-- ========================================
-- 5. BẢNG APPOINTMENTS (LỊCH HẸN)
-- ========================================
CREATE TABLE IF NOT EXISTS Appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATETIME,
    status VARCHAR(20) DEFAULT 'pending',
    note VARCHAR(255),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id),
    CHECK (status IN ('pending','confirmed','in_progress','done','cancelled'))
);

-- ========================================
-- 5.1 BẢNG WAITING QUEUE (HÀNG CHỜ KHÁM - STAFF 3B)
-- ========================================
CREATE TABLE IF NOT EXISTS WaitingQueue (
    queue_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    appointment_id INT NULL,
    queue_no VARCHAR(20) NOT NULL,
    queue_area VARCHAR(20) NOT NULL DEFAULT '3B',
    status VARCHAR(20) NOT NULL DEFAULT 'waiting',
    intake_note VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (appointment_id) REFERENCES Appointments(appointment_id),
    CHECK (status IN ('waiting','called','in_consultation','done','cancelled'))
);

CREATE UNIQUE INDEX UQ_Patients_CCCD ON Patients(cccd);
CREATE UNIQUE INDEX UQ_Patients_Phone ON Patients(phone);
CREATE UNIQUE INDEX UQ_WaitingQueue_QueueNo_Area ON WaitingQueue(queue_no, queue_area);
CREATE INDEX IX_Patients_Phone ON Patients(phone);

-- ========================================
-- 6. BẢNG MEDICAL RECORD (HỒ SƠ KHÁM)
-- ========================================
CREATE TABLE IF NOT EXISTS MedicalRecords (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_id INT,
    diagnosis VARCHAR(255),
    treatment VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id),
    FOREIGN KEY (appointment_id) REFERENCES Appointments(appointment_id)
);

-- ========================================
-- 7. BẢNG MEDICINES (THUỐC)
-- ========================================
CREATE TABLE IF NOT EXISTS Medicines (
    medicine_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    quantity INT,
    price DECIMAL(10,2),
    description VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE
);

-- ========================================
-- 8. BẢNG PRESCRIPTIONS (ĐƠN THUỐC)
-- ========================================
CREATE TABLE IF NOT EXISTS Prescriptions (
    prescription_id INT AUTO_INCREMENT PRIMARY KEY,
    record_id INT,
    medicine_id INT,
    quantity INT,
    FOREIGN KEY (record_id) REFERENCES MedicalRecords(record_id),
    FOREIGN KEY (medicine_id) REFERENCES Medicines(medicine_id)
);

-- ========================================
-- 9. BẢNG PAYMENTS (THANH TOÁN)
-- ========================================
CREATE TABLE IF NOT EXISTS Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    appointment_id INT,
    total_amount DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'unpaid',
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (appointment_id) REFERENCES Appointments(appointment_id),
    CHECK (status IN ('paid','unpaid'))
);

-- ========================================
-- 10. BẢNG INVOICES (HÓA ĐƠN)
-- ========================================
CREATE TABLE IF NOT EXISTS Invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    payment_id INT,
    service_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    FOREIGN KEY (payment_id) REFERENCES Payments(payment_id),
    FOREIGN KEY (service_id) REFERENCES Services(service_id)
);

-- ========================================
-- ⚡ INDEX (TỐI ƯU)
-- ========================================
CREATE INDEX idx_patient_name ON Patients(name);
CREATE INDEX idx_appointment_date ON Appointments(appointment_date);
CREATE INDEX idx_appt_patient_id ON Appointments(patient_id);
CREATE INDEX idx_appt_doctor_id ON Appointments(doctor_id);
CREATE INDEX idx_record_appointment_id ON MedicalRecords(appointment_id);
CREATE INDEX idx_prescription_record_id ON Prescriptions(record_id);
CREATE INDEX idx_payment_patient_id ON Payments(patient_id);
CREATE INDEX idx_payment_appointment_id ON Payments(appointment_id);
CREATE INDEX idx_invoice_payment_id ON Invoices(payment_id);

-- ========================================
-- 11. INSERT DỮ LIỆU MẪU
-- ========================================
INSERT IGNORE INTO Users (username, password, role) VALUES 
('admin','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','admin'),
('doctor1','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','doctor'),
('staff1','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','patient');

INSERT IGNORE INTO Patients (name, dob, gender, phone, address, user_id) VALUES
('Nguyễn Văn A','2000-01-01','Nam','0123456789','Hà Nội', 3),
('Trần Thị B','1995-05-10','Nữ','0987654321','HCM', NULL);

INSERT IGNORE INTO Doctors (name, specialty, phone, email, user_id) VALUES
('Bác sĩ Minh','Nội khoa','0900000001','minh@gmail.com', 2),
('Bác sĩ Hùng','Ngoại khoa','0900000002','hung@gmail.com', NULL);

INSERT IGNORE INTO Services (service_name, price) VALUES
('Khám tổng quát',200000),
('Xét nghiệm máu',150000);

INSERT IGNORE INTO Medicines (name, quantity, price) VALUES
('Paracetamol',100,5000),
('Amoxicillin',50,10000);

INSERT IGNORE INTO Appointments (patient_id, doctor_id, appointment_date, status) VALUES
(1,1,CURRENT_TIMESTAMP,'pending'),
(2,2,CURRENT_TIMESTAMP,'pending');

INSERT IGNORE INTO MedicalRecords (patient_id, doctor_id, diagnosis, treatment) VALUES
(1,1,'Sốt','Uống thuốc'),
(2,2,'Đau bụng','Nghỉ ngơi');

INSERT IGNORE INTO Payments (patient_id, appointment_id, total_amount, status) VALUES
(1, 1, 200000,'paid'),
(2, 2, 150000,'unpaid');
