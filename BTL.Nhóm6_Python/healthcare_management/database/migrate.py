import logging
from database.db import connect

# ================================
# 🏗️ CREATE TABLES
# ================================
def create_tables():
    conn = connect()
    cursor = conn.cursor()

    try:
        # USERS
        cursor.execute("""
        IF OBJECT_ID('Users', 'U') IS NULL
        CREATE TABLE Users (
            user_id INT IDENTITY(1,1) PRIMARY KEY,
            username NVARCHAR(50) UNIQUE NOT NULL,
            password NVARCHAR(255) NOT NULL,
            role NVARCHAR(20) CHECK (role IN ('admin','doctor','patient')) NOT NULL,
            is_active BIT DEFAULT 1,
            created_at DATETIME DEFAULT GETDATE()
        )
        """)

        # PATIENTS
        cursor.execute("""
        IF OBJECT_ID('Patients', 'U') IS NULL
        CREATE TABLE Patients (
            patient_id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100) NOT NULL,
            dob DATE,
            gender NVARCHAR(10),
            phone NVARCHAR(20),
            address NVARCHAR(255),
            user_id INT UNIQUE,
            is_active BIT DEFAULT 1,
            created_at DATETIME DEFAULT GETDATE(),
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
        """)

        # DOCTORS
        cursor.execute("""
        IF OBJECT_ID('Doctors', 'U') IS NULL
        CREATE TABLE Doctors (
            doctor_id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100) NOT NULL,
            specialty NVARCHAR(100),
            phone NVARCHAR(20),
            user_id INT UNIQUE,
            is_active BIT DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
        """)

        # APPOINTMENTS
        cursor.execute("""
        IF OBJECT_ID('Appointments', 'U') IS NULL
        CREATE TABLE Appointments (
            appointment_id INT IDENTITY(1,1) PRIMARY KEY,
            patient_id INT NOT NULL,
            doctor_id INT NOT NULL,
            appointment_date DATETIME,
            status NVARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending','confirmed','done','cancelled')),
            FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
            FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
        )
        """)

        # MEDICAL RECORDS
        cursor.execute("""
        IF OBJECT_ID('MedicalRecords', 'U') IS NULL
        CREATE TABLE MedicalRecords (
            record_id INT IDENTITY(1,1) PRIMARY KEY,
            appointment_id INT NOT NULL,
            diagnosis NVARCHAR(255),
            treatment NVARCHAR(255),
            created_at DATETIME DEFAULT GETDATE(),
            FOREIGN KEY (appointment_id) REFERENCES Appointments(appointment_id)
        )
        """)

        conn.commit()
        print("✅ Tables created successfully")

    except Exception as e:
        conn.rollback()
        logging.error(f"❌ Lỗi tạo bảng: {e}")

    finally:
        cursor.close()
        conn.close()


# ================================
# 🌱 SEED DATA
# ================================
def seed_data():
    conn = connect()
    cursor = conn.cursor()

    try:
        # USERS
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Users)
        INSERT INTO Users (username, password, role)
        VALUES 
        ('admin','123456','admin'),
        ('BS1','123456','doctor'),
        ('Linh','123456','patient')
        """)

        # PATIENT
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Patients)
        INSERT INTO Patients (name, dob, gender, phone, address, user_id)
        VALUES (N'Nguyễn Văn A','2000-01-01',N'Nam','0123456789',N'Hà Nội', 3)
        """)

        # DOCTOR
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Doctors)
        INSERT INTO Doctors (name, specialty, phone, user_id)
        VALUES (N'Bác sĩ Minh',N'Nội khoa','0900000001', 2)
        """)

        conn.commit()
        print("✅ Sample data inserted")

    except Exception as e:
        conn.rollback()
        logging.error(f"❌ Lỗi seed data: {e}")

    finally:
        cursor.close()
        conn.close()


# ================================
# 🚀 RUN
# ================================
if __name__ == "__main__":
    create_tables()
    seed_data()