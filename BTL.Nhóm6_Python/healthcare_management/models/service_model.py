from database.db import fetch_all, fetch_one, execute

class ServiceModel:

    @staticmethod
    def get_all():
        return fetch_all("SELECT * FROM Services")

    @staticmethod
    def create(name, price, description):
        return execute(
            "INSERT INTO Services (service_name, price, description) VALUES (?, ?, ?)",
            (name, price, description)
        )

    @staticmethod
    def update(service_id, name, price, description):
        return execute(
            "UPDATE Services SET service_name=?, price=?, description=? WHERE service_id=?",
            (name, price, description, service_id)
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
