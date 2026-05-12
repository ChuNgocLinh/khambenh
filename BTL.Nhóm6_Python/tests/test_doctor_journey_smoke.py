import os
import json

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6 import QtWidgets

from views.dashboard_view import DashboardView

_QT_APP = None


def _app():
    global _QT_APP
    _QT_APP = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    return _QT_APP


def test_doctor_journey_smoke_switches_all_mounted_pages(monkeypatch):
    _app()
    monkeypatch.setattr(DashboardView, "_render_dashboard_page", lambda self: None)
    monkeypatch.setattr(DashboardView, "_build_settings_page", lambda self: QtWidgets.QWidget())
    monkeypatch.setattr("views.doctor_schedule_view.AppointmentController.get_management_rows_by_doctor", lambda doctor_id: [])
    monkeypatch.setattr("views.doctor_examination_view.AppointmentController.get_by_doctor", lambda doctor_id: [])
    monkeypatch.setattr("views.doctor_management_views.PatientController.get_by_doctor", lambda doctor_id: [])
    monkeypatch.setattr("controllers.notification_controller.NotificationController.list_for_user", lambda user_id: [])
    monkeypatch.setattr("controllers.notification_controller.NotificationController.unread_count", lambda user_id: 0)

    view = DashboardView({"doctor_id": 1, "user_id": 2, "name": "Minh", "role": "doctor"})

    for index in [0, 1, 2, 3, 4, 5, 6, 7]:
        view.switch_page(index)
        assert view.content_stack.currentIndex() == index

    assert view.content_stack.count() == 8


def test_dashboard_quick_actions_navigate_to_runtime_pages(monkeypatch):
    _app()
    monkeypatch.setattr("views.doctor_schedule_view.AppointmentController.get_management_rows_by_doctor", lambda doctor_id: [])
    monkeypatch.setattr("views.doctor_examination_view.AppointmentController.get_by_doctor", lambda doctor_id: [])
    monkeypatch.setattr("views.doctor_management_views.PatientController.get_by_doctor", lambda doctor_id: [])
    monkeypatch.setattr("controllers.notification_controller.NotificationController.list_for_user", lambda user_id: [])
    monkeypatch.setattr("controllers.notification_controller.NotificationController.unread_count", lambda user_id: 0)

    view = DashboardView({"doctor_id": 1, "user_id": 2, "name": "Minh", "role": "doctor"})

    target_button = None
    for button in view.findChildren(QtWidgets.QPushButton):
        if button.text() == "Xem tất cả lịch hẹn >":
            target_button = button
            break

    assert target_button is not None
    target_button.click()
    assert view.content_stack.currentIndex() == 1


def test_settings_schedule_load_toggle_and_reset(monkeypatch):
    _app()
    monkeypatch.setattr("views.doctor_schedule_view.AppointmentController.get_management_rows_by_doctor", lambda doctor_id: [])
    monkeypatch.setattr("views.doctor_examination_view.AppointmentController.get_by_doctor", lambda doctor_id: [])
    monkeypatch.setattr("views.doctor_management_views.PatientController.get_by_doctor", lambda doctor_id: [])
    monkeypatch.setattr("controllers.notification_controller.NotificationController.list_for_user", lambda user_id: [])
    monkeypatch.setattr("controllers.notification_controller.NotificationController.unread_count", lambda user_id: 0)
    monkeypatch.setattr(
        "models.doctor_model.DoctorModel.get_by_id",
        lambda doctor_id: {"name": "Bác sĩ Minh", "specialty": "Nội khoa", "phone": "0900000000", "email": "minh@example.com"},
    )
    monkeypatch.setattr(
        "controllers.settings_controller.SettingsController.get_settings",
        lambda user_id: {
            "gender": "Nam",
            "address": "Ha Noi",
            "language": "Tiếng Việt",
            "backup_mode": "cloud",
            "work_schedule": json.dumps(
                [
                    {"day": "day_0", "start": "-- : --", "end": "-- : --", "working": False},
                    {"day": "day_1", "start": "07:30", "end": "17:00", "working": True},
                ]
            ),
        },
    )

    info_messages = []
    monkeypatch.setattr(
        "PyQt6.QtWidgets.QMessageBox.information",
        lambda *args: info_messages.append(args[2]) or 0,
    )

    view = DashboardView({"doctor_id": 1, "user_id": 2, "name": "Minh", "role": "doctor"})

    first_checkbox = view._settings_schedule_checkboxes[0]
    first_start = view._settings_schedule_start_inputs[0]
    first_end = view._settings_schedule_end_inputs[0]
    second_start = view._settings_schedule_start_inputs[1]

    assert first_checkbox.isChecked() is False
    assert first_start.isEnabled() is False
    assert first_end.isEnabled() is False
    assert second_start.isEnabled() is True

    first_checkbox.setChecked(True)
    assert first_start.isEnabled() is True
    assert first_end.isEnabled() is True

    first_start.setCurrentText("07:30")
    first_end.setCurrentText("17:00")
    view._reset_settings_view()

    assert first_checkbox.isChecked() is False
    assert first_start.isEnabled() is False
    assert first_end.isEnabled() is False
    assert any("đã lưu gần nhất" in message.lower() for message in info_messages)
