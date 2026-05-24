import json
from datetime import datetime

from config import DB_TYPE
from database.db import execute, fetch_all, fetch_one
from database.sql_utils import limit_clause, pagination_clause, pagination_params, select_top


class BackupModel:
    @staticmethod
    def ensure_tables_exist():
        if DB_TYPE == "mysql":
            execute(
                """
                CREATE TABLE IF NOT EXISTS BackupSettings (
                    setting_id INT PRIMARY KEY,
                    storage_location VARCHAR(100) DEFAULT 'Máy chủ nội bộ',
                    storage_path VARCHAR(255) DEFAULT '/backup/careplus/',
                    auto_backup BOOLEAN DEFAULT TRUE,
                    include_database BOOLEAN DEFAULT TRUE,
                    include_attachments BOOLEAN DEFAULT TRUE,
                    compress_data BOOLEAN DEFAULT TRUE,
                    email_notification BOOLEAN DEFAULT FALSE,
                    retention_days INT DEFAULT 30,
                    schedule_time VARCHAR(10) DEFAULT '02:00',
                    schedule_frequency VARCHAR(20) DEFAULT 'daily',
                    encryption_enabled BOOLEAN DEFAULT FALSE,
                    updated_by_user_id INT NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (updated_by_user_id) REFERENCES Users(user_id)
                )
                """
            )
            execute(
                """
                CREATE TABLE IF NOT EXISTS BackupRecords (
                    backup_id VARCHAR(40) PRIMARY KEY,
                    created_at DATETIME NOT NULL,
                    backup_type VARCHAR(20) DEFAULT 'manual',
                    size_bytes BIGINT DEFAULT 0,
                    created_by_user_id INT NULL,
                    created_by_name VARCHAR(120) DEFAULT 'Hệ thống',
                    status VARCHAR(20) DEFAULT 'success',
                    storage_mode VARCHAR(20) DEFAULT 'local',
                    storage_path VARCHAR(255),
                    checksum VARCHAR(128) NULL,
                    include_database BOOLEAN DEFAULT TRUE,
                    include_attachments BOOLEAN DEFAULT TRUE,
                    compress_data BOOLEAN DEFAULT TRUE,
                    error_message VARCHAR(255) NULL,
                    is_deleted BOOLEAN DEFAULT FALSE,
                    deleted_at DATETIME NULL,
                    FOREIGN KEY (created_by_user_id) REFERENCES Users(user_id),
                    CHECK (backup_type IN ('automatic', 'manual')),
                    CHECK (status IN ('success', 'processing', 'failed', 'expired')),
                    CHECK (storage_mode IN ('local', 'cloud'))
                )
                """
            )
            execute(
                """
                CREATE TABLE IF NOT EXISTS BackupJobs (
                    job_id VARCHAR(40) PRIMARY KEY,
                    job_type VARCHAR(20) NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    progress INT DEFAULT 0,
                    message VARCHAR(255),
                    requested_by_user_id INT NULL,
                    backup_id VARCHAR(40) NULL,
                    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    finished_at DATETIME NULL,
                    FOREIGN KEY (requested_by_user_id) REFERENCES Users(user_id),
                    FOREIGN KEY (backup_id) REFERENCES BackupRecords(backup_id),
                    CHECK (job_type IN ('backup','restore')),
                    CHECK (status IN ('pending','processing','success','failed'))
                )
                """
            )
            execute(
                """
                CREATE TABLE IF NOT EXISTS BackupRestoreRequests (
                    request_id INT AUTO_INCREMENT PRIMARY KEY,
                    backup_id VARCHAR(40) NOT NULL,
                    requested_by_user_id INT NULL,
                    confirm_text VARCHAR(30) NOT NULL,
                    create_backup_before_restore BOOLEAN DEFAULT TRUE,
                    status VARCHAR(20) DEFAULT 'processing',
                    restore_message VARCHAR(255),
                    requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    completed_at DATETIME NULL,
                    FOREIGN KEY (backup_id) REFERENCES BackupRecords(backup_id),
                    FOREIGN KEY (requested_by_user_id) REFERENCES Users(user_id),
                    CHECK (status IN ('processing','success','failed'))
                )
                """
            )
            created_at_index = fetch_one(
                """
                SELECT COUNT(*) AS c
                FROM INFORMATION_SCHEMA.STATISTICS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'BackupRecords'
                  AND INDEX_NAME = 'idx_backup_records_created_at'
                """
            )
            if not created_at_index or int(created_at_index.get("c", 0)) == 0:
                execute("CREATE INDEX idx_backup_records_created_at ON BackupRecords(created_at)")

            status_index = fetch_one(
                """
                SELECT COUNT(*) AS c
                FROM INFORMATION_SCHEMA.STATISTICS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'BackupRecords'
                  AND INDEX_NAME = 'idx_backup_records_status'
                """
            )
            if not status_index or int(status_index.get("c", 0)) == 0:
                execute("CREATE INDEX idx_backup_records_status ON BackupRecords(status)")
        else:
            execute(
                """
                IF OBJECT_ID('dbo.BackupSettings', 'U') IS NULL
                BEGIN
                    CREATE TABLE dbo.BackupSettings (
                        setting_id INT PRIMARY KEY,
                        storage_location NVARCHAR(100) DEFAULT N'Máy chủ nội bộ',
                        storage_path NVARCHAR(255) DEFAULT N'/backup/careplus/',
                        auto_backup BIT DEFAULT 1,
                        include_database BIT DEFAULT 1,
                        include_attachments BIT DEFAULT 1,
                        compress_data BIT DEFAULT 1,
                        email_notification BIT DEFAULT 0,
                        retention_days INT DEFAULT 30,
                        schedule_time NVARCHAR(10) DEFAULT N'02:00',
                        schedule_frequency NVARCHAR(20) DEFAULT N'daily',
                        encryption_enabled BIT DEFAULT 0,
                        updated_by_user_id INT NULL,
                        updated_at DATETIME2 DEFAULT SYSUTCDATETIME(),
                        CONSTRAINT FK_BackupSettings_Users FOREIGN KEY (updated_by_user_id) REFERENCES dbo.Users(user_id)
                    )
                END
                """
            )
            execute(
                """
                IF OBJECT_ID('dbo.BackupRecords', 'U') IS NULL
                BEGIN
                    CREATE TABLE dbo.BackupRecords (
                        backup_id NVARCHAR(40) PRIMARY KEY,
                        created_at DATETIME2 NOT NULL,
                        backup_type NVARCHAR(20) DEFAULT N'manual',
                        size_bytes BIGINT DEFAULT 0,
                        created_by_user_id INT NULL,
                        created_by_name NVARCHAR(120) DEFAULT N'Hệ thống',
                        status NVARCHAR(20) DEFAULT N'success',
                        storage_mode NVARCHAR(20) DEFAULT N'local',
                        storage_path NVARCHAR(255),
                        checksum NVARCHAR(128) NULL,
                        include_database BIT DEFAULT 1,
                        include_attachments BIT DEFAULT 1,
                        compress_data BIT DEFAULT 1,
                        error_message NVARCHAR(255) NULL,
                        is_deleted BIT DEFAULT 0,
                        deleted_at DATETIME2 NULL,
                        CONSTRAINT FK_BackupRecords_Users FOREIGN KEY (created_by_user_id) REFERENCES dbo.Users(user_id)
                    )
                END
                """
            )
            execute(
                """
                IF OBJECT_ID('dbo.BackupJobs', 'U') IS NULL
                BEGIN
                    CREATE TABLE dbo.BackupJobs (
                        job_id NVARCHAR(40) PRIMARY KEY,
                        job_type NVARCHAR(20) NOT NULL,
                        status NVARCHAR(20) NOT NULL,
                        progress INT DEFAULT 0,
                        message NVARCHAR(255),
                        requested_by_user_id INT NULL,
                        backup_id NVARCHAR(40) NULL,
                        started_at DATETIME2 DEFAULT SYSUTCDATETIME(),
                        finished_at DATETIME2 NULL,
                        CONSTRAINT FK_BackupJobs_Users FOREIGN KEY (requested_by_user_id) REFERENCES dbo.Users(user_id),
                        CONSTRAINT FK_BackupJobs_BackupRecords FOREIGN KEY (backup_id) REFERENCES dbo.BackupRecords(backup_id)
                    )
                END
                """
            )
            execute(
                """
                IF OBJECT_ID('dbo.BackupRestoreRequests', 'U') IS NULL
                BEGIN
                    CREATE TABLE dbo.BackupRestoreRequests (
                        request_id INT IDENTITY(1,1) PRIMARY KEY,
                        backup_id NVARCHAR(40) NOT NULL,
                        requested_by_user_id INT NULL,
                        confirm_text NVARCHAR(30) NOT NULL,
                        create_backup_before_restore BIT DEFAULT 1,
                        status NVARCHAR(20) DEFAULT N'processing',
                        restore_message NVARCHAR(255),
                        requested_at DATETIME2 DEFAULT SYSUTCDATETIME(),
                        completed_at DATETIME2 NULL,
                        CONSTRAINT FK_BackupRestoreRequests_BackupRecords FOREIGN KEY (backup_id) REFERENCES dbo.BackupRecords(backup_id),
                        CONSTRAINT FK_BackupRestoreRequests_Users FOREIGN KEY (requested_by_user_id) REFERENCES dbo.Users(user_id)
                    )
                END
                """
            )

        BackupModel._ensure_default_settings()

    @staticmethod
    def _ensure_default_settings():
        row = fetch_one("SELECT setting_id FROM BackupSettings WHERE setting_id=1")
        if row:
            return
        execute(
            """
            INSERT INTO BackupSettings (
                setting_id, storage_location, storage_path,
                auto_backup, include_database, include_attachments,
                compress_data, email_notification,
                retention_days, schedule_time, schedule_frequency, encryption_enabled
            ) VALUES (1, ?, ?, 1, 1, 1, 1, 0, 30, '02:00', 'daily', 0)
            """,
            ("Máy chủ nội bộ", "/backup/careplus/"),
        )

    @staticmethod
    def get_settings():
        BackupModel.ensure_tables_exist()
        row = fetch_one("SELECT * FROM BackupSettings WHERE setting_id=1") or {}
        if not row:
            return None
        return row

    @staticmethod
    def update_settings(fields, updated_by_user_id=None):
        BackupModel.ensure_tables_exist()
        allowed = {
            "storage_location",
            "storage_path",
            "auto_backup",
            "include_database",
            "include_attachments",
            "compress_data",
            "email_notification",
            "retention_days",
            "schedule_time",
            "schedule_frequency",
            "encryption_enabled",
        }
        safe_fields = {k: v for k, v in (fields or {}).items() if k in allowed}
        if not safe_fields:
            return False
        if updated_by_user_id:
            safe_fields["updated_by_user_id"] = updated_by_user_id
        set_clause = ", ".join(f"{key}=?" for key in safe_fields.keys())
        params = list(safe_fields.values()) + [1]
        return execute(f"UPDATE BackupSettings SET {set_clause} WHERE setting_id=?", tuple(params))

    @staticmethod
    def list_backups(page=1, limit=10):
        BackupModel.ensure_tables_exist()
        page = max(1, int(page or 1))
        limit = max(1, int(limit or 10))
        offset = (page - 1) * limit

        total_row = fetch_one("SELECT COUNT(*) AS total FROM BackupRecords WHERE is_deleted=0") or {"total": 0}
        total = int(total_row.get("total") or 0)
        rows = fetch_all(
            f"""
            SELECT *
            FROM BackupRecords
            WHERE is_deleted=0
            ORDER BY created_at DESC, backup_id DESC
            {pagination_clause()}
            """,
            pagination_params(limit, offset),
        )
        total_pages = (total + limit - 1) // limit if limit else 1
        return {
            "items": rows,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": max(total_pages, 1),
            },
        }

    @staticmethod
    def get_backup_by_id(backup_id):
        BackupModel.ensure_tables_exist()
        if not backup_id:
            return None
        return fetch_one("SELECT * FROM BackupRecords WHERE backup_id=? AND is_deleted=0", (backup_id,))

    @staticmethod
    def create_backup_record(payload):
        BackupModel.ensure_tables_exist()
        execute(
            """
            INSERT INTO BackupRecords (
                backup_id, created_at, backup_type, size_bytes,
                created_by_user_id, created_by_name, status,
                storage_mode, storage_path, checksum,
                include_database, include_attachments, compress_data,
                error_message, is_deleted, deleted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, NULL)
            """,
            (
                payload.get("backup_id"),
                payload.get("created_at"),
                payload.get("backup_type", "manual"),
                int(payload.get("size_bytes") or 0),
                payload.get("created_by_user_id"),
                payload.get("created_by_name") or "Hệ thống",
                payload.get("status") or "success",
                payload.get("storage_mode") or "local",
                payload.get("storage_path"),
                payload.get("checksum"),
                bool(payload.get("include_database", True)),
                bool(payload.get("include_attachments", True)),
                bool(payload.get("compress_data", True)),
                payload.get("error_message"),
            ),
        )
        return BackupModel.get_backup_by_id(payload.get("backup_id"))

    @staticmethod
    def mark_deleted(backup_id):
        BackupModel.ensure_tables_exist()
        return execute(
            """
            UPDATE BackupRecords
            SET is_deleted=1, deleted_at=?
            WHERE backup_id=? AND is_deleted=0
            """,
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), backup_id),
        )

    @staticmethod
    def create_job(job_payload):
        BackupModel.ensure_tables_exist()
        return execute(
            """
            INSERT INTO BackupJobs (
                job_id, job_type, status, progress,
                message, requested_by_user_id, backup_id,
                started_at, finished_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job_payload.get("job_id"),
                job_payload.get("job_type"),
                job_payload.get("status"),
                int(job_payload.get("progress") or 0),
                job_payload.get("message"),
                job_payload.get("requested_by_user_id"),
                job_payload.get("backup_id"),
                job_payload.get("started_at"),
                job_payload.get("finished_at"),
            ),
        )

    @staticmethod
    def update_job(job_id, fields):
        BackupModel.ensure_tables_exist()
        if not job_id or not fields:
            return False
        safe_fields = {k: v for k, v in fields.items() if k in {"status", "progress", "message", "backup_id", "finished_at"}}
        if not safe_fields:
            return False
        set_clause = ", ".join(f"{key}=?" for key in safe_fields.keys())
        params = list(safe_fields.values()) + [job_id]
        return execute(f"UPDATE BackupJobs SET {set_clause} WHERE job_id=?", tuple(params))

    @staticmethod
    def get_job(job_id):
        BackupModel.ensure_tables_exist()
        if not job_id:
            return None
        return fetch_one("SELECT * FROM BackupJobs WHERE job_id=?", (job_id,))

    @staticmethod
    def add_restore_request(backup_id, requested_by_user_id, confirm_text, create_backup_before_restore, status, message):
        BackupModel.ensure_tables_exist()
        return execute(
            """
            INSERT INTO BackupRestoreRequests (
                backup_id, requested_by_user_id, confirm_text,
                create_backup_before_restore, status, restore_message,
                requested_at, completed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                backup_id,
                requested_by_user_id,
                confirm_text,
                bool(create_backup_before_restore),
                status,
                message,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S") if status in {"success", "failed"} else None,
            ),
        )

    @staticmethod
    def get_summary():
        BackupModel.ensure_tables_exist()
        settings = BackupModel.get_settings() or {}
        total_row = fetch_one(
            """
            SELECT
                COALESCE(SUM(size_bytes), 0) AS total_size,
                COUNT(*) AS total_count
            FROM BackupRecords
            WHERE is_deleted=0
            """
        ) or {"total_size": 0, "total_count": 0}

        last_backup = fetch_one(
            f"""
            SELECT {select_top(1)}backup_id, created_at, status, size_bytes
            FROM BackupRecords
            WHERE is_deleted=0
            ORDER BY created_at DESC, backup_id DESC
            {limit_clause(1)}
            """
        )

        system_status = "safe"
        if not last_backup:
            system_status = "warning"
        elif str(last_backup.get("status") or "").lower() == "failed":
            system_status = "danger"

        schedule_frequency = str(settings.get("schedule_frequency") or "daily")
        schedule_time = str(settings.get("schedule_time") or "02:00")
        next_backup_at = None
        try:
            hour, minute = schedule_time.split(":")
            now = datetime.now()
            candidate = now.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
            if candidate <= now:
                delta = 1
                if schedule_frequency == "weekly":
                    delta = 7
                elif schedule_frequency == "monthly":
                    delta = 30
                candidate = datetime.fromtimestamp(candidate.timestamp() + delta * 24 * 60 * 60)
            next_backup_at = candidate.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            next_backup_at = None

        return {
            "total_size_bytes": int(total_row.get("total_size") or 0),
            "total_backups": int(total_row.get("total_count") or 0),
            "last_backup": last_backup,
            "next_backup_at": next_backup_at,
            "schedule_time": schedule_time,
            "schedule_frequency": schedule_frequency,
            "system_status": system_status,
            "storage_location": settings.get("storage_location") or "Máy chủ nội bộ",
            "storage_path": settings.get("storage_path") or "/backup/careplus/",
            "retention_days": int(settings.get("retention_days") or 30),
            "settings": settings,
        }

    @staticmethod
    def seed_sample_data():
        BackupModel.ensure_tables_exist()

        existing = fetch_one("SELECT COUNT(*) AS c FROM BackupRecords") or {"c": 0}
        if int(existing.get("c") or 0) > 0:
            return False

        now = datetime.now()
        samples = [
            {
                "backup_id": "backup_demo_001",
                "created_at": now.strftime("%Y-%m-%d 02:00:00"),
                "backup_type": "automatic",
                "size_bytes": 26628797235,
                "created_by_user_id": None,
                "created_by_name": "Hệ thống",
                "status": "success",
                "storage_mode": "local",
                "storage_path": "backups/local/backup_demo_001.json",
                "checksum": "sha256-demo-001",
                "include_database": True,
                "include_attachments": True,
                "compress_data": True,
            },
            {
                "backup_id": "backup_demo_002",
                "created_at": (now.replace(hour=2, minute=0, second=0, microsecond=0)).strftime("%Y-%m-%d %H:%M:%S"),
                "backup_type": "automatic",
                "size_bytes": 26228797235,
                "created_by_user_id": None,
                "created_by_name": "Hệ thống",
                "status": "success",
                "storage_mode": "cloud",
                "storage_path": "backups/cloud/backup_demo_002.json",
                "checksum": "sha256-demo-002",
                "include_database": True,
                "include_attachments": True,
                "compress_data": True,
            },
            {
                "backup_id": "backup_demo_003",
                "created_at": (now.replace(hour=1, minute=20, second=0, microsecond=0)).strftime("%Y-%m-%d %H:%M:%S"),
                "backup_type": "manual",
                "size_bytes": 25728797235,
                "created_by_user_id": 1,
                "created_by_name": "Admin",
                "status": "failed",
                "storage_mode": "local",
                "storage_path": "backups/local/backup_demo_003.json",
                "checksum": None,
                "include_database": True,
                "include_attachments": True,
                "compress_data": True,
                "error_message": "Không đủ dung lượng lưu trữ",
            },
        ]
        for row in samples:
            BackupModel.create_backup_record(row)

        settings = BackupModel.get_settings() or {}
        if not settings:
            return True
        BackupModel.update_settings(
            {
                "storage_location": "Máy chủ nội bộ",
                "storage_path": "backups/local",
                "auto_backup": True,
                "include_database": True,
                "include_attachments": True,
                "compress_data": True,
                "email_notification": False,
                "retention_days": 30,
                "schedule_time": "02:00",
                "schedule_frequency": "daily",
                "encryption_enabled": False,
            },
            updated_by_user_id=1,
        )
        return True

    @staticmethod
    def dump_settings_snapshot(user_id, mode):
        settings = BackupModel.get_settings() or {}
        safe_payload = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "generated_by_user_id": user_id,
            "storage_mode": mode,
            "settings": settings,
        }
        return json.dumps(safe_payload, ensure_ascii=False, indent=2)
