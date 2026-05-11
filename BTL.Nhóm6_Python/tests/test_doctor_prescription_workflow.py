import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6 import QtWidgets

from views.doctor_management_views import PrescriptionView

_QT_APP = None


def _app():
    global _QT_APP
    _QT_APP = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    return _QT_APP


def _rows():
    return [
        {
            "prescription_id": 1,
            "patient_name": "Nguyen Van A",
            "prescribed_at": "2026-05-11",
            "diagnosis": "Flu",
            "medicine_name": "Paracetamol",
            "quantity": 10,
            "status": "issued",
        },
        {
            "prescription_id": 2,
            "patient_name": "Tran Thi B",
            "prescribed_at": "2026-05-10",
            "diagnosis": "Cough",
            "medicine_name": "Amoxicillin",
            "quantity": 5,
            "status": "dispensed",
        },
    ]


def test_prescription_list_search_filter_and_cancel(monkeypatch):
    _app()
    cancelled = []
    monkeypatch.setattr("views.doctor_management_views.PrescriptionController.get_by_doctor", lambda doctor_id: _rows())
    monkeypatch.setattr("views.doctor_management_views.PrescriptionController.can_edit", lambda status: status != "dispensed")
    monkeypatch.setattr(
        "views.doctor_management_views.PrescriptionController.cancel",
        lambda prescription_id: cancelled.append(prescription_id) or {"status": True, "message": "cancelled"},
    )

    view = PrescriptionView(1)
    assert len(view.all_rows) == 2
    assert view.table.rowCount() == 2

    view.search_input.setText("para")
    assert len(view.filtered_rows) == 1
    assert view.filtered_rows[0]["prescription_id"] == 1

    result = view.cancel_prescription(view.filtered_rows[0])
    assert result["status"] is True
    assert cancelled == [1]


def test_prescription_blocks_dispensed_edit(monkeypatch):
    _app()
    monkeypatch.setattr("views.doctor_management_views.PrescriptionController.get_by_doctor", lambda doctor_id: _rows())
    monkeypatch.setattr("views.doctor_management_views.PrescriptionController.can_edit", lambda status: status != "dispensed")

    view = PrescriptionView(1)
    dispensed = view.all_rows[1]
    result = view.edit_prescription(dispensed)

    assert result["status"] is False
    assert "đã phát" in result["message"]
