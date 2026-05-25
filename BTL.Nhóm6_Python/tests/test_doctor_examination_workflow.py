import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6 import QtWidgets

from views.doctor_examination_view import DoctorExaminationView

_QT_APP = None


def _app():
    global _QT_APP
    _QT_APP = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    return _QT_APP


def test_examination_save_draft_and_finalize(monkeypatch):
    _app()
    stored = {}

    monkeypatch.setattr(
        "views.doctor_examination_view.AppointmentController.get_by_doctor",
        lambda doctor_id: [
            {
                "appointment_id": 3,
                "patient_id": 2,
                "doctor_id": doctor_id,
                "appointment_date": "2026-05-11 09:00:00",
                "status": "in_progress",
                "patient_name": "Nguyen Van A",
            }
        ],
    )
    monkeypatch.setattr(
        "views.doctor_examination_view.MedicalRecordController.get_by_appointment",
        lambda appointment_id: stored or None,
    )

    def save_draft(patient_id, doctor_id, appointment_id, diagnosis, treatment, symptoms="", conclusion="", notes=""):
        stored.update(
            {
                "record_id": 7,
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "appointment_id": appointment_id,
                "diagnosis": diagnosis,
                "treatment": treatment,
                "record_status": "draft",
            }
        )
        return {"status": True, "message": "saved", "record": stored}

    monkeypatch.setattr("views.doctor_examination_view.MedicalRecordController.save_draft", save_draft)
    monkeypatch.setattr(
        "views.doctor_examination_view.MedicalRecordController.finalize",
        lambda record_id, diagnosis, treatment, appointment_id=None: stored.update(
            {"record_status": "finalized", "diagnosis": diagnosis, "treatment": treatment}
        )
        or {"status": True, "message": "finalized"},
    )

    view = DoctorExaminationView(1)
    view.diagnosis_input.setPlainText("Final diagnosis")
    view.treatment_input.setPlainText("Treatment")

    draft = view.save_draft()
    finalized = view.finalize_exam()

    assert draft["status"] is True
    assert finalized["status"] is True
    assert stored["record_status"] == "finalized"


def test_examination_finalize_validation_message(monkeypatch):
    _app()
    monkeypatch.setattr("views.doctor_examination_view.AppointmentController.get_by_doctor", lambda doctor_id: [])

    view = DoctorExaminationView(1)
    result = view.finalize_exam()

    assert result["status"] is False
    assert "Không có" in result["message"]


def test_examination_cancel_action_returns_to_schedule(monkeypatch):
    _app()

    appointment_rows = [
        {
            "appointment_id": 5,
            "patient_id": 3,
            "doctor_id": 1,
            "appointment_date": "2026-05-11 09:00:00",
            "status": "in_progress",
            "patient_name": "Tran Thi B",
        }
    ]

    class Host(QtWidgets.QWidget):
        def __init__(self):
            super().__init__()
            self.switched_page = None

        def switch_page(self, index):
            self.switched_page = index

    monkeypatch.setattr(
        "views.doctor_examination_view.AppointmentController.get_by_doctor",
        lambda doctor_id: appointment_rows,
    )
    monkeypatch.setattr(
        "views.doctor_examination_view.MedicalRecordController.get_by_appointment",
        lambda appointment_id: None,
    )

    host = Host()
    view = DoctorExaminationView(1, parent=host)
    view.diagnosis_input.setPlainText("Draft data")
    view.treatment_input.setPlainText("More draft data")
    result = view.cancel_exam()

    assert result["status"] is True
    assert host.switched_page == 1
    assert "hủy" in result["message"].lower()
    assert view.diagnosis_input.toPlainText() == ""
    assert view.treatment_input.toPlainText() == ""


def test_vitals_validation(monkeypatch):
    _app()
    from views.doctor_examination_view import DoctorExaminationView

    monkeypatch.setattr(
        "views.doctor_examination_view.AppointmentController.get_by_doctor",
        lambda doctor_id: [{
            "appointment_id": 5,
            "patient_id": 3,
            "doctor_id": 1,
            "appointment_date": "2026-05-11 09:00:00",
            "status": "in_progress",
            "patient_name": "Tran Thi B",
        }],
    )
    monkeypatch.setattr(
        "views.doctor_examination_view.MedicalRecordController.get_by_appointment",
        lambda appointment_id: None,
    )

    view = DoctorExaminationView(1)
    view.current_appointment = {
        "appointment_id": 5,
        "patient_id": 3,
        "doctor_id": 1,
    }

    # 1. Invalid pulse
    view.pulse_input.setText("invalid_pulse")
    ok, err = view.validate_vitals()
    assert ok is False
    assert "Mạch" in err

    # 2. Invalid blood pressure
    view.pulse_input.setText("80")
    view.bp_input.setText("120") # Missing slash
    ok, err = view.validate_vitals()
    assert ok is False
    assert "Huyết áp" in err

    # 3. Invalid temperature
    view.bp_input.setText("120/80")
    view.temp_input.setText("50.0") # Too high
    ok, err = view.validate_vitals()
    assert ok is False
    assert "Nhiệt độ" in err

    # 4. Valid values
    view.temp_input.setText("37.2")
    ok, err = view.validate_vitals()
    assert ok is True

