import math
import re

from PyQt6 import QtWidgets, QtCore, QtGui
from controllers.patient_controller import PatientController
from controllers.appointment_controller import AppointmentController
from controllers.doctor_controller import DoctorController
from controllers.service_controller import ServiceController
from controllers.payment_controller import PaymentController
from controllers.settings_controller import SettingsController


class StaffServiceDonutChart(QtWidgets.QWidget):
    def __init__(self, segments, parent=None):
        super().__init__(parent)
        self.segments = segments
        self.setMinimumSize(150, 150)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        size = min(self.width(), self.height()) - 18
        rect = QtCore.QRectF(
            (self.width() - size) / 2,
            (self.height() - size) / 2,
            size,
            size,
        )

        start_angle = 90 * 16
        for _, value, color in self.segments:
            span_angle = -int(360 * 16 * value / 100)
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(QtGui.QColor(color))
            painter.drawPie(rect, start_angle, span_angle)
            start_angle += span_angle

        inner = rect.adjusted(size * 0.28, size * 0.28, -size * 0.28, -size * 0.28)
        painter.setBrush(QtGui.QColor("#ffffff"))
        painter.drawEllipse(inner)


class StaffPatientCreateDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm bệnh nhân")
        self.setModal(True)
        self.setMinimumWidth(460)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QtWidgets.QLabel("Tạo hồ sơ bệnh nhân mới")
        title.setStyleSheet("font-size: 16px; font-weight: 900; color: #0f172a;")
        subtitle = QtWidgets.QLabel("Nhập họ tên, ngày sinh, CCCD, địa chỉ và số điện thoại.")
        subtitle.setStyleSheet("font-size: 12px; color: #64748b;")
        subtitle.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        form = QtWidgets.QFormLayout()
        form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        form.setHorizontalSpacing(16)
        form.setVerticalSpacing(10)

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Ví dụ: Nguyễn Văn Hùng")

        self.gender_combo = QtWidgets.QComboBox()
        self.gender_combo.addItems(["Nam", "Nữ", "Khác"])

        self.dob_input = QtWidgets.QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDisplayFormat("dd/MM/yyyy")
        self.dob_input.setDate(QtCore.QDate(1990, 1, 1))

        self.phone_input = QtWidgets.QLineEdit()
        self.phone_input.setPlaceholderText("Ví dụ: 0987654321")

        self.cccd_input = QtWidgets.QLineEdit()
        self.cccd_input.setPlaceholderText("Ví dụ: 123456789012")

        self.address_input = QtWidgets.QLineEdit()
        self.address_input.setPlaceholderText("Ví dụ: 123 Đường Lê Lợi, Q.1, TP.HCM")

        self.occupation_input = QtWidgets.QLineEdit()
        self.occupation_input.setPlaceholderText("Ví dụ: Nhân viên văn phòng")

        for widget in [
            self.name_input,
            self.gender_combo,
            self.dob_input,
            self.phone_input,
            self.cccd_input,
            self.address_input,
            self.occupation_input,
        ]:
            widget.setStyleSheet(
                "background: #ffffff; border: 1px solid #dbe4ee; border-radius: 8px;"
                " padding: 8px 10px; color: #0f172a; font-size: 13px;"
            )

        form.addRow("Họ và tên", self.name_input)
        form.addRow("Giới tính", self.gender_combo)
        form.addRow("Ngày sinh", self.dob_input)
        form.addRow("Số điện thoại", self.phone_input)
        form.addRow("CCCD", self.cccd_input)
        form.addRow("Địa chỉ", self.address_input)
        form.addRow("Nghề nghiệp", self.occupation_input)
        layout.addLayout(form)

        self.feedback = QtWidgets.QLabel("")
        self.feedback.setStyleSheet("font-size: 12px; color: #b91c1c; font-weight: 700;")
        layout.addWidget(self.feedback)

        action_row = QtWidgets.QHBoxLayout()
        action_row.addStretch()
        cancel_btn = QtWidgets.QPushButton("Hủy")
        save_btn = QtWidgets.QPushButton("Lưu bệnh nhân")
        cancel_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        save_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        cancel_btn.setStyleSheet(
            "QPushButton { background: #ffffff; color: #334155; border: 1px solid #dbe4ee; border-radius: 8px;"
            " padding: 9px 14px; font-weight: 800; }"
            "QPushButton:hover { background: #f8fafc; }"
        )
        save_btn.setStyleSheet(
            "QPushButton { background: #10B981; color: white; border: none; border-radius: 8px;"
            " padding: 9px 14px; font-weight: 900; }"
            "QPushButton:hover { background: #0f9f6e; }"
        )
        cancel_btn.clicked.connect(self.reject)
        save_btn.clicked.connect(self._validate_and_accept)
        action_row.addWidget(cancel_btn)
        action_row.addWidget(save_btn)
        layout.addLayout(action_row)

    def _validate_and_accept(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        if not name:
            self.feedback.setText("Họ và tên không được để trống.")
            return
        if not phone:
            self.feedback.setText("Số điện thoại không được để trống.")
            return
        self.accept()

    def payload(self):
        return {
            "name": self.name_input.text().strip(),
            "gender": self.gender_combo.currentText(),
            "dob": self.dob_input.date().toString("yyyy-MM-dd"),
            "phone": self.phone_input.text().strip(),
            "cccd": self.cccd_input.text().strip(),
            "address": self.address_input.text().strip(),
            "occupation": self.occupation_input.text().strip(),
        }


class StaffDashboardView(QtWidgets.QWidget):
    def __init__(self, user_data=None):
        super().__init__()
        self.user_data = user_data or {"name": "Staff"}
        self.username = self.user_data.get("name") or self.user_data.get("username") or "Staff"
        self.intake_selected_patient = None
        self.intake_selected_appointment = None
        self.intake_patient_mode = "new"
        self.intake_date_value = QtCore.QDate.currentDate()
        self.intake_time_value = QtCore.QTime.currentTime()
        self.intake_selected_service = ""
        self.intake_selected_doctor = ""
        self.intake_reason_value = ""
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
        self.sidebar.setFixedWidth(275)
        self.sidebar.setStyleSheet("background-color: white; border-right: 1px solid #e7edf5;")
        sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(14, 30, 14, 28)
        sidebar_layout.setSpacing(10)

        logo = QtWidgets.QLabel("✚  CarePlus")
        logo.setStyleSheet("color: #24b47e; font-size: 25px; font-weight: 900; margin: 0 0 24px 14px;")
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
        right.setStyleSheet("background: #f8fbff;")
        right_layout = QtWidgets.QVBoxLayout(right)
        right_layout.setContentsMargins(24, 22, 22, 18)
        right_layout.setSpacing(18)

        topbar = QtWidgets.QFrame()
        topbar.setStyleSheet("background: transparent; border: none;")
        topbar_layout = QtWidgets.QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(4, 0, 4, 0)
        topbar_layout.setSpacing(14)

        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(4)
        welcome = QtWidgets.QLabel(f"Xin chào, {self.username}!")
        welcome.setStyleSheet("font-size: 19px; font-weight: 900; color: #0f172a;")
        role_lbl = QtWidgets.QLabel("Nhân viên lễ tân")
        role_lbl.setStyleSheet("font-size: 13px; color: #64748b; font-weight: 700;")
        title_col.addWidget(welcome)
        title_col.addWidget(role_lbl)

        bell = QtWidgets.QLabel("🔔")
        bell.setFixedSize(34, 34)
        bell.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        bell.setStyleSheet("font-size: 20px; color: #64748b;")
        avatar = QtWidgets.QLabel("👤")
        avatar.setFixedSize(38, 38)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("background: #eaf2ff; border-radius: 19px; font-size: 20px;")
        user_lbl = QtWidgets.QLabel(f"{self.username}  ▾")
        user_lbl.setStyleSheet("font-size: 13px; color: #0f172a; font-weight: 900;")

        topbar_layout.addLayout(title_col)
        topbar_layout.addStretch()
        topbar_layout.addWidget(bell)
        topbar_layout.addWidget(avatar)
        topbar_layout.addWidget(user_lbl)
        self.topbar = topbar

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

        right_layout.addWidget(self.topbar)
        right_layout.addWidget(self.content_stack, 1)
        self.main_layout.addWidget(right, 1)

    def _build_dashboard_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: #f8fbff; border: none;")
        page_layout = QtWidgets.QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(14)

        kpi_row = QtWidgets.QHBoxLayout()
        kpi_row.setSpacing(20)
        kpi_row.addWidget(self._build_kpi_card("Bệnh nhân hôm nay", "24", "↑ 12% so với hôm qua", "#1fb873", "#e7f8ef", "👥"))
        kpi_row.addWidget(self._build_kpi_card("Lịch hẹn hôm nay", "15", "↑ 8% so với hôm qua", "#2563eb", "#eaf2ff", "📅"))
        kpi_row.addWidget(self._build_kpi_card("Hóa đơn chờ thanh toán", "6", "Tổng tiền: 12.450.000 đ", "#f97316", "#fff3e4", "🧾"))
        kpi_row.addWidget(self._build_kpi_card("Đã thanh toán hôm nay", "9", "Tổng tiền: 18.750.000 đ", "#6d48d8", "#f0eaff", "✓"))
        page_layout.addLayout(kpi_row)

        first_row = QtWidgets.QHBoxLayout()
        first_row.setSpacing(18)
        appointments_card = self._build_section_card("Lịch hẹn hôm nay")
        appointments_layout = appointments_card.layout()

        table = QtWidgets.QTableWidget(5, 6)
        table.setHorizontalHeaderLabels(["Giờ hẹn", "Bệnh nhân", "Dịch vụ", "Bác sĩ", "Trạng thái", "Thao tác"])
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        table.verticalHeader().setVisible(False)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        table.setShowGrid(False)
        table.setMinimumHeight(300)
        table.setStyleSheet(
            "QTableWidget { border: 1px solid #e7edf5; border-radius: 12px; background: #ffffff; }"
            "QHeaderView::section { background: #f8fafc; color: #1f2937; font-size: 12px; font-weight: 800; border: none; padding: 10px; }"
            "QTableWidget::item { border-bottom: 1px solid #edf2f7; padding: 8px; color: #0f172a; font-weight: 600; }"
        )

        sample_rows = [
            ("08:00", "Trần Văn Nam\nNam - 35 tuổi", "Khám tổng quát", "BS. Minh", "Đã xác nhận"),
            ("09:00", "Lê Thị Hoa\nNữ - 29 tuổi", "Tư vấn sức khỏe", "BS. Minh", "Đang chờ"),
            ("10:00", "Nguyễn Hoàng Anh\nNam - 42 tuổi", "Khám tim mạch", "BS. Hường", "Đã xác nhận"),
            ("10:30", "Phạm Minh Đức\nNam - 31 tuổi", "Khám nhi", "BS. Hường", "Đang khám"),
            ("11:00", "Vũ Thị Mai\nNữ - 28 tuổi", "Khám tổng quát", "BS. Minh", "Đã hoàn tất"),
        ]
        for r, row in enumerate(sample_rows):
            table.setRowHeight(r, 54)
            for c, value in enumerate(row):
                table.setItem(r, c, QtWidgets.QTableWidgetItem(value))
            status_lbl = self._build_status_badge(row[4])
            table.setCellWidget(r, 4, status_lbl)
            table.setCellWidget(r, 5, self._build_table_actions())
        appointments_layout.addWidget(table)

        view_all_btn = QtWidgets.QPushButton("Xem tất cả lịch hẹn  ›")
        view_all_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        view_all_btn.setStyleSheet(
            "QPushButton { background: #ffffff; border: 1px solid #dbe6f3; border-radius: 8px; padding: 8px 24px; color: #2563eb; font-weight: 800; }"
            "QPushButton:hover { background: #f5f9ff; }"
        )
        view_all_btn.clicked.connect(lambda checked: self.switch_page(2))
        appointments_layout.addWidget(view_all_btn, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        quick_actions = self._build_section_card("Thao tác nhanh")
        quick_layout = quick_actions.layout()
        quick_grid = QtWidgets.QGridLayout()
        quick_grid.setHorizontalSpacing(14)
        quick_grid.setVerticalSpacing(16)
        quick_grid.addWidget(self._build_quick_action_button("Tiếp nhận\nbệnh nhân", "👥", 1, "#e8f8ef", "#14a768"), 0, 0)
        quick_grid.addWidget(self._build_quick_action_button("Tạo lịch hẹn\nmới", "📅", 2, "#eaf2ff", "#2563eb"), 0, 1)
        quick_grid.addWidget(self._build_quick_action_button("Tra cứu\nhồ sơ", "📁", 3, "#fff4df", "#f59e0b"), 0, 2)
        quick_grid.addWidget(self._build_quick_action_button("Tạo hóa đơn\nthanh toán", "🧾", 4, "#f0eaff", "#6d48d8"), 1, 0)
        quick_grid.addWidget(self._build_quick_action_button("In phiếu\nkhám", "🖨", 4, "#e9f8ff", "#2563eb"), 1, 1)
        quick_grid.addWidget(self._build_quick_action_button("Gửi\nthông báo", "🔔", 6, "#fff1e7", "#f59e0b"), 1, 2)
        quick_layout.addLayout(quick_grid)
        quick_layout.addStretch()

        first_row.addWidget(appointments_card, 2)
        first_row.addWidget(quick_actions, 1)
        page_layout.addLayout(first_row)

        second_row = QtWidgets.QHBoxLayout()
        second_row.setSpacing(18)

        waiting_card = self._build_section_card("Bệnh nhân chờ tiếp nhận")
        waiting_layout = waiting_card.layout()
        waiting_layout.addWidget(self._build_patient_waiting_row("Nguyễn Văn Hùng", "Nam - 35 tuổi", "07:45"))
        waiting_layout.addWidget(self._build_patient_waiting_row("Đỗ Thị Phương", "Nữ - 28 tuổi", "07:50"))
        waiting_layout.addWidget(self._build_patient_waiting_row("Lý Minh Tuấn", "Nam - 42 tuổi", "07:55"))

        notices_card = self._build_section_card("Thông báo")
        notices_layout = notices_card.layout()
        notices_layout.addWidget(self._build_notice_row("🔔", "Có 3 lịch hẹn mới cần xác nhận", "5 phút trước", "#f59e0b"))
        notices_layout.addWidget(self._build_notice_row("💵", "Hóa đơn #HD000125 chưa thanh toán", "20 phút trước", "#1fb873"))
        notices_layout.addWidget(self._build_notice_row("📅", "Lịch khám 10:30 sắp bắt đầu", "25 phút trước", "#2563eb"))
        notices_layout.addWidget(self._build_notice_row("👤", "Bệnh nhân Nguyễn Hoàng Anh đến sớm 10p", "40 phút trước", "#6d48d8"))

        services_card = self._build_section_card("Thống kê dịch vụ")
        services_layout = services_card.layout()
        service_data = [
            ("Khám tổng quát", 45, "#45c2a5"),
            ("Tư vấn sức khỏe", 25, "#2563eb"),
            ("Khám tim mạch", 15, "#f59e0b"),
            ("Khám nhi", 10, "#8b5cf6"),
            ("Khác", 5, "#94a3b8"),
        ]
        services_body = QtWidgets.QHBoxLayout()
        services_body.setSpacing(10)
        services_body.addWidget(StaffServiceDonutChart(service_data), 1)
        legend = QtWidgets.QVBoxLayout()
        legend.setSpacing(8)
        for name, pct, color in service_data:
            row = QtWidgets.QWidget()
            row_layout = QtWidgets.QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(8)
            dot = QtWidgets.QLabel()
            dot.setFixedSize(10, 10)
            dot.setStyleSheet(f"background: {color}; border-radius: 5px;")
            label = QtWidgets.QLabel(name)
            label.setStyleSheet("font-size: 12px; color: #0f172a; font-weight: 700;")
            pct_lbl = QtWidgets.QLabel(f"{pct}%")
            pct_lbl.setStyleSheet("font-size: 12px; color: #0f172a; font-weight: 900;")
            row_layout.addWidget(dot)
            row_layout.addWidget(label, 1)
            row_layout.addWidget(pct_lbl)
            legend.addWidget(row)
        services_body.addLayout(legend, 1)
        services_layout.addLayout(services_body)

        second_row.addWidget(waiting_card, 1)
        second_row.addWidget(notices_card, 1)
        second_row.addWidget(services_card, 1)
        page_layout.addLayout(second_row)

        todo_card = self._build_section_card("Công việc hôm nay")
        todo_layout = todo_card.layout()
        checklist_grid = QtWidgets.QGridLayout()
        checklist_grid.setHorizontalSpacing(80)
        checklist_grid.setVerticalSpacing(8)
        for index, text in enumerate(["Xác nhận lịch hẹn", "Tiếp nhận bệnh nhân", "Kiểm tra thanh toán", "In phiếu khám"]):
            cb = QtWidgets.QCheckBox(text)
            cb.setChecked(True)
            cb.setStyleSheet("QCheckBox { color: #0f172a; font-size: 13px; font-weight: 700; spacing: 10px; }")
            checklist_grid.addWidget(cb, index % 2, index // 2)
        todo_layout.addLayout(checklist_grid)
        page_layout.addWidget(todo_card)
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
        page.setStyleSheet("background: #f8fbff; border: none;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        topbar = QtWidgets.QFrame()
        topbar.setStyleSheet("background: transparent; border: none;")
        topbar_layout = QtWidgets.QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(4, 0, 4, 0)
        topbar_layout.setSpacing(14)

        topbar_left = QtWidgets.QVBoxLayout()
        topbar_left.setSpacing(5)
        heading = QtWidgets.QLabel("Tiếp nhận bệnh nhân")
        heading.setStyleSheet("font-size: 25px; color: #0f172a; font-weight: 900;")
        breadcrumb = QtWidgets.QLabel("Trang chủ  ›  Tiếp nhận bệnh nhân")
        breadcrumb.setStyleSheet("font-size: 14px; color: #64748b; font-weight: 700;")
        topbar_left.addWidget(heading)
        topbar_left.addWidget(breadcrumb)

        topbar_layout.addLayout(topbar_left)
        topbar_layout.addStretch()
        intake_bell = QtWidgets.QLabel("🔔")
        intake_bell.setFixedSize(34, 34)
        intake_bell.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        intake_bell.setStyleSheet("border: none; background: transparent; font-size: 21px; color: #64748b;")
        intake_avatar = QtWidgets.QLabel("👤")
        intake_avatar.setFixedSize(42, 42)
        intake_avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        intake_avatar.setStyleSheet("background: #eaf2ff; border-radius: 21px; font-size: 22px;")
        intake_user_lbl = QtWidgets.QLabel(f"{self.username}  ▾")
        intake_user_lbl.setStyleSheet("border: none; background: transparent; font-size: 13px; color: #0f172a; font-weight: 900;")
        topbar_layout.addWidget(intake_bell)
        topbar_layout.addWidget(intake_avatar)
        topbar_layout.addWidget(intake_user_lbl)
        layout.addWidget(topbar)

        content_wrap = QtWidgets.QHBoxLayout()
        content_wrap.setSpacing(22)

        left_col = QtWidgets.QVBoxLayout()
        left_col.setSpacing(16)

        right_col = QtWidgets.QVBoxLayout()
        right_col.setSpacing(16)

        lookup_card = self._build_section_card("1. Tìm kiếm bệnh nhân")
        lookup_form = QtWidgets.QHBoxLayout()
        lookup_form.setSpacing(10)

        self.intake_phone_input = QtWidgets.QLineEdit()
        self.intake_phone_input.setPlaceholderText("Nhập số điện thoại, CCCD hoặc mã bệnh nhân")
        self.intake_cccd_input = QtWidgets.QLineEdit()
        self.intake_cccd_input.hide()

        btn_lookup = QtWidgets.QPushButton("🔎  Tìm kiếm")
        btn_lookup.setFixedWidth(145)
        btn_lookup.setStyleSheet(self._intake_primary_button_style())
        btn_lookup.clicked.connect(self._handle_intake_lookup)
        lookup_form.addWidget(self.intake_phone_input, 1)
        lookup_form.addWidget(btn_lookup)

        lookup_card.layout().addLayout(lookup_form)
        result_title = QtWidgets.QLabel("Kết quả tìm kiếm")
        result_title.setStyleSheet("font-size: 13px; color: #0f172a; font-weight: 800;")
        lookup_card.layout().addWidget(result_title)
        self.intake_lookup_result_card = QtWidgets.QFrame()
        self.intake_lookup_result_card.setObjectName("intakeLookupResult")
        self.intake_lookup_result_card.setStyleSheet(
            "QFrame#intakeLookupResult { background: #ffffff; border: 1px solid #e4ebf4; border-radius: 12px; }"
        )
        lookup_result_layout = QtWidgets.QHBoxLayout(self.intake_lookup_result_card)
        lookup_result_layout.setContentsMargins(14, 12, 14, 12)
        lookup_result_layout.setSpacing(12)
        patient_avatar = QtWidgets.QLabel("👤")
        patient_avatar.setFixedSize(58, 58)
        patient_avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        patient_avatar.setStyleSheet("background: #eaf2ff; border-radius: 29px; font-size: 28px;")
        self.intake_lookup_result_label = QtWidgets.QLabel("Nhập SĐT/CCCD/mã bệnh nhân để tìm hồ sơ đã có.")
        self.intake_lookup_result_label.setWordWrap(True)
        self.intake_lookup_result_label.setStyleSheet("font-size: 13px; color: #475569; font-weight: 700;")
        detail_btn = QtWidgets.QPushButton("Xem chi tiết ›")
        detail_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        detail_btn.setStyleSheet("border: none; color: #2563eb; font-size: 13px; font-weight: 900;")
        detail_btn.clicked.connect(lambda checked: self.switch_page(3))
        lookup_result_layout.addWidget(patient_avatar)
        lookup_result_layout.addWidget(self.intake_lookup_result_label, 1)
        lookup_result_layout.addWidget(detail_btn)
        lookup_card.layout().addWidget(self.intake_lookup_result_card)

        intake_or_divider = QtWidgets.QLabel("────────────  HOẶC  ────────────")
        intake_or_divider.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        intake_or_divider.setStyleSheet("font-size: 12px; color: #94a3b8; font-weight: 700;")
        lookup_card.layout().addWidget(intake_or_divider)
        left_col.addWidget(lookup_card)

        profile_card = self._build_section_card("2. Thông tin bệnh nhân mới")
        intake_mode_row = QtWidgets.QHBoxLayout()
        intake_mode_row.setSpacing(28)
        self.intake_mode_new_radio = QtWidgets.QRadioButton("Bệnh nhân mới")
        self.intake_mode_walkin_radio = QtWidgets.QRadioButton("Bệnh nhân vãng lai")
        self.intake_mode_new_radio.setStyleSheet(self._intake_radio_style())
        self.intake_mode_walkin_radio.setStyleSheet(self._intake_radio_style())
        self.intake_mode_new_radio.setChecked(True)
        self.intake_mode_new_radio.toggled.connect(self._handle_intake_mode_change)
        self.intake_mode_walkin_radio.toggled.connect(self._handle_intake_mode_change)
        intake_mode_row.addWidget(self.intake_mode_new_radio)
        intake_mode_row.addWidget(self.intake_mode_walkin_radio)
        intake_mode_row.addStretch()
        profile_card.layout().addLayout(intake_mode_row)

        profile_form = QtWidgets.QGridLayout()
        profile_form.setHorizontalSpacing(18)
        profile_form.setVerticalSpacing(12)

        self.intake_name_input = QtWidgets.QLineEdit()
        self.intake_name_input.setPlaceholderText("Nhập họ và tên")
        self.intake_name_input.textChanged.connect(self._refresh_intake_summary_card)
        self.intake_phone_profile_input = QtWidgets.QLineEdit()
        self.intake_phone_profile_input.setPlaceholderText("Nhập số điện thoại")
        self.intake_phone_profile_input.textChanged.connect(self._sync_intake_phone_inputs)
        self.intake_cccd_profile_input = QtWidgets.QLineEdit()
        self.intake_cccd_profile_input.setPlaceholderText("Nhập CCCD")
        self.intake_cccd_profile_input.textChanged.connect(self._sync_intake_cccd_inputs)
        self.intake_dob_input = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.intake_dob_input.setCalendarPopup(True)
        self.intake_dob_input.setDisplayFormat("dd/MM/yyyy")
        self.intake_dob_input.dateChanged.connect(self._refresh_intake_summary_card)
        self.intake_gender_input = QtWidgets.QComboBox()
        self.intake_gender_input.addItems(["Nam", "Nữ", "Khác"])
        self.intake_gender_input.hide()
        self.intake_gender_input.currentTextChanged.connect(self._sync_intake_gender_radios)
        self.intake_gender_input.currentTextChanged.connect(self._refresh_intake_summary_card)
        self.intake_gender_selector = self._build_intake_gender_selector()
        self.intake_email_input = QtWidgets.QLineEdit()
        self.intake_email_input.setPlaceholderText("Nhập email (nếu có)")
        self.intake_email_input.textChanged.connect(self._refresh_intake_summary_card)
        self.intake_occupation_input = QtWidgets.QLineEdit()
        self.intake_occupation_input.setPlaceholderText("Nhập nghề nghiệp")
        self.intake_occupation_input.textChanged.connect(self._refresh_intake_summary_card)
        self.intake_address_input = QtWidgets.QLineEdit()
        self.intake_address_input.setPlaceholderText("Nhập địa chỉ")
        self.intake_address_input.textChanged.connect(self._refresh_intake_summary_card)
        self.intake_note_input = QtWidgets.QPlainTextEdit()
        self.intake_note_input.setPlaceholderText("Ghi chú thêm (nếu có)")
        self.intake_note_input.setFixedHeight(78)
        self.intake_note_input.textChanged.connect(self._refresh_intake_summary_card)

        profile_form.addWidget(self._build_intake_field("Họ và tên *", self.intake_name_input), 0, 0)
        profile_form.addWidget(self._build_intake_field("Ngày sinh *", self.intake_dob_input), 0, 1)
        profile_form.addWidget(self._build_intake_field("Giới tính *", self.intake_gender_selector), 1, 0)
        profile_form.addWidget(self._build_intake_field("Số điện thoại *", self.intake_phone_profile_input), 1, 1)
        profile_form.addWidget(self._build_intake_field("CCCD/CMND", self.intake_cccd_profile_input), 2, 0)
        profile_form.addWidget(self._build_intake_field("Địa chỉ", self.intake_address_input), 2, 1)
        profile_form.addWidget(self._build_intake_field("Email", self.intake_email_input), 3, 0)
        profile_form.addWidget(self._build_intake_field("Nghề nghiệp", self.intake_occupation_input), 3, 1)
        profile_form.addWidget(self._build_intake_field("Ghi chú", self.intake_note_input), 4, 1)

        btn_create_or_update = QtWidgets.QPushButton("👥  Lưu thông tin")
        btn_create_or_update.setStyleSheet(self._intake_primary_button_style())
        btn_create_or_update.clicked.connect(self._handle_intake_create_or_update)
        intake_clear_profile_btn = QtWidgets.QPushButton("🗑  Xóa thông tin")
        intake_clear_profile_btn.setStyleSheet(self._intake_secondary_button_style())
        intake_clear_profile_btn.clicked.connect(self._handle_intake_reset)
        profile_form.addWidget(intake_clear_profile_btn, 5, 0)
        profile_form.addWidget(btn_create_or_update, 5, 1)

        profile_card.layout().addLayout(profile_form)
        left_col.addWidget(profile_card)

        queue_card = self._build_section_card("3. Thông tin tiếp nhận")
        queue_layout = queue_card.layout()

        intake_schedule_form = QtWidgets.QGridLayout()
        intake_schedule_form.setHorizontalSpacing(18)
        intake_schedule_form.setVerticalSpacing(12)
        self.intake_date_input = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.intake_date_input.setCalendarPopup(True)
        self.intake_date_input.setDisplayFormat("dd/MM/yyyy")
        self.intake_date_input.dateChanged.connect(self._refresh_intake_summary_card)
        self.intake_time_input = QtWidgets.QTimeEdit(QtCore.QTime.currentTime())
        self.intake_time_input.setDisplayFormat("HH:mm")
        self.intake_time_input.timeChanged.connect(self._refresh_intake_summary_card)
        self.intake_service_combo = QtWidgets.QComboBox()
        self.intake_doctor_combo = QtWidgets.QComboBox()
        self.intake_service_combo.currentTextChanged.connect(self._refresh_intake_summary_card)
        self.intake_doctor_combo.currentTextChanged.connect(self._refresh_intake_summary_card)
        self.intake_reason_input = QtWidgets.QPlainTextEdit()
        self.intake_reason_input.setPlaceholderText("Nhập lý do khám (nếu có)")
        self.intake_reason_input.setFixedHeight(94)
        self.intake_reason_input.textChanged.connect(self._refresh_intake_summary_card)

        intake_schedule_form.addWidget(self._build_intake_field("Ngày tiếp nhận", self.intake_date_input), 0, 0)
        intake_schedule_form.addWidget(self._build_intake_field("Giờ tiếp nhận", self.intake_time_input), 0, 1)
        intake_schedule_form.addWidget(self._build_intake_field("Dịch vụ khám *", self.intake_service_combo), 1, 0, 1, 2)
        intake_schedule_form.addWidget(self._build_intake_field("Bác sĩ khám *", self.intake_doctor_combo), 2, 0, 1, 2)
        intake_schedule_form.addWidget(self._build_intake_field("Lý do khám", self.intake_reason_input), 3, 0, 1, 2)
        queue_layout.addLayout(intake_schedule_form)

        self._load_intake_service_options()
        self._load_intake_doctor_options()

        self.intake_feedback = QtWidgets.QLabel("")
        self.intake_feedback.setWordWrap(True)
        self.intake_feedback.setStyleSheet(self._intake_feedback_style("info"))
        self.intake_feedback.setVisible(False)

        queue_layout.addWidget(self.intake_feedback)
        right_col.addWidget(queue_card)

        next_steps_card = self._build_section_card("4. Xác nhận tiếp nhận")
        self.intake_patient_summary = QtWidgets.QLabel("Chưa chọn bệnh nhân.")
        self.intake_patient_summary.setStyleSheet("font-size: 13px; color: #334155; font-weight: 800;")
        self.intake_summary_card = QtWidgets.QLabel("Chưa có dữ liệu tiếp nhận.")
        self.intake_summary_card.setWordWrap(True)
        self.intake_summary_card.setStyleSheet(
            "background: #ffffff; border: 1px solid #e4ebf4; border-radius: 12px; padding: 16px; font-size: 13px; color: #0f172a; font-weight: 700;"
        )
        self.intake_appointment_summary = QtWidgets.QLabel("Trạng thái: Chờ khám")
        self.intake_appointment_summary.setStyleSheet("font-size: 13px; color: #f97316; font-weight: 900;")
        self.intake_info_badge = QtWidgets.QLabel("ⓘ  Bệnh nhân sẽ được chuyển vào danh sách chờ khám của bác sĩ.\n    Vui lòng hướng dẫn bệnh nhân ngồi chờ.")
        self.intake_info_badge.setWordWrap(True)
        self.intake_info_badge.setStyleSheet(
            "background: #eff6ff; border: 1px solid #bfdbfe; color: #2563eb; border-radius: 10px; padding: 12px 14px; font-size: 13px; font-weight: 800;"
        )
        next_steps_card.layout().addWidget(self.intake_patient_summary)
        next_steps_card.layout().addWidget(self.intake_summary_card)
        next_steps_card.layout().addWidget(self.intake_appointment_summary)
        next_steps_card.layout().addWidget(self.intake_info_badge)

        self.intake_confirm_btn = QtWidgets.QPushButton("✅  Xác nhận tiếp nhận")
        self.intake_confirm_btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.intake_confirm_btn.setStyleSheet(self._intake_primary_button_style())
        self.intake_confirm_btn.clicked.connect(self._handle_intake_checkin)

        next_steps_card.layout().addWidget(self.intake_confirm_btn)
        right_col.addWidget(next_steps_card)

        content_wrap.addLayout(left_col, 55)
        content_wrap.addLayout(right_col, 43)
        layout.addLayout(content_wrap)
        intake_controls = [
            self.intake_cccd_input,
            self.intake_phone_input,
            self.intake_name_input,
            self.intake_phone_profile_input,
            self.intake_cccd_profile_input,
            self.intake_email_input,
            self.intake_occupation_input,
            self.intake_address_input,
            self.intake_note_input,
            self.intake_reason_input,
            self.intake_gender_input,
            self.intake_service_combo,
            self.intake_doctor_combo,
            self.intake_dob_input,
            self.intake_date_input,
            self.intake_time_input,
        ]
        for widget in intake_controls:
            widget.setStyleSheet(self._intake_input_style())

        self._refresh_intake_summary_card()

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
        state = "error" if is_error else "success"
        self.intake_feedback.setStyleSheet(self._intake_feedback_style(state))
        self.intake_feedback.setText(message)
        self.intake_feedback.setVisible(bool(message))

    def _set_intake_lookup_result(self, message, has_record=False):
        if not hasattr(self, "intake_lookup_result_card") or not hasattr(self, "intake_lookup_result_label"):
            return
        if has_record:
            self.intake_lookup_result_card.setStyleSheet(
                "QFrame#intakeLookupResult { background: #ffffff; border: 1px solid #d7f2e4; border-radius: 12px; }"
            )
            self.intake_lookup_result_label.setStyleSheet("font-size: 13px; color: #166534; font-weight: 800;")
        else:
            self.intake_lookup_result_card.setStyleSheet(
                "QFrame#intakeLookupResult { background: #fff7ed; border: 1px solid #fed7aa; border-radius: 12px; }"
            )
            self.intake_lookup_result_label.setStyleSheet("font-size: 13px; color: #9a3412; font-weight: 800;")
        self.intake_lookup_result_label.setText(message)

    def _validate_intake_form(self, data):
        mode = self.intake_patient_mode
        required_fields = [
            ("name", "Họ tên"),
            ("phone", "SĐT"),
            ("dob", "Ngày sinh"),
            ("gender", "Giới tính"),
            ("address", "Địa chỉ"),
        ]
        if mode == "new":
            required_fields.extend([
                ("cccd", "CCCD"),
                ("email", "Email"),
                ("occupation", "Nghề nghiệp"),
            ])

        missing = [label for key, label in required_fields if not str(data.get(key) or "").strip()]
        if missing:
            return False, f"Thiếu thông tin bắt buộc ({' / '.join(missing)})."

        phone = str(data.get("phone") or "").strip()
        if not re.fullmatch(r"0\d{9}", phone):
            return False, "SĐT không hợp lệ. Yêu cầu 10 chữ số và bắt đầu bằng 0."

        email = str(data.get("email") or "").strip()
        if email and not re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email):
            return False, "Email không hợp lệ. Vui lòng nhập đúng định dạng (ví dụ: ten@domain.com)."

        cccd = str(data.get("cccd") or "").strip()
        if cccd and not re.fullmatch(r"\d{12}", cccd):
            return False, "CCCD không hợp lệ. Yêu cầu đúng 12 chữ số."

        return True, ""

    def _sync_intake_phone_inputs(self):
        phone = self.intake_phone_profile_input.text()
        if self.intake_phone_input.text() != phone:
            self.intake_phone_input.blockSignals(True)
            self.intake_phone_input.setText(phone)
            self.intake_phone_input.blockSignals(False)
        self._refresh_intake_summary_card()

    def _sync_intake_cccd_inputs(self):
        cccd = self.intake_cccd_profile_input.text()
        if self.intake_cccd_input.text() != cccd:
            self.intake_cccd_input.blockSignals(True)
            self.intake_cccd_input.setText(cccd)
            self.intake_cccd_input.blockSignals(False)
        self._refresh_intake_summary_card()

    def _handle_intake_mode_change(self):
        self.intake_patient_mode = "walkin" if self.intake_mode_walkin_radio.isChecked() else "new"
        if self.intake_patient_mode == "walkin":
            self._set_intake_feedback(
                "Đang ở chế độ vãng lai: bắt buộc Họ tên, SĐT, Ngày sinh, Giới tính, Địa chỉ.",
                is_error=False,
            )
        else:
            self._set_intake_feedback(
                "Đang ở chế độ bệnh nhân mới: cần bổ sung thêm CCCD, Email, Nghề nghiệp.",
                is_error=False,
            )
        self._refresh_intake_summary_card()

    def _load_intake_service_options(self):
        self.intake_service_combo.clear()
        try:
            services = ServiceController.get_all() or []
        except Exception:
            services = []

        names = []
        for service in services:
            name = str(service.get("service_name") or service.get("name") or "").strip()
            if name:
                names.append(name)

        if not names:
            self.intake_service_combo.addItem("[Không có dữ liệu dịch vụ]")
            self.intake_service_combo.setEnabled(False)
        else:
            self.intake_service_combo.addItems(names)
            self.intake_service_combo.setEnabled(True)

    def _load_intake_doctor_options(self):
        self.intake_doctor_combo.clear()
        try:
            doctors = DoctorController.get_all() or []
        except Exception:
            doctors = []

        names = []
        for doctor in doctors:
            name = str(doctor.get("doctor_name") or doctor.get("name") or "").strip()
            if name:
                names.append(name)

        if not names:
            self.intake_doctor_combo.addItem("[Không có dữ liệu bác sĩ]")
            self.intake_doctor_combo.setEnabled(False)
        else:
            for doctor in doctors:
                name = str(doctor.get("doctor_name") or doctor.get("name") or "").strip()
                if name:
                    self.intake_doctor_combo.addItem(name, doctor.get("doctor_id"))
            self.intake_doctor_combo.setEnabled(True)

    def _refresh_intake_summary_card(self):
        self.intake_date_value = self.intake_date_input.date() if hasattr(self, "intake_date_input") else QtCore.QDate.currentDate()
        self.intake_time_value = self.intake_time_input.time() if hasattr(self, "intake_time_input") else QtCore.QTime.currentTime()
        self.intake_selected_service = self.intake_service_combo.currentText().strip() if hasattr(self, "intake_service_combo") else ""
        self.intake_selected_doctor = self.intake_doctor_combo.currentText().strip() if hasattr(self, "intake_doctor_combo") else ""
        self.intake_reason_value = self._plain_text_value(self.intake_reason_input) if hasattr(self, "intake_reason_input") else ""

        patient_name = self.intake_name_input.text().strip() if hasattr(self, "intake_name_input") else ""
        patient_phone = self.intake_phone_profile_input.text().strip() if hasattr(self, "intake_phone_profile_input") else ""
        patient_gender = self.intake_gender_input.currentText().strip() if hasattr(self, "intake_gender_input") else ""
        patient_cccd = self.intake_cccd_profile_input.text().strip() if hasattr(self, "intake_cccd_profile_input") else ""

        summary_text = (
            f"{patient_name or 'Chưa nhập bệnh nhân'}\n"
            f"{patient_gender or 'Chưa rõ giới tính'}  •  {patient_phone or 'Chưa nhập SĐT'}\n"
            f"CCCD: {patient_cccd or 'Chưa nhập'}\n\n"
            f"🧾  Dịch vụ khám: {self.intake_selected_service or 'Chưa chọn'}\n"
            f"👨‍⚕️  Bác sĩ khám: {self.intake_selected_doctor or 'Chưa chọn'}\n"
            f"🕒  Thời gian khám dự kiến: {self.intake_time_value.toString('HH:mm')}\n"
            f"✅  Trạng thái: Chờ khám"
        )

        if hasattr(self, "intake_summary_card"):
            self.intake_summary_card.setText(summary_text)

    def _handle_intake_lookup(self):
        cccd = self.intake_cccd_input.text().strip()
        phone = self.intake_phone_input.text().strip()
        if not cccd and phone:
            compact = re.sub(r"\s+", "", phone)
            if re.fullmatch(r"\d{12}", compact):
                cccd = compact
                phone = ""
            elif compact.upper().startswith("BN"):
                phone = compact
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
            self.shared_selected_patient_id = None
            self.shared_selected_appointment_id = None
            self.shared_selected_service_name = ""
            self.intake_patient_summary.setText("Không tìm thấy hồ sơ bệnh nhân theo CCCD/SĐT đã nhập.")
            self.intake_appointment_summary.setText("Chưa có lịch hẹn để check-in.")
            self._set_intake_lookup_result(
                "Không tìm thấy hồ sơ phù hợp. Vui lòng nhập form bên dưới để tạo hồ sơ mới.",
                has_record=False,
            )
            self._set_intake_feedback("Không tìm thấy hồ sơ. Vui lòng tạo mới thông tin bệnh nhân.", is_error=True)
            self._refresh_intake_summary_card()
            return

        self.intake_selected_patient = patient
        self.intake_name_input.setText(str(patient.get("name") or ""))
        self.intake_phone_input.setText(str(patient.get("phone") or ""))
        self.intake_phone_profile_input.setText(str(patient.get("phone") or ""))
        self.intake_address_input.setText(str(patient.get("address") or ""))
        self.intake_cccd_profile_input.setText(str(patient.get("cccd") or cccd or ""))
        self.intake_email_input.setText(str(patient.get("email") or ""))
        self.intake_occupation_input.setText(str(patient.get("occupation") or ""))
        self.intake_note_input.setText(str(patient.get("intake_notes") or ""))
        gender = str(patient.get("gender") or "Nam")
        self.intake_gender_input.setCurrentText(gender if gender in {"Nam", "Nữ", "Khác"} else "Nam")

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
            self.intake_appointment_summary.setText("Chưa có lịch hẹn; hệ thống sẽ tạo lượt khám mới khi xác nhận.")

        self._set_intake_lookup_result(
            f"Đã tìm thấy hồ sơ BN #{patient_id}: {patient.get('name', '')} - SĐT {patient.get('phone', '')}.",
            has_record=True,
        )
        self._set_intake_feedback("Tra cứu thành công. Có thể cập nhật thông tin trước khi lưu/check-in.", is_error=False)
        self._refresh_intake_summary_card()

    def _handle_intake_create_or_update(self):
        name = self.intake_name_input.text().strip()
        phone = self.intake_phone_input.text().strip()
        cccd = self.intake_cccd_profile_input.text().strip()
        address = self.intake_address_input.text().strip()
        dob = self.intake_dob_input.date().toString("yyyy-MM-dd")
        gender = self.intake_gender_input.currentText()
        email = self.intake_email_input.text().strip()
        occupation = self.intake_occupation_input.text().strip()
        intake_notes = self._plain_text_value(self.intake_note_input)

        payload = {
            "name": name,
            "dob": dob,
            "gender": gender,
            "phone": phone,
            "cccd": cccd,
            "address": address,
            "email": email,
            "occupation": occupation,
            "intake_notes": intake_notes,
            "patient_type": "walkin" if self.intake_patient_mode == "walkin" else "general",
        }

        valid, message = self._validate_intake_form(payload)
        if not valid:
            self._set_intake_feedback(message, is_error=True)
            return

        if self.intake_selected_patient and self.intake_selected_patient.get("patient_id"):
            patient_id = self.intake_selected_patient.get("patient_id")
            result = PatientController.update_with_status(patient_id, payload)
            if not result.get("status"):
                self._set_intake_feedback(
                    result.get("message") or "Cập nhật hồ sơ thất bại. Vui lòng thử lại.",
                    is_error=True,
                )
                return
            self.intake_selected_patient = PatientController.find_by_cccd_or_phone(cccd=cccd, phone=phone)
            if self.intake_selected_patient:
                self.shared_selected_patient_id = self.intake_selected_patient.get("patient_id")
            self._set_intake_feedback(result.get("message") or "Cập nhật hồ sơ bệnh nhân thành công.", is_error=False)
            return

        result = PatientController.create_with_status(payload)
        if not result.get("status"):
            self._set_intake_feedback(
                result.get("message") or "Tạo hồ sơ bệnh nhân mới thất bại. Vui lòng thử lại.",
                is_error=True,
            )
            return

        created = PatientController.find_by_cccd_or_phone(cccd=cccd, phone=phone)
        self.intake_selected_patient = created
        if created:
            self.shared_selected_patient_id = created.get("patient_id")
            self.intake_patient_summary.setText(
                f"Đã tạo hồ sơ mới BN #{created.get('patient_id')}: {created.get('name', '')} - SĐT: {created.get('phone', '')}"
            )
            self._set_intake_lookup_result(
                f"Đã tạo mới hồ sơ BN #{created.get('patient_id')}. Có thể tiếp tục check-in.",
                has_record=True,
            )
        self._set_intake_feedback(result.get("message") or "Tạo hồ sơ bệnh nhân mới thành công.", is_error=False)

    def _handle_intake_checkin(self):
        if not self.intake_selected_patient:
            self._set_intake_feedback("Chưa có bệnh nhân để check-in. Vui lòng tra cứu hoặc tạo hồ sơ trước.", is_error=True)
            return
        patient_id = self.intake_selected_patient.get("patient_id")
        if not patient_id:
            self._set_intake_feedback("Thiếu mã bệnh nhân. Vui lòng tra cứu/chọn lại hồ sơ trước khi xác nhận tiếp nhận.", is_error=True)
            return

        doctor_id = self.intake_doctor_combo.currentData()
        if not doctor_id:
            self._set_intake_feedback("Thiếu bác sĩ phụ trách. Vui lòng chọn bác sĩ trước khi xác nhận tiếp nhận.", is_error=True)
            return

        service_name = str(self.intake_service_combo.currentText() or "").strip()
        if not service_name or service_name.lower() == "chưa có dịch vụ":
            self._set_intake_feedback("Thiếu dịch vụ. Vui lòng chọn dịch vụ hợp lệ trước khi xác nhận tiếp nhận.", is_error=True)
            return

        intake_date_str = self.intake_date_input.date().toString("yyyy-MM-dd")
        intake_time_str = self.intake_time_input.time().toString("HH:mm")
        reason_note = self._plain_text_value(self.intake_reason_input)

        if not self.intake_selected_appointment:
            create_result = AppointmentController.create_with_details(
                patient_id,
                doctor_id,
                intake_date_str,
                intake_time_str,
                "pending",
                service_name,
                reason_note,
            )
            if not create_result.get("status"):
                self._set_intake_feedback(
                    create_result.get("message") or "Không thể tạo lượt khám mới để tiếp nhận.",
                    is_error=True,
                )
                return

            created_appts = AppointmentController.get_by_patient(patient_id) or []
            self.intake_selected_appointment = created_appts[0] if created_appts else None
            if not self.intake_selected_appointment:
                self._set_intake_feedback("Đã tạo lịch nhưng chưa đọc lại được dữ liệu lịch hẹn.", is_error=True)
                return

        appointment_id = self.intake_selected_appointment.get("appointment_id")

        confirm_message = (
            f"Bạn có chắc muốn xác nhận tiếp nhận lịch hẹn #{appointment_id}?\n"
            f"- Bệnh nhân #{patient_id}\n"
            f"- Dịch vụ: {service_name}\n"
            f"- Bác sĩ ID: {doctor_id}\n"
            f"- Thời gian: {intake_date_str} {intake_time_str}"
        )
        reply = QtWidgets.QMessageBox.question(
            self,
            "Xác nhận tiếp nhận",
            confirm_message,
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        )
        if reply != QtWidgets.QMessageBox.StandardButton.Yes:
            self._set_intake_feedback("Đã hủy thao tác xác nhận tiếp nhận.", is_error=True)
            return

        try:
            result = AppointmentController.confirm_intake_checkin(
                appointment_id,
                patient_id,
                doctor_id,
                service_name,
                intake_date_str,
                intake_time_str,
                reason_note,
            )
        except Exception:
            self._set_intake_feedback(
                "Check-in bị gián đoạn tạm thời. Vui lòng thử lại sau vài giây.",
                is_error=True,
            )
            return
        if not result.get("status"):
            self._set_intake_feedback(result.get("message") or "Check-in thất bại. Không thể cập nhật trạng thái hàng chờ.", is_error=True)
            return

        next_status = str(result.get("next_status") or "in_progress")
        self.intake_selected_appointment["status"] = next_status
        self.intake_selected_appointment["doctor_id"] = doctor_id
        self.intake_selected_appointment["appointment_date"] = result.get("intake_time") or self.intake_selected_appointment.get("appointment_date")
        self.intake_selected_appointment["note"] = result.get("note") or self.intake_selected_appointment.get("note")
        self.shared_selected_appointment_id = appointment_id
        self.shared_selected_patient_id = patient_id
        self.shared_selected_service_name = service_name
        self.intake_appointment_summary.setText(
            "Đã check-in vào hàng chờ: "
            f"Lịch hẹn #{appointment_id} - trạng thái {next_status}"
        )
        self._refresh_staff_waiting_pipeline()
        success_message = result.get("message") or "Check-in thành công. Bệnh nhân đã được chuyển vào hàng chờ khám."
        self._set_intake_feedback(success_message, is_error=False)
        QtWidgets.QMessageBox.information(self, "Tiếp nhận", success_message)

    def _refresh_staff_waiting_list(self):
        waiting_widget = getattr(self, "staff_dashboard_waiting_list", None)
        if waiting_widget is None:
            return

        waiting_widget.clear()
        appointments = AppointmentController.get_all() or []
        queue_rows = []
        for appt in appointments:
            status = str(appt.get("status") or "").lower().strip()
            if status not in {"confirmed", "in_progress"}:
                continue
            queue_rows.append(appt)

        queue_rows.sort(key=lambda row: str(row.get("appointment_date") or ""))
        for appt in queue_rows[:20]:
            service_text = self._extract_service_name_from_note(str(appt.get("note") or ""))
            waiting_widget.addItem(
                f"#{appt.get('appointment_id', '')} - {appt.get('patient_name', '(chưa rõ bệnh nhân)')} | {appt.get('appointment_date', 'Không rõ giờ')} | {service_text}"
            )

    def _refresh_staff_waiting_pipeline(self):
        self._refresh_staff_appointment_table()
        self._refresh_staff_waiting_list()
        self._refresh_staff_notifications()

    def _handle_intake_reset(self):
        self.intake_selected_patient = None
        self.intake_selected_appointment = None
        self.intake_patient_mode = "new"
        self.intake_date_value = QtCore.QDate.currentDate()
        self.intake_time_value = QtCore.QTime.currentTime()
        self.intake_selected_service = ""
        self.intake_selected_doctor = ""
        self.intake_reason_value = ""

        self.shared_selected_patient_id = None
        self.shared_selected_appointment_id = None
        self.shared_selected_service_name = ""

        self.intake_mode_new_radio.setChecked(True)

        self.intake_name_input.clear()
        self.intake_phone_input.clear()
        self.intake_phone_profile_input.clear()
        self.intake_cccd_input.clear()
        self.intake_cccd_profile_input.clear()
        self.intake_dob_input.setDate(QtCore.QDate.currentDate())
        self.intake_gender_input.setCurrentIndex(0)
        self.intake_email_input.clear()
        self.intake_occupation_input.clear()
        self.intake_address_input.clear()
        self.intake_note_input.clear()

        self.intake_date_input.setDate(QtCore.QDate.currentDate())
        self.intake_time_input.setTime(QtCore.QTime.currentTime())
        if self.intake_service_combo.count() > 0:
            self.intake_service_combo.setCurrentIndex(0)
        if self.intake_doctor_combo.count() > 0:
            self.intake_doctor_combo.setCurrentIndex(0)
        self.intake_reason_input.clear()

        self.intake_patient_summary.setText("Chưa chọn bệnh nhân.")
        self.intake_appointment_summary.setText("Trạng thái: Chờ khám")
        self.intake_lookup_result_card.setStyleSheet(
            "QFrame#intakeLookupResult { background: #ffffff; border: 1px solid #e4ebf4; border-radius: 12px; }"
        )
        self.intake_lookup_result_label.setStyleSheet("font-size: 13px; color: #475569; font-weight: 700;")
        self.intake_lookup_result_label.setText("Nhập SĐT/CCCD/mã bệnh nhân để tìm hồ sơ đã có.")

        self.intake_feedback.setStyleSheet(self._intake_feedback_style("info"))
        self.intake_feedback.setText("Đã xóa toàn bộ thông tin tiếp nhận. Bạn có thể nhập mới.")
        self.intake_feedback.setVisible(True)
        self._refresh_intake_summary_card()

    @staticmethod
    def _intake_input_style():
        return (
            "QLineEdit, QComboBox, QDateEdit, QTimeEdit, QPlainTextEdit {"
            " background: #ffffff; border: 1px solid #dbe4ee; border-radius: 9px;"
            " padding: 9px 12px; color: #0f172a; font-size: 13px; min-height: 24px; }"
            "QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTimeEdit:focus, QPlainTextEdit:focus {"
            " border: 1px solid #18a66d; }"
            "QLineEdit:disabled, QComboBox:disabled, QDateEdit:disabled, QTimeEdit:disabled, QPlainTextEdit:disabled {"
            " background: #f1f5f9; border: 1px solid #d1d5db; color: #94a3b8; }"
        )

    @staticmethod
    def _plain_text_value(widget):
        if hasattr(widget, "toPlainText"):
            return str(widget.toPlainText() or "").strip()
        if hasattr(widget, "text"):
            return str(widget.text() or "").strip()
        return ""

    @staticmethod
    def _build_intake_field(label_text, widget):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        label = QtWidgets.QLabel(label_text)
        label.setStyleSheet("border: none; background: transparent; font-size: 12px; color: #334155; font-weight: 800;")
        if isinstance(widget, (QtWidgets.QLineEdit, QtWidgets.QComboBox, QtWidgets.QDateEdit, QtWidgets.QTimeEdit)):
            widget.setMinimumHeight(42)
        layout.addWidget(label)
        layout.addWidget(widget)
        return wrapper

    def _build_intake_gender_selector(self):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 7, 0, 7)
        layout.setSpacing(24)
        self.intake_gender_male_radio = QtWidgets.QRadioButton("Nam")
        self.intake_gender_female_radio = QtWidgets.QRadioButton("Nữ")
        self.intake_gender_other_radio = QtWidgets.QRadioButton("Khác")
        radios = [
            ("Nam", self.intake_gender_male_radio),
            ("Nữ", self.intake_gender_female_radio),
            ("Khác", self.intake_gender_other_radio),
        ]
        for value, radio in radios:
            radio.setStyleSheet(self._intake_radio_style())
            radio.toggled.connect(lambda checked, gender=value: self._set_intake_gender_value(gender, checked))
            layout.addWidget(radio)
        layout.addStretch()
        self.intake_gender_male_radio.setChecked(True)
        return wrapper

    def _set_intake_gender_value(self, gender, checked):
        if checked and self.intake_gender_input.currentText() != gender:
            self.intake_gender_input.setCurrentText(gender)

    def _sync_intake_gender_radios(self, gender):
        mapping = {
            "Nam": self.intake_gender_male_radio,
            "Nữ": self.intake_gender_female_radio,
            "Khác": self.intake_gender_other_radio,
        }
        radio = mapping.get(gender)
        if radio and not radio.isChecked():
            radio.blockSignals(True)
            radio.setChecked(True)
            radio.blockSignals(False)

    @staticmethod
    def _intake_primary_button_style():
        return (
            "QPushButton { background: #13a66b; color: white; padding: 11px 14px;"
            " border: 1px solid #12915f; border-radius: 9px; font-weight: 900; font-size: 13px; }"
            "QPushButton:hover { background: #178a60; }"
            "QPushButton:pressed { background: #147a55; }"
            "QPushButton:disabled { background: #a7f3d0; color: #ecfdf5; border: 1px solid #86efac; }"
        )

    @staticmethod
    def _intake_secondary_button_style():
        return (
            "QPushButton { background: #ffffff; color: #334155; padding: 11px 14px;"
            " border: 1px solid #dbe4ee; border-radius: 9px; font-weight: 900; font-size: 13px; }"
            "QPushButton:hover { background: #e2e8f0; }"
            "QPushButton:pressed { background: #cbd5e1; }"
            "QPushButton:disabled { background: #f1f5f9; color: #94a3b8; border: 1px solid #d1d5db; }"
        )

    @staticmethod
    def _intake_radio_style():
        return (
            "QRadioButton { color: #0f172a; font-size: 13px; font-weight: 600; spacing: 6px; }"
            "QRadioButton::indicator { width: 14px; height: 14px; border-radius: 7px;"
            " border: 1px solid #94a3b8; background: #ffffff; }"
            "QRadioButton::indicator:checked { border: 1px solid #1A9B6C; background: #1A9B6C; }"
            "QRadioButton:disabled { color: #94a3b8; }"
            "QRadioButton::indicator:disabled { border: 1px solid #cbd5e1; background: #f1f5f9; }"
        )

    @staticmethod
    def _intake_feedback_style(state="info"):
        style_map = {
            "error": "background: #fef2f2; border: 1px solid #fca5a5; color: #991b1b;",
            "success": "background: #ecfdf5; border: 1px solid #86efac; color: #166534;",
            "info": "background: #f1f5f9; border: 1px solid #cbd5e1; color: #334155;",
        }
        base = style_map.get(state, style_map["info"])
        return f"font-size: 13px; font-weight: 600; border-radius: 8px; padding: 8px 10px; {base}"

    def _build_staff_patient_list_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: #f8fbff; border: none;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        if not hasattr(self, "staff_patient_mock_rows") or not self.staff_patient_mock_rows:
            self.staff_patient_mock_rows = self._build_staff_patient_mock_data()

        header = QtWidgets.QFrame()
        header.setStyleSheet("background: transparent; border: none;")
        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(4, 0, 4, 0)
        header_layout.setSpacing(12)

        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(3)
        heading = QtWidgets.QLabel("Danh sách bệnh nhân")
        heading.setStyleSheet(
            "border: none; background: transparent; font-size: 25px; color: #0f172a; font-weight: 900;"
        )
        breadcrumb = QtWidgets.QLabel("Trang chủ  >  Danh sách bệnh nhân")
        breadcrumb.setStyleSheet(
            "border: none; background: transparent; font-size: 13px; color: #94a3b8; font-weight: 700;"
        )
        title_col.addWidget(heading)
        title_col.addWidget(breadcrumb)

        bell = QtWidgets.QLabel("🔔")
        bell.setFixedSize(34, 34)
        bell.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        bell.setStyleSheet("border: none; background: transparent; font-size: 21px; color: #64748b;")
        avatar = QtWidgets.QLabel("👤")
        avatar.setFixedSize(42, 42)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            "border: none; background: #eaf2ff; border-radius: 21px; font-size: 20px; color: #2563eb;"
        )
        top_username = self.user_data.get("name") or "Nguyễn Thị Lan"
        username = QtWidgets.QLabel(top_username)
        username.setStyleSheet(
            "border: none; background: transparent; font-size: 13px; color: #0f172a; font-weight: 900;"
        )

        header_layout.addLayout(title_col, 1)
        header_layout.addWidget(bell)
        header_layout.addWidget(avatar)
        header_layout.addWidget(username)
        layout.addWidget(header)

        filter_card = self._build_section_card("")
        filter_layout = filter_card.layout()
        filter_layout.setSpacing(11)

        search_row = QtWidgets.QHBoxLayout()
        search_row.setSpacing(10)
        self.staff_patient_search_input = QtWidgets.QLineEdit()
        self.staff_patient_search_input.setPlaceholderText("Nhập tên, SĐT, CCCD hoặc mã bệnh nhân...")
        self.staff_patient_search_input.setStyleSheet(self._intake_input_style())
        self.staff_patient_search_input.setMinimumHeight(44)
        self.staff_patient_search_input.textChanged.connect(self._filter_staff_patients)

        search_btn = QtWidgets.QPushButton("🔎  Tìm kiếm")
        search_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        search_btn.setStyleSheet(self._intake_primary_button_style())
        search_btn.clicked.connect(self._filter_staff_patients)

        filter_btn = QtWidgets.QPushButton("⚙  Bộ lọc")
        filter_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        filter_btn.setStyleSheet(self._intake_secondary_button_style())
        filter_btn.clicked.connect(lambda: self._set_staff_patient_info_hint("Bộ lọc nhanh đang hiển thị ngay bên dưới."))

        add_btn = QtWidgets.QPushButton("+  Thêm bệnh nhân")
        add_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        add_btn.setStyleSheet(self._intake_primary_button_style())
        add_btn.clicked.connect(self._open_staff_patient_create_dialog)

        search_row.addWidget(self.staff_patient_search_input, 1)
        search_row.addWidget(search_btn)
        search_row.addWidget(filter_btn)
        search_row.addWidget(add_btn)
        filter_layout.addLayout(search_row)

        quick_filter_row = QtWidgets.QHBoxLayout()
        quick_filter_row.setSpacing(10)
        self.staff_patient_gender_filter = self._build_staff_patient_filter_combo("Giới tính", ["Tất cả", "Nam", "Nữ"])
        self.staff_patient_age_filter = self._build_staff_patient_filter_combo(
            "Độ tuổi", ["Tất cả", "Trẻ em", "Người lớn", "Người cao tuổi"]
        )
        self.staff_patient_doctor_filter = self._build_staff_patient_filter_combo(
            "Bác sĩ", self._staff_patient_doctor_filter_options()
        )
        self.staff_patient_status_filter = self._build_staff_patient_filter_combo(
            "Trạng thái", ["Tất cả", "Khám mới", "Tái khám", "Đang điều trị", "Đã hoàn tất"]
        )
        for combo in [
            self.staff_patient_gender_filter,
            self.staff_patient_age_filter,
            self.staff_patient_doctor_filter,
            self.staff_patient_status_filter,
        ]:
            combo.currentTextChanged.connect(self._filter_staff_patients)
            quick_filter_row.addWidget(combo)

        refresh_btn = QtWidgets.QPushButton("↻  Làm mới")
        refresh_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        refresh_btn.setStyleSheet(self._intake_secondary_button_style())
        refresh_btn.clicked.connect(self._reset_staff_patient_filters)
        quick_filter_row.addWidget(refresh_btn)
        filter_layout.addLayout(quick_filter_row)
        layout.addWidget(filter_card)

        body = QtWidgets.QHBoxLayout()
        body.setSpacing(14)

        list_card = self._build_section_card("")
        list_layout = list_card.layout()

        list_header = QtWidgets.QHBoxLayout()
        self.staff_patient_list_title = QtWidgets.QLabel("Danh sách bệnh nhân (0)")
        self.staff_patient_list_title.setStyleSheet(
            "border: none; background: transparent; font-size: 17px; color: #0f172a; font-weight: 900;"
        )
        self.staff_patient_feedback = QtWidgets.QLabel("Đang tải dữ liệu bệnh nhân.")
        self.staff_patient_feedback.setStyleSheet(
            "border: none; background: transparent; font-size: 12px; color: #64748b; font-weight: 700;"
        )
        list_header.addWidget(self.staff_patient_list_title)
        list_header.addStretch()
        list_header.addWidget(self.staff_patient_feedback)
        list_layout.addLayout(list_header)

        self.staff_patient_table = QtWidgets.QTableWidget()
        self.staff_patient_table.setColumnCount(8)
        self.staff_patient_table.setHorizontalHeaderLabels(
            ["STT", "Mã BN", "Họ và tên", "Giới tính", "Ngày sinh", "SĐT", "Trạng thái", "Thao tác"]
        )
        self.staff_patient_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.staff_patient_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.staff_patient_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_patient_table.setShowGrid(False)
        self.staff_patient_table.verticalHeader().setVisible(False)
        self.staff_patient_table.verticalHeader().setDefaultSectionSize(56)
        self.staff_patient_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staff_patient_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_patient_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_patient_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_patient_table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_patient_table.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_patient_table.horizontalHeader().setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_patient_table.itemSelectionChanged.connect(self._handle_staff_patient_selection)
        self.staff_patient_table.setMinimumWidth(770)
        self.staff_patient_table.setStyleSheet(
            "QTableWidget { background: #ffffff; border: none; color: #0f172a; font-size: 13px; font-weight: 600; }"
            "QHeaderView::section { background: #f8fafc; color: #475569; border: none; border-bottom: 1px solid #e5edf7;"
            " padding: 10px 8px; font-size: 12px; font-weight: 900; }"
            "QTableWidget::item { border-bottom: 1px solid #eef2f7; padding: 8px; }"
            "QTableWidget::item:selected { background: #ecfdf5; color: #0f172a; }"
        )
        list_layout.addWidget(self.staff_patient_table, 1)

        pagination_row = QtWidgets.QHBoxLayout()
        pagination_row.setSpacing(8)
        page_size_label = QtWidgets.QLabel("Hiển thị")
        page_size_label.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        self.staff_patient_page_size_combo = QtWidgets.QComboBox()
        self.staff_patient_page_size_combo.addItems(["10", "20", "50"])
        self.staff_patient_page_size_combo.setCurrentText("10")
        self.staff_patient_page_size_combo.setMinimumWidth(72)
        self.staff_patient_page_size_combo.setStyleSheet(
            "QComboBox { background: #ffffff; border: 1px solid #dbe4ee; border-radius: 8px;"
            " padding: 6px 10px; color: #334155; font-size: 12px; font-weight: 800; }"
        )
        self.staff_patient_page_size_combo.currentTextChanged.connect(self._change_staff_patient_page_size)
        page_size_suffix = QtWidgets.QLabel("bản ghi")
        page_size_suffix.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")

        self.staff_patient_prev_page_btn = QtWidgets.QPushButton("<")
        self.staff_patient_next_page_btn = QtWidgets.QPushButton(">")
        for btn in [self.staff_patient_prev_page_btn, self.staff_patient_next_page_btn]:
            btn.setFixedSize(32, 30)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(
                "QPushButton { background: #ffffff; border: 1px solid #dbe4ee; border-radius: 8px;"
                " color: #334155; font-size: 12px; font-weight: 900; }"
                "QPushButton:hover { background: #f8fafc; }"
            )
        self.staff_patient_prev_page_btn.clicked.connect(lambda: self._go_staff_patient_page(self.staff_patient_current_page - 1))
        self.staff_patient_next_page_btn.clicked.connect(lambda: self._go_staff_patient_page(self.staff_patient_current_page + 1))

        pagination_row.addWidget(page_size_label)
        pagination_row.addWidget(self.staff_patient_page_size_combo)
        pagination_row.addWidget(page_size_suffix)
        pagination_row.addStretch()
        pagination_row.addWidget(self.staff_patient_prev_page_btn)
        self.staff_patient_page_buttons_holder = QtWidgets.QHBoxLayout()
        self.staff_patient_page_buttons_holder.setSpacing(6)
        pagination_row.addLayout(self.staff_patient_page_buttons_holder)
        pagination_row.addWidget(self.staff_patient_next_page_btn)
        list_layout.addLayout(pagination_row)

        detail_col = QtWidgets.QVBoxLayout()
        detail_col.setSpacing(14)

        detail_card = self._build_section_card("Thông tin bệnh nhân")
        detail_layout = detail_card.layout()
        detail_layout.setSpacing(10)

        profile = QtWidgets.QFrame()
        profile.setStyleSheet("QFrame { background: #ffffff; border: none; }")
        profile_layout = QtWidgets.QHBoxLayout(profile)
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.setSpacing(12)

        self.staff_patient_avatar = QtWidgets.QLabel("👤")
        self.staff_patient_avatar.setFixedSize(60, 60)
        self.staff_patient_avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.staff_patient_avatar.setStyleSheet(
            "border: none; background: #ecfeff; border-radius: 30px; color: #0891b2; font-size: 28px;"
        )
        identity_col = QtWidgets.QVBoxLayout()
        identity_col.setSpacing(4)
        name_row = QtWidgets.QHBoxLayout()
        self.staff_patient_detail_name = QtWidgets.QLabel("Chưa chọn bệnh nhân")
        self.staff_patient_detail_name.setStyleSheet(
            "border: none; background: transparent; font-size: 16px; color: #0f172a; font-weight: 900;"
        )
        self.staff_patient_detail_badge = QtWidgets.QLabel("-")
        self.staff_patient_detail_badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.staff_patient_detail_badge.setStyleSheet(self._staff_patient_gender_badge_style("Khác"))
        name_row.addWidget(self.staff_patient_detail_name, 1)
        name_row.addWidget(self.staff_patient_detail_badge)
        self.staff_patient_detail_meta = QtWidgets.QLabel("Mã BN: -")
        self.staff_patient_detail_meta.setStyleSheet(
            "border: none; background: transparent; font-size: 12px; color: #64748b; font-weight: 800;"
        )
        identity_col.addLayout(name_row)
        identity_col.addWidget(self.staff_patient_detail_meta)
        profile_layout.addWidget(self.staff_patient_avatar)
        profile_layout.addLayout(identity_col, 1)
        detail_layout.addWidget(profile)

        self.staff_patient_empty_state = QtWidgets.QLabel("Chọn một bệnh nhân trong bảng để xem thông tin chi tiết.")
        self.staff_patient_empty_state.setWordWrap(True)
        self.staff_patient_empty_state.setStyleSheet(
            "border: none; background: transparent; font-size: 12px; color: #64748b; font-weight: 700;"
        )
        detail_layout.addWidget(self.staff_patient_empty_state)

        info_grid = QtWidgets.QFormLayout()
        info_grid.setHorizontalSpacing(16)
        info_grid.setVerticalSpacing(7)
        self.staff_patient_info_code = QtWidgets.QLabel("-")
        self.staff_patient_info_dob = QtWidgets.QLabel("-")
        self.staff_patient_info_phone = QtWidgets.QLabel("-")
        self.staff_patient_info_cccd = QtWidgets.QLabel("-")
        self.staff_patient_info_address = QtWidgets.QLabel("-")
        self.staff_patient_info_status = QtWidgets.QLabel("-")
        for label in [
            self.staff_patient_info_code,
            self.staff_patient_info_dob,
            self.staff_patient_info_phone,
            self.staff_patient_info_cccd,
            self.staff_patient_info_address,
            self.staff_patient_info_status,
        ]:
            label.setWordWrap(True)
            label.setStyleSheet("font-size: 12px; color: #0f172a; font-weight: 700;")

        info_grid.addRow("Mã bệnh nhân:", self.staff_patient_info_code)
        info_grid.addRow("Ngày sinh:", self.staff_patient_info_dob)
        info_grid.addRow("Điện thoại:", self.staff_patient_info_phone)
        info_grid.addRow("CCCD:", self.staff_patient_info_cccd)
        info_grid.addRow("Địa chỉ:", self.staff_patient_info_address)
        info_grid.addRow("Trạng thái:", self.staff_patient_info_status)
        detail_layout.addLayout(info_grid)

        self.staff_patient_detail_tabs = QtWidgets.QTabWidget()
        self.staff_patient_detail_tabs.setStyleSheet(
            "QTabWidget::pane { border: 1px solid #e4ebf4; border-radius: 10px; background: #ffffff; }"
            "QTabBar::tab { background: #f8fafc; border: 1px solid #e4ebf4; border-bottom: none;"
            " border-top-left-radius: 8px; border-top-right-radius: 8px; padding: 7px 10px;"
            " color: #64748b; font-size: 11px; font-weight: 900; }"
            "QTabBar::tab:selected { background: #dcfce7; color: #15803d; border-color: #bbf7d0; }"
        )

        common_tab = QtWidgets.QWidget()
        common_layout = QtWidgets.QFormLayout(common_tab)
        common_layout.setHorizontalSpacing(12)
        common_layout.setVerticalSpacing(8)
        self.staff_patient_common_blood = QtWidgets.QLabel("-")
        self.staff_patient_common_allergy = QtWidgets.QLabel("-")
        self.staff_patient_common_job = QtWidgets.QLabel("-")
        self.staff_patient_common_emergency = QtWidgets.QLabel("-")
        for label in [
            self.staff_patient_common_blood,
            self.staff_patient_common_allergy,
            self.staff_patient_common_job,
            self.staff_patient_common_emergency,
        ]:
            label.setStyleSheet("font-size: 12px; color: #334155; font-weight: 700;")
            label.setWordWrap(True)
        common_layout.addRow("Nhóm máu", self.staff_patient_common_blood)
        common_layout.addRow("Dị ứng", self.staff_patient_common_allergy)
        common_layout.addRow("Nghề nghiệp", self.staff_patient_common_job)
        common_layout.addRow("Liên hệ khẩn cấp", self.staff_patient_common_emergency)

        history_tab = QtWidgets.QWidget()
        history_layout = QtWidgets.QVBoxLayout(history_tab)
        history_layout.setContentsMargins(6, 6, 6, 6)
        history_layout.setSpacing(8)
        self.staff_patient_history_table = QtWidgets.QTableWidget()
        self.staff_patient_history_table.setColumnCount(4)
        self.staff_patient_history_table.setHorizontalHeaderLabels(["Ngày giờ", "Trạng thái", "Bác sĩ", "Dịch vụ"])
        self.staff_patient_history_table.verticalHeader().setVisible(False)
        self.staff_patient_history_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staff_patient_history_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_patient_history_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.staff_patient_history_table.setMinimumHeight(132)
        self.staff_patient_history_empty = QtWidgets.QLabel("Chưa có lịch sử khám để hiển thị.")
        self.staff_patient_history_empty.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        history_layout.addWidget(self.staff_patient_history_table)
        history_layout.addWidget(self.staff_patient_history_empty)

        self.staff_patient_appointments_tab_content = QtWidgets.QLabel(
            "Các lịch hẹn sắp tới sẽ hiển thị ở đây khi bệnh nhân có lịch mới."
        )
        self.staff_patient_appointments_tab_content.setWordWrap(True)
        self.staff_patient_appointments_tab_content.setStyleSheet(
            "font-size: 12px; color: #334155; background: #f8fafc; border-radius: 8px; padding: 8px;"
        )
        appointments_tab = QtWidgets.QWidget()
        appointments_layout = QtWidgets.QVBoxLayout(appointments_tab)
        appointments_layout.setContentsMargins(8, 8, 8, 8)
        appointments_layout.addWidget(self.staff_patient_appointments_tab_content)

        self.staff_patient_invoices_tab_content = QtWidgets.QLabel(
            "Danh sách hóa đơn và trạng thái thanh toán sẽ hiển thị ở đây."
        )
        self.staff_patient_invoices_tab_content.setWordWrap(True)
        self.staff_patient_invoices_tab_content.setStyleSheet(
            "font-size: 12px; color: #334155; background: #f8fafc; border-radius: 8px; padding: 8px;"
        )
        invoices_tab = QtWidgets.QWidget()
        invoices_layout = QtWidgets.QVBoxLayout(invoices_tab)
        invoices_layout.setContentsMargins(8, 8, 8, 8)
        invoices_layout.addWidget(self.staff_patient_invoices_tab_content)

        self.staff_patient_detail_tabs.addTab(common_tab, "Thông tin chung")
        self.staff_patient_detail_tabs.addTab(history_tab, "Lịch sử khám")
        self.staff_patient_detail_tabs.addTab(appointments_tab, "Lịch hẹn")
        self.staff_patient_detail_tabs.addTab(invoices_tab, "Hóa đơn")
        detail_layout.addWidget(self.staff_patient_detail_tabs)

        notes_label = QtWidgets.QLabel("Ghi chú")
        notes_label.setStyleSheet(
            "border: none; background: transparent; font-size: 13px; color: #0f172a; font-weight: 900;"
        )
        self.staff_patient_note_text = QtWidgets.QTextEdit()
        self.staff_patient_note_text.setReadOnly(True)
        self.staff_patient_note_text.setMinimumHeight(74)
        self.staff_patient_note_text.setStyleSheet(
            "QTextEdit { background: #f8fafc; border: 1px solid #e4ebf4; border-radius: 10px;"
            " color: #334155; font-size: 12px; font-weight: 600; padding: 8px; }"
        )
        detail_layout.addWidget(notes_label)
        detail_layout.addWidget(self.staff_patient_note_text)

        quick_card = self._build_section_card("Thao tác nhanh")
        quick_layout = quick_card.layout()
        quick_grid = QtWidgets.QGridLayout()
        quick_grid.setHorizontalSpacing(9)
        quick_grid.setVerticalSpacing(9)
        quick_actions = [
            ("👁", "Xem hồ sơ", "#E0F2FE", "#0369A1", "view"),
            ("📅", "Tạo lịch hẹn", "#DCFCE7", "#15803D", "appointment"),
            ("💵", "Tạo hóa đơn", "#FEF9C3", "#B45309", "billing"),
            ("🖨", "In phiếu khám", "#F3E8FF", "#7E22CE", "print"),
            ("✉", "Gửi SMS", "#E0F7FA", "#0E7490", "sms"),
            ("✎", "Chỉnh sửa", "#F3F4F6", "#334155", "edit"),
        ]
        for idx, (icon, label, bg, fg, key) in enumerate(quick_actions):
            btn = self._build_staff_patient_quick_button(icon, label, bg, fg)
            btn.clicked.connect(lambda _checked=False, action_key=key: self._handle_staff_patient_quick_action(action_key))
            quick_grid.addWidget(btn, idx // 3, idx % 3)
        quick_layout.addLayout(quick_grid)

        detail_col.addWidget(detail_card)
        detail_col.addWidget(quick_card)
        body.addWidget(list_card, 11)
        body.addLayout(detail_col, 6)
        layout.addLayout(body, 1)

        self.staff_patient_current_page = 1
        self.staff_patient_total_pages = 1
        self.staff_patient_pagination_buttons = []
        self.staff_patient_using_mock_data = False
        self._refresh_staff_patient_table()
        self._reset_staff_patient_detail("Chọn một bệnh nhân trong bảng để xem thông tin chi tiết.")
        return page

    def _build_staff_patient_filter_combo(self, label, values):
        combo = QtWidgets.QComboBox()
        combo.addItems(values)
        combo.setMinimumHeight(40)
        combo.setToolTip(label)
        combo.setStyleSheet(
            "QComboBox { background: #ffffff; border: 1px solid #dbe4ee; border-radius: 9px;"
            " padding: 8px 12px; color: #334155; font-size: 12px; font-weight: 800; }"
            "QComboBox::drop-down { border: none; width: 22px; }"
        )
        return combo

    def _staff_patient_doctor_filter_options(self):
        options = ["Tất cả"]
        if hasattr(self, "staff_patient_mock_rows") and self.staff_patient_mock_rows:
            for patient in self.staff_patient_mock_rows:
                doctor_name = str(patient.get("preferred_doctor") or "").strip()
                if doctor_name and doctor_name not in options:
                    options.append(doctor_name)
        try:
            doctors = DoctorController.get_all() or []
        except Exception:
            doctors = []
        for doctor in doctors:
            name = str(doctor.get("name") or doctor.get("doctor_name") or doctor.get("full_name") or "").strip()
            if name and name not in options:
                options.append(name)
        if len(options) == 1:
            options.extend(["BS. Minh", "BS. Lan"])
        return options

    def _reset_staff_patient_filters(self):
        if hasattr(self, "staff_patient_search_input"):
            self.staff_patient_search_input.clear()
        for combo_name in [
            "staff_patient_gender_filter",
            "staff_patient_age_filter",
            "staff_patient_doctor_filter",
            "staff_patient_status_filter",
        ]:
            combo = getattr(self, combo_name, None)
            if combo:
                combo.setCurrentIndex(0)
        self.staff_patient_current_page = 1
        self._refresh_staff_patient_table()

    def _refresh_staff_patient_table(self):
        patients = []
        self.staff_patient_using_mock_data = False
        try:
            patients = PatientController.get_all() or []
        except Exception:
            patients = []

        # Use resilient mock data when DB is empty/unavailable to keep staff UI operable.
        if not patients:
            patients = [dict(row) for row in getattr(self, "staff_patient_mock_rows", [])]
            self.staff_patient_using_mock_data = True

        self.staff_patient_rows = patients
        self.staff_patient_history_cache = {}
        self._filter_staff_patients()

    def _filter_staff_patients(self):
        if not hasattr(self, "staff_patient_table"):
            return
        query = str(self.staff_patient_search_input.text() if hasattr(self, "staff_patient_search_input") else "").strip().lower()
        gender_filter = self._combo_text("staff_patient_gender_filter")
        age_filter = self._combo_text("staff_patient_age_filter")
        doctor_filter = self._combo_text("staff_patient_doctor_filter")
        status_filter = self._combo_text("staff_patient_status_filter")
        filtered = []

        for patient in self.staff_patient_rows:
            patient_id = str(patient.get("patient_id") or "")
            code = self._staff_patient_code(patient)
            name = str(patient.get("name") or "")
            phone = str(patient.get("phone") or "")
            cccd = str(patient.get("cccd") or patient.get("citizen_id") or patient.get("id_card") or "")
            gender = str(patient.get("gender") or "")
            status = self._derive_staff_patient_status(patient)
            haystack = f"{patient_id} {code} {name} {phone} {cccd}".lower()
            if query and query not in haystack:
                continue
            if gender_filter and gender_filter != "Tất cả" and gender != gender_filter:
                continue
            if age_filter and age_filter != "Tất cả" and not self._patient_matches_age_filter(patient, age_filter):
                continue
            if status_filter and status_filter != "Tất cả" and status != status_filter:
                continue
            if doctor_filter and doctor_filter != "Tất cả" and not self._patient_matches_doctor_filter(patient, doctor_filter):
                continue
            filtered.append(patient)

        self.staff_patient_filtered_rows = filtered
        if hasattr(self, "staff_patient_list_title"):
            self.staff_patient_list_title.setText(f"Danh sách bệnh nhân ({len(filtered)})")

        page_size = self._staff_patient_page_size()
        self.staff_patient_total_pages = max(1, math.ceil(len(filtered) / page_size)) if filtered else 1
        if self.staff_patient_current_page > self.staff_patient_total_pages:
            self.staff_patient_current_page = self.staff_patient_total_pages
        if self.staff_patient_current_page < 1:
            self.staff_patient_current_page = 1

        if not filtered:
            if hasattr(self, "staff_patient_feedback"):
                self.staff_patient_feedback.setText("Không có dữ liệu phù hợp.")
            self.staff_patient_table.setRowCount(0)
            self._refresh_staff_patient_pagination_controls(0, 0, 0)
            self._reset_staff_patient_detail("Không có bệnh nhân phù hợp với điều kiện lọc.")
            return

        if hasattr(self, "staff_patient_feedback"):
            self.staff_patient_feedback.setText(f"Hiển thị {len(filtered)} bệnh nhân")

        restored_row = None
        if self.staff_patient_selected:
            selected_id = str(self.staff_patient_selected.get("patient_id") or "")
            for idx, patient in enumerate(filtered):
                if str(patient.get("patient_id") or "") == selected_id:
                    restored_row = idx
                    break

        if restored_row is not None:
            self.staff_patient_current_page = (restored_row // page_size) + 1

        self._render_staff_patient_table_page()

    def _render_staff_patient_table_page(self):
        page_size = self._staff_patient_page_size()
        total = len(self.staff_patient_filtered_rows)
        if total == 0:
            self.staff_patient_table.setRowCount(0)
            self._refresh_staff_patient_pagination_controls(0, 0, 0)
            return

        start = (self.staff_patient_current_page - 1) * page_size
        end = min(start + page_size, total)
        page_rows = self.staff_patient_filtered_rows[start:end]

        self.staff_patient_table.blockSignals(True)
        self.staff_patient_table.setRowCount(len(page_rows))
        for row, patient in enumerate(page_rows):
            values = [
                str(start + row + 1),
                self._staff_patient_code(patient),
                str(patient.get("name") or "-"),
                str(patient.get("gender") or "-"),
                self._format_staff_patient_dob(patient),
                str(patient.get("phone") or "-"),
            ]
            for col, value in enumerate(values):
                item = QtWidgets.QTableWidgetItem(value)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
                self.staff_patient_table.setItem(row, col, item)
            status = self._derive_staff_patient_status(patient)
            self.staff_patient_table.setCellWidget(row, 6, self._build_staff_patient_status_badge(status))
            self.staff_patient_table.setCellWidget(row, 7, self._build_staff_patient_row_actions(patient.get("patient_id")))

        self.staff_patient_table.blockSignals(False)

        selected_row = 0
        if self.staff_patient_selected:
            selected_id = str(self.staff_patient_selected.get("patient_id") or "")
            for idx, patient in enumerate(page_rows):
                if str(patient.get("patient_id") or "") == selected_id:
                    selected_row = idx
                    break
        self.staff_patient_table.selectRow(selected_row)
        self._set_staff_patient_detail(page_rows[selected_row])
        self._refresh_staff_patient_pagination_controls(start, end, total)

    def _staff_patient_page_size(self):
        combo = getattr(self, "staff_patient_page_size_combo", None)
        if not combo:
            return 10
        try:
            return max(1, int(combo.currentText()))
        except (TypeError, ValueError):
            return 10

    def _change_staff_patient_page_size(self, *_args):
        self.staff_patient_current_page = 1
        self._render_staff_patient_table_page()

    def _go_staff_patient_page(self, page):
        self.staff_patient_current_page = max(1, min(page, self.staff_patient_total_pages))
        self._render_staff_patient_table_page()

    def _refresh_staff_patient_pagination_controls(self, start, end, total):
        if hasattr(self, "staff_patient_feedback") and total:
            suffix = " (dữ liệu mẫu)" if getattr(self, "staff_patient_using_mock_data", False) else ""
            self.staff_patient_feedback.setText(
                f"Hiển thị {start + 1}-{end} / {total} bệnh nhân{suffix}"
            )

        for btn in getattr(self, "staff_patient_pagination_buttons", []):
            btn.deleteLater()
        self.staff_patient_pagination_buttons = []

        if hasattr(self, "staff_patient_prev_page_btn"):
            self.staff_patient_prev_page_btn.setEnabled(self.staff_patient_current_page > 1 and total > 0)
        if hasattr(self, "staff_patient_next_page_btn"):
            self.staff_patient_next_page_btn.setEnabled(self.staff_patient_current_page < self.staff_patient_total_pages and total > 0)

        if not hasattr(self, "staff_patient_page_buttons_holder"):
            return

        buttons_to_show = min(self.staff_patient_total_pages, 5)
        start_page = max(1, self.staff_patient_current_page - 2)
        end_page = min(self.staff_patient_total_pages, start_page + buttons_to_show - 1)
        start_page = max(1, end_page - buttons_to_show + 1)
        for page in range(start_page, end_page + 1):
            page_btn = QtWidgets.QPushButton(str(page))
            page_btn.setFixedSize(32, 30)
            page_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            if page == self.staff_patient_current_page:
                page_btn.setStyleSheet(
                    "QPushButton { background: #10B981; color: white; border: none; border-radius: 8px; font-size: 12px; font-weight: 900; }"
                )
            else:
                page_btn.setStyleSheet(
                    "QPushButton { background: #ffffff; color: #334155; border: 1px solid #dbe4ee; border-radius: 8px;"
                    " font-size: 12px; font-weight: 900; }"
                    "QPushButton:hover { background: #f8fafc; }"
                )
            page_btn.clicked.connect(lambda _checked=False, p=page: self._go_staff_patient_page(p))
            self.staff_patient_pagination_buttons.append(page_btn)
            self.staff_patient_page_buttons_holder.addWidget(page_btn)

    def _combo_text(self, attr_name):
        combo = getattr(self, attr_name, None)
        return combo.currentText() if combo else ""

    def _handle_staff_patient_selection(self):
        if not hasattr(self, "staff_patient_table"):
            return
        row = self.staff_patient_table.currentRow()
        absolute_row = (self.staff_patient_current_page - 1) * self._staff_patient_page_size() + row
        if row < 0 or absolute_row < 0 or absolute_row >= len(self.staff_patient_filtered_rows):
            self._reset_staff_patient_detail("Chọn một bệnh nhân trong bảng để xem thông tin chi tiết.")
            return
        self._set_staff_patient_detail(self.staff_patient_filtered_rows[absolute_row])

    def _select_staff_patient_by_id(self, patient_id):
        target_id = str(patient_id or "")
        for row, patient in enumerate(self.staff_patient_filtered_rows):
            if str(patient.get("patient_id") or "") == target_id:
                self.staff_patient_selected = patient
                page_size = self._staff_patient_page_size()
                self.staff_patient_current_page = (row // page_size) + 1
                self._render_staff_patient_table_page()
                return

    def _set_staff_patient_detail(self, patient):
        self.staff_patient_selected = patient
        self.shared_selected_patient_id = patient.get("patient_id")
        patient_id = str(patient.get("patient_id") or "")
        if patient_id in getattr(self, "staff_patient_history_cache", {}):
            history = self.staff_patient_history_cache.get(patient_id, [])
        else:
            try:
                history = AppointmentController.get_by_patient(patient.get("patient_id")) or []
            except Exception:
                history = []
            self.staff_patient_history_cache[patient_id] = history

        status = self._derive_staff_patient_status(patient, history)
        name = str(patient.get("name") or "Chưa có tên")
        gender = str(patient.get("gender") or "-")
        dob = self._format_staff_patient_dob(patient)
        age_text = self._staff_patient_age_text(patient)
        phone = str(patient.get("phone") or "Chưa nhập SĐT")
        cccd = str(patient.get("cccd") or patient.get("citizen_id") or patient.get("id_card") or "Chưa nhập CCCD")
        address = str(patient.get("address") or "Chưa nhập địa chỉ")
        note = str(patient.get("note") or patient.get("notes") or "").strip()

        emergency = str(patient.get("emergency_contact") or "Nguyễn Thị Hồng (Vợ) - 0988 111 222")
        blood = str(patient.get("blood_type") or "O+")
        allergy = str(patient.get("allergies") or "Không")
        occupation = str(patient.get("job") or patient.get("occupation") or "Nhân viên văn phòng")

        self.staff_patient_detail_name.setText(name)
        self.staff_patient_detail_badge.setText(gender)
        self.staff_patient_detail_badge.setStyleSheet(self._staff_patient_gender_badge_style(gender))
        self.staff_patient_detail_meta.setText(f"{self._staff_patient_code(patient)}")
        self._set_staff_patient_info_hint(
            "Nhân viên chỉ xử lý thông tin hành chính, tạo lịch hẹn, in phiếu, hỗ trợ thanh toán."
        )
        self.staff_patient_info_code.setText(self._staff_patient_code(patient))
        self.staff_patient_info_dob.setText(f"{dob} ({age_text})")
        self.staff_patient_info_phone.setText(phone)
        self.staff_patient_info_cccd.setText(cccd)
        self.staff_patient_info_address.setText(address)
        self.staff_patient_info_status.setText(status)

        self.staff_patient_common_blood.setText(blood)
        self.staff_patient_common_allergy.setText(allergy)
        self.staff_patient_common_job.setText(occupation)
        self.staff_patient_common_emergency.setText(emergency)
        self.staff_patient_note_text.setPlainText(
            note or "Bệnh nhân có tiền sử đau dạ dày. Cân nhắc nhắc nhở kiêng đồ cay nóng."
        )

        self.staff_patient_appointments_tab_content.setText(
            f"Bệnh nhân {name} hiện có {len(history)} lần khám đã ghi nhận. "
            "Dùng nút 'Tạo lịch hẹn' để mở luồng điều phối lịch cho bệnh nhân này."
        )
        self.staff_patient_invoices_tab_content.setText(
            "Hóa đơn đang được quản lý tại trang 'Thanh toán & Hóa đơn'. "
            "Nhân viên có thể tạo mới và theo dõi trạng thái thanh toán từ đó."
        )

        self.staff_patient_history_table.setRowCount(len(history))
        for row, appt in enumerate(history):
            doctor_name = str(appt.get("doctor_name") or appt.get("doctor_id") or "-")
            service_summary = self._extract_service_name_from_note(str(appt.get("note") or "")) or str(appt.get("service_name") or "-")
            history_date = str(appt.get("appointment_date") or appt.get("date") or "-")
            appt_status = self._staff_status_label(str(appt.get("status") or ""))
            self.staff_patient_history_table.setItem(row, 0, QtWidgets.QTableWidgetItem(history_date))
            self.staff_patient_history_table.setItem(row, 1, QtWidgets.QTableWidgetItem(appt_status))
            self.staff_patient_history_table.setItem(row, 2, QtWidgets.QTableWidgetItem(doctor_name))
            self.staff_patient_history_table.setItem(row, 3, QtWidgets.QTableWidgetItem(service_summary))
        self.staff_patient_history_empty.setText(f"Hiển thị {len(history)} lịch hẹn gần nhất." if history else "Bệnh nhân này chưa có lịch sử khám.")

    def _reset_staff_patient_detail(self, message):
        self.staff_patient_selected = None
        self.shared_selected_patient_id = None
        if hasattr(self, "staff_patient_detail_name"):
            self.staff_patient_detail_name.setText("Chưa chọn bệnh nhân")
            self.staff_patient_detail_badge.setText("-")
            self.staff_patient_detail_badge.setStyleSheet(self._staff_patient_gender_badge_style("Khác"))
            self.staff_patient_detail_meta.setText("Mã BN: -")
            self._set_staff_patient_info_hint(message)
            self.staff_patient_info_code.setText("-")
            self.staff_patient_info_dob.setText("-")
            self.staff_patient_info_phone.setText("-")
            self.staff_patient_info_cccd.setText("-")
            self.staff_patient_info_address.setText("-")
            self.staff_patient_info_status.setText("-")

            self.staff_patient_common_blood.setText("-")
            self.staff_patient_common_allergy.setText("-")
            self.staff_patient_common_job.setText("-")
            self.staff_patient_common_emergency.setText("-")
            self.staff_patient_note_text.setPlainText("Chưa có ghi chú.")
            self.staff_patient_appointments_tab_content.setText(
                "Các lịch hẹn sắp tới sẽ hiển thị ở đây khi bệnh nhân có lịch mới."
            )
            self.staff_patient_invoices_tab_content.setText(
                "Danh sách hóa đơn và trạng thái thanh toán sẽ hiển thị ở đây."
            )
            self.staff_patient_history_table.setRowCount(0)
            self.staff_patient_history_empty.setText("Chưa có lịch sử khám để hiển thị.")

    def _staff_patient_code(self, patient):
        patient_id = patient.get("patient_id") or patient.get("id") or ""
        try:
            return f"BN{int(patient_id):06d}"
        except (TypeError, ValueError):
            return str(patient_id) or "BN------"

    def _format_staff_patient_dob(self, patient):
        dob = str(patient.get("dob") or patient.get("birth_date") or "").strip()
        if not dob:
            return "-"
        parsed = QtCore.QDate.fromString(dob, "yyyy-MM-dd")
        return parsed.toString("dd/MM/yyyy") if parsed.isValid() else dob

    def _staff_patient_age_text(self, patient):
        dob = str(patient.get("dob") or patient.get("birth_date") or "").strip()
        parsed = QtCore.QDate.fromString(dob, "yyyy-MM-dd")
        if not parsed.isValid():
            return "chưa rõ tuổi"
        today = QtCore.QDate.currentDate()
        age = today.year() - parsed.year()
        if today < parsed.addYears(age):
            age -= 1
        return f"{max(age, 0)} tuổi"

    def _patient_matches_age_filter(self, patient, age_filter):
        dob = str(patient.get("dob") or patient.get("birth_date") or "").strip()
        parsed = QtCore.QDate.fromString(dob, "yyyy-MM-dd")
        if not parsed.isValid():
            return False
        today = QtCore.QDate.currentDate()
        age = today.year() - parsed.year()
        if today < parsed.addYears(age):
            age -= 1
        if age_filter == "Trẻ em":
            return age < 16
        if age_filter == "Người lớn":
            return 16 <= age < 60
        if age_filter in {"Cao tuổi", "Người cao tuổi"}:
            return age >= 60
        return True

    def _patient_matches_doctor_filter(self, patient, doctor_filter):
        preferred_doctor = str(patient.get("preferred_doctor") or "")
        if preferred_doctor and doctor_filter.lower() in preferred_doctor.lower():
            return True
        patient_id = str(patient.get("patient_id") or "")
        if patient_id in getattr(self, "staff_patient_history_cache", {}):
            history = self.staff_patient_history_cache.get(patient_id, [])
        else:
            try:
                history = AppointmentController.get_by_patient(patient.get("patient_id")) or []
            except Exception:
                return True
            self.staff_patient_history_cache[patient_id] = history
        for appt in history:
            doctor_name = str(appt.get("doctor_name") or appt.get("doctor") or appt.get("doctor_id") or "")
            if doctor_filter.lower() in doctor_name.lower():
                return True
        return False

    def _derive_staff_patient_status(self, patient, history=None):
        explicit_status = str(patient.get("status") or patient.get("status_label") or "").strip()
        if explicit_status in {"Khám mới", "Tái khám", "Đang điều trị", "Đã hoàn tất"}:
            return explicit_status

        history = history or []
        status_values = {str(appt.get("status") or "") for appt in history}
        if {"confirmed", "in_progress", "pending"} & status_values:
            return "Đang điều trị"
        if "done" in status_values:
            return "Đã hoàn tất"
        return "Khám mới"

    def _staff_patient_status_badge_style(self, status):
        styles = {
            "Khám mới": ("#dcfce7", "#13a66b"),
            "Tái khám": ("#fff0df", "#f97316"),
            "Đang điều trị": ("#dbeafe", "#2563eb"),
            "Đã hoàn tất": ("#eee9ff", "#8b5cf6"),
            "Chưa chọn": ("#f1f5f9", "#64748b"),
        }
        bg, fg = styles.get(status, ("#f1f5f9", "#334155"))
        return f"background: {bg}; color: {fg}; border-radius: 10px; padding: 5px 10px; font-size: 11px; font-weight: 900;"

    def _build_staff_patient_status_badge(self, status):
        label = QtWidgets.QLabel(status)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(self._staff_patient_status_badge_style(status))
        return label

    @staticmethod
    def _staff_patient_gender_badge_style(gender):
        if str(gender).strip().lower() == "nam":
            return "background: #dbeafe; color: #1d4ed8; border-radius: 10px; padding: 5px 10px; font-size: 11px; font-weight: 900;"
        if str(gender).strip().lower() == "nữ":
            return "background: #fce7f3; color: #be185d; border-radius: 10px; padding: 5px 10px; font-size: 11px; font-weight: 900;"
        return "background: #f1f5f9; color: #475569; border-radius: 10px; padding: 5px 10px; font-size: 11px; font-weight: 900;"

    def _build_staff_patient_row_actions(self, patient_id=None):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        view_btn = QtWidgets.QPushButton("👁️")
        more_btn = QtWidgets.QPushButton("⋮")
        for btn in [view_btn, more_btn]:
            btn.setFixedSize(32, 28)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet("background: #eff6ff; color: #2563eb; border: none; border-radius: 8px; font-size: 13px; font-weight: 900;")
        view_btn.clicked.connect(lambda: self._select_staff_patient_by_id(patient_id))
        more_btn.clicked.connect(lambda: self._select_staff_patient_by_id(patient_id))
        layout.addWidget(view_btn)
        layout.addWidget(more_btn)
        return wrapper

    def _build_staff_patient_quick_button(self, icon, label, bg, fg):
        btn = QtWidgets.QPushButton(f"{icon}  {label}")
        btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        btn.setMinimumHeight(52)
        btn.setStyleSheet(
            f"QPushButton {{ background: {bg}; color: {fg}; border: none; border-radius: 10px;"
            " padding: 9px 10px; text-align: left; font-size: 12px; font-weight: 900; }}"
            "QPushButton:hover { border: 1px solid #cbd5e1; }"
        )
        return btn

    def _handle_staff_patient_quick_action(self, action):
        if not self.staff_patient_selected:
            self._set_staff_patient_info_hint("Vui lòng chọn bệnh nhân trước khi thao tác.")
            return
        self.shared_selected_patient_id = self.staff_patient_selected.get("patient_id")
        if action == "appointment":
            self.switch_page(2)
        elif action == "billing":
            self.switch_page(4)
        elif action == "edit":
            self._set_staff_patient_info_hint(
                "Chức năng chỉnh sửa hồ sơ đang tạm khóa ở màn Staff List. Vui lòng dùng luồng Tiếp nhận để cập nhật hành chính."
            )
        else:
            action_labels = {
                "view": "Đã mở phần xem hồ sơ tóm tắt ở panel bên phải.",
                "print": "Chức năng in phiếu khám đang chờ tích hợp máy in.",
                "sms": "Chức năng gửi SMS đang chờ cấu hình nhà cung cấp.",
            }
            self._set_staff_patient_info_hint(action_labels.get(action, "Đã chọn thao tác nhanh."))

    def _set_staff_patient_info_hint(self, text):
        if hasattr(self, "staff_patient_empty_state"):
            self.staff_patient_empty_state.setText(text)

    def _open_staff_patient_create_dialog(self):
        dialog = StaffPatientCreateDialog(self)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return

        payload = dialog.payload()
        form_payload = {
            "name": payload["name"],
            "dob": payload["dob"],
            "gender": payload["gender"],
            "phone": payload["phone"],
            "cccd": payload["cccd"],
            "address": payload["address"],
            "occupation": payload["occupation"],
            "intake_notes": "Tạo từ màn hình Danh sách bệnh nhân (Staff)",
            "patient_type": "general",
        }

        if not getattr(self, "staff_patient_using_mock_data", False):
            result = PatientController.create_with_status(form_payload)
            if not result.get("status"):
                self._set_staff_patient_info_hint(result.get("message") or "Không thể tạo bệnh nhân mới.")
                return
            self._refresh_staff_patient_table()
            latest_patient = PatientController.find_by_cccd_or_phone(
                cccd=payload["cccd"],
                phone=payload["phone"],
            )
            if latest_patient:
                self._select_staff_patient_by_id(latest_patient.get("patient_id"))
            self._set_staff_patient_info_hint("Đã thêm bệnh nhân mới vào cơ sở dữ liệu.")
            return

        max_patient_id = 0
        for row in self.staff_patient_rows:
            try:
                max_patient_id = max(max_patient_id, int(row.get("patient_id") or 0))
            except (TypeError, ValueError):
                continue
        for row in getattr(self, "staff_patient_mock_rows", []):
            try:
                max_patient_id = max(max_patient_id, int(row.get("patient_id") or 0))
            except (TypeError, ValueError):
                continue

        new_patient = {
            "patient_id": max_patient_id + 1,
            "name": payload["name"],
            "gender": payload["gender"],
            "dob": payload["dob"],
            "phone": payload["phone"],
            "cccd": payload["cccd"],
            "address": payload["address"],
            "occupation": payload["occupation"],
            "status": "Khám mới",
            "preferred_doctor": "BS. Minh",
            "blood_type": "O+",
            "allergies": "Không",
            "emergency_contact": "Nguyễn Thị Hồng (Vợ) - 0988 111 222",
            "note": "Hồ sơ mới được tạo tại màn hình nhân viên.",
        }
        self.staff_patient_rows.append(new_patient)
        if hasattr(self, "staff_patient_mock_rows"):
            self.staff_patient_mock_rows.append(dict(new_patient))

        self.staff_patient_current_page = self.staff_patient_total_pages
        self._filter_staff_patients()
        self._select_staff_patient_by_id(new_patient["patient_id"])
        self._set_staff_patient_info_hint(
            "Đã thêm bệnh nhân mới ở chế độ dữ liệu mẫu (mock mode), chưa ghi vào cơ sở dữ liệu thật."
        )

    @staticmethod
    def _build_staff_patient_mock_data():
        return [
            {
                "patient_id": 125,
                "name": "Nguyễn Văn Hùng",
                "gender": "Nam",
                "dob": "1990-02-15",
                "phone": "0987 654 321",
                "cccd": "123456789012",
                "address": "123 Đường Lê Lợi, P.1, Q.1, TP.HCM",
                "status": "Đang điều trị",
                "preferred_doctor": "BS. Minh",
                "blood_type": "O+",
                "allergies": "Không",
                "occupation": "Nhân viên văn phòng",
                "emergency_contact": "Nguyễn Thị Hồng (Vợ) - 0988 111 222",
                "note": "Bệnh nhân có tiền sử đau dạ dày. Cân nhắc nhắc nhở kiêng đồ cay nóng.",
            },
            {
                "patient_id": 126,
                "name": "Trần Thị Mai",
                "gender": "Nữ",
                "dob": "1988-10-03",
                "phone": "0909 112 233",
                "cccd": "223456789012",
                "address": "22 Nguyễn Đình Chiểu, Q.3, TP.HCM",
                "status": "Tái khám",
                "preferred_doctor": "BS. Lan",
                "blood_type": "A+",
                "allergies": "Dị ứng hải sản",
                "occupation": "Kế toán",
                "emergency_contact": "Trần Văn Khải (Chồng) - 0909 113 355",
                "note": "Tái khám sau 2 tuần điều trị viêm họng.",
            },
            {
                "patient_id": 127,
                "name": "Lê Minh Phúc",
                "gender": "Nam",
                "dob": "2017-06-28",
                "phone": "0933 444 555",
                "cccd": "",
                "address": "45 Trường Chinh, Tân Bình, TP.HCM",
                "status": "Khám mới",
                "preferred_doctor": "BS. Hường",
                "blood_type": "B+",
                "allergies": "Không",
                "occupation": "Học sinh",
                "emergency_contact": "Lê Thị Tuyết (Mẹ) - 0933 111 777",
                "note": "Bệnh nhân nhi lần đầu đến khám.",
            },
            {
                "patient_id": 128,
                "name": "Phạm Quốc Anh",
                "gender": "Nam",
                "dob": "1962-12-11",
                "phone": "0912 010 999",
                "cccd": "923456789012",
                "address": "18 Lý Chính Thắng, Q.3, TP.HCM",
                "status": "Đã hoàn tất",
                "preferred_doctor": "BS. Minh",
                "blood_type": "AB+",
                "allergies": "Không",
                "occupation": "Nghỉ hưu",
                "emergency_contact": "Phạm Thị Thu (Con gái) - 0912 818 818",
                "note": "Đã hoàn tất điều trị tăng huyết áp, hẹn tái khám sau 3 tháng.",
            },
            {
                "patient_id": 129,
                "name": "Đỗ Thu Hương",
                "gender": "Nữ",
                "dob": "1995-08-20",
                "phone": "0977 889 900",
                "cccd": "523456789012",
                "address": "7C Cách Mạng Tháng 8, Q.10, TP.HCM",
                "status": "Khám mới",
                "preferred_doctor": "BS. Lan",
                "blood_type": "O-",
                "allergies": "Penicillin",
                "occupation": "Thiết kế đồ họa",
                "emergency_contact": "Đỗ Văn Dũng (Anh) - 0977 112 345",
                "note": "Cần lưu ý dị ứng Penicillin.",
            },
            {
                "patient_id": 130,
                "name": "Ngô Đức Trọng",
                "gender": "Nam",
                "dob": "1982-03-09",
                "phone": "0965 120 120",
                "cccd": "623456789012",
                "address": "61 Hoàng Hoa Thám, Bình Thạnh, TP.HCM",
                "status": "Đang điều trị",
                "preferred_doctor": "BS. Hường",
                "blood_type": "B-",
                "allergies": "Không",
                "occupation": "Tài xế",
                "emergency_contact": "Ngô Thị Mỹ (Vợ) - 0965 555 666",
                "note": "Theo dõi đau lưng mạn tính, đang trong liệu trình vật lý trị liệu.",
            },
            {
                "patient_id": 131,
                "name": "Vũ Thị Mai",
                "gender": "Nữ",
                "dob": "1978-11-30",
                "phone": "0941 332 221",
                "cccd": "723456789012",
                "address": "88 Tô Hiến Thành, Q.10, TP.HCM",
                "status": "Tái khám",
                "preferred_doctor": "BS. Minh",
                "blood_type": "A-",
                "allergies": "Không",
                "occupation": "Giáo viên",
                "emergency_contact": "Vũ Quốc Bình (Con trai) - 0941 999 121",
                "note": "Tái khám sau điều trị dạ dày.",
            },
            {
                "patient_id": 132,
                "name": "Bùi Thanh Tùng",
                "gender": "Nam",
                "dob": "2003-01-14",
                "phone": "0899 101 202",
                "cccd": "823456789012",
                "address": "11A Nguyễn Trãi, Q.5, TP.HCM",
                "status": "Khám mới",
                "preferred_doctor": "BS. Lan",
                "blood_type": "O+",
                "allergies": "Không",
                "occupation": "Sinh viên",
                "emergency_contact": "Bùi Minh Châu (Mẹ) - 0899 202 303",
                "note": "Khám sức khỏe định kỳ.",
            },
            {
                "patient_id": 133,
                "name": "Hồ Ngọc Yến",
                "gender": "Nữ",
                "dob": "1992-05-02",
                "phone": "0918 450 450",
                "cccd": "923456789099",
                "address": "33 Nguyễn Hữu Cảnh, Bình Thạnh, TP.HCM",
                "status": "Đang điều trị",
                "preferred_doctor": "BS. Hường",
                "blood_type": "AB-",
                "allergies": "Không",
                "occupation": "Marketing",
                "emergency_contact": "Hồ Minh Đức (Chồng) - 0918 777 333",
                "note": "Theo dõi viêm xoang, đã kê thuốc uống 7 ngày.",
            },
            {
                "patient_id": 134,
                "name": "Trịnh Công Nam",
                "gender": "Nam",
                "dob": "1957-09-16",
                "phone": "0903 200 200",
                "cccd": "103456789012",
                "address": "5 Cộng Hòa, Tân Bình, TP.HCM",
                "status": "Đã hoàn tất",
                "preferred_doctor": "BS. Minh",
                "blood_type": "B+",
                "allergies": "Không",
                "occupation": "Nghỉ hưu",
                "emergency_contact": "Trịnh Minh Khoa (Con trai) - 0903 404 505",
                "note": "Đã hoàn tất điều trị và xuất viện.",
            },
        ]

    def _build_appointment_management_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: #f8fbff; border: none;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        shell_row = QtWidgets.QHBoxLayout()
        shell_row.setSpacing(12)

        left_sidebar = QtWidgets.QFrame()
        left_sidebar.setFixedWidth(200)
        left_sidebar.setStyleSheet("background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px;")
        left_layout = QtWidgets.QVBoxLayout(left_sidebar)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_layout.setSpacing(8)
        left_title = QtWidgets.QLabel("Danh mục lịch hẹn")
        left_title.setStyleSheet("font-size: 14px; font-weight: 800; color: #0f172a;")
        left_layout.addWidget(left_title)
        for label_text in ["Tất cả lịch hẹn", "Chờ xác nhận", "Đã xác nhận", "Đang khám", "Đã hoàn tất", "Đã hủy"]:
            item = QtWidgets.QPushButton(label_text)
            item.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            item.setStyleSheet(
                "QPushButton {text-align: left; padding: 8px 10px; background: white; border: 1px solid #e2e8f0; border-radius: 8px; color: #334155; font-size: 12px; font-weight: 600;}"
                "QPushButton:hover {border-color: #1A9B6C; color: #1A9B6C;}"
            )
            left_layout.addWidget(item)
        left_layout.addStretch()
        shell_row.addWidget(left_sidebar)

        center_right = QtWidgets.QHBoxLayout()
        center_right.setSpacing(12)

        center_panel = QtWidgets.QFrame()
        center_panel.setStyleSheet("background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;")
        center_layout = QtWidgets.QVBoxLayout(center_panel)
        center_layout.setContentsMargins(14, 14, 14, 14)
        center_layout.setSpacing(10)

        tabs_row = QtWidgets.QHBoxLayout()
        tabs_row.setSpacing(16)
        self.staff_appt_tab_today = QtWidgets.QPushButton("Lịch hẹn hôm nay")
        self.staff_appt_tab_tomorrow = QtWidgets.QPushButton("Lịch hẹn ngày mai")
        self.staff_appt_tab_by_date = QtWidgets.QPushButton("📅 Lịch hẹn theo ngày")
        for idx, btn in enumerate([self.staff_appt_tab_today, self.staff_appt_tab_tomorrow, self.staff_appt_tab_by_date]):
            btn.setCheckable(True)
            btn.setChecked(idx == 0)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(
                "QPushButton {background: transparent; border: none; padding: 4px 0 6px 0; color: #64748b; font-size: 13px; font-weight: 800;}"
                "QPushButton:checked {color: #1A9B6C; border-bottom: 2px solid #1A9B6C;}"
            )
            tabs_row.addWidget(btn)
        tabs_row.addStretch()
        center_layout.addLayout(tabs_row)

        toolbar_row = QtWidgets.QHBoxLayout()
        toolbar_row.setSpacing(8)
        self.staff_appt_search_input = QtWidgets.QLineEdit()
        self.staff_appt_search_input.setPlaceholderText("Tìm theo mã lịch hẹn, tên bệnh nhân, bác sĩ...")
        self.staff_appt_search_input.setStyleSheet(
            "QLineEdit {padding: 8px 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 12px;}"
            "QLineEdit:focus {border-color: #1A9B6C;}"
        )
        btn_create = QtWidgets.QPushButton("+ Tạo lịch hẹn")
        btn_create.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        btn_create.setStyleSheet(
            "QPushButton {background: #1A9B6C; color: white; border: none; padding: 8px 14px; border-radius: 8px; font-weight: 800; font-size: 12px;}"
            "QPushButton:hover {background: #168a60;}"
        )
        btn_create.clicked.connect(self._handle_staff_appointment_create)
        toolbar_row.addWidget(self.staff_appt_search_input, 1)
        toolbar_row.addWidget(btn_create)
        center_layout.addLayout(toolbar_row)

        filter_row = QtWidgets.QHBoxLayout()
        filter_row.setSpacing(8)
        self.staff_appt_doctor_combo = QtWidgets.QComboBox()
        self.staff_appt_doctor_combo.setMinimumWidth(150)
        self.staff_appt_doctor_combo.setStyleSheet("QComboBox {padding: 7px 8px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 12px;}")

        self.staff_appt_service_combo = QtWidgets.QComboBox()
        self.staff_appt_service_combo.setMinimumWidth(150)
        self.staff_appt_service_combo.setStyleSheet("QComboBox {padding: 7px 8px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 12px;}")

        self.staff_appt_status_combo = QtWidgets.QComboBox()
        self.staff_appt_status_combo.addItems(["pending", "confirmed", "in_progress", "done", "cancelled"])
        self.staff_appt_status_combo.setCurrentText("pending")
        self.staff_appt_status_combo.setMinimumWidth(130)
        self.staff_appt_status_combo.setStyleSheet("QComboBox {padding: 7px 8px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 12px;}")

        self.staff_appt_date_input = QtWidgets.QDateEdit()
        self.staff_appt_date_input.setCalendarPopup(True)
        self.staff_appt_date_input.setDisplayFormat("yyyy-MM-dd")
        self.staff_appt_date_input.setDate(QtCore.QDate.currentDate())
        self.staff_appt_date_input.setStyleSheet("QDateEdit {padding: 7px 8px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 12px;}")

        filter_row.addWidget(self.staff_appt_doctor_combo)
        filter_row.addWidget(self.staff_appt_service_combo)
        filter_row.addWidget(self.staff_appt_status_combo)
        filter_row.addWidget(self.staff_appt_date_input)
        filter_row.addStretch()
        center_layout.addLayout(filter_row)

        self.staff_appt_table = QtWidgets.QTableWidget()
        self.staff_appt_table.setColumnCount(6)
        self.staff_appt_table.setHorizontalHeaderLabels([
            "Giờ hẹn", "Bệnh nhân", "Dịch vụ", "Bác sĩ", "Trạng thái", "Thao tác"
        ])
        self.staff_appt_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.staff_appt_table.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.SingleSelection)
        self.staff_appt_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_appt_table.horizontalHeader().setStretchLastSection(True)
        self.staff_appt_table.verticalHeader().setVisible(False)
        self.staff_appt_table.itemSelectionChanged.connect(self._handle_staff_appointment_selection)
        center_layout.addWidget(self.staff_appt_table, 1)

        self.staff_appt_feedback = QtWidgets.QLabel("Sẵn sàng điều phối lịch hẹn.")
        self.staff_appt_feedback.setWordWrap(True)
        self.staff_appt_feedback.setStyleSheet("font-size: 12px; color: #475569;")
        center_layout.addWidget(self.staff_appt_feedback)

        right_panel = QtWidgets.QFrame()
        right_panel.setStyleSheet("background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px;")
        right_layout = QtWidgets.QVBoxLayout(right_panel)
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_layout.setSpacing(8)

        detail_title = QtWidgets.QLabel("Chi tiết lịch hẹn")
        detail_title.setStyleSheet("font-size: 14px; font-weight: 800; color: #0f172a;")
        right_layout.addWidget(detail_title)

        self.staff_appt_detail_placeholder = QtWidgets.QLabel("Chọn một lịch hẹn từ danh sách để xem thông tin chi tiết và thao tác cập nhật.")
        self.staff_appt_detail_placeholder.setWordWrap(True)
        self.staff_appt_detail_placeholder.setStyleSheet("font-size: 12px; color: #64748b; line-height: 1.4; padding: 8px; background: #ffffff; border: 1px dashed #cbd5e1; border-radius: 8px;")
        right_layout.addWidget(self.staff_appt_detail_placeholder)

        patient_card = QtWidgets.QFrame()
        patient_card.setStyleSheet("QFrame {background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px;}")
        patient_layout = QtWidgets.QVBoxLayout(patient_card)
        patient_layout.setContentsMargins(10, 10, 10, 10)
        patient_layout.setSpacing(4)
        patient_title = QtWidgets.QLabel("Bệnh nhân")
        patient_title.setStyleSheet("font-size: 12px; font-weight: 800; color: #0f172a;")
        patient_layout.addWidget(patient_title)
        self.staff_appt_patient_name_label = QtWidgets.QLabel("--")
        self.staff_appt_patient_name_label.setStyleSheet("font-size: 13px; font-weight: 800; color: #0f172a;")
        patient_layout.addWidget(self.staff_appt_patient_name_label)
        self.staff_appt_patient_meta_label = QtWidgets.QLabel("Giới tính/tuổi/SĐT: --")
        self.staff_appt_patient_meta_label.setWordWrap(True)
        self.staff_appt_patient_meta_label.setStyleSheet("font-size: 12px; color: #334155;")
        patient_layout.addWidget(self.staff_appt_patient_meta_label)
        self.staff_appt_patient_code_label = QtWidgets.QLabel("Mã bệnh nhân: --")
        self.staff_appt_patient_code_label.setStyleSheet("font-size: 12px; color: #475569;")
        patient_layout.addWidget(self.staff_appt_patient_code_label)
        right_layout.addWidget(patient_card)

        detail_grid_card = QtWidgets.QFrame()
        detail_grid_card.setStyleSheet("QFrame {background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px;}")
        detail_grid = QtWidgets.QGridLayout(detail_grid_card)
        detail_grid.setContentsMargins(10, 10, 10, 10)
        detail_grid.setHorizontalSpacing(8)
        detail_grid.setVerticalSpacing(6)
        detail_headers = [
            ("Thời gian", "staff_appt_detail_time_label"),
            ("Dịch vụ", "staff_appt_detail_service_label"),
            ("Bác sĩ", "staff_appt_detail_doctor_label"),
            ("Phòng", "staff_appt_detail_room_label"),
            ("Trạng thái", "staff_appt_detail_status_label"),
            ("Ghi chú", "staff_appt_detail_note_label"),
        ]
        for idx, (title, attr_name) in enumerate(detail_headers):
            title_lb = QtWidgets.QLabel(f"{title}:")
            title_lb.setStyleSheet("font-size: 12px; font-weight: 700; color: #334155;")
            value_lb = QtWidgets.QLabel("--")
            value_lb.setWordWrap(True)
            value_lb.setStyleSheet("font-size: 12px; color: #0f172a;")
            setattr(self, attr_name, value_lb)
            detail_grid.addWidget(title_lb, idx, 0)
            detail_grid.addWidget(value_lb, idx, 1)
        right_layout.addWidget(detail_grid_card)

        timeline_card = QtWidgets.QFrame()
        timeline_card.setStyleSheet("QFrame {background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px;}")
        timeline_layout = QtWidgets.QVBoxLayout(timeline_card)
        timeline_layout.setContentsMargins(10, 10, 10, 10)
        timeline_layout.setSpacing(4)
        timeline_title = QtWidgets.QLabel("Timeline")
        timeline_title.setStyleSheet("font-size: 12px; font-weight: 800; color: #0f172a;")
        timeline_layout.addWidget(timeline_title)
        self.staff_appt_timeline_labels = []
        for _ in range(3):
            lb = QtWidgets.QLabel("• Chưa có dữ liệu")
            lb.setWordWrap(True)
            lb.setStyleSheet("font-size: 12px; color: #475569;")
            timeline_layout.addWidget(lb)
            self.staff_appt_timeline_labels.append(lb)
        right_layout.addWidget(timeline_card)

        self.staff_appt_patient_id_input = QtWidgets.QLineEdit()
        self.staff_appt_patient_id_input.setPlaceholderText("Patient ID")
        self.staff_appt_time_input = QtWidgets.QTimeEdit()
        self.staff_appt_time_input.setDisplayFormat("HH:mm")
        self.staff_appt_time_input.setTime(QtCore.QTime.currentTime())
        self.staff_appt_note_input = QtWidgets.QLineEdit()
        self.staff_appt_note_input.setPlaceholderText("Ghi chú điều phối")

        hidden_form = QtWidgets.QFrame()
        hidden_form_layout = QtWidgets.QFormLayout(hidden_form)
        hidden_form_layout.setContentsMargins(0, 0, 0, 0)
        hidden_form_layout.addRow("Patient ID", self.staff_appt_patient_id_input)
        hidden_form_layout.addRow("Giờ", self.staff_appt_time_input)
        hidden_form_layout.addRow("Ghi chú", self.staff_appt_note_input)
        hidden_form.setVisible(False)
        right_layout.addWidget(hidden_form)

        right_layout.addStretch()

        action_block = QtWidgets.QHBoxLayout()
        self.staff_appt_btn_edit = QtWidgets.QPushButton("✏ Sửa lịch hẹn")
        self.staff_appt_btn_cancel = QtWidgets.QPushButton("🗑 Hủy lịch hẹn")
        self.staff_appt_btn_print = QtWidgets.QPushButton("🖨 In phiếu hẹn")
        for btn in [self.staff_appt_btn_edit, self.staff_appt_btn_cancel, self.staff_appt_btn_print]:
            btn.setEnabled(False)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(
                "QPushButton {padding: 7px 8px; border: 1px solid #cbd5e1; border-radius: 8px; background: #fff; font-size: 11px; font-weight: 700; color: #334155;}"
                "QPushButton:hover {border-color: #94a3b8;}"
                "QPushButton:disabled {background: #f1f5f9; color: #94a3b8; border-color: #e2e8f0;}"
            )
        self.staff_appt_btn_edit.clicked.connect(self._handle_staff_appointment_reschedule)
        self.staff_appt_btn_cancel.clicked.connect(self._handle_staff_appointment_cancel)
        self.staff_appt_btn_print.clicked.connect(self._handle_staff_appt_print)
        action_block.addWidget(self.staff_appt_btn_edit)
        action_block.addWidget(self.staff_appt_btn_cancel)
        action_block.addWidget(self.staff_appt_btn_print)
        right_layout.addLayout(action_block)

        center_right.addWidget(center_panel, 65)
        center_right.addWidget(right_panel, 35)

        center_right_holder = QtWidgets.QWidget()
        center_right_holder.setLayout(center_right)
        shell_row.addWidget(center_right_holder, 1)

        layout.addLayout(shell_row, 1)

        self._load_staff_appointment_dropdowns()
        self._refresh_staff_appointment_table()
        return page

    def _load_staff_appointment_dropdowns(self):
        self.staff_appt_doctor_combo.clear()
        self.staff_appt_service_combo.clear()
        if hasattr(self, "staff_appt_filter_doctor_combo"):
            self.staff_appt_filter_doctor_combo.clear()
            self.staff_appt_filter_doctor_combo.addItem("Chọn bác sĩ", None)
        if hasattr(self, "staff_appt_filter_service_combo"):
            self.staff_appt_filter_service_combo.clear()
            self.staff_appt_filter_service_combo.addItem("Chọn dịch vụ", "")

        doctors = DoctorController.get_all() or []
        services = ServiceController.get_all() or []

        if not doctors:
            self.staff_appt_doctor_combo.addItem("Chưa có bác sĩ", None)
        else:
            for d in doctors:
                doctor_id = d.get("doctor_id")
                label = f"#{doctor_id} - {d.get('name', '')}"
                self.staff_appt_doctor_combo.addItem(label, doctor_id)
                if hasattr(self, "staff_appt_filter_doctor_combo"):
                    self.staff_appt_filter_doctor_combo.addItem(str(d.get("name") or label), doctor_id)

        if not services:
            self.staff_appt_service_combo.addItem("Chưa có dịch vụ", "")
        else:
            for s in services:
                service_name = str(s.get("service_name") or s.get("name") or "").strip()
                if service_name:
                    self.staff_appt_service_combo.addItem(service_name, service_name)
                    if hasattr(self, "staff_appt_filter_service_combo"):
                        self.staff_appt_filter_service_combo.addItem(service_name, service_name)

    def _refresh_staff_appointment_table(self):
        role = self._get_current_user_role()
        user_context = self._build_appointment_user_context()
        rows = AppointmentController.get_all_for_role(role, user_context) or []
        if isinstance(rows, dict):
            self.staff_appointment_rows = []
            self.staff_appt_table.setRowCount(0)
            self._reset_staff_appointment_detail()
            self._set_staff_appt_feedback(rows.get("message") or "Không thể tải danh sách lịch hẹn.", is_error=True)
            return

        self.staff_appointment_rows = list(rows)
        visible_rows = self.staff_appointment_rows[:8]
        self.staff_appt_table.setRowCount(len(visible_rows))

        for row, a in enumerate(visible_rows):
            service_text = self._extract_service_name_from_note(str(a.get("note") or ""))
            self.staff_appt_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(a.get("appointment_date", ""))))
            self.staff_appt_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(a.get("patient_name", ""))))
            self.staff_appt_table.setItem(row, 2, QtWidgets.QTableWidgetItem(service_text))
            self.staff_appt_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(a.get("doctor_name", ""))))
            self.staff_appt_table.setCellWidget(row, 4, self._create_status_badge_widget(str(a.get("status") or "pending")))
            self.staff_appt_table.setCellWidget(row, 5, self._create_appointment_actions_widget(row))
        if visible_rows:
            self.staff_appt_table.selectRow(0)
        else:
            self._reset_staff_appointment_detail()

    def _get_current_user_role(self):
        role = str(self.user_data.get("role") or "staff").lower().strip()
        if role not in {"admin", "staff", "doctor", "patient"}:
            return "staff"
        return role

    def _build_appointment_user_context(self):
        return {
            "user_id": self.user_data.get("user_id"),
            "patient_id": self.user_data.get("patient_id"),
            "doctor_id": self.user_data.get("doctor_id"),
            "username": self.user_data.get("username") or self.user_data.get("name"),
        }

    def _get_status_badge_style(self, status):
        status_key = str(status or "pending").lower().strip()
        color_map = {
            "confirmed": ("#DCFCE7", "#16A34A"),
            "pending": ("#FEF3C7", "#D97706"),
            "in_progress": ("#DBEAFE", "#2563EB"),
            "done": ("#EDE9FE", "#7C3AED"),
            "cancelled": ("#FEE2E2", "#DC2626"),
        }
        return color_map.get(status_key, color_map["pending"])

    def _create_status_badge_widget(self, status):
        bg_color, fg_color = self._get_status_badge_style(status)
        text = str(status or "pending").lower().strip()
        badge = QtWidgets.QLabel(text)
        badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            f"background: {bg_color}; color: {fg_color}; border: none; border-radius: 10px; padding: 4px 10px; font-size: 11px; font-weight: 700;"
        )
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.addWidget(badge)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        return wrapper

    def _create_appointment_actions_widget(self, row):
        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(2, 0, 2, 0)
        layout.setSpacing(6)

        view_btn = QtWidgets.QPushButton("👁️")
        view_btn.setToolTip("Xem chi tiết")
        view_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        view_btn.setFixedSize(28, 24)
        view_btn.setStyleSheet("QPushButton {border: 1px solid #cbd5e1; border-radius: 6px; background: #ffffff;} QPushButton:hover {border-color: #1A9B6C;}")
        view_btn.clicked.connect(lambda _, r=row: self._handle_staff_appt_quick_view(r))

        menu_btn = QtWidgets.QPushButton("⋮")
        menu_btn.setToolTip("Tùy chọn")
        menu_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        menu_btn.setFixedSize(28, 24)
        menu_btn.setStyleSheet("QPushButton {border: 1px solid #cbd5e1; border-radius: 6px; background: #ffffff;} QPushButton:hover {border-color: #1A9B6C;}")
        menu_btn.clicked.connect(lambda _, r=row, b=menu_btn: self._show_staff_appt_actions_menu(r, b))

        layout.addWidget(view_btn)
        layout.addWidget(menu_btn)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        return container

    def _get_allowed_appointment_actions(self, appt):
        role = self._get_current_user_role()
        status = str(appt.get("status") or "").lower().strip()
        if role in {"admin", "staff"}:
            return ["view", "edit", "reschedule", "reassign", "cancel", "print"]
        if role == "doctor":
            return ["view", "start", "complete"]
        if role == "patient":
            actions = ["view"]
            if status not in {"in_progress", "done"}:
                actions.append("cancel")
            return actions
        return ["view"]

    def _handle_staff_appt_quick_view(self, row):
        if row < 0 or row >= len(self.staff_appointment_rows):
            return
        self.staff_appt_table.selectRow(row)
        self._handle_staff_appointment_selection()

    def _show_staff_appt_actions_menu(self, row, button):
        if row < 0 or row >= len(self.staff_appointment_rows):
            return
        appt = self.staff_appointment_rows[row]
        menu = QtWidgets.QMenu(self)
        label_map = {
            "view": "Xem",
            "edit": "Chỉnh sửa",
            "reschedule": "Dời lịch",
            "reassign": "Đổi bác sĩ",
            "cancel": "Hủy lịch",
            "print": "In phiếu",
            "start": "Bắt đầu khám",
            "complete": "Hoàn tất",
        }
        for action_key in self._get_allowed_appointment_actions(appt):
            action = menu.addAction(label_map.get(action_key, action_key))
            action.triggered.connect(lambda _=False, k=action_key, r=row: self._handle_staff_appt_menu_action(k, r))
        menu.exec(button.mapToGlobal(QtCore.QPoint(0, button.height())))

    def _handle_staff_appt_menu_action(self, action_key, row):
        if row < 0 or row >= len(self.staff_appointment_rows):
            return
        appt = self.staff_appointment_rows[row]
        self.staff_appointment_selected_id = appt.get("appointment_id")
        self.shared_selected_appointment_id = self.staff_appointment_selected_id
        if action_key == "view":
            self._handle_staff_appt_quick_view(row)
            return
        if action_key in {"edit", "reschedule", "reassign"}:
            self._handle_staff_appt_quick_view(row)
            self._set_staff_appt_feedback("Đã nạp lịch hẹn vào panel chi tiết. Vui lòng cập nhật thông tin và bấm Dời/Cập nhật.", is_error=False)
            return
        if action_key == "cancel":
            self._handle_staff_appt_quick_view(row)
            self._handle_staff_appt_cancel()
            return
        if action_key == "print":
            self._set_staff_appt_feedback(f"Đã ghi nhận yêu cầu in phiếu cho lịch hẹn #{self.staff_appointment_selected_id}.", is_error=False)
            return
        if action_key in {"start", "complete"}:
            target_status = "in_progress" if action_key == "start" else "done"
            role = self._get_current_user_role()
            user_context = self._build_appointment_user_context()
            result = AppointmentController.update_status(
                self.staff_appointment_selected_id,
                target_status,
                role=role,
                user_context=user_context,
            )
            if isinstance(result, dict):
                ok = bool(result.get("status"))
                message = result.get("message") or "Cập nhật trạng thái thất bại."
            else:
                ok = bool(result)
                message = "Cập nhật trạng thái thất bại."
            if not ok:
                self._set_staff_appt_feedback(message, is_error=True)
                return
            self._refresh_staff_appointment_table()
            self._set_staff_appt_feedback(f"Đã cập nhật trạng thái lịch hẹn #{self.staff_appointment_selected_id} -> {target_status}.", is_error=False)
            return
        self._set_staff_appt_feedback("Tác vụ chưa được hỗ trợ ở phiên bản hiện tại.", is_error=True)

    def _handle_staff_appt_print(self):
        if not self.staff_appointment_selected_id:
            self._set_staff_appt_feedback("Vui lòng chọn lịch hẹn để in phiếu.", is_error=True)
            return
        self._set_staff_appt_feedback(
            f"Đã ghi nhận yêu cầu in phiếu cho lịch hẹn #{self.staff_appointment_selected_id}.",
            is_error=False,
        )

    def _update_staff_appt_right_panel(self, appt):
        if not appt:
            self.staff_appt_detail_placeholder.setText("Chọn một lịch hẹn từ danh sách để xem thông tin chi tiết và thao tác cập nhật.")
            self.staff_appt_patient_name_label.setText("--")
            self.staff_appt_patient_meta_label.setText("Giới tính/tuổi/SĐT: --")
            self.staff_appt_patient_code_label.setText("Mã bệnh nhân: --")
            self.staff_appt_detail_time_label.setText("--")
            self.staff_appt_detail_service_label.setText("--")
            self.staff_appt_detail_doctor_label.setText("--")
            self.staff_appt_detail_room_label.setText("--")
            self.staff_appt_detail_status_label.setText("--")
            self.staff_appt_detail_note_label.setText("--")
            for lb in self.staff_appt_timeline_labels:
                lb.setText("• Chưa có dữ liệu")
            self.staff_appt_btn_edit.setEnabled(False)
            self.staff_appt_btn_cancel.setEnabled(False)
            self.staff_appt_btn_print.setEnabled(False)
            return

        patient_name = str(appt.get("patient_name") or "Không rõ bệnh nhân")
        gender = str(appt.get("gender") or "--")
        age = str(appt.get("age") or "--")
        phone = str(appt.get("phone") or appt.get("patient_phone") or "--")
        patient_code = str(appt.get("patient_id") or appt.get("code") or "--")
        date_val = str(appt.get("appointment_date") or "")
        time_val = str(appt.get("appointment_time") or "")
        service_name = str(appt.get("service_name") or "--")
        doctor_name = str(appt.get("doctor_name") or "--")
        room = str(appt.get("room") or appt.get("room_name") or "Chưa phân phòng")
        status = str(appt.get("status") or "pending")
        note = str(appt.get("reason") or appt.get("note") or "Không có ghi chú")

        self.staff_appt_detail_placeholder.setText(f"Đang xem lịch hẹn #{appt.get('appointment_id')}")
        self.staff_appt_patient_name_label.setText(patient_name)
        self.staff_appt_patient_meta_label.setText(f"Giới tính/tuổi/SĐT: {gender} / {age} / {phone}")
        self.staff_appt_patient_code_label.setText(f"Mã bệnh nhân: {patient_code}")
        self.staff_appt_detail_time_label.setText(f"{date_val} {time_val}".strip() or "--")
        self.staff_appt_detail_service_label.setText(service_name)
        self.staff_appt_detail_doctor_label.setText(doctor_name)
        self.staff_appt_detail_room_label.setText(room)
        self.staff_appt_detail_status_label.setText(status)
        self.staff_appt_detail_note_label.setText(note)

        timeline_entries = [
            f"• {time_val or '--'} | Tiếp nhận lịch hẹn ({date_val or 'chưa rõ ngày'})",
            f"• {time_val or '--'} | Trạng thái hiện tại: {status}",
            f"• {time_val or '--'} | BS {doctor_name} - {service_name}",
        ]
        for idx, lb in enumerate(self.staff_appt_timeline_labels):
            lb.setText(timeline_entries[idx] if idx < len(timeline_entries) else "• Chưa có dữ liệu")

        allowed = set(self._get_allowed_appointment_actions(appt))
        self.staff_appt_btn_edit.setEnabled(any(act in allowed for act in {"edit", "reschedule", "reassign"}))
        self.staff_appt_btn_cancel.setEnabled("cancel" in allowed)
        self.staff_appt_btn_print.setEnabled("print" in allowed)

    def _handle_staff_appointment_selection(self):
        selected = self.staff_appt_table.selectedItems()
        if not selected:
            self.staff_appointment_selected_id = None
            self.shared_selected_appointment_id = None
            self._update_staff_appt_right_panel(None)
            return

        row = selected[0].row()
        if row < 0 or row >= len(self.staff_appointment_rows):
            self.staff_appointment_selected_id = None
            self.shared_selected_appointment_id = None
            self._update_staff_appt_right_panel(None)
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
        self._update_staff_appt_right_panel(appt)
        self._set_staff_appt_feedback(
            f"Đã chọn lịch hẹn #{self.staff_appointment_selected_id} để cập nhật/hủy.",
            is_error=False,
        )
        self._set_staff_appointment_detail(appt)

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

    def _toggle_staff_appointment_form(self):
        is_visible = self.staff_appt_form_card.isVisible()
        self.staff_appt_form_card.setVisible(not is_visible)
        if not is_visible:
            self._reset_staff_appointment_form()

    def _show_staff_appointment_form_for_selected(self):
        if not self.staff_appointment_selected_id:
            self._set_staff_appt_feedback("Vui lòng chọn một lịch hẹn trước khi sửa.", is_error=True)
            return
        self.staff_appt_form_card.setVisible(True)

    def _reset_staff_appointment_detail(self):
        if not hasattr(self, "staff_appt_detail_patient"):
            return
        self.staff_appt_detail_patient.setText("Chưa chọn lịch hẹn")
        self.staff_appt_detail_info.setText("Chọn một lịch hẹn ở bảng bên trái để xem chi tiết.")
        self.staff_appt_detail_timeline.setText("Lịch sử cập nhật sẽ hiển thị tại đây.")

    def _set_staff_appointment_detail(self, appt):
        if not hasattr(self, "staff_appt_detail_patient"):
            self._update_staff_appt_right_panel(appt)
            return

        service_text = self._extract_service_name_from_note(str(appt.get("note") or "")) or "-"
        status = str(appt.get("status") or "")
        patient_name = str(appt.get("patient_name") or "Chưa có tên")
        appointment_date = str(appt.get("appointment_date") or "")
        self.staff_appt_detail_patient.setText(
            f"👤  {patient_name}\n"
            f"BN #{appt.get('patient_id', '')}  •  {appt.get('patient_phone', 'Chưa có SĐT')}"
        )
        self.staff_appt_detail_info.setText(
            f"Thời gian hẹn: {appointment_date}\n"
            f"Dịch vụ khám: {service_text}\n"
            f"Bác sĩ: {appt.get('doctor_name', '')}\n"
            f"Phòng khám: Phòng khám 1\n"
            f"Trạng thái: {self._staff_status_label(status)}\n"
            f"Ghi chú: {appt.get('note') or 'Không có'}"
        )
        date_part = appointment_date[:10] if appointment_date else "Hôm nay"
        self.staff_appt_detail_timeline.setText(
            f"● {date_part} 07:30\n  Nhân viên tạo lịch hẹn\n\n"
            f"● {date_part} 07:35\n  Bệnh nhân xác nhận lịch hẹn\n\n"
            f"● {date_part} 07:40\n  Nhân viên xác nhận lịch hẹn"
        )

    @staticmethod
    def _staff_status_label(status):
        labels = {
            "pending": "Đang chờ",
            "confirmed": "Đã xác nhận",
            "in_progress": "Đang khám",
            "done": "Đã hoàn tất",
            "cancelled": "Đã hủy",
        }
        return labels.get(status, status or "-")

    def _build_staff_appointment_status_badge(self, status):
        styles = {
            "pending": ("#fff0df", "#f97316"),
            "confirmed": ("#dcfce7", "#13a66b"),
            "in_progress": ("#e4f0ff", "#2563eb"),
            "done": ("#eee9ff", "#8b5cf6"),
            "cancelled": ("#fee2e2", "#ef4444"),
        }
        bg, fg = styles.get(status, ("#eef2f7", "#334155"))
        label = QtWidgets.QLabel(self._staff_status_label(status))
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"background: {bg}; color: {fg}; border-radius: 10px; padding: 4px 10px; font-size: 11px; font-weight: 900;")
        return label

    def _build_staff_appointment_row_actions(self):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        view_btn = QtWidgets.QPushButton("👁")
        more_btn = QtWidgets.QPushButton("⋮")
        for btn in [view_btn, more_btn]:
            btn.setFixedSize(34, 30)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet("background: #eff6ff; color: #2563eb; border: none; border-radius: 8px; font-weight: 900;")
        view_btn.clicked.connect(self._handle_staff_appointment_selection)
        more_btn.clicked.connect(self._show_staff_appointment_form_for_selected)
        layout.addWidget(view_btn)
        layout.addWidget(more_btn)
        return wrapper

    def _build_staff_status_legend_item(self, title, color, note):
        item = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(item)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        title_row = QtWidgets.QHBoxLayout()
        title_row.setSpacing(6)
        dot = QtWidgets.QLabel()
        dot.setFixedSize(10, 10)
        dot.setStyleSheet(f"background: {color}; border-radius: 5px;")
        title_lbl = QtWidgets.QLabel(title)
        title_lbl.setStyleSheet("border: none; background: transparent; font-size: 12px; color: #0f172a; font-weight: 900;")
        note_lbl = QtWidgets.QLabel(note)
        note_lbl.setWordWrap(True)
        note_lbl.setStyleSheet("border: none; background: transparent; font-size: 11px; color: #64748b; font-weight: 700;")
        title_row.addWidget(dot)
        title_row.addWidget(title_lbl)
        title_row.addStretch()
        layout.addLayout(title_row)
        layout.addWidget(note_lbl)
        return item

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
        card.setObjectName("sectionCard")
        card.setStyleSheet(
            "QFrame#sectionCard { background: #ffffff; border: 1px solid #e4ebf4; border-radius: 14px; }"
        )
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(10)

        if title:
            title_lbl = QtWidgets.QLabel(title)
            title_lbl.setStyleSheet("border: none; background: transparent; font-size: 17px; font-weight: 900; color: #0f172a;")
            card_layout.addWidget(title_lbl)
        return card

    def _build_kpi_card(self, title, value, note, accent, icon_bg="#f1f5f9", icon_text=""):
        card = QtWidgets.QFrame()
        card.setMinimumHeight(118)
        card.setStyleSheet(
            "QFrame { background: #ffffff; border: 1px solid #e4ebf4; border-radius: 14px; }"
        )
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(14)

        text_col = QtWidgets.QVBoxLayout()
        text_col.setSpacing(3)

        title_lbl = QtWidgets.QLabel(title)
        title_lbl.setWordWrap(True)
        title_lbl.setStyleSheet("font-size: 12px; color: #0f172a; font-weight: 900;")

        value_lbl = QtWidgets.QLabel(value)
        value_lbl.setStyleSheet(f"font-size: 32px; color: {accent}; font-weight: 900;")

        note_lbl = QtWidgets.QLabel(note)
        note_lbl.setWordWrap(True)
        note_lbl.setStyleSheet("font-size: 11px; color: #64748b; font-weight: 700;")

        text_col.addWidget(title_lbl)
        text_col.addWidget(value_lbl)
        text_col.addWidget(note_lbl)
        if icon_text:
            icon = QtWidgets.QLabel(icon_text)
            icon.setFixedSize(64, 64)
            icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            icon.setStyleSheet(f"background: {icon_bg}; color: {accent}; border-radius: 12px; font-size: 27px; font-weight: 900;")
            layout.addWidget(icon)
        layout.addLayout(text_col, 1)
        return card

    def _build_quick_action_button(self, title, icon, target_index, bg_color, accent):
        btn = QtWidgets.QPushButton(f"{icon}\n{title}")
        btn.setMinimumSize(96, 126)
        btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        btn.setStyleSheet(
            "QPushButton {"
            f"background: {bg_color}; border: none; border-radius: 14px;"
            f"color: #0f172a; font-size: 13px; font-weight: 900; padding: 12px;"
            "}"
            f"QPushButton:hover {{ color: {accent}; }}"
        )
        btn.clicked.connect(lambda checked, idx=target_index: self.switch_page(idx))
        return btn

    def _build_status_badge(self, status):
        styles = {
            "Đã xác nhận": ("#e3f7ec", "#13995f"),
            "Đang chờ": ("#fff0df", "#f97316"),
            "Đang khám": ("#e4f0ff", "#2563eb"),
            "Đã hoàn tất": ("#eee9ff", "#6d48d8"),
        }
        bg, fg = styles.get(status, ("#eef2f7", "#334155"))
        label = QtWidgets.QLabel(status)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"background: {bg}; color: {fg}; border-radius: 10px; padding: 4px 10px; font-size: 11px; font-weight: 900;")
        return label

    def _build_table_actions(self):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        for label, bg in [("👁", "#f0efff"), ("✎", "#eaf5ff")]:
            btn = QtWidgets.QPushButton(label)
            btn.setFixedSize(32, 28)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(f"background: {bg}; color: #2563eb; border: none; border-radius: 8px; font-weight: 900;")
            btn.clicked.connect(lambda checked: self.switch_page(2))
            layout.addWidget(btn)
        return wrapper

    def _build_patient_waiting_row(self, name, detail, time_text):
        row = QtWidgets.QFrame()
        row.setStyleSheet("border-bottom: 1px solid #edf2f7;")
        layout = QtWidgets.QHBoxLayout(row)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(10)

        avatar = QtWidgets.QLabel("👤")
        avatar.setFixedSize(34, 34)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("background: #eaf2ff; border-radius: 17px; font-size: 17px;")

        text_col = QtWidgets.QVBoxLayout()
        text_col.setSpacing(2)
        name_lbl = QtWidgets.QLabel(name)
        name_lbl.setStyleSheet("font-size: 13px; color: #0f172a; font-weight: 900;")
        detail_lbl = QtWidgets.QLabel(detail)
        detail_lbl.setStyleSheet("font-size: 12px; color: #334155; font-weight: 700;")
        text_col.addWidget(name_lbl)
        text_col.addWidget(detail_lbl)

        time_lbl = QtWidgets.QLabel(time_text)
        time_lbl.setStyleSheet("font-size: 12px; color: #475569; font-weight: 800;")
        arrow = QtWidgets.QLabel("›")
        arrow.setStyleSheet("font-size: 22px; color: #64748b; font-weight: 900;")

        layout.addWidget(avatar)
        layout.addLayout(text_col, 1)
        layout.addWidget(time_lbl)
        layout.addWidget(arrow)
        return row

    def _build_notice_row(self, icon_text, content, when, color):
        row = QtWidgets.QFrame()
        row.setStyleSheet("border-bottom: 1px solid #edf2f7;")
        layout = QtWidgets.QHBoxLayout(row)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(10)

        icon = QtWidgets.QLabel(icon_text)
        icon.setFixedSize(26, 26)
        icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet(f"background: #f8fafc; color: {color}; border-radius: 7px; font-size: 14px;")

        content_lbl = QtWidgets.QLabel(content)
        content_lbl.setWordWrap(True)
        content_lbl.setStyleSheet("font-size: 12px; color: #0f172a; font-weight: 700;")
        when_lbl = QtWidgets.QLabel(when)
        when_lbl.setStyleSheet("font-size: 11px; color: #64748b; font-weight: 700;")

        layout.addWidget(icon)
        layout.addWidget(content_lbl, 1)
        layout.addWidget(when_lbl)
        return row

    def _build_staff_billing_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: #f8fbff; border: none;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        header = QtWidgets.QHBoxLayout()
        title_col = QtWidgets.QVBoxLayout()
        heading = QtWidgets.QLabel("Thanh toán & Hóa đơn")
        heading.setStyleSheet("border: none; background: transparent; font-size: 25px; color: #0f172a; font-weight: 900;")
        breadcrumb = QtWidgets.QLabel("Trang chủ  ›  Thanh toán & Hóa đơn")
        breadcrumb.setStyleSheet("border: none; background: transparent; font-size: 14px; color: #64748b; font-weight: 700;")
        title_col.addWidget(heading)
        title_col.addWidget(breadcrumb)
        header.addLayout(title_col, 1)
        for text, style in [("🔔", "font-size: 21px;"), ("👤", "background: #eaf2ff; border-radius: 21px; font-size: 20px;")]:
            lbl = QtWidgets.QLabel(text)
            lbl.setFixedSize(42, 42)
            lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("border: none; " + style)
            header.addWidget(lbl)
        user_lbl = QtWidgets.QLabel(f"{self.username}  ▾")
        user_lbl.setStyleSheet("border: none; background: transparent; color: #0f172a; font-weight: 900;")
        header.addWidget(user_lbl)
        layout.addLayout(header)

        self.staff_billing_rows = self._build_staff_billing_catalog()
        pending = [b for b in self.staff_billing_rows if self._staff_bill_status_key(b) == "unpaid"]
        paid = [b for b in self.staff_billing_rows if self._staff_bill_status_key(b) == "paid"]
        refunded = [b for b in self.staff_billing_rows if self._staff_bill_status_key(b) == "refunded"]
        paid_total = sum(float(b.get("total_amount") or 0) for b in paid)
        kpi_row = QtWidgets.QHBoxLayout()
        kpi_row.setSpacing(16)
        kpi_row.addWidget(self._staff_bill_kpi("🧾", "Hóa đơn chờ thanh toán", len(pending), f"Tổng tiền: {self._format_staff_money(sum(float(b.get('total_amount') or 0) for b in pending))}", "#fff3e4", "#f97316"))
        kpi_row.addWidget(self._staff_bill_kpi("💵", "Đã thanh toán hôm nay", len(paid), f"Tổng tiền: {self._format_staff_money(paid_total)}", "#e8f8ef", "#13a66b"))
        kpi_row.addWidget(self._staff_bill_kpi("↩", "Hoàn tiền hôm nay", len(refunded), f"Tổng tiền: {self._format_staff_money(sum(float(b.get('total_amount') or 0) for b in refunded))}", "#eaf2ff", "#2563eb"))
        kpi_row.addWidget(self._staff_bill_kpi("♦", "Doanh thu hôm nay", self._format_staff_money(paid_total), f"{len(paid)} hóa đơn", "#f0eaff", "#6d5dfc"), 2)
        layout.addLayout(kpi_row)

        body = QtWidgets.QHBoxLayout()
        body.setSpacing(18)
        left = self._build_section_card("")
        left_layout = left.layout()
        tabs = QtWidgets.QHBoxLayout()
        self.staff_bill_active_tab = "all"
        self.staff_bill_status_tabs = {}
        for key, text in [("all", "Tất cả"), ("unpaid", f"Chờ thanh toán  {len(pending)}"), ("paid", "Đã thanh toán"), ("cancelled", "Đã hủy"), ("refunded", "Hoàn tiền")]:
            btn = QtWidgets.QPushButton(text)
            btn.setCheckable(True)
            btn.setChecked(key == "all")
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(
                "QPushButton { background: #ffffff; border: 1px solid transparent; border-radius: 9px; padding: 9px 13px; color: #64748b; font-size: 13px; font-weight: 900; }"
                "QPushButton:checked { background: #ecfdf5; color: #13a66b; border-color: #d1fae5; }"
            )
            btn.clicked.connect(lambda _, k=key: self._set_staff_bill_tab(k))
            self.staff_bill_status_tabs[key] = btn
            tabs.addWidget(btn)
        tabs.addStretch()
        left_layout.addLayout(tabs)

        filters = QtWidgets.QHBoxLayout()
        filters.setSpacing(10)
        self.staff_bill_search_input = QtWidgets.QLineEdit()
        self.staff_bill_search_input.setPlaceholderText("Tìm kiếm bệnh nhân, mã hóa đơn...")
        self.staff_bill_search_input.setStyleSheet(self._intake_input_style())
        self.staff_bill_from_date = QtWidgets.QDateEdit(QtCore.QDate.currentDate().addDays(-7))
        self.staff_bill_to_date = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        for date_input in [self.staff_bill_from_date, self.staff_bill_to_date]:
            date_input.setCalendarPopup(True)
            date_input.setDisplayFormat("dd/MM/yyyy")
            date_input.setStyleSheet(self._intake_input_style())
            date_input.dateChanged.connect(self._refresh_staff_billing_table)
        self.staff_bill_search_input.textChanged.connect(self._refresh_staff_billing_table)
        filter_btn = QtWidgets.QPushButton("⚗  Bộ lọc")
        filter_btn.setStyleSheet(self._intake_secondary_button_style())
        filter_btn.clicked.connect(self._refresh_staff_billing_table)
        filters.addWidget(self.staff_bill_search_input, 2)
        filters.addWidget(self.staff_bill_from_date)
        filters.addWidget(QtWidgets.QLabel("~"))
        filters.addWidget(self.staff_bill_to_date)
        filters.addWidget(filter_btn)
        left_layout.addLayout(filters)

        self.staff_bill_patient_id_input = QtWidgets.QLineEdit()
        self.staff_bill_appointment_id_input = QtWidgets.QLineEdit()
        self.staff_bill_amount_input = QtWidgets.QLineEdit()
        for hidden_input in [self.staff_bill_patient_id_input, self.staff_bill_appointment_id_input, self.staff_bill_amount_input]:
            hidden_input.setVisible(False)

        self.staff_bill_list_title = QtWidgets.QLabel("Danh sách hóa đơn (0)")
        self.staff_bill_list_title.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 16px; font-weight: 900;")
        left_layout.addWidget(self.staff_bill_list_title)
        self.staff_bill_table = QtWidgets.QTableWidget(0, 6)
        self.staff_bill_table.setHorizontalHeaderLabels(["Mã hóa đơn", "Bệnh nhân", "Ngày tạo", "Tổng tiền", "Trạng thái", "Thao tác"])
        self.staff_bill_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.staff_bill_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.staff_bill_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_bill_table.setShowGrid(False)
        self.staff_bill_table.verticalHeader().setVisible(False)
        self.staff_bill_table.verticalHeader().setDefaultSectionSize(58)
        self.staff_bill_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staff_bill_table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_bill_table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_bill_table.setStyleSheet(
            "QTableWidget { border: 1px solid #e7edf5; border-radius: 12px; background: #ffffff; color: #0f172a; font-size: 13px; font-weight: 700; }"
            "QHeaderView::section { background: #f8fafc; color: #1f2937; font-size: 12px; font-weight: 900; border: none; padding: 10px; }"
            "QTableWidget::item { border-bottom: 1px solid #edf2f7; padding: 8px; }"
            "QTableWidget::item:selected { background: #ecfdf5; color: #0f172a; }"
        )
        self.staff_bill_table.itemSelectionChanged.connect(self._on_staff_billing_row_selected)
        left_layout.addWidget(self.staff_bill_table, 1)
        self.staff_bill_footer_label = QtWidgets.QLabel("Hiển thị 0 bản ghi")
        self.staff_bill_footer_label.setStyleSheet("border: none; background: transparent; color: #64748b; font-size: 12px; font-weight: 700;")
        left_layout.addWidget(self.staff_bill_footer_label)

        right = self._build_section_card("Thông tin hóa đơn")
        right_layout = right.layout()
        print_row = QtWidgets.QHBoxLayout()
        print_row.addStretch()
        print_btn = QtWidgets.QPushButton("🖨  In hóa đơn")
        print_btn.clicked.connect(self._handle_staff_print_receipt)
        print_btn.setStyleSheet("background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; border-radius: 8px; padding: 7px 12px; font-weight: 900;")
        print_row.addWidget(print_btn)
        right_layout.addLayout(print_row)
        self.staff_bill_detail_header = QtWidgets.QLabel("Chưa chọn hóa đơn")
        self.staff_bill_detail_header.setWordWrap(True)
        self.staff_bill_detail_header.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 13px; font-weight: 800;")
        self.staff_bill_patient_card = QtWidgets.QLabel("Chọn hóa đơn ở bảng bên trái để xem chi tiết.")
        self.staff_bill_patient_card.setWordWrap(True)
        self.staff_bill_patient_card.setStyleSheet("background: #f8fafc; border: 1px solid #e7edf5; border-radius: 10px; padding: 12px; color: #334155; font-weight: 800;")
        right_layout.addWidget(self.staff_bill_detail_header)
        right_layout.addWidget(self.staff_bill_patient_card)
        title = QtWidgets.QLabel("Chi tiết dịch vụ")
        title.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 15px; font-weight: 900;")
        right_layout.addWidget(title)
        self.staff_bill_service_table = QtWidgets.QTableWidget(0, 4)
        self.staff_bill_service_table.setHorizontalHeaderLabels(["Dịch vụ", "SL", "Đơn giá", "Thành tiền"])
        self.staff_bill_service_table.verticalHeader().setVisible(False)
        self.staff_bill_service_table.setShowGrid(False)
        self.staff_bill_service_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_bill_service_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staff_bill_service_table.setFixedHeight(155)
        self.staff_bill_service_table.setStyleSheet("QTableWidget { border: none; background: #ffffff; font-size: 12px; } QHeaderView::section { border: none; background: #ffffff; color: #64748b; font-weight: 800; } QTableWidget::item { border-bottom: 1px solid #edf2f7; padding: 6px; }")
        right_layout.addWidget(self.staff_bill_service_table)
        self.staff_bill_total_label = QtWidgets.QLabel("Tổng cần thanh toán: --")
        self.staff_bill_total_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.staff_bill_total_label.setStyleSheet("border: none; background: transparent; color: #f97316; font-size: 18px; font-weight: 900;")
        right_layout.addWidget(self.staff_bill_total_label)
        pay_title = QtWidgets.QLabel("Thanh toán")
        pay_title.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 15px; font-weight: 900;")
        right_layout.addWidget(pay_title)
        method_row = QtWidgets.QHBoxLayout()
        self.staff_bill_method_buttons = []
        for idx, text in enumerate(["✓  Tiền mặt", "💳  Thẻ ATM/Visa", "🏦  Chuyển khoản"]):
            btn = QtWidgets.QPushButton(text)
            btn.setCheckable(True)
            btn.setChecked(idx == 0)
            btn.setStyleSheet("QPushButton { background: #ffffff; color: #475569; border: 1px solid #dbe4ee; border-radius: 8px; padding: 10px; font-size: 12px; font-weight: 900; } QPushButton:checked { background: #13a66b; color: #ffffff; border-color: #13a66b; }")
            btn.clicked.connect(lambda _, b=btn: self._set_staff_bill_payment_method(b))
            self.staff_bill_method_buttons.append(btn)
            method_row.addWidget(btn)
        right_layout.addLayout(method_row)
        right_layout.addWidget(QtWidgets.QLabel("Số tiền nhận"))
        self.staff_bill_received_input = QtWidgets.QLineEdit()
        self.staff_bill_received_input.setStyleSheet(self._intake_input_style())
        self.staff_bill_received_input.textChanged.connect(self._update_staff_bill_change)
        right_layout.addWidget(self.staff_bill_received_input)
        self.staff_bill_change_label = QtWidgets.QLabel("Tiền thừa: 0 đ")
        self.staff_bill_change_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.staff_bill_change_label.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 13px; font-weight: 900;")
        right_layout.addWidget(self.staff_bill_change_label)
        self.staff_bill_confirm_btn = QtWidgets.QPushButton("✓  Xác nhận thanh toán")
        self.staff_bill_confirm_btn.setStyleSheet(self._intake_primary_button_style())
        self.staff_bill_confirm_btn.clicked.connect(self._handle_staff_confirm_payment)
        right_layout.addWidget(self.staff_bill_confirm_btn)
        self.staff_bill_feedback = QtWidgets.QLabel("")
        self.staff_bill_feedback.setWordWrap(True)
        self.staff_bill_feedback.setStyleSheet("border: none; background: transparent; font-size: 12px; color: #166534; font-weight: 700;")
        right_layout.addWidget(self.staff_bill_feedback)
        right_layout.addStretch()

        body.addWidget(left, 7)
        body.addWidget(right, 3)
        layout.addLayout(body, 1)
        self._refresh_staff_billing_table()
        return page

    def _staff_bill_kpi(self, icon, title, value, note, bg_color, fg_color):
        card = QtWidgets.QFrame()
        card.setMinimumHeight(96)
        card.setStyleSheet("background: #ffffff; border: 1px solid #e7edf5; border-radius: 14px;")
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        icon_lbl = QtWidgets.QLabel(str(icon))
        icon_lbl.setFixedSize(44, 44)
        icon_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet(f"background: {bg_color}; color: {fg_color}; border: none; border-radius: 12px; font-size: 20px; font-weight: 900;")
        text_col = QtWidgets.QVBoxLayout()
        for text, style in [
            (title, "color: #334155; font-size: 12px; font-weight: 900;"),
            (str(value), f"color: {fg_color}; font-size: 22px; font-weight: 900;"),
            (note, "color: #64748b; font-size: 11px; font-weight: 700;"),
        ]:
            label = QtWidgets.QLabel(text)
            label.setStyleSheet("border: none; background: transparent; " + style)
            text_col.addWidget(label)
        layout.addWidget(icon_lbl)
        layout.addLayout(text_col, 1)
        return card

    def _build_staff_billing_catalog(self):
        sample = [
            (128, "Nguyễn Văn Hùng", 850000, "unpaid", "0987 654 321", 35),
            (127, "Trần Thị Mai", 650000, "unpaid", "0912 345 678", 28),
            (126, "Lê Văn Nam", 1200000, "unpaid", "0908 111 222", 42),
            (125, "Phạm Thị Lan", 1500000, "paid", "0933 222 111", 31),
            (124, "Hoàng Anh Tuấn", 700000, "paid", "0977 333 444", 39),
            (123, "Vũ Thị Hương", 1350000, "unpaid", "0966 444 555", 46),
            (122, "Đỗ Minh Quân", 950000, "paid", "0955 555 666", 30),
            (121, "Nguyễn Thị Hoa", 600000, "cancelled", "0944 666 777", 52),
            (120, "Bùi Văn Dũng", 1100000, "unpaid", "0933 777 888", 44),
            (119, "Trương Thị Kiều", 800000, "refunded", "0922 888 999", 27),
        ]
        rows = []
        try:
            rows = PaymentController.get_all() or []
        except Exception:
            rows = []
        catalog = []
        for idx, row in enumerate(rows):
            item = dict(row)
            sid, name, amount, status, phone, age = sample[idx % len(sample)]
            item.setdefault("patient_name", name)
            item.setdefault("patient_phone", phone)
            item.setdefault("patient_age", age)
            item.setdefault("patient_address", "123 Đường Lê Lợi, P.1, Q.1, TP.HCM")
            item.setdefault("staff_name", self.username)
            catalog.append(item)
        seen = {str(x.get("payment_id")) for x in catalog}
        for sid, name, amount, status, phone, age in sample:
            if str(sid) not in seen:
                catalog.append({"payment_id": sid, "patient_name": name, "patient_phone": phone, "patient_age": age, "patient_address": "123 Đường Lê Lợi, P.1, Q.1, TP.HCM", "payment_date": "23/05/2026 08:15", "total_amount": amount, "status": status, "staff_name": "Nguyễn Thị Lan"})
        return catalog

    def _staff_bill_status_key(self, bill):
        raw = str(bill.get("status") or "unpaid").lower().strip()
        return {"pending": "unpaid", "waiting": "unpaid", "paid": "paid", "done": "paid", "cancelled": "cancelled", "canceled": "cancelled", "refunded": "refunded", "refund": "refunded"}.get(raw, raw if raw in {"unpaid", "paid", "cancelled", "refunded"} else "unpaid")

    def _staff_bill_status_text(self, bill):
        return {"unpaid": "Chờ thanh toán", "paid": "Đã thanh toán", "cancelled": "Đã hủy", "refunded": "Hoàn tiền"}.get(self._staff_bill_status_key(bill), "Chờ thanh toán")

    def _set_staff_bill_tab(self, key):
        self.staff_bill_active_tab = key
        for tab_key, btn in self.staff_bill_status_tabs.items():
            btn.setChecked(tab_key == key)
        self._refresh_staff_billing_table()

    def _refresh_staff_billing_table(self):
        if not hasattr(self, "staff_bill_table"):
            return
        if not getattr(self, "staff_billing_rows", None):
            self.staff_billing_rows = self._build_staff_billing_catalog()
        keyword = str(self.staff_bill_search_input.text() or "").strip().lower() if hasattr(self, "staff_bill_search_input") else ""
        active_tab = getattr(self, "staff_bill_active_tab", "all")
        filtered = []
        for bill in self.staff_billing_rows:
            haystack = f"{self._staff_bill_code(bill)} {bill.get('patient_name', '')} {self._staff_bill_status_text(bill)}".lower()
            if active_tab != "all" and self._staff_bill_status_key(bill) != active_tab:
                continue
            if keyword and keyword not in haystack:
                continue
            filtered.append(bill)
        self.staff_billing_filtered_rows = filtered
        self.staff_bill_table.blockSignals(True)
        self.staff_bill_table.setRowCount(len(filtered))
        for row, bill in enumerate(filtered):
            for col, value in enumerate([self._staff_bill_code(bill), self._staff_display_text(bill.get("patient_name") or ""), str(bill.get("payment_date") or bill.get("appointment_date") or ""), self._format_staff_money(bill.get("total_amount"))]):
                self.staff_bill_table.setItem(row, col, QtWidgets.QTableWidgetItem(value))
            self.staff_bill_table.setCellWidget(row, 4, self._staff_bill_badge(bill))
            self.staff_bill_table.setCellWidget(row, 5, self._staff_bill_actions(row))
        self.staff_bill_table.blockSignals(False)
        self.staff_bill_list_title.setText(f"Danh sách hóa đơn ({len(filtered)})")
        self.staff_bill_footer_label.setText(f"Hiển thị {min(len(filtered), 10)} bản ghi")
        if filtered:
            self.staff_bill_table.selectRow(0)
            self._update_staff_bill_detail(filtered[0])
        else:
            self._reset_staff_bill_detail()

    def _staff_bill_code(self, bill):
        try:
            return f"HD{int(bill.get('payment_id') or 0):06d}"
        except (TypeError, ValueError):
            return f"HD{bill.get('payment_id') or '------'}"

    def _staff_bill_badge(self, bill):
        bg, fg = {"unpaid": ("#fff3e4", "#f97316"), "paid": ("#dcfce7", "#16a34a"), "cancelled": ("#fee2e2", "#ef4444"), "refunded": ("#dbeafe", "#2563eb")}.get(self._staff_bill_status_key(bill), ("#fff3e4", "#f97316"))
        badge = QtWidgets.QLabel(self._staff_bill_status_text(bill))
        badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        badge.setMinimumWidth(116)
        badge.setStyleSheet(f"background: {bg}; color: {fg}; border: none; border-radius: 11px; padding: 5px 10px; font-size: 11px; font-weight: 900;")
        wrap = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrap)
        layout.setContentsMargins(2, 4, 2, 4)
        layout.addWidget(badge)
        return wrap

    def _staff_bill_actions(self, row):
        wrap = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrap)
        layout.setContentsMargins(0, 0, 0, 0)
        for icon in ["👁", "⋮"]:
            btn = QtWidgets.QPushButton(icon)
            btn.setFixedSize(32, 30)
            btn.setStyleSheet("QPushButton { background: #ffffff; border: 1px solid #dbe4ee; border-radius: 8px; color: #2563eb; font-weight: 900; }")
            btn.clicked.connect(lambda _, r=row: self._select_staff_bill_row(r))
            layout.addWidget(btn)
        return wrap

    def _select_staff_bill_row(self, row):
        if 0 <= row < len(getattr(self, "staff_billing_filtered_rows", [])):
            self.staff_bill_table.selectRow(row)
            self._update_staff_bill_detail(self.staff_billing_filtered_rows[row])

    def _on_staff_billing_row_selected(self):
        row = self.staff_bill_table.currentRow()
        if row < 0 or row >= len(getattr(self, "staff_billing_filtered_rows", [])):
            self.staff_billing_selected_id = None
            self.staff_billing_selected_status = ""
            return
        self._update_staff_bill_detail(self.staff_billing_filtered_rows[row])

    def _update_staff_bill_detail(self, bill):
        self.staff_billing_selected = bill
        self.staff_billing_selected_id = bill.get("payment_id")
        self.staff_billing_selected_status = self._staff_bill_status_key(bill)
        amount = float(bill.get("total_amount") or 0)
        self.staff_bill_detail_header.setText(f"Mã hóa đơn        {self._staff_bill_code(bill)}        {self._staff_bill_status_text(bill)}\nNgày tạo: {bill.get('payment_date') or bill.get('appointment_date') or '--'}\nNhân viên: {bill.get('staff_name') or self.username}")
        self.staff_bill_patient_card.setText(f"👤  {self._staff_display_text(bill.get('patient_name') or '')}\n{bill.get('patient_age', 35)} tuổi  •  {bill.get('patient_phone') or 'Chưa có SĐT'}\nĐịa chỉ: {bill.get('patient_address') or '--'}")
        services = self._staff_bill_services(bill)
        self.staff_bill_service_table.setRowCount(len(services))
        for row, (name, qty, unit_price) in enumerate(services):
            for col, value in enumerate([name, str(qty), self._format_staff_money(unit_price), self._format_staff_money(qty * unit_price)]):
                self.staff_bill_service_table.setItem(row, col, QtWidgets.QTableWidgetItem(value))
        self.staff_bill_total_label.setText(f"Tổng cần thanh toán: {self._format_staff_money(amount)}")
        self.staff_bill_received_input.blockSignals(True)
        self.staff_bill_received_input.setText(str(int(amount)) if self.staff_billing_selected_status == "unpaid" else "")
        self.staff_bill_received_input.blockSignals(False)
        self._update_staff_bill_change()
        can_pay = self.staff_billing_selected_status == "unpaid"
        self.staff_bill_confirm_btn.setEnabled(can_pay)
        self.staff_bill_confirm_btn.setText("✓  Xác nhận thanh toán" if can_pay else "Đã xử lý hóa đơn")
        self._set_staff_billing_feedback(f"Đã chọn hóa đơn {self._staff_bill_code(bill)}.", is_error=False)

    def _reset_staff_bill_detail(self):
        self.staff_billing_selected = None
        self.staff_billing_selected_id = None
        self.staff_billing_selected_status = ""
        self.staff_bill_detail_header.setText("Chưa chọn hóa đơn")
        self.staff_bill_patient_card.setText("Chọn hóa đơn ở bảng bên trái để xem chi tiết.")
        self.staff_bill_service_table.setRowCount(0)
        self.staff_bill_total_label.setText("Tổng cần thanh toán: --")
        self.staff_bill_received_input.clear()
        self.staff_bill_change_label.setText("Tiền thừa: 0 đ")

    def _staff_bill_services(self, bill):
        amount = float(bill.get("total_amount") or 0)
        if amount >= 850000:
            return [("Khám tổng quát", 1, 300000), ("Xét nghiệm máu", 1, 250000), ("Siêu âm ổ bụng", 1, max(0, amount - 550000))]
        return [("Khám tổng quát", 1, amount)]

    def _set_staff_bill_payment_method(self, selected_btn):
        for btn in self.staff_bill_method_buttons:
            btn.setChecked(btn is selected_btn)

    def _update_staff_bill_change(self):
        bill = getattr(self, "staff_billing_selected", None)
        amount = float((bill or {}).get("total_amount") or 0)
        raw = self.staff_bill_received_input.text().replace(".", "").replace(",", "").strip() if hasattr(self, "staff_bill_received_input") else ""
        try:
            received = float(raw or 0)
        except ValueError:
            received = 0
        self.staff_bill_change_label.setText(f"Tiền thừa: {self._format_staff_money(max(0, received - amount))}")

    def _handle_staff_confirm_payment(self):
        bill = getattr(self, "staff_billing_selected", None)
        if not bill:
            self._set_staff_billing_feedback("Vui lòng chọn hóa đơn trước khi xác nhận thanh toán.", is_error=True)
            return
        if self._staff_bill_status_key(bill) != "unpaid":
            self._set_staff_billing_feedback("Chỉ hóa đơn chờ thanh toán mới được xác nhận.", is_error=True)
            return
        raw = self.staff_bill_received_input.text().replace(".", "").replace(",", "").strip()
        try:
            received = float(raw or 0)
        except ValueError:
            self._set_staff_billing_feedback("Số tiền nhận không hợp lệ.", is_error=True)
            return
        if received < float(bill.get("total_amount") or 0):
            self._set_staff_billing_feedback("Số tiền nhận chưa đủ để thanh toán hóa đơn.", is_error=True)
            return
        try:
            if isinstance(bill.get("payment_id"), int):
                PaymentController.update_status(bill["payment_id"], "paid")
        except Exception:
            pass
        bill["status"] = "paid"
        self._refresh_staff_billing_table()
        self._set_staff_billing_feedback(f"Đã xác nhận thanh toán cho {self._staff_bill_code(bill)}.", is_error=False)

    def _handle_staff_print_receipt(self):
        bill = getattr(self, "staff_billing_selected", None)
        if not bill:
            self._set_staff_billing_feedback("Vui lòng chọn hóa đơn để in.", is_error=True)
            return
        QtWidgets.QMessageBox.information(self, "In hóa đơn", f"Hóa đơn {self._staff_bill_code(bill)} đã sẵn sàng để in.")
        self._set_staff_billing_feedback(f"Đã mở xem trước hóa đơn {self._staff_bill_code(bill)}.", is_error=False)

    def _set_staff_billing_feedback(self, message, is_error=False):
        if not hasattr(self, "staff_bill_feedback"):
            return
        color = "#b91c1c" if is_error else "#166534"
        self.staff_bill_feedback.setStyleSheet(f"border: none; background: transparent; font-size: 12px; color: {color}; font-weight: 700;")
        self.staff_bill_feedback.setText(message)

    def _build_appointment_management_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: #f8fbff; border: none;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        header = QtWidgets.QFrame()
        header.setStyleSheet("background: transparent; border: none;")
        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(4, 0, 4, 0)
        header_layout.setSpacing(14)

        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(5)
        heading = QtWidgets.QLabel("Quản lý lịch hẹn")
        heading.setStyleSheet("border: none; background: transparent; font-size: 25px; color: #0f172a; font-weight: 900;")
        breadcrumb = QtWidgets.QLabel("Trang chủ  ›  Quản lý lịch hẹn")
        breadcrumb.setStyleSheet("border: none; background: transparent; font-size: 14px; color: #64748b; font-weight: 700;")
        title_col.addWidget(heading)
        title_col.addWidget(breadcrumb)

        bell = QtWidgets.QLabel("🔔")
        bell.setFixedSize(34, 34)
        bell.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        bell.setStyleSheet("border: none; background: transparent; font-size: 21px; color: #64748b;")
        avatar = QtWidgets.QLabel("👤")
        avatar.setFixedSize(42, 42)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("border: none; background: #eaf2ff; border-radius: 21px; font-size: 22px;")
        user_lbl = QtWidgets.QLabel(f"{self.username}  ▾")
        user_lbl.setStyleSheet("border: none; background: transparent; font-size: 13px; color: #0f172a; font-weight: 900;")
        header_layout.addLayout(title_col)
        header_layout.addStretch()
        header_layout.addWidget(bell)
        header_layout.addWidget(avatar)
        header_layout.addWidget(user_lbl)
        layout.addWidget(header)

        tabs = QtWidgets.QHBoxLayout()
        tabs.setSpacing(28)
        for index, label in enumerate(["Lịch hẹn hôm nay", "Lịch hẹn ngày mai", "📅  Lịch hẹn theo ngày"]):
            tab = QtWidgets.QPushButton(label)
            tab.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            if index == 0:
                tab.setStyleSheet(
                    "QPushButton { border: none; border-bottom: 3px solid #13a66b; background: transparent; padding: 8px 12px; color: #13a66b; font-size: 15px; font-weight: 900; }"
                )
            else:
                tab.setStyleSheet(
                    "QPushButton { border: none; background: transparent; padding: 8px 12px; color: #64748b; font-size: 15px; font-weight: 800; }"
                    "QPushButton:hover { color: #13a66b; }"
                )
            tabs.addWidget(tab)
        tabs.addStretch()
        layout.addLayout(tabs)

        content = QtWidgets.QHBoxLayout()
        content.setSpacing(22)

        form_card = self._build_section_card("Thông tin lịch hẹn")
        self.staff_appt_form_card = form_card
        self.staff_appt_form_card.setVisible(False)
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
        for widget in [
            self.staff_appt_patient_id_input,
            self.staff_appt_doctor_combo,
            self.staff_appt_service_combo,
            self.staff_appt_date_input,
            self.staff_appt_time_input,
            self.staff_appt_status_combo,
            self.staff_appt_note_input,
        ]:
            widget.setStyleSheet(self._intake_input_style())

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
        btn_create_form = QtWidgets.QPushButton("➕ Tạo lịch hẹn")
        btn_reschedule = QtWidgets.QPushButton("🕒 Dời/Cập nhật lịch")
        btn_cancel = QtWidgets.QPushButton("❌ Hủy lịch đã chọn")
        btn_clear = QtWidgets.QPushButton("Làm mới biểu mẫu")
        btn_create_form.setStyleSheet(self._intake_primary_button_style())
        for btn in [btn_reschedule, btn_cancel, btn_clear]:
            btn.setStyleSheet(self._intake_secondary_button_style())
        btn_create_form.clicked.connect(self._handle_staff_appointment_create)
        btn_reschedule.clicked.connect(self._handle_staff_appointment_reschedule)
        btn_cancel.clicked.connect(self._handle_staff_appointment_cancel)
        btn_clear.clicked.connect(self._reset_staff_appointment_form)
        actions.addWidget(btn_create_form)
        actions.addWidget(btn_reschedule)
        actions.addWidget(btn_cancel)
        actions.addStretch()
        actions.addWidget(btn_clear)

        self.staff_appt_feedback = QtWidgets.QLabel("Sẵn sàng điều phối lịch hẹn.")
        self.staff_appt_feedback.setWordWrap(True)
        self.staff_appt_feedback.setStyleSheet("border: none; background: transparent; font-size: 12px; color: #475569;")
        form_card.layout().addLayout(form_grid)
        form_card.layout().addLayout(actions)
        form_card.layout().addWidget(self.staff_appt_feedback)

        left_panel = self._build_section_card("")
        left_layout = left_panel.layout()
        search_row = QtWidgets.QHBoxLayout()
        search_row.setSpacing(10)
        self.staff_appt_search_input = QtWidgets.QLineEdit()
        self.staff_appt_search_input.setPlaceholderText("Tìm kiếm bệnh nhân, SĐT, dịch vụ...")
        self.staff_appt_search_input.setMinimumHeight(42)
        self.staff_appt_search_input.setStyleSheet(self._intake_input_style())
        self.staff_appt_search_input.textChanged.connect(self._apply_staff_appointment_filters)
        create_btn = QtWidgets.QPushButton("+  Tạo lịch hẹn")
        create_btn.setFixedWidth(150)
        create_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        create_btn.setStyleSheet(self._intake_primary_button_style())
        create_btn.clicked.connect(self._toggle_staff_appointment_form)
        search_row.addWidget(self.staff_appt_search_input, 1)
        search_row.addWidget(create_btn)
        left_layout.addLayout(search_row)

        filters = QtWidgets.QHBoxLayout()
        filters.setSpacing(10)
        self.staff_appt_filter_doctor_combo = QtWidgets.QComboBox()
        self.staff_appt_filter_service_combo = QtWidgets.QComboBox()
        self.staff_appt_filter_status_combo = QtWidgets.QComboBox()
        self.staff_appt_filter_status_combo.addItems(["Trạng thái", "pending", "confirmed", "in_progress", "done", "cancelled"])
        self.staff_appt_filter_date_input = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.staff_appt_filter_date_input.setDisplayFormat("dd/MM/yyyy")
        self.staff_appt_filter_date_input.setCalendarPopup(True)
        for widget in [
            self.staff_appt_filter_doctor_combo,
            self.staff_appt_filter_service_combo,
            self.staff_appt_filter_status_combo,
            self.staff_appt_filter_date_input,
        ]:
            widget.setStyleSheet(self._intake_input_style())
        for combo in [self.staff_appt_filter_doctor_combo, self.staff_appt_filter_service_combo, self.staff_appt_filter_status_combo]:
            combo.currentIndexChanged.connect(self._apply_staff_appointment_filters)
        self.staff_appt_filter_date_input.dateChanged.connect(self._apply_staff_appointment_filters)
        filters.addWidget(self.staff_appt_filter_doctor_combo)
        filters.addWidget(self.staff_appt_filter_service_combo)
        filters.addWidget(self.staff_appt_filter_status_combo)
        filters.addWidget(self.staff_appt_filter_date_input)
        left_layout.addLayout(filters)
        left_layout.addWidget(self.staff_appt_form_card)

        self.staff_appt_table = QtWidgets.QTableWidget()
        self.staff_appt_table.setColumnCount(6)
        self.staff_appt_table.setHorizontalHeaderLabels(["Giờ hẹn", "Bệnh nhân", "Dịch vụ", "Bác sĩ", "Trạng thái", "Thao tác"])
        self.staff_appt_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.staff_appt_table.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.SingleSelection)
        self.staff_appt_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_appt_table.setShowGrid(False)
        self.staff_appt_table.verticalHeader().setVisible(False)
        self.staff_appt_table.verticalHeader().setDefaultSectionSize(48)
        self.staff_appt_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staff_appt_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_appt_table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.staff_appt_table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_appt_table.setColumnWidth(4, 150)
        self.staff_appt_table.setColumnWidth(5, 92)
        self.staff_appt_table.setStyleSheet(
            "QTableWidget { border: 1px solid #e7edf5; border-radius: 12px; background: #ffffff; }"
            "QHeaderView::section { background: #f8fafc; color: #1f2937; font-size: 12px; font-weight: 900; border: none; padding: 10px; }"
            "QTableWidget::item { border-bottom: 1px solid #edf2f7; padding: 8px; color: #0f172a; font-weight: 700; }"
            "QTableWidget::item:selected { background: #ecfdf5; color: #0f172a; }"
        )
        self.staff_appt_table.itemSelectionChanged.connect(self._handle_staff_appointment_selection)
        left_layout.addWidget(self.staff_appt_table, 1)

        self.staff_appt_paging_label = QtWidgets.QLabel("Hiển thị 0 lịch hẹn")
        self.staff_appt_paging_label.setStyleSheet("border: none; background: transparent; color: #64748b; font-size: 12px; font-weight: 700;")
        left_layout.addWidget(self.staff_appt_paging_label)

        legend = QtWidgets.QHBoxLayout()
        legend.setSpacing(18)
        for text, color, note in [
            ("Đang chờ", "#f59e0b", "Bệnh nhân chưa đến/chưa xác nhận"),
            ("Đã xác nhận", "#13a66b", "Bệnh nhân và chờ đến lượt"),
            ("Đang khám", "#2563eb", "Bệnh nhân đang được bác sĩ khám"),
            ("Đã hoàn tất", "#8b5cf6", "Khám xong và đã thanh toán"),
            ("Đã hủy", "#ef4444", "Lịch hẹn đã bị hủy"),
        ]:
            legend.addWidget(self._build_staff_status_legend_item(text, color, note))
        left_layout.addLayout(legend)

        detail_panel = self._build_section_card("Chi tiết lịch hẹn")
        detail_layout = detail_panel.layout()
        self.staff_appt_detail_patient = QtWidgets.QLabel("Chưa chọn lịch hẹn")
        self.staff_appt_detail_patient.setWordWrap(True)
        self.staff_appt_detail_patient.setStyleSheet("border: none; background: transparent; font-size: 15px; color: #0f172a; font-weight: 900;")
        self.staff_appt_detail_info = QtWidgets.QLabel("Chọn một lịch hẹn ở bảng bên trái để xem chi tiết.")
        self.staff_appt_detail_info.setWordWrap(True)
        self.staff_appt_detail_info.setStyleSheet("border: none; background: transparent; font-size: 13px; color: #475569; font-weight: 700;")
        self.staff_appt_detail_timeline = QtWidgets.QLabel("Lịch sử cập nhật sẽ hiển thị tại đây.")
        self.staff_appt_detail_timeline.setWordWrap(True)
        self.staff_appt_detail_timeline.setStyleSheet("border: none; background: transparent; font-size: 13px; color: #475569; font-weight: 700;")
        detail_layout.addWidget(self.staff_appt_detail_patient)
        detail_layout.addWidget(self.staff_appt_detail_info)
        detail_layout.addSpacing(10)
        timeline_title = QtWidgets.QLabel("Lịch sử cập nhật")
        timeline_title.setStyleSheet("border: none; background: transparent; font-size: 15px; color: #0f172a; font-weight: 900;")
        detail_layout.addWidget(timeline_title)
        detail_layout.addWidget(self.staff_appt_detail_timeline)
        detail_layout.addStretch()

        detail_actions_title = QtWidgets.QLabel("Thao tác")
        detail_actions_title.setStyleSheet("border: none; background: transparent; font-size: 15px; color: #0f172a; font-weight: 900;")
        self.staff_appt_btn_edit = QtWidgets.QPushButton("✎  Sửa lịch hẹn")
        self.staff_appt_btn_cancel = QtWidgets.QPushButton("🗑  Hủy lịch hẹn")
        self.staff_appt_btn_print = QtWidgets.QPushButton("🖨  In phiếu hẹn")
        self.staff_appt_btn_edit.clicked.connect(self._show_staff_appointment_form_for_selected)
        self.staff_appt_btn_cancel.clicked.connect(self._handle_staff_appointment_cancel)
        self.staff_appt_btn_print.clicked.connect(self._handle_staff_appt_print)
        self.staff_appt_btn_edit.setStyleSheet("background: #ffffff; color: #13a66b; border: 1px solid #13a66b; border-radius: 9px; padding: 10px; font-weight: 900;")
        self.staff_appt_btn_cancel.setStyleSheet("background: #ffffff; color: #ef4444; border: 1px solid #ef4444; border-radius: 9px; padding: 10px; font-weight: 900;")
        self.staff_appt_btn_print.setStyleSheet(self._intake_primary_button_style())
        detail_layout.addWidget(detail_actions_title)
        detail_layout.addWidget(self.staff_appt_btn_edit)
        detail_layout.addWidget(self.staff_appt_btn_cancel)
        detail_layout.addWidget(self.staff_appt_btn_print)

        content.addWidget(left_panel, 7)
        content.addWidget(detail_panel, 3)
        layout.addLayout(content, 1)

        self._load_staff_appointment_dropdowns()
        self._refresh_staff_appointment_table()
        return page

    def _apply_staff_appointment_filters(self):
        self._refresh_staff_appointment_table()

    def _refresh_staff_appointment_table(self):
        role = self._get_current_user_role()
        user_context = self._build_appointment_user_context()
        rows = AppointmentController.get_all_for_role(role, user_context) or []
        if isinstance(rows, dict):
            self.staff_appointment_rows = []
            self.staff_appt_table.setRowCount(0)
            self._reset_staff_appointment_detail()
            self._set_staff_appt_feedback(rows.get("message") or "Không thể tải danh sách lịch hẹn.", is_error=True)
            return

        query = str(self.staff_appt_search_input.text() if hasattr(self, "staff_appt_search_input") else "").strip().lower()
        doctor_id = self.staff_appt_filter_doctor_combo.currentData() if hasattr(self, "staff_appt_filter_doctor_combo") else None
        service_name = str(self.staff_appt_filter_service_combo.currentData() or "") if hasattr(self, "staff_appt_filter_service_combo") else ""
        status_filter = self.staff_appt_filter_status_combo.currentText() if hasattr(self, "staff_appt_filter_status_combo") else "Trạng thái"

        filtered = []
        for appt in list(rows):
            current_service = self._extract_service_name_from_note(str(appt.get("note") or ""))
            haystack = " ".join([
                str(appt.get("appointment_id") or ""),
                str(appt.get("patient_name") or ""),
                str(appt.get("patient_phone") or ""),
                str(appt.get("doctor_name") or ""),
                current_service,
            ]).lower()
            if query and query not in haystack:
                continue
            if doctor_id and str(appt.get("doctor_id") or "") != str(doctor_id):
                continue
            if service_name and current_service != service_name:
                continue
            if status_filter != "Trạng thái" and str(appt.get("status") or "") != status_filter:
                continue
            appt = dict(appt)
            appt["service_name"] = current_service
            filtered.append(appt)

        self.staff_appointment_rows = filtered
        self.staff_appt_table.blockSignals(True)
        self.staff_appt_table.setRowCount(len(filtered))
        for row, appt in enumerate(filtered):
            service_text = str(appt.get("service_name") or "")
            self.staff_appt_table.setItem(row, 0, QtWidgets.QTableWidgetItem(self._staff_display_text(str(appt.get("appointment_date", "")))))
            self.staff_appt_table.setItem(row, 1, QtWidgets.QTableWidgetItem(self._staff_display_text(str(appt.get("patient_name", "")))))
            self.staff_appt_table.setItem(row, 2, QtWidgets.QTableWidgetItem(self._staff_display_text(service_text)))
            self.staff_appt_table.setItem(row, 3, QtWidgets.QTableWidgetItem(self._staff_display_text(str(appt.get("doctor_name", "")))))
            self.staff_appt_table.setCellWidget(row, 4, self._create_status_badge_widget(str(appt.get("status") or "pending")))
            self.staff_appt_table.setCellWidget(row, 5, self._create_appointment_actions_widget(row))
        self.staff_appt_table.blockSignals(False)

        if hasattr(self, "staff_appt_paging_label"):
            self.staff_appt_paging_label.setText(f"Hiển thị {len(filtered)} lịch hẹn")
        if filtered:
            self.staff_appt_table.selectRow(0)
            self._set_staff_appointment_detail(filtered[0])
        else:
            self._reset_staff_appointment_detail()

    def _handle_staff_appointment_selection(self):
        row = self.staff_appt_table.currentRow()
        if row < 0 or row >= len(self.staff_appointment_rows):
            self.staff_appointment_selected_id = None
            self.shared_selected_appointment_id = None
            self._reset_staff_appointment_detail()
            return

        appt = self.staff_appointment_rows[row]
        self.staff_appointment_selected_id = appt.get("appointment_id")
        self.shared_selected_appointment_id = self.staff_appointment_selected_id
        self.shared_selected_patient_id = appt.get("patient_id")
        self.staff_appt_patient_id_input.setText(str(appt.get("patient_id") or ""))

        doctor_index = self.staff_appt_doctor_combo.findData(appt.get("doctor_id"))
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
        status_index = self.staff_appt_status_combo.findText(str(appt.get("status") or "pending"))
        if status_index >= 0:
            self.staff_appt_status_combo.setCurrentIndex(status_index)
        self.staff_appt_note_input.setText(str(appt.get("note") or ""))
        self._set_staff_appointment_detail(appt)
        self._set_staff_appt_feedback(f"Đã chọn lịch hẹn #{self.staff_appointment_selected_id} để cập nhật/hủy.", is_error=False)

    def _build_staff_service_lookup_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: #f8fbff; border: none;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        header = QtWidgets.QFrame()
        header.setStyleSheet("background: transparent; border: none;")
        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(4, 0, 4, 0)
        header_layout.setSpacing(14)
        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(5)
        heading = QtWidgets.QLabel("Dịch vụ & Gói khám")
        heading.setStyleSheet("border: none; background: transparent; font-size: 25px; color: #0f172a; font-weight: 900;")
        breadcrumb = QtWidgets.QLabel("Trang chủ  ›  Dịch vụ & Gói khám")
        breadcrumb.setStyleSheet("border: none; background: transparent; font-size: 14px; color: #64748b; font-weight: 700;")
        title_col.addWidget(heading)
        title_col.addWidget(breadcrumb)
        bell = QtWidgets.QLabel("🔔")
        bell.setFixedSize(34, 34)
        bell.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        bell.setStyleSheet("border: none; background: transparent; font-size: 21px; color: #64748b;")
        avatar = QtWidgets.QLabel("👤")
        avatar.setFixedSize(42, 42)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("border: none; background: #eaf2ff; border-radius: 21px; font-size: 20px;")
        user_lbl = QtWidgets.QLabel(f"{self.username}  ▾")
        user_lbl.setStyleSheet("border: none; background: transparent; font-size: 13px; color: #0f172a; font-weight: 900;")
        header_layout.addLayout(title_col, 1)
        header_layout.addWidget(bell)
        header_layout.addWidget(avatar)
        header_layout.addWidget(user_lbl)
        layout.addWidget(header)

        self.staff_service_rows = self._build_staff_service_catalog()

        kpi_row = QtWidgets.QHBoxLayout()
        kpi_row.setSpacing(16)
        total_services = len([s for s in self.staff_service_rows if not s.get("is_package")])
        total_packages = len([s for s in self.staff_service_rows if s.get("is_package")])
        active_count = len([s for s in self.staff_service_rows if self._staff_service_is_active(s)])
        revenue = sum(float(s.get("price") or 0) for s in self.staff_service_rows[:10]) * 21
        kpi_row.addWidget(self._build_staff_service_kpi_card("📄", "Tổng dịch vụ", str(total_services), "Đang áp dụng", "#efe9ff", "#6d5dfc"))
        kpi_row.addWidget(self._build_staff_service_kpi_card("💼", "Gói khám", str(total_packages), "Đang áp dụng", "#eaf2ff", "#2563eb"))
        kpi_row.addWidget(self._build_staff_service_kpi_card("🎓", "Dịch vụ nổi bật", "6", "Được quan tâm", "#ffeaf1", "#f43f5e"))
        kpi_row.addWidget(self._build_staff_service_kpi_card("💧", "Tổng doanh thu dịch vụ", self._format_staff_money(revenue), "Trong tháng 05", "#eaf2ff", "#4f46e5"), 2)
        layout.addLayout(kpi_row)

        body = QtWidgets.QHBoxLayout()
        body.setSpacing(18)

        list_card = self._build_section_card("")
        list_layout = list_card.layout()
        tab_row = QtWidgets.QHBoxLayout()
        tab_row.setSpacing(22)
        self.staff_service_tab_service = QtWidgets.QPushButton("Dịch vụ")
        self.staff_service_tab_package = QtWidgets.QPushButton("Gói khám")
        for idx, btn in enumerate([self.staff_service_tab_service, self.staff_service_tab_package]):
            btn.setCheckable(True)
            btn.setChecked(idx == 0)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(
                "QPushButton { border: none; background: transparent; padding: 8px 12px; color: #64748b; font-size: 14px; font-weight: 900; }"
                "QPushButton:checked { color: #13a66b; border-bottom: 3px solid #13a66b; }"
            )
        self.staff_service_tab_service.clicked.connect(lambda: self._set_staff_service_mode(False))
        self.staff_service_tab_package.clicked.connect(lambda: self._set_staff_service_mode(True))
        tab_row.addWidget(self.staff_service_tab_service)
        tab_row.addWidget(self.staff_service_tab_package)
        tab_row.addStretch()
        list_layout.addLayout(tab_row)

        filter_row = QtWidgets.QHBoxLayout()
        filter_row.setSpacing(12)
        self.staff_service_search_input = QtWidgets.QLineEdit()
        self.staff_service_search_input.setPlaceholderText("Tìm kiếm dịch vụ...")
        self.staff_service_search_input.setStyleSheet(self._intake_input_style())
        self.staff_service_category_combo = QtWidgets.QComboBox()
        self.staff_service_category_combo.addItems(["Tất cả danh mục", "Khám bệnh", "Khám chuyên khoa", "Xét nghiệm", "Chẩn đoán hình ảnh", "Tiêm chủng", "Tư vấn"])
        self.staff_service_category_combo.setStyleSheet(self._intake_input_style())
        self.staff_service_status_combo = QtWidgets.QComboBox()
        self.staff_service_status_combo.addItems(["Tất cả", "Đang áp dụng", "Ngưng áp dụng"])
        self.staff_service_status_combo.setStyleSheet(self._intake_input_style())
        add_btn = QtWidgets.QPushButton("+  Thêm dịch vụ")
        add_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        add_btn.setStyleSheet(self._intake_primary_button_style())
        add_btn.clicked.connect(self._show_staff_service_add_dialog)
        self.staff_service_search_input.textChanged.connect(self._refresh_staff_service_lookup)
        self.staff_service_category_combo.currentIndexChanged.connect(self._refresh_staff_service_lookup)
        self.staff_service_status_combo.currentIndexChanged.connect(self._refresh_staff_service_lookup)
        filter_row.addWidget(self.staff_service_search_input, 2)
        filter_row.addWidget(self.staff_service_category_combo)
        filter_row.addWidget(self.staff_service_status_combo)
        filter_row.addWidget(add_btn)
        list_layout.addLayout(filter_row)

        self.staff_service_list_title = QtWidgets.QLabel("Danh sách dịch vụ (0)")
        self.staff_service_list_title.setStyleSheet("border: none; background: transparent; font-size: 17px; color: #0f172a; font-weight: 900;")
        list_layout.addWidget(self.staff_service_list_title)

        self.staff_service_table = QtWidgets.QTableWidget(0, 7)
        self.staff_service_table.setHorizontalHeaderLabels(["STT", "Tên dịch vụ", "Danh mục", "Giá (đ)", "Thời gian", "Trạng thái", "Thao tác"])
        self.staff_service_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.staff_service_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.staff_service_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_service_table.setShowGrid(False)
        self.staff_service_table.verticalHeader().setVisible(False)
        self.staff_service_table.verticalHeader().setDefaultSectionSize(58)
        self.staff_service_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staff_service_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_service_table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_service_table.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_service_table.setStyleSheet(
            "QTableWidget { border: 1px solid #e7edf5; border-radius: 12px; background: #ffffff; color: #0f172a; font-size: 13px; font-weight: 700; }"
            "QHeaderView::section { background: #f8fafc; color: #1f2937; font-size: 12px; font-weight: 900; border: none; padding: 10px; }"
            "QTableWidget::item { border-bottom: 1px solid #edf2f7; padding: 8px; }"
            "QTableWidget::item:selected { background: #ecfdf5; color: #0f172a; }"
        )
        self.staff_service_table.itemSelectionChanged.connect(self._handle_staff_service_selection)
        list_layout.addWidget(self.staff_service_table, 1)

        footer = QtWidgets.QHBoxLayout()
        self.staff_service_lookup_empty = QtWidgets.QLabel("Hiển thị 0 bản ghi")
        self.staff_service_lookup_empty.setStyleSheet("border: none; background: transparent; color: #64748b; font-size: 12px; font-weight: 700;")
        footer.addWidget(self.staff_service_lookup_empty)
        footer.addStretch()
        for label in ["‹", "1", "2", "3", "4", "›"]:
            btn = QtWidgets.QPushButton(label)
            btn.setFixedSize(36, 32)
            btn.setStyleSheet(
                "QPushButton { background: #ffffff; border: 1px solid #dbe4ee; border-radius: 8px; color: #334155; font-weight: 900; }"
                "QPushButton:hover { border-color: #13a66b; color: #13a66b; }"
            )
            if label == "1":
                btn.setStyleSheet("background: #13a66b; border: none; border-radius: 8px; color: white; font-weight: 900;")
            footer.addWidget(btn)
        list_layout.addLayout(footer)

        detail_card = self._build_section_card("Thông tin dịch vụ")
        detail_layout = detail_card.layout()
        detail_layout.setSpacing(14)
        profile = QtWidgets.QHBoxLayout()
        self.staff_service_icon = QtWidgets.QLabel("✚")
        self.staff_service_icon.setFixedSize(82, 82)
        self.staff_service_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.staff_service_icon.setStyleSheet("background: #e7f8ef; color: #13a66b; border-radius: 14px; font-size: 40px; font-weight: 900;")
        info_col = QtWidgets.QVBoxLayout()
        self.staff_service_detail_name = QtWidgets.QLabel("Chưa chọn dịch vụ")
        self.staff_service_detail_name.setWordWrap(True)
        self.staff_service_detail_name.setStyleSheet("border: none; background: transparent; font-size: 18px; color: #0f172a; font-weight: 900;")
        self.staff_service_detail_meta = QtWidgets.QLabel("Danh mục: --")
        self.staff_service_detail_meta.setStyleSheet("border: none; background: transparent; font-size: 13px; color: #475569; font-weight: 700;")
        info_col.addWidget(self.staff_service_detail_name)
        info_col.addWidget(self.staff_service_detail_meta)
        profile.addWidget(self.staff_service_icon)
        profile.addLayout(info_col, 1)
        detail_layout.addLayout(profile)

        self.staff_service_detail_info = QtWidgets.QLabel("Giá dịch vụ: --\nThời gian: --\nTrạng thái: --")
        self.staff_service_detail_info.setWordWrap(True)
        self.staff_service_detail_info.setStyleSheet("border: none; background: transparent; color: #334155; font-size: 13px; font-weight: 800; line-height: 150%;")
        detail_layout.addWidget(self.staff_service_detail_info)
        self.staff_service_detail_description = QtWidgets.QLabel("Mô tả\nChưa có thông tin.")
        self.staff_service_detail_description.setWordWrap(True)
        self.staff_service_detail_description.setStyleSheet("border: none; background: transparent; color: #334155; font-size: 13px; font-weight: 700;")
        detail_layout.addWidget(self.staff_service_detail_description)
        self.staff_service_detail_process = QtWidgets.QLabel(
            "Quy trình thực hiện\n1. Đăng ký thông tin\n2. Khám lâm sàng\n3. Chỉ định cận lâm sàng (nếu cần)\n4. Bác sĩ tư vấn kết quả"
        )
        self.staff_service_detail_process.setWordWrap(True)
        self.staff_service_detail_process.setStyleSheet("border: none; background: transparent; color: #334155; font-size: 13px; font-weight: 700;")
        detail_layout.addWidget(self.staff_service_detail_process)
        self.staff_service_detail_note = QtWidgets.QLabel("Lưu ý\n- Mang theo giấy tờ tùy thân")
        self.staff_service_detail_note.setWordWrap(True)
        self.staff_service_detail_note.setStyleSheet("border: none; background: transparent; color: #334155; font-size: 13px; font-weight: 700;")
        detail_layout.addWidget(self.staff_service_detail_note)

        detail_actions = QtWidgets.QHBoxLayout()
        self.staff_service_edit_btn = QtWidgets.QPushButton("✎  Sửa dịch vụ")
        self.staff_service_disable_btn = QtWidgets.QPushButton("🗑  Ngưng áp dụng")
        self.staff_service_edit_btn.clicked.connect(self._show_staff_service_edit_dialog)
        self.staff_service_disable_btn.clicked.connect(self._handle_staff_service_disable)
        self.staff_service_edit_btn.setStyleSheet("background: #ffffff; color: #2563eb; border: 1px solid #bfdbfe; border-radius: 9px; padding: 11px; font-weight: 900;")
        self.staff_service_disable_btn.setStyleSheet("background: #fff1f2; color: #ef4444; border: 1px solid #fca5a5; border-radius: 9px; padding: 11px; font-weight: 900;")
        detail_actions.addWidget(self.staff_service_edit_btn)
        detail_actions.addWidget(self.staff_service_disable_btn)
        detail_layout.addLayout(detail_actions)

        related_title = QtWidgets.QLabel("Dịch vụ thường được chọn kèm")
        related_title.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 16px; font-weight: 900;")
        detail_layout.addWidget(related_title)
        self.staff_service_related_box = QtWidgets.QVBoxLayout()
        detail_layout.addLayout(self.staff_service_related_box)
        detail_layout.addStretch()

        self.staff_service_feedback = QtWidgets.QLabel("")
        self.staff_service_feedback.setWordWrap(True)
        self.staff_service_feedback.setStyleSheet("border: none; background: transparent; font-size: 13px; color: #0f766e; font-weight: 700;")
        detail_layout.addWidget(self.staff_service_feedback)

        body.addWidget(list_card, 7)
        body.addWidget(detail_card, 3)
        layout.addLayout(body, 1)

        self.staff_service_show_packages = False
        self._refresh_staff_service_lookup()
        return page

    def _build_staff_service_catalog(self):
        sample_services = [
            {"service_id": "sample-1", "service_name": "Khám tổng quát", "category": "Khám bệnh", "price": 300000, "duration": 30, "description": "Khám sức khỏe tổng quát, đánh giá các chỉ số cơ bản và tư vấn hướng điều trị.", "is_active": True},
            {"service_id": "sample-2", "service_name": "Khám tim mạch", "category": "Khám chuyên khoa", "price": 400000, "duration": 30, "description": "Khám chuyên khoa tim mạch, đo huyết áp, điện tim và tư vấn theo tình trạng bệnh.", "is_active": True},
            {"service_id": "sample-3", "service_name": "Khám nhi khoa", "category": "Khám chuyên khoa", "price": 350000, "duration": 25, "description": "Khám và tư vấn sức khỏe cho trẻ em.", "is_active": True},
            {"service_id": "sample-4", "service_name": "Khám tai mũi họng", "category": "Khám chuyên khoa", "price": 320000, "duration": 25, "description": "Khám tai mũi họng, nội soi khi cần và kê đơn điều trị.", "is_active": True},
            {"service_id": "sample-5", "service_name": "Khám răng hàm mặt", "category": "Khám chuyên khoa", "price": 250000, "duration": 20, "description": "Kiểm tra răng miệng, tư vấn chăm sóc và điều trị cơ bản.", "is_active": True},
            {"service_id": "sample-6", "service_name": "Siêu âm tổng quát", "category": "Chẩn đoán hình ảnh", "price": 450000, "duration": 20, "description": "Siêu âm ổ bụng tổng quát, hỗ trợ chẩn đoán nhanh.", "is_active": True},
            {"service_id": "sample-7", "service_name": "Siêu âm tim", "category": "Chẩn đoán hình ảnh", "price": 600000, "duration": 30, "description": "Siêu âm tim, đánh giá cấu trúc và chức năng tim.", "is_active": True},
            {"service_id": "sample-8", "service_name": "Xét nghiệm máu tổng quát", "category": "Xét nghiệm", "price": 180000, "duration": 15, "description": "Xét nghiệm công thức máu và các chỉ số cơ bản.", "is_active": True},
            {"service_id": "sample-9", "service_name": "Xét nghiệm đường huyết", "category": "Xét nghiệm", "price": 90000, "duration": 10, "description": "Kiểm tra đường huyết nhanh.", "is_active": True},
            {"service_id": "sample-10", "service_name": "X-quang phổi", "category": "Chẩn đoán hình ảnh", "price": 120000, "duration": 15, "description": "Chụp X-quang phổi hỗ trợ chẩn đoán hô hấp.", "is_active": False},
        ]
        sample_packages = [
            {"service_id": "package-1", "service_name": "Gói khám tổng quát", "category": "Gói khám", "price": 1200000, "duration": 90, "description": "Gói kiểm tra sức khỏe định kỳ gồm khám tổng quát, xét nghiệm máu và siêu âm.", "is_active": True, "is_package": True},
            {"service_id": "package-2", "service_name": "Gói khám doanh nghiệp", "category": "Gói khám", "price": 950000, "duration": 75, "description": "Gói khám sức khỏe cho nhân viên doanh nghiệp.", "is_active": True, "is_package": True},
            {"service_id": "package-3", "service_name": "Gói tim mạch nâng cao", "category": "Gói khám", "price": 1500000, "duration": 100, "description": "Gói khám chuyên sâu tim mạch kèm siêu âm tim và xét nghiệm cần thiết.", "is_active": True, "is_package": True},
        ]

        rows = []
        try:
            rows = ServiceController.get_all() or []
        except Exception:
            rows = []

        catalog = []
        seen_names = set()
        for row in rows:
            service = dict(row)
            name = str(service.get("service_name") or service.get("name") or "").strip()
            if not name:
                continue
            service["service_name"] = self._staff_display_text(name)
            service.setdefault("category", self._staff_service_category(service))
            service.setdefault("duration", self._staff_service_duration(service))
            service.setdefault("description", self._staff_service_description(service))
            service["is_package"] = "gói" in service["service_name"].lower()
            catalog.append(service)
            seen_names.add(service["service_name"].lower())

        for item in sample_services + sample_packages:
            if item["service_name"].lower() not in seen_names:
                catalog.append(dict(item))
        return catalog

    def _build_staff_service_kpi_card(self, icon, title, value, note, bg_color, fg_color):
        card = QtWidgets.QFrame()
        card.setMinimumHeight(92)
        card.setStyleSheet("background: #ffffff; border: 1px solid #e7edf5; border-radius: 14px;")
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(12)
        icon_label = QtWidgets.QLabel(icon)
        icon_label.setFixedSize(44, 44)
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"background: {bg_color}; color: {fg_color}; border: none; border-radius: 12px; font-size: 20px;")
        text_col = QtWidgets.QVBoxLayout()
        text_col.setSpacing(3)
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("border: none; background: transparent; color: #64748b; font-size: 12px; font-weight: 800;")
        value_label = QtWidgets.QLabel(str(value))
        value_label.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 21px; font-weight: 900;")
        note_label = QtWidgets.QLabel(note)
        note_label.setStyleSheet("border: none; background: transparent; color: #94a3b8; font-size: 11px; font-weight: 700;")
        text_col.addWidget(title_label)
        text_col.addWidget(value_label)
        text_col.addWidget(note_label)
        layout.addWidget(icon_label)
        layout.addLayout(text_col, 1)
        return card

    @staticmethod
    def _format_staff_money(value):
        try:
            amount = int(float(value or 0))
        except (TypeError, ValueError):
            amount = 0
        return f"{amount:,}".replace(",", ".") + " đ"

    def _staff_service_category(self, service):
        category = str(service.get("category") or service.get("service_type") or "").strip()
        if category:
            return self._staff_display_text(category)
        name = str(service.get("service_name") or service.get("name") or "").lower()
        if "xét nghiệm" in name or "xet nghiem" in name:
            return "Xét nghiệm"
        if "siêu âm" in name or "x-quang" in name or "x quang" in name:
            return "Chẩn đoán hình ảnh"
        if "tiêm" in name:
            return "Tiêm chủng"
        if "gói" in name:
            return "Gói khám"
        if any(token in name for token in ["tim", "nhi", "tai", "răng", "rang"]):
            return "Khám chuyên khoa"
        return "Khám bệnh"

    def _staff_service_duration(self, service):
        duration = service.get("duration") or service.get("duration_minutes")
        try:
            return int(duration)
        except (TypeError, ValueError):
            pass
        category = self._staff_service_category(service)
        if category == "Xét nghiệm":
            return 15
        if category == "Chẩn đoán hình ảnh":
            return 20
        if category == "Gói khám":
            return 90
        return 30

    def _staff_service_description(self, service):
        description = str(service.get("description") or "").strip()
        if description:
            return self._staff_display_text(description)
        return "Dịch vụ được áp dụng tại CarePlus, hỗ trợ tiếp nhận và điều phối khám nhanh."

    def _staff_service_is_active(self, service):
        status = str(service.get("status") or "").lower().strip()
        if status in {"inactive", "disabled", "ngưng áp dụng", "ngung ap dung"}:
            return False
        if "is_active" in service:
            return bool(service.get("is_active"))
        return True

    def _staff_service_status_text(self, service):
        return "Đang áp dụng" if self._staff_service_is_active(service) else "Ngưng áp dụng"

    def _set_staff_service_mode(self, show_packages):
        self.staff_service_show_packages = bool(show_packages)
        self.staff_service_tab_service.setChecked(not show_packages)
        self.staff_service_tab_package.setChecked(bool(show_packages))
        self._refresh_staff_service_lookup()

    def _refresh_staff_service_lookup(self):
        if not hasattr(self, "staff_service_table"):
            return
        if not getattr(self, "staff_service_rows", None):
            self.staff_service_rows = self._build_staff_service_catalog()

        keyword = str(self.staff_service_search_input.text() or "").strip().lower()
        category_filter = str(self.staff_service_category_combo.currentText() or "")
        status_filter = str(self.staff_service_status_combo.currentText() or "")
        show_packages = bool(getattr(self, "staff_service_show_packages", False))

        filtered = []
        for service in self.staff_service_rows:
            is_package = bool(service.get("is_package"))
            if is_package != show_packages:
                continue
            name = str(service.get("service_name") or service.get("name") or "")
            category = self._staff_service_category(service)
            status_text = self._staff_service_status_text(service)
            haystack = f"{name} {category} {status_text}".lower()
            if keyword and keyword not in haystack:
                continue
            if not category_filter.startswith("Tất cả") and category != category_filter:
                continue
            if not status_filter.startswith("Tất cả") and status_text != status_filter:
                continue
            filtered.append(service)

        self.staff_service_filtered_rows = filtered
        self.staff_service_table.blockSignals(True)
        self.staff_service_table.setRowCount(len(filtered))
        for row, service in enumerate(filtered):
            name = self._staff_display_text(service.get("service_name") or service.get("name") or "")
            category = self._staff_service_category(service)
            price = self._format_staff_money(service.get("price")).replace(" đ", "")
            duration = f"{self._staff_service_duration(service)} phút"
            values = [str(row + 1), name, category, price, duration]
            for col, value in enumerate(values):
                item = QtWidgets.QTableWidgetItem(value)
                align = QtCore.Qt.AlignmentFlag.AlignVCenter
                if col == 0:
                    align |= QtCore.Qt.AlignmentFlag.AlignCenter
                else:
                    align |= QtCore.Qt.AlignmentFlag.AlignLeft
                item.setTextAlignment(align)
                if col == 1:
                    item.setData(QtCore.Qt.ItemDataRole.UserRole, row)
                self.staff_service_table.setItem(row, col, item)
            self.staff_service_table.setCellWidget(row, 5, self._build_staff_service_status_badge(service))
            self.staff_service_table.setCellWidget(row, 6, self._build_staff_service_actions_widget(row))
        self.staff_service_table.blockSignals(False)

        title = "Danh sách gói khám" if show_packages else "Danh sách dịch vụ"
        self.staff_service_list_title.setText(f"{title} ({len(filtered)})")
        self.staff_service_lookup_empty.setText(f"Hiển thị {len(filtered)} bản ghi")
        if filtered:
            self.staff_service_table.selectRow(0)
            self._update_staff_service_detail(filtered[0])
        else:
            self._reset_staff_service_detail()

    def _build_staff_service_status_badge(self, service):
        active = self._staff_service_is_active(service)
        label = QtWidgets.QLabel(self._staff_service_status_text(service))
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setMinimumWidth(108)
        label.setStyleSheet(
            "background: #dcfce7; color: #16a34a; border: none; border-radius: 12px; padding: 5px 10px; font-size: 12px; font-weight: 900;"
            if active else
            "background: #fee2e2; color: #ef4444; border: none; border-radius: 12px; padding: 5px 10px; font-size: 12px; font-weight: 900;"
        )
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(2, 4, 2, 4)
        layout.addWidget(label)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        return wrapper

    def _build_staff_service_actions_widget(self, row):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        actions = [("👁", "Xem chi tiết"), ("✎", "Sửa dịch vụ"), ("⋮", "Thêm thao tác")]
        for icon, tooltip in actions:
            btn = QtWidgets.QPushButton(icon)
            btn.setToolTip(tooltip)
            btn.setFixedSize(32, 30)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(
                "QPushButton { background: #ffffff; border: 1px solid #dbe4ee; border-radius: 8px; color: #475569; font-size: 13px; font-weight: 900; }"
                "QPushButton:hover { border-color: #13a66b; color: #13a66b; }"
            )
            if tooltip.startswith("Xem"):
                btn.clicked.connect(lambda _, r=row: self._select_staff_service_row(r))
            elif tooltip.startswith("Sửa"):
                btn.clicked.connect(lambda _, r=row: self._edit_staff_service_row(r))
            else:
                btn.clicked.connect(lambda _, r=row: self._select_staff_service_row(r))
            layout.addWidget(btn)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        return wrapper

    def _select_staff_service_row(self, row):
        if 0 <= row < len(getattr(self, "staff_service_filtered_rows", [])):
            self.staff_service_table.selectRow(row)
            self._update_staff_service_detail(self.staff_service_filtered_rows[row])

    def _edit_staff_service_row(self, row):
        self._select_staff_service_row(row)
        self._show_staff_service_edit_dialog()

    def _handle_staff_service_selection(self):
        if not hasattr(self, "staff_service_table"):
            return
        row = self.staff_service_table.currentRow()
        if row < 0 or row >= len(getattr(self, "staff_service_filtered_rows", [])):
            return
        self._update_staff_service_detail(self.staff_service_filtered_rows[row])

    def _update_staff_service_detail(self, service):
        self.staff_service_selected = service
        name = self._staff_display_text(service.get("service_name") or service.get("name") or "")
        category = self._staff_service_category(service)
        self.staff_service_detail_name.setText(name)
        self.staff_service_detail_meta.setText(f"Danh mục: {category}")
        self.staff_service_icon.setText("💼" if service.get("is_package") else "✚")
        self.staff_service_detail_info.setText(
            f"Giá dịch vụ: {self._format_staff_money(service.get('price'))}\n"
            f"Thời gian: {self._staff_service_duration(service)} phút\n"
            f"Trạng thái: {self._staff_service_status_text(service)}"
        )
        self.staff_service_detail_description.setText(f"Mô tả\n{self._staff_service_description(service)}")
        self.staff_service_detail_process.setText(
            "Quy trình thực hiện\n"
            "1. Đăng ký thông tin tại quầy\n"
            "2. Điều dưỡng hướng dẫn vào phòng khám\n"
            "3. Thực hiện khám hoặc chỉ định cận lâm sàng\n"
            "4. Bác sĩ tư vấn kết quả và hướng xử lý"
        )
        self.staff_service_detail_note.setText("Lưu ý\n- Mang theo giấy tờ tùy thân\n- Đến trước giờ hẹn 10 phút")
        self.staff_service_disable_btn.setText("🗑  Ngưng áp dụng" if self._staff_service_is_active(service) else "↺  Áp dụng lại")

        while self.staff_service_related_box.count():
            item = self.staff_service_related_box.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        related = [s for s in self.staff_service_rows if s is not service and not s.get("is_package") and self._staff_service_is_active(s)][:3]
        for row in related:
            self.staff_service_related_box.addWidget(self._build_staff_related_service_row(row))

    def _reset_staff_service_detail(self):
        self.staff_service_selected = None
        self.staff_service_detail_name.setText("Chưa chọn dịch vụ")
        self.staff_service_detail_meta.setText("Danh mục: --")
        self.staff_service_detail_info.setText("Giá dịch vụ: --\nThời gian: --\nTrạng thái: --")
        self.staff_service_detail_description.setText("Mô tả\nChưa có thông tin.")
        self.staff_service_feedback.setText("")

    def _build_staff_related_service_row(self, service):
        row = QtWidgets.QFrame()
        row.setStyleSheet("background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px;")
        layout = QtWidgets.QHBoxLayout(row)
        layout.setContentsMargins(10, 8, 10, 8)
        name = QtWidgets.QLabel(self._staff_display_text(service.get("service_name") or service.get("name") or ""))
        name.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 12px; font-weight: 800;")
        price = QtWidgets.QLabel(self._format_staff_money(service.get("price")))
        price.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        price.setStyleSheet("border: none; background: transparent; color: #13a66b; font-size: 12px; font-weight: 900;")
        layout.addWidget(name, 1)
        layout.addWidget(price)
        return row

    def _show_staff_service_add_dialog(self):
        self._open_staff_service_editor()

    def _show_staff_service_edit_dialog(self):
        if not getattr(self, "staff_service_selected", None):
            self._set_staff_service_feedback("Vui lòng chọn dịch vụ cần sửa.", is_error=True)
            return
        self._open_staff_service_editor(self.staff_service_selected)

    def _open_staff_service_editor(self, service=None):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Sửa dịch vụ" if service else "Thêm dịch vụ")
        dialog.setMinimumWidth(460)
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        name_input = QtWidgets.QLineEdit()
        name_input.setPlaceholderText("Tên dịch vụ")
        name_input.setText(str((service or {}).get("service_name") or (service or {}).get("name") or ""))
        price_input = QtWidgets.QDoubleSpinBox()
        price_input.setRange(0, 999999999)
        price_input.setDecimals(0)
        price_input.setSingleStep(50000)
        price_input.setValue(float((service or {}).get("price") or 0))
        category_combo = QtWidgets.QComboBox()
        category_combo.addItems(["Khám bệnh", "Khám chuyên khoa", "Xét nghiệm", "Chẩn đoán hình ảnh", "Tiêm chủng", "Tư vấn", "Gói khám"])
        category_index = category_combo.findText(self._staff_service_category(service or {}))
        if category_index >= 0:
            category_combo.setCurrentIndex(category_index)
        duration_input = QtWidgets.QSpinBox()
        duration_input.setRange(5, 240)
        duration_input.setSuffix(" phút")
        duration_input.setValue(self._staff_service_duration(service or {}))
        desc_input = QtWidgets.QTextEdit()
        desc_input.setPlaceholderText("Mô tả dịch vụ")
        desc_input.setPlainText(self._staff_service_description(service or {}) if service else "")

        for label_text, widget in [
            ("Tên dịch vụ", name_input),
            ("Danh mục", category_combo),
            ("Giá", price_input),
            ("Thời gian", duration_input),
            ("Mô tả", desc_input),
        ]:
            label = QtWidgets.QLabel(label_text)
            label.setStyleSheet("font-weight: 800; color: #334155;")
            layout.addWidget(label)
            widget.setStyleSheet(self._intake_input_style())
            layout.addWidget(widget)

        actions = QtWidgets.QHBoxLayout()
        cancel_btn = QtWidgets.QPushButton("Hủy")
        save_btn = QtWidgets.QPushButton("Lưu")
        cancel_btn.clicked.connect(dialog.reject)
        save_btn.setStyleSheet(self._intake_primary_button_style())
        cancel_btn.setStyleSheet("background: #ffffff; color: #475569; border: 1px solid #dbe4ee; border-radius: 8px; padding: 9px 14px; font-weight: 800;")
        actions.addStretch()
        actions.addWidget(cancel_btn)
        actions.addWidget(save_btn)
        layout.addLayout(actions)

        def save_service():
            name = name_input.text().strip()
            if not name:
                self._set_staff_service_feedback("Tên dịch vụ không được để trống.", is_error=True)
                return
            data = {
                "name": name,
                "price": float(price_input.value()),
                "description": desc_input.toPlainText().strip(),
                "category": category_combo.currentText(),
                "duration": duration_input.value(),
            }
            try:
                if service and isinstance(service.get("service_id"), int):
                    ServiceController.update(service["service_id"], data)
                elif service and str(service.get("service_id", "")).startswith(("sample-", "package-")):
                    service.update({"service_name": data["name"], "price": data["price"], "description": data["description"], "category": data["category"], "duration": data["duration"]})
                else:
                    ServiceController.create(data)
                    self.staff_service_rows = self._build_staff_service_catalog()
            except Exception as exc:
                if service:
                    service.update({"service_name": data["name"], "price": data["price"], "description": data["description"], "category": data["category"], "duration": data["duration"]})
                else:
                    self.staff_service_rows.insert(0, {"service_id": f"local-{len(self.staff_service_rows) + 1}", "service_name": data["name"], "price": data["price"], "description": data["description"], "category": data["category"], "duration": data["duration"], "is_active": True, "is_package": data["category"] == "Gói khám"})
                self._set_staff_service_feedback(f"Lưu trên giao diện vì chưa ghi được CSDL: {exc}", is_error=True)
            dialog.accept()
            self._refresh_staff_service_lookup()

        save_btn.clicked.connect(save_service)
        dialog.exec()

    def _handle_staff_service_disable(self):
        service = getattr(self, "staff_service_selected", None)
        if not service:
            self._set_staff_service_feedback("Vui lòng chọn dịch vụ trước.", is_error=True)
            return
        new_state = not self._staff_service_is_active(service)
        service_id = service.get("service_id")
        try:
            if isinstance(service_id, int):
                from database.db import execute
                execute("UPDATE Services SET is_active=? WHERE service_id=?", (1 if new_state else 0, service_id))
            service["is_active"] = new_state
            self._set_staff_service_feedback("Đã cập nhật trạng thái dịch vụ.", is_error=False)
        except Exception as exc:
            service["is_active"] = new_state
            self._set_staff_service_feedback(f"Đã cập nhật tạm trên giao diện: {exc}", is_error=True)
        self._refresh_staff_service_lookup()

    @staticmethod
    def _staff_display_text(value):
        text = str(value or "")
        replacements = {
            "Nguy?n Van A": "Nguyễn Văn A",
            "Tr?n Th? B": "Trần Thị B",
            "Bác si": "Bác sĩ",
            "Xét nghi?m": "Xét nghiệm",
            "Khám t?ng quát": "Khám tổng quát",
            "N?i khoa": "Nội khoa",
            "Ngo?i khoa": "Ngoại khoa",
            "ChÆ°a cÃ³ SÄT": "Chưa có SĐT",
        }
        for source, target in replacements.items():
            text = text.replace(source, target)
        return text

    @staticmethod
    def _staff_status_label(status):
        labels = {
            "pending": "Đang chờ",
            "confirmed": "Đã xác nhận",
            "in_progress": "Đang khám",
            "done": "Đã hoàn tất",
            "cancelled": "Đã hủy",
        }
        return labels.get(str(status or "").lower().strip(), status or "-")

    def _create_status_badge_widget(self, status):
        status_key = str(status or "pending").lower().strip()
        bg_color, fg_color = self._get_status_badge_style(status_key)
        badge = QtWidgets.QLabel(self._staff_status_label(status_key))
        badge.setMinimumWidth(104)
        badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            f"background: {bg_color}; color: {fg_color}; border: none; border-radius: 11px;"
            " padding: 5px 12px; font-size: 12px; font-weight: 900;"
        )
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.addWidget(badge)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        return wrapper

    def _create_appointment_actions_widget(self, row):
        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        view_btn = QtWidgets.QPushButton("👁")
        view_btn.setToolTip("Xem chi tiết")
        menu_btn = QtWidgets.QPushButton("⋮")
        menu_btn.setToolTip("Tùy chọn")
        for btn in [view_btn, menu_btn]:
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setFixedSize(34, 30)
            btn.setStyleSheet(
                "QPushButton {border: 1px solid #cbd5e1; border-radius: 8px; background: #ffffff;"
                " color: #334155; font-size: 13px; font-weight: 900;}"
                "QPushButton:hover {border-color: #1A9B6C; color: #1A9B6C;}"
            )
        view_btn.clicked.connect(lambda _, r=row: self._handle_staff_appt_quick_view(r))
        menu_btn.clicked.connect(lambda _, r=row, b=menu_btn: self._show_staff_appt_actions_menu(r, b))
        layout.addWidget(view_btn)
        layout.addWidget(menu_btn)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        return container

    def _set_staff_appointment_detail(self, appt):
        service_text = self._staff_display_text(self._extract_service_name_from_note(str(appt.get("note") or "")) or "-")
        status = str(appt.get("status") or "")
        patient_name = self._staff_display_text(str(appt.get("patient_name") or "Chưa có tên"))
        appointment_date = self._staff_display_text(str(appt.get("appointment_date") or ""))
        doctor_name = self._staff_display_text(str(appt.get("doctor_name") or ""))
        phone = self._staff_display_text(str(appt.get("patient_phone") or "Chưa có SĐT"))
        note = self._staff_display_text(str(appt.get("note") or "Không có"))
        self.staff_appt_detail_patient.setText(
            f"👤  {patient_name}\n"
            f"BN #{appt.get('patient_id', '')}  •  {phone}"
        )
        self.staff_appt_detail_info.setText(
            f"Thời gian hẹn: {appointment_date}\n"
            f"Dịch vụ khám: {service_text}\n"
            f"Bác sĩ: {doctor_name}\n"
            f"Phòng khám: Phòng khám 1\n"
            f"Trạng thái: {self._staff_status_label(status)}\n"
            f"Ghi chú: {note}"
        )
        date_part = appointment_date[:10] if appointment_date else "Hôm nay"
        self.staff_appt_detail_timeline.setText(
            f"● {date_part} 07:30\n  Nhân viên tạo lịch hẹn\n\n"
            f"● {date_part} 07:35\n  Bệnh nhân xác nhận lịch hẹn\n\n"
            f"● {date_part} 07:40\n  Nhân viên xác nhận lịch hẹn"
        )

    def _nav_button_style(self, is_active=False):
        base = (
            "QPushButton { border: none; text-align: left; padding: 14px 20px; border-radius: 10px; "
            "font-size: 15px; color: #111827; font-weight: 700; }"
        )
        if is_active:
            return base + "QPushButton { background-color: #e3f5ef; color: #0f9f6e; font-weight: 900; }"
        return base + "QPushButton:hover { background-color: #f1f5f9; }"

    def switch_page(self, index):
        if index < 0 or index >= len(self.nav_buttons):
            return

        if hasattr(self, "topbar"):
            self.topbar.setVisible(index not in {1, 2, 3, 4, 5})

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
