from models.medical_record_model import MedicalRecordModel

class MedicalRecordController:

    @staticmethod
    def get_by_patient(patient_id):
        return MedicalRecordModel.get_by_patient(patient_id)

    @staticmethod
    def create(patient_id, doctor_id, appointment_id, diagnosis, treatment):
        return MedicalRecordModel.create(
            patient_id,
            doctor_id,
            appointment_id,
            diagnosis,
            treatment
        )