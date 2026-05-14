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

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Users' AND COLUMN_NAME = 'is_active'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Users ADD COLUMN is_active BOOLEAN DEFAULT TRUE', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

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

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Patients' AND COLUMN_NAME = 'cccd'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Patients ADD COLUMN cccd VARCHAR(20) NULL', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Patients' AND COLUMN_NAME = 'email'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Patients ADD COLUMN email VARCHAR(100) NULL', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Patients' AND COLUMN_NAME = 'patient_type'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Patients ADD COLUMN patient_type VARCHAR(30) DEFAULT ''general''', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Patients' AND COLUMN_NAME = 'occupation'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Patients ADD COLUMN occupation VARCHAR(100) NULL', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Patients' AND COLUMN_NAME = 'intake_notes'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Patients ADD COLUMN intake_notes VARCHAR(500) NULL', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Patients' AND COLUMN_NAME = 'is_active'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Patients ADD COLUMN is_active BOOLEAN DEFAULT TRUE', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

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

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Doctors' AND COLUMN_NAME = 'is_active'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Doctors ADD COLUMN is_active BOOLEAN DEFAULT TRUE', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

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
    work_schedule TEXT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'UserSettings' AND COLUMN_NAME = 'work_schedule'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE UserSettings ADD COLUMN work_schedule TEXT NULL', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ========================================
-- 4. BẢNG SERVICES (DỊCH VỤ KHÁM)
-- ========================================
CREATE TABLE IF NOT EXISTS Services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(100),
    service_code VARCHAR(30),
    category VARCHAR(100),
    duration INT DEFAULT 30,
    price DECIMAL(10,2),
    description VARCHAR(255),
    is_visible BOOLEAN DEFAULT TRUE,
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

-- Create indexes through INFORMATION_SCHEMA checks so rerunning init_db.sql stays safe.
SET @idx_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Patients' AND INDEX_NAME = 'UQ_Patients_CCCD'
);
SET @idx_sql = IF(@idx_exists = 0, 'CREATE UNIQUE INDEX UQ_Patients_CCCD ON Patients(cccd)', 'SELECT 1');
PREPARE stmt FROM @idx_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @idx_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Patients' AND INDEX_NAME = 'UQ_Patients_Phone'
);
SET @idx_sql = IF(@idx_exists = 0, 'CREATE UNIQUE INDEX UQ_Patients_Phone ON Patients(phone)', 'SELECT 1');
PREPARE stmt FROM @idx_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @idx_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'WaitingQueue' AND INDEX_NAME = 'UQ_WaitingQueue_QueueNo_Area'
);
SET @idx_sql = IF(@idx_exists = 0, 'CREATE UNIQUE INDEX UQ_WaitingQueue_QueueNo_Area ON WaitingQueue(queue_no, queue_area)', 'SELECT 1');
PREPARE stmt FROM @idx_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @idx_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Patients' AND INDEX_NAME = 'IX_Patients_Phone'
);
SET @idx_sql = IF(@idx_exists = 0, 'CREATE INDEX IX_Patients_Phone ON Patients(phone)', 'SELECT 1');
PREPARE stmt FROM @idx_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

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
    record_status VARCHAR(20) DEFAULT 'draft',
    finalized_at DATETIME NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id),
    FOREIGN KEY (appointment_id) REFERENCES Appointments(appointment_id),
    CHECK (record_status IN ('draft','finalized'))
);

-- ========================================
-- 7. BẢNG MEDICINES (THUỐC)
-- ========================================
CREATE TABLE IF NOT EXISTS Medicines (
    medicine_id INT AUTO_INCREMENT PRIMARY KEY,
    medicine_code VARCHAR(30),
    name VARCHAR(100),
    active_ingredient VARCHAR(100),
    category VARCHAR(100),
    unit VARCHAR(30),
    supplier VARCHAR(100),
    quantity INT,
    import_price DECIMAL(10,2) DEFAULT 0,
    price DECIMAL(10,2),
    description VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE
);

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Medicines' AND COLUMN_NAME = 'is_active'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Medicines ADD COLUMN is_active BOOLEAN DEFAULT TRUE', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Medicines' AND COLUMN_NAME = 'medicine_code'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Medicines ADD COLUMN medicine_code VARCHAR(30) NULL', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Medicines' AND COLUMN_NAME = 'active_ingredient'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Medicines ADD COLUMN active_ingredient VARCHAR(100) NULL', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Medicines' AND COLUMN_NAME = 'category'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Medicines ADD COLUMN category VARCHAR(100) NULL', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Medicines' AND COLUMN_NAME = 'unit'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Medicines ADD COLUMN unit VARCHAR(30) NULL', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Medicines' AND COLUMN_NAME = 'supplier'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Medicines ADD COLUMN supplier VARCHAR(100) NULL', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Medicines' AND COLUMN_NAME = 'import_price'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Medicines ADD COLUMN import_price DECIMAL(10,2) DEFAULT 0', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Services' AND COLUMN_NAME = 'service_code'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Services ADD COLUMN service_code VARCHAR(30) NULL', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Services' AND COLUMN_NAME = 'category'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Services ADD COLUMN category VARCHAR(100) NULL', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Services' AND COLUMN_NAME = 'duration'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Services ADD COLUMN duration INT DEFAULT 30', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Services' AND COLUMN_NAME = 'is_visible'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Services ADD COLUMN is_visible BOOLEAN DEFAULT TRUE', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ========================================
-- 8. BẢNG PRESCRIPTIONS (ĐƠN THUỐC)
-- ========================================
CREATE TABLE IF NOT EXISTS Prescriptions (
    prescription_id INT AUTO_INCREMENT PRIMARY KEY,
    record_id INT,
    medicine_id INT,
    quantity INT,
    status VARCHAR(20) DEFAULT 'draft',
    dispensed_at DATETIME NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (record_id) REFERENCES MedicalRecords(record_id),
    FOREIGN KEY (medicine_id) REFERENCES Medicines(medicine_id),
    CHECK (status IN ('draft','issued','dispensed','cancelled'))
);

CREATE TABLE IF NOT EXISTS Notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    content VARCHAR(500),
    type VARCHAR(50) DEFAULT 'system',
    target_page VARCHAR(50) DEFAULT 'dashboard',
    target_id INT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    read_at DATETIME NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    CHECK (target_page IN ('schedule','patient_profile','prescriptions','dashboard','settings'))
);

-- ========================================
-- 9. BẢNG PAYMENTS (THANH TOÁN)
-- ========================================
CREATE TABLE IF NOT EXISTS Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    appointment_id INT,
    total_amount DECIMAL(10,2),
    method VARCHAR(50) DEFAULT 'Tiền mặt',
    status VARCHAR(20) DEFAULT 'unpaid',
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (appointment_id) REFERENCES Appointments(appointment_id),
    CHECK (status IN ('paid','unpaid','failed','refunded','cancelled'))
);

SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Payments' AND COLUMN_NAME = 'method'
);
SET @col_sql = IF(@col_exists = 0, 'ALTER TABLE Payments ADD COLUMN method VARCHAR(50) DEFAULT ''Tiền mặt''', 'SELECT 1');
PREPARE stmt FROM @col_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

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
SET @idx_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Patients' AND INDEX_NAME = 'idx_patient_name'
);
SET @idx_sql = IF(@idx_exists = 0, 'CREATE INDEX idx_patient_name ON Patients(name)', 'SELECT 1');
PREPARE stmt FROM @idx_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @idx_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Appointments' AND INDEX_NAME = 'idx_appointment_date'
);
SET @idx_sql = IF(@idx_exists = 0, 'CREATE INDEX idx_appointment_date ON Appointments(appointment_date)', 'SELECT 1');
PREPARE stmt FROM @idx_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @idx_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Appointments' AND INDEX_NAME = 'idx_appt_patient_id'
);
SET @idx_sql = IF(@idx_exists = 0, 'CREATE INDEX idx_appt_patient_id ON Appointments(patient_id)', 'SELECT 1');
PREPARE stmt FROM @idx_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @idx_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Appointments' AND INDEX_NAME = 'idx_appt_doctor_id'
);
SET @idx_sql = IF(@idx_exists = 0, 'CREATE INDEX idx_appt_doctor_id ON Appointments(doctor_id)', 'SELECT 1');
PREPARE stmt FROM @idx_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @idx_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'MedicalRecords' AND INDEX_NAME = 'idx_record_appointment_id'
);
SET @idx_sql = IF(@idx_exists = 0, 'CREATE INDEX idx_record_appointment_id ON MedicalRecords(appointment_id)', 'SELECT 1');
PREPARE stmt FROM @idx_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @idx_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Prescriptions' AND INDEX_NAME = 'idx_prescription_record_id'
);
SET @idx_sql = IF(@idx_exists = 0, 'CREATE INDEX idx_prescription_record_id ON Prescriptions(record_id)', 'SELECT 1');
PREPARE stmt FROM @idx_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @idx_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Notifications' AND INDEX_NAME = 'idx_notifications_user_read'
);
SET @idx_sql = IF(@idx_exists = 0, 'CREATE INDEX idx_notifications_user_read ON Notifications(user_id, is_read)', 'SELECT 1');
PREPARE stmt FROM @idx_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @idx_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Payments' AND INDEX_NAME = 'idx_payment_patient_id'
);
SET @idx_sql = IF(@idx_exists = 0, 'CREATE INDEX idx_payment_patient_id ON Payments(patient_id)', 'SELECT 1');
PREPARE stmt FROM @idx_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @idx_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Payments' AND INDEX_NAME = 'idx_payment_appointment_id'
);
SET @idx_sql = IF(@idx_exists = 0, 'CREATE INDEX idx_payment_appointment_id ON Payments(appointment_id)', 'SELECT 1');
PREPARE stmt FROM @idx_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @idx_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Invoices' AND INDEX_NAME = 'idx_invoice_payment_id'
);
SET @idx_sql = IF(@idx_exists = 0, 'CREATE INDEX idx_invoice_payment_id ON Invoices(payment_id)', 'SELECT 1');
PREPARE stmt FROM @idx_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ========================================
-- 11. INSERT DỮ LIỆU KHỞI TẠO VẬN HÀNH
-- ========================================
-- Mật khẩu mặc định cho seed users là 123456 (đã SHA256).
INSERT IGNORE INTO Users (username, password, role, is_active) VALUES
('admin','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','admin',1),
('doctor1','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','doctor',1),
('staff1','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','patient',1),
('nam.nguyen','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','admin',1),
('mai.tran','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','doctor',1),
('cuong.le','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','doctor',1),
('lan.pham','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','staff',1),
('tuan.hoang','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','staff',1),
('huong.vu','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','staff',0),
('quan.do','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','staff',1),
('hoa.nguyen','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','staff',0),
('dung.bui','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','staff',1),
('kien.truong','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','patient',1);

INSERT INTO Patients (name, dob, gender, phone, cccd, email, address, user_id, is_active)
SELECT 'Lễ tân hệ thống','2000-01-01','Nữ','0123456789','000000000001','staff1@careplus.vn','TP.HCM',
       (SELECT user_id FROM Users WHERE username='staff1' LIMIT 1), 1
WHERE NOT EXISTS (
    SELECT 1 FROM Patients WHERE phone='0123456789'
);

INSERT INTO Patients (name, dob, gender, phone, cccd, email, address, user_id, is_active)
SELECT 'Nguyễn Văn Nam','1990-05-24','Nam','0987654321','000000000002','nam.nguyen@gmail.com','Quận 1, TP.HCM',
       (SELECT user_id FROM Users WHERE username='nam.nguyen' LIMIT 1), 1
WHERE NOT EXISTS (
    SELECT 1 FROM Patients WHERE phone='0987654321'
);

INSERT INTO Patients (name, dob, gender, phone, cccd, email, address, user_id, is_active)
SELECT 'Phạm Thị Lan','1992-08-14','Nữ','0909876543','000000000003','lan.pham@gmail.com','Quận 3, TP.HCM',
       (SELECT user_id FROM Users WHERE username='lan.pham' LIMIT 1), 1
WHERE NOT EXISTS (
    SELECT 1 FROM Patients WHERE phone='0909876543'
);

INSERT INTO Patients (name, dob, gender, phone, cccd, email, address, user_id, is_active)
SELECT 'Hoàng Anh Tuấn','1989-11-20','Nam','0988765432','000000000004','tuan.hoang@gmail.com','Quận 7, TP.HCM',
       (SELECT user_id FROM Users WHERE username='tuan.hoang' LIMIT 1), 1
WHERE NOT EXISTS (
    SELECT 1 FROM Patients WHERE phone='0988765432'
);

INSERT INTO Patients (name, dob, gender, phone, cccd, email, address, user_id, is_active)
SELECT 'Vũ Thị Hương','1993-03-16','Nữ','0977654321','000000000005','huong.vu@gmail.com','Quận 10, TP.HCM',
       (SELECT user_id FROM Users WHERE username='huong.vu' LIMIT 1), 0
WHERE NOT EXISTS (
    SELECT 1 FROM Patients WHERE phone='0977654321'
);

INSERT INTO Patients (name, dob, gender, phone, cccd, email, address, user_id, is_active)
SELECT 'Đỗ Minh Quân','1996-09-28','Nam','0966543210','000000000006','quan.do@gmail.com','Quận Bình Thạnh, TP.HCM',
       (SELECT user_id FROM Users WHERE username='quan.do' LIMIT 1), 1
WHERE NOT EXISTS (
    SELECT 1 FROM Patients WHERE phone='0966543210'
);

INSERT INTO Patients (name, dob, gender, phone, cccd, email, address, user_id, is_active)
SELECT 'Nguyễn Thị Hoa','1988-12-02','Nữ','0908111222','000000000007','hoa.nguyen@gmail.com','Quận Phú Nhuận, TP.HCM',
       (SELECT user_id FROM Users WHERE username='hoa.nguyen' LIMIT 1), 0
WHERE NOT EXISTS (
    SELECT 1 FROM Patients WHERE phone='0908111222'
);

INSERT INTO Patients (name, dob, gender, phone, cccd, email, address, user_id, is_active)
SELECT 'Bùi Văn Dũng','1991-06-07','Nam','0982333444','000000000008','dung.bui@gmail.com','Quận Tân Bình, TP.HCM',
       (SELECT user_id FROM Users WHERE username='dung.bui' LIMIT 1), 1
WHERE NOT EXISTS (
    SELECT 1 FROM Patients WHERE phone='0982333444'
);

INSERT INTO Patients (name, dob, gender, phone, cccd, email, address, user_id, is_active)
SELECT 'Trương Văn Kiên','1994-01-11','Nam','0933999000','000000000009','kien.truong@gmail.com','Quận 5, TP.HCM',
       (SELECT user_id FROM Users WHERE username='kien.truong' LIMIT 1), 1
WHERE NOT EXISTS (
    SELECT 1 FROM Patients WHERE phone='0933999000'
);

INSERT INTO Doctors (name, specialty, phone, email, user_id, is_active)
SELECT 'Bác sĩ Minh','Nội khoa','0900000001','minh@gmail.com',
       (SELECT user_id FROM Users WHERE username='doctor1' LIMIT 1), 1
WHERE NOT EXISTS (
    SELECT 1 FROM Doctors WHERE phone='0900000001'
);

INSERT INTO Doctors (name, specialty, phone, email, user_id, is_active)
SELECT 'Trần Thị Mai','Tim mạch','0912345678','mai.tran@gmail.com',
       (SELECT user_id FROM Users WHERE username='mai.tran' LIMIT 1), 1
WHERE NOT EXISTS (
    SELECT 1 FROM Doctors WHERE phone='0912345678'
);

INSERT INTO Doctors (name, specialty, phone, email, user_id, is_active)
SELECT 'Lê Văn Cường','Da liễu','0933456789','cuong.le@gmail.com',
       (SELECT user_id FROM Users WHERE username='cuong.le' LIMIT 1), 1
WHERE NOT EXISTS (
    SELECT 1 FROM Doctors WHERE phone='0933456789'
);

INSERT INTO Services (service_code, service_name, category, duration, price, description, is_visible, is_active)
SELECT 'DV001', 'Khám tổng quát', 'Khám bệnh', 30, 200000, 'Khám sức khỏe tổng quát', 1, 1
WHERE NOT EXISTS (
    SELECT 1 FROM Services WHERE service_code='DV001'
);

INSERT INTO Services (service_code, service_name, category, duration, price, description, is_visible, is_active)
SELECT 'DV002', 'Xét nghiệm máu', 'Xét nghiệm', 20, 150000, 'Xét nghiệm máu tổng quát', 1, 1
WHERE NOT EXISTS (
    SELECT 1 FROM Services WHERE service_code='DV002'
);

INSERT INTO Medicines (medicine_code, name, active_ingredient, category, unit, supplier, quantity, import_price, price, description, is_active)
SELECT 'TH001', 'Paracetamol', 'Paracetamol', 'Giảm đau - Hạ sốt', 'Viên', 'Dược Hậu Giang', 100, 3500, 5000, 'Thuốc giảm đau hạ sốt', 1
WHERE NOT EXISTS (
    SELECT 1 FROM Medicines WHERE medicine_code='TH001'
);

INSERT INTO Medicines (medicine_code, name, active_ingredient, category, unit, supplier, quantity, import_price, price, description, is_active)
SELECT 'TH002', 'Amoxicillin', 'Amoxicillin', 'Kháng sinh', 'Viên', 'Traphaco', 50, 7000, 10000, 'Kháng sinh phổ rộng', 1
WHERE NOT EXISTS (
    SELECT 1 FROM Medicines WHERE medicine_code='TH002'
);

INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status)
SELECT p.patient_id,
       (
           SELECT doctor_id
           FROM Doctors
           WHERE phone='0900000001'
           ORDER BY CASE WHEN user_id IS NULL THEN 1 ELSE 0 END, doctor_id ASC
           LIMIT 1
       ),
       CURRENT_TIMESTAMP,
       'pending'
FROM Patients p
WHERE p.phone='0123456789'
  AND NOT EXISTS (
      SELECT 1 FROM Appointments a
      WHERE a.patient_id = p.patient_id
        AND a.doctor_id = (
            SELECT doctor_id
            FROM Doctors
            WHERE phone='0900000001'
            ORDER BY CASE WHEN user_id IS NULL THEN 1 ELSE 0 END, doctor_id ASC
            LIMIT 1
        )
        AND a.status='pending'
  )
LIMIT 1;

INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status)
SELECT p.patient_id,
       (
           SELECT doctor_id
           FROM Doctors
           WHERE phone='0912345678'
           ORDER BY CASE WHEN user_id IS NULL THEN 1 ELSE 0 END, doctor_id ASC
           LIMIT 1
       ),
       CURRENT_TIMESTAMP,
       'pending'
FROM Patients p
WHERE p.phone='0987654321'
  AND NOT EXISTS (
      SELECT 1 FROM Appointments a
      WHERE a.patient_id = p.patient_id
        AND a.doctor_id = (
            SELECT doctor_id
            FROM Doctors
            WHERE phone='0912345678'
            ORDER BY CASE WHEN user_id IS NULL THEN 1 ELSE 0 END, doctor_id ASC
            LIMIT 1
        )
        AND a.status='pending'
  )
LIMIT 1;

INSERT INTO MedicalRecords (patient_id, doctor_id, diagnosis, treatment)
SELECT p.patient_id,
       (
           SELECT doctor_id
           FROM Doctors
           WHERE phone='0900000001'
           ORDER BY CASE WHEN user_id IS NULL THEN 1 ELSE 0 END, doctor_id ASC
           LIMIT 1
       ),
       'Sốt',
       'Uống thuốc'
FROM Patients p
WHERE p.phone='0123456789'
  AND NOT EXISTS (
      SELECT 1 FROM MedicalRecords mr
      WHERE mr.patient_id = p.patient_id
        AND mr.doctor_id = (
            SELECT doctor_id
            FROM Doctors
            WHERE phone='0900000001'
            ORDER BY CASE WHEN user_id IS NULL THEN 1 ELSE 0 END, doctor_id ASC
            LIMIT 1
        )
  )
LIMIT 1;

INSERT INTO MedicalRecords (patient_id, doctor_id, diagnosis, treatment)
SELECT p.patient_id,
       (
           SELECT doctor_id
           FROM Doctors
           WHERE phone='0912345678'
           ORDER BY CASE WHEN user_id IS NULL THEN 1 ELSE 0 END, doctor_id ASC
           LIMIT 1
       ),
       'Đau bụng',
       'Nghỉ ngơi'
FROM Patients p
WHERE p.phone='0987654321'
  AND NOT EXISTS (
      SELECT 1 FROM MedicalRecords mr
      WHERE mr.patient_id = p.patient_id
        AND mr.doctor_id = (
            SELECT doctor_id
            FROM Doctors
            WHERE phone='0912345678'
            ORDER BY CASE WHEN user_id IS NULL THEN 1 ELSE 0 END, doctor_id ASC
            LIMIT 1
        )
  )
LIMIT 1;

INSERT INTO Payments (patient_id, appointment_id, total_amount, method, status)
SELECT p.patient_id, a.appointment_id, 200000, 'Chuyển khoản', 'paid'
FROM Patients p
LEFT JOIN Appointments a ON a.patient_id = p.patient_id
LEFT JOIN Doctors d ON d.doctor_id = a.doctor_id
WHERE p.phone='0123456789'
  AND (d.phone='0900000001' OR d.phone IS NULL)
  AND NOT EXISTS (
      SELECT 1 FROM Payments pay
      WHERE pay.patient_id = p.patient_id AND pay.total_amount=200000 AND pay.status='paid'
  )
ORDER BY a.appointment_id ASC
LIMIT 1;

INSERT INTO Payments (patient_id, appointment_id, total_amount, method, status)
SELECT p.patient_id, a.appointment_id, 150000, 'Tiền mặt', 'unpaid'
FROM Patients p
LEFT JOIN Appointments a ON a.patient_id = p.patient_id
LEFT JOIN Doctors d ON d.doctor_id = a.doctor_id
WHERE p.phone='0987654321'
  AND (d.phone='0912345678' OR d.phone IS NULL)
  AND NOT EXISTS (
      SELECT 1 FROM Payments pay
      WHERE pay.patient_id = p.patient_id AND pay.total_amount=150000 AND pay.status='unpaid'
  )
ORDER BY a.appointment_id ASC
LIMIT 1;

INSERT INTO Invoices (payment_id, service_id, quantity, unit_price)
SELECT p.payment_id,
       (
           SELECT s.service_id
           FROM Services s
           WHERE s.service_code = 'DV001'
           ORDER BY s.service_id ASC
           LIMIT 1
       ),
       1,
       p.total_amount
FROM Payments p
WHERE p.status = 'paid'
  AND NOT EXISTS (
      SELECT 1 FROM Invoices i
      WHERE i.payment_id = p.payment_id
  )
LIMIT 1;

INSERT INTO Invoices (payment_id, service_id, quantity, unit_price)
SELECT p.payment_id,
       (
           SELECT s.service_id
           FROM Services s
           WHERE s.service_code = 'DV002'
           ORDER BY s.service_id ASC
           LIMIT 1
       ),
       1,
       p.total_amount
FROM Payments p
WHERE p.status = 'unpaid'
  AND NOT EXISTS (
      SELECT 1 FROM Invoices i
      WHERE i.payment_id = p.payment_id
  )
LIMIT 1;

INSERT INTO Payments (patient_id, appointment_id, total_amount, method, status)
SELECT p.patient_id, a.appointment_id, 350000, 'Thẻ ngân hàng', 'paid'
FROM Patients p
LEFT JOIN Appointments a ON a.patient_id = p.patient_id
WHERE p.phone='0987654321'
  AND NOT EXISTS (
      SELECT 1 FROM Payments pay
      WHERE pay.patient_id = p.patient_id AND pay.total_amount=350000 AND pay.status='paid'
  )
ORDER BY a.appointment_id DESC
LIMIT 1;

INSERT INTO Payments (patient_id, appointment_id, total_amount, method, status)
SELECT p.patient_id, a.appointment_id, 120000, 'Ví điện tử', 'failed'
FROM Patients p
LEFT JOIN Appointments a ON a.patient_id = p.patient_id
WHERE p.phone='0123456789'
  AND NOT EXISTS (
      SELECT 1 FROM Payments pay
      WHERE pay.patient_id = p.patient_id AND pay.total_amount=120000 AND pay.status='failed'
  )
ORDER BY a.appointment_id ASC
LIMIT 1;

INSERT INTO Payments (patient_id, appointment_id, total_amount, method, status)
SELECT p.patient_id, a.appointment_id, 500000, 'Chuyển khoản', 'refunded'
FROM Patients p
LEFT JOIN Appointments a ON a.patient_id = p.patient_id
WHERE p.phone='0909876543'
  AND NOT EXISTS (
      SELECT 1 FROM Payments pay
      WHERE pay.patient_id = p.patient_id AND pay.total_amount=500000 AND pay.status='refunded'
  )
ORDER BY a.appointment_id ASC
LIMIT 1;

INSERT INTO Invoices (payment_id, service_id, quantity, unit_price)
SELECT p.payment_id,
       (SELECT s.service_id FROM Services s WHERE s.service_code = 'DV003' ORDER BY s.service_id ASC LIMIT 1),
       1, p.total_amount
FROM Payments p
WHERE p.total_amount = 350000
  AND NOT EXISTS (SELECT 1 FROM Invoices i WHERE i.payment_id = p.payment_id)
LIMIT 1;

INSERT INTO Invoices (payment_id, service_id, quantity, unit_price)
SELECT p.payment_id,
       (SELECT s.service_id FROM Services s WHERE s.service_code = 'DV004' ORDER BY s.service_id ASC LIMIT 1),
       1, p.total_amount
FROM Payments p
WHERE p.total_amount = 120000
  AND NOT EXISTS (SELECT 1 FROM Invoices i WHERE i.payment_id = p.payment_id)
LIMIT 1;

INSERT INTO Invoices (payment_id, service_id, quantity, unit_price)
SELECT p.payment_id,
       (SELECT s.service_id FROM Services s WHERE s.service_code = 'DV005' ORDER BY s.service_id ASC LIMIT 1),
       1, p.total_amount
FROM Payments p
WHERE p.total_amount = 500000
  AND NOT EXISTS (SELECT 1 FROM Invoices i WHERE i.payment_id = p.payment_id)
LIMIT 1;

INSERT INTO Notifications (user_id, title, content, type, target_page)
SELECT u.user_id, 'Sao lưu dữ liệu thành công', 'Dữ liệu hệ thống đã được sao lưu lúc 02:00 AM', 'backup', 'settings'
FROM Users u
WHERE u.role = 'admin'
  AND NOT EXISTS (
      SELECT 1 FROM Notifications n
      WHERE n.user_id = u.user_id AND n.title = 'Sao lưu dữ liệu thành công'
  )
LIMIT 1;

INSERT INTO Notifications (user_id, title, content, type, target_page)
SELECT u.user_id, 'Cảnh báo tồn kho thuốc', 'Một số thuốc đang ở ngưỡng sắp hết hàng', 'inventory', 'dashboard'
FROM Users u
WHERE u.role = 'admin'
  AND NOT EXISTS (
      SELECT 1 FROM Notifications n
      WHERE n.user_id = u.user_id AND n.title = 'Cảnh báo tồn kho thuốc'
  )
LIMIT 1;
INSERT INTO Services (service_code, service_name, category, duration, price, description, is_visible, is_active)
SELECT 'DV003', 'Khám chuyên khoa Nội tiết', 'Khám bệnh', 45, 200000, 'Khám và tư vấn bệnh lý nội tiết', 1, 1
WHERE NOT EXISTS (SELECT 1 FROM Services WHERE service_code='DV003');

INSERT INTO Services (service_code, service_name, category, duration, price, description, is_visible, is_active)
SELECT 'DV004', 'Xét nghiệm đường huyết', 'Xét nghiệm', 10, 80000, 'Kiểm tra lượng đường trong máu', 1, 1
WHERE NOT EXISTS (SELECT 1 FROM Services WHERE service_code='DV004');

INSERT INTO Services (service_code, service_name, category, duration, price, description, is_visible, is_active)
SELECT 'DV005', 'Xét nghiệm mỡ máu', 'Xét nghiệm', 15, 150000, 'Định lượng Cholesterol, Triglycerid, HDL, LDL', 1, 1
WHERE NOT EXISTS (SELECT 1 FROM Services WHERE service_code='DV005');

INSERT INTO Services (service_code, service_name, category, duration, price, description, is_visible, is_active)
SELECT 'DV006', 'Siêu âm ổ bụng tổng quát', 'Chẩn đoán hình ảnh', 30, 250000, 'Siêu âm 4D ổ bụng', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM Services WHERE service_code='DV006');

INSERT INTO Services (service_code, service_name, category, duration, price, description, is_visible, is_active)
SELECT 'DV007', 'Chụp X-quang phổi', 'Chẩn đoán hình ảnh', 20, 200000, 'Chụp X-quang tim phổi thẳng', 1, 1
WHERE NOT EXISTS (SELECT 1 FROM Services WHERE service_code='DV007');

INSERT INTO Services (service_code, service_name, category, duration, price, description, is_visible, is_active)
SELECT 'DV008', 'Điện tâm đồ (ECG)', 'Thăm dò chức năng', 15, 120000, 'Đo điện tim đồ 12 chuyển đạo', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM Services WHERE service_code='DV008');

INSERT INTO Services (service_code, service_name, category, duration, price, description, is_visible, is_active)
SELECT 'DV009', 'Vật lý trị liệu', 'Điều trị', 30, 180000, 'Phục hồi chức năng cơ xương khớp', 1, 1
WHERE NOT EXISTS (SELECT 1 FROM Services WHERE service_code='DV009');

-- ========================================
-- 12. DATASET MẪU CHO DASHBOARD BÁO CÁO (DỮ LIỆU ĐỘNG)
-- ========================================
INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status, note)
SELECT
    p.patient_id,
    d.doctor_id,
    DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 25 DAY),
    'done',
    'Tái khám định kỳ'
FROM Patients p
JOIN Doctors d ON d.phone = '0900000001'
WHERE p.phone = '0987654321'
  AND NOT EXISTS (
    SELECT 1 FROM Appointments a
    WHERE a.patient_id = p.patient_id
      AND a.doctor_id = d.doctor_id
      AND DATE(a.appointment_date) = DATE(DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 25 DAY))
  )
LIMIT 1;

INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status, note)
SELECT
    p.patient_id,
    d.doctor_id,
    DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 18 DAY),
    'done',
    'Khám chuyên khoa tim mạch'
FROM Patients p
JOIN Doctors d ON d.phone = '0912345678'
WHERE p.phone = '0909876543'
  AND NOT EXISTS (
    SELECT 1 FROM Appointments a
    WHERE a.patient_id = p.patient_id
      AND a.doctor_id = d.doctor_id
      AND DATE(a.appointment_date) = DATE(DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 18 DAY))
  )
LIMIT 1;

INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status, note)
SELECT
    p.patient_id,
    d.doctor_id,
    DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 12 DAY),
    'done',
    'Theo dõi sau xét nghiệm'
FROM Patients p
JOIN Doctors d ON d.phone = '0933456789'
WHERE p.phone = '0966543210'
  AND NOT EXISTS (
    SELECT 1 FROM Appointments a
    WHERE a.patient_id = p.patient_id
      AND a.doctor_id = d.doctor_id
      AND DATE(a.appointment_date) = DATE(DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 12 DAY))
  )
LIMIT 1;

INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status, note)
SELECT
    p.patient_id,
    d.doctor_id,
    DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 9 DAY),
    'confirmed',
    'Đặt lịch kiểm tra tổng quát'
FROM Patients p
JOIN Doctors d ON d.phone = '0900000001'
WHERE p.phone = '0933999000'
  AND NOT EXISTS (
    SELECT 1 FROM Appointments a
    WHERE a.patient_id = p.patient_id
      AND a.doctor_id = d.doctor_id
      AND DATE(a.appointment_date) = DATE(DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 9 DAY))
  )
LIMIT 1;

INSERT INTO Payments (patient_id, appointment_id, total_amount, method, status, payment_date)
SELECT
    a.patient_id,
    a.appointment_id,
    280000,
    'Tiền mặt',
    'paid',
    DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 25 DAY)
FROM Appointments a
JOIN Patients p ON p.patient_id = a.patient_id
WHERE p.phone = '0987654321'
  AND DATE(a.appointment_date) = DATE(DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 25 DAY))
  AND NOT EXISTS (
    SELECT 1 FROM Payments pay
    WHERE pay.appointment_id = a.appointment_id
      AND pay.total_amount = 280000
      AND pay.status = 'paid'
  )
LIMIT 1;

INSERT INTO Payments (patient_id, appointment_id, total_amount, method, status, payment_date)
SELECT
    a.patient_id,
    a.appointment_id,
    420000,
    'Chuyển khoản',
    'paid',
    DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 18 DAY)
FROM Appointments a
JOIN Patients p ON p.patient_id = a.patient_id
WHERE p.phone = '0909876543'
  AND DATE(a.appointment_date) = DATE(DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 18 DAY))
  AND NOT EXISTS (
    SELECT 1 FROM Payments pay
    WHERE pay.appointment_id = a.appointment_id
      AND pay.total_amount = 420000
      AND pay.status = 'paid'
  )
LIMIT 1;

INSERT INTO Payments (patient_id, appointment_id, total_amount, method, status, payment_date)
SELECT
    a.patient_id,
    a.appointment_id,
    360000,
    'Thẻ ngân hàng',
    'paid',
    DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 12 DAY)
FROM Appointments a
JOIN Patients p ON p.patient_id = a.patient_id
WHERE p.phone = '0966543210'
  AND DATE(a.appointment_date) = DATE(DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 12 DAY))
  AND NOT EXISTS (
    SELECT 1 FROM Payments pay
    WHERE pay.appointment_id = a.appointment_id
      AND pay.total_amount = 360000
      AND pay.status = 'paid'
  )
LIMIT 1;

INSERT INTO Payments (patient_id, appointment_id, total_amount, method, status, payment_date)
SELECT
    a.patient_id,
    a.appointment_id,
    190000,
    'Ví điện tử',
    'unpaid',
    DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 9 DAY)
FROM Appointments a
JOIN Patients p ON p.patient_id = a.patient_id
WHERE p.phone = '0933999000'
  AND DATE(a.appointment_date) = DATE(DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 9 DAY))
  AND NOT EXISTS (
    SELECT 1 FROM Payments pay
    WHERE pay.appointment_id = a.appointment_id
      AND pay.total_amount = 190000
      AND pay.status = 'unpaid'
  )
LIMIT 1;

INSERT INTO Invoices (payment_id, service_id, quantity, unit_price)
SELECT
    pay.payment_id,
    s.service_id,
    1,
    pay.total_amount
FROM Payments pay
JOIN Services s ON s.service_code = 'DV001'
WHERE pay.total_amount = 280000
  AND pay.status = 'paid'
  AND NOT EXISTS (
    SELECT 1 FROM Invoices i
    WHERE i.payment_id = pay.payment_id
  )
LIMIT 1;

INSERT INTO Invoices (payment_id, service_id, quantity, unit_price)
SELECT
    pay.payment_id,
    s.service_id,
    1,
    pay.total_amount
FROM Payments pay
JOIN Services s ON s.service_code = 'DV003'
WHERE pay.total_amount = 420000
  AND pay.status = 'paid'
  AND NOT EXISTS (
    SELECT 1 FROM Invoices i
    WHERE i.payment_id = pay.payment_id
  )
LIMIT 1;

INSERT INTO Invoices (payment_id, service_id, quantity, unit_price)
SELECT
    pay.payment_id,
    s.service_id,
    1,
    pay.total_amount
FROM Payments pay
JOIN Services s ON s.service_code = 'DV007'
WHERE pay.total_amount = 360000
  AND pay.status = 'paid'
  AND NOT EXISTS (
    SELECT 1 FROM Invoices i
    WHERE i.payment_id = pay.payment_id
  )
LIMIT 1;

INSERT INTO Invoices (payment_id, service_id, quantity, unit_price)
SELECT
    pay.payment_id,
    s.service_id,
    1,
    pay.total_amount
FROM Payments pay
JOIN Services s ON s.service_code = 'DV004'
WHERE pay.total_amount = 190000
  AND pay.status = 'unpaid'
  AND NOT EXISTS (
    SELECT 1 FROM Invoices i
    WHERE i.payment_id = pay.payment_id
  )
LIMIT 1;
