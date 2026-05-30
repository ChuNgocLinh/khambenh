from PyQt6 import QtCore, QtWidgets

from controllers.appointment_controller import AppointmentController
from controllers.medical_record_controller import MedicalRecordController
from views.doctor_ui_utils import PAGE_BG, avatar, badge, button, card, input_style, page_title, parse_datetime


class DoctorExaminationView(QtWidgets.QWidget):
    def __init__(self, doctor_id, parent=None):
        super().__init__(parent)
        self.doctor_id = doctor_id
        self.role = "doctor"
        self.current_appointment = None
        self.current_record = None
        self.setStyleSheet(f"background: {PAGE_BG};")

        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        content = QtWidgets.QWidget()
        content.setStyleSheet(f"background: {PAGE_BG};")
        root = QtWidgets.QVBoxLayout(content)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(8)
        root.addWidget(page_title("Khám bệnh", "Trang chủ  >  Khám bệnh  >  Thông tin khám"))
        root.addWidget(self._build_step_progress())
        root.addWidget(self._build_patient_summary())

        body = QtWidgets.QHBoxLayout()
        body.setSpacing(10)
        body.addWidget(self._build_form_card(), 8)
        body.addWidget(self._build_context_sidebar(), 2)
        root.addLayout(body, 1)
        root.addWidget(self._build_footer_actions())
        scroll.setWidget(content)
        outer.addWidget(scroll)
        self.load_appointments()

    def _build_step_progress(self):
        wrapper = card()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(12, 8, 12, 8)
        steps = ["1. Thông tin khám", "2. Chẩn đoán - Kết luận", "3. Chỉ định - Kê đơn", "4. Hoàn tất"]
        for idx, text in enumerate(steps):
            active = idx == 0
            layout.addWidget(badge(text, "#FFFFFF" if active else "#667085", "#16B364" if active else "#F2F4F7"))
            if idx < len(steps) - 1:
                line = QtWidgets.QFrame()
                line.setFixedHeight(1)
                line.setStyleSheet("background: #EAECF0;")
                layout.addWidget(line, 1)
        return wrapper

    def _build_patient_summary(self):
        wrapper = card()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)
        self.patient_avatar_holder = QtWidgets.QWidget()
        self.patient_avatar_layout = QtWidgets.QVBoxLayout(self.patient_avatar_holder)
        self.patient_avatar_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.patient_avatar_holder)
        info = QtWidgets.QVBoxLayout()
        self.patient_name_label = QtWidgets.QLabel("Chọn lịch hẹn để bắt đầu khám")
        self.patient_name_label.setStyleSheet("font-size: 18px; font-weight: 900; color: #101828;")
        self.patient_meta_label = QtWidgets.QLabel("")
        self.patient_meta_label.setStyleSheet("color: #667085; font-size: 13px;")
        self.status_label = QtWidgets.QLabel("Chọn lịch hẹn để bắt đầu khám.")
        self.status_label.setStyleSheet("color: #667085; font-size: 13px;")
        info.addWidget(self.patient_name_label)
        info.addWidget(self.patient_meta_label)
        info.addWidget(self.status_label)
        layout.addLayout(info, 1)
        self.appointment_combo = QtWidgets.QComboBox()
        self.appointment_combo.setMinimumHeight(34)
        self.appointment_combo.setMinimumWidth(240)
        self.appointment_combo.setStyleSheet(input_style())
        self.appointment_combo.currentIndexChanged.connect(self._load_selected_context)
        layout.addWidget(self.appointment_combo)
        return wrapper

    def _build_form_card(self):
        wrapper = card()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)
        layout.addWidget(self._section_title("Triệu chứng - Hỏi bệnh"))
        self.reason_input = self._text_input(46)
        self.symptoms_input = self._text_input(46)
        self.history_input = self._text_input(44)
        layout.addLayout(self._form_row([("Lý do khám", self.reason_input), ("Triệu chứng", self.symptoms_input)]))
        layout.addLayout(self._form_row([("Tiền sử bệnh / dị ứng", self.history_input)]))

        layout.addWidget(self._section_title("Khám lâm sàng"))
        vitals = QtWidgets.QGridLayout()
        vitals.setHorizontalSpacing(8)
        vitals.setVerticalSpacing(6)
        self.pulse_input = self._line_input("Mạch")
        self.bp_input = self._line_input("Huyết áp")
        self.temp_input = self._line_input("Nhiệt độ")
        self.breath_input = self._line_input("Nhịp thở")
        self.weight_input = self._line_input("Cân nặng")
        self.height_input = self._line_input("Chiều cao")
        for idx, (label, widget) in enumerate(
            [
                ("Mạch", self.pulse_input),
                ("Huyết áp", self.bp_input),
                ("Nhiệt độ", self.temp_input),
                ("Nhịp thở", self.breath_input),
                ("Cân nặng", self.weight_input),
                ("Chiều cao", self.height_input),
            ]
        ):
            vitals.addWidget(self._field(label, widget), idx // 3, idx % 3)
        layout.addLayout(vitals)
        self.clinical_input = self._text_input(46)
        layout.addLayout(self._form_row([("Kết quả khám", self.clinical_input)]))

        layout.addWidget(self._section_title("Chẩn đoán sơ bộ"))
        self.diagnosis_input = self._text_input(46)
        self.treatment_input = self._text_input(46)
        self.notes_input = self._text_input(44)
        layout.addLayout(self._form_row([("Chẩn đoán", self.diagnosis_input), ("Hướng điều trị", self.treatment_input)]))
        layout.addLayout(self._form_row([("Ghi chú", self.notes_input)]))
        return wrapper

    def _build_context_sidebar(self):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        self.quick_info = QtWidgets.QLabel("Nhóm máu: Chưa cập nhật\nNghề nghiệp: Chưa cập nhật\nBHYT: Chưa cập nhật")
        self.history_label = QtWidgets.QLabel("Chưa có lịch sử khám được chọn.")
        self.lab_label = QtWidgets.QLabel("Kết quả cận lâm sàng: Chưa cập nhật")
        for title, label in [("Thông tin nhanh", self.quick_info), ("Lịch sử khám", self.history_label), ("Kết quả cận lâm sàng", self.lab_label)]:
            panel = card()
            panel_layout = QtWidgets.QVBoxLayout(panel)
            panel_layout.setContentsMargins(10, 10, 10, 10)
            head = QtWidgets.QLabel(title)
            head.setStyleSheet("font-size: 15px; font-weight: 900; color: #101828;")
            label.setWordWrap(True)
            label.setStyleSheet("color: #475467; font-size: 13px;")
            panel_layout.addWidget(head)
            panel_layout.addWidget(label)
            layout.addWidget(panel)
        layout.addStretch()
        return wrapper

    def _build_footer_actions(self):
        wrapper = card()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(12, 6, 12, 6)
        self.cancel_btn = button("Hủy khám", "danger")
        self.save_draft_btn = button("Lưu tạm", "outline")
        self.finalize_btn = button("Hoàn tất khám")
        self.prescription_btn = button("Tạo đơn thuốc", "outline")
        self.cancel_btn.clicked.connect(self.cancel_exam)
        self.save_draft_btn.clicked.connect(self.save_draft)
        self.finalize_btn.clicked.connect(self.finalize_exam)
        self.prescription_btn.clicked.connect(self.open_prescription_page)
        layout.addStretch()
        for btn in [self.cancel_btn, self.save_draft_btn, self.finalize_btn, self.prescription_btn]:
            layout.addWidget(btn)
        return wrapper

    def _section_title(self, text):
        label = QtWidgets.QLabel(text)
        label.setStyleSheet("font-size: 16px; font-weight: 900; color: #101828; margin-top: 2px;")
        return label

    def _line_input(self, placeholder=""):
        widget = QtWidgets.QLineEdit()
        widget.setPlaceholderText(placeholder)
        widget.setFixedHeight(32)
        widget.setStyleSheet(input_style())
        return widget

    def _text_input(self, height):
        widget = QtWidgets.QTextEdit()
        widget.setFixedHeight(height)
        widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        widget.setStyleSheet(input_style())
        return widget

    def _field(self, label, widget):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        text = QtWidgets.QLabel(label)
        text.setStyleSheet("font-size: 12px; color: #667085; font-weight: 800;")
        layout.addWidget(text)
        layout.addWidget(widget)
        return wrapper

    def _form_row(self, fields):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(8)
        for label, widget in fields:
            row.addWidget(self._field(label, widget), 1)
        return row

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
        self._clear_form_inputs()

        if not self.current_appointment:
            self.patient_name_label.setText("Không có lịch hẹn phù hợp để khám.")
            self.patient_meta_label.setText("")
            self.status_label.setText("Không có lịch hẹn phù hợp để khám.")
            return

        appt = self.current_appointment
        while self.patient_avatar_layout.count():
            item = self.patient_avatar_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.patient_avatar_layout.addWidget(avatar(appt.get("patient_name"), 58))
        dt = parse_datetime(appt.get("appointment_date"))
        self.patient_name_label.setText(str(appt.get("patient_name") or "Bệnh nhân"))
        self.patient_meta_label.setText(
            f"Mã BN: BN{int(appt.get('patient_id') or 0):06d} | Ngày khám: {dt.strftime('%d/%m/%Y %H:%M') if dt else appt.get('appointment_date', '')}"
        )
        appointment_id = appt.get("appointment_id")
        self.current_record = MedicalRecordController.get_by_appointment(appointment_id)
        if self.current_record:
            self.diagnosis_input.setPlainText(str(self.current_record.get("diagnosis") or ""))
            self.treatment_input.setPlainText(str(self.current_record.get("treatment") or ""))
            self.symptoms_input.setPlainText(str(self.current_record.get("symptoms") or ""))
            self.clinical_input.setPlainText(str(self.current_record.get("conclusion") or ""))
            self.notes_input.setPlainText(str(self.current_record.get("notes") or ""))
            self.status_label.setText(f"Đã tải bản nháp cho lịch #{appointment_id}.")
        else:
            self.status_label.setText(f"Sẵn sàng khám lịch #{appointment_id}.")

    def validate_vitals(self):
        pulse = self.pulse_input.text().strip()
        bp = self.bp_input.text().strip()
        temp = self.temp_input.text().strip()
        breath = self.breath_input.text().strip()
        weight = self.weight_input.text().strip()
        height = self.height_input.text().strip()

        if pulse:
            try:
                val = int(pulse)
                if val <= 0 or val > 300:
                    raise ValueError()
            except ValueError:
                return False, "Mạch phải là số nguyên dương hợp lệ (30 - 300)."

        if bp:
            import re
            if not re.match(r"^\d+/\d+$", bp):
                return False, "Huyết áp phải có định dạng dạng tâm thu/tâm trương (ví dụ: 120/80)."

        if temp:
            try:
                val = float(temp)
                if val < 30.0 or val > 45.0:
                    raise ValueError()
            except ValueError:
                return False, "Nhiệt độ phải là số hợp lệ (30.0 - 45.0 °C)."

        if breath:
            try:
                val = int(breath)
                if val <= 0 or val > 100:
                    raise ValueError()
            except ValueError:
                return False, "Nhịp thở phải là số nguyên dương hợp lệ (10 - 100)."

        if weight:
            try:
                val = float(weight)
                if val <= 0 or val > 500:
                    raise ValueError()
            except ValueError:
                return False, "Cân nặng phải là số dương hợp lệ (kg)."

        if height:
            try:
                val = float(height)
                if val <= 0 or val > 300:
                    raise ValueError()
            except ValueError:
                return False, "Chiều cao phải là số dương hợp lệ (cm)."

        return True, ""

    def save_draft(self):
        if not self.current_appointment:
            result = {"status": False, "message": "Không có lịch hẹn để lưu."}
            self.status_label.setText(result["message"])
            return result
        
        ok_vitals, err_msg = self.validate_vitals()
        if not ok_vitals:
            self.status_label.setText(err_msg)
            return {"status": False, "message": err_msg}

        result = MedicalRecordController.save_draft(
            self.current_appointment.get("patient_id"),
            self.doctor_id,
            self.current_appointment.get("appointment_id"),
            self.diagnosis_input.toPlainText().strip(),
            self.treatment_input.toPlainText().strip(),
            self.symptoms_input.toPlainText().strip(),
            self.clinical_input.toPlainText().strip(),
            self.notes_input.toPlainText().strip(),
        )
        self.current_record = result.get("record")
        self.status_label.setText(result.get("message", ""))
        return result

    def finalize_exam(self):
        draft_result = self.save_draft()
        if not draft_result.get("status"):
            return draft_result
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
        if not self.current_record or str(self.current_record.get("record_status") or "").lower() != "finalized":
            result = self.finalize_exam()
            if not result.get("status"):
                return result
        parent = self.parent()
        while parent and not hasattr(parent, "switch_page"):
            parent = parent.parent()
        if parent:
            prescription_page = getattr(parent, "page_prescription", None)
            if hasattr(prescription_page, "set_record"):
                prescription_page.set_record(
                    self.current_record.get("record_id"),
                    self.current_appointment.get("patient_id") if self.current_appointment else None,
                )
            parent.switch_page(5)
        return {"status": True, "message": "Đã chuyển sang màn kê đơn thuốc."}

    def cancel_exam(self):
        self._clear_form_inputs()
        self.current_record = None
        self.current_appointment = None
        self.appointment_combo.blockSignals(True)
        self.appointment_combo.setCurrentIndex(-1)
        self.appointment_combo.blockSignals(False)
        while self.patient_avatar_layout.count():
            item = self.patient_avatar_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.patient_name_label.setText("Chọn lịch hẹn để bắt đầu khám")
        self.patient_meta_label.setText("")
        self.status_label.setText("Đã hủy thao tác khám hiện tại.")
        parent = self.parent()
        while parent and not hasattr(parent, "switch_page"):
            parent = parent.parent()
        if parent:
            parent.switch_page(1)
        return {"status": True, "message": "Đã hủy thao tác khám hiện tại."}

    def _clear_form_inputs(self):
        for widget in [self.reason_input, self.symptoms_input, self.history_input, self.clinical_input, self.diagnosis_input, self.treatment_input, self.notes_input]:
            widget.clear()
        for widget in [self.pulse_input, self.bp_input, self.temp_input, self.breath_input, self.weight_input, self.height_input]:
            widget.clear()
