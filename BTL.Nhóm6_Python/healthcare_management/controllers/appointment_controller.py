from models.appointment_model import AppointmentModel
from datetime import datetime


class AppointmentController:
    VALID_STATUSES = {"pending", "confirmed", "in_progress", "done", "cancelled"}

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
        if status not in AppointmentController.VALID_STATUSES:
            return False

        existing = AppointmentModel.get_by_id(appointment_id)
        if not existing:
            return False

        current_status = str(existing.get("status", ""))
        if current_status in {"done", "cancelled"} and status != current_status:
            return False

        return AppointmentModel.update_status(appointment_id, status)

    @staticmethod
    def get_management_rows_by_doctor(doctor_id):
        return AppointmentModel.get_management_rows_by_doctor(doctor_id)

    @staticmethod
    def get_by_id(appointment_id):
        return AppointmentModel.get_by_id(appointment_id)

    @staticmethod
    def update_full(appointment_id, patient_id, doctor_id, date_str, time_str, status, service_name, note):
        required_fields = [appointment_id, patient_id, doctor_id, date_str, time_str]
        if not all(required_fields):
            return {
                "status": False,
                "message": "Thiếu dữ liệu để cập nhật lịch hẹn.",
            }

        if status not in AppointmentController.VALID_STATUSES:
            return {
                "status": False,
                "message": "Trạng thái lịch hẹn không hợp lệ.",
            }

        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            selected_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            return {
                "status": False,
                "message": "Ngày hoặc giờ không hợp lệ.",
            }

        appointment_datetime = datetime.combine(selected_date, selected_time)
        appointment_dt_str = appointment_datetime.strftime("%Y-%m-%d %H:%M:%S")

        existing = AppointmentModel.get_by_id(appointment_id)
        if not existing:
            return {
                "status": False,
                "message": "Không tìm thấy lịch hẹn cần cập nhật.",
            }

        existing_status = str(existing.get("status", ""))
        if existing_status in {"done", "cancelled"} and status != existing_status:
            return {
                "status": False,
                "message": "Không thể thay đổi trạng thái của lịch hẹn đã kết thúc hoặc đã hủy.",
            }

        doctor_conflict, patient_conflict = AppointmentModel.has_conflict(
            doctor_id,
            patient_id,
            appointment_dt_str,
            appointment_id,
        )

        if doctor_conflict:
            return {
                "status": False,
                "message": "Bác sĩ đã có lịch ở khung giờ này.",
            }

        if patient_conflict:
            return {
                "status": False,
                "message": "Bệnh nhân đã có lịch ở khung giờ này.",
            }

        if appointment_datetime < datetime.now() and status in {"pending", "confirmed", "in_progress"}:
            return {
                "status": False,
                "message": "Không thể đặt trạng thái hoạt động cho lịch hẹn trong quá khứ.",
            }

        normalized_service = (service_name or "").strip()
        normalized_note = (note or "").strip()

        if normalized_service:
            combined_note = f"Dịch vụ: {normalized_service}"
            if normalized_note:
                combined_note += f" | {normalized_note}"
        else:
            combined_note = normalized_note

        is_updated = AppointmentModel.update_full(
            appointment_id,
            patient_id,
            doctor_id,
            appointment_dt_str,
            status,
            combined_note,
        )

        if not is_updated:
            return {
                "status": False,
                "message": "Không thể cập nhật lịch hẹn.",
            }

        return {
            "status": True,
            "message": "Cập nhật lịch hẹn thành công.",
        }

    @staticmethod
    def create_with_details(patient_id, doctor_id, date_str, time_str, status, service_name, note):
        required_fields = [patient_id, doctor_id, date_str, time_str]
        if not all(required_fields):
            return {
                "status": False,
                "message": "Thiếu dữ liệu để tạo lịch hẹn.",
            }

        if status not in AppointmentController.VALID_STATUSES:
            return {
                "status": False,
                "message": "Trạng thái lịch hẹn không hợp lệ.",
            }

        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            selected_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            return {
                "status": False,
                "message": "Ngày hoặc giờ không hợp lệ.",
            }

        appointment_datetime = datetime.combine(selected_date, selected_time)
        appointment_dt_str = appointment_datetime.strftime("%Y-%m-%d %H:%M:%S")

        if appointment_datetime < datetime.now() and status in {"pending", "confirmed", "in_progress"}:
            return {
                "status": False,
                "message": "Không thể tạo lịch hẹn hoạt động trong quá khứ.",
            }

        doctor_conflict, patient_conflict = AppointmentModel.has_conflict(
            doctor_id,
            patient_id,
            appointment_dt_str,
        )
        if doctor_conflict:
            return {
                "status": False,
                "message": "Bác sĩ đã có lịch ở khung giờ này.",
            }
        if patient_conflict:
            return {
                "status": False,
                "message": "Bệnh nhân đã có lịch ở khung giờ này.",
            }

        normalized_service = (service_name or "").strip() or "Khám tổng quát"
        normalized_note = (note or "").strip()
        combined_note = f"Dịch vụ: {normalized_service}"
        if normalized_note:
            combined_note += f" | {normalized_note}"

        is_created = AppointmentModel.create(
            patient_id,
            doctor_id,
            appointment_dt_str,
            status,
            combined_note,
        )
        if not is_created:
            return {
                "status": False,
                "message": "Không thể tạo lịch hẹn.",
            }

        return {
            "status": True,
            "message": "Đã thêm lịch hẹn mới.",
        }
