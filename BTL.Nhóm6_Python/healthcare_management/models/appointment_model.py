from database.db import fetch_all, fetch_one, execute

class AppointmentModel:

    @staticmethod
    def _build_role_scoped_query(base_conditions, date_mode=None, date_value=None, search=None, doctor_id=None, service_name=None, status=None):
        query = """
            SELECT
                a.appointment_id,
                a.patient_id,
                a.doctor_id,
                a.appointment_date,
                a.status,
                a.note,
                p.name AS patient_name,
                p.phone AS patient_phone,
                d.name AS doctor_name,
                d.specialty AS doctor_specialty,
                COALESCE(GROUP_CONCAT(DISTINCT s.service_name ORDER BY s.service_name SEPARATOR ', '), '') AS service_names
            FROM Appointments a
            JOIN Patients p ON a.patient_id = p.patient_id
            JOIN Doctors d ON a.doctor_id = d.doctor_id
            LEFT JOIN Payments pay ON pay.appointment_id = a.appointment_id
            LEFT JOIN Invoices i ON i.payment_id = pay.payment_id
            LEFT JOIN Services s ON s.service_id = i.service_id
            WHERE 1=1
        """
        params = []

        for condition, value in base_conditions:
            query += f" AND {condition}"
            if value is not None:
                params.append(value)

        if date_mode == "today":
            query += " AND DATE(a.appointment_date) = CURDATE()"
        elif date_mode == "tomorrow":
            query += " AND DATE(a.appointment_date) = DATE_ADD(CURDATE(), INTERVAL 1 DAY)"
        elif date_mode == "by-date" and date_value:
            query += " AND DATE(a.appointment_date) = ?"
            params.append(date_value)

        if search:
            like_value = f"%{search.strip()}%"
            query += """
                AND (
                    p.name LIKE ?
                    OR p.phone LIKE ?
                    OR s.service_name LIKE ?
                )
            """
            params.extend([like_value, like_value, like_value])

        if doctor_id is not None:
            query += " AND a.doctor_id = ?"
            params.append(doctor_id)

        if service_name:
            query += " AND s.service_name LIKE ?"
            params.append(f"%{service_name.strip()}%")

        if status:
            query += " AND a.status = ?"
            params.append(status)

        query += """
            GROUP BY
                a.appointment_id,
                a.patient_id,
                a.doctor_id,
                a.appointment_date,
                a.status,
                a.note,
                p.name,
                p.phone,
                d.name,
                d.specialty
            ORDER BY a.appointment_date ASC, a.appointment_id ASC
        """
        return query, tuple(params)

    @staticmethod
    def get_all():
        return fetch_all("""
            SELECT a.*, p.name AS patient_name, d.name AS doctor_name
            FROM Appointments a
            JOIN Patients p ON a.patient_id = p.patient_id
            JOIN Doctors d ON a.doctor_id = d.doctor_id
        """)

    @staticmethod
    def get_for_staff_admin(date_mode=None, date_value=None, search=None, doctor_id=None, service_name=None, status=None):
        query, params = AppointmentModel._build_role_scoped_query(
            base_conditions=[],
            date_mode=date_mode,
            date_value=date_value,
            search=search,
            doctor_id=doctor_id,
            service_name=service_name,
            status=status,
        )
        return fetch_all(query, params)

    @staticmethod
    def get_for_doctor(doctor_id, date_mode=None, date_value=None, search=None, service_name=None, status=None):
        query, params = AppointmentModel._build_role_scoped_query(
            base_conditions=[("a.doctor_id = ?", doctor_id)],
            date_mode=date_mode,
            date_value=date_value,
            search=search,
            doctor_id=None,
            service_name=service_name,
            status=status,
        )
        return fetch_all(query, params)

    @staticmethod
    def get_for_patient(patient_id, date_mode=None, date_value=None, search=None, doctor_id=None, service_name=None, status=None):
        query, params = AppointmentModel._build_role_scoped_query(
            base_conditions=[("a.patient_id = ?", patient_id)],
            date_mode=date_mode,
            date_value=date_value,
            search=search,
            doctor_id=doctor_id,
            service_name=service_name,
            status=status,
        )
        return fetch_all(query, params)

    @staticmethod
    def get_detail_with_joins(appointment_id):
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
                p.address AS patient_address,
                d.name AS doctor_name,
                d.specialty AS doctor_specialty,
                COALESCE(GROUP_CONCAT(DISTINCT s.service_name ORDER BY s.service_name SEPARATOR ', '), '') AS service_names
            FROM Appointments a
            JOIN Patients p ON a.patient_id = p.patient_id
            JOIN Doctors d ON a.doctor_id = d.doctor_id
            LEFT JOIN Payments pay ON pay.appointment_id = a.appointment_id
            LEFT JOIN Invoices i ON i.payment_id = pay.payment_id
            LEFT JOIN Services s ON s.service_id = i.service_id
            WHERE a.appointment_id = ?
            GROUP BY
                a.appointment_id,
                a.patient_id,
                a.doctor_id,
                a.appointment_date,
                a.status,
                a.note,
                p.name,
                p.phone,
                p.dob,
                p.address,
                d.name,
                d.specialty
            ORDER BY a.appointment_date ASC, a.appointment_id ASC
            """,
            (appointment_id,),
        )

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

    @staticmethod
    def update_intake_checkin(appointment_id, patient_id, doctor_id, intake_datetime, status, note):
        return execute(
            """
            UPDATE Appointments
            SET doctor_id = ?, appointment_date = ?, status = ?, note = ?
            WHERE appointment_id = ? AND patient_id = ?
            """,
            (doctor_id, intake_datetime, status, note, appointment_id, patient_id),
        )
