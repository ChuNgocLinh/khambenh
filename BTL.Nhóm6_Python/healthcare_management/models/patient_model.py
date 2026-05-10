from database.db import fetch_all, fetch_one, execute

class PatientModel:

    @staticmethod
    def get_all():
        return fetch_all("SELECT * FROM Patients")

    @staticmethod
    def get_by_id(patient_id):
        return fetch_one("SELECT * FROM Patients WHERE patient_id=?", (patient_id,))

    @staticmethod
    def get_by_phone(phone):
        return fetch_one(
            "SELECT * FROM Patients WHERE phone=? ORDER BY patient_id DESC",
            (phone,),
        )

    @staticmethod
    def get_by_cccd(cccd):
        return fetch_one(
            "SELECT * FROM Patients WHERE cccd=? ORDER BY patient_id DESC",
            (cccd,),
        )

    @staticmethod
    def create(
        name,
        dob,
        gender,
        phone,
        cccd,
        address,
        email,
        occupation,
        intake_notes,
        patient_type,
    ):
        query = """
        INSERT INTO Patients (
            name, dob, gender, phone, cccd, address, email, occupation, intake_notes, patient_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return execute(
            query,
            (name, dob, gender, phone, cccd, address, email, occupation, intake_notes, patient_type),
        )

    @staticmethod
    def update(
        patient_id,
        name,
        dob,
        gender,
        phone,
        cccd,
        address,
        email,
        occupation,
        intake_notes,
        patient_type,
    ):
        query = """
        UPDATE Patients 
        SET name=?, dob=?, gender=?, phone=?, cccd=?, address=?, email=?, occupation=?, intake_notes=?, patient_type=?
        WHERE patient_id=?
        """
        return execute(
            query,
            (
                name,
                dob,
                gender,
                phone,
                cccd,
                address,
                email,
                occupation,
                intake_notes,
                patient_type,
                patient_id,
            ),
        )

    @staticmethod
    def delete(patient_id):
        return execute("DELETE FROM Patients WHERE patient_id=?", (patient_id,))
