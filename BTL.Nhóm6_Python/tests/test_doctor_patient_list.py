import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6 import QtWidgets

from views.doctor_management_views import DoctorPatientListView

_QT_APP = None


def _app():
    global _QT_APP
    _QT_APP = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    return _QT_APP


def _patients():
    return [
        {
            "patient_id": 1,
            "name": "Nguyen Van A",
            "gender": "Nam",
            "dob": "1990-01-01",
            "phone": "0901",
            "appointment_count": 1,
            "record_count": 0,
        },
        {
            "patient_id": 2,
            "name": "Tran Thi B",
            "gender": "Nu",
            "dob": "1992-02-02",
            "phone": "0902",
            "appointment_count": 2,
            "record_count": 1,
            "last_visit": "2026-05-01 09:00:00",
        },
        {
            "patient_id": 3,
            "name": "Le Van C",
            "gender": "Male",
            "dob": "1993-03-03",
            "phone": "0903",
            "appointment_count": 1,
            "record_count": 1,
            "draft_record_count": 1,
        },
    ]


def test_patient_list_search_filter_and_empty_state(monkeypatch):
    _app()
    captured = {}
    monkeypatch.setattr(
        "views.doctor_management_views.PatientController.get_by_doctor",
        lambda doctor_id: captured.setdefault("doctor_id", doctor_id) and _patients(),
    )

    view = DoctorPatientListView(1)
    assert captured["doctor_id"] == 1
    assert len(view.all_rows) == 3
    assert view.table.rowCount() == 3

    view.search_input.setText("0902")
    assert len(view.filtered_rows) == 1
    assert view.filtered_rows[0]["patient_id"] == 2

    view.search_input.setText("")
    view.gender_filter.setCurrentText("Nam")
    assert {row["patient_id"] for row in view.filtered_rows} == {1, 3}

    view.search_input.setText("missing")
    assert view.filtered_rows == []
    assert "Không có bệnh nhân" in view.status_label.text()


def test_patient_list_pagination_and_profile_selection(monkeypatch):
    _app()
    rows = [
        {
            "patient_id": idx,
            "name": f"Patient {idx}",
            "gender": "Nam",
            "dob": "1990-01-01",
            "phone": f"09{idx:02d}",
            "appointment_count": 1,
            "record_count": 0,
        }
        for idx in range(1, 13)
    ]
    monkeypatch.setattr("views.doctor_management_views.PatientController.get_by_doctor", lambda doctor_id: rows)

    view = DoctorPatientListView(1)
    assert view.page_label.text() == "1/2"
    assert view.table.rowCount() == 10

    view._go_page(2)
    assert view.page_label.text() == "2/2"
    assert view.table.rowCount() == 2

    view.open_patient_profile(0)
    assert view.selected_patient_id == 11


def test_patient_list_status_uses_real_visit_fields(monkeypatch):
    _app()
    rows = [
        {"patient_id": 1, "name": "New", "appointment_count": 1, "record_count": 0},
        {"patient_id": 2, "name": "Active", "active_appointment_count": 1, "appointment_count": 3},
        {"patient_id": 3, "name": "Follow", "next_visit": "2026-06-01 08:00:00", "appointment_count": 2},
        {"patient_id": 4, "name": "Recent", "last_visit": "2026-05-01 08:00:00", "appointment_count": 2, "record_count": 1},
    ]
    monkeypatch.setattr("views.doctor_management_views.PatientController.get_by_doctor", lambda doctor_id: rows)

    view = DoctorPatientListView(7)

    assert [row["status_key"] for row in view.all_rows] == ["new", "active", "follow_up", "recent"]
    assert view.all_rows[3]["last_visit"] == "01/05/2026"
