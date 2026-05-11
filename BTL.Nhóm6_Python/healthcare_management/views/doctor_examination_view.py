from PyQt6 import QtWidgets

from controllers.appointment_controller import AppointmentController
from controllers.medical_record_controller import MedicalRecordController


class DoctorExaminationView(QtWidgets.QWidget):
    def __init__(self, doctor_id, parent=None):
        super().__init__(parent)
        self.doctor_id = doctor_id
        self.role = "doctor"
        self.current_appointment = None
        self.current_record = None
        self.setStyleSheet("background: #f8fbff; border: none;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        title = QtWidgets.QLabel("Khám bệnh")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0f172a;")
        layout.addWidget(title)

        self.appointment_combo = QtWidgets.QComboBox()
        self.appointment_combo.setMinimumHeight(40)
        self.appointment_combo.currentIndexChanged.connect(self._load_selected_context)
        layout.addWidget(self.appointment_combo)

        self.status_label = QtWidgets.QLabel("Chọn lịch hẹn để bắt đầu khám.")
        self.status_label.setStyleSheet("color: #64748b;")
        layout.addWidget(self.status_label)

        form = QtWidgets.QFormLayout()
        self.reason_input = QtWidgets.QTextEdit()
        self.symptoms_input = QtWidgets.QTextEdit()
        self.diagnosis_input = QtWidgets.QTextEdit()
        self.treatment_input = QtWidgets.QTextEdit()
        self.notes_input = QtWidgets.QTextEdit()
        for widget in [
            self.reason_input,
            self.symptoms_input,
            self.diagnosis_input,
            self.treatment_input,
            self.notes_input,
        ]:
            widget.setMinimumHeight(72)
            widget.setStyleSheet(
                "background: white; color: #1f2937; border: 1px solid #dbe4ee; border-radius: 8px;"
            )

        form.addRow("Lý do khám", self.reason_input)
        form.addRow("Triệu chứng", self.symptoms_input)
        form.addRow("Chẩn đoán", self.diagnosis_input)
        form.addRow("Hướng điều trị", self.treatment_input)
        form.addRow("Ghi chú", self.notes_input)
        layout.addLayout(form, 1)

        actions = QtWidgets.QHBoxLayout()
        self.save_draft_btn = QtWidgets.QPushButton("Lưu tạm")
        self.finalize_btn = QtWidgets.QPushButton("Hoàn tất khám")
        self.prescription_btn = QtWidgets.QPushButton("Tạo đơn thuốc")
        for button in [self.save_draft_btn, self.finalize_btn, self.prescription_btn]:
            button.setMinimumHeight(42)
            actions.addWidget(button)
        actions.addStretch()
        layout.addLayout(actions)

        self.save_draft_btn.clicked.connect(self.save_draft)
        self.finalize_btn.clicked.connect(self.finalize_exam)
        self.prescription_btn.clicked.connect(self.open_prescription_page)
        self.load_appointments()

    def load_appointments(self):
        self.appointment_combo.blockSignals(True)
        self.appointment_combo.clear()
        rows = AppointmentController.get_by_doctor(self.doctor_id) or []
        for row in rows:
            if AppointmentController.can_start_exam(row.get("status")):
                self.appointment_combo.addItem(
                    f"#{row.get('appointment_id')} - {row.get('patient_name', '')} - {row.get('appointment_date', '')}",
                    row,
                )
        self.appointment_combo.blockSignals(False)
        self._load_selected_context()

    def set_appointment(self, appointment_id):
        for index in range(self.appointment_combo.count()):
            row = self.appointment_combo.itemData(index)
            if row and str(row.get("appointment_id")) == str(appointment_id):
                self.appointment_combo.setCurrentIndex(index)
                self._load_selected_context()
                return True
        return False

    def _load_selected_context(self):
        self.current_appointment = self.appointment_combo.currentData()
        self.current_record = None
        for widget in [
            self.reason_input,
            self.symptoms_input,
            self.diagnosis_input,
            self.treatment_input,
            self.notes_input,
        ]:
            widget.clear()

        if not self.current_appointment:
            self.status_label.setText("Không có lịch hẹn phù hợp để khám.")
            return

        appointment_id = self.current_appointment.get("appointment_id")
        self.current_record = MedicalRecordController.get_by_appointment(appointment_id)
        if self.current_record:
            self.diagnosis_input.setPlainText(str(self.current_record.get("diagnosis") or ""))
            self.treatment_input.setPlainText(str(self.current_record.get("treatment") or ""))
            self.status_label.setText(f"Đã tải bản nháp cho lịch #{appointment_id}.")
        else:
            self.status_label.setText(f"Sẵn sàng khám lịch #{appointment_id}.")

    def save_draft(self):
        if not self.current_appointment:
            self.status_label.setText("Không có lịch hẹn để lưu.")
            return {"status": False}

        result = MedicalRecordController.save_draft(
            self.current_appointment.get("patient_id"),
            self.doctor_id,
            self.current_appointment.get("appointment_id"),
            self.diagnosis_input.toPlainText().strip(),
            self.treatment_input.toPlainText().strip(),
            self.symptoms_input.toPlainText().strip(),
            "",
            self.notes_input.toPlainText().strip(),
        )
        self.current_record = result.get("record")
        self.status_label.setText(result.get("message", ""))
        return result

    def finalize_exam(self):
        if not self.current_record:
            draft_result = self.save_draft()
            self.current_record = draft_result.get("record")

        if not self.current_record:
            result = {"status": False, "message": "Không có bản ghi khám để hoàn tất."}
            self.status_label.setText(result["message"])
            return result

        result = MedicalRecordController.finalize(
            self.current_record.get("record_id"),
            self.diagnosis_input.toPlainText().strip(),
            self.treatment_input.toPlainText().strip(),
            self.current_appointment.get("appointment_id") if self.current_appointment else None,
        )
        self.status_label.setText(result.get("message", ""))
        return result

    def open_prescription_page(self):
        parent = self.parent()
        while parent and not hasattr(parent, "switch_page"):
            parent = parent.parent()
        if parent:
            parent.switch_page(5)
