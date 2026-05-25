import hashlib
import logging
import re

from config import DB_TYPE
from database.db import execute, fetch_all, fetch_one


class UserModel:
    LEGACY_STAFF_ROLE_FALLBACK: bool = False
    CANONICAL_ROLES: set[str] = {"admin", "staff", "doctor", "patient"}
    STAFF_EFFECTIVE_ROLES: set[str] = {"staff", "receptionist", "accountant", "nurse"}
    _auth_schema_checked = False

    @staticmethod
    def normalize_role(role):
        return str(role or "").lower().strip()

    @staticmethod
    def resolve_login_role(role, username=""):
        normalized_role = UserModel.normalize_role(role)
        normalized_username = str(username or "").lower().strip()

        if normalized_role in UserModel.CANONICAL_ROLES:
            return normalized_role

        if (
            UserModel.LEGACY_STAFF_ROLE_FALLBACK
            and normalized_role == "patient"
            and re.match(r"^staff\d+$", normalized_username)
        ):
            logging.warning(
                "LEGACY_STAFF_ROLE_FALLBACK applied for username='%s': role '%s' -> 'staff'",
                normalized_username,
                normalized_role,
            )
            return "staff"

        return normalized_role

    @staticmethod
    def _ensure_auth_schema():
        pass

    @staticmethod
    def _load_effective_roles(user_id, base_role):
        role_rows = fetch_all(
            """
            SELECT DISTINCT r.role_key
            FROM rbac_user_role_assignments ura
            JOIN rbac_roles r ON r.role_id = ura.role_id
            WHERE ura.user_id = ?
              AND COALESCE(ura.is_active, 1) = 1
              AND COALESCE(r.is_active, 1) = 1
            ORDER BY r.role_key
            """,
            (user_id,),
        )
        effective_roles = [
            UserModel.normalize_role(row.get("role_key"))
            for row in (role_rows or [])
            if row.get("role_key")
        ]

        normalized_base = UserModel.normalize_role(base_role)
        if normalized_base and normalized_base not in effective_roles:
            effective_roles.insert(0, normalized_base)

        return [role for role in effective_roles if role]

    @staticmethod
    def _load_permissions(user_id):
        rows = fetch_all(
            """
            SELECT DISTINCT p.permission_key
            FROM rbac_user_role_assignments ura
            JOIN rbac_roles r ON r.role_id = ura.role_id
            JOIN rbac_role_permissions rp ON rp.role_id = r.role_id
            JOIN rbac_permissions p ON p.permission_id = rp.permission_id
            WHERE ura.user_id = ?
              AND COALESCE(ura.is_active, 1) = 1
              AND COALESCE(r.is_active, 1) = 1
              AND COALESCE(p.is_active, 1) = 1
              AND COALESCE(rp.allowed, 1) = 1
            ORDER BY p.permission_key
            """,
            (user_id,),
        )
        return [
            str(row.get("permission_key"))
            for row in (rows or [])
            if row.get("permission_key")
        ]

    @staticmethod
    def _shell_role(base_role, effective_roles):
        normalized_base = UserModel.normalize_role(base_role)
        normalized_effective = {
            UserModel.normalize_role(role)
            for role in (effective_roles or [])
        }
        if normalized_effective & UserModel.STAFF_EFFECTIVE_ROLES:
            return "staff"
        if normalized_base in UserModel.CANONICAL_ROLES:
            return normalized_base
        return normalized_base

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def login(username, password):
        UserModel._ensure_auth_schema()
        hashed_password = UserModel.hash_password(password)
        query = """
            SELECT user_id, username, password, role, COALESCE(is_active, 1) AS is_active, deleted_at
            FROM Users
            WHERE username=?
              AND password=?
              AND COALESCE(is_active, 1) = 1
              AND deleted_at IS NULL
        """
        row = fetch_one(query, (username, hashed_password))

        if not row:
            return None

        if isinstance(row, tuple):
            user_data = {
                "user_id": row[0],
                "username": row[1],
                "password": row[2],
                "role": row[3],
                "is_active": row[4] if len(row) > 4 else 1,
                "deleted_at": row[5] if len(row) > 5 else None,
            }
        elif isinstance(row, dict):
            user_data = row
        else:
            return None

        base_role = UserModel.resolve_login_role(
            user_data.get("role"),
            user_data.get("username") or "",
        )
        user_data["effective_roles"] = UserModel._load_effective_roles(user_data.get("user_id"), base_role)
        user_data["permissions"] = UserModel._load_permissions(user_data.get("user_id"))
        user_data["role"] = UserModel._shell_role(base_role, user_data["effective_roles"])

        if user_data["role"] in ("patient", "staff"):
            p_row = fetch_one("SELECT patient_id, name FROM Patients WHERE user_id=?", (user_data["user_id"],))
            if p_row:
                p_dict = p_row if isinstance(p_row, dict) else {"patient_id": p_row[0], "name": p_row[1]}
                user_data["patient_id"] = p_dict.get("patient_id")
                user_data["name"] = p_dict.get("name")
            else:
                user_data["name"] = user_data.get("username")
        elif user_data["role"] == "doctor":
            d_row = fetch_one("SELECT doctor_id, name FROM Doctors WHERE user_id=?", (user_data["user_id"],))
            if d_row:
                d_dict = d_row if isinstance(d_row, dict) else {"doctor_id": d_row[0], "name": d_row[1]}
                user_data["doctor_id"] = d_dict.get("doctor_id")
                user_data["name"] = d_dict.get("name")
            else:
                user_data["name"] = user_data.get("username")
        elif user_data["role"] == "admin":
            user_data["name"] = user_data.get("username") or "Admin"
        else:
            user_data.setdefault("name", user_data.get("username", "Unknown"))

        return user_data

    @staticmethod
    def register_patient(username, password, name, phone, email):
        UserModel._ensure_auth_schema()
        if fetch_one("SELECT user_id FROM Users WHERE username=?", (username,)):
            return False, "Tai khoan da ton tai"

        hashed_password = UserModel.hash_password(password)
        success = execute(
            "INSERT INTO Users (username, password, role, is_active) VALUES (?, ?, 'patient', 1)",
            (username, hashed_password),
        )
        if not success:
            return False, "Loi tao tai khoan"

        new_user = fetch_one("SELECT user_id FROM Users WHERE username=?", (username,))
        if not new_user:
            return False, "Khong tim thay tai khoan vua tao"

        user_id = new_user.get("user_id") if isinstance(new_user, dict) else new_user[0]

        success = execute(
            "INSERT INTO Patients (name, phone, email, user_id, is_active) VALUES (?, ?, ?, ?, 1)",
            (name, phone, email, user_id),
        )
        if not success:
            return False, "Loi tao thong tin benh nhan"

        return True, "Dang ky thanh cong"

    @staticmethod
    def verify_password(user_id, password):
        row = fetch_one("SELECT password FROM Users WHERE user_id=? AND COALESCE(is_active, 1)=1", (user_id,))
        if not row:
            return False

        hashed_input = UserModel.hash_password(password)
        stored_hash = str(row.get("password", "")) if isinstance(row, dict) else str(row[0])

        if hashed_input == stored_hash:
            return True

        if password == stored_hash:
            execute("UPDATE Users SET password=? WHERE user_id=?", (hashed_input, user_id))
            return True

        return False

    @staticmethod
    def change_password(user_id, current_password, new_password):
        if not UserModel.verify_password(user_id, current_password):
            return False

        new_hash = UserModel.hash_password(new_password)
        return execute("UPDATE Users SET password=? WHERE user_id=?", (new_hash, user_id))
