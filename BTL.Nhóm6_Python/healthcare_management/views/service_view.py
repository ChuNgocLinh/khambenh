from PyQt6 import QtWidgets, QtCore
from controllers.appointment_controller import AppointmentController

# =========================
# SERVICE PAGE (TRANG DỊCH VỤ)
# =========================
class ServicePage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QtWidgets.QLabel("Dịch vụ y tế của chúng tôi")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)

        # Danh sách dịch vụ hiển thị dạng Card
        services = [
            ("Khám tổng quát", "500.000đ", "Kiểm tra sức khỏe định kỳ toàn diện."),
            ("Xét nghiệm máu", "300.000đ", "Phân tích các chỉ số sinh hóa cơ bản."),
            ("Siêu âm tổng quát", "400.000đ", "Chẩn đoán hình ảnh nội tạng hiện đại."),
            ("Chụp X-Quang", "250.000đ", "Kiểm tra cấu trúc xương và phổi.")
        ]

        for name, price, desc in services:
            card = QtWidgets.QFrame()
            card.setStyleSheet("""
                QFrame {
                    background: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 15px;
                }
                QFrame:hover {
                    border: 1px solid #5fc9b5;
                }
            """)
            card_layout = QtWidgets.QHBoxLayout(card)
            card_layout.setContentsMargins(20, 20, 20, 20)

            # Thông tin dịch vụ
            info_layout = QtWidgets.QVBoxLayout()
            n_label = QtWidgets.QLabel(name)
            n_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333; border: none;")
            p_label = QtWidgets.QLabel(price)
            p_label.setStyleSheet("font-size: 16px; color: #5fc9b5; font-weight: bold; border: none;")
            d_label = QtWidgets.QLabel(desc)
            d_label.setStyleSheet("color: #666; border: none;")

            info_layout.addWidget(n_label)
            info_layout.addWidget(p_label)
            info_layout.addWidget(d_label)

            card_layout.addLayout(info_layout)
            card_layout.addStretch()

            # Nút chọn dịch vụ
            select_btn = QtWidgets.QPushButton("Chọn dịch vụ")
            select_btn.setStyleSheet("""
                QPushButton {
                    background: #f0fdfa;
                    color: #5fc9b5;
                    border: 1px solid #5fc9b5;
                    padding: 8px 20px;
                    border-radius: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #5fc9b5;
                    color: white;
                }
            """)
            card_layout.addWidget(select_btn)
            
            layout.addWidget(card)

        layout.addStretch()
        self.setStyleSheet("background: #f8fafc;")

# =========================
# MAIN PATIENT VIEW
# =========================
class PatientView(QtWidgets.QWidget):
    def __init__(self, parent=None, username="Guest"):
        super().__init__(parent)
        self.username = username
        self.selected_time = None

        # Layout chính của cả View
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # ===== NAVBAR (Thanh điều hướng) =====
        navbar = QtWidgets.QFrame()
        navbar.setStyleSheet("background: white; border-bottom: 1px solid #eee; min-height: 70px;")
        nav_layout = QtWidgets.QHBoxLayout(navbar)
        nav_layout.setContentsMargins(20, 0, 20, 0)

        logo = QtWidgets.QLabel("⊕ CarePlus")
        logo.setStyleSheet("font-size: 22px; font-weight: bold; color: #5fc9b5;")
        nav_layout.addWidget(logo)

        nav_layout.addStretch()

        # Nút chuyển trang
        self.btn_home = QtWidgets.QPushButton("Trang chủ")
        self.btn_service = QtWidgets.QPushButton("Dịch vụ")
        self.btn_booking = QtWidgets.QPushButton("Đặt lịch khám")

        for btn in [self.btn_home, self.btn_service, self.btn_booking]:
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("QPushButton { border: none; background: transparent; font-size: 15px; padding: 10px 15px; color: #444; } QPushButton:hover { color: #5fc9b5; }")
            nav_layout.addWidget(btn)

        nav_layout.addStretch()

        user_label = QtWidgets.QLabel(f"👤 {username}")
        user_label.setStyleSheet("font-weight: bold; color: #333; margin-right: 10px;")
        nav_layout.addWidget(user_label)

        logout = QtWidgets.QPushButton("Đăng xuất")
        logout.setStyleSheet("background: #ff7875; color: white; border-radius: 6px; padding: 8px 15px; font-weight: bold; border: none;")
        nav_layout.addWidget(logout)

        self.main_layout.addWidget(navbar)

        # ===== STACKED WIDGET (Vùng nội dung thay đổi) =====
        self.stacked_widget = QtWidgets.QStackedWidget()
        
        # Trang 1: Trang chủ (Toàn bộ logic cũ của bạn)
        self.home_widget = QtWidgets.QWidget()
        self.setup_home_ui()
        
        # Trang 2: Trang dịch vụ
        self.service_widget = ServicePage()

        self.stacked_widget.addWidget(self.home_widget)    # Index 0
        self.stacked_widget.addWidget(self.service_widget) # Index 1

        self.main_layout.addWidget(self.stacked_widget)

        # Kết nối sự kiện chuyển trang
        self.btn_home.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_service.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_booking.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

    def setup_home_ui(self):
        """Giữ nguyên cấu trúc Hero và Booking cũ của bạn vào đây"""
        layout = QtWidgets.QVBoxLayout(self.home_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Hero section
        hero = QtWidgets.QFrame()
        hero.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e0f7fa, stop:1 #e3f2fd); border-radius: 15px;")
        hero_layout = QtWidgets.QVBoxLayout(hero)
        hero_layout.setContentsMargins(30, 30, 30, 30)

        title = QtWidgets.QLabel("Chăm sóc sức khỏe chuyên nghiệp")
        title.setStyleSheet("font-size: 28px; font-weight: bold; border: none;")
        hero_layout.addWidget(title)
        hero_layout.addWidget(QtWidgets.QLabel("Đặt lịch khám nhanh chóng với đội ngũ bác sĩ hàng đầu"))
        layout.addWidget(hero)

        # Booking Card
        card = QtWidgets.QFrame()
        card.setStyleSheet("background: white; border-radius: 10px; border: 1px solid #eee;")
        card_layout = QtWidgets.QVBoxLayout(card)
        
        row = QtWidgets.QHBoxLayout()
        self.doctor = QtWidgets.QComboBox()
        self.doctor.addItems(["BS Minh", "BS Lan"])
        self.date = QtWidgets.QDateEdit()
        self.date.setCalendarPopup(True)
        row.addWidget(self.doctor)
        row.addWidget(self.date)
        card_layout.addLayout(row)

        time_layout = QtWidgets.QHBoxLayout()
        self.buttons = []
        for t in ["08:00", "09:00", "10:00", "11:00"]:
            btn = QtWidgets.QPushButton(t)
            btn.clicked.connect(lambda _, b=btn: self.select_time(b))
            btn.setStyleSheet("background: #f0f0f0; border-radius: 6px; padding: 10px;")
            self.buttons.append(btn)
            time_layout.addWidget(btn)
        card_layout.addLayout(time_layout)

        book = QtWidgets.QPushButton("Đặt lịch ngay")
        book.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4facfe, stop:1 #43e97b); color: white; padding: 12px; border-radius: 8px; font-weight: bold;")
        book.clicked.connect(self.book)
        card_layout.addWidget(book)
        layout.addWidget(card)

        # Features
        feature_layout = QtWidgets.QHBoxLayout()
        for text in ["Đặt lịch dễ dàng", "Quản lý lịch sử", "Theo dõi đơn thuốc"]:
            box = QtWidgets.QFrame()
            box.setStyleSheet("background: white; border: 1px solid #eee; border-radius: 10px;")
            v = QtWidgets.QVBoxLayout(box)
            v.addWidget(QtWidgets.QLabel(text))
            v.addWidget(QtWidgets.QLabel("Mô tả chi tiết chức năng..."))
            feature_layout.addWidget(box)
        layout.addLayout(feature_layout)

    def select_time(self, btn):
        for b in self.buttons:
            b.setStyleSheet("background: #f0f0f0;")
        btn.setStyleSheet("background: #4facfe; color: white;")
        self.selected_time = btn.text()

    def book(self):
        doctor = self.doctor.currentText()
        date = self.date.date().toString("yyyy-MM-dd")
        if not self.selected_time:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng chọn giờ khám")
            return
        AppointmentController.book(doctor, date, self.selected_time, self.username)
        QtWidgets.QMessageBox.information(self, "Thành công", "Lịch khám đã được ghi nhận!")