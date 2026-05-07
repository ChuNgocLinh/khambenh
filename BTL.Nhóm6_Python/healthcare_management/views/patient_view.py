from PyQt6 import QtWidgets, QtCore
from controllers.service_controller import ServiceController
from controllers.doctor_controller import DoctorController
from database.db import fetch_all


class DetailDialog(QtWidgets.QDialog):
    def __init__(self, title, fields, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(520)

        layout = QtWidgets.QVBoxLayout(self)
        card = QtWidgets.QFrame()
        card.setStyleSheet(
            "background: white; border: 1px solid #e2e8f0; border-radius: 14px;"
        )
        form = QtWidgets.QFormLayout(card)
        form.setContentsMargins(20, 20, 20, 20)
        form.setHorizontalSpacing(24)
        form.setVerticalSpacing(14)

        for label, value in fields:
            key_label = QtWidgets.QLabel(label)
            key_label.setStyleSheet("font-weight: 700; color: #334155;")

            val_label = QtWidgets.QLabel(str(value) if value is not None else "")
            val_label.setWordWrap(True)
            val_label.setStyleSheet("color: #0f172a;")
            form.addRow(key_label, val_label)

        layout.addWidget(card)

        close_btn = QtWidgets.QPushButton("Đóng")
        close_btn.setStyleSheet(
            "background: #69c0a5; color: white; border-radius: 8px; padding: 8px 16px; font-weight: 700;"
        )
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, 0, QtCore.Qt.AlignmentFlag.AlignRight)

# --- TRANG DỊCH VỤ (VIEW MỚI) ---
class ServicePage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20) # Thêm lề cho thoáng
        
        title = QtWidgets.QLabel("Danh sách dịch vụ y tế")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)

        desc = QtWidgets.QLabel("Nhấn vào từng dịch vụ để xem thông tin chi tiết.")
        desc.setStyleSheet("color: #64748b; font-size: 14px; margin-bottom: 8px;")
        layout.addWidget(desc)

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
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        
        services_data = ServiceController.get_all()
        self.services_data = services_data
        self.table.setRowCount(len(services_data))
        for i, s in enumerate(services_data):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(s.get("service_name", ""))))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(s.get("price", ""))))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(s.get("description", ""))))
            self.table.setRowHeight(i, 50)

        self.table.cellDoubleClicked.connect(self.show_detail)
            
        layout.addWidget(self.table)
        layout.addStretch()

    def show_detail(self, row, _col):
        if row < 0 or row >= len(self.services_data):
            return

        service = self.services_data[row]
        fields = [
            ("Mã dịch vụ", service.get("service_id", "")),
            ("Tên dịch vụ", service.get("service_name", "")),
            ("Giá", service.get("price", "")),
            ("Mô tả", service.get("description", "")),
        ]
        dialog = DetailDialog("Chi tiết dịch vụ", fields, self)
        dialog.exec()


class DoctorPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)

        title = QtWidgets.QLabel("Đội ngũ bác sĩ")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #2c3e50;")
        layout.addWidget(title)

        desc = QtWidgets.QLabel("Danh sách bác sĩ đang khám tại CarePlus. Nhấn đúp để xem chi tiết.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #64748b; font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(desc)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Họ tên", "Chuyên khoa", "SĐT"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setStyleSheet(
            """
            QTableWidget { background: white; border-radius: 12px; border: 1px solid #eef0f2; font-size: 14px; }
            QHeaderView::section { background-color: #f8f9fa; padding: 12px; font-weight: bold; border: none; border-bottom: 2px solid #69c0a5; }
            QTableWidget::item { padding: 12px; border-bottom: 1px solid #f1f5f9; }
            """
        )

        doctors = DoctorController.get_all()
        self.doctors_data = doctors
        self.table.setRowCount(len(doctors))
        for i, doctor in enumerate(doctors):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(doctor.get("name", ""))))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(doctor.get("specialty", ""))))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(doctor.get("phone", ""))))
            self.table.setRowHeight(i, 48)

        self.table.cellDoubleClicked.connect(self.show_detail)
        layout.addWidget(self.table)
        layout.addStretch()

    def show_detail(self, row, _col):
        if row < 0 or row >= len(self.doctors_data):
            return

        doctor = self.doctors_data[row]
        fields = [
            ("Mã bác sĩ", doctor.get("doctor_id", "")),
            ("Họ tên", doctor.get("name", "")),
            ("Chuyên khoa", doctor.get("specialty", "")),
            ("SĐT", doctor.get("phone", "")),
            ("Email", doctor.get("email", "")),
        ]
        dialog = DetailDialog("Chi tiết bác sĩ", fields, self)
        dialog.exec()


class NewsPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)

        title = QtWidgets.QLabel("Tin tức & tư vấn sức khỏe")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #2c3e50;")
        layout.addWidget(title)

        self.news_items = [
            {
                "title": "5 dấu hiệu cần đi khám tổng quát định kỳ",
                "summary": "Những biểu hiện cơ thể cảnh báo bạn nên kiểm tra sức khỏe sớm.",
                "content": "Nếu bạn thường xuyên mệt mỏi, rối loạn giấc ngủ, giảm tập trung hoặc thay đổi cân nặng bất thường, hãy đi khám sớm để phát hiện nguy cơ tiềm ẩn.",
            },
            {
                "title": "Lưu ý trước khi xét nghiệm máu",
                "summary": "Chuẩn bị đúng giúp kết quả xét nghiệm chính xác hơn.",
                "content": "Bạn nên nhịn ăn từ 8-12 giờ tùy loại xét nghiệm, ngủ đủ giấc và hạn chế dùng chất kích thích trước ngày khám.",
            },
            {
                "title": "Chương trình tiêm chủng theo độ tuổi",
                "summary": "Cập nhật lịch tiêm chủng giúp phòng bệnh hiệu quả.",
                "content": "Người lớn cần tiêm nhắc một số vaccine định kỳ. Trẻ em cần bám sát lịch tiêm để tăng miễn dịch cộng đồng.",
            },
        ]

        desc = QtWidgets.QLabel(
            "Nhấn vào từng mục để xem chi tiết. Một số chuyên mục nâng cao đang được bổ sung nội dung."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #64748b; font-size: 14px; margin-bottom: 8px;")
        layout.addWidget(desc)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setStyleSheet(
            """
            QListWidget { background: white; border: 1px solid #eef0f2; border-radius: 12px; padding: 6px; }
            QListWidget::item { padding: 12px; border-bottom: 1px solid #f1f5f9; }
            QListWidget::item:selected { background: #e1f2ee; color: #1f2937; border-radius: 8px; }
            """
        )

        for item in self.news_items:
            self.list_widget.addItem(f"📰 {item['title']}\n{item['summary']}")

        self.list_widget.itemDoubleClicked.connect(self.show_detail)
        layout.addWidget(self.list_widget)

        note = QtWidgets.QLabel(
            "Chuyên mục video tư vấn và livestream bác sĩ đang trong quá trình phát triển."
        )
        note.setStyleSheet(
            "color: #92400e; background: #fffbeb; border: 1px solid #fde68a; border-radius: 10px; padding: 10px;"
        )
        layout.addWidget(note)
        layout.addStretch()

    def show_detail(self, item):
        row = self.list_widget.row(item)
        if row < 0 or row >= len(self.news_items):
            return

        news = self.news_items[row]
        fields = [
            ("Tiêu đề", news["title"]),
            ("Tóm tắt", news["summary"]),
            ("Nội dung", news["content"]),
        ]
        dialog = DetailDialog("Chi tiết tin tức", fields, self)
        dialog.exec()

# --- TRANG LỊCH SỬ KHÁM ---
class HistoryPage(QtWidgets.QWidget):
    def __init__(self, patient_id):
        super().__init__()
        self.patient_id = patient_id
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)
        
        title = QtWidgets.QLabel("Lịch sử khám bệnh")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Ngày khám", "Bác sĩ", "Chẩn đoán", "Điều trị"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget { background: white; border-radius: 12px; border: 1px solid #eef0f2; font-size: 14px; }
            QHeaderView::section { background-color: #f8f9fa; padding: 12px; font-weight: bold; border: none; border-bottom: 2px solid #69c0a5; }
            QTableWidget::item { padding: 15px; border-bottom: 1px solid #f1f5f9; }
        """)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        
        records = fetch_all("""
            SELECT r.*, d.name as doctor_name
            FROM MedicalRecords r
            JOIN Doctors d ON r.doctor_id = d.doctor_id
            WHERE r.patient_id = ?
            ORDER BY r.created_at DESC
        """, (self.patient_id,))
        
        self.table.setRowCount(len(records))
        for i, r in enumerate(records):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(r.get("created_at", ""))))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(r.get("doctor_name", ""))))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(r.get("diagnosis", ""))))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(r.get("treatment", ""))))
            self.table.setRowHeight(i, 50)
            
        layout.addWidget(self.table)
        layout.addStretch()

# --- TRANG HỒ SƠ CÁ NHÂN ---
class ProfilePage(QtWidgets.QWidget):
    def __init__(self, patient_id):
        super().__init__()
        self.patient_id = patient_id
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)
        
        title = QtWidgets.QLabel("Hồ sơ cá nhân")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        form_widget = QtWidgets.QWidget()
        form_widget.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #eef0f2; padding: 20px;")
        form_layout = QtWidgets.QFormLayout(form_widget)
        
        self.name_input = QtWidgets.QLineEdit()
        self.dob_input = QtWidgets.QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.gender_input = QtWidgets.QComboBox()
        self.gender_input.addItems(["Nam", "Nữ"])
        self.phone_input = QtWidgets.QLineEdit()
        self.address_input = QtWidgets.QLineEdit()
        
        for w in [self.name_input, self.dob_input, self.gender_input, self.phone_input, self.address_input]:
            w.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #ddd; font-size: 14px;")
        
        form_layout.addRow("Họ tên:", self.name_input)
        form_layout.addRow("Ngày sinh:", self.dob_input)
        form_layout.addRow("Giới tính:", self.gender_input)
        form_layout.addRow("SĐT:", self.phone_input)
        form_layout.addRow("Địa chỉ:", self.address_input)
        
        self.load_data()
        
        save_btn = QtWidgets.QPushButton("Cập nhật thông tin")
        save_btn.setStyleSheet("background: #69c0a5; color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold; font-size: 14px;")
        save_btn.clicked.connect(self.save_data)
        
        layout.addWidget(form_widget)
        layout.addWidget(save_btn, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addStretch()
        
    def load_data(self):
        from models.patient_model import PatientModel
        p = PatientModel.get_by_id(self.patient_id)
        if p:
            self.name_input.setText(str(p.get("name", "")))
            self.phone_input.setText(str(p.get("phone", "")))
            self.address_input.setText(str(p.get("address", "")))
            self.gender_input.setCurrentText(str(p.get("gender", "Nam")))
            if p.get("dob"):
                self.dob_input.setDate(QtCore.QDate.fromString(str(p.get("dob")), "yyyy-MM-dd"))
                
    def save_data(self):
        from models.patient_model import PatientModel
        success = PatientModel.update(
            self.patient_id,
            self.name_input.text(),
            self.dob_input.date().toString("yyyy-MM-dd"),
            self.gender_input.currentText(),
            self.phone_input.text(),
            self.address_input.text()
        )
        if success:
            QtWidgets.QMessageBox.information(self, "Thành công", "Đã cập nhật thông tin cá nhân!")
        else:
            QtWidgets.QMessageBox.warning(self, "Thất bại", "Không thể cập nhật thông tin. Vui lòng thử lại.")

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
        QtWidgets.QMessageBox.information(
            self,
            "Thông báo",
            "Luồng đặt lịch đã được nâng cấp trên giao diện bệnh nhân chính. Vui lòng sử dụng menu mới để đặt lịch chính xác.",
        )
