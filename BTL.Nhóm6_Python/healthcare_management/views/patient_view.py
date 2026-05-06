from PyQt6 import QtWidgets, QtCore, QtGui
from controllers.appointment_controller import AppointmentController

# --- TRANG DỊCH VỤ (VIEW MỚI) ---
class ServicePage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20) # Thêm lề cho thoáng
        
        title = QtWidgets.QLabel("Danh sách dịch vụ y tế")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)

        # Bảng danh sách dịch vụ
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Tên dịch vụ", "Giá tiền", "Mô tả"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        # Style bảng cho chuyên nghiệp giống image_ade63a.png
        self.table.setStyleSheet("""
            QTableWidget { 
                background: white; border-radius: 12px; border: 1px solid #eef0f2; 
                gridline-color: #f1f5f9; font-size: 14px;
            }
            QHeaderView::section { 
                background-color: #f8f9fa; padding: 12px; font-weight: bold; 
                border: none; border-bottom: 2px solid #69c0a5; color: #1e293b;
            }
            QTableWidget::item { padding: 15px; border-bottom: 1px solid #f1f5f9; }
        """)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        
        services = [
            ("Khám tổng quát", "500,000 VND", "Kiểm tra sức khỏe toàn diện"),
            ("Xét nghiệm máu", "350,000 VND", "Tầm soát các chỉ số cơ bản"),
            ("Siêu âm ổ bụng", "400,000 VND", "Chẩn đoán hình ảnh nội soi"),
            ("Chụp X-Quang", "250,000 VND", "Kiểm tra xương khớp và phổi")
        ]
        
        self.table.setRowCount(len(services))
        for i, (name, price, desc) in enumerate(services):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(name))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(price))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(desc))
            self.table.setRowHeight(i, 50)
            
        layout.addWidget(self.table)
        layout.addStretch()

# --- TRANG CHỦ (GIỮ NGUYÊN NỘI DUNG CỦA BẠN) ---
class HomePage(QtWidgets.QWidget):
    def __init__(self, username, parent_view):
        super().__init__()
        self.username = username
        self.parent_view = parent_view 
        self.selected_time = None
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)

        # ===== HERO =====
        hero = QtWidgets.QFrame()
        hero.setStyleSheet("background: #e1f2ee; border-radius: 20px;")
        hero_layout = QtWidgets.QVBoxLayout(hero)
        hero_layout.setContentsMargins(30, 30, 30, 30)
        
        title = QtWidgets.QLabel("Chăm sóc sức khỏe chuyên nghiệp")
        title.setStyleSheet("font-size: 30px; font-weight: 800; color: #2c3e50;")
        hero_layout.addWidget(title)
        
        sub_title = QtWidgets.QLabel("Đặt lịch khám nhanh chóng với bác sĩ hàng đầu")
        sub_title.setStyleSheet("font-size: 16px; color: #64748b;")
        hero_layout.addWidget(sub_title)
        layout.addWidget(hero)

        # ===== BOOKING =====
        card = QtWidgets.QFrame()
        card.setStyleSheet("background:white; border-radius:15px; border:1px solid #eef0f2;")
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        
        row = QtWidgets.QHBoxLayout()
        self.doctor = QtWidgets.QComboBox()
        self.doctor.addItems(["BS Minh", "BS Lan"])
        self.doctor.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #ddd;")
        
        self.date = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.date.setCalendarPopup(True)
        self.date.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #ddd;")
        
        row.addWidget(self.doctor)
        row.addWidget(self.date)
        card_layout.addLayout(row)

        time_layout = QtWidgets.QHBoxLayout()
        self.buttons = []
        for t in ["08:00", "09:00", "10:00", "11:00"]:
            btn = QtWidgets.QPushButton(t)
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, b=btn: self.parent_view.select_time(b, self))
            btn.setStyleSheet("QPushButton { background:#f1f5f9; border-radius:8px; padding:12px; font-weight: bold; border: none; } QPushButton:hover { background: #e2e8f0; }")
            self.buttons.append(btn)
            time_layout.addWidget(btn)
        card_layout.addLayout(time_layout)

        book = QtWidgets.QPushButton("Đặt lịch ngay")
        book.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        book.setStyleSheet("QPushButton { background: #69c0a5; color:white; padding:12px; border-radius:10px; font-weight: 800; font-size: 15px; border: none; } QPushButton:hover { background: #58a68e; }")
        book.clicked.connect(lambda: self.parent_view.book(self))
        card_layout.addWidget(book)
        layout.addWidget(card)

        # ===== FEATURES =====
        feature_layout = QtWidgets.QHBoxLayout()
        for text in ["📅 Đặt lịch dễ dàng", "📜 Lịch sử khám", "💊 Đơn thuốc"]:
            box = QtWidgets.QFrame()
            box.setStyleSheet("background:white; border:1px solid #eef0f2; border-radius:12px;")
            v = QtWidgets.QVBoxLayout(box)
            lbl_title = QtWidgets.QLabel(text)
            lbl_title.setStyleSheet("font-weight: 800; font-size: 14px; color: #1e293b;")
            v.addWidget(lbl_title)
            v.addWidget(QtWidgets.QLabel("Mô tả chức năng chi tiết..."))
            feature_layout.addWidget(box)
        layout.addLayout(feature_layout)

# --- VIEW CHÍNH ĐIỀU HƯỚNG ---
class PatientView(QtWidgets.QWidget):
    def __init__(self, parent=None, username="Guest"):
        super().__init__(parent)
        self.username = username
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # ===== NAVBAR =====
        navbar = QtWidgets.QFrame()
        navbar.setFixedHeight(70)
        navbar.setStyleSheet("background:white; border-bottom: 1px solid #f1f5f9;")
        nav_layout = QtWidgets.QHBoxLayout(navbar)
        nav_layout.setContentsMargins(40, 0, 40, 0)

        logo = QtWidgets.QLabel("⊕ CarePlus")
        logo.setStyleSheet("color: #69c0a5; font-size: 24px; font-weight: 900;")
        nav_layout.addWidget(logo)
        nav_layout.addStretch()

        # Tạo các nút điều hướng
        self.btn_home = QtWidgets.QPushButton("Trang chủ")
        self.btn_service = QtWidgets.QPushButton("Dịch vụ")
        self.btn_booking = QtWidgets.QPushButton("Đặt lịch khám")

        self.nav_buttons = [self.btn_home, self.btn_service, self.btn_booking]
        for btn in self.nav_buttons:
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton { border:none; background:transparent; font-size: 15px; font-weight: 700; color: #64748b; padding: 10px 15px; }
                QPushButton:hover { color: #69c0a5; }
            """)
            nav_layout.addWidget(btn)

        nav_layout.addStretch()
        user_info = QtWidgets.QLabel(f"👤 {username}")
        user_info.setStyleSheet("font-weight: 700; color: #1e293b; margin-right: 10px;")
        nav_layout.addWidget(user_info)
        
        logout = QtWidgets.QPushButton("Đăng xuất")
        logout.setStyleSheet("background:#ff7875; color:white; border-radius:8px; padding: 8px 18px; font-weight: bold; border: none;")
        nav_layout.addWidget(logout)
        
        self.main_layout.addWidget(navbar)

        # ===== STACKED WIDGET (Quản lý các trang) =====
        self.content_stack = QtWidgets.QStackedWidget()
        
        self.home_page = HomePage(self.username, self)
        self.service_page = ServicePage()
        
        self.content_stack.addWidget(self.home_page)    # Index 0
        self.content_stack.addWidget(self.service_page) # Index 1
        
        self.main_layout.addWidget(self.content_stack)

        # Kết nối sự kiện bấm nút để chuyển trang và đổi màu nút tích cực
        self.btn_home.clicked.connect(lambda: self.switch_page(0))
        self.btn_service.clicked.connect(lambda: self.switch_page(1))
        self.btn_booking.clicked.connect(lambda: self.switch_page(0))

        # Mặc định trang chủ được chọn
        self.switch_page(0)

    def switch_page(self, index):
        self.content_stack.setCurrentIndex(index)
        # Đổi màu text để người dùng biết mình đang ở trang nào
        for i, btn in enumerate([self.btn_home, self.btn_service, self.btn_booking]):
            if i == index or (index == 0 and i == 2): # Booking cũng dẫn về trang chủ
                btn.setStyleSheet("border:none; background:transparent; font-size: 15px; font-weight: 800; color: #69c0a5; border-bottom: 2px solid #69c0a5;")
            else:
                btn.setStyleSheet("border:none; background:transparent; font-size: 15px; font-weight: 700; color: #64748b;")

    # Logic cũ giữ nguyên
    def select_time(self, btn, page):
        for b in page.buttons:
            b.setStyleSheet("QPushButton { background:#f1f5f9; border-radius:8px; padding:12px; font-weight: bold; border: none; } QPushButton:hover { background: #e2e8f0; }")
        btn.setStyleSheet("background:#69c0a5; color:white; border-radius:8px; padding:12px; font-weight: bold; border: none;")
        page.selected_time = btn.text()

    def book(self, page):
        doctor = page.doctor.currentText()
        date = page.date.date().toString("yyyy-MM-dd")
        if not page.selected_time:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng chọn khung giờ khám!")
            return
        AppointmentController.book(doctor, date, page.selected_time, self.username)
        QtWidgets.QMessageBox.information(self, "Thành công", f"Đã đặt lịch khám với {doctor} vào {page.selected_time} ngày {date}")