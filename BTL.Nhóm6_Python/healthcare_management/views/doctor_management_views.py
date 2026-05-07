from PyQt6 import QtWidgets, QtCore
from controllers.medical_record_controller import MedicalRecordController
from controllers.prescription_controller import PrescriptionController
from controllers.appointment_controller import AppointmentController
from controllers.patient_controller import PatientController
from controllers.medicine_controller import MedicineController

class BaseDoctorView(QtWidgets.QWidget):
    def __init__(self, title_text, headers, doctor_id, parent=None):
        super().__init__(parent)
        self.doctor_id = doctor_id
        self.layout = QtWidgets.QVBoxLayout(self)
        
        title = QtWidgets.QLabel(title_text)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        self.layout.addWidget(title)
        
        toolbar = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm...")
        self.search_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #ddd; font-size: 14px;")
        toolbar.addWidget(self.search_input)
        
        self.btn_search = QtWidgets.QPushButton("🔍 Tìm kiếm")
        self.btn_search.setStyleSheet("background: #f1f5f9; padding: 8px 15px; border-radius: 5px; font-weight: bold;")
        self.btn_search.clicked.connect(self.load_data)
        toolbar.addWidget(self.btn_search)
        
        toolbar.addStretch()
        
        self.btn_add = QtWidgets.QPushButton("➕ Thêm mới")
        self.btn_add.setStyleSheet("background: #69c0a5; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold;")
        self.btn_add.clicked.connect(self.add_new)
        toolbar.addWidget(self.btn_add)
        
        self.layout.addLayout(toolbar)
        
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setStyleSheet("""
            QTableWidget { border: 1px solid #e2e8f0; border-radius: 10px; background: white; font-size: 14px; color: #333; }
            QHeaderView::section { background-color: #f8fafc; padding: 12px; font-weight: bold; border: none; border-bottom: 2px solid #e2e8f0; }
            QTableWidget::item { padding: 10px; border-bottom: 1px solid #f1f5f9; }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.layout.addWidget(self.table)
        
    def load_data(self):
        pass
        
    def add_new(self):
        pass


class MedicalRecordDialog(QtWidgets.QDialog):
    def __init__(self, doctor_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tạo Bệnh Án")
        self.setMinimumWidth(400)
        self.doctor_id = doctor_id
        
        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        
        self.appt_combo = QtWidgets.QComboBox()
        # Load pending/in-progress appointments for this doctor
        self.appts = AppointmentController.get_by_doctor(self.doctor_id)
        for a in self.appts:
            if a["status"] in ["pending", "in_progress", "confirmed"]:
                self.appt_combo.addItem(f"{a['appointment_id']} - {a['patient_name']} ({a['appointment_date']})", a)
                
        self.diag_input = QtWidgets.QTextEdit()
        self.treat_input = QtWidgets.QTextEdit()
        
        form.addRow("Chọn Lịch Hẹn:", self.appt_combo)
        form.addRow("Chẩn đoán:", self.diag_input)
        form.addRow("Điều trị:", self.treat_input)
        
        layout.addLayout(form)
        
        btn_layout = QtWidgets.QHBoxLayout()
        save_btn = QtWidgets.QPushButton("Lưu Bệnh Án")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QtWidgets.QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn); btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
    def get_data(self):
        appt = self.appt_combo.currentData()
        return {
            "patient_id": appt["patient_id"] if appt else None,
            "appointment_id": appt["appointment_id"] if appt else None,
            "diagnosis": self.diag_input.toPlainText(),
            "treatment": self.treat_input.toPlainText()
        }


class PrescriptionDialog(QtWidgets.QDialog):
    def __init__(self, record_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kê Đơn Thuốc")
        self.setMinimumWidth(400)
        self.record_id = record_id
        
        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        
        self.med_combo = QtWidgets.QComboBox()
        self.meds = MedicineController.get_all()
        for m in self.meds:
            if m.get("is_active", True) and m.get("quantity", 0) > 0:
                self.med_combo.addItem(f"{m['name']} (Còn: {m['quantity']})", m)
                
        self.qty_input = QtWidgets.QSpinBox()
        self.qty_input.setMinimum(1)
        self.qty_input.setMaximum(100)
        
        form.addRow("Chọn Thuốc:", self.med_combo)
        form.addRow("Số lượng:", self.qty_input)
        
        layout.addLayout(form)
        
        btn_layout = QtWidgets.QHBoxLayout()
        save_btn = QtWidgets.QPushButton("Thêm")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QtWidgets.QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn); btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
    def get_data(self):
        med = self.med_combo.currentData()
        return {
            "record_id": self.record_id,
            "medicine_id": med["medicine_id"] if med else None,
            "quantity": self.qty_input.value()
        }


class MedicalRecordView(BaseDoctorView):
    def __init__(self, doctor_id):
        super().__init__("Hồ sơ Bệnh Án", ["ID", "Ngày Khám", "Bệnh Nhân", "Chẩn Đoán", "Điều Trị", "Hành động"], doctor_id)
        self.load_data()

    def load_data(self):
        # We need to get all records for this doctor. The model currently gets by patient.
        # So we fetch all appointments for doctor, then get records. 
        # For simplicity, we just fetch all appointments and their records or use a direct query.
        from database.db import fetch_all
        records = fetch_all("SELECT r.*, p.name as patient_name FROM MedicalRecords r JOIN Patients p ON r.patient_id = p.patient_id WHERE r.doctor_id = ?", (self.doctor_id,))
        
        query = self.search_input.text().lower()
        if query:
            records = [r for r in records if query in str(r.get("patient_name", "")).lower() or query in str(r.get("diagnosis", "")).lower()]
            
        self.table.setRowCount(len(records))
        for row, r in enumerate(records):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(r["record_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(r.get("created_at", ""))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(r.get("patient_name", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(r.get("diagnosis", ""))))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(r.get("treatment", ""))))
            
            btn_presc = QtWidgets.QPushButton("Kê đơn")
            btn_presc.clicked.connect(lambda _, r_id=r["record_id"]: self.add_prescription(r_id))
            self.table.setCellWidget(row, 5, btn_presc)

    def add_new(self):
        dialog = MedicalRecordDialog(self.doctor_id, self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data["patient_id"]:
                MedicalRecordController.create(data["patient_id"], self.doctor_id, data["appointment_id"], data["diagnosis"], data["treatment"])
                # Mark appt as done
                AppointmentController.update_status(data["appointment_id"], "done")
                self.load_data()
                
    def add_prescription(self, record_id):
        dialog = PrescriptionDialog(record_id, self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data["medicine_id"]:
                PrescriptionController.add(data["record_id"], data["medicine_id"], data["quantity"])
                QtWidgets.QMessageBox.information(self, "Thành công", "Đã kê đơn thuốc thành công!")


class PrescriptionView(BaseDoctorView):
    def __init__(self, doctor_id):
        super().__init__("Quản lý Đơn Thuốc", ["ID Đơn", "ID Bệnh Án", "Bệnh Nhân", "Thuốc", "Số Lượng"], doctor_id)
        self.btn_add.hide()
        self.load_data()

    def load_data(self):
        from database.db import fetch_all
        presc = fetch_all("""
            SELECT pr.*, m.name as med_name, p.name as patient_name
            FROM Prescriptions pr
            JOIN MedicalRecords mr ON pr.record_id = mr.record_id
            JOIN Patients p ON mr.patient_id = p.patient_id
            JOIN Medicines m ON pr.medicine_id = m.medicine_id
            WHERE mr.doctor_id = ?
        """, (self.doctor_id,))
        
        self.table.setRowCount(len(presc))
        for row, p in enumerate(presc):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(p["prescription_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(p["record_id"])))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(p.get("patient_name", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(p.get("med_name", ""))))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(p.get("quantity", ""))))


class DoctorPatientListView(BaseDoctorView):
    def __init__(self, doctor_id):
        super().__init__("Danh Sách Bệnh Nhân", ["ID Bệnh Nhân", "Họ Tên", "Ngày Sinh", "SĐT", "Lượt Khám"], doctor_id)
        self.btn_add.hide()
        self.load_data()

    def load_data(self):
        from database.db import fetch_all
        patients = fetch_all("""
            SELECT p.patient_id, p.name, p.dob, p.phone, COUNT(a.appointment_id) as visits
            FROM Patients p
            JOIN Appointments a ON p.patient_id = a.patient_id
            WHERE a.doctor_id = ? AND a.status IN ('done', 'completed')
            GROUP BY p.patient_id, p.name, p.dob, p.phone
        """, (self.doctor_id,))
        
        self.table.setRowCount(len(patients))
        for row, p in enumerate(patients):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(p["patient_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(p.get("name", ""))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(p.get("dob", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(p.get("phone", ""))))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(p.get("visits", "1"))))


class DoctorAppointmentView(BaseDoctorView):
    def __init__(self, doctor_id):
        super().__init__("Tất Cả Lịch Hẹn", ["ID", "Ngày Khám", "Bệnh Nhân", "SĐT", "Trạng Thái"], doctor_id)
        self.btn_add.hide()
        self.load_data()

    def load_data(self):
        from database.db import fetch_all
        appts = fetch_all("""
            SELECT a.appointment_id, a.appointment_date, a.status, p.name, p.phone
            FROM Appointments a
            JOIN Patients p ON a.patient_id = p.patient_id
            WHERE a.doctor_id = ?
            ORDER BY a.appointment_date DESC
        """, (self.doctor_id,))
        
        self.table.setRowCount(len(appts))
        for row, a in enumerate(appts):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(a["appointment_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(a.get("appointment_date", ""))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(a.get("name", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(a.get("phone", ""))))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(a.get("status", "pending"))))
