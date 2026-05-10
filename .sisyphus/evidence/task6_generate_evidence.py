import sys
from pathlib import Path
from unittest.mock import patch

from PyQt6 import QtWidgets

ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = ROOT / "BTL.Nhóm6_Python"
HEALTH_DIR = APP_ROOT / "healthcare_management"
for path in (APP_ROOT, HEALTH_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from views.staff_dashboard_view import StaffDashboardView


def ensure_app():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    return app


def main():
    ensure_app()
    view = StaffDashboardView({"name": "QA"})
    view.show()

    evidence_dir = Path(".sisyphus/evidence")
    evidence_dir.mkdir(parents=True, exist_ok=True)

    # Success path: lookup + save through controller contract
    fake_patient = {
        "patient_id": 999,
        "name": "Nguyen Van A",
        "phone": "0912345678",
        "cccd": "012345678901",
        "address": "1 Le Loi",
        "email": "a@example.com",
        "occupation": "Ky su",
        "intake_notes": "tai kham",
        "gender": "Nam",
        "dob": "1990-01-01",
    }
    fake_appt = {
        "appointment_id": 321,
        "status": "confirmed",
        "doctor_name": "BS Tran",
        "appointment_date": "2026-05-10",
        "note": "Dich vu: Tong quat",
    }

    with patch("BTL.Nhóm6_Python.healthcare_management.views.staff_dashboard_view.PatientController.find_by_cccd_or_phone", side_effect=[fake_patient, fake_patient, fake_patient]), patch(
        "BTL.Nhóm6_Python.healthcare_management.views.staff_dashboard_view.AppointmentController.get_by_patient",
        return_value=[fake_appt],
    ), patch(
        "BTL.Nhóm6_Python.healthcare_management.views.staff_dashboard_view.PatientController.create_with_status",
        return_value={"status": True, "message": "Tạo hồ sơ bệnh nhân thành công."},
    ), patch(
        "BTL.Nhóm6_Python.healthcare_management.views.staff_dashboard_view.PatientController.update_with_status",
        return_value={"status": True, "message": "Cập nhật hồ sơ bệnh nhân thành công."},
    ):
        view.intake_cccd_input.setText("012345678901")
        view.intake_phone_input.setText("0912345678")
        view._handle_intake_lookup()

        view.intake_selected_patient = None
        view.intake_mode_new_radio.setChecked(True)
        view.intake_name_input.setText("Nguyen Van A")
        view.intake_phone_input.setText("0912345678")
        view.intake_phone_profile_input.setText("0912345678")
        view.intake_cccd_profile_input.setText("012345678901")
        view.intake_email_input.setText("a@example.com")
        view.intake_occupation_input.setText("Ky su")
        view.intake_address_input.setText("1 Le Loi")
        view._handle_intake_create_or_update()

        success_report = (
            "Lookup result: " + view.intake_lookup_result_label.text() + "\n"
            "Feedback: " + view.intake_feedback.text() + "\n"
            "Summary patient: " + view.intake_patient_summary.text() + "\n"
        )
        (evidence_dir / "task-6-save-success.txt").write_text(success_report, encoding="utf-8")

    # Validation error screenshot
    view.intake_selected_patient = None
    view.intake_mode_new_radio.setChecked(True)
    view.intake_name_input.setText("Test")
    view.intake_phone_input.setText("123")
    view.intake_phone_profile_input.setText("123")
    view.intake_cccd_profile_input.setText("123")
    view.intake_email_input.setText("invalid-email")
    view.intake_occupation_input.setText("")
    view.intake_address_input.setText("Ha Noi")
    view._handle_intake_create_or_update()
    view.intake_feedback.grab().save(str(evidence_dir / "task-6-validation-error.png"))

    print("Evidence generated")


if __name__ == "__main__":
    main()
