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
