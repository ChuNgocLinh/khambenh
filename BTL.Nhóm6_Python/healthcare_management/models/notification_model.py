from config import DB_TYPE
from database.db import execute, fetch_all, fetch_one


class NotificationModel:
    TARGET_PAGES = {"schedule", "patient_profile", "prescriptions", "dashboard", "settings"}

    @staticmethod
    def ensure_table_exists():
        if DB_TYPE == "mysql":
            ok = execute(
                """
                CREATE TABLE IF NOT EXISTS Notifications (
                    notification_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    title VARCHAR(150) NOT NULL,
                    content VARCHAR(500),
                    type VARCHAR(50) DEFAULT 'system',
                    target_page VARCHAR(50) DEFAULT 'dashboard',
                    target_id INT NULL,
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    read_at DATETIME NULL,
                    FOREIGN KEY (user_id) REFERENCES Users(user_id),
                    CHECK (target_page IN ('schedule','patient_profile','prescriptions','dashboard','settings'))
                )
                """
            )
            index_exists = fetch_one(
                """
                SELECT COUNT(*) AS c
                FROM INFORMATION_SCHEMA.STATISTICS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'Notifications'
                  AND INDEX_NAME = 'idx_notifications_user_read'
                """
            )
            if not index_exists or int(index_exists.get("c", 0)) == 0:
                execute("CREATE INDEX idx_notifications_user_read ON Notifications(user_id, is_read)")
            return ok

        ok = execute(
            """
            IF OBJECT_ID('dbo.Notifications', 'U') IS NULL
            BEGIN
                CREATE TABLE dbo.Notifications (
                    notification_id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id INT NOT NULL,
                    title NVARCHAR(150) NOT NULL,
                    content NVARCHAR(500) NULL,
                    type NVARCHAR(50) NOT NULL DEFAULT 'system',
                    target_page NVARCHAR(50) NOT NULL DEFAULT 'dashboard',
                    target_id INT NULL,
                    is_read BIT NOT NULL DEFAULT 0,
                    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
                    read_at DATETIME2 NULL,
                    CONSTRAINT FK_Notifications_Users FOREIGN KEY (user_id) REFERENCES dbo.Users(user_id),
                    CONSTRAINT CK_Notifications_TargetPage CHECK (target_page IN ('schedule','patient_profile','prescriptions','dashboard','settings'))
                )
            END
            """
        )
        execute(
            """
            IF NOT EXISTS (
                SELECT 1 FROM sys.indexes
                WHERE name = 'IX_Notifications_User_Read'
                  AND object_id = OBJECT_ID('dbo.Notifications')
            )
            BEGIN
                CREATE INDEX IX_Notifications_User_Read
                ON dbo.Notifications(user_id, is_read, created_at DESC)
            END
            """
        )
        return ok

    @staticmethod
    def list_for_user(user_id):
        NotificationModel.ensure_table_exists()
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
        NotificationModel.ensure_table_exists()
        row = fetch_one(
            "SELECT COUNT(*) AS c FROM Notifications WHERE user_id=? AND is_read=0",
            (user_id,),
        )
        return int(row.get("c", 0) if row else 0)

    @staticmethod
    def create(user_id, title, content="", type_="system", target_page="dashboard", target_id=None):
        NotificationModel.ensure_table_exists()
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
        NotificationModel.ensure_table_exists()
        return execute(
            """
            UPDATE Notifications
            SET is_read=1, read_at=COALESCE(read_at, CURRENT_TIMESTAMP)
            WHERE notification_id=? AND user_id=?
            """,
            (notification_id, user_id),
        )

    @staticmethod
    def mark_all_read(user_id):
        NotificationModel.ensure_table_exists()
        return execute(
            """
            UPDATE Notifications
            SET is_read=1, read_at=COALESCE(read_at, CURRENT_TIMESTAMP)
            WHERE user_id=? AND is_read=0
            """,
            (user_id,),
        )

    @staticmethod
    def delete(notification_id, user_id):
        NotificationModel.ensure_table_exists()
        return execute(
            "DELETE FROM Notifications WHERE notification_id=? AND user_id=?",
            (notification_id, user_id),
        )
