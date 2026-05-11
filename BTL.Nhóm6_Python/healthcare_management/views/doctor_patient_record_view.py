from PyQt6 import QtCore, QtWidgets

from controllers.appointment_controller import AppointmentController
from controllers.medical_record_controller import MedicalRecordController
from controllers.patient_controller import PatientController
from controllers.prescription_controller import PrescriptionController
from views.doctor_ui_utils import PAGE_BG, age_from_dob, avatar, badge, button, card, input_style, page_title, parse_datetime, table_style


class DoctorPatientRecordView(QtWidgets.QWidget):
    def __init__(self, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        self.patient_id = None
        self.patient = None
        self.records = []
        self.prescriptions = []
        self.appointments = []
        self.selected_record = None
        self.setStyleSheet(f"background: {PAGE_BG};")

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(14)
        root.addWidget(page_title("Hồ sơ bệnh nhân", "Trang chủ  >  Hồ sơ bệnh nhân  >  Chi tiết hồ sơ"))
        root.addWidget(self._build_profile_card())
        root.addWidget(self._build_tabs(), 1)
        root.addLayout(self._build_actions())

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
        info.addWidget(self.title_label)
        info.addWidget(self.summary_label)
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

        self.records_table = self._table(["Ngày", "Chẩn đoán", "Điều trị", "Trạng thái"])
        self.prescriptions_table = self._table(["Mã đơn", "Thuốc", "Số lượng", "Trạng thái"])
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
        self.history_search.setPlaceholderText("Tìm kiếm lịch sử khám...")
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
        self.metric_label = QtWidgets.QLabel("Tổng số lần khám: 0\nTổng đơn thuốc: 0\nTổng lịch hẹn: 0")
        self.metric_label.setStyleSheet("color: #475467; font-size: 13px;")
        layout.addWidget(QtWidgets.QLabel("Tóm tắt hồ sơ"))
        layout.addWidget(self.metric_label)
        layout.addWidget(badge("Bệnh mãn tính: Chưa cập nhật", "#F79009", "#FFF7ED"))
        layout.addWidget(badge("Dị ứng: Chưa cập nhật", "#F04438", "#FEF3F2"))
        for text, page in [("Tạo lịch hẹn", 1), ("Khám bệnh", 3), ("Kê đơn thuốc", 5), ("In hồ sơ", None)]:
            btn = button(text, "outline")
            if page is not None:
                btn.clicked.connect(lambda checked=False, p=page: self._switch_page(p))
            layout.addWidget(btn)
        layout.addStretch()
        return wrapper

    def _build_actions(self):
        actions = QtWidgets.QHBoxLayout()
        self.open_exam_btn = button("Khám bệnh", "outline")
        self.open_prescription_btn = button("Tạo đơn thuốc", "outline")
        self.refresh_btn = button("Làm mới", "primary")
        self.open_exam_btn.clicked.connect(lambda: self._switch_page(3))
        self.open_prescription_btn.clicked.connect(lambda: self._switch_page(5))
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

    def set_patient(self, patient_id):
        self.patient_id = patient_id
        self.load_data()

    def load_data(self):
        if not self.patient_id:
            self._render_empty("Chọn bệnh nhân để xem hồ sơ.")
            return
        try:
            self.patient = PatientController.get_by_id(self.patient_id)
        except AttributeError:
            from models.patient_model import PatientModel

            self.patient = PatientModel.get_by_id(self.patient_id)
        except Exception:
            self.patient = None
        try:
            self.records = MedicalRecordController.get_by_patient(self.patient_id) or []
        except Exception:
            self.records = []
        try:
            self.appointments = AppointmentController.get_by_patient(self.patient_id) or []
        except Exception:
            self.appointments = []
        self.prescriptions = []
        for record in self.records:
            try:
                self.prescriptions.extend(PrescriptionController.get_by_record(record.get("record_id")) or [])
            except Exception:
                continue
        self._render()

    def _render_empty(self, message):
        self.summary_label.setText(message)
        self.title_label.setText("Hồ sơ bệnh nhân")
        self.records_table.setRowCount(0)
        self.prescriptions_table.setRowCount(0)
        self.appointments_table.setRowCount(0)
        self._render_visit_cards()
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
            f"Giới tính: {self.patient.get('gender', '')} | "
            f"Ngày sinh: {self.patient.get('dob', '')} ({age_from_dob(self.patient.get('dob')) or 'Chưa rõ tuổi'}) | "
            f"SĐT: {self.patient.get('phone', '')}\n"
            f"Email: {self.patient.get('email') or 'Chưa cập nhật'} | Địa chỉ: {self.patient.get('address') or 'Chưa cập nhật'}"
        )
        self.profile_side.setText("Nhóm máu: Chưa cập nhật\nNghề nghiệp: Chưa cập nhật\nBHYT: Chưa cập nhật\nNgười liên hệ: Chưa cập nhật")
        self.metric_label.setText(
            f"Tổng số lần khám: {len(self.records)}\nTổng đơn thuốc: {len(self.prescriptions)}\nTổng lịch hẹn: {len(self.appointments)}"
        )
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
        rows = [
            row for row in self.records if not keyword or keyword in f"{row.get('created_at', '')} {row.get('diagnosis', '')} {row.get('treatment', '')}".lower()
        ]
        if not rows:
            empty = QtWidgets.QLabel("Chưa có lịch sử khám.")
            empty.setStyleSheet("color: #667085;")
            self.visit_list.addWidget(empty)
            self.visit_list.addStretch()
            return
        for row in rows:
            btn = QtWidgets.QPushButton(
                f"{row.get('created_at', 'Chưa rõ ngày')}\n{row.get('diagnosis') or 'Chưa có chẩn đoán'}"
            )
            btn.setMinimumHeight(72)
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(
                "QPushButton { text-align: left; background: white; color: #344054; border: 1px solid #EAECF0; "
                "border-radius: 12px; padding: 10px; font-weight: 700; } QPushButton:hover { background: #F9FAFB; }"
            )
            btn.clicked.connect(lambda checked=False, r=row: self._select_record(r))
            self.visit_list.addWidget(btn)
        self.visit_list.addStretch()

    def _select_record(self, row):
        self.selected_record = row
        dt = parse_datetime(row.get("created_at"))
        self.visit_detail_title.setText(f"Chi tiết lần khám - {dt.strftime('%d/%m/%Y') if dt else row.get('created_at', '')}")
        self.visit_detail_body.setText(
            f"Lý do khám: {row.get('reason') or 'Chưa cập nhật'}\n"
            f"Triệu chứng: {row.get('symptoms') or 'Chưa cập nhật'}\n\n"
            "Khám lâm sàng:\n"
            f"- Mạch: {row.get('pulse') or 'Chưa cập nhật'}\n"
            f"- Huyết áp: {row.get('blood_pressure') or 'Chưa cập nhật'}\n"
            f"- Nhiệt độ: {row.get('temperature') or 'Chưa cập nhật'}\n\n"
            f"Chẩn đoán: {row.get('diagnosis') or 'Chưa cập nhật'}\n"
            f"Kết luận/Hướng điều trị: {row.get('treatment') or 'Chưa cập nhật'}\n"
            f"Trạng thái: {row.get('record_status') or 'Chưa cập nhật'}"
        )

    def _render_records(self):
        self.records_table.setRowCount(len(self.records))
        for index, row in enumerate(self.records):
            for col, value in enumerate([row.get("created_at", ""), row.get("diagnosis", ""), row.get("treatment", ""), row.get("record_status", "")]):
                self.records_table.setItem(index, col, QtWidgets.QTableWidgetItem(str(value)))

    def _render_prescriptions(self):
        self.prescriptions_table.setRowCount(len(self.prescriptions))
        for index, row in enumerate(self.prescriptions):
            for col, value in enumerate([row.get("prescription_id", ""), row.get("name") or row.get("medicine_name", ""), row.get("quantity", ""), row.get("status", "")]):
                self.prescriptions_table.setItem(index, col, QtWidgets.QTableWidgetItem(str(value)))

    def _render_appointments(self):
        self.appointments_table.setRowCount(len(self.appointments))
        for index, row in enumerate(self.appointments):
            for col, value in enumerate([row.get("appointment_date", ""), row.get("doctor_name", ""), row.get("status", ""), row.get("note", "")]):
                self.appointments_table.setItem(index, col, QtWidgets.QTableWidgetItem(str(value)))

    def _switch_page(self, index):
        parent = self.parent()
        while parent and not hasattr(parent, "switch_page"):
            parent = parent.parent()
        if parent:
            parent.switch_page(index)
