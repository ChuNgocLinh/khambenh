from models.appointment_model import AppointmentModel


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


    # 🔹 TẠO LỊCH HẸN (TỪ FORM WEB/APP)
    @staticmethod
    def create(patient_id, doctor_id, date):
        return AppointmentModel.create(patient_id, doctor_id, date, "pending")


    # 🔹 CẬP NHẬT TRẠNG THÁI
    @staticmethod
    def update_status(appointment_id, status):
        return AppointmentModel.update_status(appointment_id, status)