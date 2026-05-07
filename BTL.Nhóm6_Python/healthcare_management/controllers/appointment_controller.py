from models.appointment_model import AppointmentModel
from datetime import datetime


class AppointmentController:

    # 🔹 LẤY TẤT CẢ LỊCH HẸN
    @staticmethod
    def get_all():
        return AppointmentModel.get_all()
        
    @staticmethod
    def get_by_patient(patient_id):
        return AppointmentModel.get_by_patient(patient_id)
        
    @staticmethod
    def get_by_doctor(doctor_id):
        return AppointmentModel.get_by_doctor(doctor_id)

    @staticmethod
    def get_upcoming_by_patient(patient_id):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return AppointmentModel.get_upcoming_by_patient(patient_id, current_datetime)


    # 🔹 TẠO LỊCH HẸN (TỪ FORM WEB/APP)
    @staticmethod
    def create(patient_id, doctor_id, date):
        return AppointmentModel.create(patient_id, doctor_id, date, "pending", "")

    @staticmethod
    def book_with_validation(patient_id, doctor_id, service_name, date_str, time_str):
        required_fields = [patient_id, doctor_id, service_name, date_str, time_str]
        if not all(required_fields):
            return {
                "status": False,
                "message": "Vui lòng chọn đầy đủ dịch vụ, ngày, giờ và bác sĩ.",
            }

        if service_name.strip().lower() == "chưa có dịch vụ":
            return {
                "status": False,
                "message": "Hiện chưa có dịch vụ khả dụng để đặt lịch.",
            }

        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return {
                "status": False,
                "message": "Ngày khám không đúng định dạng.",
            }

        try:
            selected_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            return {
                "status": False,
                "message": "Giờ khám không hợp lệ.",
            }

        if selected_date < datetime.now().date():
            return {
                "status": False,
                "message": "Không thể đặt lịch cho ngày trong quá khứ.",
            }

        appointment_datetime = datetime.combine(selected_date, selected_time)
        appointment_dt_str = appointment_datetime.strftime("%Y-%m-%d %H:%M:%S")

        if appointment_datetime < datetime.now():
            return {
                "status": False,
                "message": "Không thể đặt lịch cho khung giờ đã qua.",
            }

        # Use exact datetime matching to prevent double-booking at the same slot.
        doctor_conflict, patient_conflict = AppointmentModel.has_conflict(
            doctor_id,
            patient_id,
            appointment_dt_str,
        )

        if doctor_conflict:
            return {
                "status": False,
                "message": "Bác sĩ đã có lịch ở khung giờ này. Vui lòng chọn thời gian khác.",
            }

        if patient_conflict:
            return {
                "status": False,
                "message": "Bạn đã có lịch ở khung giờ này. Vui lòng chọn thời gian khác.",
            }

        note = f"Dịch vụ: {service_name}"
        is_created = AppointmentModel.create(
            patient_id,
            doctor_id,
            appointment_dt_str,
            "pending",
            note,
        )

        if not is_created:
            return {
                "status": False,
                "message": "Không thể lưu lịch hẹn. Vui lòng thử lại.",
            }

        return {
            "status": True,
            "message": "Đặt lịch khám thành công.",
        }


    # 🔹 CẬP NHẬT TRẠNG THÁI
    @staticmethod
    def update_status(appointment_id, status):
        return AppointmentModel.update_status(appointment_id, status)
