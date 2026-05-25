import pytest
from healthcare_management.controllers.scoping_helper import enforce_patient_scope, enforce_doctor_scope


def test_enforce_patient_scope_success():
    # Admin / Staff / Doctor should always pass
    enforce_patient_scope(2, {"role": "admin"})
    enforce_patient_scope(2, {"role": "staff"})
    enforce_patient_scope(2, {"role": "doctor"})

    # Patient matching their own patient_id should pass
    enforce_patient_scope(2, {"role": "patient", "patient_id": 2})
    enforce_patient_scope("2", {"role": "patient", "patient_id": 2})


def test_enforce_patient_scope_failure():
    # Patient mismatch
    with pytest.raises(PermissionError) as excinfo:
        enforce_patient_scope(3, {"role": "patient", "patient_id": 2})
    assert "truy cập thông tin của bệnh nhân này" in str(excinfo.value)

    # Missing patient_id
    with pytest.raises(PermissionError):
        enforce_patient_scope(3, {"role": "patient"})

    # Invalid role
    with pytest.raises(PermissionError):
        enforce_patient_scope(3, {"role": "hacker"})


def test_enforce_doctor_scope_success():
    # Admin / Staff should always pass
    enforce_doctor_scope(5, {"role": "admin"})
    enforce_doctor_scope(5, {"role": "staff"})

    # Doctor matching their own doctor_id should pass
    enforce_doctor_scope(5, {"role": "doctor", "doctor_id": 5})
    enforce_doctor_scope("5", {"role": "doctor", "doctor_id": 5})


def test_enforce_doctor_scope_failure():
    # Doctor mismatch
    with pytest.raises(PermissionError) as excinfo:
        enforce_doctor_scope(6, {"role": "doctor", "doctor_id": 5})
    assert "thao tác cho bác sĩ này" in str(excinfo.value)

    # Missing doctor_id
    with pytest.raises(PermissionError):
        enforce_doctor_scope(6, {"role": "doctor"})

    # Patient is not allowed doctor actions
    with pytest.raises(PermissionError):
        enforce_doctor_scope(6, {"role": "patient", "patient_id": 1})


def test_patient_controller_scoping(monkeypatch):
    from controllers.patient_controller import PatientController
    
    # Mock models
    class MockPatientModel:
        @staticmethod
        def get_by_id(patient_id):
            return {"patient_id": patient_id, "name": "Test Patient"}

        @staticmethod
        def update(patient_id, *args):
            return True

    class MockMedicalRecordModel:
        @staticmethod
        def get_by_patient(patient_id):
            return [{"record_id": 1, "patient_id": patient_id}]

    monkeypatch.setattr("controllers.patient_controller.PatientModel", MockPatientModel)
    monkeypatch.setattr("models.medical_record_model.MedicalRecordModel", MockMedicalRecordModel)

    # 1. Success cases with matching patient_id
    user_ctx = {"role": "patient", "patient_id": 1}
    patient = PatientController.get_by_id(1, user_context=user_ctx)
    assert patient["patient_id"] == 1

    records = PatientController.get_medical_history(1, user_context=user_ctx)
    assert len(records) == 1
    assert records[0]["patient_id"] == 1

    update_res = PatientController.update_with_status(1, {"name": "New Name"}, user_context=user_ctx)
    assert update_res["status"] is True

    # 2. Failure cases (IDOR prevention) with mismatched patient_id
    user_ctx_bad = {"role": "patient", "patient_id": 2}
    with pytest.raises(PermissionError):
        PatientController.get_by_id(1, user_context=user_ctx_bad)

    with pytest.raises(PermissionError):
        PatientController.get_medical_history(1, user_context=user_ctx_bad)

    with pytest.raises(PermissionError):
        PatientController.update_with_status(1, {"name": "New Name"}, user_context=user_ctx_bad)

