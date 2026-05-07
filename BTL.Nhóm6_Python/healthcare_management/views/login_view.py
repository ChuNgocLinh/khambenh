from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox, QFrame, 
    QStackedWidget, QCheckBox, QGridLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont, QCursor

from controllers.auth_controller import AuthController
from views.main_view import MainView

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CarePlus - Healthcare Management System")
        self.resize(1150, 800)
        self.setStyleSheet("background-color: #f4f9ff;")

        window_layout = QVBoxLayout(self)
        
        self.main_card = QFrame()
        self.main_card.setFixedSize(1050, 720)
        self.main_card.setStyleSheet("background-color: white; border-radius: 30px;")
        window_layout.addWidget(self.main_card, alignment=Qt.AlignmentFlag.AlignCenter)

        card_layout = QHBoxLayout(self.main_card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        # ================= LEFT PANEL =================
        left_panel = QFrame()
        left_panel.setFixedWidth(520)

        left_panel.setStyleSheet("""
            QFrame {
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                background-color: black;
            }
        """)

        # ===== ẢNH NỀN =====
        bg_label = QLabel(left_panel)
        bg_label.setGeometry(0, 0, 520, 720)

        pixmap = QPixmap("healthcare_management/assets/bg.jpg")

        bg_label.setPixmap(
            pixmap.scaled(
                520,
                720,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        bg_label.setScaledContents(True)

        # ===== OVERLAY TỐI NHẸ =====
        overlay = QFrame(left_panel)
        overlay.setGeometry(0, 0, 520, 720)

        overlay.setStyleSheet("""
            background-color: rgba(0, 0, 0, 90);
            border-top-left-radius: 30px;
            border-bottom-left-radius: 30px;
        """)

        # ===== ĐƯA ẢNH RA SAU =====
        bg_label.lower()
        overlay.raise_()

        # ===== LAYOUT CHỮ =====
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(40, 40, 40, 40)

        # Logo
        header_logo = QLabel("🛡️ CarePlus")
        header_logo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            background: transparent;
        """)
        left_layout.addWidget(header_logo)
        
        left_layout.addSpacing(20)

        # Tiêu đề chính
        title_large = QLabel("Chăm sóc sức khỏe\ndễ dàng hơn mỗi ngày")
        title_large.setStyleSheet("""
            font-size: 44px;
            font-weight: 900;
            color: white;
            line-height: 1.2;
            background: transparent;
        """)
        left_layout.addWidget(title_large)

        # Mô tả
        sub_desc = QLabel("Nền tảng đặt lịch khám bệnh thông minh,\nkết nối bạn với đội ngũ bác sĩ uy tín.")
        sub_desc.setStyleSheet("""
            font-size: 16px;
            color: rgba(255,255,255,220);
            margin-top: 15px;
            background: transparent;
        """)
        left_layout.addWidget(sub_desc)

        left_layout.addStretch()

        # Banner tiện ích
        banner_frame = QFrame()
        banner_frame.setFixedHeight(130)
        banner_frame.setStyleSheet("""
            background-color: rgba(255, 255, 255, 220);
            border-radius: 20px;
        """)
        banner_layout = QHBoxLayout(banner_frame)
        banner_layout.setContentsMargins(10, 10, 10, 10)
        banner_layout.setSpacing(5)
        
        features = [
            ("🛡️", "An toàn", "Bảo mật thông tin\ntuyệt đối"),
            ("🕒", "Nhanh chóng", "Đặt lịch chỉ trong\nvài bước"),
            ("👨‍⚕️", "Uy tín", "Đội ngũ bác sĩ\nchuyên môn cao"),
            ("❤️", "Tận tâm", "Chăm sóc bạn bằng\ncả trái tim")
        ]

        for icon, title, desc in features:
            f_item = QVBoxLayout()
            f_icon = QLabel(icon)
            f_icon.setStyleSheet("font-size: 20px; background: transparent;")
            f_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            f_title = QLabel(title)
            f_title.setStyleSheet("font-weight: bold; font-size: 13px; color: #1a2d42; background: transparent;")
            f_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            f_desc = QLabel(desc)
            f_desc.setWordWrap(True)
            f_desc.setFixedWidth(100)
            f_desc.setStyleSheet("font-size: 10px; color: #666; background: transparent;")
            f_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            f_item.addWidget(f_icon)
            f_item.addWidget(f_title)
            f_item.addWidget(f_desc)
            banner_layout.addLayout(f_item)

        left_layout.addWidget(banner_frame)

        # ================= RIGHT PANEL =================
        self.right_stack = QStackedWidget()
        self.login_page = QWidget()
        self.setup_login_page()
        self.register_page = QWidget()
        self.setup_register_page()
        self.forgot_page = QWidget()
        self.setup_forgot_page()

        self.right_stack.addWidget(self.login_page)
        self.right_stack.addWidget(self.register_page)
        self.right_stack.addWidget(self.forgot_page)

        card_layout.addWidget(left_panel)
        card_layout.addWidget(self.right_stack)

    def setup_login_page(self):
        layout = QVBoxLayout(self.login_page)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(18)

        tab_layout = QHBoxLayout()
        btn_tab_login = QPushButton("👤 Đăng nhập")
        btn_tab_login.setStyleSheet("font-weight: bold; color: #006fe6; border: none; border-bottom: 3px solid #006fe6; padding: 10px; font-size: 16px;")
        
        btn_tab_reg = QPushButton("👤+ Đăng ký")
        btn_tab_reg.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_tab_reg.setStyleSheet("color: #888; border: none; padding: 10px; font-size: 16px;")
        btn_tab_reg.clicked.connect(lambda: self.right_stack.setCurrentIndex(1))

        tab_layout.addWidget(btn_tab_login)
        tab_layout.addWidget(btn_tab_reg)
        tab_layout.addStretch()
        layout.addLayout(tab_layout)

        welcome = QLabel("Chào mừng bạn trở lại! 👋")
        welcome.setStyleSheet("font-size: 28px; font-weight: bold; color: #000; margin-top: 10px;")
        layout.addWidget(welcome)

        desc = QLabel("Đăng nhập để quản lý sức khỏe của bạn")
        desc.setStyleSheet("color: #555; font-size: 14px;")
        layout.addWidget(desc)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Email hoặc số điện thoại")
        self.username.setStyleSheet(self.get_input_style())
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("Mật khẩu")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet(self.get_input_style())

        layout.addWidget(self.username)
        layout.addWidget(self.password)

        hbox = QHBoxLayout()
        remember = QCheckBox("Ghi nhớ tôi")
        remember.setStyleSheet("""
            QCheckBox { color: #006fe6; font-size: 13px; font-weight: 500; }
            QCheckBox::indicator { width: 18px; height: 18px; }
            QCheckBox::indicator:unchecked { border: 2px solid #ddd; border-radius: 4px; background: white; }
            QCheckBox::indicator:checked { border: 2px solid #006fe6; border-radius: 4px; background: #006fe6; }
        """)
        
        forgot_btn = QPushButton("Quên mật khẩu?")
        forgot_btn.setStyleSheet("color: #006fe6; border: none; font-size: 13px; font-weight: bold;")
        forgot_btn.clicked.connect(lambda: self.right_stack.setCurrentIndex(2))
        hbox.addWidget(remember)
        hbox.addStretch()
        hbox.addWidget(forgot_btn)
        layout.addLayout(hbox)

        self.login_btn = QPushButton("🔒 Đăng nhập ngay")
        self.login_btn.setStyleSheet(self.get_main_btn_style())
        self.login_btn.clicked.connect(self.login)
        layout.addWidget(self.login_btn)

        layout.addStretch()
        footer = QFrame()
        footer.setStyleSheet("border-top: 1px solid #eee; padding-top: 10px;")
        footer_layout = QVBoxLayout(footer)
        help_text = QLabel("📞 Hotline: 1900 6000\n🛡️ Bảo mật chuẩn y khoa ISO 27001")
        help_text.setStyleSheet("color: #666; font-size: 12px; line-height: 1.5;")
        help_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addWidget(help_text)
        layout.addWidget(footer)

    def setup_register_page(self):
        layout = QVBoxLayout(self.register_page)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(15)

        title = QLabel("Tạo tài khoản mới 📝")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #000;")
        layout.addWidget(title)
        
        desc = QLabel("Tham gia cùng cộng đồng CarePlus ngay hôm nay")
        desc.setStyleSheet("color: #555; font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(desc)

        fields = ["Họ và tên", "Số điện thoại", "Email cá nhân", "Mật khẩu", "Xác nhận mật khẩu"]
        self.reg_inputs = {}
        for f in fields:
            edit = QLineEdit()
            edit.setPlaceholderText(f)
            edit.setStyleSheet(self.get_input_style())
            if "Mật khẩu" in f: edit.setEchoMode(QLineEdit.EchoMode.Password)
            layout.addWidget(edit)
            self.reg_inputs[f] = edit

        reg_btn = QPushButton("Đăng ký tài khoản")
        reg_btn.setStyleSheet(self.get_main_btn_style())
        reg_btn.clicked.connect(self.register_account)
        layout.addWidget(reg_btn)

        back_btn = QPushButton("← Đã có tài khoản? Đăng nhập ngay")
        back_btn.setStyleSheet("border: none; color: #006fe6; font-weight: bold;")
        back_btn.clicked.connect(lambda: self.right_stack.setCurrentIndex(0))
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

    def register_account(self):
        name = self.reg_inputs["Họ và tên"].text().strip()
        phone = self.reg_inputs["Số điện thoại"].text().strip()
        email = self.reg_inputs["Email cá nhân"].text().strip()
        pwd = self.reg_inputs["Mật khẩu"].text().strip()
        pwd_conf = self.reg_inputs["Xác nhận mật khẩu"].text().strip()
        
        if not all([name, phone, email, pwd, pwd_conf]):
            msg = QMessageBox(self)
            msg.setText("Vui lòng điền đầy đủ thông tin!")
            msg.setStyleSheet("QLabel{ color: #000; }")
            msg.exec()
            return
            
        if pwd != pwd_conf:
            msg = QMessageBox(self)
            msg.setText("Mật khẩu xác nhận không khớp!")
            msg.setStyleSheet("QLabel{ color: #000; }")
            msg.exec()
            return
            
        res = AuthController.register(email, pwd, name, phone, email)
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Thông báo")
        msg.setText(res["message"])
        msg.setStyleSheet("""
            QLabel{ color: #000000; font-size: 14px; }
            QPushButton{ width: 80px; color: black; background-color: #eee; font-weight: bold; border-radius: 5px; padding: 5px;}
        """)
        msg.setIcon(QMessageBox.Icon.Information if res["status"] else QMessageBox.Icon.Warning)
        msg.exec()
        if res["status"]:
            self.right_stack.setCurrentIndex(0)

    def setup_forgot_page(self):
        layout = QVBoxLayout(self.forgot_page)
        layout.setContentsMargins(50, 80, 50, 80)
        layout.setSpacing(20)
        
        lbl = QLabel("Khôi phục mật khẩu 🔑")
        lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #000;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        sub = QLabel("Nhập email để nhận mã khôi phục")
        sub.setStyleSheet("color: #555; font-size: 14px;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        email_forgot = QLineEdit()
        email_forgot.setPlaceholderText("Email của bạn...")
        email_forgot.setStyleSheet(self.get_input_style())
        
        send_btn = QPushButton("Gửi yêu cầu")
        send_btn.setStyleSheet(self.get_main_btn_style())
        
        back_btn = QPushButton("Quay lại")
        back_btn.clicked.connect(lambda: self.right_stack.setCurrentIndex(0))
        back_btn.setStyleSheet("border: none; color: #888; font-weight: bold;")

        layout.addWidget(lbl)
        layout.addWidget(sub)
        layout.addWidget(email_forgot)
        layout.addWidget(send_btn)
        layout.addWidget(back_btn)
        layout.addStretch()

    def get_input_style(self):
        return """
            QLineEdit {
                padding: 15px; border: 1px solid #ddd; border-radius: 12px;
                background-color: #fcfcfc; font-size: 14px; color: #000;
            }
            QLineEdit:focus { border: 2px solid #006fe6; background-color: #fff; }
        """

    def get_main_btn_style(self):
        return """
            QPushButton {
                background-color: #006fe6; color: white; font-weight: bold; font-size: 16px;
                padding: 15px; border-radius: 12px;
            }
            QPushButton:hover { background-color: #0056b3; }
        """

    def login(self):
        user = self.username.text().strip()
        pwd = self.password.text().strip()
        if not user or not pwd:
            msg = QMessageBox(self)
            msg.setText("Vui lòng nhập đủ thông tin!")
            msg.setStyleSheet("QLabel{ color: #000; }")
            msg.exec()
            return
            
        res = AuthController.login(user, pwd)
        if res and res.get("status"):
            user_data = res.get("user")
            self.main_window = MainView(res.get("role"), user_data, self)
            self.main_window.show()
            self.close()
        else:
            msg = QMessageBox(self)
            msg.setText(res.get("message") if res else "Đăng nhập thất bại")
            msg.setStyleSheet("QLabel{ color: #000; }")
            msg.exec()