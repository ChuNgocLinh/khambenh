from datetime import datetime, timedelta

from healthcare_management.controllers.appointment_controller import AppointmentController


def _future_date_time(days=1):
    dt = datetime.now() + timedelta(days=days)
    return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M")


def test_rbac_allow_and_deny_for_all_roles():
    allowed_admin, _ = AppointmentController.authorize("admin", "list_all")
    assert allowed_admin is True

    allowed_staff, _ = AppointmentController.authorize("staff", "list_all")
    assert allowed_staff is True

    denied_doctor, message_doctor = AppointmentController.authorize("doctor", "list_all")
    assert denied_doctor is False
    assert "không có quyền" in message_doctor.lower()

    denied_patient, message_patient = AppointmentController.authorize("patient", "list_all")
    assert denied_patient is False
    assert "không có quyền" in message_patient.lower()


def test_forbidden_action_regression_patient_cannot_start_consultation():
    allowed, message = AppointmentController.authorize("patient", "start_consultation")
    assert allowed is False
    assert "không có quyền" in message.lower()


def test_ownership_deny_patient_mutating_other_patient_appointment():
    appointment = {"patient_id": 2, "doctor_id": 1}
    allowed, message = AppointmentController.authorize(
        "patient",
        "cancel",
        user_context={"patient_id": 1},
        appointment=appointment,
    )
    assert allowed is False
    assert "chính mình" in message.lower()


def test_ownership_deny_doctor_mutating_not_assigned_appointment():
    appointment = {"patient_id": 10, "doctor_id": 7}
    allowed, message = AppointmentController.authorize(
        "doctor",
        "update_time",
        user_context={"doctor_id": 3},
        appointment=appointment,
    )
    assert allowed is False
    assert "chính mình" in message.lower()


def test_status_transition_regression_blocks_invalid_flow():
    assert AppointmentController._can_transition("done", "confirmed") is False
    assert AppointmentController._can_transition("cancelled", "pending") is False


def test_update_appointment_denied_by_ownership_before_db_mutation(monkeypatch):
    future_date, future_time = _future_date_time(days=2)

    monkeypatch.setattr(
        "healthcare_management.controllers.appointment_controller.AppointmentModel.get_by_id",
        lambda appointment_id: {
            "appointment_id": appointment_id,
            "patient_id": 99,
            "doctor_id": 10,
            "status": "pending",
        },
    )

    called = {"updated": False}

    def _mark_update_called(*_args, **_kwargs):
        called["updated"] = True
        return True

    monkeypatch.setattr(
        "healthcare_management.controllers.appointment_controller.AppointmentModel.update_appointment",
        _mark_update_called,
    )

    result = AppointmentController.update_appointment(
        appointment_id=101,
        date=future_date,
        time=future_time,
        doctor_id=10,
        status="pending",
        role="patient",
        user_context={"patient_id": 1},
    )

    assert result["status"] is False
    assert "chính mình" in result["message"].lower()
    assert called["updated"] is False
