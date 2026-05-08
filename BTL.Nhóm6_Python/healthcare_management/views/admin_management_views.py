from PyQt6 import QtWidgets, QtCore
from controllers.patient_controller import PatientController
from controllers.doctor_controller import DoctorController
from controllers.appointment_controller import AppointmentController
from controllers.medicine_controller import MedicineController
from controllers.service_controller import ServiceController
from controllers.payment_controller import PaymentController

# ==========================================
# CÁC DIALOG THÊM / SỬA
# ==========================================
class PatientDialog(QtWidgets.QDialog):
    def __init__(self, patient=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Bệnh Nhân" if not patient else "Sửa Bệnh Nhân")
        self.setMinimumWidth(400)
        self.patient = patient
        
        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        
        self.name_input = QtWidgets.QLineEdit(patient.get('name', '') if patient else '')
        self.dob_input = QtWidgets.QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.gender_input = QtWidgets.QComboBox()
        self.gender_input.addItems(["Nam", "Nữ"])
        if patient: self.gender_input.setCurrentText(patient.get('gender', 'Nam'))
        
        self.phone_input = QtWidgets.QLineEdit(patient.get('phone', '') if patient else '')
        self.address_input = QtWidgets.QLineEdit(patient.get('address', '') if patient else '')
        
        form.addRow("Họ tên:", self.name_input)
        form.addRow("Ngày sinh:", self.dob_input)
        form.addRow("Giới tính:", self.gender_input)
        form.addRow("SĐT:", self.phone_input)
        form.addRow("Địa chỉ:", self.address_input)
        
        layout.addLayout(form)
        
        btn_layout = QtWidgets.QHBoxLayout()
        save_btn = QtWidgets.QPushButton("Lưu")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QtWidgets.QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn); btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
    def get_data(self):
        return {
            "name": self.name_input.text(),
            "dob": self.dob_input.date().toString("yyyy-MM-dd"),
            "gender": self.gender_input.currentText(),
            "phone": self.phone_input.text(),
            "address": self.address_input.text()
        }

class DoctorDialog(QtWidgets.QDialog):
    def __init__(self, doctor=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Bác Sĩ" if not doctor else "Sửa Bác Sĩ")
        self.setMinimumWidth(400)
        self.doctor = doctor
        
        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        
        self.name_input = QtWidgets.QLineEdit(doctor.get('name', '') if doctor else '')
        self.specialty_input = QtWidgets.QLineEdit(doctor.get('specialty', '') if doctor else '')
        self.phone_input = QtWidgets.QLineEdit(doctor.get('phone', '') if doctor else '')
        
        form.addRow("Họ tên:", self.name_input)
        form.addRow("Chuyên khoa:", self.specialty_input)
        form.addRow("SĐT:", self.phone_input)
        
        layout.addLayout(form)
        
        btn_layout = QtWidgets.QHBoxLayout()
        save_btn = QtWidgets.QPushButton("Lưu")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QtWidgets.QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn); btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
    def get_data(self):
        return {
            "name": self.name_input.text(),
            "specialty": self.specialty_input.text(),
            "phone": self.phone_input.text()
        }

class MedicineDialog(QtWidgets.QDialog):
    def __init__(self, medicine=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Thuốc" if not medicine else "Sửa Thuốc")
        self.setMinimumWidth(400)
        self.medicine = medicine
        
        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        
        self.name_input = QtWidgets.QLineEdit(medicine.get('name', '') if medicine else '')
        self.qty_input = QtWidgets.QSpinBox()
        self.qty_input.setMaximum(10000)
        if medicine: self.qty_input.setValue(int(medicine.get('quantity', 0)))
        
        self.price_input = QtWidgets.QDoubleSpinBox()
        self.price_input.setMaximum(100000000)
        if medicine: self.price_input.setValue(float(medicine.get('price', 0)))
        
        self.desc_input = QtWidgets.QLineEdit(medicine.get('description', '') if medicine else '')
        
        form.addRow("Tên thuốc:", self.name_input)
        form.addRow("Số lượng:", self.qty_input)
        form.addRow("Giá:", self.price_input)
        form.addRow("Mô tả:", self.desc_input)
        
        layout.addLayout(form)
        
        btn_layout = QtWidgets.QHBoxLayout()
        save_btn = QtWidgets.QPushButton("Lưu")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QtWidgets.QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn); btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
    def get_data(self):
        return {
            "name": self.name_input.text(),
            "quantity": self.qty_input.value(),
            "price": self.price_input.value(),
            "description": self.desc_input.text()
        }

class ServiceDialog(QtWidgets.QDialog):
    def __init__(self, service=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Dịch Vụ" if not service else "Sửa Dịch Vụ")
        self.setMinimumWidth(400)
        self.service = service
        
        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        
        self.name_input = QtWidgets.QLineEdit(service.get('service_name', '') if service else '')
        self.price_input = QtWidgets.QDoubleSpinBox()
        self.price_input.setMaximum(100000000)
        if service: self.price_input.setValue(float(service.get('price', 0)))
        self.desc_input = QtWidgets.QLineEdit(service.get('description', '') if service else '')
        
        form.addRow("Tên dịch vụ:", self.name_input)
        form.addRow("Giá:", self.price_input)
        form.addRow("Mô tả:", self.desc_input)
        
        layout.addLayout(form)
        
        btn_layout = QtWidgets.QHBoxLayout()
        save_btn = QtWidgets.QPushButton("Lưu")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QtWidgets.QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn); btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
    def get_data(self):
        return {
            "name": self.name_input.text(),
            "price": self.price_input.value(),
            "description": self.desc_input.text()
        }

# ==========================================
# CÁC VIEW QUẢN LÝ
# ==========================================

class BaseManagementView(QtWidgets.QWidget):
    def __init__(self, title_text, headers, parent=None):
        super().__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)
        
        title = QtWidgets.QLabel(title_text)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        self.layout.addWidget(title)
        
        toolbar = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm...")
        self.search_input.setStyleSheet(
            "padding: 8px; border-radius: 5px; border: 1px solid #ddd; font-size: 14px; color: #1f2937; background: white;"
        )
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

class PatientManagementView(BaseManagementView):
    def __init__(self):
        super().__init__("Quản lý Bệnh nhân", ["ID", "Họ tên", "Ngày sinh", "Giới tính", "SĐT", "Địa chỉ", "Hành động"])
        self.table.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(6, 120)
        self.load_data()

    def load_data(self):
        patients = PatientController.get_all()
        query = self.search_input.text().lower()
        if query:
            patients = [p for p in patients if query in str(p.get("name", "")).lower() or query in str(p.get("phone", ""))]
            
        self.table.setRowCount(len(patients))
        for row, p in enumerate(patients):
            if not p.get('is_active', True): continue
            
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(p["patient_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(p.get("name", ""))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(p.get("dob", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(p.get("gender", ""))))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(p.get("phone", ""))))
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(p.get("address", ""))))
            
            action_widget = QtWidgets.QWidget()
            action_layout = QtWidgets.QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 5, 5, 5)
            
            btn_edit = QtWidgets.QPushButton("Sửa")
            btn_edit.clicked.connect(lambda _, p_data=p: self.edit_patient(p_data))
            
            btn_del = QtWidgets.QPushButton("Xóa")
            btn_del.clicked.connect(lambda _, pid=p["patient_id"]: self.delete_patient(pid))
            
            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_del)
            self.table.setCellWidget(row, 6, action_widget)

    def add_new(self):
        dialog = PatientDialog(parent=self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            PatientController.create(data)
            self.load_data()
            
    def edit_patient(self, patient):
        dialog = PatientDialog(patient, self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            PatientController.update(patient["patient_id"], data)
            self.load_data()
            
    def delete_patient(self, pid):
        # Soft delete logic in controller / model is required or hard delete
        PatientController.delete(pid)
        self.load_data()


class DoctorManagementView(BaseManagementView):
    def __init__(self):
        super().__init__("Quản lý Bác sĩ", ["ID", "Họ tên", "Chuyên khoa", "SĐT", "Hành động"])
        self.table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 120)
        self.load_data()

    def load_data(self):
        doctors = DoctorController.get_all()
        query = self.search_input.text().lower()
        if query:
            doctors = [d for d in doctors if query in str(d.get("name", "")).lower()]
            
        self.table.setRowCount(len(doctors))
        for row, d in enumerate(doctors):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(d["doctor_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(d.get("name", ""))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(d.get("specialty", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(d.get("phone", ""))))
            
            action_widget = QtWidgets.QWidget()
            action_layout = QtWidgets.QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 5, 5, 5)
            
            btn_edit = QtWidgets.QPushButton("Sửa")
            btn_edit.clicked.connect(lambda _, d_data=d: self.edit_doctor(d_data))
            
            btn_del = QtWidgets.QPushButton("Xóa")
            btn_del.clicked.connect(lambda _, did=d["doctor_id"]: self.delete_doctor(did))
            
            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_del)
            self.table.setCellWidget(row, 4, action_widget)

    def add_new(self):
        dialog = DoctorDialog(parent=self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            DoctorController.create(data)
            self.load_data()
            
    def edit_doctor(self, doctor):
        dialog = DoctorDialog(doctor, self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            DoctorController.update(doctor["doctor_id"], data)
            self.load_data()
            
    def delete_doctor(self, did):
        DoctorController.delete(did)
        self.load_data()


class AppointmentManagementView(BaseManagementView):
    def __init__(self):
        super().__init__("Quản lý Lịch hẹn", ["ID", "Ngày", "Bệnh nhân", "Bác sĩ", "Trạng thái", "Thao tác"])
        self.btn_add.hide() # Admin không thêm lịch hẹn ở đây, bệnh nhân thêm
        self.load_data()

    def load_data(self):
        appts = AppointmentController.get_all()
        self.table.setRowCount(len(appts))
        for row, a in enumerate(appts):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(a["appointment_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(a.get("appointment_date", ""))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(a.get("patient_name", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(a.get("doctor_name", ""))))
            
            cb_status = QtWidgets.QComboBox()
            cb_status.addItems(["pending", "confirmed", "in_progress", "done", "cancelled"])
            cb_status.setCurrentText(str(a.get("status", "pending")))
            cb_status.currentTextChanged.connect(lambda text, a_id=a["appointment_id"]: AppointmentController.update_status(a_id, text))
            self.table.setCellWidget(row, 4, cb_status)
            
            btn_del = QtWidgets.QPushButton("Hủy lịch")
            btn_del.clicked.connect(lambda _, a_id=a["appointment_id"]: AppointmentController.update_status(a_id, "cancelled"))
            self.table.setCellWidget(row, 5, btn_del)


class MedicineManagementView(BaseManagementView):
    def __init__(self):
        super().__init__("Quản lý Thuốc", ["ID", "Tên", "Số lượng", "Giá", "Mô tả", "Hành động"])
        self.load_data()

    def load_data(self):
        meds = MedicineController.get_all()
        query = self.search_input.text().lower()
        if query: meds = [m for m in meds if query in str(m.get("name", "")).lower()]
            
        self.table.setRowCount(len(meds))
        for row, m in enumerate(meds):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(m["medicine_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(m.get("name", ""))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(m.get("quantity", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(m.get("price", ""))))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(m.get("description", ""))))
            
            action_widget = QtWidgets.QWidget()
            action_layout = QtWidgets.QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 5, 5, 5)
            
            btn_edit = QtWidgets.QPushButton("Sửa")
            btn_edit.clicked.connect(lambda _, m_data=m: self.edit_medicine(m_data))
            
            btn_del = QtWidgets.QPushButton("Xóa")
            btn_del.clicked.connect(lambda _, mid=m["medicine_id"]: self.delete_medicine(mid))
            
            action_layout.addWidget(btn_edit); action_layout.addWidget(btn_del)
            self.table.setCellWidget(row, 5, action_widget)

    def add_new(self):
        dialog = MedicineDialog(parent=self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            MedicineController.create(dialog.get_data())
            self.load_data()
            
    def edit_medicine(self, medicine):
        dialog = MedicineDialog(medicine, self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            MedicineController.update(medicine["medicine_id"], dialog.get_data())
            self.load_data()
            
    def delete_medicine(self, mid):
        MedicineController.delete(mid)
        self.load_data()


class ServiceManagementView(BaseManagementView):
    def __init__(self):
        super().__init__("Quản lý Dịch vụ", ["ID", "Tên dịch vụ", "Giá", "Mô tả", "Hành động"])
        self.load_data()

    def load_data(self):
        services = ServiceController.get_all()
        self.table.setRowCount(len(services))
        for row, s in enumerate(services):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(s["service_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(s.get("service_name", ""))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(s.get("price", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(s.get("description", ""))))
            
            action_widget = QtWidgets.QWidget()
            action_layout = QtWidgets.QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 5, 5, 5)
            
            btn_edit = QtWidgets.QPushButton("Sửa")
            btn_edit.clicked.connect(lambda _, s_data=s: self.edit_service(s_data))
            
            btn_del = QtWidgets.QPushButton("Xóa")
            btn_del.clicked.connect(lambda _, sid=s["service_id"]: self.delete_service(sid))
            
            action_layout.addWidget(btn_edit); action_layout.addWidget(btn_del)
            self.table.setCellWidget(row, 4, action_widget)

    def add_new(self):
        dialog = ServiceDialog(parent=self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            ServiceController.create(dialog.get_data())
            self.load_data()
            
    def edit_service(self, service):
        dialog = ServiceDialog(service, self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            ServiceController.update(service["service_id"], dialog.get_data())
            self.load_data()
            
    def delete_service(self, sid):
        ServiceController.delete(sid)
        self.load_data()


class PaymentManagementView(BaseManagementView):
    def __init__(self):
        super().__init__("Quản lý Doanh thu / Thanh toán", ["ID", "Lịch hẹn", "Ngày", "Tổng tiền", "Trạng thái", "Hành động"])
        self.btn_add.hide()
        self.load_data()

    def load_data(self):
        payments = PaymentController.get_all()
        self.table.setRowCount(len(payments))
        for row, p in enumerate(payments):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(p["payment_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(p.get("appointment_id", ""))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(p.get("payment_date", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(p.get("total_amount", ""))))
            
            cb_status = QtWidgets.QComboBox()
            cb_status.addItems(["unpaid", "paid"])
            cb_status.setCurrentText(str(p.get("status", "unpaid")))
            cb_status.currentTextChanged.connect(lambda text, p_id=p["payment_id"]: PaymentController.update_status(p_id, text))
            self.table.setCellWidget(row, 4, cb_status)
            
            btn_inv = QtWidgets.QPushButton("Hóa đơn")
            self.table.setCellWidget(row, 5, btn_inv)


class ReportStatsView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)
        
        title = QtWidgets.QLabel("Báo cáo Thống kê Doanh thu")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        self.layout.addWidget(title)
        
        # Stats summary
        stats_layout = QtWidgets.QHBoxLayout()
        self.total_revenue = QtWidgets.QLabel("Tổng doanh thu: 0 VND")
        self.total_revenue.setStyleSheet("font-size: 18px; font-weight: bold; color: #16a34a; background: #f0fdf4; padding: 15px; border-radius: 10px;")
        
        self.total_paid = QtWidgets.QLabel("Hóa đơn đã thanh toán: 0")
        self.total_paid.setStyleSheet("font-size: 18px; font-weight: bold; color: #2563eb; background: #eff6ff; padding: 15px; border-radius: 10px;")
        
        stats_layout.addWidget(self.total_revenue)
        stats_layout.addWidget(self.total_paid)
        stats_layout.addStretch()
        self.layout.addLayout(stats_layout)
        
        # Table
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Thanh Toán", "Ngày", "Tổng Tiền", "Trạng Thái"])
        self.table.setStyleSheet("""
            QTableWidget { border: 1px solid #e2e8f0; border-radius: 10px; background: white; font-size: 14px; color: #333; }
            QHeaderView::section { background-color: #f8fafc; padding: 12px; font-weight: bold; border: none; border-bottom: 2px solid #e2e8f0; }
            QTableWidget::item { padding: 10px; border-bottom: 1px solid #f1f5f9; }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.layout.addWidget(self.table)
        
        self.load_data()
        
    def load_data(self):
        from database.db import fetch_all
        payments = fetch_all("SELECT * FROM Payments ORDER BY payment_date DESC")
        
        self.table.setRowCount(len(payments))
        total_rev = 0
        paid_count = 0
        
        for row, p in enumerate(payments):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(p["payment_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(p.get("payment_date", ""))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(p.get("total_amount", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(p.get("status", "unpaid"))))
            
            if p.get("status") == "paid":
                total_rev += float(p.get("total_amount", 0))
                paid_count += 1
                
        self.total_revenue.setText(f"Tổng doanh thu: {total_rev:,.0f} VND")
        self.total_paid.setText(f"Hóa đơn đã thanh toán: {paid_count}")
