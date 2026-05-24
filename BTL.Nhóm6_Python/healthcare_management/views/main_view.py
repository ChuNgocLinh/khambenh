from PyQt6 import QtWidgets, QtCore, QtGui
from pathlib import Path
from views.dashboard_view import DashboardView, AdminDashboardView 
from views.staff_dashboard_view import StaffDashboardView
from models.doctor_model import DoctorModel
from controllers.appointment_controller import AppointmentController
from controllers.doctor_controller import DoctorController
from controllers.service_controller import ServiceController

CANONICAL_ROLES = {"admin", "staff", "doctor", "patient"}


def normalize_role(role):
    normalized = str(role or "").strip().lower()
    return normalized if normalized in CANONICAL_ROLES else "unknown"

class MainView(QtWidgets.QMainWindow):
    def __init__(self, role, user_data, login_window=None):
        super().__init__()
        self.raw_role = str(role or "").strip()
        self.role = normalize_role(role)
        self.user_data = user_data if isinstance(user_data, dict) else {"username": "Unknown", "patient_id": 1, "doctor_id": 1}
        self.user_data["role"] = self.role
        self.username = self.user_data.get("name") or self.user_data.get("username")
        
        # QUAN TRỌNG: Lưu tham chiếu cửa sổ đăng nhập
        self.login_window = login_window 
        self.selected_time = None
        self._time_buttons = []

        role_title = self.role.upper() if self.role != "unknown" else "UNKNOWN ROLE"
        self.setWindowTitle(f"CarePlus - {role_title}")
        self.resize(1150, 850) 

        central = QtWidgets.QWidget()
        central.setStyleSheet("background-color: #f8faff;") 
        self.setCentralWidget(central)

        self.main_layout = QtWidgets.QVBoxLayout(central)
        self.main_layout.setContentsMargins(0, 0, 0, 0) 
        self.main_layout.setSpacing(0)

        self._route_role_view()

    def _route_role_view(self):
        if self.role == "admin":
            self.admin_dashboard = AdminDashboardView(self.user_data)
            self.admin_dashboard.btn_logout.clicked.connect(self.logout)
            self.main_layout.addWidget(self.admin_dashboard)
            return

        if self.role == "doctor":
            self.doctor_dashboard = DashboardView(self.user_data)
            self.doctor_dashboard.user_name_lbl.setText(f"Bác sĩ {self.username} ▿")
            self.doctor_dashboard.btn_logout.clicked.connect(self.logout)
            self.main_layout.addWidget(self.doctor_dashboard)
            return

        if self.role == "staff":
            self.staff_dashboard = StaffDashboardView(self.user_data)
            self.staff_dashboard.btn_logout.clicked.connect(self.logout)
            self.main_layout.addWidget(self.staff_dashboard)
            return

        if self.role == "patient":
            self.init_patient_ui()
            return

        self.init_unknown_role_ui()

    def init_unknown_role_ui(self):
        unknown_widget = QtWidgets.QWidget()
        unknown_layout = QtWidgets.QVBoxLayout(unknown_widget)
        unknown_layout.setContentsMargins(40, 40, 40, 40)

        title = QtWidgets.QLabel("Vai trò không được hỗ trợ")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1f2937;")

        detail = QtWidgets.QLabel(f"Hệ thống chưa có giao diện cho vai trò: {self.raw_role or 'unknown'}")
        detail.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        detail.setWordWrap(True)
        detail.setStyleSheet("font-size: 14px; color: #4b5563;")

        logout_btn = QtWidgets.QPushButton("Đăng xuất")
        logout_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #006fe6;
                color: white;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover { background-color: #0056b3; }
        """)
        logout_btn.clicked.connect(self.logout)

        unknown_layout.addStretch()
        unknown_layout.addWidget(title)
        unknown_layout.addWidget(detail)
        unknown_layout.addSpacing(16)
        unknown_layout.addWidget(logout_btn, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        unknown_layout.addStretch()

        self.main_layout.addWidget(unknown_widget)

    def init_patient_ui(self):
        # Tạo StackedWidget để quản lý các trang
        self.patient_stack = QtWidgets.QStackedWidget()
        self.main_layout.addWidget(self.patient_stack)

        # --- TRANG 0: DASHBOARD ---
        self.page_dashboard = QtWidgets.QWidget()
        dashboard_layout = QtWidgets.QVBoxLayout(self.page_dashboard)
        dashboard_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        
        container = QtWidgets.QWidget()
        container.setStyleSheet("background-color: #f8faff;")
        container_layout = QtWidgets.QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 40)
        container_layout.setSpacing(20)

        container_layout.addWidget(self.create_navbar(0))

        main_content_widget = QtWidgets.QWidget()
        main_content_layout = QtWidgets.QVBoxLayout(main_content_widget)
        main_content_layout.setContentsMargins(40, 10, 40, 10)
        main_content_layout.setSpacing(20)

        # 2. Hero Banner
        hero_bg = QtWidgets.QFrame()
        hero_bg.setFixedHeight(300)
        hero_bg.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #eefaf9, stop:1 #ffffff); border-radius: 30px;")
        hero_h_layout = QtWidgets.QHBoxLayout(hero_bg)
        hero_h_layout.setContentsMargins(50, 20, 50, 20)

        txt_layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("Chăm sóc sức khỏe\nchuyên nghiệp")
        title.setStyleSheet("font-size: 38px; font-weight: 900; color: #1a2a3a;")
        sub = QtWidgets.QLabel("Đặt lịch khám bệnh dễ dàng và nhanh chóng\nvới đội ngũ bác sĩ hàng đầu tại CarePlus")
        sub.setStyleSheet("font-size: 16px; color: #5f6c7b;")
        txt_layout.addStretch(); txt_layout.addWidget(title); txt_layout.addWidget(sub); txt_layout.addStretch()
        
        doc_img = QtWidgets.QLabel()
        pix = QtGui.QPixmap(str(Path(__file__).resolve().parents[1] / "assets" / "bg.jpg"))
        if not pix.isNull():
            doc_img.setPixmap(pix.scaled(400, 400, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
        else:
            doc_img.setText("👨‍⚕️")
            doc_img.setStyleSheet("font-size: 150px;")
        
        hero_h_layout.addLayout(txt_layout)
        hero_h_layout.addWidget(doc_img, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        main_content_layout.addWidget(hero_bg)

        # 3. Grid Dashboard
        grid_layout = QtWidgets.QHBoxLayout()
        grid_layout.setSpacing(25)

        # --- CỘT TRÁI: ĐẶT LỊCH ---
        booking_card = QtWidgets.QFrame()
        booking_card.setFixedWidth(550)
        booking_card.setStyleSheet("background: white; border-radius: 20px; border: 1px solid #f0f0f0;")
        bk_v = QtWidgets.QVBoxLayout(booking_card)
        bk_v.setContentsMargins(25, 25, 25, 25); bk_v.setSpacing(15)

        bk_title = QtWidgets.QLabel("Đặt lịch khám")
        bk_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1a2a3a; border:none;")
        bk_v.addWidget(bk_title)

        combo_style = """
            QComboBox { 
                padding: 10px; border: 1px solid #eee; border-radius: 10px; 
                background: #f8faff; color: #333; font-size: 14px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #333;
                selection-background-color: #69c0a5;
                selection-color: white;
                outline: none;
                border: 1px solid #eee;
            }
            QDateEdit { 
                padding: 10px; border: 1px solid #eee; border-radius: 10px; 
                background: #f8faff; color: #333; font-size: 14px;
            }
        """

        row_service = QtWidgets.QHBoxLayout()
        self.cb_service = QtWidgets.QComboBox()
        self.cb_service.setStyleSheet(combo_style)
        services = ServiceController.get_visible_active()
        for service in services:
            service_name = str(service.get("service_name", ""))
            if service_name:
                self.cb_service.addItem(service_name, userData=service.get("service_id"))
        if self.cb_service.count() == 0:
            self.cb_service.addItem("Chưa có dịch vụ")

        service_label = QtWidgets.QLabel("Dịch vụ khám")
        service_label.setStyleSheet("font-weight: 700; color: #334155;")
        row_service.addWidget(service_label)
        row_service.addWidget(self.cb_service)
        bk_v.addLayout(row_service)

        row_cb = QtWidgets.QHBoxLayout()
        
        self.cb_doc = QtWidgets.QComboBox()
        docs = DoctorController.get_available_for_patient()
        for doc in docs:
            self.cb_doc.addItem(f"BS {doc['name']}", userData=doc["doctor_id"])
        self.cb_doc.setStyleSheet(combo_style)
        
        self.de_date = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.de_date.setCalendarPopup(True)
        self.de_date.setStyleSheet(combo_style)
        
        calendar = self.de_date.calendarWidget()
        calendar.setStyleSheet("""
            QCalendarWidget QWidget { color: #333; }
            QCalendarWidget QToolButton { color: #333; background-color: white; }
            QCalendarWidget QMenu { background-color: white; color: #333; }
            QCalendarWidget QSpinBox { color: #333; }
            QCalendarWidget QAbstractItemView:enabled { color: #333; selection-background-color: #69c0a5; }
        """)

        row_cb.addWidget(self.cb_doc); row_cb.addWidget(self.de_date)
        bk_v.addLayout(row_cb)

        self.time_grid = QtWidgets.QGridLayout()
        self.time_grid.setHorizontalSpacing(8)
        self.time_grid.setVerticalSpacing(8)
        bk_v.addLayout(self.time_grid)

        self.booking_hint = QtWidgets.QLabel("Vui lòng chọn dịch vụ, ngày, bác sĩ và giờ khám.")
        self.booking_hint.setStyleSheet("color: #64748b; font-size: 13px;")
        bk_v.addWidget(self.booking_hint)

        self.cb_service.currentIndexChanged.connect(self.refresh_available_slots)
        self.cb_doc.currentIndexChanged.connect(self.refresh_available_slots)
        self.de_date.dateChanged.connect(self.refresh_available_slots)
        self.refresh_available_slots()

        btn_book = QtWidgets.QPushButton("Đặt lịch ngay")
        btn_book.setFixedHeight(50)
        btn_book.setStyleSheet("background: #27ae60; color: white; border-radius: 12px; font-size: 18px; font-weight: bold;")
        btn_book.clicked.connect(self.book_appointment)
        bk_v.addWidget(btn_book)
        grid_layout.addWidget(booking_card)

        # --- CỘT PHẢI ---
        right_col = QtWidgets.QVBoxLayout(); right_col.setSpacing(20)

        apt_card = QtWidgets.QFrame(); apt_card.setStyleSheet("background: white; border-radius: 20px; border: 1px solid #eee;")
        apt_v = QtWidgets.QVBoxLayout(apt_card); apt_v.setContentsMargins(20, 20, 20, 20)
        apt_head = QtWidgets.QHBoxLayout()
        apt_head.addWidget(QtWidgets.QLabel("Lịch hẹn sắp tới", styleSheet="font-weight:bold; font-size:18px; color:#1a2a3a; border:none;"))
        apt_head.addStretch(); apt_head.addWidget(QtWidgets.QLabel("Xem tất cả >", styleSheet="color:#3498db; border:none;"))
        apt_v.addLayout(apt_head)
        
        self.appointment_list_layout = apt_v
        self.load_appointments(self.appointment_list_layout)
        right_col.addWidget(apt_card)

        noti_card = QtWidgets.QFrame(); noti_card.setStyleSheet("background: white; border-radius: 20px; border: 1px solid #eee;")
        noti_v = QtWidgets.QVBoxLayout(noti_card); noti_v.setContentsMargins(20, 20, 20, 20)
        noti_v.addWidget(QtWidgets.QLabel("Thông báo", styleSheet="font-weight:bold; font-size:18px; color:#1a2a3a; border:none;"))
        for icon, txt, time in [("🔔", "Lịch hẹn đã xác nhận", "2 giờ trước"), ("📅", "Vui lòng đến sớm 15p", "1 ngày trước")]:
            n_row = QtWidgets.QHBoxLayout()
            n_row.addWidget(QtWidgets.QLabel(icon))
            n_row.addWidget(QtWidgets.QLabel(txt, styleSheet="color: #333; border:none;"))
            n_row.addStretch(); n_row.addWidget(QtWidgets.QLabel(time, styleSheet="color: #999; font-size: 11px; border:none;"))
            noti_v.addLayout(n_row)
        right_col.addWidget(noti_card)
        grid_layout.addLayout(right_col)

        main_content_layout.addLayout(grid_layout)

        # 4. Feature section
        bottom_layout = QtWidgets.QHBoxLayout(); bottom_layout.setSpacing(20)
        features = [
            ("📅", "Đặt lịch khám dễ dàng", "Chọn bác sĩ và thời gian phù hợp để đặt lịch khám bệnh một cách nhanh chóng"),
            ("📋", "Quản lý lịch sử khám", "Xem lại lịch sử khám bệnh và kết quả chẩn đoán mọi lúc, mọi nơi"),
            ("💊", "Theo dõi đơn thuốc", "Dễ dàng theo dõi đơn thuốc và liệu trình điều trị của bạn")
        ]
        for icon, tit, desc in features:
            f_card = QtWidgets.QFrame()
            f_card.setStyleSheet("background: white; border-radius: 15px; border: 1px solid #eef2f5;")
            f_v = QtWidgets.QHBoxLayout(f_card)
            f_v.setContentsMargins(20, 20, 20, 20)
            
            f_icon = QtWidgets.QLabel(icon)
            f_icon.setStyleSheet("font-size: 32px; color: #3498db; background: #eef7fe; padding: 10px; border-radius: 12px; border:none;")
            f_icon.setFixedSize(65, 65)
            f_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            
            f_text_container = QtWidgets.QVBoxLayout()
            f_tit = QtWidgets.QLabel(tit)
            f_tit.setStyleSheet("font-weight: bold; font-size: 16px; color: #1a2a3a; border: none;")
            f_desc = QtWidgets.QLabel(desc)
            f_desc.setWordWrap(True)
            f_desc.setStyleSheet("color: #7f8c8d; font-size: 13px; border: none; line-height: 18px;")
            
            f_text_container.addWidget(f_tit)
            f_text_container.addWidget(f_desc)
            
            f_v.addWidget(f_icon)
            f_v.addLayout(f_text_container)
            f_v.setStretch(1, 1) 
            bottom_layout.addWidget(f_card)
        
        main_content_layout.addLayout(bottom_layout)

        container_layout.addWidget(main_content_widget)
        scroll.setWidget(container)
        dashboard_layout.addWidget(scroll)
        
        self.patient_stack.addWidget(self.page_dashboard) # Index 0

        # --- CÁC TRANG KHÁC ---
        from views.patient_view import ServicePage, DoctorPage, NewsPage, HistoryPage, ProfilePage
        
        # Wrapper cho các trang khác để có navbar
        def create_page_with_navbar(page_content, active_index):
            page = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout(page)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.create_navbar(active_index))
            layout.addWidget(page_content, 1)
            return page

        self.page_service = create_page_with_navbar(ServicePage(on_navigate=self.handle_doctor_page_navigation), 1)
        self.page_doctor = create_page_with_navbar(
            DoctorPage(
                on_navigate=self.handle_doctor_page_navigation,
                on_logout=self.logout,
                on_open_profile=lambda: self.switch_patient_page(5),
                on_update_profile=lambda: self.switch_patient_page(5),
                on_change_password=self.show_change_password_placeholder,
            ),
            2,
        )
        self.page_news = create_page_with_navbar(NewsPage(), 3)
        self.page_history = create_page_with_navbar(HistoryPage(self.user_data.get("patient_id")), 0)
        self.page_profile = create_page_with_navbar(ProfilePage(self.user_data.get("patient_id")), 0)

        self.patient_stack.addWidget(self.page_service)  # Index 1
        self.patient_stack.addWidget(self.page_doctor)   # Index 2
        self.patient_stack.addWidget(self.page_news)     # Index 3
        self.patient_stack.addWidget(self.page_history)  # Index 4
        self.patient_stack.addWidget(self.page_profile)  # Index 5

    def switch_patient_page(self, index):
        self.patient_stack.setCurrentIndex(index)
        self._update_dynamic_navbar()

    def handle_doctor_page_navigation(self, action_key, doctor=None):
        if action_key == "home":
            self.switch_patient_page(0)
            return

        if action_key == "booking":
            if isinstance(doctor, dict):
                self.prefill_booking_from_doctor(doctor, view_only=False)
            else:
                self.switch_patient_page(0)
            return

        if action_key == "view_slots":
            if isinstance(doctor, dict):
                self.prefill_booking_from_doctor(doctor, view_only=True)
            else:
                self.switch_patient_page(0)
            return

        if action_key == "appointments":
            self.switch_patient_page(0)
            QtWidgets.QMessageBox.information(
                self,
                "Lịch hẹn của tôi",
                "Lịch hẹn sắp tới đang hiển thị tại thẻ 'Lịch hẹn sắp tới' trên Trang chủ.",
            )
            return

        if action_key == "service":
            self.switch_patient_page(1)
            return

        if action_key == "doctor":
            self.switch_patient_page(2)
            return

        if action_key == "news":
            self.switch_patient_page(3)
            return

        if action_key == "history":
            self.switch_patient_page(4)
            return

        if action_key in {"profile", "update_profile"}:
            self.switch_patient_page(5)
            return

        if action_key == "change_password":
            self.show_change_password_placeholder()
            return

        if action_key == "lab_results":
            QtWidgets.QMessageBox.information(
                self,
                "Kết quả xét nghiệm",
                "Chức năng xem kết quả xét nghiệm đang trong quá trình phát triển.",
            )
            return

        if action_key == "prescriptions":
            QtWidgets.QMessageBox.information(
                self,
                "Đơn thuốc",
                "Chức năng xem đơn thuốc đang trong quá trình phát triển.",
            )
            return

        if action_key == "billing":
            QtWidgets.QMessageBox.information(
                self,
                "Thanh toán",
                "Thanh toán online đang trong quá trình phát triển. Vui lòng thanh toán tại quầy hoặc liên hệ CarePlus.",
            )
            return

        if action_key == "support":
            QtWidgets.QMessageBox.information(
                self,
                "Hỗ trợ khách hàng",
                "Hotline hỗ trợ khẩn cấp: 1900 1234. Bộ phận CSKH hoạt động 24/7.",
            )
            return

        if action_key == "insurance":
            QtWidgets.QMessageBox.information(
                self,
                "Bảo hiểm y tế",
                "Thông tin bảo hiểm y tế và quyền lợi đang được cập nhật.",
            )
            return

        if action_key == "notifications":
            QtWidgets.QMessageBox.information(
                self,
                "Thông báo",
                "Thông báo lịch khám, kết quả và thanh toán sẽ được hiển thị tại đây trong phiên bản tiếp theo.",
            )
            return

    def prefill_booking_from_doctor(self, doctor, view_only=False):
        self.switch_patient_page(0)
        if not isinstance(doctor, dict):
            return

        doctor_id = doctor.get("doctor_id")
        if doctor_id is None:
            return

        # Reset current booking selection to avoid stale time slot across doctors.
        self._reset_booking_selection()

        for index in range(self.cb_doc.count()):
            if self.cb_doc.itemData(index) == doctor_id:
                self.cb_doc.setCurrentIndex(index)
                QtWidgets.QMessageBox.information(
                    self,
                    "Lịch khám bác sĩ" if view_only else "Đặt lịch khám",
                    (
                        f"Đã chọn sẵn BS {doctor.get('name', '')}. Vui lòng chọn ngày và giờ để xem lịch trống."
                        if view_only
                        else f"Đã chọn sẵn BS {doctor.get('name', '')}. Vui lòng chọn ngày và giờ khám."
                    ),
                )
                return

    def show_change_password_placeholder(self):
        QtWidgets.QMessageBox.information(
            self,
            "Đổi mật khẩu",
            "Chức năng đổi mật khẩu đang được phát triển ở phiên bản tiếp theo.",
        )

    def create_navbar(self, active_index=0):
        nav = QtWidgets.QWidget(); nav.setFixedHeight(80); nav.setStyleSheet("background: white; border-bottom: 1px solid #eee;")
        nav_layout = QtWidgets.QHBoxLayout(nav); nav_layout.setContentsMargins(40, 0, 40, 0)
        logo = QtWidgets.QPushButton("⊕ CarePlus")
        logo.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        logo.setStyleSheet(
            "QPushButton {"
            " color: #69c0a5; font-size: 24px; font-weight: bold;"
            " border: none; background: transparent; padding: 0;"
            "}"
            "QPushButton:hover { color: #58a68e; }"
        )
        logo.clicked.connect(lambda: self.switch_patient_page(0))
        nav_layout.addWidget(logo); nav_layout.addStretch()
        nav_items = [("Trang chủ", 0), ("Dịch vụ", 1), ("Bác sĩ", 2), ("Tin tức", 3)]
        for text, page_index in nav_items:
            btn = QtWidgets.QPushButton(text)
            default_style = "QPushButton { border: none; padding: 10px 15px; color: #555; font-size: 15px; }"
            active_style = "QPushButton { border: none; padding: 10px 15px; color: #69c0a5; font-size: 15px; font-weight: bold; border-bottom: 2px solid #69c0a5; }"
            btn.setStyleSheet(active_style if active_index == page_index else default_style)
            btn.clicked.connect(lambda _, idx=page_index: self.switch_patient_page(idx))
            nav_layout.addWidget(btn)
        nav_layout.addStretch()
        
        user_btn = QtWidgets.QPushButton(f"👤 {self.username} ▿")
        user_btn.setStyleSheet("background: #f0f7f6; border-radius: 15px; padding: 8px 15px; font-weight: bold; color: #333;")
        user_btn.clicked.connect(lambda _, b=user_btn: self.show_menu(b))
        nav_layout.addWidget(user_btn)

        # ĐÃ SỬA: Gán vào biến self để không bị Garbage Collection xóa mất kết nối
        self.btn_logout_nav = QtWidgets.QPushButton("Đăng xuất")
        self.btn_logout_nav.setStyleSheet("background: #ffeded; color: #ff4d4f; border-radius: 10px; padding: 8px 15px; font-weight: bold;")
        self.btn_logout_nav.clicked.connect(self.logout)
        nav_layout.addWidget(self.btn_logout_nav)
        
        return nav

    def _update_dynamic_navbar(self):
        current_index = self.patient_stack.currentIndex()
        if current_index == 0:
            target_active = 0
        elif current_index == 1:
            target_active = 1
        elif current_index == 2:
            target_active = 2
        elif current_index == 3:
            target_active = 3
        else:
            target_active = 0

        for page in [
            self.page_service,
            self.page_doctor,
            self.page_news,
            self.page_history,
            self.page_profile,
        ]:
            layout = page.layout()
            if not layout or layout.count() == 0:
                continue

            first_item = layout.itemAt(0)
            old_nav = first_item.widget() if first_item else None
            if old_nav is not None:
                layout.removeWidget(old_nav)
                old_nav.deleteLater()

            layout.insertWidget(0, self.create_navbar(target_active))

    def show_menu(self, anchor_btn):
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet("QMenu { background: white; color: #333; border: 1px solid #eee; } QMenu::item { padding: 10px 30px; } QMenu::item:selected { background: #f8faff; color: #69c0a5; }")
        
        act_booking = menu.addAction("📅 Đặt lịch khám")
        act_history = menu.addAction("📋 Lịch sử khám")
        act_profile = menu.addAction("👤 Hồ sơ cá nhân")
        act_update_profile = menu.addAction("🛠️ Cập nhật thông tin")
        act_change_password = menu.addAction("🔒 Đổi mật khẩu")
        act_service = menu.addAction("🩺 Dịch vụ")
        act_doctor = menu.addAction("👨‍⚕️ Bác sĩ")
        act_news = menu.addAction("📰 Tin tức")
        act_dev = menu.addAction("🚧 Tính năng khác đang phát triển")

        act_booking.triggered.connect(lambda: self.switch_patient_page(0))
        act_service.triggered.connect(lambda: self.switch_patient_page(1))
        act_doctor.triggered.connect(lambda: self.switch_patient_page(2))
        act_news.triggered.connect(lambda: self.switch_patient_page(3))
        act_history.triggered.connect(lambda: self.switch_patient_page(4))
        act_profile.triggered.connect(lambda: self.switch_patient_page(5))
        act_update_profile.triggered.connect(lambda: self.switch_patient_page(5))
        act_change_password.triggered.connect(self.show_change_password_placeholder)
        act_dev.triggered.connect(
            lambda: QtWidgets.QMessageBox.information(
                self,
                "Thông báo",
                "Một số chức năng nâng cao đang trong quá trình phát triển.",
            )
        )
        
        menu.addSeparator()
        logout_act = menu.addAction("🚪 Đăng xuất")
        logout_act.triggered.connect(self.logout)
        menu.exec(anchor_btn.mapToGlobal(QtCore.QPoint(0, anchor_btn.height() + 5)))

    def _slot_button_style(self, selected=False, disabled=False):
        if disabled:
            return "background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 10px; color: #94a3b8; padding: 10px;"
        if selected:
            return "background: #e1f2ee; border: 1px solid #69c0a5; border-radius: 10px; color: #1a2a3a; padding: 10px; font-weight: bold;"
        return "background: white; border: 1px solid #eee; border-radius: 10px; color: #333; padding: 10px;"

    def _clear_time_grid(self):
        while self.time_grid.count():
            item = self.time_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def refresh_available_slots(self):
        if not hasattr(self, "time_grid"):
            return
        self.selected_time = None
        self._time_buttons = []
        self._clear_time_grid()

        doctor_id = self.cb_doc.currentData()
        service_id = self.cb_service.currentData()
        date_value = self.de_date.date().toString("yyyy-MM-dd")
        result = AppointmentController.get_available_slots(doctor_id, date_value, service_id)
        slots = result.get("slots", []) if isinstance(result, dict) else []
        if not slots:
            disabled = QtWidgets.QPushButton("Chưa có khung giờ")
            disabled.setEnabled(False)
            disabled.setStyleSheet(self._slot_button_style(disabled=True))
            self.time_grid.addWidget(disabled, 0, 0)
            self.booking_hint.setText(result.get("message", "Không có khung giờ khả dụng.") if isinstance(result, dict) else "Không có khung giờ khả dụng.")
            return

        for idx, slot in enumerate(slots):
            time_value = slot.get("time")
            available = bool(slot.get("available"))
            button = QtWidgets.QPushButton(f"{time_value}\n{'Còn trống' if available else 'Đã đặt'}")
            button.setEnabled(available)
            button.setStyleSheet(self._slot_button_style(disabled=not available))
            if available:
                button.clicked.connect(lambda _, selected=time_value: self.select_time_slot(selected))
            self._time_buttons.append(button)
            self.time_grid.addWidget(button, idx // 4, idx % 4)

        self.booking_hint.setText("Vui lòng chọn dịch vụ, ngày, bác sĩ và giờ khám.")

    def book_appointment(self):
        doc_id = self.cb_doc.currentData()
        service_name = self.cb_service.currentText().strip()
        date = self.de_date.date().toString("yyyy-MM-dd")
        patient_id = self.user_data.get("patient_id")

        if not self.selected_time:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng chọn khung giờ khám.")
            return

        confirm_msg = (
            f"Dịch vụ: {service_name}\n"
            f"Bác sĩ: {self.cb_doc.currentText()}\n"
            f"Ngày: {date}\n"
            f"Giờ: {self.selected_time}\n\n"
            "Bạn có muốn xác nhận đặt lịch không?"
        )
        reply = QtWidgets.QMessageBox.question(
            self,
            "Xác nhận đặt lịch",
            confirm_msg,
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        )
        if reply != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        if not doc_id or not patient_id:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Không thể đặt lịch do thiếu dữ liệu Bác sĩ hoặc Bệnh nhân")
            return

        result = AppointmentController.book_with_validation(
            patient_id,
            doc_id,
            service_name,
            date,
            self.selected_time,
            role="patient",
            user_context=self.user_data,
        )
        if result["status"]:
            QtWidgets.QMessageBox.information(self, "Thành công", result["message"])
            self._reset_booking_selection()
            self._reload_upcoming_appointments()
        else:
            QtWidgets.QMessageBox.warning(self, "Thất bại", result["message"])

    def select_time_slot(self, time_value):
        self.selected_time = time_value
        for button in self._time_buttons:
            button_time = button.text().split("\n", maxsplit=1)[0]
            if button_time == time_value:
                button.setStyleSheet(self._slot_button_style(selected=True))
            else:
                button.setStyleSheet(self._slot_button_style())
        self.booking_hint.setText(f"Đã chọn giờ khám: {time_value}")

    def _reset_booking_selection(self):
        self.selected_time = None
        self.booking_hint.setText("Vui lòng chọn dịch vụ, ngày, bác sĩ và giờ khám.")
        if self.cb_service.count() > 0:
            self.cb_service.setCurrentIndex(0)
        self.refresh_available_slots()

    def _reload_upcoming_appointments(self):
        if not hasattr(self, "appointment_list_layout"):
            return

        while self.appointment_list_layout.count() > 1:
            item = self.appointment_list_layout.takeAt(1)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.load_appointments(self.appointment_list_layout)

    def load_appointments(self, layout):
        patient_id = self.user_data.get("patient_id")
        if not patient_id:
            return
            
        appointments = AppointmentController.get_upcoming_by_patient(patient_id)
        if not appointments:
            layout.addWidget(QtWidgets.QLabel("Bạn chưa có lịch hẹn nào."))
            return
            
        # Lấy tối đa 3 lịch hẹn
        for appt in appointments[:3]:
            item = QtWidgets.QFrame(); item.setStyleSheet("background: #f9f9f9; border-radius: 12px; border: 1px solid #f0f0f0;")
            item_h = QtWidgets.QHBoxLayout(item)
            item_h.addWidget(QtWidgets.QLabel("📅"))
            
            import datetime
            if isinstance(appt["appointment_date"], datetime.datetime):
                dt_str = appt["appointment_date"].strftime("%d/%m/%Y • %H:%M")
            else:
                dt_str = str(appt["appointment_date"])
                
            info = QtWidgets.QLabel(f"<b style='color:#1a2a3a;'>BS {appt['doctor_name']}</b><br><span style='color:#333;'>{dt_str}</span><br><span style='color:#555;'>{appt.get('specialty', '')}</span>")
            
            stt = QtWidgets.QLabel(appt["status"])
            if appt["status"] == "pending":
                stt.setStyleSheet("background: #fff4e6; color: #fd7e14; padding: 5px 10px; border-radius: 8px; border:none; font-size: 11px;")
            elif appt["status"] == "confirmed":
                stt.setStyleSheet("background: #e0f2fe; color: #0369a1; padding: 5px 10px; border-radius: 8px; border:none; font-size: 11px;")
            elif appt["status"] == "in_progress":
                stt.setStyleSheet("background: #ede9fe; color: #5b21b6; padding: 5px 10px; border-radius: 8px; border:none; font-size: 11px;")
            else:
                stt.setStyleSheet("background: #f1f5f9; color: #475569; padding: 5px 10px; border-radius: 8px; border:none; font-size: 11px;")
                
            item_h.addWidget(info); item_h.addStretch(); item_h.addWidget(stt)
            layout.addWidget(item)

    def logout(self):
     reply = QtWidgets.QMessageBox.question(
        self,
        "Đăng xuất",
        "Bạn có chắc muốn đăng xuất không?",
        QtWidgets.QMessageBox.StandardButton.Yes |
        QtWidgets.QMessageBox.StandardButton.No
    )

     if reply == QtWidgets.QMessageBox.StandardButton.Yes:

        # Đóng giao diện hiện tại
        self.close()

        # Import LoginView
        from views.login_view import LoginView

        # Mở lại màn hình đăng nhập
        self.login_window = LoginView()
        self.login_window.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    login_screen = QtWidgets.QLabel("MÀN HÌNH ĐĂNG NHẬP (GIẢ LẬP)")
    login_screen.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    login_screen.resize(400, 300)
    login_screen.setStyleSheet("background: white; font-size: 20px; font-weight: bold;")
    
    window = MainView("patient", "Nguyễn Văn A", login_window=login_screen) 
    window.show()
    
    sys.exit(app.exec())
