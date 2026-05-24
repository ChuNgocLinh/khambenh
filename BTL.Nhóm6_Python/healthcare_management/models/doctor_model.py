from database.db import fetch_all, fetch_one, execute

class DoctorModel:

    @staticmethod
    def get_all():
        return fetch_all("SELECT * FROM Doctors")

    @staticmethod
    def get_available_for_patient():
        return fetch_all(
            """
            SELECT *
            FROM Doctors
            WHERE COALESCE(is_active, 1) = 1
              AND (
                  work_status IS NULL
                  OR work_status NOT IN (N'Đã nghỉ việc', N'Nghỉ phép', N'Tạm nghỉ')
              )
            ORDER BY specialty ASC, name ASC, doctor_id ASC
            """
        )

    @staticmethod
    def get_by_id(doctor_id):
        return fetch_one("SELECT * FROM Doctors WHERE doctor_id=?", (doctor_id,))

    @staticmethod
    def create(name, specialty, phone):
        return execute("""
            INSERT INTO Doctors (name, specialty, phone)
            VALUES (?, ?, ?)
        """, (name, specialty, phone))

    @staticmethod
    def update(doctor_id, name, specialty, phone):
        return execute("""
            UPDATE Doctors
            SET name=?, specialty=?, phone=?
            WHERE doctor_id=?
        """, (name, specialty, phone, doctor_id))

    @staticmethod
    def update_profile_details(doctor_id, name, specialty, phone, email):
        return execute(
            """
            UPDATE Doctors
            SET name=?, specialty=?, phone=?, email=?
            WHERE doctor_id=?
            """,
            (name, specialty, phone, email, doctor_id),
        )

    @staticmethod
    def delete(doctor_id):
        return execute("DELETE FROM Doctors WHERE doctor_id=?", (doctor_id,))
