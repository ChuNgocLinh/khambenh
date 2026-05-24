import logging

from PyQt6 import QtCore, QtWidgets

from controllers.appointment_controller import AppointmentController
from controllers.medical_record_controller import MedicalRecordController
from controllers.patient_controller import PatientController
from controllers.prescription_controller import PrescriptionController
from views.doctor_ui_utils import (
    PAGE_BG,
    age_from_dob,
    avatar,
    badge,
    button,
    card,
    input_style,
    page_title,
    parse_datetime,
    table_style,
)

logger = logging.getLogger(__name__)


class DoctorPatientRecordView(QtWidgets.QWidget):
    def __init__(self, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        self.role = "doctor"
        self.patient_id = None
        self.patient = None
        self.records = []
        self.prescriptions = []
        self.appointments = []
        self.patient_options = []
        self.selected_record = None
        self.last_error = ""
        self.setStyleSheet(f"background: {PAGE_BG};")

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(14)
        root.addWidget(page_title("Hồ sơ bệnh nhân", "Trang chủ  >  Hồ sơ bệnh nhân  >  Chi tiết hồ sơ"))
        root.addWidget(self._build_patient_selector())
        root.addWidget(self._build_profile_card())
        root.addWidget(self._build_tabs(), 1)
        root.addLayout(self._build_actions())
        self._load_patient_options()
        self._render_empty("Chọn bệnh nhân để xem hồ sơ.")

    def _build_patient_selector(self):
        wrapper = card()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        label = QtWidgets.QLabel("Bệnh nhân")
        label.setStyleSheet("font-size: 14px; font-weight: 900; color: #101828;")
        self.patient_search = QtWidgets.QLineEdit()
        self.patient_search.setPlaceholderText("Tìm theo tên, SĐT, mã BN...")
        self.patient_search.setStyleSheet(input_style())
        self.patient_combo = QtWidgets.QComboBox()
        self.patient_combo.setMinimumWidth(320)
        self.patient_combo.setMinimumHeight(42)
        self.patient_combo.setStyleSheet(input_style())
        self.patient_combo.currentIndexChanged.connect(self._select_patient_from_combo)
        self.patient_search.textChanged.connect(self._filter_patient_options)
        reload_btn = button("Tải danh sách", "outline")
        reload_btn.clicked.connect(self._load_patient_options)

        layout.addWidget(label)
        layout.addWidget(self.patient_search, 1)
        layout.addWidget(self.patient_combo, 1)
        layout.addWidget(reload_btn)
        return wrapper

    def _build_profile_card(self):
        wrapper = card()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        self.profile_avatar_box = QtWidgets.QWidget()
        self.profile_avatar_layout = QtWidgets.QVBoxLayout(self.profile_avatar_box)
        self.profile_avatar_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.profile_avatar_box)

        info = QtWidgets.QVBoxLayout()
        self.title_label = QtWidgets.QLabel("Hồ sơ bệnh nhân")
        self.title_label.setStyleSheet("font-size: 22px; font-weight: 900; color: #101828;")
        self.summary_label = QtWidgets.QLabel("Chọn bệnh nhân để xem hồ sơ.")
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet("color: #475467; font-size: 13px;")
        self.error_label = QtWidgets.QLabel("")
        self.error_label.setWordWrap(True)
        self.error_label.setStyleSheet("color: #B42318; font-size: 13px; font-weight: 700;")
        info.addWidget(self.title_label)
        info.addWidget(self.summary_label)
        info.addWidget(self.error_label)
        layout.addLayout(info, 2)

        self.profile_side = QtWidgets.QLabel("Nhóm máu: Chưa cập nhật\nBHYT: Chưa cập nhật\nNgười liên hệ: Chưa cập nhật")
        self.profile_side.setWordWrap(True)
        self.profile_side.setStyleSheet("color: #475467; font-size: 13px;")
        layout.addWidget(self.profile_side, 1)
        return wrapper

    def _build_tabs(self):
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet(
            "QTabWidget::pane { border: 1px solid #EAECF0; border-radius: 14px; background: white; }"
            "QTabBar::tab { background: white; color: #667085; padding: 10px 14px; font-weight: 800; }"
            "QTabBar::tab:selected { color: #16B364; border-bottom: 2px solid #16B364; }"
        )

        history_page = QtWidgets.QWidget()
        history_layout = QtWidgets.QHBoxLayout(history_page)
        history_layout.setContentsMargins(14, 14, 14, 14)
        history_layout.setSpacing(14)
        history_layout.addWidget(self._build_visit_sidebar(), 3)
        history_layout.addWidget(self._build_visit_detail(), 4)
        history_layout.addWidget(self._build_summary_sidebar(), 2)
        self.tabs.addTab(history_page, "Lịch sử khám")

        self.records_table = self._table(["Ngày", "Bác sĩ", "Chẩn đoán", "Điều trị", "Trạng thái"])
        self.prescriptions_table = self._table(["Hồ sơ", "Thuốc đã kê", "Tổng SL", "Trạng thái"])
        self.appointments_table = self._table(["Ngày hẹn", "Bác sĩ", "Trạng thái", "Ghi chú"])
        self.tabs.addTab(self.records_table, "Bệnh sử")
        self.tabs.addTab(self.prescriptions_table, "Đơn thuốc")
        self.tabs.addTab(self.appointments_table, "Lịch hẹn")
        self.tabs.addTab(self._placeholder("Kết quả xét nghiệm đang được đồng bộ."), "Kết quả xét nghiệm")
        self.tabs.addTab(self._placeholder("Tài liệu đính kèm chưa cập nhật."), "Tài liệu đính kèm")
        return self.tabs

    def _build_visit_sidebar(self):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        title = QtWidgets.QLabel("Lịch sử khám")
        title.setStyleSheet("font-size: 17px; font-weight: 900; color: #101828;")
        self.history_search = QtWidgets.QLineEdit()
        self.history_search.setPlaceholderText("Tìm theo ngày, bác sĩ, lý do khám, chẩn đoán...")
        self.history_search.setStyleSheet(input_style())
        self.history_search.textChanged.connect(self._render_visit_cards)
        self.visit_list = QtWidgets.QVBoxLayout()
        self.visit_list.setSpacing(10)
        scroll_body = QtWidgets.QWidget()
        scroll_body.setLayout(self.visit_list)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll.setWidget(scroll_body)
        layout.addWidget(title)
        layout.addWidget(self.history_search)
        layout.addWidget(scroll, 1)
        return wrapper

    def _build_visit_detail(self):
        wrapper = card()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)
        self.visit_detail_title = QtWidgets.QLabel("Chi tiết lần khám")
        self.visit_detail_title.setStyleSheet("font-size: 18px; font-weight: 900; color: #101828;")
        self.visit_detail_body = QtWidgets.QLabel("Chọn một lần khám để xem chi tiết.")
        self.visit_detail_body.setWordWrap(True)
        self.visit_detail_body.setStyleSheet("color: #475467; font-size: 13px; line-height: 150%;")
        layout.addWidget(self.visit_detail_title)
        layout.addWidget(self.visit_detail_body)
        layout.addStretch()
        return wrapper

    def _build_summary_sidebar(self):
        wrapper = card()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        title = QtWidgets.QLabel("Tóm tắt hồ sơ")
        title.setStyleSheet("font-size: 16px; font-weight: 900; color: #101828;")
        self.metric_label = QtWidgets.QLabel("Tổng số lần khám: 0\nTổng đơn thuốc: 0\nTổng lịch hẹn: 0")
        self.metric_label.setStyleSheet("color: #475467; font-size: 13px;")
        self.medical_alerts_label = QtWidgets.QLabel("Bệnh mãn tính/Dị ứng: Chưa cập nhật")
        self.medical_alerts_label.setWordWrap(True)
        self.medical_alerts_label.setStyleSheet("color: #B54708; font-size: 13px; font-weight: 700;")
        layout.addWidget(title)
        layout.addWidget(self.metric_label)
        layout.addWidget(badge("Bệnh mãn tính: Chưa cập nhật", "#F79009", "#FFF7ED"))
        layout.addWidget(badge("Dị ứng: Chưa cập nhật", "#F04438", "#FEF3F2"))
        layout.addWidget(self.medical_alerts_label)
        for text, page, callback in [
            ("Tạo lịch hẹn", 1, None),
            ("Khám bệnh", 3, self._open_exam_with_context),
            ("Kê đơn thuốc", 5, self._open_prescription_with_context),
            ("In hồ sơ", None, self._print_record),
        ]:
            btn = button(text, "outline")
            if callback:
                btn.clicked.connect(callback)
            elif page is not None:
                btn.clicked.connect(lambda checked=False, p=page: self._switch_page(p))
            layout.addWidget(btn)
        layout.addStretch()
        return wrapper

    def _build_actions(self):
        actions = QtWidgets.QHBoxLayout()
        self.open_exam_btn = button("Khám bệnh", "outline")
        self.open_prescription_btn = button("Tạo đơn thuốc", "outline")
        self.refresh_btn = button("Làm mới", "primary")
        self.open_exam_btn.clicked.connect(self._open_exam_with_context)
        self.open_prescription_btn.clicked.connect(self._open_prescription_with_context)
        self.refresh_btn.clicked.connect(self.load_data)
        actions.addStretch()
        for btn in [self.open_exam_btn, self.open_prescription_btn, self.refresh_btn]:
            actions.addWidget(btn)
        return actions

    def _placeholder(self, text):
        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("background: white; color: #667085;")
        return label

    def _table(self, headers):
        table = QtWidgets.QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setStyleSheet(table_style())
        table.setShowGrid(False)
        return table

    def _load_patient_options(self):
        try:
            self.patient_options = PatientController.get_by_doctor(self.doctor_id) or []
            self.last_error = ""
        except Exception as exc:
            logger.exception("Cannot load patient options for doctor_id=%s", self.doctor_id)
            self.patient_options = []
            self._set_error(f"Không thể tải danh sách bệnh nhân: {exc}")
        self._filter_patient_options()

    def _filter_patient_options(self):
        if not hasattr(self, "patient_combo"):
            return
        keyword = self.patient_search.text().strip().lower() if hasattr(self, "patient_search") else ""
        current_id = self.patient_id
        self.patient_combo.blockSignals(True)
        self.patient_combo.clear()
        self.patient_combo.addItem("Chọn bệnh nhân", None)
        for row in self.patient_options:
            haystack = f"BN{int(row.get('patient_id') or 0):06d} {row.get('name', '')} {row.get('phone', '')}".lower()
            if keyword and keyword not in haystack:
                continue
            self.patient_combo.addItem(
                f"BN{int(row.get('patient_id') or 0):06d} - {row.get('name', '')} - {row.get('phone') or 'Chưa có SĐT'}",
                row.get("patient_id"),
            )
            if current_id and str(row.get("patient_id")) == str(current_id):
                self.patient_combo.setCurrentIndex(self.patient_combo.count() - 1)
        self.patient_combo.blockSignals(False)

    def _select_patient_from_combo(self):
        patient_id = self.patient_combo.currentData()
        if patient_id and str(patient_id) != str(self.patient_id):
            self.set_patient(patient_id)

    def _set_error(self, message):
        self.last_error = message or ""
        if hasattr(self, "error_label"):
            self.error_label.setText(self.last_error)

    def set_patient(self, patient_id):
        self.patient_id = patient_id
        self._filter_patient_options()
        self.load_data()

    def load_data(self):
        if not self.patient_id:
            self._render_empty("Chọn bệnh nhân để xem hồ sơ.")
            return
        self._set_error("")
        self.selected_record = None
        try:
            self.patient = PatientController.get_by_id(self.patient_id)
        except AttributeError:
            from models.patient_model import PatientModel

            self.patient = PatientModel.get_by_id(self.patient_id)
        except Exception as exc:
            logger.exception("Cannot load patient_id=%s", self.patient_id)
            self.patient = None
            self._set_error(f"Không thể tải thông tin bệnh nhân: {exc}")

        try:
            self.records = MedicalRecordController.get_by_patient(self.patient_id) or []
        except Exception as exc:
            logger.exception("Cannot load medical records for patient_id=%s", self.patient_id)
            self.records = []
            self._set_error(f"Không thể tải lịch sử khám: {exc}")

        try:
            self.appointments = AppointmentController.get_by_patient(self.patient_id) or []
        except Exception as exc:
            logger.exception("Cannot load appointments for patient_id=%s", self.patient_id)
            self.appointments = []
            self._set_error(f"Không thể tải lịch hẹn: {exc}")

        if not self.patient:
            self._render_empty("Không tìm thấy bệnh nhân.")
            return

        if not self._can_current_doctor_view_patient():
            self.records = []
            self.prescriptions = []
            self.appointments = []
            self._render_empty("Bạn không có quyền xem hồ sơ bệnh nhân này.")
            return

        self.prescriptions = []
        for record in self.records:
            try:
                for item in PrescriptionController.get_by_record(record.get("record_id")) or []:
                    item["record_id"] = record.get("record_id")
                    self.prescriptions.append(item)
            except Exception as exc:
                logger.exception("Cannot load prescriptions for record_id=%s", record.get("record_id"))
                self._set_error(f"Không thể tải đơn thuốc của hồ sơ #{record.get('record_id')}: {exc}")
        self._render()

    def _can_current_doctor_view_patient(self):
        if str(getattr(self, "role", "doctor")).lower() != "doctor":
            return True
        if not self.doctor_id:
            return False
        allowed_ids = {
            str(row.get("patient_id"))
            for row in (self.patient_options or [])
            if row.get("patient_id") not in (None, "")
        }
        if str(self.patient_id) in allowed_ids:
            return True
        rows = (self.records or []) + (self.appointments or [])
        scoped_rows = [row for row in rows if row.get("doctor_id") not in (None, "")]
        return any(str(row.get("doctor_id")) == str(self.doctor_id) for row in scoped_rows)

    def _render_empty(self, message):
        self.summary_label.setText(message)
        self.title_label.setText("Hồ sơ bệnh nhân")
        self.profile_side.setText("Nhóm máu: Chưa cập nhật\nBHYT: Chưa cập nhật\nNgười liên hệ: Chưa cập nhật")
        self.metric_label.setText("Tổng số lần khám: 0\nTổng đơn thuốc: 0\nTổng lịch hẹn: 0")
        self.records_table.setRowCount(0)
        self.prescriptions_table.setRowCount(0)
        self.appointments_table.setRowCount(0)
        self._render_visit_cards()
        self.visit_detail_title.setText("Chi tiết lần khám")
        self.visit_detail_body.setText(message)

    def _render(self):
        if not self.patient:
            self._render_empty("Không tìm thấy bệnh nhân.")
            return
        patient_name = str(self.patient.get("name", "") or "")
        while self.profile_avatar_layout.count():
            item = self.profile_avatar_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.profile_avatar_layout.addWidget(avatar(patient_name, 64))
        self.title_label.setText(patient_name)
        self.summary_label.setText(
            f"{patient_name}\n"
            f"Mã BN: BN{int(self.patient.get('patient_id') or 0):06d} | "
            f"Giới tính: {self.patient.get('gender') or 'Chưa cập nhật'} | "
            f"Ngày sinh: {self.patient.get('dob') or 'Chưa cập nhật'} "
            f"({age_from_dob(self.patient.get('dob')) or 'Chưa rõ tuổi'}) | "
            f"SĐT: {self.patient.get('phone') or 'Chưa cập nhật'}\n"
            f"Email: {self.patient.get('email') or 'Chưa cập nhật'} | "
            f"Địa chỉ: {self.patient.get('address') or 'Chưa cập nhật'}"
        )
        self.profile_side.setText(
            "Nhóm máu: Chưa cập nhật\n"
            f"Nghề nghiệp: {self.patient.get('occupation') or 'Chưa cập nhật'}\n"
            f"CCCD: {self.patient.get('cccd') or 'Chưa cập nhật'}\n"
            f"Ghi chú tiếp nhận: {self.patient.get('intake_notes') or 'Chưa cập nhật'}"
        )
        last_record = self.records[0].get("created_at") if self.records else "Chưa có"
        last_prescription = self.prescriptions[0].get("updated_at") if self.prescriptions else "Chưa có"
        self.metric_label.setText(
            f"Tổng số lần khám: {len(self.records)}\n"
            f"Tổng dòng thuốc đã kê: {len(self.prescriptions)}\n"
            f"Tổng lịch hẹn: {len(self.appointments)}\n"
            f"Lần khám gần nhất: {last_record}\n"
            f"Đơn thuốc gần nhất: {last_prescription}"
        )
        self.medical_alerts_label.setText(f"Bệnh mãn tính/Dị ứng: {self.patient.get('intake_notes') or 'Chưa cập nhật'}")
        self._render_records()
        self._render_prescriptions()
        self._render_appointments()
        self._render_visit_cards()
        if self.records:
            self._select_record(self.records[0])
        else:
            self.visit_detail_body.setText("Chưa có lần khám nào trong hồ sơ.")

    def _render_visit_cards(self):
        while self.visit_list.count():
            item = self.visit_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        keyword = self.history_search.text().strip().lower() if hasattr(self, "history_search") else ""
        rows = [row for row in self.records if not keyword or keyword in self._record_search_text(row)]
        if not rows:
            empty = QtWidgets.QLabel("Chưa có lịch sử khám.")
            empty.setStyleSheet("color: #667085;")
            self.visit_list.addWidget(empty)
            self.visit_list.addStretch()
            return
        for row in rows:
            is_selected = self.selected_record and self.selected_record.get("record_id") == row.get("record_id")
            service = row.get("service_names") or "Chưa rõ dịch vụ"
            btn = QtWidgets.QPushButton(
                f"{row.get('created_at') or row.get('appointment_date') or 'Chưa rõ ngày'}\n"
                f"{row.get('doctor_name') or 'Chưa rõ bác sĩ'} - {service}\n"
                f"{row.get('diagnosis') or 'Chưa có chẩn đoán'}"
            )
            btn.setMinimumHeight(92)
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            border = "#16B364" if is_selected else "#EAECF0"
            background = "#ECFDF3" if is_selected else "white"
            btn.setStyleSheet(
                f"QPushButton {{ text-align: left; background: {background}; color: #344054; border: 1px solid {border}; "
                "border-radius: 12px; padding: 10px; font-weight: 700; } QPushButton:hover { background: #F9FAFB; }"
            )
            btn.clicked.connect(lambda checked=False, r=row: self._select_record(r))
            self.visit_list.addWidget(btn)
        self.visit_list.addStretch()

    def _record_search_text(self, row):
        fields = [
            "created_at",
            "appointment_date",
            "diagnosis",
            "treatment",
            "doctor_name",
            "reason",
            "symptoms",
            "record_status",
            "appointment_status",
            "service_names",
            "note",
        ]
        return " ".join(str(row.get(field) or "") for field in fields).lower()

    def _select_record(self, row):
        self.selected_record = row
        dt = parse_datetime(row.get("created_at"))
        self.visit_detail_title.setText(f"Chi tiết lần khám - {dt.strftime('%d/%m/%Y') if dt else row.get('created_at', '')}")
        self.visit_detail_body.setText(
            f"Bác sĩ: {row.get('doctor_name') or 'Chưa cập nhật'}\n"
            f"Lịch hẹn: {row.get('appointment_date') or 'Chưa cập nhật'}\n"
            f"Dịch vụ: {row.get('service_names') or 'Chưa cập nhật'}\n"
            f"Lý do khám/Ghi chú: {row.get('reason') or row.get('note') or 'Chưa cập nhật'}\n"
            f"Triệu chứng: {row.get('symptoms') or 'Chưa cập nhật'}\n\n"
            "Khám lâm sàng:\n"
            f"- Mạch: {row.get('pulse') or 'Chưa cập nhật'}\n"
            f"- Huyết áp: {row.get('blood_pressure') or 'Chưa cập nhật'}\n"
            f"- Nhiệt độ: {row.get('temperature') or 'Chưa cập nhật'}\n\n"
            f"Chẩn đoán: {row.get('diagnosis') or 'Chưa cập nhật'}\n"
            f"Kết luận/Hướng điều trị: {row.get('treatment') or 'Chưa cập nhật'}\n"
            f"Trạng thái hồ sơ: {row.get('record_status') or 'Chưa cập nhật'}\n"
            f"Trạng thái lịch: {row.get('appointment_status') or 'Chưa cập nhật'}"
        )
        self._render_visit_cards()

    def _render_records(self):
        self.records_table.setRowCount(len(self.records))
        for index, row in enumerate(self.records):
            values = [
                row.get("created_at", ""),
                row.get("doctor_name", ""),
                row.get("diagnosis", ""),
                row.get("treatment", ""),
                row.get("record_status", ""),
            ]
            for col, value in enumerate(values):
                self.records_table.setItem(index, col, QtWidgets.QTableWidgetItem(str(value)))

    def _group_prescriptions(self):
        grouped = {}
        for row in self.prescriptions:
            key = row.get("record_id") or row.get("prescription_id")
            group = grouped.setdefault(
                key,
                {"record_id": key, "medicines": [], "quantity": 0, "statuses": set()},
            )
            name = row.get("name") or row.get("medicine_name") or "Thuốc chưa rõ"
            try:
                quantity = int(row.get("quantity") or 0)
            except (TypeError, ValueError):
                quantity = 0
            group["medicines"].append(f"{name} x{quantity}")
            group["quantity"] += quantity
            group["statuses"].add(str(row.get("status") or "draft"))
        return list(grouped.values())

    def _render_prescriptions(self):
        rows = self._group_prescriptions()
        self.prescriptions_table.setRowCount(len(rows))
        for index, row in enumerate(rows):
            values = [
                row.get("record_id", ""),
                ", ".join(row.get("medicines", [])),
                row.get("quantity", ""),
                ", ".join(sorted(row.get("statuses", []))),
            ]
            for col, value in enumerate(values):
                self.prescriptions_table.setItem(index, col, QtWidgets.QTableWidgetItem(str(value)))

    def _render_appointments(self):
        self.appointments_table.setRowCount(len(self.appointments))
        for index, row in enumerate(self.appointments):
            for col, value in enumerate([row.get("appointment_date", ""), row.get("doctor_name", ""), row.get("status", ""), row.get("note", "")]):
                self.appointments_table.setItem(index, col, QtWidgets.QTableWidgetItem(str(value)))

    def _latest_actionable_appointment_id(self):
        for row in self.appointments:
            if AppointmentController.can_start_exam(row.get("status")) and str(row.get("doctor_id")) == str(self.doctor_id):
                return row.get("appointment_id")
        return None

    def _open_exam_with_context(self):
        appointment_id = self._latest_actionable_appointment_id()
        return self._switch_page(3, appointment_id=appointment_id)

    def _open_prescription_with_context(self):
        record_id = self.selected_record.get("record_id") if self.selected_record else None
        return self._switch_page(5, record_id=record_id, patient_id=self.patient_id)

    def _print_record(self):
        QtWidgets.QMessageBox.information(self, "In hồ sơ", "Chức năng in/xuất PDF hồ sơ bệnh nhân chưa được triển khai.")

    def _switch_page(self, index, appointment_id=None, record_id=None, patient_id=None):
        parent = self.parent()
        while parent and not hasattr(parent, "switch_page"):
            parent = parent.parent()
        if not parent:
            return False

        target = parent.content_stack.widget(index) if hasattr(parent, "content_stack") and parent.content_stack.count() > index else None
        if appointment_id and hasattr(target, "set_appointment"):
            target.set_appointment(appointment_id)
        if record_id and hasattr(target, "set_record"):
            target.set_record(record_id)
        if patient_id and hasattr(target, "set_patient"):
            target.set_patient(patient_id)
        parent.switch_page(index)
        return True
