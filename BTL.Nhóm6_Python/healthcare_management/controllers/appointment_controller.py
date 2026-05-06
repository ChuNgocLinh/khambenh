from healthcare_management.models.appointment_model import AppointmentModel


class AppointmentController:

    # 🔹 LẤY TẤT CẢ LỊCH HẸN
    @staticmethod
    def get_all():
        return AppointmentModel.get_all()


    # 🔹 TẠO LỊCH HẸN (TỪ FORM WEB)
    @staticmethod
    def create(form):
        return AppointmentModel.create(
            form.get("patient_id"),
            form.get("doctor_id"),
            form.get("date"),
            form.get("time"),
            form.get("status", "pending")  # mặc định
        )


    # 🔹 CẬP NHẬT TRẠNG THÁI
    @staticmethod
    def update_status(appointment_id, status):
        return AppointmentModel.update_status(appointment_id, status)