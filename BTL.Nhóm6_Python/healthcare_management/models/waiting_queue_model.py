from datetime import datetime

from config import DB_TYPE
from database.db import execute, fetch_all, fetch_one
from database.sql_utils import by_date_filter


class WaitingQueueModel:
    _schema_checked = False

    @staticmethod
    def ensure_schema():
        if WaitingQueueModel._schema_checked:
            return
        WaitingQueueModel._schema_checked = True

        if DB_TYPE == "mysql":
            execute(
                """
                CREATE TABLE IF NOT EXISTS WaitingQueue (
                    queue_id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT NOT NULL,
                    appointment_id INT NULL,
                    queue_no VARCHAR(20) NOT NULL,
                    queue_area VARCHAR(20) NOT NULL DEFAULT '3B',
                    status VARCHAR(20) NOT NULL DEFAULT 'waiting',
                    intake_note VARCHAR(500),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            return

        execute(
            """
            IF OBJECT_ID('dbo.WaitingQueue', 'U') IS NULL
            BEGIN
                CREATE TABLE dbo.WaitingQueue (
                    queue_id INT IDENTITY(1,1) PRIMARY KEY,
                    patient_id INT NOT NULL,
                    appointment_id INT NULL,
                    queue_no NVARCHAR(20) NOT NULL,
                    queue_area NVARCHAR(20) NOT NULL DEFAULT N'3B',
                    status NVARCHAR(20) NOT NULL DEFAULT N'waiting',
                    intake_note NVARCHAR(500) NULL,
                    created_at DATETIME2 DEFAULT SYSUTCDATETIME(),
                    updated_at DATETIME2 DEFAULT SYSUTCDATETIME()
                )
            END
            """
        )

    @staticmethod
    def _next_queue_no(area="3B"):
        WaitingQueueModel.ensure_schema()
        today = datetime.now().strftime("%Y-%m-%d")
        row = fetch_one(
            f"""
            SELECT COUNT(*) AS total
            FROM WaitingQueue
            WHERE queue_area = ?
              AND {by_date_filter('created_at')}
            """,
            (area, today),
        ) or {"total": 0}
        return f"{area}-{int(row.get('total') or 0) + 1:03d}"

    @staticmethod
    def check_in(patient_id, appointment_id=None, intake_note="", area="3B"):
        WaitingQueueModel.ensure_schema()
        existing = None
        if appointment_id:
            existing = fetch_one(
                """
                SELECT *
                FROM WaitingQueue
                WHERE appointment_id = ?
                  AND status IN ('waiting', 'called', 'in_consultation')
                ORDER BY queue_id DESC
                """,
                (appointment_id,),
            )
        if existing:
            return existing

        queue_no = WaitingQueueModel._next_queue_no(area)
        ok = execute(
            """
            INSERT INTO WaitingQueue (
                patient_id, appointment_id, queue_no, queue_area, status, intake_note, created_at, updated_at
            ) VALUES (?, ?, ?, ?, 'waiting', ?, ?, ?)
            """,
            (
                patient_id,
                appointment_id,
                queue_no,
                area,
                intake_note,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        if not ok:
            return None
        return fetch_one("SELECT * FROM WaitingQueue WHERE queue_no=? AND queue_area=?", (queue_no, area))

    @staticmethod
    def get_waiting(area="3B"):
        WaitingQueueModel.ensure_schema()
        return fetch_all(
            """
            SELECT q.*, p.name AS patient_name, p.phone AS patient_phone, a.appointment_date
            FROM WaitingQueue q
            JOIN Patients p ON p.patient_id = q.patient_id
            LEFT JOIN Appointments a ON a.appointment_id = q.appointment_id
            WHERE q.queue_area = ?
              AND q.status IN ('waiting', 'called', 'in_consultation')
            ORDER BY q.created_at ASC, q.queue_id ASC
            """,
            (area,),
        )
