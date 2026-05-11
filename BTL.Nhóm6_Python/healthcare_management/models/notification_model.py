from database.db import execute, fetch_all, fetch_one


class NotificationModel:
    TARGET_PAGES = {"schedule", "patient_profile", "prescriptions", "dashboard", "settings"}

    @staticmethod
    def list_for_user(user_id):
        return fetch_all(
            """
            SELECT *
            FROM Notifications
            WHERE user_id=?
            ORDER BY created_at DESC, notification_id DESC
            """,
            (user_id,),
        )

    @staticmethod
    def unread_count(user_id):
        row = fetch_one(
            "SELECT COUNT(*) AS c FROM Notifications WHERE user_id=? AND is_read=FALSE",
            (user_id,),
        )
        return int(row.get("c", 0) if row else 0)

    @staticmethod
    def create(user_id, title, content="", type_="system", target_page="dashboard", target_id=None):
        if target_page not in NotificationModel.TARGET_PAGES:
            target_page = "dashboard"
        return execute(
            """
            INSERT INTO Notifications (user_id, title, content, type, target_page, target_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, title, content, type_, target_page, target_id),
        )

    @staticmethod
    def mark_read(notification_id, user_id):
        return execute(
            """
            UPDATE Notifications
            SET is_read=TRUE, read_at=COALESCE(read_at, CURRENT_TIMESTAMP)
            WHERE notification_id=? AND user_id=?
            """,
            (notification_id, user_id),
        )

    @staticmethod
    def mark_all_read(user_id):
        return execute(
            """
            UPDATE Notifications
            SET is_read=TRUE, read_at=COALESCE(read_at, CURRENT_TIMESTAMP)
            WHERE user_id=? AND is_read=FALSE
            """,
            (user_id,),
        )
