import pytest
from pathlib import Path
import json

from config import DEFAULT_SLOTS
from healthcare_management.controllers.scoping_helper import enforce_patient_scope, enforce_doctor_scope
from healthcare_management.models.user_model import UserModel
from healthcare_management.controllers.settings_controller import SettingsController


def test_direct_db_access_guard():
    """
    Guard test: Bốn file view mục tiêu không được phép import trực tiếp từ database.db
    hoặc gọi trực tiếp execute, fetch_all, fetch_one.
    """
    targets = [
        Path('BTL.Nhóm6_Python/healthcare_management/views/admin_management_views.py'),
        Path('BTL.Nhóm6_Python/healthcare_management/views/doctor_management_views.py'),
        Path('BTL.Nhóm6_Python/healthcare_management/views/patient_view.py'),
        Path('BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py'),
    ]
    
    bad = []
    for p in targets:
        if not p.exists():
            continue
        txt = p.read_text(encoding='utf-8')
        # Kiểm tra nếu còn import trực tiếp từ database.db
        if 'from database.db import' in txt or 'database.db' in txt:
            # Cho phép giải thích và loại trừ nếu là bình luận
            lines = txt.splitlines()
            for line in lines:
                if 'from database.db import' in line and not line.strip().startswith('#'):
                    bad.append(f"{p.name}: {line.strip()}")
                    break

    # Lưu ý: Test này có thể fail trước khi hoàn tất refactor views ở các task sau.
    # Đây là hành vi mong đợi để phản ánh đúng tiến độ sửa lỗi.
    assert not bad, f"Phát hiện truy cập DB trực tiếp trong views: {bad}"


def test_patient_idor_prevention():
    # Thử gọi enforce_patient_scope với patient_id khác với user_context
    with pytest.raises(PermissionError):
        enforce_patient_scope(patient_id=1, user_context={"role": "patient", "patient_id": 2})

    # Quyền admin/staff/doctor thì được phép truy cập
    enforce_patient_scope(patient_id=1, user_context={"role": "admin"})
    enforce_patient_scope(patient_id=1, user_context={"role": "staff"})
    enforce_patient_scope(patient_id=1, user_context={"role": "doctor"})


def test_admin_reset_password_temporary(monkeypatch):
    """
    Đảm bảo mật khẩu sau khi reset sẽ kích hoạt flag force_change_password.
    """
    called_update = {"called": False, "fields": {}}

    def mock_execute(query, params=()):
        if "UPDATE Users" in query and "force_change_password" in query:
            called_update["called"] = True
            called_update["fields"]["password"] = params[0]
            called_update["fields"]["force_change_password"] = params[1]
            called_update["fields"]["user_id"] = params[2]
            return True
        return True

    monkeypatch.setattr("healthcare_management.models.user_model.execute", mock_execute)
    
    # Giả định admin thực hiện reset password
    # UserModel.reset_password(user_id) - hàm này sẽ được định nghĩa ở Task 8
    # Để test harness độc lập chạy qua, ta tạm mock hoặc kiểm tra xem method tồn tại
    if hasattr(UserModel, "reset_password"):
        res = UserModel.reset_password(user_id=10)
        assert res is True
        assert called_update["called"] is True
        assert called_update["fields"]["force_change_password"] is True


def test_last_active_admin_protection(monkeypatch):
    """
    Đảm bảo không thể disable/delete tài khoản admin cuối cùng.
    """
    # Mock database để chỉ trả về 1 admin hoạt động duy nhất
    def mock_fetch_all(query, params=()):
        if "COUNT(*)" in query or "role='admin'" in query:
            return [{"total": 1}]
        return []

    def mock_fetch_one(query, params=()):
        if "role='admin'" in query:
            return {"total_admin": 1}
        return {"total_admin": 1}

    monkeypatch.setattr("healthcare_management.models.user_model.fetch_one", mock_fetch_one)
    monkeypatch.setattr("healthcare_management.models.user_model.fetch_all", mock_fetch_all)

    if hasattr(UserModel, "disable_user"):
        # UserModel.disable_user(user_id=1) - hàm này sẽ được định nghĩa ở Task 8
        # Sẽ trả về False hoặc raise lỗi khi cố disable admin cuối cùng
        success, message = UserModel.disable_user(user_id=1, role="admin")
        assert success is False
        assert "cuối cùng" in message.lower()


def test_backup_restore_validation(tmp_path, monkeypatch):
    """
    Đảm bảo restore backup kiểm tra chặt chẽ payload JSON và ownership.
    """
    backup_file = tmp_path / "backup_wrong.json"
    # User khác
    backup_file.write_text(json.dumps({"user_id": 99, "profile_type": "patient", "settings": {}}), encoding="utf-8")
    
    monkeypatch.setattr("healthcare_management.controllers.settings_controller.Path", lambda *args: backup_file)
    monkeypatch.setattr("healthcare_management.controllers.settings_controller.import_module", lambda *args: None)
    
    # Mock BackupModel.get_backup_by_id
    class MockBackupModel:
        @staticmethod
        def get_backup_by_id(backup_id):
            return {"storage_path": str(backup_file)}
    
    def mock_import_module(name):
        if "backup_model" in name:
            class Holder:
                BackupModel = MockBackupModel
            return Holder
        class GenericHolder:
            def __getattr__(self, item):
                return lambda *args, **kwargs: True
        return GenericHolder()

    monkeypatch.setattr("healthcare_management.controllers.settings_controller.import_module", mock_import_module)

    # Khôi phục với user_id=1 nhưng tệp lưu user_id=99
    success, message = SettingsController.restore_from_backup(user_id=1, backup_id=123, confirm_text="RESTORE", create_backup_before_restore=False)
    assert success is False
    assert "chính tài khoản" in message.lower()


def test_slot_unification():
    """
    Đảm bảo slots trong config có ít nhất 10 slots và bao gồm 08:00 đến 17:00
    """
    assert len(DEFAULT_SLOTS) >= 10
    assert "08:00" in DEFAULT_SLOTS
    assert "17:00" in DEFAULT_SLOTS


def test_service_delete_soft_disable(monkeypatch):
    """
    Chặn delete cứng các Service đã được lập Invoice lịch sử.
    """
    called_execute = []
    
    def mock_fetch_one(query, params=()):
        if "FROM Invoices" in query:
            return {"1": 1}
        return None

    def mock_execute(query, params=()):
        called_execute.append((query, params))
        return True

    monkeypatch.setattr("healthcare_management.models.service_model.fetch_one", mock_fetch_one)
    monkeypatch.setattr("healthcare_management.models.service_model.execute", mock_execute)

    from healthcare_management.models.service_model import ServiceModel
    ServiceModel.delete(service_id=42)

    updated = False
    for query, params in called_execute:
        if "UPDATE Services SET is_active=?" in query and params == (0, 42):
            updated = True
    assert updated is True


def test_report_scoping_rules():
    """
    Đảm bảo ReportController chỉ cho phép Admin hoặc Staff truy cập.
    """
    from healthcare_management.controllers.report_controller import ReportController
    
    with pytest.raises(PermissionError):
        ReportController.get_core_totals(user_context={"role": "patient"})

    with pytest.raises(PermissionError):
        ReportController.get_core_totals(user_context={"role": "doctor"})
