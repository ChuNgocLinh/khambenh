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


if __name__ == "__main__":
    migrate_legacy_staff_roles()
