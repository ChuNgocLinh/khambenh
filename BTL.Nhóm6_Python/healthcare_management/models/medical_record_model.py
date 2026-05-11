from database.db import execute, fetch_all, fetch_one


class MedicalRecordModel:
    VALID_RECORD_STATUSES = {"draft", "finalized"}

    @staticmethod
    def get_by_patient(patient_id):
        return fetch_all(
            """
            SELECT mr.*, d.name AS doctor_name
            FROM MedicalRecords mr
            LEFT JOIN Doctors d ON d.doctor_id = mr.doctor_id
            WHERE mr.patient_id=?
            ORDER BY mr.created_at DESC, mr.record_id DESC
            """,
            (patient_id,),
        )

    @staticmethod
    def get_by_id(record_id):
        return fetch_one("SELECT * FROM MedicalRecords WHERE record_id=?", (record_id,))

    @staticmethod
    def get_by_appointment(appointment_id):
        return fetch_one(
            "SELECT * FROM MedicalRecords WHERE appointment_id=? ORDER BY record_id DESC LIMIT 1",
            (appointment_id,),
        )

    @staticmethod
    def create(patient_id, doctor_id, appointment_id, diagnosis, treatment):
        return MedicalRecordModel.save_draft(
            patient_id,
            doctor_id,
            appointment_id,
            diagnosis=diagnosis,
            treatment=treatment,
        )

    @staticmethod
    def save_draft(patient_id, doctor_id, appointment_id, diagnosis="", treatment="", symptoms="", conclusion="", notes=""):
        body = treatment or conclusion or notes or symptoms
        existing = MedicalRecordModel.get_by_appointment(appointment_id)
        if existing:
            return execute(
                """
                UPDATE MedicalRecords
                SET diagnosis=?, treatment=?, record_status='draft', updated_at=CURRENT_TIMESTAMP
                WHERE record_id=?
                """,
                (diagnosis, body, existing.get("record_id")),
            )

        return execute(
            """
            INSERT INTO MedicalRecords
                (patient_id, doctor_id, appointment_id, diagnosis, treatment, record_status, updated_at)
            VALUES (?, ?, ?, ?, ?, 'draft', CURRENT_TIMESTAMP)
            """,
            (patient_id, doctor_id, appointment_id, diagnosis, body),
        )

    @staticmethod
    def finalize(record_id, diagnosis, treatment):
        return execute(
            """
            UPDATE MedicalRecords
            SET diagnosis=?, treatment=?, record_status='finalized',
                finalized_at=CURRENT_TIMESTAMP, updated_at=CURRENT_TIMESTAMP
            WHERE record_id=?
            """,
            (diagnosis, treatment, record_id),
        )
