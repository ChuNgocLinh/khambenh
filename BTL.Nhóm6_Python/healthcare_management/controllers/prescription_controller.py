from models.prescription_model import PrescriptionModel

class PrescriptionController:

    @staticmethod
    def get_by_record(record_id):
        return PrescriptionModel.get_by_record(record_id)

    @staticmethod
    def add(record_id, medicine_id, quantity):
        return PrescriptionModel.add(
            record_id,
            medicine_id,
            quantity
        )