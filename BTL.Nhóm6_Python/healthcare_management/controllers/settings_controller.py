import re
import json
import shutil
from pathlib import Path
from datetime import datetime
from importlib import import_module


class SettingsController:
    DISPLAY_OPTION_MAP = {
        "theme_mode": ["Sáng", "Tối"],
        "font_size": ["Nhỏ", "Trung bình", "Lớn"],
        "display_density": ["Thoải mái", "Gọn"],
    }
    LANGUAGES = ["Tiếng Việt", "English"]

    @staticmethod
    def _normalize_doctor_name(name):
        normalized_name = str(name or "").strip()
        if normalized_name.lower().startswith("bác sĩ "):
            return normalized_name[7:].strip()
        return normalized_name

    @staticmethod
    def get_settings(user_id):
        if not user_id:
            return None
        SettingsModel = import_module("models.settings_model").SettingsModel
        return SettingsModel.get_or_create_by_user_id(user_id)

    @staticmethod
    def update_personal_info(doctor_id, user_id, payload):
        DoctorModel = import_module("models.doctor_model").DoctorModel
        SettingsModel = import_module("models.settings_model").SettingsModel

        name = SettingsController._normalize_doctor_name(payload.get("name", ""))
        if not name:
            return False, "Vui lòng nhập họ tên."
        if len(name) > 100:
            return False, "Họ tên không được vượt quá 100 ký tự."

        email = str(payload.get("email", "")).strip().lower()
        if email and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            return False, "Email không hợp lệ."
        if len(email) > 100:
            return False, "Email không được vượt quá 100 ký tự."

        phone = str(payload.get("phone", "")).strip()
        if phone and not re.match(r"^[0-9+\-\s]{8,20}$", phone):
            return False, "Số điện thoại không hợp lệ."

        specialty = str(payload.get("specialty", "")).strip()
        if len(specialty) > 100:
            return False, "Chuyên khoa không được vượt quá 100 ký tự."

        gender = str(payload.get("gender", "Nam")).strip() or "Nam"
        if gender not in {"Nam", "Nữ"}:
            return False, "Giới tính không hợp lệ."

        dob = payload.get("dob")
        if dob:
            try:
                datetime.strptime(str(dob), "%Y-%m-%d")
            except ValueError:
                return False, "Ngày sinh không hợp lệ."

        address = str(payload.get("address", "")).strip()
        if len(address) > 255:
            return False, "Địa chỉ không được vượt quá 255 ký tự."

        previous_doctor = DoctorModel.get_by_id(doctor_id) or {}

        doctor_saved = DoctorModel.update_profile_details(
            doctor_id=doctor_id,
            name=name,
            specialty=specialty,
            phone=phone,
            email=email,
        )
        if not doctor_saved:
            return False, "Không thể cập nhật hồ sơ bác sĩ."

        SettingsModel.get_or_create_by_user_id(user_id)
        settings_saved = SettingsModel.update_fields(
            user_id,
            {
                "gender": gender,
                "dob": dob,
                "address": address,
            },
        )
        if not settings_saved:
            if isinstance(previous_doctor, dict):
                # Roll back doctor profile update to reduce cross-table inconsistency.
                DoctorModel.update_profile_details(
                    doctor_id=doctor_id,
                    name=str(previous_doctor.get("name", "")),
                    specialty=str(previous_doctor.get("specialty", "")),
                    phone=str(previous_doctor.get("phone", "")),
                    email=str(previous_doctor.get("email", "")),
                )
            return False, "Không thể lưu cài đặt cá nhân."

        return True, "Đã lưu thông tin cá nhân thành công."

    @staticmethod
    def update_avatar(user_id, avatar_path):
        if not user_id:
            return False
        if not avatar_path or not Path(avatar_path).is_file():
            return False

        SettingsModel = import_module("models.settings_model").SettingsModel
        SettingsModel.get_or_create_by_user_id(user_id)
        return SettingsModel.update_fields(user_id, {"avatar_path": avatar_path})

    @staticmethod
    def update_notification(user_id, key, value):
        if key not in {"notify_new_appointment", "notify_reminder", "notify_system"}:
            return False

        SettingsModel = import_module("models.settings_model").SettingsModel
        SettingsModel.get_or_create_by_user_id(user_id)
        return SettingsModel.update_fields(user_id, {key: bool(value)})

    @staticmethod
    def update_display_option(user_id, key, value):
        allowed_values = SettingsController.DISPLAY_OPTION_MAP.get(key)
        if not allowed_values or value not in allowed_values:
            return False

        SettingsModel = import_module("models.settings_model").SettingsModel
        SettingsModel.get_or_create_by_user_id(user_id)
        return SettingsModel.update_fields(user_id, {key: value})

    @staticmethod
    def update_language(user_id, language):
        if language not in SettingsController.LANGUAGES:
            return False

        SettingsModel = import_module("models.settings_model").SettingsModel
        SettingsModel.get_or_create_by_user_id(user_id)
        return SettingsModel.update_fields(user_id, {"language": language})

    @staticmethod
    def backup_now(user_id, backup_mode):
        if backup_mode not in {"cloud", "local"}:
            return False, "Chế độ backup không hợp lệ."

        SettingsModel = import_module("models.settings_model").SettingsModel
        user_settings = SettingsModel.get_or_create_by_user_id(user_id)
        if not isinstance(user_settings, dict):
            return False, "Không thể tải cài đặt người dùng."

        doctor_data = import_module("database.db").fetch_one(
            "SELECT * FROM Doctors WHERE user_id=?",
            (user_id,),
        ) or {}

        if not isinstance(doctor_data, dict):
            doctor_data = {}

        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        backups_root = Path(__file__).resolve().parents[1] / "backups"
        local_dir = backups_root / "local"
        cloud_dir = backups_root / "cloud"
        local_dir.mkdir(parents=True, exist_ok=True)
        cloud_dir.mkdir(parents=True, exist_ok=True)

        backup_payload = {
            "generated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id,
            "doctor": {
                "doctor_id": doctor_data.get("doctor_id"),
                "name": doctor_data.get("name"),
                "specialty": doctor_data.get("specialty"),
                "phone": doctor_data.get("phone"),
                "email": doctor_data.get("email"),
            },
            "settings": {
                "gender": user_settings.get("gender"),
                "dob": user_settings.get("dob"),
                "address": user_settings.get("address"),
                "avatar_path": user_settings.get("avatar_path"),
                "notify_new_appointment": user_settings.get("notify_new_appointment"),
                "notify_reminder": user_settings.get("notify_reminder"),
                "notify_system": user_settings.get("notify_system"),
                "theme_mode": user_settings.get("theme_mode"),
                "font_size": user_settings.get("font_size"),
                "display_density": user_settings.get("display_density"),
                "language": user_settings.get("language"),
                "backup_mode": backup_mode,
            },
        }

        local_file = local_dir / f"settings_user_{user_id}_{timestamp}.json"
        with local_file.open("w", encoding="utf-8") as backup_file:
            json.dump(backup_payload, backup_file, ensure_ascii=False, indent=2)

        if backup_mode == "cloud":
            cloud_file = cloud_dir / local_file.name
            shutil.copy2(local_file, cloud_file)

        SettingsModel.get_or_create_by_user_id(user_id)
        saved = SettingsModel.update_fields(
            user_id,
            {
                "backup_mode": backup_mode,
                "last_backup_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
        )
        if not saved:
            return False, "Đã tạo file backup nhưng không thể cập nhật trạng thái vào DB."

        return True, str(local_file)

    @staticmethod
    def sync_now(user_id):
        SettingsModel = import_module("models.settings_model").SettingsModel

        now = datetime.now()
        backups_root = Path(__file__).resolve().parents[1] / "backups"
        local_dir = backups_root / "local"
        cloud_dir = backups_root / "cloud"
        local_dir.mkdir(parents=True, exist_ok=True)
        cloud_dir.mkdir(parents=True, exist_ok=True)

        backup_files = sorted(local_dir.glob("settings_user_*.json"), key=lambda path: path.stat().st_mtime)
        if not backup_files:
            return False, "Chưa có file backup local để đồng bộ."

        synced_count = 0
        for backup_file in backup_files:
            destination = cloud_dir / backup_file.name
            shutil.copy2(backup_file, destination)
            synced_count += 1

        SettingsModel.get_or_create_by_user_id(user_id)
        saved = SettingsModel.update_fields(
            user_id,
            {
                "last_sync_at": now.strftime("%Y-%m-%d %H:%M:%S"),
            },
        )
        if not saved:
            return False, "Đồng bộ file thành công nhưng không thể cập nhật trạng thái vào DB."

        return True, f"Đã đồng bộ {synced_count} file backup lên thư mục cloud."

    @staticmethod
    def change_password(user_id, current_password, new_password, confirm_password):
        UserModel = import_module("models.user_model").UserModel

        if not current_password or not new_password or not confirm_password:
            return False, "Vui lòng nhập đầy đủ thông tin mật khẩu."

        if new_password != confirm_password:
            return False, "Mật khẩu xác nhận không khớp."

        if len(new_password) < 8:
            return False, "Mật khẩu mới phải có ít nhất 8 ký tự."

        if new_password == current_password:
            return False, "Mật khẩu mới không được trùng mật khẩu cũ."

        changed = UserModel.change_password(user_id, current_password, new_password)
        if not changed:
            return False, "Mật khẩu cũ không chính xác hoặc cập nhật thất bại."

        return True, "Đổi mật khẩu thành công."
