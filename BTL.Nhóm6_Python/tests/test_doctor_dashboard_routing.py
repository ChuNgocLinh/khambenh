import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6 import QtWidgets

from views.dashboard_view import DashboardView
from views.doctor_examination_view import DoctorExaminationView
from views.doctor_management_views import DoctorPatientListView, PrescriptionView
from views.doctor_patient_record_view import DoctorPatientRecordView
from views.doctor_schedule_view import DoctorScheduleView
from views.main_view import MainView

_QT_APP = None


def _app():
    global _QT_APP
    _QT_APP = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    return _QT_APP


def _patch_dashboard_dependencies(monkeypatch):
    monkeypatch.setattr(DashboardView, "_render_dashboard_page", lambda self: None)
    monkeypatch.setattr(DashboardView, "_build_notification_center_page", lambda self, notifications: QtWidgets.QWidget())
    monkeypatch.setattr(DashboardView, "_build_settings_page", lambda self: QtWidgets.QWidget())
    monkeypatch.setattr(
        "views.doctor_schedule_view.AppointmentController.get_management_rows_by_doctor",
        lambda doctor_id: [],
    )
    monkeypatch.setattr(
        "views.doctor_examination_view.AppointmentController.get_by_doctor",
        lambda doctor_id: [],
    )
    monkeypatch.setattr(
        "views.doctor_management_views.PatientController.get_all",
        lambda: [],
    )
    monkeypatch.setattr(
        "controllers.notification_controller.NotificationController.list_for_user",
        lambda user_id: [],
    )
    monkeypatch.setattr(
        "controllers.notification_controller.NotificationController.unread_count",
        lambda user_id: 0,
    )


def test_doctor_router_mounts_expected_runtime_widgets(monkeypatch):
    _app()
    _patch_dashboard_dependencies(monkeypatch)

    dashboard = DashboardView({"doctor_id": 1, "user_id": 2, "name": "Minh", "role": "doctor"})

    assert dashboard.content_stack.count() == 8
    assert dashboard.content_stack.widget(0) is dashboard.page_dashboard
    assert isinstance(dashboard.content_stack.widget(1), DoctorScheduleView)
    assert isinstance(dashboard.content_stack.widget(2), DoctorPatientListView)
    assert isinstance(dashboard.content_stack.widget(3), DoctorExaminationView)
    assert isinstance(dashboard.content_stack.widget(4), DoctorPatientRecordView)
    assert isinstance(dashboard.content_stack.widget(5), PrescriptionView)

    for index in range(8):
        dashboard.switch_page(index)
        assert dashboard.content_stack.currentIndex() == index


def test_main_view_routes_only_doctor_role_to_doctor_dashboard(monkeypatch):
    _app()
    _patch_dashboard_dependencies(monkeypatch)

    doctor_main = MainView("doctor", {"doctor_id": 1, "user_id": 2, "name": "Minh"})
    assert hasattr(doctor_main, "doctor_dashboard")
    assert isinstance(doctor_main.doctor_dashboard, DashboardView)

    unknown_main = MainView("unsupported", {"user_id": 3, "name": "Other"})
    assert not hasattr(unknown_main, "doctor_dashboard")
