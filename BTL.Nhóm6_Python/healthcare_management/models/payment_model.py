from database.db import fetch_all, execute
from database.sql_utils import string_agg

class PaymentModel:

    @staticmethod
    def get_all():
        return fetch_all("""
            SELECT p.*, a.appointment_date
            FROM Payments p
            JOIN Appointments a ON p.appointment_id = a.appointment_id
        """)

    @staticmethod
    def get_enriched_all(status=None, date_from=None, date_to=None):
        try:
            from models.appointment_model import AppointmentModel

            AppointmentModel._ensure_schema()
        except Exception:
            pass

        service_names = string_agg("COALESCE(invoice_service.service_name, appointment_service.service_name)")
        query = f"""
            SELECT
                p.payment_id,
                p.patient_id,
                p.appointment_id,
                p.total_amount,
                p.method,
                p.status,
                p.payment_date,
                pat.name AS patient_name,
                pat.phone AS patient_phone,
                a.appointment_date,
                d.name AS doctor_name,
                COALESCE({service_names}, '') AS service_names,
                COUNT(i.invoice_id) AS invoice_item_count
            FROM Payments p
            LEFT JOIN Patients pat ON pat.patient_id = p.patient_id
            LEFT JOIN Appointments a ON a.appointment_id = p.appointment_id
            LEFT JOIN Doctors d ON d.doctor_id = a.doctor_id
            LEFT JOIN Services appointment_service ON appointment_service.service_id = a.service_id
            LEFT JOIN Invoices i ON i.payment_id = p.payment_id
            LEFT JOIN Services invoice_service ON invoice_service.service_id = i.service_id
            WHERE 1=1
        """
        params = []
        if status:
            query += " AND p.status = ?"
            params.append(status)
        if date_from:
            query += " AND p.payment_date >= ?"
            params.append(date_from)
        if date_to:
            query += " AND p.payment_date < ?"
            params.append(date_to)
        query += """
            GROUP BY
                p.payment_id,
                p.patient_id,
                p.appointment_id,
                p.total_amount,
                p.method,
                p.status,
                p.payment_date,
                pat.name,
                pat.phone,
                a.appointment_date,
                d.name
            ORDER BY p.payment_date DESC, p.payment_id DESC
        """
        return fetch_all(query, tuple(params))

    @staticmethod
    def create(patient_id, appointment_id, total_amount):
        query = """
        INSERT INTO Payments (patient_id, appointment_id, total_amount, status)
        VALUES (?, ?, ?, 'unpaid')
        """
        return execute(query, (patient_id, appointment_id, total_amount))

    @staticmethod
    def update_status(payment_id, status):
        return execute(
            "UPDATE Payments SET status=? WHERE payment_id=?",
            (status, payment_id)
        )
