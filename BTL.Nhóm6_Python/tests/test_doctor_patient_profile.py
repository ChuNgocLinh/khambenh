import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6 import QtWidgets

from views.doctor_patient_record_view import DoctorPatientRecordView

_QT_APP = None


def _app():
    global _QT_APP
    _QT_APP = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    return _QT_APP


def test_patient_profile_renders_real_read_model(monkeypatch):
    _app()
    monkeypatch.setattr(
        "views.doctor_patient_record_view.PatientController.get_by_id",
        lambda patient_id: {
            "patient_id": patient_id,
            "name": "Nguyen Van A",
            "gender": "Nam",
            "dob": "1990-01-01",
            "phone": "0901",
            "address": "Ha Noi",
        },
    )
    monkeypatch.setattr(
        "views.doctor_patient_record_view.MedicalRecordController.get_by_patient",
        lambda patient_id: [
            {
                "record_id": 5,
                "created_at": "2026-05-11",
                "diagnosis": "Flu",
                "treatment": "Rest",
                "record_status": "finalized",
            }
        ],
    )
    monkeypatch.setattr(
        "views.doctor_patient_record_view.PrescriptionController.get_by_record",
        lambda record_id: [{"prescription_id": 9, "name": "Paracetamol", "quantity": 10, "status": "issued"}],
    )
    monkeypatch.setattr(
        "views.doctor_patient_record_view.AppointmentController.get_by_patient",
        lambda patient_id: [{"appointment_date": "2026-05-11", "doctor_name": "Dr A", "status": "done", "note": ""}],
    )

    view = DoctorPatientRecordView(1)
    view.set_patient(2)

    assert "Nguyen Van A" in view.summary_label.text()
    assert view.records_table.rowCount() == 1
    assert view.prescriptions_table.rowCount() == 1
    assert view.appointments_table.rowCount() == 1


def test_patient_profile_empty_state(monkeypatch):
    _app()
    monkeypatch.setattr("views.doctor_patient_record_view.PatientController.get_by_id", lambda patient_id: None)
    monkeypatch.setattr("views.doctor_patient_record_view.MedicalRecordController.get_by_patient", lambda patient_id: [])
    monkeypatch.setattr("views.doctor_patient_record_view.AppointmentController.get_by_patient", lambda patient_id: [])

    view = DoctorPatientRecordView(1)
    view.set_patient(999)

    assert "Không tìm thấy" in view.summary_label.text()
    assert view.records_table.rowCount() == 0
