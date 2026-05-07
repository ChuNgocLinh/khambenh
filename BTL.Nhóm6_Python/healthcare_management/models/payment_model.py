from database.db import fetch_all, execute

class PaymentModel:

    @staticmethod
    def get_all():
        return fetch_all("""
            SELECT p.*, a.appointment_date
            FROM Payments p
            JOIN Appointments a ON p.appointment_id = a.appointment_id
        """)

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