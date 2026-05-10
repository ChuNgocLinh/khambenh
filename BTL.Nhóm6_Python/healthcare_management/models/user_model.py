from database.db import fetch_one, execute
import hashlib
import re

class UserModel:

    @staticmethod
    def normalize_role(role, username=""):
        normalized_role = str(role or "").lower().strip()
        normalized_username = str(username or "").lower().strip()

        # Hỗ trợ dữ liệu cũ: chỉ ánh xạ các username staff dạng legacy rõ ràng (staff + số)
        # để tránh false-positive cho patient username bắt đầu bằng "staff".
        if normalized_role == "patient" and re.match(r"^staff\d+$", normalized_username):
            return "staff"
        return normalized_role

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def login(username, password):
        hashed_password = UserModel.hash_password(password)
        query = "SELECT user_id, username, password, role FROM Users WHERE username=? AND password=?"
        row = fetch_one(query, (username, hashed_password))
        
        if not row:
            return None
            
        if isinstance(row, tuple):
            user_data = {
                "user_id": row[0],
                "username": row[1],
                "password": row[2],
                "role": row[3]
            }
        elif isinstance(row, dict):
            user_data = row
        else:
            return None

        user_data["role"] = UserModel.normalize_role(user_data.get("role"), user_data.get("username"))
            
        # Dựa vào role, lấy thêm id của patient hoặc doctor
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
        elif user_data["role"] == "admin":
            user_data["name"] = "Admin"
        else:
            user_data.setdefault("name", user_data.get("username", "Unknown"))
                
        return user_data

    @staticmethod
    def register_patient(username, password, name, phone, email):
        # Kiểm tra xem username đã tồn tại chưa
        if fetch_one("SELECT user_id FROM Users WHERE username=?", (username,)):
            return False, "Tài khoản đã tồn tại"
            
        # Thêm user
        hashed_password = UserModel.hash_password(password)
        success = execute("INSERT INTO Users (username, password, role) VALUES (?, ?, 'patient')", (username, hashed_password))
        if not success:
            return False, "Lỗi tạo tài khoản"
            
        # Lấy user_id vừa tạo
        new_user = fetch_one("SELECT user_id FROM Users WHERE username=?", (username,))
        if not new_user:
            return False, "Không tìm thấy tài khoản vừa tạo"

        user_id = new_user.get("user_id") if isinstance(new_user, dict) else new_user[0]
        
        # Thêm patient
        success = execute("INSERT INTO Patients (name, phone, user_id) VALUES (?, ?, ?)", (name, phone, user_id))
        if not success:
            return False, "Lỗi tạo thông tin bệnh nhân"
            
        return True, "Đăng ký thành công"

    @staticmethod
    def verify_password(user_id, password):
        row = fetch_one("SELECT password FROM Users WHERE user_id=?", (user_id,))
        if not row:
            return False

        hashed_input = UserModel.hash_password(password)
        stored_hash = str(row.get("password", "")) if isinstance(row, dict) else str(row[0])

        if hashed_input == stored_hash:
            return True

        # Support legacy plaintext passwords and migrate on successful verification.
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
