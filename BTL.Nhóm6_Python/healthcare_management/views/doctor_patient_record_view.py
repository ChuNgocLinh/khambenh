from PyQt6 import QtWidgets

from controllers.appointment_controller import AppointmentController
from controllers.medical_record_controller import MedicalRecordController
from controllers.patient_controller import PatientController
from controllers.prescription_controller import PrescriptionController


class DoctorPatientRecordView(QtWidgets.QWidget):
    def __init__(self, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        self.patient_id = None
        self.patient = None
        self.records = []
        self.prescriptions = []
        self.appointments = []
        self.setStyleSheet("background: #f8fbff; border: none;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.title_label = QtWidgets.QLabel("Hồ sơ bệnh nhân")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: 800; color: #0f172a;")
        layout.addWidget(self.title_label)

        self.summary_label = QtWidgets.QLabel("Chọn bệnh nhân để xem hồ sơ.")
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet("background: white; color: #1f2937; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px;")
        layout.addWidget(self.summary_label)

        self.tabs = QtWidgets.QTabWidget()
        self.records_table = self._table(["Ngày", "Chẩn đoán", "Điều trị", "Trạng thái"])
        self.prescriptions_table = self._table(["Mã đơn", "Thuốc", "Số lượng", "Trạng thái"])
        self.appointments_table = self._table(["Ngày hẹn", "Bác sĩ", "Trạng thái", "Ghi chú"])
        self.tabs.addTab(self.records_table, "Lịch sử khám")
        self.tabs.addTab(self.prescriptions_table, "Đơn thuốc")
        self.tabs.addTab(self.appointments_table, "Lịch hẹn")
        layout.addWidget(self.tabs, 1)

        actions = QtWidgets.QHBoxLayout()
        self.open_exam_btn = QtWidgets.QPushButton("Khám bệnh")
        self.open_prescription_btn = QtWidgets.QPushButton("Tạo đơn thuốc")
        self.refresh_btn = QtWidgets.QPushButton("Làm mới")
        for button in [self.open_exam_btn, self.open_prescription_btn, self.refresh_btn]:
            button.setMinimumHeight(40)
            actions.addWidget(button)
        actions.addStretch()
        layout.addLayout(actions)

        self.open_exam_btn.clicked.connect(lambda: self._switch_page(3))
        self.open_prescription_btn.clicked.connect(lambda: self._switch_page(5))
        self.refresh_btn.clicked.connect(self.load_data)

    def _table(self, headers):
        table = QtWidgets.QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        return table

    def set_patient(self, patient_id):
        self.patient_id = patient_id
        self.load_data()

    def load_data(self):
        if not self.patient_id:
            self._render_empty("Chọn bệnh nhân để xem hồ sơ.")
            return

        self.patient = PatientController.find_by_cccd_or_phone() if False else None
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
            record_id = record.get("record_id")
            try:
                self.prescriptions.extend(PrescriptionController.get_by_record(record_id) or [])
            except Exception:
                continue

        self._render()

    def _render_empty(self, message):
        self.summary_label.setText(message)
        for table in [self.records_table, self.prescriptions_table, self.appointments_table]:
            table.setRowCount(0)

    def _render(self):
        if not self.patient:
            self._render_empty("Không tìm thấy bệnh nhân.")
            return

        self.summary_label.setText(
            f"{self.patient.get('name', '')}\n"
            f"Mã BN: BN{int(self.patient.get('patient_id') or 0):06d} | "
            f"Giới tính: {self.patient.get('gender', '')} | "
            f"Ngày sinh: {self.patient.get('dob', '')} | "
            f"SĐT: {self.patient.get('phone', '')}\n"
            f"Địa chỉ: {self.patient.get('address', '') or 'Chưa cập nhật'}"
        )
        self._render_records()
        self._render_prescriptions()
        self._render_appointments()

    def _render_records(self):
        self.records_table.setRowCount(len(self.records))
        for index, row in enumerate(self.records):
            values = [
                row.get("created_at", ""),
                row.get("diagnosis", ""),
                row.get("treatment", ""),
                row.get("record_status", ""),
            ]
            for col, value in enumerate(values):
                self.records_table.setItem(index, col, QtWidgets.QTableWidgetItem(str(value)))

    def _render_prescriptions(self):
        self.prescriptions_table.setRowCount(len(self.prescriptions))
        for index, row in enumerate(self.prescriptions):
            values = [
                row.get("prescription_id", ""),
                row.get("name") or row.get("medicine_name", ""),
                row.get("quantity", ""),
                row.get("status", ""),
            ]
            for col, value in enumerate(values):
                self.prescriptions_table.setItem(index, col, QtWidgets.QTableWidgetItem(str(value)))

    def _render_appointments(self):
        self.appointments_table.setRowCount(len(self.appointments))
        for index, row in enumerate(self.appointments):
            values = [
                row.get("appointment_date", ""),
                row.get("doctor_name", ""),
                row.get("status", ""),
                row.get("note", ""),
            ]
            for col, value in enumerate(values):
                self.appointments_table.setItem(index, col, QtWidgets.QTableWidgetItem(str(value)))

    def _switch_page(self, index):
        parent = self.parent()
        while parent and not hasattr(parent, "switch_page"):
            parent = parent.parent()
        if parent:
            parent.switch_page(index)
