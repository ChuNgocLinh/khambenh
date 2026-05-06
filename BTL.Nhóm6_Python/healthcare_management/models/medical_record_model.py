from database.db import fetch_all, execute

class MedicalRecordModel:

    @staticmethod
    def get_by_patient(patient_id):
        return fetch_all("""
            SELECT * FROM MedicalRecords WHERE patient_id=?
        """, (patient_id,)) 

    @staticmethod
    def create(appointment_id, diagnosis, treatment):
        query = """
        INSERT INTO MedicalRecords (appointment_id, diagnosis, treatment)
        VALUES (?, ?, ?)
        """
        return execute(query, (appointment_id, diagnosis, treatment))