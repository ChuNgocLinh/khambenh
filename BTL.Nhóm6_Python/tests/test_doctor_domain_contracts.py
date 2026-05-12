from healthcare_management.controllers.appointment_controller import AppointmentController
from healthcare_management.controllers.medical_record_controller import MedicalRecordController
from healthcare_management.controllers.notification_controller import NotificationController
from healthcare_management.controllers.prescription_controller import PrescriptionController


def test_exam_draft_and_finalize_contract(monkeypatch):
    stored = {}

    def fake_save(patient_id, doctor_id, appointment_id, diagnosis, treatment, symptoms, conclusion, notes):
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
        return True

    monkeypatch.setattr(
        "healthcare_management.controllers.medical_record_controller.MedicalRecordModel.save_draft",
        fake_save,
    )
    monkeypatch.setattr(
        "healthcare_management.controllers.medical_record_controller.MedicalRecordModel.get_by_appointment",
        lambda appointment_id: stored,
    )
    monkeypatch.setattr(
        "healthcare_management.controllers.medical_record_controller.MedicalRecordModel.finalize",
        lambda record_id, diagnosis, treatment: stored.update(
            {"record_status": "finalized", "diagnosis": diagnosis, "treatment": treatment}
        )
        or True,
    )
    monkeypatch.setattr(
        "healthcare_management.controllers.appointment_controller.AppointmentModel.get_by_id",
        lambda appointment_id: {"appointment_id": appointment_id, "status": "in_progress", "doctor_id": 1, "patient_id": 2},
    )
    monkeypatch.setattr(
        "healthcare_management.controllers.appointment_controller.AppointmentModel.update_status",
        lambda appointment_id, status: stored.update({"appointment_status": status}) or True,
    )

    draft = MedicalRecordController.save_draft(2, 1, 3, "Draft diagnosis", "Draft treatment")
    assert draft["status"] is True
    assert draft["record"]["record_status"] == "draft"

    missing = MedicalRecordController.finalize(7, "", "Treatment", appointment_id=3)
    assert missing["status"] is False

    finalized = MedicalRecordController.finalize(7, "Final diagnosis", "Treatment", appointment_id=3)
    assert finalized["status"] is True
    assert stored["record_status"] == "finalized"
    assert stored["appointment_status"] == "done"


def test_prescription_lifecycle_blocks_dispensed_edit(monkeypatch):
    monkeypatch.setattr(
        "healthcare_management.controllers.prescription_controller.PrescriptionModel.get_by_id",
        lambda prescription_id: {"prescription_id": prescription_id, "record_id": 5, "status": "dispensed"},
    )

    result = PrescriptionController.cancel(12)
    assert result["status"] is False
    assert "da phat" in result["message"].lower()

    assert PrescriptionController.can_edit("draft") is True
    assert PrescriptionController.can_edit("issued") is True
    assert PrescriptionController.can_edit("dispensed") is False
    assert PrescriptionController.can_edit("cancelled") is False


def test_notification_contract_and_target_mapping(monkeypatch):
    calls = {}
    monkeypatch.setattr(
        "healthcare_management.controllers.notification_controller.NotificationModel.create",
        lambda user_id, title, content, type_, target_page, target_id: calls.update(
            {
                "user_id": user_id,
                "title": title,
                "target_page": target_page,
                "target_id": target_id,
            }
        )
        or True,
    )
    monkeypatch.setattr(
        "healthcare_management.controllers.notification_controller.NotificationModel.unread_count",
        lambda user_id: 4,
    )

    assert NotificationController.create(2, "Lịch mới", "Có lịch mới", target_page="schedule", target_id=8)
    assert calls["target_page"] == "schedule"
    assert NotificationController.unread_count(2) == 4
    assert NotificationController.target_index("schedule") == 1
    assert NotificationController.target_index("patient_profile") == 4
    assert NotificationController.target_index("unknown") == 0


def test_appointment_start_exam_transition_contract():
    assert AppointmentController.can_start_exam("pending") is True
    assert AppointmentController.can_start_exam("confirmed") is True
    assert AppointmentController.can_start_exam("in_progress") is True
    assert AppointmentController.can_start_exam("done") is False
    assert AppointmentController.can_start_exam("cancelled") is False
