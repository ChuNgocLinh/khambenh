from database.db import fetch_all

class ReportController:

    @staticmethod
    def revenue():
        return fetch_all("""
            SELECT SUM(total_amount) AS total_revenue
            FROM Payments
            WHERE status='paid'
        """)

    @staticmethod
    def appointments_count():
        return fetch_all("""
            SELECT COUNT(*) AS total_appointments
            FROM Appointments
        """)

    @staticmethod
    def patients_count():
        return fetch_all("""
            SELECT COUNT(*) AS total_patients
            FROM Patients
        """)