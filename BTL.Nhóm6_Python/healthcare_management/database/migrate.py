import re

from database.db import connect


LEGACY_STAFF_USERNAME_PATTERN = re.compile(r"^staff\d+$")
CANONICAL_ROLES = ("admin", "doctor", "patient", "staff")


def _get_role_distribution(cursor):
    cursor.execute("SELECT role, COUNT(*) AS total FROM Users GROUP BY role")
    rows = cursor.fetchall() or []
    return {str(role): int(total) for role, total in rows}


def _format_distribution(distribution):
    ordered = [f"{role}={distribution.get(role, 0)}" for role in CANONICAL_ROLES]
    non_canonical = sorted(
        (role, count)
        for role, count in distribution.items()
        if role not in CANONICAL_ROLES
    )
    ordered.extend(f"{role}={count}" for role, count in non_canonical)
    return ", ".join(ordered)


def _normalize_users_role_check_mysql(cursor):
    """
    MySQL version-safe: chỉ cố gắng thêm CHECK nếu chưa tồn tại biểu thức có staff.
    Không raise lỗi nếu engine/version không hỗ trợ DROP/ADD CHECK.
    """
    cursor.execute(
        """
        SELECT tc.CONSTRAINT_NAME, cc.CHECK_CLAUSE
        FROM information_schema.TABLE_CONSTRAINTS tc
        JOIN information_schema.CHECK_CONSTRAINTS cc
          ON tc.CONSTRAINT_SCHEMA = cc.CONSTRAINT_SCHEMA
         AND tc.CONSTRAINT_NAME = cc.CONSTRAINT_NAME
        WHERE tc.TABLE_SCHEMA = DATABASE()
          AND tc.TABLE_NAME = 'Users'
          AND tc.CONSTRAINT_TYPE = 'CHECK'
        """
    )
    checks = cursor.fetchall() or []

    def has_staff_role_check(clause):
        normalized = str(clause or "").replace(" ", "").lower()
        return (
            "role" in normalized
            and "admin" in normalized
            and "doctor" in normalized
            and "patient" in normalized
            and "staff" in normalized
        )

    if any(has_staff_role_check(clause) for _, clause in checks):
        return

    for name, _ in checks:
        try:
            cursor.execute(f"ALTER TABLE Users DROP CHECK {name}")
        except Exception:
            # DB/phiên bản không hỗ trợ DROP CHECK theo cú pháp này.
            pass

    try:
        cursor.execute(
            "ALTER TABLE Users ADD CONSTRAINT chk_users_role "
            "CHECK (role IN ('admin','doctor','patient','staff'))"
        )
    except Exception:
        # Bỏ qua để không làm hỏng migration nếu CHECK không hỗ trợ cưỡng chế.
        pass


def migrate_legacy_staff_roles():
    conn = connect()
    if not conn:
        raise RuntimeError("Không thể kết nối database")

    cursor = conn.cursor()
    migrated_count = 0

    try:
        before_distribution = _get_role_distribution(cursor)

        # Đồng bộ CHECK role an toàn cho MySQL nếu cần.
        _normalize_users_role_check_mysql(cursor)

        # Chỉ backfill dữ liệu cũ theo đúng normalize_role:
        # role='patient' AND username khớp ^staff\d+$
        cursor.execute("SELECT user_id, username FROM Users WHERE role='patient'")
        candidate_rows = cursor.fetchall() or []

        legacy_staff_user_ids = []
        for user_id, username in candidate_rows:
            normalized_username = str(username or "").lower().strip()
            if LEGACY_STAFF_USERNAME_PATTERN.match(normalized_username):
                legacy_staff_user_ids.append(int(user_id))

        if legacy_staff_user_ids:
            placeholders = ",".join(["%s"] * len(legacy_staff_user_ids))
            cursor.execute(
                f"UPDATE Users SET role='staff' "
                f"WHERE user_id IN ({placeholders}) AND role='patient'",
                legacy_staff_user_ids,
            )
            migrated_count = int(cursor.rowcount or 0)

        conn.commit()

        after_distribution = _get_role_distribution(cursor)

        print("[role-migrate] before:", _format_distribution(before_distribution))
        print("[role-migrate] migrated_to_staff:", migrated_count)
        print("[role-migrate] after:", _format_distribution(after_distribution))

        return {
            "before": before_distribution,
            "after": after_distribution,
            "migrated_to_staff": migrated_count,
        }
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def run_schema_migrations():
    conn = connect()
    if not conn:
        raise RuntimeError("Không thể kết nối database")
    cursor = conn.cursor()
    try:
        # Helper to check if column exists
        def column_exists(table, column):
            cursor.execute(
                f"SELECT COUNT(*) FROM information_schema.COLUMNS "
                f"WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = '{table}' AND COLUMN_NAME = '{column}'"
            )
            row = cursor.fetchone()
            return row and int(row[0]) > 0

        # Helper to check if table exists
        def table_exists(table):
            cursor.execute(
                f"SELECT COUNT(*) FROM information_schema.TABLES "
                f"WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = '{table}'"
            )
            row = cursor.fetchone()
            return row and int(row[0]) > 0

        # Check and create RBAC tables if missing
        if not table_exists("rbac_roles"):
            cursor.execute(
                """
                CREATE TABLE rbac_roles (
                    role_id INT AUTO_INCREMENT PRIMARY KEY,
                    role_key VARCHAR(50) NOT NULL UNIQUE,
                    display_name VARCHAR(100) NOT NULL,
                    description VARCHAR(255),
                    color_kind VARCHAR(20) DEFAULT 'neutral',
                    is_system BOOLEAN DEFAULT FALSE,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
                """
            )
        if not table_exists("rbac_permission_groups"):
            cursor.execute(
                """
                CREATE TABLE rbac_permission_groups (
                    group_id INT AUTO_INCREMENT PRIMARY KEY,
                    group_key VARCHAR(100) NOT NULL UNIQUE,
                    display_name VARCHAR(150) NOT NULL,
                    description VARCHAR(255),
                    sort_order INT DEFAULT 0,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        if not table_exists("rbac_permissions"):
            cursor.execute(
                """
                CREATE TABLE rbac_permissions (
                    permission_id INT AUTO_INCREMENT PRIMARY KEY,
                    group_id INT NOT NULL,
                    permission_key VARCHAR(120) NOT NULL UNIQUE,
                    display_name VARCHAR(150) NOT NULL,
                    description VARCHAR(255),
                    is_sensitive BOOLEAN DEFAULT FALSE,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (group_id) REFERENCES rbac_permission_groups(group_id)
                )
                """
            )
        if not table_exists("rbac_role_permissions"):
            cursor.execute(
                """
                CREATE TABLE rbac_role_permissions (
                    role_id INT NOT NULL,
                    permission_id INT NOT NULL,
                    allowed BOOLEAN DEFAULT TRUE,
                    granted_by_user_id INT NULL,
                    granted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (role_id, permission_id),
                    FOREIGN KEY (role_id) REFERENCES rbac_roles(role_id),
                    FOREIGN KEY (permission_id) REFERENCES rbac_permissions(permission_id),
                    FOREIGN KEY (granted_by_user_id) REFERENCES Users(user_id)
                )
                """
            )
        if not table_exists("rbac_user_role_assignments"):
            cursor.execute(
                """
                CREATE TABLE rbac_user_role_assignments (
                    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    role_id INT NOT NULL,
                    assigned_by_user_id INT NULL,
                    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    UNIQUE KEY uq_rbac_user_role_active (user_id, role_id),
                    FOREIGN KEY (user_id) REFERENCES Users(user_id),
                    FOREIGN KEY (role_id) REFERENCES rbac_roles(role_id),
                    FOREIGN KEY (assigned_by_user_id) REFERENCES Users(user_id)
                )
                """
            )
        if not table_exists("rbac_audit_logs"):
            cursor.execute(
                """
                CREATE TABLE rbac_audit_logs (
                    audit_id INT AUTO_INCREMENT PRIMARY KEY,
                    actor_user_id INT NULL,
                    action_key VARCHAR(100) NOT NULL,
                    target_type VARCHAR(50) NOT NULL,
                    target_id VARCHAR(100) NOT NULL,
                    details TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (actor_user_id) REFERENCES Users(user_id)
                )
                """
            )

        # 1. Users table
        if not column_exists("Users", "deleted_at"):
            cursor.execute("ALTER TABLE Users ADD COLUMN deleted_at DATETIME NULL")
        if not column_exists("Users", "force_change_password"):
            cursor.execute("ALTER TABLE Users ADD COLUMN force_change_password BOOLEAN DEFAULT FALSE")

        # 2. Doctors table
        if not column_exists("Doctors", "work_status"):
            cursor.execute("ALTER TABLE Doctors ADD COLUMN work_status VARCHAR(50) DEFAULT 'active'")
        if not column_exists("Doctors", "created_at"):
            cursor.execute("ALTER TABLE Doctors ADD COLUMN created_at DATETIME NULL")
        if not column_exists("Doctors", "updated_at"):
            cursor.execute("ALTER TABLE Doctors ADD COLUMN updated_at DATETIME NULL")

        # 3. Appointments table
        if not column_exists("Appointments", "service_id"):
            cursor.execute("ALTER TABLE Appointments ADD COLUMN service_id INT NULL")
            try:
                cursor.execute("ALTER TABLE Appointments ADD CONSTRAINT fk_appointments_services FOREIGN KEY (service_id) REFERENCES Services(service_id)")
            except Exception:
                pass

        # 4. MedicalRecords table
        if not column_exists("MedicalRecords", "symptoms"):
            cursor.execute("ALTER TABLE MedicalRecords ADD COLUMN symptoms TEXT NULL")
        if not column_exists("MedicalRecords", "conclusion"):
            cursor.execute("ALTER TABLE MedicalRecords ADD COLUMN conclusion TEXT NULL")
        if not column_exists("MedicalRecords", "notes"):
            cursor.execute("ALTER TABLE MedicalRecords ADD COLUMN notes TEXT NULL")

        conn.commit()
        print("[schema-migrate] Schema migrations completed successfully.")
    except Exception as e:
        conn.rollback()
        print(f"[schema-migrate] Error: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    run_schema_migrations()
    migrate_legacy_staff_roles()
