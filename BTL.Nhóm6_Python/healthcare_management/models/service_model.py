from database.db import fetch_all, fetch_one, execute
from database.sql_utils import select_top

class ServiceModel:

    @staticmethod
    def get_all():
        return fetch_all("SELECT * FROM Services ORDER BY service_id DESC")

    @staticmethod
    def get_visible_active():
        return fetch_all(
            """
            SELECT *
            FROM Services
            WHERE COALESCE(is_visible, 1) = 1
              AND COALESCE(is_active, 1) = 1
            ORDER BY category ASC, service_name ASC, service_id ASC
            """
        )

    @staticmethod
    def get_by_id(service_id):
        return fetch_one("SELECT * FROM Services WHERE service_id=?", (service_id,))

    @staticmethod
    def create(code, name, category, duration, price, description, is_visible, is_active):
        return execute(
            "INSERT INTO Services (service_code, service_name, category, duration, price, description, is_visible, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (code, name, category, duration, price, description, is_visible, is_active)
        )

    @staticmethod
    def update(service_id, code, name, category, duration, price, description, is_visible, is_active):
        return execute(
            "UPDATE Services SET service_code=?, service_name=?, category=?, duration=?, price=?, description=?, is_visible=?, is_active=? WHERE service_id=?",
            (code, name, category, duration, price, description, is_visible, is_active, service_id)
        )

    @staticmethod
    def delete(service_id):
        return execute("DELETE FROM Services WHERE service_id=?", (service_id,))

    @staticmethod
    def set_active(service_id, is_active):
        return execute(
            "UPDATE Services SET is_active=? WHERE service_id=?",
            (1 if bool(is_active) else 0, service_id)
        )
    
    @staticmethod
    def check_used(service_id):
        invoice = fetch_one(f"SELECT {select_top(1)}1 FROM Invoices WHERE service_id=?", (service_id,))
        if invoice:
            return True
        return False
