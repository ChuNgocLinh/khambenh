import os

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
    monkeypatch.setattr("views.doctor_management_views.PatientController.get_all", lambda: [])
    monkeypatch.setattr("controllers.notification_controller.NotificationController.list_for_user", lambda user_id: [])
    monkeypatch.setattr("controllers.notification_controller.NotificationController.unread_count", lambda user_id: 0)

    view = DashboardView({"doctor_id": 1, "user_id": 2, "name": "Minh", "role": "doctor"})

    for index in [0, 1, 2, 3, 4, 5, 6, 7]:
        view.switch_page(index)
        assert view.content_stack.currentIndex() == index

    assert view.content_stack.count() == 8
