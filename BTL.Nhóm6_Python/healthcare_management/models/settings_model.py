from datetime import datetime
import json

from config import DB_TYPE
from database.db import execute, fetch_one


class SettingsModel:
    DEFAULTS = {
        "gender": "Nam",
        "dob": None,
        "address": "",
        "avatar_path": "",
        "notify_new_appointment": True,
        "notify_reminder": True,
        "notify_system": True,
        "theme_mode": "Sáng",
        "font_size": "Trung bình",
        "display_density": "Thoải mái",
        "language": "Tiếng Việt",
        "backup_mode": "cloud",
        "last_backup_at": None,
        "last_sync_at": None,
        "work_schedule": "[]",
    }

    ALLOWED_UPDATE_FIELDS = {
        "gender",
        "dob",
        "address",
        "avatar_path",
        "notify_new_appointment",
        "notify_reminder",
        "notify_system",
        "theme_mode",
        "font_size",
        "display_density",
        "language",
        "backup_mode",
        "last_backup_at",
        "last_sync_at",
        "work_schedule",
    }

    @staticmethod
    def ensure_table_exists():
        if DB_TYPE != "mysql":
            return execute(
                """
                IF OBJECT_ID('dbo.UserSettings', 'U') IS NULL
                BEGIN
                    CREATE TABLE dbo.UserSettings (
                        user_id INT PRIMARY KEY,
                        gender NVARCHAR(10) NULL DEFAULT N'Nam',
                        dob DATE NULL,
                        address NVARCHAR(255) NULL DEFAULT N'',
                        avatar_path NVARCHAR(255) NULL DEFAULT N'',
                        notify_new_appointment BIT NOT NULL DEFAULT 1,
                        notify_reminder BIT NOT NULL DEFAULT 1,
                        notify_system BIT NOT NULL DEFAULT 1,
                        theme_mode NVARCHAR(20) NULL DEFAULT N'Sáng',
                        font_size NVARCHAR(20) NULL DEFAULT N'Trung bình',
                        display_density NVARCHAR(20) NULL DEFAULT N'Thoải mái',
                        language NVARCHAR(20) NULL DEFAULT N'Tiếng Việt',
                        backup_mode NVARCHAR(20) NULL DEFAULT N'cloud',
                        last_backup_at DATETIME2 NULL,
                        last_sync_at DATETIME2 NULL,
                        work_schedule NVARCHAR(MAX) NULL DEFAULT N'[]',
                        updated_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
                        CONSTRAINT FK_UserSettings_Users FOREIGN KEY (user_id) REFERENCES dbo.Users(user_id)
                    )
                END
                """
            )

        return execute(
            """
            CREATE TABLE IF NOT EXISTS UserSettings (
                user_id INT PRIMARY KEY,
                gender VARCHAR(10) DEFAULT 'Nam',
                dob DATE NULL,
                address VARCHAR(255) DEFAULT '',
                avatar_path VARCHAR(255) DEFAULT '',
                notify_new_appointment BOOLEAN DEFAULT TRUE,
                notify_reminder BOOLEAN DEFAULT TRUE,
                notify_system BOOLEAN DEFAULT TRUE,
                theme_mode VARCHAR(20) DEFAULT 'Sáng',
                font_size VARCHAR(20) DEFAULT 'Trung bình',
                display_density VARCHAR(20) DEFAULT 'Thoải mái',
                language VARCHAR(20) DEFAULT 'Tiếng Việt',
                backup_mode VARCHAR(20) DEFAULT 'cloud',
                last_backup_at DATETIME NULL,
                last_sync_at DATETIME NULL,
                work_schedule TEXT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            )
            """
        )

    @staticmethod
    def _create_default_row(user_id):
        defaults = SettingsModel.DEFAULTS
        return execute(
            """
            INSERT INTO UserSettings (
                user_id, gender, dob, address, avatar_path,
                notify_new_appointment, notify_reminder, notify_system,
                theme_mode, font_size, display_density, language,
                backup_mode, last_backup_at, last_sync_at, work_schedule
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                defaults["gender"],
                defaults["dob"],
                defaults["address"],
                defaults["avatar_path"],
                defaults["notify_new_appointment"],
                defaults["notify_reminder"],
                defaults["notify_system"],
                defaults["theme_mode"],
                defaults["font_size"],
                defaults["display_density"],
                defaults["language"],
                defaults["backup_mode"],
                defaults["last_backup_at"],
                defaults["last_sync_at"],
                defaults["work_schedule"],
            ),
        )

    @staticmethod
    def get_or_create_by_user_id(user_id):
        SettingsModel.ensure_table_exists()

        row = fetch_one("SELECT * FROM UserSettings WHERE user_id=?", (user_id,))
        if row:
            return row

        created = SettingsModel._create_default_row(user_id)
        if not created:
            return None

        return fetch_one("SELECT * FROM UserSettings WHERE user_id=?", (user_id,))

    @staticmethod
    def update_fields(user_id, fields):
        if not fields:
            return True

        safe_fields = {
            key: value
            for key, value in fields.items()
            if key in SettingsModel.ALLOWED_UPDATE_FIELDS
        }
        if not safe_fields:
            return False

        safe_fields["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        set_clause = ", ".join(f"{key}=?" for key in safe_fields.keys())
        params = list(safe_fields.values()) + [user_id]

        return execute(
            f"UPDATE UserSettings SET {set_clause} WHERE user_id=?",
            tuple(params),
        )

    @staticmethod
    def normalize_work_schedule(value):
        if isinstance(value, str):
            text = value.strip() or "[]"
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                return []
            return parsed if isinstance(parsed, list) else []
        if isinstance(value, list):
            return value
        return []
