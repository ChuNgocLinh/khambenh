import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6 import QtWidgets

from views.dashboard_view import DashboardView

_QT_APP = None


def _app():
    global _QT_APP
    _QT_APP = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    return _QT_APP


def _patch_dashboard(monkeypatch, rows, unread):
    monkeypatch.setattr(DashboardView, "_render_dashboard_page", lambda self: None)
    monkeypatch.setattr(DashboardView, "_build_settings_page", lambda self: QtWidgets.QWidget())
    monkeypatch.setattr("views.doctor_schedule_view.AppointmentController.get_management_rows_by_doctor", lambda doctor_id: [])
    monkeypatch.setattr("views.doctor_examination_view.AppointmentController.get_by_doctor", lambda doctor_id: [])
    monkeypatch.setattr("views.doctor_management_views.PatientController.get_by_doctor", lambda doctor_id: [])
    monkeypatch.setattr("controllers.notification_controller.NotificationController.list_for_user", lambda user_id: rows)
    monkeypatch.setattr("controllers.notification_controller.NotificationController.unread_count", lambda user_id: unread[0])


def test_notification_feed_badge_mark_read_and_navigation(monkeypatch):
    _app()
    rows = [
        {
            "notification_id": 1,
            "title": "Lịch mới",
            "content": "Có lịch mới",
            "target_page": "schedule",
            "is_read": False,
        }
    ]
    unread = [1]
    marked = []
    monkeypatch.setattr(
        "controllers.notification_controller.NotificationController.mark_read",
        lambda notification_id, user_id: marked.append((notification_id, user_id)) or unread.__setitem__(0, 0) or True,
    )
    monkeypatch.setattr(
        "controllers.notification_controller.NotificationController.mark_all_read",
        lambda user_id: unread.__setitem__(0, 0) or True,
    )
    _patch_dashboard(monkeypatch, rows, unread)

    view = DashboardView({"doctor_id": 1, "user_id": 2, "name": "Minh", "role": "doctor"})

    assert view.bell_badge.text() == "1"
    assert view.notification_list.count() == 1

    view._open_notification_item(view.notification_list.item(0))
    assert marked == [(1, 2)]
    assert view.content_stack.currentIndex() == 1
    assert view.bell_badge.text() == "0"


def test_notification_empty_and_mark_all(monkeypatch):
    _app()
    unread = [0]
    marked_all = []
    monkeypatch.setattr(
        "controllers.notification_controller.NotificationController.mark_all_read",
        lambda user_id: marked_all.append(user_id) or True,
    )
    monkeypatch.setattr("controllers.notification_controller.NotificationController.mark_read", lambda *_: True)
    _patch_dashboard(monkeypatch, [], unread)

    view = DashboardView({"doctor_id": 1, "user_id": 2, "name": "Minh", "role": "doctor"})
    assert view.notification_list.item(0).text() == "Không có thông báo."

    view.mark_all_notifications_read()
    assert marked_all == [2]
