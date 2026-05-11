from config import DB_TYPE
from database.db import execute, fetch_all, fetch_one


class MedicalRecordModel:
    VALID_RECORD_STATUSES = {"draft", "finalized"}

    @staticmethod
    def get_by_patient(patient_id):
        if DB_TYPE == "mysql":
            service_select = "COALESCE(GROUP_CONCAT(DISTINCT s.service_name ORDER BY s.service_name SEPARATOR ', '), '') AS service_names"
        else:
            service_select = "COALESCE(STRING_AGG(CAST(s.service_name AS NVARCHAR(MAX)), ', '), '') AS service_names"

        return fetch_all(
            f"""
            SELECT
                mr.*,
                d.name AS doctor_name,
                d.specialty AS doctor_specialty,
                a.appointment_date,
                a.status AS appointment_status,
                a.note,
                {service_select}
            FROM MedicalRecords mr
            LEFT JOIN Doctors d ON d.doctor_id = mr.doctor_id
            LEFT JOIN Appointments a ON a.appointment_id = mr.appointment_id
            LEFT JOIN Payments pay ON pay.appointment_id = a.appointment_id
            LEFT JOIN Invoices i ON i.payment_id = pay.payment_id
            LEFT JOIN Services s ON s.service_id = i.service_id
            WHERE mr.patient_id=?
            GROUP BY
                mr.record_id,
                mr.patient_id,
                mr.doctor_id,
                mr.appointment_id,
                mr.diagnosis,
                mr.treatment,
                mr.record_status,
                mr.finalized_at,
                mr.updated_at,
                mr.created_at,
                d.name,
                d.specialty,
                a.appointment_date,
                a.status,
                a.note
            ORDER BY mr.created_at DESC, mr.record_id DESC
            """,
            (patient_id,),
        )

    @staticmethod
    def get_by_id(record_id):
        return fetch_one("SELECT * FROM MedicalRecords WHERE record_id=?", (record_id,))

    @staticmethod
    def get_by_appointment(appointment_id):
        if DB_TYPE == "mysql":
            query = "SELECT * FROM MedicalRecords WHERE appointment_id=? ORDER BY record_id DESC LIMIT 1"
        else:
            query = "SELECT TOP 1 * FROM MedicalRecords WHERE appointment_id=? ORDER BY record_id DESC"
        return fetch_one(
            query,
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
