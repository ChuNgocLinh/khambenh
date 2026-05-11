from models.notification_model import NotificationModel


class NotificationController:
    PAGE_TO_INDEX = {
        "dashboard": 0,
        "schedule": 1,
        "patient_profile": 4,
        "prescriptions": 5,
        "settings": 7,
    }

    @staticmethod
    def list_for_user(user_id):
        if not user_id:
            return []
        return NotificationModel.list_for_user(user_id)

    @staticmethod
    def unread_count(user_id):
        if not user_id:
            return 0
        return NotificationModel.unread_count(user_id)

    @staticmethod
    def create(user_id, title, content="", type_="system", target_page="dashboard", target_id=None):
        if not user_id or not title:
            return False
        return NotificationModel.create(user_id, title, content, type_, target_page, target_id)

    @staticmethod
    def mark_read(notification_id, user_id):
        if not notification_id or not user_id:
            return False
        return NotificationModel.mark_read(notification_id, user_id)

    @staticmethod
    def mark_all_read(user_id):
        if not user_id:
            return False
        return NotificationModel.mark_all_read(user_id)

    @staticmethod
    def delete(notification_id, user_id):
        if not notification_id or not user_id:
            return False
        return NotificationModel.delete(notification_id, user_id)

    @staticmethod
    def target_index(target_page):
        return NotificationController.PAGE_TO_INDEX.get(str(target_page or "dashboard"), 0)
