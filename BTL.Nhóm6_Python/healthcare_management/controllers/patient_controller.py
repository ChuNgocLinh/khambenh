from models.patient_model import PatientModel


class PatientController:

    # 🔹 LẤY DANH SÁCH BỆNH NHÂN
    @staticmethod
    def get_all():
        return PatientModel.get_all()


    # 🔹 TẠO BỆNH NHÂN (DÙNG CHO FORM WEB)
    @staticmethod
    def create(form):
        return PatientModel.create(
            form.get("name"),
            form.get("dob"),
            form.get("gender"),
            form.get("phone"),
            form.get("address")
        )


    # 🔹 CẬP NHẬT
    @staticmethod
    def update(patient_id, form):
        return PatientModel.update(
            patient_id,
            form.get("name"),
            form.get("dob"),
            form.get("gender"),
            form.get("phone"),
            form.get("address")
        )


    # 🔹 XÓA
    @staticmethod
    def delete(patient_id):
        return PatientModel.delete(patient_id)