from models.medicine_model import MedicineModel

class MedicineController:

    @staticmethod
    def get_all():
        return MedicineModel.get_all()

    @staticmethod
    def create(data):
        return MedicineModel.create(
            data["name"],
            data["quantity"],
            data["price"],
            data["description"]
        )

    @staticmethod
    def update(medicine_id, data):
        return MedicineModel.update(
            medicine_id,
            data["name"],
            data["quantity"],
            data["price"],
            data["description"]
        )

    @staticmethod
    def delete(medicine_id):
        return MedicineModel.delete(medicine_id)