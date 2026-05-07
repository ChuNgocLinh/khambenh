from models.doctor_model import DoctorModel


class DoctorController:

    # 🔹 LẤY DANH SÁCH BÁC SĨ
    @staticmethod
    def get_all():
        return DoctorModel.get_all()


    # 🔹 TẠO BÁC SĨ (DÙNG FORM WEB)
    @staticmethod
    def create(form):
        return DoctorModel.create(
            form.get("name"),
            form.get("specialty"),
            form.get("phone")
        )


    # 🔹 CẬP NHẬT
    @staticmethod
    def update(doctor_id, form):
        return DoctorModel.update(
            doctor_id,
            form.get("name"),
            form.get("specialty"),
            form.get("phone")
        )


    # 🔹 XÓA
    @staticmethod
    def delete(doctor_id):
        return DoctorModel.delete(doctor_id)