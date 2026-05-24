SET NOCOUNT ON;
SET XACT_ABORT ON;

IF COL_LENGTH('dbo.Payments', 'method') IS NULL
BEGIN
    ALTER TABLE dbo.Payments ADD method NVARCHAR(50) NULL;
END;

IF COL_LENGTH('dbo.Services', 'category') IS NOT NULL
BEGIN
    ALTER TABLE dbo.Services ALTER COLUMN category NVARCHAR(100) NULL;
END;

IF COL_LENGTH('dbo.Medicines', 'active_ingredient') IS NOT NULL
BEGIN
    ALTER TABLE dbo.Medicines ALTER COLUMN active_ingredient NVARCHAR(100) NULL;
END;

IF COL_LENGTH('dbo.Medicines', 'category') IS NOT NULL
BEGIN
    ALTER TABLE dbo.Medicines ALTER COLUMN category NVARCHAR(100) NULL;
END;

IF COL_LENGTH('dbo.Medicines', 'unit') IS NOT NULL
BEGIN
    ALTER TABLE dbo.Medicines ALTER COLUMN unit NVARCHAR(30) NULL;
END;

IF COL_LENGTH('dbo.Medicines', 'supplier') IS NOT NULL
BEGIN
    ALTER TABLE dbo.Medicines ALTER COLUMN supplier NVARCHAR(100) NULL;
END;

DECLARE @drop_payment_checks NVARCHAR(MAX) = N'';
SELECT @drop_payment_checks = @drop_payment_checks
    + N'ALTER TABLE dbo.Payments DROP CONSTRAINT ' + QUOTENAME(name) + N';'
FROM sys.check_constraints
WHERE parent_object_id = OBJECT_ID('dbo.Payments');

IF @drop_payment_checks <> N''
BEGIN
    EXEC sp_executesql @drop_payment_checks;
END;

IF NOT EXISTS (
    SELECT 1
    FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('dbo.Payments')
      AND name = 'CK_Payments_Status'
)
BEGIN
    ALTER TABLE dbo.Payments
    ADD CONSTRAINT CK_Payments_Status
    CHECK (status IN ('paid', 'unpaid', 'failed', 'refunded', 'cancelled'));
END;

GO

BEGIN TRANSACTION;

DELETE FROM BackupRestoreRequests;
DELETE FROM BackupJobs;
DELETE FROM BackupRecords;
DELETE FROM BackupSettings;
DELETE FROM Prescriptions;
DELETE FROM Invoices;
DELETE FROM Payments;
DELETE FROM MedicalRecords;
DELETE FROM Appointments;
DELETE FROM Notifications;
DELETE FROM UserSettings;
DELETE FROM Doctors;
DELETE FROM Patients;
DELETE FROM Medicines;
DELETE FROM Services;
DELETE FROM Users;

IF OBJECT_ID('BackupRestoreRequests', 'U') IS NOT NULL DBCC CHECKIDENT ('BackupRestoreRequests', RESEED, 0) WITH NO_INFOMSGS;
IF OBJECT_ID('Prescriptions', 'U') IS NOT NULL DBCC CHECKIDENT ('Prescriptions', RESEED, 0) WITH NO_INFOMSGS;
IF OBJECT_ID('Invoices', 'U') IS NOT NULL DBCC CHECKIDENT ('Invoices', RESEED, 0) WITH NO_INFOMSGS;
IF OBJECT_ID('Payments', 'U') IS NOT NULL DBCC CHECKIDENT ('Payments', RESEED, 0) WITH NO_INFOMSGS;
IF OBJECT_ID('MedicalRecords', 'U') IS NOT NULL DBCC CHECKIDENT ('MedicalRecords', RESEED, 0) WITH NO_INFOMSGS;
IF OBJECT_ID('Appointments', 'U') IS NOT NULL DBCC CHECKIDENT ('Appointments', RESEED, 0) WITH NO_INFOMSGS;
IF OBJECT_ID('Notifications', 'U') IS NOT NULL DBCC CHECKIDENT ('Notifications', RESEED, 0) WITH NO_INFOMSGS;
IF OBJECT_ID('Doctors', 'U') IS NOT NULL DBCC CHECKIDENT ('Doctors', RESEED, 0) WITH NO_INFOMSGS;
IF OBJECT_ID('Patients', 'U') IS NOT NULL DBCC CHECKIDENT ('Patients', RESEED, 0) WITH NO_INFOMSGS;
IF OBJECT_ID('Medicines', 'U') IS NOT NULL DBCC CHECKIDENT ('Medicines', RESEED, 0) WITH NO_INFOMSGS;
IF OBJECT_ID('Services', 'U') IS NOT NULL DBCC CHECKIDENT ('Services', RESEED, 0) WITH NO_INFOMSGS;
IF OBJECT_ID('Users', 'U') IS NOT NULL DBCC CHECKIDENT ('Users', RESEED, 0) WITH NO_INFOMSGS;

DECLARE @password NVARCHAR(255) = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92';

INSERT INTO Users (username, password, role, is_active, created_at) VALUES
('admin', @password, 'admin', 1, GETDATE()),
('doctor1', @password, 'doctor', 1, GETDATE()),
('staff1', @password, 'staff', 1, GETDATE()),
('nam.nguyen', @password, 'admin', 1, GETDATE()),
('mai.tran', @password, 'doctor', 1, GETDATE()),
('cuong.le', @password, 'doctor', 1, GETDATE()),
('lan.pham', @password, 'staff', 1, GETDATE()),
('tuan.hoang', @password, 'staff', 1, GETDATE()),
('huong.vu', @password, 'staff', 0, GETDATE()),
('quan.do', @password, 'staff', 1, GETDATE()),
('hoa.nguyen', @password, 'staff', 0, GETDATE()),
('dung.bui', @password, 'staff', 1, GETDATE()),
('kien.truong', @password, 'patient', 1, GETDATE());

INSERT INTO Patients (name, dob, gender, phone, cccd, email, address, user_id, is_active, created_at) VALUES
(N'Lễ tân hệ thống', '2000-01-01', N'Nữ', '0123456789', '000000000001', 'staff1@careplus.vn', N'TP.HCM', 3, 1, GETDATE()),
(N'Nguyễn Văn Nam', '1990-05-24', N'Nam', '0987654321', '000000000002', 'nam.nguyen@gmail.com', N'Quận 1, TP.HCM', 4, 1, GETDATE()),
(N'Phạm Thị Lan', '1992-08-14', N'Nữ', '0909876543', '000000000003', 'lan.pham@gmail.com', N'Quận 3, TP.HCM', 7, 1, GETDATE()),
(N'Hoàng Anh Tuấn', '1989-11-20', N'Nam', '0988765432', '000000000004', 'tuan.hoang@gmail.com', N'Quận 7, TP.HCM', 8, 1, GETDATE()),
(N'Vũ Thị Hương', '1993-03-16', N'Nữ', '0977654321', '000000000005', 'huong.vu@gmail.com', N'Quận 10, TP.HCM', 9, 0, GETDATE()),
(N'Đỗ Minh Quân', '1996-09-28', N'Nam', '0966543210', '000000000006', 'quan.do@gmail.com', N'Quận Bình Thạnh, TP.HCM', 10, 1, GETDATE()),
(N'Nguyễn Thị Hoa', '1988-12-02', N'Nữ', '0908111222', '000000000007', 'hoa.nguyen@gmail.com', N'Quận Phú Nhuận, TP.HCM', 11, 0, GETDATE()),
(N'Bùi Văn Dũng', '1991-06-07', N'Nam', '0982333444', '000000000008', 'dung.bui@gmail.com', N'Quận Tân Bình, TP.HCM', 12, 1, GETDATE()),
(N'Trương Văn Kiên', '1994-01-11', N'Nam', '0933999000', '000000000009', 'kien.truong@gmail.com', N'Quận 5, TP.HCM', 13, 1, GETDATE());

INSERT INTO Doctors (name, specialty, phone, email, user_id, is_active, work_status, created_at, updated_at) VALUES
(N'Bác sĩ Minh', N'Nội khoa', '0900000001', 'minh@gmail.com', 2, 1, N'Đang làm việc', GETDATE(), GETDATE()),
(N'Trần Thị Mai', N'Tim mạch', '0912345678', 'mai.tran@gmail.com', 5, 1, N'Đang làm việc', GETDATE(), GETDATE()),
(N'Lê Văn Cường', N'Da liễu', '0933456789', 'cuong.le@gmail.com', 6, 1, N'Đang làm việc', GETDATE(), GETDATE());

INSERT INTO Services (service_code, service_name, category, duration, price, description, is_visible, is_active) VALUES
('DV001', N'Khám tổng quát', N'Khám bệnh', 30, 200000, N'Khám sức khỏe tổng quát', 1, 1),
('DV002', N'Xét nghiệm máu', N'Xét nghiệm', 20, 150000, N'Xét nghiệm máu tổng quát', 1, 1),
('DV003', N'Khám chuyên khoa Nội tiết', N'Khám bệnh', 45, 200000, N'Khám và tư vấn bệnh lý nội tiết', 1, 1),
('DV004', N'Xét nghiệm đường huyết', N'Xét nghiệm', 10, 80000, N'Kiểm tra lượng đường trong máu', 1, 1),
('DV005', N'Xét nghiệm mỡ máu', N'Xét nghiệm', 15, 150000, N'Định lượng Cholesterol, Triglycerid, HDL, LDL', 1, 1),
('DV006', N'Siêu âm ổ bụng tổng quát', N'Chẩn đoán hình ảnh', 30, 250000, N'Siêu âm 4D ổ bụng', 1, 0),
('DV007', N'Chụp X-quang phổi', N'Chẩn đoán hình ảnh', 20, 200000, N'Chụp X-quang tim phổi thẳng', 1, 1),
('DV008', N'Điện tâm đồ (ECG)', N'Thăm dò chức năng', 15, 120000, N'Đo điện tim đồ 12 chuyển đạo', 1, 0),
('DV009', N'Vật lý trị liệu', N'Điều trị', 30, 180000, N'Phục hồi chức năng cơ xương khớp', 1, 1);

INSERT INTO Medicines (medicine_code, name, active_ingredient, category, unit, supplier, quantity, import_price, price, description, is_active) VALUES
('TH001', N'Paracetamol', N'Paracetamol', N'Giảm đau - Hạ sốt', N'Viên', N'Dược Hậu Giang', 100, 3500, 5000, N'Thuốc giảm đau hạ sốt', 1),
('TH002', N'Amoxicillin', N'Amoxicillin', N'Kháng sinh', N'Viên', N'Traphaco', 50, 7000, 10000, N'Kháng sinh phổ rộng', 1);

INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status, note) VALUES
(1, 1, GETDATE(), 'pending', NULL),
(2, 2, GETDATE(), 'pending', NULL),
(2, 1, DATEADD(DAY, -25, GETDATE()), 'done', N'Tái khám định kỳ'),
(3, 2, DATEADD(DAY, -18, GETDATE()), 'done', N'Khám chuyên khoa tim mạch'),
(6, 3, DATEADD(DAY, -12, GETDATE()), 'done', N'Theo dõi sau xét nghiệm'),
(9, 1, DATEADD(DAY, -9, GETDATE()), 'confirmed', N'Đặt lịch kiểm tra tổng quát');

INSERT INTO MedicalRecords (patient_id, doctor_id, appointment_id, diagnosis, treatment, created_at, record_status, finalized_at, updated_at) VALUES
(1, 1, 1, N'Sốt', N'Uống thuốc', GETDATE(), N'completed', GETDATE(), GETDATE()),
(2, 2, 2, N'Đau bụng', N'Nghỉ ngơi', GETDATE(), N'completed', GETDATE(), GETDATE());

INSERT INTO Prescriptions (record_id, medicine_id, quantity, updated_at, dispensed_at) VALUES
(1, 1, 10, GETDATE(), NULL),
(2, 2, 7, GETDATE(), NULL);

INSERT INTO Payments (patient_id, appointment_id, total_amount, method, status, payment_date) VALUES
(1, 1, 200000, N'Chuyển khoản', 'paid', GETDATE()),
(2, 2, 150000, N'Tiền mặt', 'unpaid', GETDATE()),
(2, 2, 350000, N'Thẻ ngân hàng', 'paid', GETDATE()),
(1, 1, 120000, N'Ví điện tử', 'failed', GETDATE()),
(3, 4, 500000, N'Chuyển khoản', 'refunded', GETDATE()),
(2, 3, 280000, N'Tiền mặt', 'paid', DATEADD(DAY, -25, GETDATE())),
(3, 4, 420000, N'Chuyển khoản', 'paid', DATEADD(DAY, -18, GETDATE())),
(6, 5, 360000, N'Thẻ ngân hàng', 'paid', DATEADD(DAY, -12, GETDATE())),
(9, 6, 190000, N'Ví điện tử', 'unpaid', DATEADD(DAY, -9, GETDATE()));

INSERT INTO Invoices (payment_id, service_id, quantity, unit_price) VALUES
(1, 1, 1, 200000),
(2, 2, 1, 150000),
(3, 3, 1, 350000),
(4, 4, 1, 120000),
(5, 5, 1, 500000),
(6, 1, 1, 280000),
(7, 3, 1, 420000),
(8, 7, 1, 360000),
(9, 4, 1, 190000);

INSERT INTO Notifications (user_id, title, content, type, target_page, is_read, created_at) VALUES
(1, N'Sao lưu dữ liệu thành công', N'Dữ liệu hệ thống đã được sao lưu lúc 02:00 AM', N'backup', N'settings', 0, SYSDATETIME()),
(1, N'Cảnh báo tồn kho thuốc', N'Một số thuốc đang ở ngưỡng sắp hết hàng', N'inventory', N'dashboard', 0, SYSDATETIME());

INSERT INTO UserSettings (user_id, gender, dob, address, backup_mode, updated_at)
SELECT user_id, N'Nam', NULL, N'', 'cloud', GETDATE()
FROM Users;

INSERT INTO BackupSettings (
    setting_id, storage_location, storage_path, auto_backup, include_database, include_attachments,
    compress_data, email_notification, retention_days, schedule_time,
    schedule_frequency, encryption_enabled, updated_by_user_id, updated_at
) VALUES (
    1, 'local', N'D:\khambenh\backups', 0, 1, 1,
    1, 0, 30, '02:00',
    'daily', 0, 1, SYSDATETIME()
);

COMMIT TRANSACTION;

SELECT 'Users' AS table_name, COUNT(*) AS total FROM Users
UNION ALL SELECT 'Patients', COUNT(*) FROM Patients
UNION ALL SELECT 'Doctors', COUNT(*) FROM Doctors
UNION ALL SELECT 'Services', COUNT(*) FROM Services
UNION ALL SELECT 'Medicines', COUNT(*) FROM Medicines
UNION ALL SELECT 'Appointments', COUNT(*) FROM Appointments
UNION ALL SELECT 'MedicalRecords', COUNT(*) FROM MedicalRecords
UNION ALL SELECT 'Prescriptions', COUNT(*) FROM Prescriptions
UNION ALL SELECT 'Payments', COUNT(*) FROM Payments
UNION ALL SELECT 'Invoices', COUNT(*) FROM Invoices
UNION ALL SELECT 'Notifications', COUNT(*) FROM Notifications;
