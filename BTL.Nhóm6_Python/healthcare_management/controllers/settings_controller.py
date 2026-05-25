import re
import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from importlib import import_module

from config import DB_TYPE


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
    def update_staff_personal_info(user_id, payload):
        if not user_id:
            return False, "Không tìm thấy user_id để cập nhật hồ sơ staff."

        SettingsModel = import_module("models.settings_model").SettingsModel
        db_module = import_module("database.db")
        fetch_one = db_module.fetch_one
        execute = db_module.execute

        name = str(payload.get("name", "")).strip()
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

        patient_row = fetch_one(
            """
            SELECT {top_one} patient_id, name, phone, email
            FROM Patients
            WHERE user_id=?
            ORDER BY patient_id DESC
            {limit_one}
            """.format(
                top_one="" if DB_TYPE == "mysql" else "TOP 1",
                limit_one="LIMIT 1" if DB_TYPE == "mysql" else "",
            ),
            (user_id,),
        )
        if not isinstance(patient_row, dict):
            return False, (
                "Không tìm thấy hồ sơ bệnh nhân liên kết với tài khoản staff. "
                "Chưa thể lưu họ tên/SĐT/email một cách an toàn."
            )

        previous_patient = {
            "name": str(patient_row.get("name") or ""),
            "phone": str(patient_row.get("phone") or ""),
            "email": str(patient_row.get("email") or ""),
        }
        patient_saved = execute(
            "UPDATE Patients SET name=?, phone=?, email=? WHERE patient_id=?",
            (
                name,
                phone,
                email,
                patient_row.get("patient_id"),
            ),
        )
        if not patient_saved:
            return False, "Không thể cập nhật thông tin staff trong hồ sơ bệnh nhân."

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
            # Roll back patient profile update to keep settings/profile consistent.
            execute(
                "UPDATE Patients SET name=?, phone=?, email=? WHERE patient_id=?",
                (
                    previous_patient["name"],
                    previous_patient["phone"],
                    previous_patient["email"],
                    patient_row.get("patient_id"),
                ),
            )
            return False, "Không thể lưu cài đặt cá nhân cho staff."

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
    def update_work_schedule(user_id, schedule_rows):
        SettingsModel = import_module("models.settings_model").SettingsModel
        if not user_id:
            return False, "Không xác định được người dùng hiện tại."
        if not isinstance(schedule_rows, list):
            return False, "Dữ liệu lịch làm việc không hợp lệ."

        normalized_rows = []
        for row in schedule_rows:
            if not isinstance(row, dict):
                return False, "Dữ liệu lịch làm việc không hợp lệ."

            start_value = str(row.get("start") or "-- : --")
            end_value = str(row.get("end") or "-- : --")
            working = bool(row.get("working"))
            if working and (start_value == "-- : --" or end_value == "-- : --"):
                return False, "Vui lòng chọn đầy đủ giờ bắt đầu và kết thúc cho ngày làm việc."

            normalized_rows.append(
                {
                    "day": str(row.get("day") or ""),
                    "start": start_value,
                    "end": end_value,
                    "working": working,
                }
            )

        SettingsModel.get_or_create_by_user_id(user_id)
        saved = SettingsModel.update_fields(user_id, {"work_schedule": json.dumps(normalized_rows, ensure_ascii=False)})
        if not saved:
            return False, "Không thể lưu lịch làm việc."
        return True, "Đã lưu lịch làm việc thành công."

    @staticmethod
    def backup_now(user_id, backup_mode):
        BackupModel = import_module("models.backup_model").BackupModel
        if backup_mode not in {"cloud", "local"}:
            return False, "Chế độ backup không hợp lệ."

        if not user_id:
            return False, "Không xác định được người dùng thực hiện sao lưu."

        BackupModel.ensure_tables_exist()

        SettingsModel = import_module("models.settings_model").SettingsModel
        db_module = import_module("database.db")
        fetch_one = db_module.fetch_one
        user_settings = SettingsModel.get_or_create_by_user_id(user_id)
        if not isinstance(user_settings, dict):
            return False, "Không thể tải cài đặt người dùng."

        user_row = fetch_one(
            "SELECT username, role FROM Users WHERE user_id=?",
            (user_id,),
        ) or {}
        role = str(user_row.get("role") or "staff").lower()

        patient_data = fetch_one(
            """
            SELECT {top_one} patient_id, name, phone, email
            FROM Patients
            WHERE user_id=?
            ORDER BY patient_id DESC
            {limit_one}
            """.format(
                top_one="" if DB_TYPE == "mysql" else "TOP 1",
                limit_one="LIMIT 1" if DB_TYPE == "mysql" else "",
            ),
            (user_id,),
        ) or {}

        doctor_data = fetch_one(
            """
            SELECT {top_one} doctor_id, name, specialty, phone, email
            FROM Doctors
            WHERE user_id=?
            ORDER BY doctor_id DESC
            {limit_one}
            """.format(
                top_one="" if DB_TYPE == "mysql" else "TOP 1",
                limit_one="LIMIT 1" if DB_TYPE == "mysql" else "",
            ),
            (user_id,),
        ) or {}

        if not isinstance(patient_data, dict):
            patient_data = {}
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
            "payload_version": "v1",
            "generated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id,
            "role": role,
            "username": user_row.get("username"),
            "profile_type": "doctor" if role == "doctor" else "patient",
            "profile": {
                "doctor": {
                    "doctor_id": doctor_data.get("doctor_id"),
                    "name": doctor_data.get("name"),
                    "specialty": doctor_data.get("specialty"),
                    "phone": doctor_data.get("phone"),
                    "email": doctor_data.get("email"),
                },
                "patient": {
                    "patient_id": patient_data.get("patient_id"),
                    "name": patient_data.get("name"),
                    "phone": patient_data.get("phone"),
                    "email": patient_data.get("email"),
                },
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

        with local_file.open("rb") as backup_binary:
            checksum = hashlib.sha256(backup_binary.read()).hexdigest()

        backup_id = f"backup_{timestamp}_{user_id}"
        BackupModel.create_backup_record(
            {
                "backup_id": backup_id,
                "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),
                "backup_type": "manual",
                "size_bytes": local_file.stat().st_size,
                "created_by_user_id": user_id,
                "created_by_name": user_row.get("username") or "Admin",
                "status": "success",
                "storage_mode": backup_mode,
                "storage_path": str((cloud_dir / local_file.name) if backup_mode == "cloud" else local_file),
                "checksum": checksum,
                "include_database": True,
                "include_attachments": True,
                "compress_data": True,
            }
        )

        BackupModel.create_job(
            {
                "job_id": f"job_backup_{timestamp}_{user_id}",
                "job_type": "backup",
                "status": "success",
                "progress": 100,
                "message": "Sao lưu hoàn tất",
                "requested_by_user_id": user_id,
                "backup_id": backup_id,
                "started_at": now.strftime("%Y-%m-%d %H:%M:%S"),
                "finished_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

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
        BackupModel = import_module("models.backup_model").BackupModel
        SettingsModel = import_module("models.settings_model").SettingsModel

        if not user_id:
            return False, "Không xác định được người dùng hiện tại để đồng bộ."

        now = datetime.now()
        backups_root = Path(__file__).resolve().parents[1] / "backups"
        local_dir = backups_root / "local"
        cloud_dir = backups_root / "cloud"
        local_dir.mkdir(parents=True, exist_ok=True)
        cloud_dir.mkdir(parents=True, exist_ok=True)

        backup_files = sorted(local_dir.glob(f"settings_user_{user_id}_*.json"), key=lambda path: path.stat().st_mtime)
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

        BackupModel.ensure_tables_exist()

        return True, f"Đã đồng bộ {synced_count} file backup lên thư mục cloud."

    @staticmethod
    def backup_summary():
        BackupModel = import_module("models.backup_model").BackupModel
        return BackupModel.get_summary()

    @staticmethod
    def backup_history(page=1, limit=10):
        BackupModel = import_module("models.backup_model").BackupModel
        return BackupModel.list_backups(page=page, limit=limit)

    @staticmethod
    def update_backup_settings(user_id, payload):
        BackupModel = import_module("models.backup_model").BackupModel
        if not isinstance(payload, dict):
            return False, "Dữ liệu cấu hình sao lưu không hợp lệ."

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
        data = {k: v for k, v in payload.items() if k in allowed}
        if "retention_days" in data:
            retention_days = int(data.get("retention_days") or 0)
            if retention_days <= 0:
                return False, "Số ngày lưu trữ phải lớn hơn 0."
            data["retention_days"] = retention_days
        if "schedule_time" in data:
            schedule_time = str(data.get("schedule_time") or "").strip()
            if not re.match(r"^\d{2}:\d{2}$", schedule_time):
                return False, "Giờ sao lưu không hợp lệ (định dạng HH:MM)."
        if "schedule_frequency" in data:
            if str(data.get("schedule_frequency") or "").lower() not in {"daily", "weekly", "monthly"}:
                return False, "Chu kỳ sao lưu không hợp lệ."

        ok = BackupModel.update_settings(data, updated_by_user_id=user_id)
        if not ok:
            return False, "Không thể cập nhật cấu hình sao lưu."
        return True, "Đã cập nhật cấu hình sao lưu."

    @staticmethod
    def delete_backup_record(backup_id):
        BackupModel = import_module("models.backup_model").BackupModel
        record = BackupModel.get_backup_by_id(backup_id)
        if not isinstance(record, dict):
            return False, "Không tìm thấy bản sao lưu."

        storage_path = Path(str(record.get("storage_path") or ""))
        if storage_path.exists() and storage_path.is_file():
            storage_path.unlink(missing_ok=True)

        ok = BackupModel.mark_deleted(backup_id)
        if not ok:
            return False, "Không thể xóa bản sao lưu khỏi hệ thống."
        return True, "Đã xóa bản sao lưu."

    @staticmethod
    def restore_from_backup(user_id, backup_id, confirm_text="RESTORE", create_backup_before_restore=True):
        BackupModel = import_module("models.backup_model").BackupModel
        SettingsModel = import_module("models.settings_model").SettingsModel
        db_module = import_module("database.db")
        fetch_one = db_module.fetch_one
        execute = db_module.execute

        if confirm_text != "RESTORE":
            return False, "Xác nhận khôi phục không hợp lệ."

        record = BackupModel.get_backup_by_id(backup_id)
        if not isinstance(record, dict):
            return False, "Không tìm thấy bản sao lưu cần khôi phục."

        backup_file = Path(str(record.get("storage_path") or ""))
        if not backup_file.exists() or not backup_file.is_file():
            return False, "Tệp bản sao lưu không tồn tại trên máy chủ."

        try:
            payload = json.loads(backup_file.read_text(encoding="utf-8"))
        except Exception as e:
            import sys, traceback
            print(f"[settings_controller] Error reading backup file '{backup_file}': {e}", file=sys.stderr)
            traceback.print_exc()
            return False, "Không thể đọc dữ liệu bản sao lưu."

        source_user_id = int(payload.get("user_id") or 0)
        if source_user_id != int(user_id or 0):
            return False, "Chỉ được khôi phục bản sao lưu của chính tài khoản hiện tại."

        if create_backup_before_restore:
            SettingsController.backup_now(user_id, "local")

        settings_payload = payload.get("settings") if isinstance(payload, dict) else {}
        if not isinstance(settings_payload, dict):
            settings_payload = {}
        settings_fields = {
            "gender": settings_payload.get("gender"),
            "dob": settings_payload.get("dob"),
            "address": settings_payload.get("address"),
            "avatar_path": settings_payload.get("avatar_path"),
            "notify_new_appointment": bool(settings_payload.get("notify_new_appointment", True)),
            "notify_reminder": bool(settings_payload.get("notify_reminder", True)),
            "notify_system": bool(settings_payload.get("notify_system", True)),
            "theme_mode": settings_payload.get("theme_mode") or "Sáng",
            "font_size": settings_payload.get("font_size") or "Trung bình",
            "display_density": settings_payload.get("display_density") or "Thoải mái",
            "language": settings_payload.get("language") or "Tiếng Việt",
            "backup_mode": settings_payload.get("backup_mode") or "cloud",
        }
        SettingsModel.get_or_create_by_user_id(user_id)
        if not SettingsModel.update_fields(user_id, settings_fields):
            return False, "Không thể khôi phục phần cài đặt người dùng."

        profile = payload.get("profile") if isinstance(payload, dict) else {}
        profile_type = str(payload.get("profile_type") or "patient").lower()
        if profile_type == "doctor":
            doctor_payload = profile.get("doctor") if isinstance(profile, dict) else {}
            if isinstance(doctor_payload, dict) and doctor_payload.get("doctor_id"):
                execute(
                    """
                    UPDATE Doctors
                    SET name=?, specialty=?, phone=?, email=?
                    WHERE doctor_id=?
                    """,
                    (
                        doctor_payload.get("name"),
                        doctor_payload.get("specialty"),
                        doctor_payload.get("phone"),
                        doctor_payload.get("email"),
                        doctor_payload.get("doctor_id"),
                    ),
                )
        else:
            patient_payload = profile.get("patient") if isinstance(profile, dict) else {}
            if isinstance(patient_payload, dict) and patient_payload.get("patient_id"):
                execute(
                    """
                    UPDATE Patients
                    SET name=?, phone=?, email=?
                    WHERE patient_id=?
                    """,
                    (
                        patient_payload.get("name"),
                        patient_payload.get("phone"),
                        patient_payload.get("email"),
                        patient_payload.get("patient_id"),
                    ),
                )

        BackupModel.add_restore_request(
            backup_id=backup_id,
            requested_by_user_id=user_id,
            confirm_text=confirm_text,
            create_backup_before_restore=create_backup_before_restore,
            status="success",
            message="Khôi phục dữ liệu từ bản sao lưu thành công.",
        )
        return True, "Khôi phục dữ liệu thành công."

    @staticmethod
    def ensure_backup_seed_data():
        return False

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
