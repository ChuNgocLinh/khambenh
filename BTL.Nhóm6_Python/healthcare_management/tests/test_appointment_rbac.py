from datetime import datetime, timedelta

from healthcare_management.controllers.appointment_controller import AppointmentController


def _future_date_time(days=1):
    dt = datetime.now() + timedelta(days=days)
    return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M")


def test_rbac_allow_and_deny_matrix_examples():
    allowed, _ = AppointmentController.authorize("staff", "list_all")
    assert allowed is True

    denied, message = AppointmentController.authorize("doctor", "list_all")
    assert denied is False
    assert "không có quyền" in message.lower()

    denied_doctor_create, _ = AppointmentController.authorize("doctor", "create")
    assert denied_doctor_create is False

    allowed_patient_create, _ = AppointmentController.authorize("patient", "create")
    assert allowed_patient_create is True


def test_forbidden_action_regression_patient_cannot_start_consultation():
    allowed, message = AppointmentController.authorize("patient", "start_consultation")
    assert allowed is False
    assert "không có quyền" in message.lower()


def test_ownership_deny_patient_mutating_other_patient_appointment():
    appt = {"patient_id": 2, "doctor_id": 1}
    allowed, message = AppointmentController.authorize(
        "patient",
        "cancel",
        user_context={"patient_id": 1},
        appointment=appt,
    )
    assert allowed is False
    assert "chính mình" in message.lower()


def test_ownership_deny_doctor_mutating_not_assigned_appointment():
    appt = {"patient_id": 2, "doctor_id": 5}
    allowed, message = AppointmentController.authorize(
        "doctor",
        "update_time",
        user_context={"doctor_id": 3},
        appointment=appt,
    )
    assert allowed is False
    assert "chính mình" in message.lower()


def test_status_transition_guard_done_to_confirmed_disallowed():
    assert AppointmentController._can_transition("done", "confirmed") is False
    assert AppointmentController._can_transition("cancelled", "pending") is False


def test_update_appointment_denied_by_ownership_before_db_mutation(monkeypatch):
    future_date, future_time = _future_date_time(days=2)

    monkeypatch.setattr(
        "healthcare_management.controllers.appointment_controller.AppointmentModel.get_by_id",
        lambda _id: {
            "appointment_id": _id,
            "patient_id": 999,
            "doctor_id": 10,
            "status": "pending",
        },
    )

    called = {"update": False}

    def _fail_if_called(*_args, **_kwargs):
        called["update"] = True
        return True

    monkeypatch.setattr(
        "healthcare_management.controllers.appointment_controller.AppointmentModel.update_full",
        _fail_if_called,
    )

    monkeypatch.setattr(
        "healthcare_management.controllers.appointment_controller.AppointmentModel.has_conflict",
        lambda *_args, **_kwargs: (False, False),
    )
    result = AppointmentController.update_full(
        appointment_id=100,
        patient_id=2,
        doctor_id=10,
        date_str=future_date,
        time_str=future_time,
        status="cancelled",
        note="deny test",
        service_name="Xét nghiệm",
        role="patient",
        user_context={"patient_id": 1},
    )

    assert result["status"] is False
    message = str(result["message"]) 
    assert "chính mình" in message.lower()
    assert called["update"] is False
