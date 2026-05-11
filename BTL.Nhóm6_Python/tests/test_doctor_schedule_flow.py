import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6 import QtCore, QtWidgets

from views.doctor_schedule_view import DoctorScheduleView

_QT_APP = None


def _app():
    global _QT_APP
    _QT_APP = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    return _QT_APP


def _row(status="pending"):
    return {
        "appointment_id": 10,
        "patient_id": 2,
        "doctor_id": 1,
        "appointment_date": "2026-05-11 09:00:00",
        "status": status,
        "note": "Dịch vụ: Khám tổng quát",
        "patient_name": "Nguyen Van A",
        "patient_phone": "0900000000",
        "gender": "Nam",
        "age": 30,
    }


def test_schedule_uses_real_rows_without_mock_fallback(monkeypatch):
    _app()
    monkeypatch.setattr(
        "views.doctor_schedule_view.AppointmentController.get_management_rows_by_doctor",
        lambda doctor_id: [_row()],
    )

    view = DoctorScheduleView(1)
    view.date_input.setDate(QtCore.QDate(2026, 5, 11))

    assert len(view.all_rows) == 1
    assert view.all_rows[0]["appointment_id"] == 10
    assert not any(str(row.get("appointment_id", "")).startswith("100") for row in view.all_rows)
    assert len(view.filtered_rows) == 1


def test_schedule_empty_state_when_no_real_rows(monkeypatch):
    _app()
    monkeypatch.setattr(
        "views.doctor_schedule_view.AppointmentController.get_management_rows_by_doctor",
        lambda doctor_id: [],
    )

    view = DoctorScheduleView(1)
    assert view.all_rows == []
    assert view.filtered_rows == []
    assert "Không có lịch khám" in view.detail_info.text()


def test_schedule_start_and_cancel_update_status(monkeypatch):
    _app()
    calls = []
    monkeypatch.setattr(
        "views.doctor_schedule_view.AppointmentController.get_management_rows_by_doctor",
        lambda doctor_id: [_row()],
    )
    monkeypatch.setattr(
        "views.doctor_schedule_view.AppointmentController.update_status",
        lambda appointment_id, status: calls.append((appointment_id, status)) or True,
    )

    view = DoctorScheduleView(1)
    view.date_input.setDate(QtCore.QDate(2026, 5, 11))
    view._select_schedule(view.filtered_rows[0])
    view._start_selected_exam()
    view._select_schedule(view.filtered_rows[0])
    view._cancel_selected_appointment()

    assert (10, "in_progress") in calls
    assert (10, "cancelled") in calls
