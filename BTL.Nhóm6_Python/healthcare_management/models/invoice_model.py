from database.db import fetch_all, execute

class InvoiceModel:

    @staticmethod
    def get_by_payment(payment_id):
        return fetch_all("""
            SELECT i.*, s.service_name
            FROM Invoices i
            JOIN Services s ON i.service_id = s.service_id
            WHERE i.payment_id=?
        """, (payment_id,))

    @staticmethod
    def add_item(payment_id, service_id, quantity, unit_price):
        return execute("""
            INSERT INTO Invoices (payment_id, service_id, quantity, unit_price)
            VALUES (?, ?, ?, ?)
        """, (payment_id, service_id, quantity, unit_price))