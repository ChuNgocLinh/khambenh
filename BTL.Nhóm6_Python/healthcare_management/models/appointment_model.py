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
    def get_by_patient(patient_id):
        return fetch_all("""
            SELECT a.*, d.name AS doctor_name, d.specialty
            FROM Appointments a
            JOIN Doctors d ON a.doctor_id = d.doctor_id
            WHERE a.patient_id = ?
            ORDER BY a.appointment_date DESC
        """, (patient_id,))

    @staticmethod
    def get_by_doctor(doctor_id):
        return fetch_all("""
            SELECT a.*, p.name AS patient_name, p.phone AS patient_phone
            FROM Appointments a
            JOIN Patients p ON a.patient_id = p.patient_id
            WHERE a.doctor_id = ?
            ORDER BY a.appointment_date ASC
        """, (doctor_id,))

    @staticmethod
    def create(patient_id, doctor_id, date, status='pending'):
        query = """
        INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status)
        VALUES (?, ?, ?, ?)
        """
        return execute(query, (patient_id, doctor_id, date, status))

    @staticmethod
    def update_status(appointment_id, status):
        return execute(
            "UPDATE Appointments SET status=? WHERE appointment_id=?",
            (status, appointment_id)
        )