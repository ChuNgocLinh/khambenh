from models.service_model import ServiceModel

class ServiceController:

    @staticmethod
    def get_all():
        return ServiceModel.get_all()

    @staticmethod
    def get_visible_active():
        return ServiceModel.get_visible_active()
    
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
        existing = ServiceModel.get_by_id(service_id) or {}
        return ServiceModel.update(
            service_id,
            data.get("code", existing.get("service_code", "")),
            data.get("name", existing.get("service_name", "")),
            data.get("category", existing.get("category", "")),
            data.get("duration", existing.get("duration", 30)),
            data.get("price", existing.get("price", 0)),
            data.get("description", existing.get("description", "")),
            data.get("is_visible", existing.get("is_visible", True)),
            data.get("is_active", existing.get("is_active", True))
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
