from database.db import fetch_all, fetch_one, execute

class PatientModel:

    @staticmethod
    def get_all():
        return fetch_all(
            """
            SELECT *
            FROM Patients
            WHERE COALESCE(is_active, 1) = 1
            ORDER BY patient_id DESC
            """
        )

    @staticmethod
    def get_by_doctor(doctor_id):
        return fetch_all(
            """
            SELECT
                p.*,
                COALESCE(ap.appointment_count, 0) AS appointment_count,
                COALESCE(ap.active_appointment_count, 0) AS active_appointment_count,
                ap.last_visit,
                ap.next_visit,
                ap.latest_appointment_at,
                COALESCE(mr.record_count, 0) AS record_count,
                COALESCE(mr.draft_record_count, 0) AS draft_record_count,
                mr.last_record_at
            FROM Patients p
            LEFT JOIN (
                SELECT
                    patient_id,
                    COUNT(*) AS appointment_count,
                    SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) AS active_appointment_count,
                    MAX(CASE WHEN status = 'done' THEN appointment_date ELSE NULL END) AS last_visit,
                    MIN(CASE
                        WHEN status IN ('pending', 'confirmed', 'in_progress')
                         AND appointment_date >= CURRENT_TIMESTAMP
                        THEN appointment_date
                        ELSE NULL
                    END) AS next_visit,
                    MAX(appointment_date) AS latest_appointment_at
                FROM Appointments
                WHERE doctor_id = ?
                GROUP BY patient_id
            ) ap ON ap.patient_id = p.patient_id
            LEFT JOIN (
                SELECT
                    patient_id,
                    COUNT(*) AS record_count,
                    SUM(CASE WHEN record_status = 'draft' THEN 1 ELSE 0 END) AS draft_record_count,
                    MAX(COALESCE(finalized_at, updated_at, created_at)) AS last_record_at
                FROM MedicalRecords
                WHERE doctor_id = ?
                GROUP BY patient_id
            ) mr ON mr.patient_id = p.patient_id
            WHERE (ap.patient_id IS NOT NULL OR mr.patient_id IS NOT NULL)
              AND COALESCE(p.is_active, 1) = 1
            ORDER BY COALESCE(ap.last_visit, mr.last_record_at, ap.latest_appointment_at, p.created_at) DESC,
                     p.patient_id DESC
            """,
            (doctor_id, doctor_id),
        )

    @staticmethod
    def get_by_id(patient_id):
        return fetch_one("SELECT * FROM Patients WHERE patient_id=?", (patient_id,))

    @staticmethod
    def get_by_phone(phone):
        return fetch_one(
            "SELECT * FROM Patients WHERE phone=? ORDER BY patient_id DESC",
            (phone,),
        )

    @staticmethod
    def get_by_cccd(cccd):
        return fetch_one(
            "SELECT * FROM Patients WHERE cccd=? ORDER BY patient_id DESC",
            (cccd,),
        )

    @staticmethod
    def create(
        name,
        dob,
        gender,
        phone,
        cccd,
        address,
        email,
        occupation,
        intake_notes,
        patient_type,
    ):
        query = """
        INSERT INTO Patients (
            name, dob, gender, phone, cccd, address, email, occupation, intake_notes, patient_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return execute(
            query,
            (name, dob, gender, phone, cccd, address, email, occupation, intake_notes, patient_type),
        )

    @staticmethod
    def update(
        patient_id,
        name,
        dob,
        gender,
        phone,
        cccd,
        address,
        email,
        occupation,
        intake_notes,
        patient_type,
    ):
        query = """
        UPDATE Patients 
        SET name=?, dob=?, gender=?, phone=?, cccd=?, address=?, email=?, occupation=?, intake_notes=?, patient_type=?
        WHERE patient_id=?
        """
        return execute(
            query,
            (
                name,
                dob,
                gender,
                phone,
                cccd,
                address,
                email,
                occupation,
                intake_notes,
                patient_type,
                patient_id,
            ),
        )

    @staticmethod
    def delete(patient_id):
        return execute(
            """
            UPDATE Patients
            SET is_active=0
            WHERE patient_id=?
            """,
            (patient_id,),
        )
