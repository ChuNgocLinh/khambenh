from PyQt6 import QtWidgets, QtCore, QtGui
from controllers.patient_controller import PatientController
from controllers.doctor_controller import DoctorController

class PatientManagementView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        
        # Header
        title = QtWidgets.QLabel("Quản lý Bệnh nhân")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        # Toolbar
        toolbar = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm theo tên hoặc SĐT...")
        self.search_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #ddd; font-size: 14px;")
        toolbar.addWidget(self.search_input)

        self.btn_search = QtWidgets.QPushButton("🔍 Tìm kiếm")
        self.btn_search.setStyleSheet("background: #f1f5f9; padding: 8px 15px; border-radius: 5px; font-weight: bold; color: #333;")
        self.btn_search.clicked.connect(self.load_data)
        toolbar.addWidget(self.btn_search)

        toolbar.addStretch()
        
        self.btn_add = QtWidgets.QPushButton("➕ Thêm mới")
        self.btn_add.setStyleSheet("background: #69c0a5; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold;")
        # self.btn_add.clicked.connect(...)
        toolbar.addWidget(self.btn_add)
        
        layout.addLayout(toolbar)

        # Table
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Họ tên", "Ngày sinh", "Giới tính", "SĐT", "Địa chỉ", "Hành động"])
        self.table.setStyleSheet("""
            QTableWidget { border: 1px solid #e2e8f0; border-radius: 10px; background: white; font-size: 14px; color: #333; }
            QHeaderView::section { background-color: #f8fafc; padding: 12px; font-weight: bold; border: none; border-bottom: 2px solid #e2e8f0; color: #1e293b; }
            QTableWidget::item { padding: 10px; border-bottom: 1px solid #f1f5f9; }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(6, 120)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        patients = PatientController.get_all()
        query = self.search_input.text().lower()
        if query:
            patients = [p for p in patients if query in str(p.get("name", "")).lower() or query in str(p.get("phone", ""))]
            
        self.table.setRowCount(len(patients))
        for row, p in enumerate(patients):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(p["patient_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(p.get("name", ""))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(p.get("dob", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(p.get("gender", ""))))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(p.get("phone", ""))))
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(p.get("address", ""))))
            
            # Action buttons
            action_widget = QtWidgets.QWidget()
            action_layout = QtWidgets.QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 5, 5, 5)
            
            btn_edit = QtWidgets.QPushButton("Sửa")
            btn_edit.setStyleSheet("background-color: #f0f9ff; color: #0284c7; border: 1px solid #bae6fd; border-radius: 4px; padding: 4px 8px;")
            
            btn_del = QtWidgets.QPushButton("Xóa")
            btn_del.setStyleSheet("background-color: #fef2f2; color: #ef4444; border: 1px solid #fecaca; border-radius: 4px; padding: 4px 8px;")
            
            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_del)
            self.table.setCellWidget(row, 6, action_widget)


class DoctorManagementView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        
        # Header
        title = QtWidgets.QLabel("Quản lý Bác sĩ")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        # Toolbar
        toolbar = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm theo tên, chuyên khoa...")
        self.search_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #ddd; font-size: 14px;")
        toolbar.addWidget(self.search_input)

        self.btn_search = QtWidgets.QPushButton("🔍 Tìm kiếm")
        self.btn_search.setStyleSheet("background: #f1f5f9; padding: 8px 15px; border-radius: 5px; font-weight: bold; color: #333;")
        self.btn_search.clicked.connect(self.load_data)
        toolbar.addWidget(self.btn_search)

        toolbar.addStretch()
        
        self.btn_add = QtWidgets.QPushButton("➕ Thêm Bác sĩ")
        self.btn_add.setStyleSheet("background: #69c0a5; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold;")
        # self.btn_add.clicked.connect(...)
        toolbar.addWidget(self.btn_add)
        
        layout.addLayout(toolbar)

        # Table
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Họ tên", "Chuyên khoa", "SĐT", "Email", "Hành động"])
        self.table.setStyleSheet("""
            QTableWidget { border: 1px solid #e2e8f0; border-radius: 10px; background: white; font-size: 14px; color: #333; }
            QHeaderView::section { background-color: #f8fafc; padding: 12px; font-weight: bold; border: none; border-bottom: 2px solid #e2e8f0; color: #1e293b; }
            QTableWidget::item { padding: 10px; border-bottom: 1px solid #f1f5f9; }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(5, 120)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        doctors = DoctorController.get_all()
        query = self.search_input.text().lower()
        if query:
            doctors = [d for d in doctors if query in str(d.get("name", "")).lower() or query in str(d.get("specialty", "")).lower()]
            
        self.table.setRowCount(len(doctors))
        for row, d in enumerate(doctors):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(d["doctor_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(d.get("name", ""))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(d.get("specialty", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(d.get("phone", ""))))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(d.get("email", ""))))
            
            # Action buttons
            action_widget = QtWidgets.QWidget()
            action_layout = QtWidgets.QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 5, 5, 5)
            
            btn_edit = QtWidgets.QPushButton("Sửa")
            btn_edit.setStyleSheet("background-color: #f0f9ff; color: #0284c7; border: 1px solid #bae6fd; border-radius: 4px; padding: 4px 8px;")
            
            btn_del = QtWidgets.QPushButton("Xóa")
            btn_del.setStyleSheet("background-color: #fef2f2; color: #ef4444; border: 1px solid #fecaca; border-radius: 4px; padding: 4px 8px;")
            
            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_del)
            self.table.setCellWidget(row, 5, action_widget)
