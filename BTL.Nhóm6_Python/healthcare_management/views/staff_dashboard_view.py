from PyQt6 import QtWidgets, QtCore, QtGui
from controllers.patient_controller import PatientController
from controllers.appointment_controller import AppointmentController
from controllers.doctor_controller import DoctorController
from controllers.service_controller import ServiceController
from controllers.payment_controller import PaymentController
from controllers.settings_controller import SettingsController


class StaffDashboardView(QtWidgets.QWidget):
    def __init__(self, user_data=None):
        super().__init__()
        self.user_data = user_data or {"name": "Staff"}
        self.username = self.user_data.get("name") or self.user_data.get("username") or "Staff"
        self.intake_selected_patient = None
        self.intake_selected_appointment = None
        self.staff_appointment_selected_id = None
        self.staff_appointment_rows = []
        self.staff_patient_rows = []
        self.staff_patient_filtered_rows = []
        self.staff_patient_selected = None
        self.staff_billing_rows = []
        self.staff_billing_selected_id = None
        self.staff_billing_selected_status = ""
        self.staff_service_rows = []
        self.staff_service_filtered_rows = []
        self.staff_service_selected = None
        self.staff_notification_rows = []
        self.shared_selected_patient_id = None
        self.shared_selected_appointment_id = None
        self.shared_selected_service_name = ""

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QtWidgets.QFrame()
        self.sidebar.setFixedWidth(260)
        self.sidebar.setStyleSheet("background-color: white; border-right: 1px solid #e2e8f0;")
        sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 25, 15, 25)
        sidebar_layout.setSpacing(5)

        logo = QtWidgets.QLabel("⊕ CarePlus Staff")
        logo.setStyleSheet("color: #69c0a5; font-size: 22px; font-weight: 900; margin-bottom: 20px;")
        sidebar_layout.addWidget(logo)

        self.menu_items = [
            ("🏠", "Dashboard"),
            ("📝", "Tiếp nhận bệnh nhân"),
            ("📅", "Quản lý lịch hẹn"),
            ("👥", "Danh sách bệnh nhân"),
            ("💳", "Thanh toán & Hóa đơn"),
            ("🩺", "Dịch vụ & Gói khám"),
            ("🔔", "Thông báo"),
            ("📊", "Báo cáo"),
            ("⚙️", "Cài đặt"),
        ]

        self.nav_buttons = []
        for i, (icon, text) in enumerate(self.menu_items):
            btn = QtWidgets.QPushButton(f"   {icon}     {text}")
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(self._nav_button_style(is_active=(i == 0)))
            btn.clicked.connect(lambda checked, idx=i: self.switch_page(idx))
            self.nav_buttons.append(btn)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        self.btn_logout = QtWidgets.QPushButton("🚪    Đăng xuất")
        self.btn_logout.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_logout.setStyleSheet(
            "QPushButton { border: none; text-align: left; padding: 12px 15px; color: #ef4444; font-weight: 800; font-size: 14px; } "
            "QPushButton:hover { background: #fee2e2; border-radius: 10px; }"
        )
        sidebar_layout.addWidget(self.btn_logout)
        self.main_layout.addWidget(self.sidebar)

        # Main content
        right = QtWidgets.QWidget()
        right.setStyleSheet("background: #f8fafc;")
        right_layout = QtWidgets.QVBoxLayout(right)
        right_layout.setContentsMargins(25, 25, 25, 25)
        right_layout.setSpacing(15)

        topbar = QtWidgets.QFrame()
        topbar.setStyleSheet("background: white; border: 1px solid #e5e7eb; border-radius: 12px;")
        topbar_layout = QtWidgets.QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(20, 12, 20, 12)
        topbar_layout.setSpacing(10)

        welcome = QtWidgets.QLabel("Bảng điều khiển Nhân viên")
        welcome.setStyleSheet("font-size: 18px; font-weight: 800; color: #0f172a;")
        user_lbl = QtWidgets.QLabel(f"Nhân viên: {self.username}")
        user_lbl.setStyleSheet("font-size: 13px; color: #64748b; font-weight: 600;")

        topbar_layout.addWidget(welcome)
        topbar_layout.addStretch()
        topbar_layout.addWidget(user_lbl)

        self.content_stack = QtWidgets.QStackedWidget()
        self.content_stack.setStyleSheet("QStackedWidget { background: transparent; }")

        self.content_stack.addWidget(self._build_dashboard_page())
        self.content_stack.addWidget(self._build_patient_intake_page())
        self.content_stack.addWidget(self._build_appointment_management_page())
        self.content_stack.addWidget(self._build_staff_patient_list_page())
        self.content_stack.addWidget(self._build_staff_billing_page())
        self.content_stack.addWidget(self._build_staff_service_lookup_page())
        self.content_stack.addWidget(self._build_staff_notifications_page())
        self.content_stack.addWidget(self._build_staff_reports_page())
        self.content_stack.addWidget(self._build_staff_settings_page())

        right_layout.addWidget(topbar)
        right_layout.addWidget(self.content_stack, 1)
        self.main_layout.addWidget(right, 1)

    def _build_dashboard_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: white; border: 1px solid #e5e7eb; border-radius: 16px;")
        page_layout = QtWidgets.QVBoxLayout(page)
        page_layout.setContentsMargins(24, 24, 24, 24)
        page_layout.setSpacing(16)

        # KPI cards
        kpi_row = QtWidgets.QHBoxLayout()
        kpi_row.setSpacing(12)
        kpi_row.addWidget(self._build_kpi_card("Bệnh nhân hôm nay", "26", "+4 so với hôm qua", "#0ea5e9"))
        kpi_row.addWidget(self._build_kpi_card("Lịch hẹn hôm nay", "18", "5 lịch hẹn mới", "#3b82f6"))
        kpi_row.addWidget(self._build_kpi_card("Hóa đơn chờ thanh toán", "09", "Cần theo dõi tại quầy", "#f59e0b"))
        kpi_row.addWidget(self._build_kpi_card("Đã thanh toán hôm nay", "14", "Tổng tạm tính 21.4 triệu", "#10b981"))
        page_layout.addLayout(kpi_row)

        content_grid = QtWidgets.QGridLayout()
        content_grid.setHorizontalSpacing(14)
        content_grid.setVerticalSpacing(14)
        content_grid.setColumnStretch(0, 3)
        content_grid.setColumnStretch(1, 2)

        # Lịch hẹn hôm nay
        appointments_card = self._build_section_card("Lịch hẹn hôm nay")
        appointments_layout = appointments_card.layout()

        table = QtWidgets.QTableWidget(3, 6)
        table.setHorizontalHeaderLabels(["giờ hẹn", "bệnh nhân", "dịch vụ", "bác sĩ", "trạng thái", "thao tác"])
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        table.setAlternatingRowColors(True)
        table.setStyleSheet(
            "QTableWidget { border: 1px solid #e2e8f0; border-radius: 8px; background: #ffffff; gridline-color: #f1f5f9; }"
            "QHeaderView::section { background: #f8fafc; color: #334155; font-size: 12px; font-weight: 700; border: none; padding: 8px; }"
            "QTableWidget::item { padding: 8px; color: #0f172a; }"
            "QTableWidget::item:alternate { background: #f8fafc; }"
        )

        sample_rows = [
            ("08:30", "Nguyễn Minh T.", "Khám tổng quát", "BS. Thanh", "Chờ tiếp nhận", "Tiếp nhận"),
            ("09:10", "Lê Hoài A.", "Xét nghiệm máu", "BS. Huy", "Đang chờ", "Mở hồ sơ"),
            ("10:00", "", "", "", "", ""),
        ]
        for r, row in enumerate(sample_rows):
            for c, value in enumerate(row):
                table.setItem(r, c, QtWidgets.QTableWidgetItem(value))

        if not any(all(v.strip() for v in row) for row in sample_rows):
            empty_notice = QtWidgets.QLabel("Chưa có lịch hẹn cho hôm nay.")
            empty_notice.setStyleSheet("color: #64748b; font-size: 13px;")
            appointments_layout.addWidget(empty_notice)
        appointments_layout.addWidget(table)

        # Thao tác nhanh
        quick_actions = self._build_section_card("Thao tác nhanh")
        quick_layout = quick_actions.layout()
        quick_layout.addWidget(self._build_quick_action_button("Tiếp nhận bệnh nhân mới", "Mở trang tiếp nhận", 1, "#0ea5e9"))
        quick_layout.addWidget(self._build_quick_action_button("Quản lý lịch hẹn", "Đi tới lịch hẹn hôm nay", 2, "#6366f1"))
        quick_layout.addWidget(self._build_quick_action_button("Tra cứu danh sách bệnh nhân", "Mở hồ sơ bệnh nhân", 3, "#14b8a6"))
        quick_layout.addWidget(self._build_quick_action_button("Xử lý thanh toán", "Đi tới thanh toán & hóa đơn", 4, "#f59e0b"))
        quick_layout.addStretch()

        # Bệnh nhân chờ tiếp nhận
        waiting_card = self._build_section_card("Bệnh nhân chờ tiếp nhận")
        waiting_layout = waiting_card.layout()
        waiting_list = QtWidgets.QListWidget()
        waiting_list.addItems([
            "STT 12 - Trần Mai K. | 08:45 | Khám nội tổng hợp",
            "STT 13 - Phạm Quốc B. | 09:00 | Tư vấn dịch vụ",
        ])
        waiting_list.setStyleSheet("QListWidget { border: 1px solid #e2e8f0; border-radius: 8px; padding: 4px; }")
        waiting_layout.addWidget(waiting_list)
        waiting_empty = QtWidgets.QLabel("Khi không có bệnh nhân chờ, danh sách sẽ hiển thị trống.")
        waiting_empty.setStyleSheet("color: #64748b; font-size: 12px;")
        waiting_layout.addWidget(waiting_empty)

        # Thông báo
        notices_card = self._build_section_card("Thông báo")
        notices_layout = notices_card.layout()
        notices_list = QtWidgets.QListWidget()
        notices_list.addItems([
            "• 08:20 - Nhắc lịch: BN Lê Hoài A. đến sau 10 phút.",
            "• 08:05 - Hệ thống: Cập nhật biểu phí xét nghiệm đã áp dụng.",
        ])
        notices_list.setStyleSheet("QListWidget { border: 1px solid #e2e8f0; border-radius: 8px; padding: 4px; }")
        notices_layout.addWidget(notices_list)
        notice_empty = QtWidgets.QLabel("Nếu chưa có thông báo mới, khu vực này hiển thị: 'Không có thông báo'.")
        notice_empty.setStyleSheet("color: #64748b; font-size: 12px;")
        notices_layout.addWidget(notice_empty)

        # Thống kê dịch vụ (lightweight)
        services_card = self._build_section_card("Thống kê dịch vụ")
        services_layout = services_card.layout()
        service_data = [
            ("Khám tổng quát", 40),
            ("Xét nghiệm máu", 25),
            ("Siêu âm", 20),
            ("Tiêm chủng", 15),
        ]
        for name, pct in service_data:
            row = QtWidgets.QWidget()
            row_layout = QtWidgets.QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(10)
            label = QtWidgets.QLabel(name)
            label.setMinimumWidth(130)
            bar = QtWidgets.QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(pct)
            bar.setTextVisible(True)
            bar.setFormat(f"{pct}%")
            bar.setStyleSheet(
                "QProgressBar { border: 1px solid #dbeafe; border-radius: 6px; text-align: center; background: #eff6ff; }"
                "QProgressBar::chunk { background-color: #60a5fa; border-radius: 5px; }"
            )
            row_layout.addWidget(label)
            row_layout.addWidget(bar, 1)
            services_layout.addWidget(row)

        # Công việc hôm nay
        todo_card = self._build_section_card("Công việc hôm nay")
        todo_layout = todo_card.layout()
        checklist = [
            ("Đối soát lịch hẹn buổi sáng", True),
            ("Gọi xác nhận 3 lịch hẹn chiều", False),
            ("Kiểm tra hóa đơn chờ thanh toán", False),
        ]
        for text, checked in checklist:
            cb = QtWidgets.QCheckBox(text)
            cb.setChecked(checked)
            cb.setStyleSheet("QCheckBox { color: #1e293b; font-size: 13px; }")
            todo_layout.addWidget(cb)
        todo_empty = QtWidgets.QLabel("Không có công việc mới sẽ hiển thị danh sách trống.")
        todo_empty.setStyleSheet("color: #64748b; font-size: 12px;")
        todo_layout.addWidget(todo_empty)

        content_grid.addWidget(appointments_card, 0, 0)
        content_grid.addWidget(quick_actions, 0, 1)
        content_grid.addWidget(waiting_card, 1, 0)
        content_grid.addWidget(notices_card, 1, 1)
        content_grid.addWidget(services_card, 2, 0)
        content_grid.addWidget(todo_card, 2, 1)

        page_layout.addLayout(content_grid)
        return page

    def _build_placeholder_page(self, title):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: white; border: 1px solid #e5e7eb; border-radius: 16px;")
        page_layout = QtWidgets.QVBoxLayout(page)
        page_layout.setContentsMargins(32, 32, 32, 32)
        page_layout.setSpacing(12)

        heading = QtWidgets.QLabel(title)
        heading.setStyleSheet("font-size: 26px; color: #0f172a; font-weight: 900;")
        sub = QtWidgets.QLabel(f"Trang {title} đang sẵn sàng để tích hợp nghiệp vụ ở các task tiếp theo.")
        sub.setWordWrap(True)
        sub.setStyleSheet("font-size: 14px; color: #64748b;")

        page_layout.addWidget(heading)
        page_layout.addWidget(sub)
        page_layout.addStretch()
        return page

    def _build_staff_notifications_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: white; border: 1px solid #e5e7eb; border-radius: 16px;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        heading = QtWidgets.QLabel("Thông báo vận hành")
        heading.setStyleSheet("font-size: 24px; color: #0f172a; font-weight: 900;")
        sub = QtWidgets.QLabel("Theo dõi lịch hẹn mới/hủy, bệnh nhân chờ khám và hóa đơn chưa thanh toán theo thời gian thực.")
        sub.setStyleSheet("font-size: 13px; color: #64748b;")
        sub.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(sub)

        actions = QtWidgets.QHBoxLayout()
        actions.setSpacing(8)
        refresh_btn = QtWidgets.QPushButton("🔄 Làm mới")
        refresh_btn.setStyleSheet("background: #0ea5e9; color: white; padding: 8px 12px; border-radius: 6px; font-weight: 700;")
        refresh_btn.clicked.connect(self._refresh_staff_notifications)
        clear_btn = QtWidgets.QPushButton("✅ Đánh dấu đã xử lý")
        clear_btn.setStyleSheet("background: #e2e8f0; color: #0f172a; padding: 8px 12px; border-radius: 6px; font-weight: 700;")
        clear_btn.clicked.connect(self._mark_notification_as_handled)
        actions.addWidget(refresh_btn)
        actions.addWidget(clear_btn)
        actions.addStretch()
        layout.addLayout(actions)

        self.staff_notification_feedback = QtWidgets.QLabel("Danh sách thông báo sẽ hiển thị tại đây.")
        self.staff_notification_feedback.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 600;")
        layout.addWidget(self.staff_notification_feedback)

        feed_card = self._build_section_card("Feed thông báo")
        self.staff_notification_table = QtWidgets.QTableWidget(0, 4)
        self.staff_notification_table.setHorizontalHeaderLabels(["Loại", "Nội dung", "Thời điểm", "Trạng thái"])
        self.staff_notification_table.verticalHeader().setVisible(False)
        self.staff_notification_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.staff_notification_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.staff_notification_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_notification_table.setAlternatingRowColors(True)
        self.staff_notification_table.horizontalHeader().setStretchLastSection(True)
        self.staff_notification_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_notification_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staff_notification_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_notification_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_notification_table.setMinimumHeight(300)
        feed_card.layout().addWidget(self.staff_notification_table)
        layout.addWidget(feed_card, 1)

        self._refresh_staff_notifications()
        return page

    def _build_staff_reports_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: white; border: 1px solid #e5e7eb; border-radius: 16px;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        heading = QtWidgets.QLabel("Báo cáo nhanh trong ngày")
        heading.setStyleSheet("font-size: 24px; color: #0f172a; font-weight: 900;")
        sub = QtWidgets.QLabel("KPI vận hành ở quầy: lượt bệnh nhân, lịch hẹn, doanh thu đã thu và số tiền còn chờ thanh toán.")
        sub.setStyleSheet("font-size: 13px; color: #64748b;")
        sub.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(sub)

        self.staff_report_kpi_row = QtWidgets.QHBoxLayout()
        self.staff_report_kpi_row.setSpacing(12)
        layout.addLayout(self.staff_report_kpi_row)

        summary_card = self._build_section_card("Tóm tắt ca trực")
        self.staff_report_summary_lbl = QtWidgets.QLabel("Dữ liệu báo cáo sẽ hiển thị sau khi tải.")
        self.staff_report_summary_lbl.setWordWrap(True)
        self.staff_report_summary_lbl.setStyleSheet("font-size: 13px; color: #334155;")
        summary_card.layout().addWidget(self.staff_report_summary_lbl)
        layout.addWidget(summary_card)

        reports_actions = QtWidgets.QHBoxLayout()
        reports_actions.setSpacing(8)
        refresh_btn = QtWidgets.QPushButton("🔄 Cập nhật KPI")
        refresh_btn.setStyleSheet("background: #2563eb; color: white; padding: 8px 12px; border-radius: 6px; font-weight: 700;")
        refresh_btn.clicked.connect(self._refresh_staff_reports)
        reports_actions.addWidget(refresh_btn)
        reports_actions.addStretch()
        layout.addLayout(reports_actions)

        self._refresh_staff_reports()
        return page

    def _build_staff_settings_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: white; border: 1px solid #e5e7eb; border-radius: 16px;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        heading = QtWidgets.QLabel("Cài đặt cá nhân")
        heading.setStyleSheet("font-size: 24px; color: #0f172a; font-weight: 900;")
        sub = QtWidgets.QLabel("Cập nhật thông tin cá nhân, đổi mật khẩu và đăng xuất khỏi phiên làm việc hiện tại.")
        sub.setStyleSheet("font-size: 13px; color: #64748b;")
        sub.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(sub)

        profile_card = self._build_section_card("1) Hồ sơ cá nhân")
        profile_form = QtWidgets.QGridLayout()
        profile_form.setHorizontalSpacing(10)
        profile_form.setVerticalSpacing(8)

        self.staff_settings_name_input = QtWidgets.QLineEdit(str(self.user_data.get("name") or self.user_data.get("username") or ""))
        self.staff_settings_phone_input = QtWidgets.QLineEdit(str(self.user_data.get("phone") or ""))
        self.staff_settings_email_input = QtWidgets.QLineEdit(str(self.user_data.get("email") or ""))

        profile_form.addWidget(QtWidgets.QLabel("Họ tên *:"), 0, 0)
        profile_form.addWidget(self.staff_settings_name_input, 0, 1)
        profile_form.addWidget(QtWidgets.QLabel("SĐT:"), 1, 0)
        profile_form.addWidget(self.staff_settings_phone_input, 1, 1)
        profile_form.addWidget(QtWidgets.QLabel("Email:"), 2, 0)
        profile_form.addWidget(self.staff_settings_email_input, 2, 1)

        save_profile_btn = QtWidgets.QPushButton("💾 Lưu thông tin")
        save_profile_btn.setStyleSheet("background: #22c55e; color: white; padding: 8px 12px; border-radius: 6px; font-weight: 700;")
        save_profile_btn.clicked.connect(self._handle_staff_profile_update)
        profile_form.addWidget(save_profile_btn, 0, 2, 3, 1)

        profile_card.layout().addLayout(profile_form)
        self.staff_settings_profile_feedback = QtWidgets.QLabel("Chưa có thay đổi mới.")
        self.staff_settings_profile_feedback.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 600;")
        profile_card.layout().addWidget(self.staff_settings_profile_feedback)
        layout.addWidget(profile_card)

        password_card = self._build_section_card("2) Đổi mật khẩu")
        password_form = QtWidgets.QGridLayout()
        password_form.setHorizontalSpacing(10)
        password_form.setVerticalSpacing(8)

        self.staff_settings_current_password_input = QtWidgets.QLineEdit()
        self.staff_settings_current_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.staff_settings_new_password_input = QtWidgets.QLineEdit()
        self.staff_settings_new_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.staff_settings_confirm_password_input = QtWidgets.QLineEdit()
        self.staff_settings_confirm_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        password_form.addWidget(QtWidgets.QLabel("Mật khẩu hiện tại *:"), 0, 0)
        password_form.addWidget(self.staff_settings_current_password_input, 0, 1)
        password_form.addWidget(QtWidgets.QLabel("Mật khẩu mới *:"), 1, 0)
        password_form.addWidget(self.staff_settings_new_password_input, 1, 1)
        password_form.addWidget(QtWidgets.QLabel("Xác nhận mật khẩu mới *:"), 2, 0)
        password_form.addWidget(self.staff_settings_confirm_password_input, 2, 1)

        change_password_btn = QtWidgets.QPushButton("🔒 Cập nhật mật khẩu")
        change_password_btn.setStyleSheet("background: #1d4ed8; color: white; padding: 8px 12px; border-radius: 6px; font-weight: 700;")
        change_password_btn.clicked.connect(self._handle_staff_password_change)
        password_form.addWidget(change_password_btn, 0, 2, 3, 1)

        password_card.layout().addLayout(password_form)
        self.staff_settings_password_feedback = QtWidgets.QLabel("Mật khẩu mới cần tối thiểu 8 ký tự.")
        self.staff_settings_password_feedback.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 600;")
        password_card.layout().addWidget(self.staff_settings_password_feedback)
        layout.addWidget(password_card)

        session_card = self._build_section_card("3) Phiên đăng nhập")
        logout_hint = QtWidgets.QLabel("Nút đăng xuất bên trái vẫn dùng cùng luồng logout của MainView để đảm bảo tương thích hệ thống.")
        logout_hint.setWordWrap(True)
        logout_hint.setStyleSheet("font-size: 12px; color: #475569;")
        session_card.layout().addWidget(logout_hint)

        trigger_logout_btn = QtWidgets.QPushButton("🚪 Đăng xuất ngay")
        trigger_logout_btn.setStyleSheet("background: #ef4444; color: white; padding: 8px 12px; border-radius: 6px; font-weight: 700;")
        trigger_logout_btn.clicked.connect(self.btn_logout.click)
        session_card.layout().addWidget(trigger_logout_btn, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(session_card)
        layout.addStretch()
        return page

    def _build_patient_intake_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: white; border: 1px solid #e5e7eb; border-radius: 16px;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        heading = QtWidgets.QLabel("Tiếp nhận bệnh nhân")
        heading.setStyleSheet("font-size: 24px; color: #0f172a; font-weight: 900;")
        sub = QtWidgets.QLabel("Tra cứu theo CCCD/SĐT, tạo hồ sơ cơ bản và xác nhận check-in vào hàng chờ khám.")
        sub.setStyleSheet("font-size: 13px; color: #64748b;")
        sub.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(sub)

        lookup_card = self._build_section_card("1) Tra cứu hồ sơ")
        lookup_form = QtWidgets.QGridLayout()
        lookup_form.setHorizontalSpacing(10)
        lookup_form.setVerticalSpacing(8)

        self.intake_cccd_input = QtWidgets.QLineEdit()
        self.intake_cccd_input.setPlaceholderText("Nhập CCCD")
        self.intake_phone_input = QtWidgets.QLineEdit()
        self.intake_phone_input.setPlaceholderText("Nhập số điện thoại")

        lookup_form.addWidget(QtWidgets.QLabel("CCCD:"), 0, 0)
        lookup_form.addWidget(self.intake_cccd_input, 0, 1)
        lookup_form.addWidget(QtWidgets.QLabel("SĐT:"), 1, 0)
        lookup_form.addWidget(self.intake_phone_input, 1, 1)

        btn_lookup = QtWidgets.QPushButton("🔍 Tra cứu")
        btn_lookup.setStyleSheet("background: #0ea5e9; color: white; padding: 8px 12px; border-radius: 6px; font-weight: 700;")
        btn_lookup.clicked.connect(self._handle_intake_lookup)
        lookup_form.addWidget(btn_lookup, 0, 2, 2, 1)

        lookup_card.layout().addLayout(lookup_form)
        layout.addWidget(lookup_card)

        profile_card = self._build_section_card("2) Hồ sơ bệnh nhân")
        profile_form = QtWidgets.QGridLayout()
        profile_form.setHorizontalSpacing(10)
        profile_form.setVerticalSpacing(8)

        self.intake_name_input = QtWidgets.QLineEdit()
        self.intake_dob_input = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.intake_dob_input.setCalendarPopup(True)
        self.intake_gender_input = QtWidgets.QComboBox()
        self.intake_gender_input.addItems(["Nam", "Nữ"])
        self.intake_address_input = QtWidgets.QLineEdit()

        profile_form.addWidget(QtWidgets.QLabel("Họ tên *:"), 0, 0)
        profile_form.addWidget(self.intake_name_input, 0, 1)
        profile_form.addWidget(QtWidgets.QLabel("Ngày sinh *:"), 1, 0)
        profile_form.addWidget(self.intake_dob_input, 1, 1)
        profile_form.addWidget(QtWidgets.QLabel("Giới tính *:"), 2, 0)
        profile_form.addWidget(self.intake_gender_input, 2, 1)
        profile_form.addWidget(QtWidgets.QLabel("Địa chỉ *:"), 3, 0)
        profile_form.addWidget(self.intake_address_input, 3, 1)

        btn_create_or_update = QtWidgets.QPushButton("💾 Tạo/Cập nhật hồ sơ")
        btn_create_or_update.setStyleSheet("background: #10b981; color: white; padding: 8px 12px; border-radius: 6px; font-weight: 700;")
        btn_create_or_update.clicked.connect(self._handle_intake_create_or_update)
        profile_form.addWidget(btn_create_or_update, 0, 2, 4, 1)

        profile_card.layout().addLayout(profile_form)
        layout.addWidget(profile_card)

        queue_card = self._build_section_card("3) Check-in vào hàng chờ")
        queue_layout = queue_card.layout()
        self.intake_patient_summary = QtWidgets.QLabel("Chưa chọn bệnh nhân.")
        self.intake_patient_summary.setStyleSheet("font-size: 13px; color: #334155;")
        self.intake_appointment_summary = QtWidgets.QLabel("Chưa tìm thấy lịch hẹn phù hợp.")
        self.intake_appointment_summary.setStyleSheet("font-size: 13px; color: #64748b;")

        btn_checkin = QtWidgets.QPushButton("✅ Xác nhận check-in")
        btn_checkin.setStyleSheet("background: #6366f1; color: white; padding: 8px 12px; border-radius: 6px; font-weight: 700;")
        btn_checkin.clicked.connect(self._handle_intake_checkin)

        self.intake_feedback = QtWidgets.QLabel("")
        self.intake_feedback.setWordWrap(True)
        self.intake_feedback.setStyleSheet("font-size: 13px; color: #1e293b;")

        queue_layout.addWidget(self.intake_patient_summary)
        queue_layout.addWidget(self.intake_appointment_summary)
        queue_layout.addWidget(btn_checkin)
        queue_layout.addWidget(self.intake_feedback)
        layout.addWidget(queue_card)

        layout.addStretch()
        return page

    def _build_staff_service_lookup_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: white; border: 1px solid #e5e7eb; border-radius: 16px;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        heading = QtWidgets.QLabel("Dịch vụ & Gói khám")
        heading.setStyleSheet("font-size: 24px; color: #0f172a; font-weight: 900;")
        sub = QtWidgets.QLabel(
            "Tra cứu danh mục dịch vụ cho tư vấn/đặt lịch và chọn nhanh để điền sẵn thông tin vào luồng nhân viên."
        )
        sub.setStyleSheet("font-size: 13px; color: #64748b;")
        sub.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(sub)

        filter_card = self._build_section_card("Bộ lọc tra cứu")
        filter_row = QtWidgets.QHBoxLayout()
        filter_row.setSpacing(8)

        self.staff_service_search_input = QtWidgets.QLineEdit()
        self.staff_service_search_input.setPlaceholderText("Tìm theo tên dịch vụ...")

        self.staff_service_type_combo = QtWidgets.QComboBox()
        self.staff_service_type_combo.addItem("Tất cả loại", "__all__")

        search_btn = QtWidgets.QPushButton("Tìm kiếm")
        search_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        search_btn.clicked.connect(self._refresh_staff_service_lookup)
        search_btn.setStyleSheet(
            "QPushButton { background: #0ea5e9; color: white; border: none; border-radius: 8px; padding: 8px 14px; font-weight: 700; }"
            "QPushButton:hover { background: #0284c7; }"
        )

        clear_btn = QtWidgets.QPushButton("Xóa lọc")
        clear_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        clear_btn.clicked.connect(self._handle_clear_staff_service_filters)

        filter_row.addWidget(self.staff_service_search_input, 1)
        filter_row.addWidget(self.staff_service_type_combo)
        filter_row.addWidget(search_btn)
        filter_row.addWidget(clear_btn)
        filter_card.layout().addLayout(filter_row)
        layout.addWidget(filter_card)

        table_card = self._build_section_card("Danh sách dịch vụ")
        self.staff_service_table = QtWidgets.QTableWidget(0, 5)
        self.staff_service_table.setHorizontalHeaderLabels(["ID", "Tên dịch vụ", "Loại", "Giá", "Tóm tắt"])
        self.staff_service_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.staff_service_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.staff_service_table.itemSelectionChanged.connect(self._handle_staff_service_selection)
        self.staff_service_table.horizontalHeader().setStretchLastSection(True)
        self.staff_service_table.verticalHeader().setVisible(False)
        table_card.layout().addWidget(self.staff_service_table)

        self.staff_service_lookup_empty = QtWidgets.QLabel("Chưa có dữ liệu dịch vụ để hiển thị.")
        self.staff_service_lookup_empty.setStyleSheet("font-size: 13px; color: #64748b;")
        table_card.layout().addWidget(self.staff_service_lookup_empty)
        layout.addWidget(table_card)

        select_card = self._build_section_card("Dịch vụ đã chọn")
        self.staff_service_selected_label = QtWidgets.QLabel("Chưa chọn dịch vụ nào.")
        self.staff_service_selected_label.setWordWrap(True)
        self.staff_service_selected_label.setStyleSheet("font-size: 13px; color: #1e293b;")

        select_btn = QtWidgets.QPushButton("Chọn dịch vụ cho luồng làm việc")
        select_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        select_btn.clicked.connect(self._apply_selected_staff_service_context)
        select_btn.setStyleSheet(
            "QPushButton { background: #10b981; color: white; border: none; border-radius: 8px; padding: 8px 14px; font-weight: 700; }"
            "QPushButton:hover { background: #059669; }"
        )

        self.staff_service_feedback = QtWidgets.QLabel("")
        self.staff_service_feedback.setWordWrap(True)
        self.staff_service_feedback.setStyleSheet("font-size: 13px; color: #0f766e; font-weight: 600;")

        select_layout = select_card.layout()
        select_layout.addWidget(self.staff_service_selected_label)
        select_layout.addWidget(select_btn)
        select_layout.addWidget(self.staff_service_feedback)
        layout.addWidget(select_card)

        layout.addStretch()

        self._load_staff_service_type_options()
        self._refresh_staff_service_lookup()
        self.staff_service_search_input.returnPressed.connect(self._refresh_staff_service_lookup)
        self.staff_service_type_combo.currentIndexChanged.connect(self._refresh_staff_service_lookup)
        return page

    def _load_staff_service_type_options(self):
        services = ServiceController.get_all() or []
        self.staff_service_rows = services

        seen_types = set()
        for s in services:
            service_type = self._extract_staff_service_type(s)
            if service_type and service_type not in seen_types:
                seen_types.add(service_type)
                self.staff_service_type_combo.addItem(service_type, service_type)

    def _extract_staff_service_type(self, service):
        return str(
            service.get("service_type")
            or service.get("type")
            or service.get("category")
            or "Chưa phân loại"
        ).strip()

    def _refresh_staff_service_lookup(self):
        if not hasattr(self, "staff_service_table"):
            return

        if not self.staff_service_rows:
            self.staff_service_rows = ServiceController.get_all() or []

        keyword = str(self.staff_service_search_input.text() or "").strip().lower()
        selected_type = str(self.staff_service_type_combo.currentData() or "__all__")

        filtered = []
        for s in self.staff_service_rows:
            service_name = str(s.get("service_name") or s.get("name") or "").strip()
            service_type = self._extract_staff_service_type(s)
            type_ok = selected_type == "__all__" or service_type == selected_type
            name_ok = not keyword or keyword in service_name.lower()
            if type_ok and name_ok:
                filtered.append(s)

        self.staff_service_filtered_rows = filtered
        self.staff_service_table.setRowCount(len(filtered))

        for row, s in enumerate(filtered):
            service_id = s.get("service_id")
            service_name = str(s.get("service_name") or s.get("name") or "")
            service_type = self._extract_staff_service_type(s)
            price = s.get("price")
            summary = str(s.get("description") or s.get("summary") or "")

            self.staff_service_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(service_id or "")))
            self.staff_service_table.setItem(row, 1, QtWidgets.QTableWidgetItem(service_name))
            self.staff_service_table.setItem(row, 2, QtWidgets.QTableWidgetItem(service_type))
            self.staff_service_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(price or "")))
            self.staff_service_table.setItem(row, 4, QtWidgets.QTableWidgetItem(summary))

        self.staff_service_table.resizeColumnsToContents()
        if not filtered:
            self.staff_service_lookup_empty.setText("Không có dịch vụ phù hợp bộ lọc hiện tại.")
        else:
            self.staff_service_lookup_empty.setText(f"Hiển thị {len(filtered)} dịch vụ.")

    def _handle_clear_staff_service_filters(self):
        self.staff_service_search_input.clear()
        self.staff_service_type_combo.setCurrentIndex(0)
        self._refresh_staff_service_lookup()
        self._set_staff_service_feedback("Đã xóa bộ lọc tra cứu.", is_error=False)

    def _handle_staff_service_selection(self):
        selected = self.staff_service_table.selectedItems()
        if not selected:
            return

        row = selected[0].row()
        if row < 0 or row >= len(self.staff_service_filtered_rows):
            return

        service = self.staff_service_filtered_rows[row]
        self.staff_service_selected = service
        service_name = str(service.get("service_name") or service.get("name") or "")
        service_type = self._extract_staff_service_type(service)
        price = str(service.get("price") or "")

        self.staff_service_selected_label.setText(
            f"Đã chọn: #{service.get('service_id', '')} - {service_name} | Loại: {service_type} | Giá: {price}"
        )

    def _apply_selected_staff_service_context(self):
        if not self.staff_service_selected:
            self._set_staff_service_feedback("Vui lòng chọn một dịch vụ trước khi áp dụng.", is_error=True)
            return

        service_name = str(self.staff_service_selected.get("service_name") or self.staff_service_selected.get("name") or "").strip()
        service_price = self.staff_service_selected.get("price")

        if hasattr(self, "staff_appt_service_combo") and self.staff_appt_service_combo.count() > 0:
            service_index = self.staff_appt_service_combo.findData(service_name)
            if service_index < 0:
                service_index = self.staff_appt_service_combo.findText(service_name)
            if service_index >= 0:
                self.staff_appt_service_combo.setCurrentIndex(service_index)

        if hasattr(self, "staff_bill_amount_input") and service_price is not None:
            current_amount = str(self.staff_bill_amount_input.text() or "").strip()
            if not current_amount:
                self.staff_bill_amount_input.setText(str(service_price))

        self.shared_selected_service_name = service_name

        self._set_staff_service_feedback(
            "Đã áp dụng dịch vụ đã chọn vào ngữ cảnh đặt lịch/thanh toán (dịch vụ lịch hẹn + gợi ý tổng tiền).",
            is_error=False,
        )

    def _apply_shared_context_to_appointment_form(self):
        if self.shared_selected_patient_id is not None:
            self.staff_appt_patient_id_input.setText(str(self.shared_selected_patient_id))

        if self.shared_selected_service_name:
            service_index = self.staff_appt_service_combo.findData(self.shared_selected_service_name)
            if service_index < 0:
                service_index = self.staff_appt_service_combo.findText(self.shared_selected_service_name)
            if service_index >= 0:
                self.staff_appt_service_combo.setCurrentIndex(service_index)

    def _apply_shared_context_to_billing_form(self):
        if self.shared_selected_patient_id is not None:
            self.staff_bill_patient_id_input.setText(str(self.shared_selected_patient_id))
        if self.shared_selected_appointment_id is not None:
            self.staff_bill_appointment_id_input.setText(str(self.shared_selected_appointment_id))

        if self.shared_selected_service_name:
            current_amount = str(self.staff_bill_amount_input.text() or "").strip()
            if not current_amount:
                suggested_amount = self._get_service_price_suggestion(self.shared_selected_service_name)
                if suggested_amount is not None:
                    self.staff_bill_amount_input.setText(str(suggested_amount))

    def _get_service_price_suggestion(self, service_name):
        service_name_norm = str(service_name or "").strip().lower()
        if not service_name_norm:
            return None

        for row in self.staff_service_rows:
            row_name = str(row.get("service_name") or row.get("name") or "").strip().lower()
            if row_name == service_name_norm:
                return row.get("price")
        return None

    def _set_staff_service_feedback(self, message, is_error=False):
        color = "#b91c1c" if is_error else "#0f766e"
        self.staff_service_feedback.setStyleSheet(f"font-size: 13px; color: {color}; font-weight: 600;")
        self.staff_service_feedback.setText(message)

    def _set_intake_feedback(self, message, is_error=False):
        color = "#b91c1c" if is_error else "#0f766e"
        self.intake_feedback.setStyleSheet(f"font-size: 13px; color: {color}; font-weight: 600;")
        self.intake_feedback.setText(message)

    def _handle_intake_lookup(self):
        cccd = self.intake_cccd_input.text().strip()
        phone = self.intake_phone_input.text().strip()
        if not cccd and not phone:
            self._set_intake_feedback("Vui lòng nhập CCCD hoặc SĐT để tra cứu.", is_error=True)
            return

        try:
            patient = PatientController.find_by_cccd_or_phone(cccd=cccd, phone=phone)
        except Exception:
            self._set_intake_feedback(
                "Tra cứu bị gián đoạn tạm thời. Vui lòng kiểm tra kết nối dữ liệu và thử lại.",
                is_error=True,
            )
            return
        if not patient:
            self.intake_selected_patient = None
            self.intake_selected_appointment = None
            self.intake_patient_summary.setText("Không tìm thấy hồ sơ bệnh nhân theo CCCD/SĐT đã nhập.")
            self.intake_appointment_summary.setText("Chưa có lịch hẹn để check-in.")
            self._set_intake_feedback("Không tìm thấy hồ sơ. Vui lòng tạo mới thông tin bệnh nhân.", is_error=True)
            return

        self.intake_selected_patient = patient
        self.intake_name_input.setText(str(patient.get("name") or ""))
        self.intake_phone_input.setText(str(patient.get("phone") or ""))
        self.intake_address_input.setText(str(patient.get("address") or ""))
        gender = str(patient.get("gender") or "Nam")
        self.intake_gender_input.setCurrentText(gender if gender in {"Nam", "Nữ"} else "Nam")

        dob_str = str(patient.get("dob") or "")
        dob = QtCore.QDate.fromString(dob_str, "yyyy-MM-dd")
        if dob.isValid():
            self.intake_dob_input.setDate(dob)

        patient_id = patient.get("patient_id")
        self.shared_selected_patient_id = patient_id
        appts = AppointmentController.get_by_patient(patient_id) or []
        checkin_target = None
        for appt in appts:
            if str(appt.get("status") or "").lower() in {"pending", "confirmed"}:
                checkin_target = appt
                break
        self.intake_selected_appointment = checkin_target
        self.shared_selected_appointment_id = checkin_target.get("appointment_id") if checkin_target else None
        self.shared_selected_service_name = self._extract_service_name_from_note(str((checkin_target or {}).get("note") or ""))

        self.intake_patient_summary.setText(
            f"Đã chọn BN #{patient_id}: {patient.get('name', '')} - SĐT: {patient.get('phone', '')}"
        )
        if checkin_target:
            self.intake_appointment_summary.setText(
                "Lịch hẹn sẵn sàng check-in: "
                f"#{checkin_target.get('appointment_id')} | BS {checkin_target.get('doctor_name', '')} | "
                f"{checkin_target.get('appointment_date', '')}"
            )
        else:
            self.intake_appointment_summary.setText("Không có lịch hẹn pending/confirmed để check-in.")

        extra = " (CCCD hiện đang đối soát qua SĐT do schema chưa có cột CCCD)." if cccd and not phone else ""
        self._set_intake_feedback("Tra cứu thành công." + extra, is_error=False)

    def _handle_intake_create_or_update(self):
        name = self.intake_name_input.text().strip()
        phone = self.intake_phone_input.text().strip()
        address = self.intake_address_input.text().strip()
        dob = self.intake_dob_input.date().toString("yyyy-MM-dd")
        gender = self.intake_gender_input.currentText()

        if not name or not phone or not address or not dob or not gender:
            self._set_intake_feedback("Thiếu thông tin bắt buộc: Họ tên, SĐT, ngày sinh, giới tính, địa chỉ.", is_error=True)
            return

        payload = {
            "name": name,
            "dob": dob,
            "gender": gender,
            "phone": phone,
            "address": address,
        }

        if self.intake_selected_patient and self.intake_selected_patient.get("patient_id"):
            patient_id = self.intake_selected_patient.get("patient_id")
            ok = PatientController.update(patient_id, payload)
            if not ok:
                self._set_intake_feedback("Cập nhật hồ sơ thất bại. Vui lòng thử lại.", is_error=True)
                return
            self.intake_selected_patient = PatientController.find_by_cccd_or_phone(phone=phone)
            if self.intake_selected_patient:
                self.shared_selected_patient_id = self.intake_selected_patient.get("patient_id")
            self._set_intake_feedback("Cập nhật hồ sơ bệnh nhân thành công.", is_error=False)
            return

        ok = PatientController.create(payload)
        if not ok:
            self._set_intake_feedback("Tạo hồ sơ bệnh nhân mới thất bại. Vui lòng thử lại.", is_error=True)
            return

        created = PatientController.find_by_cccd_or_phone(phone=phone)
        self.intake_selected_patient = created
        if created:
            self.shared_selected_patient_id = created.get("patient_id")
            self.intake_patient_summary.setText(
                f"Đã tạo hồ sơ mới BN #{created.get('patient_id')}: {created.get('name', '')} - SĐT: {created.get('phone', '')}"
            )
        self._set_intake_feedback("Tạo hồ sơ bệnh nhân mới thành công.", is_error=False)

    def _handle_intake_checkin(self):
        if not self.intake_selected_patient:
            self._set_intake_feedback("Chưa có bệnh nhân để check-in. Vui lòng tra cứu hoặc tạo hồ sơ trước.", is_error=True)
            return

        if not self.intake_selected_appointment:
            self._set_intake_feedback(
                "Không có lịch hẹn pending/confirmed để check-in. Vui lòng tạo/lên lịch hẹn trước.",
                is_error=True,
            )
            return

        appointment_id = self.intake_selected_appointment.get("appointment_id")
        try:
            ok = AppointmentController.update_status(appointment_id, "in_progress")
        except Exception:
            self._set_intake_feedback(
                "Check-in bị gián đoạn tạm thời. Vui lòng thử lại sau vài giây.",
                is_error=True,
            )
            return
        if not ok:
            self._set_intake_feedback("Check-in thất bại. Không thể cập nhật trạng thái hàng chờ.", is_error=True)
            return

        self.intake_selected_appointment["status"] = "in_progress"
        self.shared_selected_appointment_id = appointment_id
        self.shared_selected_patient_id = self.intake_selected_patient.get("patient_id")
        self.shared_selected_service_name = self._extract_service_name_from_note(
            str(self.intake_selected_appointment.get("note") or "")
        )
        self.intake_appointment_summary.setText(
            "Đã check-in vào hàng chờ: "
            f"Lịch hẹn #{appointment_id} - trạng thái in_progress"
        )
        self._refresh_staff_appointment_table()
        self._set_intake_feedback("Check-in thành công. Bệnh nhân đã được chuyển vào hàng chờ khám.", is_error=False)

    def _build_staff_patient_list_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: white; border: 1px solid #e5e7eb; border-radius: 16px;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        heading = QtWidgets.QLabel("Danh sách bệnh nhân")
        heading.setStyleSheet("font-size: 24px; color: #0f172a; font-weight: 900;")
        sub = QtWidgets.QLabel(
            "Tra cứu theo mã bệnh nhân, tên hoặc số điện thoại để xem hồ sơ cơ bản và lịch sử lịch hẹn (chỉ đọc)."
        )
        sub.setStyleSheet("font-size: 13px; color: #64748b;")
        sub.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(sub)

        search_row = QtWidgets.QHBoxLayout()
        search_row.setSpacing(10)

        self.staff_patient_search_input = QtWidgets.QLineEdit()
        self.staff_patient_search_input.setPlaceholderText("Tìm theo ID / Tên / SĐT")
        self.staff_patient_search_input.textChanged.connect(self._filter_staff_patients)

        refresh_btn = QtWidgets.QPushButton("Làm mới")
        refresh_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        refresh_btn.setStyleSheet(
            "QPushButton {"
            "background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px;"
            "padding: 8px 12px; font-weight: 700; color: #0f172a;"
            "}"
            "QPushButton:hover { background: #eef2f7; }"
        )
        refresh_btn.clicked.connect(self._refresh_staff_patient_table)

        search_row.addWidget(self.staff_patient_search_input, 1)
        search_row.addWidget(refresh_btn)
        layout.addLayout(search_row)

        body = QtWidgets.QHBoxLayout()
        body.setSpacing(14)

        list_card = self._build_section_card("Kết quả tra cứu")
        list_layout = list_card.layout()

        self.staff_patient_table = QtWidgets.QTableWidget()
        self.staff_patient_table.setColumnCount(5)
        self.staff_patient_table.setHorizontalHeaderLabels(["ID", "Họ tên", "SĐT", "Giới tính", "Ngày sinh"])
        self.staff_patient_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.staff_patient_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.staff_patient_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_patient_table.verticalHeader().setVisible(False)
        self.staff_patient_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staff_patient_table.itemSelectionChanged.connect(self._handle_staff_patient_selection)
        self.staff_patient_table.setMinimumWidth(540)
        list_layout.addWidget(self.staff_patient_table)

        self.staff_patient_feedback = QtWidgets.QLabel("Chưa có dữ liệu bệnh nhân.")
        self.staff_patient_feedback.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 600;")
        list_layout.addWidget(self.staff_patient_feedback)

        detail_card = self._build_section_card("Hồ sơ & lịch sử (chỉ đọc)")
        detail_layout = detail_card.layout()

        self.staff_patient_empty_state = QtWidgets.QLabel(
            "Chưa chọn bệnh nhân. Vui lòng chọn một dòng ở bảng bên trái để xem chi tiết."
        )
        self.staff_patient_empty_state.setWordWrap(True)
        self.staff_patient_empty_state.setStyleSheet("font-size: 12px; color: #475569;")
        detail_layout.addWidget(self.staff_patient_empty_state)

        form = QtWidgets.QFormLayout()
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(8)

        self.staff_patient_id_display = QtWidgets.QLineEdit()
        self.staff_patient_name_display = QtWidgets.QLineEdit()
        self.staff_patient_phone_display = QtWidgets.QLineEdit()
        self.staff_patient_gender_display = QtWidgets.QLineEdit()
        self.staff_patient_dob_display = QtWidgets.QLineEdit()
        self.staff_patient_address_display = QtWidgets.QTextEdit()
        self.staff_patient_address_display.setFixedHeight(64)

        readonly_fields = [
            self.staff_patient_id_display,
            self.staff_patient_name_display,
            self.staff_patient_phone_display,
            self.staff_patient_gender_display,
            self.staff_patient_dob_display,
        ]
        for field in readonly_fields:
            field.setReadOnly(True)
            field.setStyleSheet("background: #f8fafc; color: #0f172a;")

        self.staff_patient_address_display.setReadOnly(True)
        self.staff_patient_address_display.setStyleSheet("background: #f8fafc; color: #0f172a;")

        form.addRow("Mã bệnh nhân:", self.staff_patient_id_display)
        form.addRow("Họ tên:", self.staff_patient_name_display)
        form.addRow("SĐT:", self.staff_patient_phone_display)
        form.addRow("Giới tính:", self.staff_patient_gender_display)
        form.addRow("Ngày sinh:", self.staff_patient_dob_display)
        form.addRow("Địa chỉ:", self.staff_patient_address_display)
        detail_layout.addLayout(form)

        history_title = QtWidgets.QLabel("Lịch sử lịch hẹn")
        history_title.setStyleSheet("font-size: 13px; color: #334155; font-weight: 800;")
        detail_layout.addWidget(history_title)

        self.staff_patient_history_table = QtWidgets.QTableWidget()
        self.staff_patient_history_table.setColumnCount(4)
        self.staff_patient_history_table.setHorizontalHeaderLabels(["Ngày giờ", "Trạng thái", "Bác sĩ", "Tóm tắt dịch vụ"])
        self.staff_patient_history_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_patient_history_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.staff_patient_history_table.verticalHeader().setVisible(False)
        self.staff_patient_history_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staff_patient_history_table.setMinimumHeight(220)
        detail_layout.addWidget(self.staff_patient_history_table)

        self.staff_patient_history_empty = QtWidgets.QLabel("Chưa có lịch sử lịch hẹn để hiển thị.")
        self.staff_patient_history_empty.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 600;")
        detail_layout.addWidget(self.staff_patient_history_empty)

        body.addWidget(list_card, 3)
        body.addWidget(detail_card, 4)
        layout.addLayout(body, 1)

        self._refresh_staff_patient_table()
        self._reset_staff_patient_detail("Chưa chọn bệnh nhân. Vui lòng chọn một dòng ở bảng bên trái để xem chi tiết.")
        return page

    def _refresh_staff_patient_table(self):
        patients = PatientController.get_all() or []
        self.staff_patient_rows = patients
        self._filter_staff_patients()

    def _filter_staff_patients(self):
        query = str(self.staff_patient_search_input.text() if hasattr(self, "staff_patient_search_input") else "").strip().lower()
        filtered = []

        for patient in self.staff_patient_rows:
            patient_id = str(patient.get("patient_id") or "")
            name = str(patient.get("name") or "")
            phone = str(patient.get("phone") or "")
            haystack = f"{patient_id} {name} {phone}".lower()
            if not query or query in haystack:
                filtered.append(patient)

        self.staff_patient_filtered_rows = filtered
        self.staff_patient_table.setRowCount(len(filtered))

        for row, patient in enumerate(filtered):
            self.staff_patient_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(patient.get("patient_id") or "")))
            self.staff_patient_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(patient.get("name") or "")))
            self.staff_patient_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(patient.get("phone") or "")))
            self.staff_patient_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(patient.get("gender") or "")))
            self.staff_patient_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(patient.get("dob") or "")))

        if not filtered:
            self.staff_patient_feedback.setText("Không có bệnh nhân phù hợp với từ khóa tìm kiếm.")
            self._reset_staff_patient_detail("Không có bệnh nhân được chọn từ kết quả tìm kiếm.")
        else:
            self.staff_patient_feedback.setText(f"Tìm thấy {len(filtered)} bệnh nhân.")
            if self.staff_patient_selected:
                selected_id = str(self.staff_patient_selected.get("patient_id") or "")
                restored = None
                for patient in filtered:
                    if str(patient.get("patient_id") or "") == selected_id:
                        restored = patient
                        break
                if restored:
                    self._set_staff_patient_detail(restored)
                    return
            self.staff_patient_table.selectRow(0)

    def _handle_staff_patient_selection(self):
        row = self.staff_patient_table.currentRow()
        if row < 0 or row >= len(self.staff_patient_filtered_rows):
            self._reset_staff_patient_detail("Chưa chọn bệnh nhân. Vui lòng chọn một dòng ở bảng bên trái để xem chi tiết.")
            return

        patient = self.staff_patient_filtered_rows[row]
        self._set_staff_patient_detail(patient)

    def _set_staff_patient_detail(self, patient):
        self.staff_patient_selected = patient
        self.staff_patient_empty_state.setText(
            "Chi tiết hồ sơ đang ở chế độ chỉ đọc. Nhân viên không được chỉnh sửa chẩn đoán/điều trị/đơn thuốc tại đây."
        )

        self.staff_patient_id_display.setText(str(patient.get("patient_id") or ""))
        self.staff_patient_name_display.setText(str(patient.get("name") or ""))
        self.staff_patient_phone_display.setText(str(patient.get("phone") or ""))
        self.staff_patient_gender_display.setText(str(patient.get("gender") or ""))
        self.staff_patient_dob_display.setText(str(patient.get("dob") or ""))
        self.staff_patient_address_display.setPlainText(str(patient.get("address") or ""))

        patient_id = patient.get("patient_id")
        history = AppointmentController.get_by_patient(patient_id) or []
        self.staff_patient_history_table.setRowCount(len(history))

        for row, appt in enumerate(history):
            doctor_name = str(appt.get("doctor_name") or appt.get("doctor_id") or "")
            service_summary = self._extract_service_name_from_note(str(appt.get("note") or ""))
            if not service_summary:
                service_summary = str(appt.get("note") or "") or "-"

            history_date = str(appt.get("appointment_date") or appt.get("date") or "")
            self.staff_patient_history_table.setItem(row, 0, QtWidgets.QTableWidgetItem(history_date))
            self.staff_patient_history_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(appt.get("status") or "")))
            self.staff_patient_history_table.setItem(row, 2, QtWidgets.QTableWidgetItem(doctor_name))
            self.staff_patient_history_table.setItem(row, 3, QtWidgets.QTableWidgetItem(service_summary))

        if not history:
            self.staff_patient_history_empty.setText("Bệnh nhân này chưa có lịch sử lịch hẹn.")
        else:
            self.staff_patient_history_empty.setText(f"Hiển thị {len(history)} lịch hẹn gần nhất.")

    def _reset_staff_patient_detail(self, message):
        self.staff_patient_selected = None
        self.staff_patient_empty_state.setText(message)
        self.staff_patient_id_display.clear()
        self.staff_patient_name_display.clear()
        self.staff_patient_phone_display.clear()
        self.staff_patient_gender_display.clear()
        self.staff_patient_dob_display.clear()
        self.staff_patient_address_display.clear()
        self.staff_patient_history_table.setRowCount(0)
        self.staff_patient_history_empty.setText("Chưa có lịch sử lịch hẹn để hiển thị.")

    def _build_appointment_management_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: white; border: 1px solid #e5e7eb; border-radius: 16px;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        heading = QtWidgets.QLabel("Quản lý lịch hẹn")
        heading.setStyleSheet("font-size: 24px; color: #0f172a; font-weight: 900;")
        sub = QtWidgets.QLabel(
            "Tạo mới, dời lịch, hủy lịch hẹn cho quầy tiếp đón. Không bao gồm chỉnh sửa kết quả khám lâm sàng."
        )
        sub.setStyleSheet("font-size: 13px; color: #64748b;")
        sub.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(sub)

        form_card = self._build_section_card("Thông tin lịch hẹn")
        form_grid = QtWidgets.QGridLayout()
        form_grid.setHorizontalSpacing(10)
        form_grid.setVerticalSpacing(8)

        self.staff_appt_patient_id_input = QtWidgets.QLineEdit()
        self.staff_appt_patient_id_input.setPlaceholderText("Nhập Patient ID")

        self.staff_appt_doctor_combo = QtWidgets.QComboBox()
        self.staff_appt_service_combo = QtWidgets.QComboBox()

        self.staff_appt_date_input = QtWidgets.QDateEdit()
        self.staff_appt_date_input.setCalendarPopup(True)
        self.staff_appt_date_input.setDisplayFormat("yyyy-MM-dd")
        self.staff_appt_date_input.setDate(QtCore.QDate.currentDate())

        self.staff_appt_time_input = QtWidgets.QTimeEdit()
        self.staff_appt_time_input.setDisplayFormat("HH:mm")
        self.staff_appt_time_input.setTime(QtCore.QTime.currentTime())

        self.staff_appt_status_combo = QtWidgets.QComboBox()
        self.staff_appt_status_combo.addItems(["pending", "confirmed", "in_progress", "done", "cancelled"])
        self.staff_appt_status_combo.setCurrentText("pending")

        self.staff_appt_note_input = QtWidgets.QLineEdit()
        self.staff_appt_note_input.setPlaceholderText("Ghi chú điều phối (tuỳ chọn)")

        form_grid.addWidget(QtWidgets.QLabel("Patient ID:"), 0, 0)
        form_grid.addWidget(self.staff_appt_patient_id_input, 0, 1)
        form_grid.addWidget(QtWidgets.QLabel("Bác sĩ:"), 0, 2)
        form_grid.addWidget(self.staff_appt_doctor_combo, 0, 3)

        form_grid.addWidget(QtWidgets.QLabel("Dịch vụ:"), 1, 0)
        form_grid.addWidget(self.staff_appt_service_combo, 1, 1)
        form_grid.addWidget(QtWidgets.QLabel("Ngày khám:"), 1, 2)
        form_grid.addWidget(self.staff_appt_date_input, 1, 3)

        form_grid.addWidget(QtWidgets.QLabel("Giờ khám:"), 2, 0)
        form_grid.addWidget(self.staff_appt_time_input, 2, 1)
        form_grid.addWidget(QtWidgets.QLabel("Trạng thái:"), 2, 2)
        form_grid.addWidget(self.staff_appt_status_combo, 2, 3)

        form_grid.addWidget(QtWidgets.QLabel("Ghi chú:"), 3, 0)
        form_grid.addWidget(self.staff_appt_note_input, 3, 1, 1, 3)

        actions = QtWidgets.QHBoxLayout()
        btn_create = QtWidgets.QPushButton("➕ Tạo lịch hẹn")
        btn_reschedule = QtWidgets.QPushButton("🕒 Dời/Cập nhật lịch")
        btn_cancel = QtWidgets.QPushButton("❌ Hủy lịch đã chọn")
        btn_clear = QtWidgets.QPushButton("Làm mới biểu mẫu")
        for btn in [btn_create, btn_reschedule, btn_cancel, btn_clear]:
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        btn_create.clicked.connect(self._handle_staff_appointment_create)
        btn_reschedule.clicked.connect(self._handle_staff_appointment_reschedule)
        btn_cancel.clicked.connect(self._handle_staff_appointment_cancel)
        btn_clear.clicked.connect(self._reset_staff_appointment_form)

        actions.addWidget(btn_create)
        actions.addWidget(btn_reschedule)
        actions.addWidget(btn_cancel)
        actions.addStretch()
        actions.addWidget(btn_clear)

        self.staff_appt_feedback = QtWidgets.QLabel("Sẵn sàng điều phối lịch hẹn.")
        self.staff_appt_feedback.setWordWrap(True)
        self.staff_appt_feedback.setStyleSheet("font-size: 12px; color: #475569;")

        form_card.layout().addLayout(form_grid)
        form_card.layout().addLayout(actions)
        form_card.layout().addWidget(self.staff_appt_feedback)
        layout.addWidget(form_card)

        table_card = self._build_section_card("Danh sách lịch hẹn")
        self.staff_appt_table = QtWidgets.QTableWidget()
        self.staff_appt_table.setColumnCount(7)
        self.staff_appt_table.setHorizontalHeaderLabels([
            "ID", "Ngày giờ", "Patient ID", "Bệnh nhân", "Bác sĩ", "Trạng thái", "Dịch vụ"
        ])
        self.staff_appt_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.staff_appt_table.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.SingleSelection)
        self.staff_appt_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_appt_table.horizontalHeader().setStretchLastSection(True)
        self.staff_appt_table.itemSelectionChanged.connect(self._handle_staff_appointment_selection)
        table_card.layout().addWidget(self.staff_appt_table)
        layout.addWidget(table_card, 1)

        self._load_staff_appointment_dropdowns()
        self._refresh_staff_appointment_table()
        return page

    def _load_staff_appointment_dropdowns(self):
        self.staff_appt_doctor_combo.clear()
        self.staff_appt_service_combo.clear()

        doctors = DoctorController.get_all() or []
        services = ServiceController.get_all() or []

        if not doctors:
            self.staff_appt_doctor_combo.addItem("Chưa có bác sĩ", None)
        else:
            for d in doctors:
                doctor_id = d.get("doctor_id")
                label = f"#{doctor_id} - {d.get('name', '')}"
                self.staff_appt_doctor_combo.addItem(label, doctor_id)

        if not services:
            self.staff_appt_service_combo.addItem("Chưa có dịch vụ", "")
        else:
            for s in services:
                service_name = str(s.get("name") or "").strip()
                if service_name:
                    self.staff_appt_service_combo.addItem(service_name, service_name)

    def _refresh_staff_appointment_table(self):
        self.staff_appointment_rows = AppointmentController.get_all() or []
        self.staff_appt_table.setRowCount(len(self.staff_appointment_rows))

        for row, a in enumerate(self.staff_appointment_rows):
            service_text = self._extract_service_name_from_note(str(a.get("note") or ""))
            self.staff_appt_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(a.get("appointment_id", ""))))
            self.staff_appt_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(a.get("appointment_date", ""))))
            self.staff_appt_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(a.get("patient_id", ""))))
            self.staff_appt_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(a.get("patient_name", ""))))
            self.staff_appt_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(a.get("doctor_name", ""))))
            self.staff_appt_table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(a.get("status", ""))))
            self.staff_appt_table.setItem(row, 6, QtWidgets.QTableWidgetItem(service_text))

        self.staff_appt_table.resizeColumnsToContents()

    def _handle_staff_appointment_selection(self):
        selected = self.staff_appt_table.selectedItems()
        if not selected:
            return

        row = selected[0].row()
        if row < 0 or row >= len(self.staff_appointment_rows):
            return

        appt = self.staff_appointment_rows[row]
        self.staff_appointment_selected_id = appt.get("appointment_id")
        self.shared_selected_appointment_id = self.staff_appointment_selected_id
        self.shared_selected_patient_id = appt.get("patient_id")

        self.staff_appt_patient_id_input.setText(str(appt.get("patient_id") or ""))

        doctor_id = appt.get("doctor_id")
        doctor_index = self.staff_appt_doctor_combo.findData(doctor_id)
        if doctor_index >= 0:
            self.staff_appt_doctor_combo.setCurrentIndex(doctor_index)

        service_name = self._extract_service_name_from_note(str(appt.get("note") or ""))
        self.shared_selected_service_name = service_name
        service_index = self.staff_appt_service_combo.findData(service_name)
        if service_index >= 0:
            self.staff_appt_service_combo.setCurrentIndex(service_index)

        dt = QtCore.QDateTime.fromString(str(appt.get("appointment_date") or ""), "yyyy-MM-dd HH:mm:ss")
        if dt.isValid():
            self.staff_appt_date_input.setDate(dt.date())
            self.staff_appt_time_input.setTime(dt.time())

        status_text = str(appt.get("status") or "pending")
        status_index = self.staff_appt_status_combo.findText(status_text)
        if status_index >= 0:
            self.staff_appt_status_combo.setCurrentIndex(status_index)

        self.staff_appt_note_input.setText(str(appt.get("note") or ""))
        self._set_staff_appt_feedback(
            f"Đã chọn lịch hẹn #{self.staff_appointment_selected_id} để cập nhật/hủy.",
            is_error=False,
        )

    def _collect_staff_appointment_payload(self):
        patient_id = str(self.staff_appt_patient_id_input.text() or "").strip()
        doctor_id = self.staff_appt_doctor_combo.currentData()
        service_name = str(self.staff_appt_service_combo.currentData() or self.staff_appt_service_combo.currentText() or "").strip()
        date_str = self.staff_appt_date_input.date().toString("yyyy-MM-dd")
        time_str = self.staff_appt_time_input.time().toString("HH:mm")
        status = self.staff_appt_status_combo.currentText().strip()
        note = self.staff_appt_note_input.text().strip()

        if not patient_id or not doctor_id or not service_name:
            return None, "Vui lòng nhập Patient ID, chọn bác sĩ và chọn dịch vụ."

        try:
            patient_id_int = int(patient_id)
            doctor_id_int = int(doctor_id)
        except (TypeError, ValueError):
            return None, "Patient ID và Doctor ID phải là số hợp lệ."

        payload = {
            "patient_id": patient_id_int,
            "doctor_id": doctor_id_int,
            "service_name": service_name,
            "date_str": date_str,
            "time_str": time_str,
            "status": status,
            "note": note,
        }
        return payload, ""

    def _handle_staff_appointment_create(self):
        payload, error = self._collect_staff_appointment_payload()
        if error:
            self._set_staff_appt_feedback(error, is_error=True)
            return

        try:
            result = AppointmentController.create_with_details(
                payload["patient_id"],
                payload["doctor_id"],
                payload["date_str"],
                payload["time_str"],
                payload["status"],
                payload["service_name"],
                payload["note"],
            )
        except Exception:
            self._set_staff_appt_feedback(
                "Tạo lịch hẹn bị gián đoạn tạm thời. Vui lòng thử lại.",
                is_error=True,
            )
            return

        if not result.get("status"):
            self._set_staff_appt_feedback(str(result.get("message") or "Không thể tạo lịch hẹn."), is_error=True)
            return

        self._refresh_staff_appointment_table()
        self.shared_selected_patient_id = payload["patient_id"]
        self.shared_selected_service_name = payload["service_name"]
        self._set_staff_appt_feedback(str(result.get("message") or "Đã tạo lịch hẹn mới."), is_error=False)

    def _handle_staff_appointment_reschedule(self):
        if not self.staff_appointment_selected_id:
            self._set_staff_appt_feedback("Vui lòng chọn một lịch hẹn trong bảng để dời/cập nhật.", is_error=True)
            return

        payload, error = self._collect_staff_appointment_payload()
        if error:
            self._set_staff_appt_feedback(error, is_error=True)
            return

        try:
            result = AppointmentController.update_full(
                self.staff_appointment_selected_id,
                payload["patient_id"],
                payload["doctor_id"],
                payload["date_str"],
                payload["time_str"],
                payload["status"],
                payload["service_name"],
                payload["note"],
            )
        except Exception:
            self._set_staff_appt_feedback(
                "Cập nhật lịch hẹn bị gián đoạn tạm thời. Vui lòng thử lại.",
                is_error=True,
            )
            return

        if not result.get("status"):
            self._set_staff_appt_feedback(str(result.get("message") or "Không thể cập nhật lịch hẹn."), is_error=True)
            return

        self._refresh_staff_appointment_table()
        self.shared_selected_patient_id = payload["patient_id"]
        self.shared_selected_appointment_id = self.staff_appointment_selected_id
        self.shared_selected_service_name = payload["service_name"]
        self._set_staff_appt_feedback(str(result.get("message") or "Đã cập nhật lịch hẹn."), is_error=False)

    def _handle_staff_appointment_cancel(self):
        if not self.staff_appointment_selected_id:
            self._set_staff_appt_feedback("Vui lòng chọn một lịch hẹn để hủy.", is_error=True)
            return

        try:
            ok = AppointmentController.update_status(self.staff_appointment_selected_id, "cancelled")
        except Exception:
            self._set_staff_appt_feedback(
                "Hủy lịch hẹn bị gián đoạn tạm thời. Vui lòng thử lại.",
                is_error=True,
            )
            return
        if not ok:
            self._set_staff_appt_feedback(
                "Không thể hủy lịch hẹn. Lịch đã hoàn tất/đã hủy hoặc đang ở trạng thái không hợp lệ.",
                is_error=True,
            )
            return

        self._refresh_staff_appointment_table()
        self.shared_selected_appointment_id = self.staff_appointment_selected_id
        self._set_staff_appt_feedback(f"Đã hủy lịch hẹn #{self.staff_appointment_selected_id}.", is_error=False)

    def _reset_staff_appointment_form(self):
        self.staff_appointment_selected_id = None
        self.staff_appt_patient_id_input.clear()
        if self.staff_appt_doctor_combo.count() > 0:
            self.staff_appt_doctor_combo.setCurrentIndex(0)
        if self.staff_appt_service_combo.count() > 0:
            self.staff_appt_service_combo.setCurrentIndex(0)
        self.staff_appt_date_input.setDate(QtCore.QDate.currentDate())
        self.staff_appt_time_input.setTime(QtCore.QTime.currentTime())
        self.staff_appt_status_combo.setCurrentText("pending")
        self.staff_appt_note_input.clear()
        self.staff_appt_table.clearSelection()
        self._set_staff_appt_feedback("Đã làm mới biểu mẫu.", is_error=False)

    def _build_staff_billing_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: white; border: 1px solid #e5e7eb; border-radius: 16px;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        heading = QtWidgets.QLabel("Thanh toán & Hóa đơn")
        heading.setStyleSheet("font-size: 24px; color: #0f172a; font-weight: 900;")
        sub = QtWidgets.QLabel(
            "Lập hóa đơn theo lịch hẹn, xác nhận thu tiền tại quầy, in biên nhận và theo dõi lịch sử thanh toán."
        )
        sub.setStyleSheet("font-size: 13px; color: #64748b;")
        sub.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(sub)

        form_card = self._build_section_card("Tạo hóa đơn mới")
        form_grid = QtWidgets.QGridLayout()
        form_grid.setHorizontalSpacing(10)
        form_grid.setVerticalSpacing(8)

        self.staff_bill_patient_id_input = QtWidgets.QLineEdit()
        self.staff_bill_patient_id_input.setPlaceholderText("Patient ID")

        self.staff_bill_appointment_id_input = QtWidgets.QLineEdit()
        self.staff_bill_appointment_id_input.setPlaceholderText("Appointment ID")

        self.staff_bill_amount_input = QtWidgets.QLineEdit()
        self.staff_bill_amount_input.setPlaceholderText("Tổng tiền (VND)")

        form_grid.addWidget(QtWidgets.QLabel("Patient ID:"), 0, 0)
        form_grid.addWidget(self.staff_bill_patient_id_input, 0, 1)
        form_grid.addWidget(QtWidgets.QLabel("Appointment ID:"), 0, 2)
        form_grid.addWidget(self.staff_bill_appointment_id_input, 0, 3)
        form_grid.addWidget(QtWidgets.QLabel("Tổng tiền:"), 1, 0)
        form_grid.addWidget(self.staff_bill_amount_input, 1, 1)

        create_btn = QtWidgets.QPushButton("Tạo hóa đơn")
        create_btn.clicked.connect(self._handle_staff_create_invoice)
        create_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        create_btn.setStyleSheet(
            "QPushButton { background: #0ea5e9; color: white; border: none; border-radius: 8px; padding: 8px 14px; font-weight: 700; }"
            "QPushButton:hover { background: #0284c7; }"
        )

        refresh_btn = QtWidgets.QPushButton("Làm mới lịch sử")
        refresh_btn.clicked.connect(self._refresh_staff_billing_table)
        refresh_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        form_actions = QtWidgets.QHBoxLayout()
        form_actions.setSpacing(8)
        form_actions.addWidget(create_btn)
        form_actions.addWidget(refresh_btn)
        form_actions.addStretch()

        form_card.layout().addLayout(form_grid)
        form_card.layout().addLayout(form_actions)
        layout.addWidget(form_card)

        history_card = self._build_section_card("Lịch sử thanh toán")
        self.staff_bill_table = QtWidgets.QTableWidget()
        self.staff_bill_table.setColumnCount(7)
        self.staff_bill_table.setHorizontalHeaderLabels(
            ["Payment ID", "Patient ID", "Appointment ID", "Ngày", "Tổng tiền", "Trạng thái", "Biên nhận"]
        )
        self.staff_bill_table.horizontalHeader().setStretchLastSection(True)
        self.staff_bill_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staff_bill_table.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self.staff_bill_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.staff_bill_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_bill_table.itemSelectionChanged.connect(self._on_staff_billing_row_selected)
        history_card.layout().addWidget(self.staff_bill_table)

        history_actions = QtWidgets.QHBoxLayout()
        history_actions.setSpacing(8)

        confirm_btn = QtWidgets.QPushButton("Xác nhận đã thanh toán")
        confirm_btn.clicked.connect(self._handle_staff_confirm_payment)
        confirm_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        confirm_btn.setStyleSheet(
            "QPushButton { background: #16a34a; color: white; border: none; border-radius: 8px; padding: 8px 14px; font-weight: 700; }"
            "QPushButton:hover { background: #15803d; }"
        )

        print_btn = QtWidgets.QPushButton("In biên nhận")
        print_btn.clicked.connect(self._handle_staff_print_receipt)
        print_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        history_actions.addWidget(confirm_btn)
        history_actions.addWidget(print_btn)
        history_actions.addStretch()
        history_card.layout().addLayout(history_actions)

        self.staff_bill_feedback = QtWidgets.QLabel("Sẵn sàng xử lý thanh toán tại quầy.")
        self.staff_bill_feedback.setWordWrap(True)
        self.staff_bill_feedback.setStyleSheet("font-size: 12px; color: #166534; font-weight: 600;")
        history_card.layout().addWidget(self.staff_bill_feedback)

        layout.addWidget(history_card, 1)

        self._refresh_staff_billing_table()
        return page

    def _refresh_staff_billing_table(self):
        payments = PaymentController.get_all()
        self.staff_billing_rows = list(payments or [])
        self.staff_billing_selected_id = None
        self.staff_billing_selected_status = ""

        self.staff_bill_table.setRowCount(len(self.staff_billing_rows))
        for row_idx, payment in enumerate(self.staff_billing_rows):
            payment_id = payment.get("payment_id", "")
            patient_id = payment.get("patient_id", "")
            appointment_id = payment.get("appointment_id", "")
            payment_date = payment.get("payment_date", "")
            total_amount = payment.get("total_amount", "")
            status = str(payment.get("status", "unpaid"))

            self.staff_bill_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(payment_id)))
            self.staff_bill_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(patient_id)))
            self.staff_bill_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(appointment_id)))
            self.staff_bill_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(payment_date)))
            self.staff_bill_table.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(str(total_amount)))
            self.staff_bill_table.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(status))

            receipt_text = "Có thể in" if status == "paid" else "Chưa thu tiền"
            self.staff_bill_table.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(receipt_text))

        if len(self.staff_billing_rows) == 0:
            self._set_staff_billing_feedback("Chưa có hóa đơn nào trong hệ thống.", is_error=False)

    def _on_staff_billing_row_selected(self):
        selected_rows = self.staff_bill_table.selectionModel().selectedRows()
        if not selected_rows:
            self.staff_billing_selected_id = None
            self.staff_billing_selected_status = ""
            return

        row = selected_rows[0].row()
        if row < 0 or row >= len(self.staff_billing_rows):
            self.staff_billing_selected_id = None
            self.staff_billing_selected_status = ""
            return

        selected_payment = self.staff_billing_rows[row]
        self.staff_billing_selected_id = selected_payment.get("payment_id")
        self.staff_billing_selected_status = str(selected_payment.get("status", "unpaid"))
        self._set_staff_billing_feedback(
            f"Đã chọn hóa đơn #{self.staff_billing_selected_id} - trạng thái {self.staff_billing_selected_status}.",
            is_error=False,
        )

    def _handle_staff_create_invoice(self):
        patient_raw = self.staff_bill_patient_id_input.text().strip()
        appointment_raw = self.staff_bill_appointment_id_input.text().strip()
        amount_raw = self.staff_bill_amount_input.text().strip()

        if not patient_raw or not appointment_raw or not amount_raw:
            self._set_staff_billing_feedback("Vui lòng nhập đủ Patient ID, Appointment ID và tổng tiền.", is_error=True)
            return

        try:
            patient_id = int(patient_raw)
            appointment_id = int(appointment_raw)
            total_amount = float(amount_raw)
        except ValueError:
            self._set_staff_billing_feedback("Patient ID, Appointment ID phải là số và tổng tiền phải hợp lệ.", is_error=True)
            return

        if total_amount <= 0:
            self._set_staff_billing_feedback("Tổng tiền phải lớn hơn 0.", is_error=True)
            return

        appts = AppointmentController.get_by_patient(patient_id) or []
        target_appt = None
        for appt in appts:
            if int(appt.get("appointment_id", -1)) == appointment_id:
                target_appt = appt
                break
        if not target_appt:
            self._set_staff_billing_feedback(
                "Appointment ID không thuộc bệnh nhân đã nhập hoặc không tồn tại.",
                is_error=True,
            )
            return

        for payment in self.staff_billing_rows:
            if int(payment.get("appointment_id", -1)) == appointment_id:
                self._set_staff_billing_feedback(
                    f"Lịch hẹn #{appointment_id} đã có hóa đơn #{payment.get('payment_id')}. Không thể tạo trùng.",
                    is_error=True,
                )
                return

        try:
            ok = PaymentController.create(patient_id, appointment_id, total_amount)
        except Exception:
            self._set_staff_billing_feedback(
                "Tạo hóa đơn bị gián đoạn tạm thời. Vui lòng thử lại.",
                is_error=True,
            )
            return
        if not ok:
            self._set_staff_billing_feedback("Không thể tạo hóa đơn. Vui lòng thử lại.", is_error=True)
            return

        self.staff_bill_amount_input.clear()
        self._refresh_staff_billing_table()
        self.shared_selected_patient_id = patient_id
        self.shared_selected_appointment_id = appointment_id
        self._set_staff_billing_feedback(
            f"Đã tạo hóa đơn cho lịch hẹn #{appointment_id}. Trạng thái ban đầu: unpaid.",
            is_error=False,
        )

    def _handle_staff_confirm_payment(self):
        if not self.staff_billing_selected_id:
            self._set_staff_billing_feedback("Vui lòng chọn hóa đơn trước khi xác nhận thanh toán.", is_error=True)
            return

        if self.staff_billing_selected_status == "paid":
            self._set_staff_billing_feedback(
                f"Hóa đơn #{self.staff_billing_selected_id} đã ở trạng thái paid. Không thể xác nhận lần nữa.",
                is_error=True,
            )
            return

        try:
            ok = PaymentController.update_status(self.staff_billing_selected_id, "paid")
        except Exception:
            self._set_staff_billing_feedback(
                "Xác nhận thanh toán bị gián đoạn tạm thời. Vui lòng thử lại.",
                is_error=True,
            )
            return
        if not ok:
            self._set_staff_billing_feedback("Xác nhận thanh toán thất bại. Vui lòng thử lại.", is_error=True)
            return

        paid_id = self.staff_billing_selected_id
        self._refresh_staff_billing_table()
        self._set_staff_billing_feedback(f"Đã xác nhận thanh toán cho hóa đơn #{paid_id}.", is_error=False)

    def _handle_staff_print_receipt(self):
        if not self.staff_billing_selected_id:
            self._set_staff_billing_feedback("Vui lòng chọn hóa đơn để in biên nhận.", is_error=True)
            return

        if self.staff_billing_selected_status != "paid":
            self._set_staff_billing_feedback(
                "Chỉ in biên nhận sau khi hóa đơn đã được xác nhận paid.",
                is_error=True,
            )
            return

        message = (
            f"Biên nhận hóa đơn #{self.staff_billing_selected_id} đã sẵn sàng. "
            "Môi trường desktop hiện tại dùng chế độ xem trước thay cho in trực tiếp."
        )
        QtWidgets.QMessageBox.information(self, "In biên nhận", message)
        self._set_staff_billing_feedback("Đã mở luồng in biên nhận (fallback preview).", is_error=False)

    def _set_staff_billing_feedback(self, message, is_error=False):
        self.staff_bill_feedback.setText(message)
        color = "#b91c1c" if is_error else "#166534"
        self.staff_bill_feedback.setStyleSheet(f"font-size: 12px; color: {color}; font-weight: 600;")

    def _set_staff_appt_feedback(self, message, is_error=False):
        self.staff_appt_feedback.setText(message)
        color = "#b91c1c" if is_error else "#166534"
        self.staff_appt_feedback.setStyleSheet(f"font-size: 12px; color: {color}; font-weight: 600;")

    def _refresh_staff_notifications(self):
        rows = []
        appts = AppointmentController.get_all() or []
        payments = PaymentController.get_all() or []

        for appt in appts:
            status = str(appt.get("status") or "").lower().strip()
            doctor_name = appt.get("doctor_name") or "(chưa phân công)"
            patient_id = appt.get("patient_id")
            appt_id = appt.get("appointment_id")
            when = appt.get("appointment_date") or "Không rõ"

            if status == "scheduled":
                rows.append(("Lịch hẹn mới", f"Lịch hẹn #{appt_id} của bệnh nhân #{patient_id} với BS {doctor_name} vừa được tạo.", str(when), "Mới"))
            elif status == "cancelled":
                rows.append(("Lịch hẹn hủy", f"Lịch hẹn #{appt_id} của bệnh nhân #{patient_id} đã hủy. Cần liên hệ xác nhận lại.", str(when), "Khẩn"))
            elif status == "in_progress":
                rows.append(("Bệnh nhân chờ", f"Bệnh nhân #{patient_id} đang ở trạng thái chờ khám (phiên #{appt_id}).", str(when), "Theo dõi"))

        for payment in payments:
            pay_status = str(payment.get("status") or "").lower().strip()
            if pay_status != "paid":
                rows.append((
                    "Hóa đơn chưa thu",
                    f"Hóa đơn #{payment.get('payment_id')} của bệnh nhân #{payment.get('patient_id')} chưa thanh toán.",
                    str(payment.get("created_at") or "Chưa có thời gian"),
                    "Cần thu",
                ))

        rows = sorted(rows, key=lambda item: item[2], reverse=True)
        self.staff_notification_rows = rows
        self.staff_notification_table.setRowCount(len(rows))

        status_colors = {
            "Mới": "#1d4ed8",
            "Khẩn": "#b91c1c",
            "Theo dõi": "#b45309",
            "Cần thu": "#7c2d12",
        }
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value))
                if col_idx == 3:
                    color = status_colors.get(str(value), "#334155")
                    item.setForeground(QtGui.QColor(color))
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                self.staff_notification_table.setItem(row_idx, col_idx, item)

        if rows:
            self._set_staff_notification_feedback(f"Đã tải {len(rows)} thông báo cần xử lý.", is_error=False)
        else:
            self._set_staff_notification_feedback("Không có thông báo mới. Quầy đang ở trạng thái ổn định.", is_error=False)

    def _mark_notification_as_handled(self):
        selected_row = self.staff_notification_table.currentRow()
        if selected_row < 0:
            self._set_staff_notification_feedback("Vui lòng chọn một thông báo để đánh dấu đã xử lý.", is_error=True)
            return

        content_item = self.staff_notification_table.item(selected_row, 1)
        content_text = content_item.text() if content_item else "Thông báo"
        self._set_staff_notification_feedback(f"Đã đánh dấu xử lý: {content_text}", is_error=False)

    def _set_staff_notification_feedback(self, message, is_error=False):
        self.staff_notification_feedback.setText(message)
        color = "#b91c1c" if is_error else "#166534"
        self.staff_notification_feedback.setStyleSheet(f"font-size: 12px; color: {color}; font-weight: 600;")

    def _refresh_staff_reports(self):
        patients = PatientController.get_all() or []
        appts = AppointmentController.get_all() or []
        payments = PaymentController.get_all() or []

        total_patients = len(patients)
        total_appointments = len(appts)
        paid_total = 0
        unpaid_total = 0
        for payment in payments:
            amount = float(payment.get("total_amount") or 0)
            if str(payment.get("status") or "").lower().strip() == "paid":
                paid_total += amount
            else:
                unpaid_total += amount

        while self.staff_report_kpi_row.count():
            item = self.staff_report_kpi_row.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.staff_report_kpi_row.addWidget(self._build_kpi_card("Bệnh nhân", str(total_patients), "Tổng hồ sơ đang quản lý", "#0ea5e9"))
        self.staff_report_kpi_row.addWidget(self._build_kpi_card("Lịch hẹn", str(total_appointments), "Tổng lịch hẹn hiện có", "#3b82f6"))
        self.staff_report_kpi_row.addWidget(self._build_kpi_card("Đã thu", f"{int(paid_total):,} đ", "Doanh thu đã xác nhận", "#16a34a"))
        self.staff_report_kpi_row.addWidget(self._build_kpi_card("Chưa thu", f"{int(unpaid_total):,} đ", "Giá trị chờ thanh toán", "#f97316"))

        if total_appointments == 0 and total_patients == 0 and paid_total == 0 and unpaid_total == 0:
            self.staff_report_summary_lbl.setText("Chưa có dữ liệu vận hành để tổng hợp. Vui lòng kiểm tra sau khi phát sinh lịch hẹn/hóa đơn.")
        else:
            self.staff_report_summary_lbl.setText(
                f"Hôm nay hệ thống đang theo dõi {total_patients} hồ sơ bệnh nhân, {total_appointments} lịch hẹn, "
                f"đã thu {int(paid_total):,} đ và còn {int(unpaid_total):,} đ chờ thanh toán."
            )

    def _handle_staff_profile_update(self):
        name = self.staff_settings_name_input.text().strip()
        phone = self.staff_settings_phone_input.text().strip()
        email = self.staff_settings_email_input.text().strip().lower()

        if not name:
            self._set_staff_profile_feedback("Họ tên không được để trống.", is_error=True)
            return

        if phone and len(phone) < 8:
            self._set_staff_profile_feedback("Số điện thoại phải có tối thiểu 8 ký tự số.", is_error=True)
            return

        if email and ("@" not in email or "." not in email):
            self._set_staff_profile_feedback("Email không hợp lệ.", is_error=True)
            return

        self.user_data["name"] = name
        self.user_data["phone"] = phone
        self.user_data["email"] = email
        self.username = name
        self._set_staff_profile_feedback("Đã cập nhật thông tin cá nhân trong phiên làm việc hiện tại.", is_error=False)

    def _set_staff_profile_feedback(self, message, is_error=False):
        self.staff_settings_profile_feedback.setText(message)
        color = "#b91c1c" if is_error else "#166534"
        self.staff_settings_profile_feedback.setStyleSheet(f"font-size: 12px; color: {color}; font-weight: 600;")

    def _handle_staff_password_change(self):
        user_id = self.user_data.get("user_id")
        if not user_id:
            self._set_staff_password_feedback("Không tìm thấy user_id để đổi mật khẩu.", is_error=True)
            return

        current_password = self.staff_settings_current_password_input.text().strip()
        new_password = self.staff_settings_new_password_input.text().strip()
        confirm_password = self.staff_settings_confirm_password_input.text().strip()

        ok, message = SettingsController.change_password(
            user_id,
            current_password,
            new_password,
            confirm_password,
        )
        self._set_staff_password_feedback(message, is_error=(not ok))
        if ok:
            self.staff_settings_current_password_input.clear()
            self.staff_settings_new_password_input.clear()
            self.staff_settings_confirm_password_input.clear()

    def _set_staff_password_feedback(self, message, is_error=False):
        self.staff_settings_password_feedback.setText(message)
        color = "#b91c1c" if is_error else "#166534"
        self.staff_settings_password_feedback.setStyleSheet(f"font-size: 12px; color: {color}; font-weight: 600;")

    @staticmethod
    def _extract_service_name_from_note(note):
        prefix = "Dịch vụ:"
        if prefix not in note:
            return ""
        service_part = note.split(prefix, 1)[1].strip()
        if "|" in service_part:
            service_part = service_part.split("|", 1)[0].strip()
        return service_part

    def _build_section_card(self, title):
        card = QtWidgets.QFrame()
        card.setStyleSheet("background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;")
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(14, 14, 14, 14)
        card_layout.setSpacing(10)

        title_lbl = QtWidgets.QLabel(title)
        title_lbl.setStyleSheet("font-size: 15px; font-weight: 800; color: #0f172a;")
        card_layout.addWidget(title_lbl)
        return card

    def _build_kpi_card(self, title, value, note, accent):
        card = QtWidgets.QFrame()
        card.setMinimumHeight(100)
        card.setStyleSheet(
            "QFrame { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }"
        )
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)

        title_lbl = QtWidgets.QLabel(title)
        title_lbl.setStyleSheet("font-size: 12px; color: #475569; font-weight: 700;")

        value_lbl = QtWidgets.QLabel(value)
        value_lbl.setStyleSheet(f"font-size: 28px; color: {accent}; font-weight: 900;")

        note_lbl = QtWidgets.QLabel(note)
        note_lbl.setStyleSheet("font-size: 11px; color: #64748b;")

        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)
        layout.addWidget(note_lbl)
        return card

    def _build_quick_action_button(self, title, subtitle, target_index, accent):
        btn = QtWidgets.QPushButton(f"{title}\n{subtitle}")
        btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        btn.setStyleSheet(
            "QPushButton {"
            f"background: #ffffff; border: 1px solid {accent}; border-radius: 10px;"
            "text-align: left; padding: 10px 12px; color: #0f172a; font-size: 12px; font-weight: 700;"
            "}"
            "QPushButton:hover { background: #f8fafc; }"
        )
        btn.clicked.connect(lambda checked, idx=target_index: self.switch_page(idx))
        return btn

    def _nav_button_style(self, is_active=False):
        base = (
            "QPushButton { border: none; text-align: left; padding: 12px 15px; border-radius: 10px; "
            "font-size: 14px; color: #1e293b; font-weight: 600; }"
        )
        if is_active:
            return base + "QPushButton { background-color: #e1f2ee; color: #69c0a5; font-weight: 800; }"
        return base + "QPushButton:hover { background-color: #f1f5f9; }"

    def switch_page(self, index):
        if index < 0 or index >= len(self.nav_buttons):
            return

        for i, btn in enumerate(self.nav_buttons):
            btn.setStyleSheet(self._nav_button_style(is_active=(i == index)))

        if index == 2:
            self._refresh_staff_appointment_table()
            self._apply_shared_context_to_appointment_form()
        elif index == 3:
            self._refresh_staff_patient_table()
        elif index == 4:
            self._refresh_staff_billing_table()
            self._apply_shared_context_to_billing_form()
        elif index == 5:
            self._refresh_staff_service_lookup()
        elif index == 6:
            self._refresh_staff_notifications()
        elif index == 7:
            self._refresh_staff_reports()

        self.content_stack.setCurrentIndex(index)
