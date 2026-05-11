from database.db import execute, fetch_all, fetch_one


class PrescriptionModel:
    VALID_STATUSES = {"draft", "issued", "dispensed", "cancelled"}

    @staticmethod
    def get_by_record(record_id):
        return fetch_all(
            """
            SELECT p.*, m.name
            FROM Prescriptions p
            JOIN Medicines m ON p.medicine_id = m.medicine_id
            WHERE p.record_id=?
            """,
            (record_id,),
        )

    @staticmethod
    def get_by_id(prescription_id):
        return fetch_one("SELECT * FROM Prescriptions WHERE prescription_id=?", (prescription_id,))

    @staticmethod
    def get_by_doctor(doctor_id):
        return fetch_all(
            """
            SELECT
                p.*,
                m.name AS medicine_name,
                mr.patient_id,
                mr.doctor_id,
                mr.diagnosis,
                mr.created_at AS prescribed_at,
                pa.name AS patient_name,
                pa.gender AS patient_gender,
                pa.dob AS patient_dob
            FROM Prescriptions p
            JOIN MedicalRecords mr ON mr.record_id = p.record_id
            JOIN Patients pa ON pa.patient_id = mr.patient_id
            JOIN Medicines m ON m.medicine_id = p.medicine_id
            WHERE mr.doctor_id=?
            ORDER BY COALESCE(p.updated_at, mr.created_at) DESC, p.prescription_id DESC
            """,
            (doctor_id,),
        )

    @staticmethod
    def add(record_id, medicine_id, quantity, status="draft"):
        return execute(
            """
            INSERT INTO Prescriptions (record_id, medicine_id, quantity, status, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (record_id, medicine_id, quantity, status),
        )

    @staticmethod
    def update_item(prescription_id, medicine_id, quantity, status):
        return execute(
            """
            UPDATE Prescriptions
            SET medicine_id=?, quantity=?, status=?, updated_at=CURRENT_TIMESTAMP
            WHERE prescription_id=?
            """,
            (medicine_id, quantity, status, prescription_id),
        )

    @staticmethod
    def update_status(prescription_id, status):
        dispensed_sql = ", dispensed_at=CURRENT_TIMESTAMP" if status == "dispensed" else ""
        return execute(
            f"UPDATE Prescriptions SET status=?, updated_at=CURRENT_TIMESTAMP{dispensed_sql} WHERE prescription_id=?",
            (status, prescription_id),
        )
