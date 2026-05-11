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
        {"patient_id": 1, "name": "Nguyen Van A", "gender": "Nam", "dob": "1990-01-01", "phone": "0901"},
        {"patient_id": 2, "name": "Tran Thi B", "gender": "Nữ", "dob": "1992-02-02", "phone": "0902"},
        {"patient_id": 3, "name": "Le Van C", "gender": "Nam", "dob": "1993-03-03", "phone": "0903"},
    ]


def test_patient_list_search_filter_and_empty_state(monkeypatch):
    _app()
    monkeypatch.setattr("views.doctor_management_views.PatientController.get_all", lambda: _patients())

    view = DoctorPatientListView(1)
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
        {"patient_id": idx, "name": f"Patient {idx}", "gender": "Nam", "dob": "1990-01-01", "phone": f"09{idx:02d}"}
        for idx in range(1, 13)
    ]
    monkeypatch.setattr("views.doctor_management_views.PatientController.get_all", lambda: rows)

    view = DoctorPatientListView(1)
    assert view.page_label.text() == "1/2"
    assert view.table.rowCount() == 10

    view._go_page(2)
    assert view.page_label.text() == "2/2"
    assert view.table.rowCount() == 2

    view.open_patient_profile(0)
    assert view.selected_patient_id == 11
