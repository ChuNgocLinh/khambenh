from datetime import datetime

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
    }

    @staticmethod
    def ensure_table_exists():
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
                backup_mode, last_backup_at, last_sync_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
