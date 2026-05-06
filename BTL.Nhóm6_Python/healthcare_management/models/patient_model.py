from database.db import fetch_all, fetch_one, execute

class PatientModel:

    @staticmethod
    def get_all():
        return fetch_all("SELECT * FROM Patients")

    @staticmethod
    def get_by_id(patient_id):
        return fetch_one("SELECT * FROM Patients WHERE patient_id=?", (patient_id,))

    @staticmethod
    def create(name, dob, gender, phone, address):
        query = """
        INSERT INTO Patients (name, dob, gender, phone, address)
        VALUES (?, ?, ?, ?, ?)
        """
        return execute(query, (name, dob, gender, phone, address))

    @staticmethod
    def update(patient_id, name, dob, gender, phone, address):
        query = """
        UPDATE Patients 
        SET name=?, dob=?, gender=?, phone=?, address=?
        WHERE patient_id=?
        """
        return execute(query, (name, dob, gender, phone, address, patient_id))

    @staticmethod
    def delete(patient_id):
        return execute("DELETE FROM Patients WHERE patient_id=?", (patient_id,))