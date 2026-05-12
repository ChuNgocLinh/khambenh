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
    name VARCHAR(100),
    quantity INT,
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
-- 11. INSERT DỮ LIỆU MẪU
-- ========================================
INSERT IGNORE INTO Users (username, password, role) VALUES 
('admin','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','admin'),
('doctor1','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','doctor'),
('staff1','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','patient');

INSERT INTO Patients (name, dob, gender, phone, address, user_id)
SELECT 'Nguyễn Văn A','2000-01-01','Nam','0123456789','Hà Nội',
       (SELECT user_id FROM Users WHERE username='staff1' LIMIT 1)
WHERE NOT EXISTS (
    SELECT 1 FROM Patients WHERE phone='0123456789'
);

INSERT INTO Patients (name, dob, gender, phone, address, user_id)
SELECT 'Trần Thị B','1995-05-10','Nữ','0987654321','HCM', NULL
WHERE NOT EXISTS (
    SELECT 1 FROM Patients WHERE phone='0987654321'
);

INSERT INTO Doctors (name, specialty, phone, email, user_id)
SELECT 'Bác sĩ Minh','Nội khoa','0900000001','minh@gmail.com',
       (SELECT user_id FROM Users WHERE username='doctor1' LIMIT 1)
WHERE NOT EXISTS (
    SELECT 1 FROM Doctors WHERE phone='0900000001'
);

INSERT INTO Doctors (name, specialty, phone, email, user_id)
SELECT 'Bác sĩ Hùng','Ngoại khoa','0900000002','hung@gmail.com', NULL
WHERE NOT EXISTS (
    SELECT 1 FROM Doctors WHERE phone='0900000002'
);

INSERT INTO Services (service_name, price)
SELECT 'Khám tổng quát', 200000
WHERE NOT EXISTS (
    SELECT 1 FROM Services WHERE price=200000
);

INSERT INTO Services (service_name, price)
SELECT 'Xét nghiệm máu', 150000
WHERE NOT EXISTS (
    SELECT 1 FROM Services WHERE price=150000
);

INSERT INTO Medicines (name, quantity, price)
SELECT 'Paracetamol', 100, 5000
WHERE NOT EXISTS (
    SELECT 1 FROM Medicines WHERE name='Paracetamol' AND price=5000
);

INSERT INTO Medicines (name, quantity, price)
SELECT 'Amoxicillin', 50, 10000
WHERE NOT EXISTS (
    SELECT 1 FROM Medicines WHERE name='Amoxicillin' AND price=10000
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
           WHERE phone='0900000002'
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
            WHERE phone='0900000002'
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
           WHERE phone='0900000002'
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
            WHERE phone='0900000002'
            ORDER BY CASE WHEN user_id IS NULL THEN 1 ELSE 0 END, doctor_id ASC
            LIMIT 1
        )
  )
LIMIT 1;

INSERT INTO Payments (patient_id, appointment_id, total_amount, status)
SELECT p.patient_id, a.appointment_id, 200000, 'paid'
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

INSERT INTO Payments (patient_id, appointment_id, total_amount, status)
SELECT p.patient_id, a.appointment_id, 150000, 'unpaid'
FROM Patients p
LEFT JOIN Appointments a ON a.patient_id = p.patient_id
LEFT JOIN Doctors d ON d.doctor_id = a.doctor_id
WHERE p.phone='0987654321'
  AND (d.phone='0900000002' OR d.phone IS NULL)
  AND NOT EXISTS (
      SELECT 1 FROM Payments pay
      WHERE pay.patient_id = p.patient_id AND pay.total_amount=150000 AND pay.status='unpaid'
  )
ORDER BY a.appointment_id ASC
LIMIT 1;
