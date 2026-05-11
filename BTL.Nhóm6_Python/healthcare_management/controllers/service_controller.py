from models.service_model import ServiceModel

class ServiceController:

    @staticmethod
    def get_all():
        return ServiceModel.get_all()

    @staticmethod
    def create(data):
        return ServiceModel.create(
            data["name"],
            data["price"],
            data["description"]
        )

    @staticmethod
    def update(service_id, data):
        return ServiceModel.update(
            service_id,
            data["name"],
            data["price"],
            data["description"]
        )

    @staticmethod
    def delete(service_id):
        return ServiceModel.delete(service_id)

    @staticmethod
    def set_active(service_id, is_active):
        return ServiceModel.set_active(service_id, is_active)
