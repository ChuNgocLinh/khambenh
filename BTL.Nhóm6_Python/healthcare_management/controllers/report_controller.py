from database.db import fetch_all


class ReportController:

    @staticmethod
    def _coerce_number(value, default=0.0):
        try:
            return float(value or 0)
        except (TypeError, ValueError):
            return float(default)

    @staticmethod
    def _extract_first_numeric(rows, key, default=0.0):
        if not isinstance(rows, list) or not rows:
            return float(default)
        first = rows[0] if isinstance(rows[0], dict) else {}
        return ReportController._coerce_number(first.get(key), default)

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

    @staticmethod
    def get_core_totals():
        # Return a stable shape so views can render safely even when DB rows are empty.
        patients_rows = ReportController.patients_count() or []
        appointments_rows = ReportController.appointments_count() or []
        revenue_rows = ReportController.revenue() or []

        total_patients = int(ReportController._extract_first_numeric(patients_rows, "total_patients", 0))
        total_appointments = int(ReportController._extract_first_numeric(appointments_rows, "total_appointments", 0))
        total_revenue = ReportController._extract_first_numeric(revenue_rows, "total_revenue", 0)

        return {
            "total_patients": max(total_patients, 0),
            "total_appointments": max(total_appointments, 0),
            "total_revenue": max(total_revenue, 0.0),
        }
