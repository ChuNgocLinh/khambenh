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
    def has_conflict(doctor_id, patient_id, appointment_datetime, exclude_appointment_id=None):
        doctor_query = """
            SELECT appointment_id
            FROM Appointments
            WHERE doctor_id = ?
              AND appointment_date = ?
              AND status <> 'cancelled'
        """
        doctor_params = [doctor_id, appointment_datetime]
        if exclude_appointment_id is not None:
            doctor_query += " AND appointment_id <> ?"
            doctor_params.append(exclude_appointment_id)

        doctor_conflict = fetch_one(
            doctor_query,
            tuple(doctor_params),
        )

        patient_query = """
            SELECT appointment_id
            FROM Appointments
            WHERE patient_id = ?
              AND appointment_date = ?
              AND status <> 'cancelled'
        """
        patient_params = [patient_id, appointment_datetime]
        if exclude_appointment_id is not None:
            patient_query += " AND appointment_id <> ?"
            patient_params.append(exclude_appointment_id)

        patient_conflict = fetch_one(
            patient_query,
            tuple(patient_params),
        )

        return bool(doctor_conflict), bool(patient_conflict)

    @staticmethod
    def update_status(appointment_id, status):
        return execute(
            "UPDATE Appointments SET status=? WHERE appointment_id=?",
            (status, appointment_id)
        )

    @staticmethod
    def get_management_rows_by_doctor(doctor_id):
        return fetch_all(
            """
            SELECT
                a.appointment_id,
                a.patient_id,
                a.doctor_id,
                a.appointment_date,
                a.status,
                a.note,
                p.name AS patient_name,
                p.phone AS patient_phone,
                p.dob AS patient_dob,
                d.name AS doctor_name,
                d.specialty AS doctor_specialty
            FROM Appointments a
            JOIN Patients p ON a.patient_id = p.patient_id
            JOIN Doctors d ON a.doctor_id = d.doctor_id
            WHERE a.doctor_id = ?
            ORDER BY a.appointment_date DESC
            """,
            (doctor_id,),
        )

    @staticmethod
    def get_by_id(appointment_id):
        return fetch_one(
            """
            SELECT
                a.appointment_id,
                a.patient_id,
                a.doctor_id,
                a.appointment_date,
                a.status,
                a.note,
                p.name AS patient_name,
                p.phone AS patient_phone,
                p.dob AS patient_dob,
                d.name AS doctor_name,
                d.specialty AS doctor_specialty
            FROM Appointments a
            JOIN Patients p ON a.patient_id = p.patient_id
            JOIN Doctors d ON a.doctor_id = d.doctor_id
            WHERE a.appointment_id = ?
            """,
            (appointment_id,),
        )

    @staticmethod
    def update_full(appointment_id, patient_id, doctor_id, appointment_date, status, note):
        return execute(
            """
            UPDATE Appointments
            SET patient_id = ?, doctor_id = ?, appointment_date = ?, status = ?, note = ?
            WHERE appointment_id = ?
            """,
            (patient_id, doctor_id, appointment_date, status, note, appointment_id),
        )
