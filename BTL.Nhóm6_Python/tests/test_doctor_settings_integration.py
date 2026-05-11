from controllers.settings_controller import SettingsController


def test_settings_validation_and_notification_preference(monkeypatch):
    updated = {}

    class FakeDoctorModel:
        @staticmethod
        def get_by_id(doctor_id):
            return {"name": "Old", "specialty": "Old", "phone": "0900000000", "email": "old@example.com"}

        @staticmethod
        def update_profile_details(**kwargs):
            updated["doctor"] = kwargs
            return True

    class FakeSettingsModel:
        @staticmethod
        def get_or_create_by_user_id(user_id):
            updated["settings_user"] = user_id
            return {"user_id": user_id}

        @staticmethod
        def update_fields(user_id, fields):
            updated.setdefault("fields", {}).update(fields)
            return True

    def fake_import(name):
        if name == "models.doctor_model":
            return type("Module", (), {"DoctorModel": FakeDoctorModel})
        if name == "models.settings_model":
            return type("Module", (), {"SettingsModel": FakeSettingsModel})
        raise AssertionError(name)

    monkeypatch.setattr("controllers.settings_controller.import_module", fake_import)

    ok, message = SettingsController.update_personal_info(
        1,
        2,
        {
            "name": "Bác sĩ Minh",
            "email": "minh@example.com",
            "phone": "0900000000",
            "specialty": "Nội khoa",
            "gender": "Nam",
            "dob": "1990-01-01",
            "address": "Ha Noi",
        },
    )

    assert ok is True
    assert updated["doctor"]["name"] == "Minh"
    assert updated["fields"]["address"] == "Ha Noi"

    bad, _ = SettingsController.update_personal_info(1, 2, {"name": "", "email": "bad"})
    assert bad is False

    assert SettingsController.update_notification(2, "notify_system", False) is True
    assert updated["fields"]["notify_system"] is False


def test_change_password_validation(monkeypatch):
    class FakeUserModel:
        @staticmethod
        def change_password(user_id, current_password, new_password):
            return current_password == "old-password"

    monkeypatch.setattr(
        "controllers.settings_controller.import_module",
        lambda name: type("Module", (), {"UserModel": FakeUserModel}),
    )

    ok, _ = SettingsController.change_password(2, "old-password", "new-password", "new-password")
    assert ok is True

    mismatch, message = SettingsController.change_password(2, "old-password", "new-password", "other-password")
    assert mismatch is False
    assert "kh" in message.lower()
