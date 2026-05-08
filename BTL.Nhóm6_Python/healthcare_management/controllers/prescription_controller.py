from models.prescription_model import PrescriptionModel
from models.medicine_model import MedicineModel

class PrescriptionController:

    @staticmethod
    def get_by_record(record_id):
        return PrescriptionModel.get_by_record(record_id)

    @staticmethod
    def add(record_id, medicine_id, quantity):
        medicine = MedicineModel.get_by_id(medicine_id)
        if not medicine:
            return False

        available_qty = int(medicine.get("quantity", 0) or 0)
        requested_qty = int(quantity or 0)
        if requested_qty <= 0 or requested_qty > available_qty:
            return False

        return PrescriptionModel.add(
            record_id,
            medicine_id,
            quantity
        )
