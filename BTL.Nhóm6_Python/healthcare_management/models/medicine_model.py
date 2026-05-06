from database.db import fetch_all, fetch_one, execute

class MedicineModel:

    @staticmethod
    def get_all():
        return fetch_all("SELECT * FROM Medicines")

    @staticmethod
    def get_by_id(medicine_id):
        return fetch_one("SELECT * FROM Medicines WHERE medicine_id=?", (medicine_id,))

    @staticmethod
    def create(name, quantity, price, description):
        query = """
        INSERT INTO Medicines (name, quantity, price, description)
        VALUES (?, ?, ?, ?)
        """
        return execute(query, (name, quantity, price, description))

    @staticmethod
    def update(medicine_id, name, quantity, price, description):
        query = """
        UPDATE Medicines
        SET name=?, quantity=?, price=?, description=?
        WHERE medicine_id=?
        """
        return execute(query, (name, quantity, price, description, medicine_id))

    @staticmethod
    def delete(medicine_id):
        return execute("DELETE FROM Medicines WHERE medicine_id=?", (medicine_id,))