from PyQt6 import QtWidgets, QtCore, QtGui
from controllers.medical_record_controller import MedicalRecordController
from controllers.prescription_controller import PrescriptionController

class MedicalRecordView(QtWidgets.QWidget):
    def __init__(self, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        layout = QtWidgets.QVBoxLayout(self)
        
        # Header
        title = QtWidgets.QLabel("Quản lý Hồ sơ Bệnh án")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        # Toolbar
        toolbar = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm theo ID Bệnh nhân...")
        self.search_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #ddd; font-size: 14px;")
        toolbar.addWidget(self.search_input)

        self.btn_search = QtWidgets.QPushButton("🔍 Tìm kiếm")
        self.btn_search.setStyleSheet("background: #f1f5f9; padding: 8px 15px; border-radius: 5px; font-weight: bold; color: #333;")
        self.btn_search.clicked.connect(self.load_data)
        toolbar.addWidget(self.btn_search)

        toolbar.addStretch()
        
        self.btn_add = QtWidgets.QPushButton("➕ Tạo Hồ sơ mới")
        self.btn_add.setStyleSheet("background: #69c0a5; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold;")
        toolbar.addWidget(self.btn_add)
        
        layout.addLayout(toolbar)

        # Table
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID Hồ sơ", "ID Bệnh nhân", "ID Lịch hẹn", "Chẩn đoán", "Điều trị"])
        self.table.setStyleSheet("""
            QTableWidget { border: 1px solid #e2e8f0; border-radius: 10px; background: white; font-size: 14px; color: #333; }
            QHeaderView::section { background-color: #f8fafc; padding: 12px; font-weight: bold; border: none; border-bottom: 2px solid #e2e8f0; color: #1e293b; }
            QTableWidget::item { padding: 10px; border-bottom: 1px solid #f1f5f9; }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        layout.addWidget(self.table)
        
        # Load data would require fetching all records, but our controller has get_by_patient
        # For simplicity, we just leave it empty until user searches

    def load_data(self):
        patient_id = self.search_input.text()
        if not patient_id.isdigit():
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID bệnh nhân là số")
            return
            
        records = MedicalRecordController.get_by_patient(int(patient_id))
        self.table.setRowCount(len(records))
        for row, r in enumerate(records):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(r["record_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(r["patient_id"])))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(r["appointment_id"])))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(r.get("diagnosis", ""))))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(r.get("treatment", ""))))

class PrescriptionView(QtWidgets.QWidget):
    def __init__(self, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        layout = QtWidgets.QVBoxLayout(self)
        
        # Header
        title = QtWidgets.QLabel("Quản lý Đơn thuốc")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        # Toolbar
        toolbar = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm theo ID Hồ sơ...")
        self.search_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #ddd; font-size: 14px;")
        toolbar.addWidget(self.search_input)

        self.btn_search = QtWidgets.QPushButton("🔍 Tìm kiếm")
        self.btn_search.setStyleSheet("background: #f1f5f9; padding: 8px 15px; border-radius: 5px; font-weight: bold; color: #333;")
        self.btn_search.clicked.connect(self.load_data)
        toolbar.addWidget(self.btn_search)

        toolbar.addStretch()
        
        self.btn_add = QtWidgets.QPushButton("➕ Kê đơn mới")
        self.btn_add.setStyleSheet("background: #69c0a5; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold;")
        toolbar.addWidget(self.btn_add)
        
        layout.addLayout(toolbar)

        # Table
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Đơn thuốc", "Tên thuốc", "Số lượng", "Hành động"])
        self.table.setStyleSheet("""
            QTableWidget { border: 1px solid #e2e8f0; border-radius: 10px; background: white; font-size: 14px; color: #333; }
            QHeaderView::section { background-color: #f8fafc; padding: 12px; font-weight: bold; border: none; border-bottom: 2px solid #e2e8f0; color: #1e293b; }
            QTableWidget::item { padding: 10px; border-bottom: 1px solid #f1f5f9; }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        layout.addWidget(self.table)

    def load_data(self):
        record_id = self.search_input.text()
        if not record_id.isdigit():
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID Hồ sơ là số")
            return
            
        items = PrescriptionController.get_by_record(int(record_id))
        self.table.setRowCount(len(items))
        for row, item in enumerate(items):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item["prescription_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(item.get("name", ""))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item.get("quantity", ""))))
            
            btn_del = QtWidgets.QPushButton("Xóa")
            btn_del.setStyleSheet("background-color: #fef2f2; color: #ef4444; border: 1px solid #fecaca; border-radius: 4px; padding: 4px 8px;")
            self.table.setCellWidget(row, 3, btn_del)
