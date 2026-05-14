from models.service_model import ServiceModel

class ServiceController:

    @staticmethod
    def get_all():
        return ServiceModel.get_all()
    
    @staticmethod
    def get_by_id(service_id):
        return ServiceModel.get_by_id(service_id)

    @staticmethod
    def create(data):
        return ServiceModel.create(
            data.get("code", ""),
            data.get("name", ""),
            data.get("category", ""),
            data.get("duration", 30),
            data.get("price", 0),
            data.get("description", ""),
            data.get("is_visible", True),
            data.get("is_active", True)
        )

    @staticmethod
    def update(service_id, data):
        return ServiceModel.update(
            service_id,
            data.get("code", ""),
            data.get("name", ""),
            data.get("category", ""),
            data.get("duration", 30),
            data.get("price", 0),
            data.get("description", ""),
            data.get("is_visible", True),
            data.get("is_active", True)
        )

    @staticmethod
    def delete(service_id):
        # Prevent hard deleting if used
        if ServiceModel.check_used(service_id):
            return ServiceModel.set_active(service_id, False) # mark as discontinued instead
        return ServiceModel.delete(service_id)

    @staticmethod
    def set_active(service_id, is_active):
        return ServiceModel.set_active(service_id, is_active)

