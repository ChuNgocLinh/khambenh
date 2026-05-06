from database.db import fetch_all, execute

class AppointmentModel:

    @staticmethod
    def get_all():
        return fetch_all("""
            SELECT a.*, p.name AS patient_name, d.name AS doctor_name
            FROM Appointments a
            JOIN Patients p ON a.patient_id = p.patient_id
            JOIN Doctors d ON a.doctor_id = d.doctor_id
        """)

    @staticmethod
    def create(patient_id, doctor_id, date):
        query = """
        INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status)
        VALUES (?, ?, ?, 'pending')
        """
        return execute(query, (patient_id, doctor_id, date))

    @staticmethod
    def update_status(appointment_id, status):
        return execute(
            "UPDATE Appointments SET status=? WHERE appointment_id=?",
            (status, appointment_id)
        )