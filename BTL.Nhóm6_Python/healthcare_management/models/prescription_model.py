from database.db import fetch_all, execute

class PrescriptionModel:

    @staticmethod
    def get_by_record(record_id):
        return fetch_all("""
            SELECT p.*, m.name 
            FROM Prescriptions p
            JOIN Medicines m ON p.medicine_id = m.medicine_id
            WHERE p.record_id=?
        """, (record_id,))

    @staticmethod
    def add(record_id, medicine_id, quantity):
        return execute("""
            INSERT INTO Prescriptions (record_id, medicine_id, quantity)
            VALUES (?, ?, ?)
        """, (record_id, medicine_id, quantity))