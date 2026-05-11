from models.medical_record_model import MedicalRecordModel


class MedicalRecordController:
    @staticmethod
    def get_by_patient(patient_id):
        return MedicalRecordModel.get_by_patient(patient_id)

    @staticmethod
    def get_by_appointment(appointment_id):
        return MedicalRecordModel.get_by_appointment(appointment_id)

    @staticmethod
    def create(patient_id, doctor_id, appointment_id, diagnosis, treatment):
        return MedicalRecordModel.create(
            patient_id,
            doctor_id,
            appointment_id,
            diagnosis,
            treatment,
        )

    @staticmethod
    def save_draft(patient_id, doctor_id, appointment_id, diagnosis="", treatment="", symptoms="", conclusion="", notes=""):
        if not patient_id or not doctor_id or not appointment_id:
            return {"status": False, "message": "Thieu benh nhan, bac si hoac lich hen."}

        saved = MedicalRecordModel.save_draft(
            patient_id,
            doctor_id,
            appointment_id,
            diagnosis,
            treatment,
            symptoms,
            conclusion,
            notes,
        )
        return {
            "status": bool(saved),
            "message": "Da luu tam ca kham." if saved else "Khong the luu tam ca kham.",
            "record": MedicalRecordModel.get_by_appointment(appointment_id),
        }

    @staticmethod
    def finalize(record_id, diagnosis, treatment, appointment_id=None):
        diagnosis = str(diagnosis or "").strip()
        treatment = str(treatment or "").strip()
        if not diagnosis:
            return {"status": False, "message": "Vui long nhap chan doan truoc khi hoan tat."}
        if not treatment:
            return {"status": False, "message": "Vui long nhap huong dieu tri truoc khi hoan tat."}

        saved = MedicalRecordModel.finalize(record_id, diagnosis, treatment)
        if saved and appointment_id:
            from controllers.appointment_controller import AppointmentController

            AppointmentController.update_status(appointment_id, "done")
        return {
            "status": bool(saved),
            "message": "Da hoan tat ca kham." if saved else "Khong the hoan tat ca kham.",
        }
