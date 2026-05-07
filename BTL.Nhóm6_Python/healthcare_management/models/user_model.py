from database.db import fetch_one, execute
import hashlib

class UserModel:

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
            
        # Dựa vào role, lấy thêm id của patient hoặc doctor
        if user_data["role"] == "patient":
            p_row = fetch_one("SELECT patient_id, name FROM Patients WHERE user_id=?", (user_data["user_id"],))
            if p_row:
                p_dict = p_row if isinstance(p_row, dict) else {"patient_id": p_row[0], "name": p_row[1]}
                user_data["patient_id"] = p_dict.get("patient_id")
                user_data["name"] = p_dict.get("name")
        elif user_data["role"] == "doctor":
            d_row = fetch_one("SELECT doctor_id, name FROM Doctors WHERE user_id=?", (user_data["user_id"],))
            if d_row:
                d_dict = d_row if isinstance(d_row, dict) else {"doctor_id": d_row[0], "name": d_row[1]}
                user_data["doctor_id"] = d_dict.get("doctor_id")
                user_data["name"] = d_dict.get("name")
        elif user_data["role"] == "admin":
            user_data["name"] = "Admin"
                
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
        user_id = new_user.get("user_id") if isinstance(new_user, dict) else new_user[0]
        
        # Thêm patient
        success = execute("INSERT INTO Patients (name, phone, user_id) VALUES (?, ?, ?)", (name, phone, user_id))
        if not success:
            return False, "Lỗi tạo thông tin bệnh nhân"
            
        return True, "Đăng ký thành công"