from models.medicine_model import MedicineModel
from models.prescription_model import PrescriptionModel


class PrescriptionController:
    @staticmethod
    def get_by_record(record_id):
        return PrescriptionModel.get_by_record(record_id)

    @staticmethod
    def get_by_doctor(doctor_id):
        return PrescriptionModel.get_by_doctor(doctor_id)

    @staticmethod
    def can_edit(status):
        return str(status or "draft") != "dispensed"

    @staticmethod
    def _medicine_quantity_valid(medicine_id, quantity):
        medicine = MedicineModel.get_by_id(medicine_id)
        if not medicine:
            return False

        available_qty = int(medicine.get("quantity", 0) or 0)
        requested_qty = int(quantity or 0)
        return requested_qty > 0 and requested_qty <= available_qty

    @staticmethod
    def add(record_id, medicine_id, quantity, status="draft"):
        if status not in PrescriptionModel.VALID_STATUSES:
            return False
        if not PrescriptionController._medicine_quantity_valid(medicine_id, quantity):
            return False

        return PrescriptionModel.add(record_id, medicine_id, quantity, status)

    @staticmethod
    def update_item(prescription_id, medicine_id, quantity, status="draft"):
        existing = PrescriptionModel.get_by_id(prescription_id)
        if not existing or not PrescriptionController.can_edit(existing.get("status")):
            return {"status": False, "message": "Khong the sua don thuoc da phat."}
        if status not in PrescriptionModel.VALID_STATUSES:
            return {"status": False, "message": "Trang thai don thuoc khong hop le."}
        if not PrescriptionController._medicine_quantity_valid(medicine_id, quantity):
            return {"status": False, "message": "Du lieu thuoc khong hop le."}

        updated = PrescriptionModel.update_item(prescription_id, medicine_id, quantity, status)
        return {"status": bool(updated), "message": "Da cap nhat don thuoc."}

    @staticmethod
    def cancel(prescription_id):
        existing = PrescriptionModel.get_by_id(prescription_id)
        if not existing or not PrescriptionController.can_edit(existing.get("status")):
            return {"status": False, "message": "Khong the huy don thuoc da phat."}

        updated = PrescriptionModel.update_status(prescription_id, "cancelled")
        return {"status": bool(updated), "message": "Da huy don thuoc."}
