from database.db import fetch_all, fetch_one, execute

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
    def get_upcoming_by_patient(patient_id, current_datetime):
        return fetch_all(
            """
            SELECT a.*, d.name AS doctor_name, d.specialty
            FROM Appointments a
            JOIN Doctors d ON a.doctor_id = d.doctor_id
            WHERE a.patient_id = ?
              AND a.appointment_date >= ?
              AND a.status IN ('pending', 'confirmed', 'in_progress')
            ORDER BY a.appointment_date ASC
            """,
            (patient_id, current_datetime),
        )

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
    def create(patient_id, doctor_id, date, status='pending', note=''):
        query = """
        INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status, note)
        VALUES (?, ?, ?, ?, ?)
        """
        return execute(query, (patient_id, doctor_id, date, status, note))

    @staticmethod
    def has_conflict(doctor_id, patient_id, appointment_datetime):
        doctor_conflict = fetch_one(
            """
            SELECT appointment_id
            FROM Appointments
            WHERE doctor_id = ?
              AND appointment_date = ?
              AND status <> 'cancelled'
            """,
            (doctor_id, appointment_datetime),
        )

        patient_conflict = fetch_one(
            """
            SELECT appointment_id
            FROM Appointments
            WHERE patient_id = ?
              AND appointment_date = ?
              AND status <> 'cancelled'
            """,
            (patient_id, appointment_datetime),
        )

        return bool(doctor_conflict), bool(patient_conflict)

    @staticmethod
    def update_status(appointment_id, status):
        return execute(
            "UPDATE Appointments SET status=? WHERE appointment_id=?",
            (status, appointment_id)
        )
