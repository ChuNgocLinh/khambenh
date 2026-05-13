import math
import re
from pathlib import Path
from typing import Any

from PyQt6 import QtWidgets, QtCore, QtGui
from controllers.patient_controller import PatientController
from controllers.appointment_controller import AppointmentController
from controllers.doctor_controller import DoctorController
from controllers.service_controller import ServiceController
from controllers.payment_controller import PaymentController
from controllers.report_controller import ReportController
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
        self.staff_billing_filtered_rows = []
        self.staff_billing_selected_id = None
        self.staff_billing_selected_payment = None
        self.staff_billing_selected_status = ""
        self.staff_billing_action_in_progress = False
        self.staff_billing_status_filter = "__all__"
        self.staff_billing_status_filters = ["__all__", "unpaid", "paid", "cancelled", "refunded"]
        self.staff_service_source_rows = []
        self.staff_service_rows = []
        self.staff_service_package_rows = []
        self.staff_service_filtered_rows = []
        self.staff_service_selected = None
        self.staff_service_active_tab = "service"
        self.staff_notification_rows = []
        self.staff_notification_filtered_rows = []
        self.staff_notification_active_tab = "all"
        self.staff_notification_priority_filter = "__all__"
        self.staff_notification_selected_id = None
        self.staff_report_metric_mode = "active_tab"
        self.shared_selected_patient_id = None
        self.shared_selected_appointment_id = None
        self.shared_selected_service_name = ""
        self._shared_appt_context_patient_id = None
        self._shared_appt_context_service_name = ""
        self._shared_billing_context_patient_id = None
        self._shared_billing_context_appointment_id = None
        self._shared_billing_context_service_name = ""
        self._shared_billing_context_amount = None
        self._staff_settings_options_sync_in_progress = False

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
        self.dashboard_welcome_label = QtWidgets.QLabel(f"Xin chào, {self.username}!")
        self.dashboard_welcome_label.setStyleSheet("font-size: 19px; font-weight: 900; color: #0f172a;")
        role_lbl = QtWidgets.QLabel("Nhân viên lễ tân")
        role_lbl.setStyleSheet("font-size: 13px; color: #64748b; font-weight: 700;")
        title_col.addWidget(self.dashboard_welcome_label)
        title_col.addWidget(role_lbl)

        bell = QtWidgets.QLabel("🔔")
        bell.setFixedSize(34, 34)
        bell.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        bell.setStyleSheet("font-size: 20px; color: #64748b;")
        avatar = QtWidgets.QLabel("👤")
        avatar.setFixedSize(38, 38)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("background: #eaf2ff; border-radius: 19px; font-size: 20px;")
        self.dashboard_user_label = QtWidgets.QLabel(f"{self.username}  ▾")
        self.dashboard_user_label.setStyleSheet("font-size: 13px; color: #0f172a; font-weight: 900;")

        topbar_layout.addLayout(title_col)
        topbar_layout.addStretch()
        topbar_layout.addWidget(bell)
        topbar_layout.addWidget(avatar)
        topbar_layout.addWidget(self.dashboard_user_label)
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
        page.setStyleSheet("background: #f8fbff; border: none;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        heading = QtWidgets.QLabel("Thông báo vận hành")
        heading.setStyleSheet("font-size: 24px; color: #0f172a; font-weight: 900;")
        sub = QtWidgets.QLabel(
            "Theo dõi cảnh báo từ lịch hẹn và thanh toán, ưu tiên thông báo chưa đọc và mở nhanh nguồn dữ liệu liên quan."
        )
        sub.setStyleSheet("font-size: 13px; color: #64748b;")
        sub.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(sub)

        kpi_row = QtWidgets.QHBoxLayout()
        kpi_row.setSpacing(12)
        self.staff_notification_kpi_total = self._build_kpi_card("Tổng thông báo", "0", "Toàn bộ feed hiện tại", "#2563eb", "#eaf2ff", "🔔")
        self.staff_notification_kpi_appointment = self._build_kpi_card("Lịch hẹn", "0", "Cập nhật từ Appointments", "#0ea5e9", "#e0f2fe", "📅")
        self.staff_notification_kpi_payment = self._build_kpi_card("Thanh toán", "0", "Nhắc thu tiền chưa paid", "#f97316", "#fff3e4", "💳")
        self.staff_notification_kpi_system = self._build_kpi_card("Hệ thống", "0", "Thông báo fallback vận hành", "#7c3aed", "#f3e8ff", "⚙")
        kpi_row.addWidget(self.staff_notification_kpi_total)
        kpi_row.addWidget(self.staff_notification_kpi_appointment)
        kpi_row.addWidget(self.staff_notification_kpi_payment)
        kpi_row.addWidget(self.staff_notification_kpi_system)
        layout.addLayout(kpi_row)

        self.staff_notification_tab_buttons = {}
        tab_row = QtWidgets.QHBoxLayout()
        tab_row.setSpacing(8)
        tab_specs = [
            ("all", "Tất cả"),
            ("unread", "Chưa đọc"),
            ("appointment", "Lịch hẹn"),
            ("payment", "Thanh toán"),
            ("system", "Hệ thống"),
        ]
        for tab_key, tab_label in tab_specs:
            tab_btn = QtWidgets.QPushButton(tab_label)
            tab_btn.setCheckable(True)
            tab_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            tab_btn.clicked.connect(lambda checked=False, key=tab_key: self._set_staff_notification_tab(key))
            self.staff_notification_tab_buttons[tab_key] = tab_btn
            tab_row.addWidget(tab_btn)
        tab_row.addStretch()

        refresh_btn = QtWidgets.QPushButton("🔄 Làm mới")
        refresh_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        refresh_btn.setStyleSheet(
            "QPushButton { background: #0ea5e9; color: white; border: none; border-radius: 8px; padding: 8px 12px; font-weight: 800; }"
            "QPushButton:hover { background: #0284c7; }"
        )
        refresh_btn.clicked.connect(self._refresh_staff_notifications)
        tab_row.addWidget(refresh_btn)
        layout.addLayout(tab_row)
        self._refresh_staff_notification_tab_styles()

        filter_card = self._build_section_card("Tìm kiếm & lọc")
        filter_row = QtWidgets.QHBoxLayout()
        filter_row.setSpacing(10)

        self.staff_notification_search_input = QtWidgets.QLineEdit()
        self.staff_notification_search_input.setPlaceholderText("Tìm theo nội dung, mã lịch hẹn/hóa đơn, bệnh nhân...")
        self.staff_notification_search_input.setMinimumHeight(40)

        self.staff_notification_priority_combo = QtWidgets.QComboBox()
        self.staff_notification_priority_combo.setMinimumHeight(40)
        self.staff_notification_priority_combo.addItem("Mọi mức độ", "__all__")
        self.staff_notification_priority_combo.addItem("Mới", "new")
        self.staff_notification_priority_combo.addItem("Theo dõi", "watch")
        self.staff_notification_priority_combo.addItem("Cần xử lý", "urgent")

        search_btn = QtWidgets.QPushButton("Lọc")
        search_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        search_btn.setMinimumHeight(40)
        search_btn.setStyleSheet(
            "QPushButton { background: #2563eb; color: white; border: none; border-radius: 8px; padding: 8px 14px; font-weight: 700; }"
            "QPushButton:hover { background: #1d4ed8; }"
        )
        search_btn.clicked.connect(self._apply_staff_notification_filters)

        clear_btn = QtWidgets.QPushButton("Xóa lọc")
        clear_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        clear_btn.setMinimumHeight(40)
        clear_btn.clicked.connect(self._clear_staff_notification_filters)

        filter_row.addWidget(self.staff_notification_search_input, 1)
        filter_row.addWidget(self.staff_notification_priority_combo)
        filter_row.addWidget(search_btn)
        filter_row.addWidget(clear_btn)
        filter_card.layout().addLayout(filter_row)
        layout.addWidget(filter_card)

        self.staff_notification_feedback = QtWidgets.QLabel("Danh sách thông báo sẽ hiển thị tại đây.")
        self.staff_notification_feedback.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 600;")
        layout.addWidget(self.staff_notification_feedback)

        content_row = QtWidgets.QHBoxLayout()
        content_row.setSpacing(18)

        list_card = self._build_section_card("Danh sách thông báo")
        self.staff_notification_table_summary = QtWidgets.QLabel(
            "Chọn một dòng để xem chi tiết và thao tác nhanh ở panel bên phải."
        )
        self.staff_notification_table_summary.setWordWrap(True)
        self.staff_notification_table_summary.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        list_card.layout().addWidget(self.staff_notification_table_summary)

        self.staff_notification_table = QtWidgets.QTableWidget(0, 5)
        self.staff_notification_table.setHorizontalHeaderLabels(["Loại", "Nội dung", "Thời điểm", "Mức độ", "Đọc"])
        self.staff_notification_table.verticalHeader().setVisible(False)
        self.staff_notification_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.staff_notification_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.staff_notification_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_notification_table.setShowGrid(False)
        self.staff_notification_table.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.staff_notification_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staff_notification_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_notification_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_notification_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_notification_table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_notification_table.setMinimumHeight(360)
        self.staff_notification_table.itemSelectionChanged.connect(self._handle_staff_notification_selection)
        self.staff_notification_table.setStyleSheet(
            "QTableWidget { border: 1px solid #e7edf5; border-radius: 12px; background: #ffffff; }"
            "QHeaderView::section { background: #f8fafc; color: #1f2937; font-size: 12px; font-weight: 800; border: none; padding: 10px; }"
            "QTableWidget::item { border-bottom: 1px solid #edf2f7; padding: 8px; color: #0f172a; font-weight: 600; }"
            "QTableWidget::item:selected { background: #ecfeff; color: #0f172a; }"
        )
        list_card.layout().addWidget(self.staff_notification_table)

        self.staff_notification_empty_state = QtWidgets.QLabel("Không có thông báo khớp bộ lọc hiện tại.")
        self.staff_notification_empty_state.setWordWrap(True)
        self.staff_notification_empty_state.setStyleSheet(
            "background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 10px; padding: 10px 12px; font-size: 12px; color: #64748b; font-weight: 700;"
        )
        list_card.layout().addWidget(self.staff_notification_empty_state)

        detail_card = self._build_section_card("Chi tiết thông báo")
        self.staff_notification_detail_placeholder = QtWidgets.QLabel(
            "Chọn thông báo trong danh sách để xem nội dung, nguồn dữ liệu và thao tác xử lý."
        )
        self.staff_notification_detail_placeholder.setWordWrap(True)
        self.staff_notification_detail_placeholder.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        detail_card.layout().addWidget(self.staff_notification_detail_placeholder)

        self.staff_notification_detail_type = QtWidgets.QLabel("Loại: -")
        self.staff_notification_detail_priority = QtWidgets.QLabel("Mức độ: -")
        self.staff_notification_detail_time = QtWidgets.QLabel("Thời điểm: -")
        self.staff_notification_detail_source = QtWidgets.QLabel("Nguồn dữ liệu: -")
        self.staff_notification_detail_message = QtWidgets.QLabel("Nội dung: -")
        self.staff_notification_detail_message.setWordWrap(True)
        for detail_label in [
            self.staff_notification_detail_type,
            self.staff_notification_detail_priority,
            self.staff_notification_detail_time,
            self.staff_notification_detail_source,
            self.staff_notification_detail_message,
        ]:
            detail_label.setStyleSheet("font-size: 12px; color: #334155; font-weight: 700;")
            detail_card.layout().addWidget(detail_label)

        detail_actions = QtWidgets.QHBoxLayout()
        detail_actions.setSpacing(8)
        self.staff_notification_open_source_btn = QtWidgets.QPushButton("🔎 Đi tới nguồn dữ liệu")
        self.staff_notification_open_source_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.staff_notification_open_source_btn.setStyleSheet(
            "QPushButton { padding: 8px 10px; border: 1px solid #cbd5e1; border-radius: 8px; background: #ffffff; font-size: 11px; font-weight: 800; color: #334155; }"
            "QPushButton:hover { border-color: #94a3b8; }"
            "QPushButton:disabled { background: #f1f5f9; color: #94a3b8; border-color: #e2e8f0; }"
        )
        self.staff_notification_open_source_btn.clicked.connect(self._handle_staff_notification_open_source)

        self.staff_notification_mark_read_btn = QtWidgets.QPushButton("✅ Đánh dấu đã đọc")
        self.staff_notification_mark_read_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.staff_notification_mark_read_btn.setStyleSheet(
            "QPushButton { padding: 8px 10px; border: 1px solid #16a34a; border-radius: 8px; background: #f0fdf4; font-size: 11px; font-weight: 800; color: #166534; }"
            "QPushButton:hover { background: #dcfce7; }"
            "QPushButton:disabled { background: #f1f5f9; color: #94a3b8; border-color: #e2e8f0; }"
        )
        self.staff_notification_mark_read_btn.clicked.connect(self._mark_notification_as_handled)

        detail_actions.addWidget(self.staff_notification_open_source_btn)
        detail_actions.addWidget(self.staff_notification_mark_read_btn)
        detail_card.layout().addLayout(detail_actions)
        detail_card.layout().addStretch()

        content_row.addWidget(list_card, 64)
        content_row.addWidget(detail_card, 36)
        layout.addLayout(content_row, 1)

        self._update_staff_notification_detail(None)

        self._refresh_staff_notifications()
        return page

    def _build_staff_reports_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: #f8fbff; border: none;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        heading = QtWidgets.QLabel("Báo cáo vận hành")
        heading.setStyleSheet("font-size: 24px; color: #0f172a; font-weight: 900;")
        sub = QtWidgets.QLabel(
            "Theo dõi nhanh dữ liệu quầy lễ tân theo từng nhóm báo cáo. Biểu đồ đang dùng dạng placeholder/tóm tắt để đảm bảo trung thực với dữ liệu hiện có."
        )
        sub.setStyleSheet("font-size: 13px; color: #64748b;")
        sub.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(sub)

        self.staff_report_tab_buttons = {}
        self.staff_report_active_tab = "overview"
        tab_row = QtWidgets.QHBoxLayout()
        tab_row.setSpacing(8)
        tab_specs = [
            ("overview", "Tổng quan"),
            ("revenue", "Doanh thu"),
            ("appointments", "Lịch hẹn"),
            ("patients", "Bệnh nhân"),
            ("staff", "Nhân viên"),
            ("services", "Dịch vụ"),
        ]
        for tab_key, tab_label in tab_specs:
            tab_btn = QtWidgets.QPushButton(tab_label)
            tab_btn.setCheckable(True)
            tab_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            tab_btn.clicked.connect(lambda checked=False, key=tab_key: self._set_staff_report_tab(key))
            self.staff_report_tab_buttons[tab_key] = tab_btn
            tab_row.addWidget(tab_btn)
        tab_row.addStretch()
        layout.addLayout(tab_row)
        self._refresh_staff_report_tab_styles()

        filter_card = self._build_section_card("Bộ lọc báo cáo")
        filter_row = QtWidgets.QHBoxLayout()
        filter_row.setSpacing(10)

        self.staff_report_period_combo = QtWidgets.QComboBox()
        self.staff_report_period_combo.setMinimumHeight(40)
        self.staff_report_period_combo.addItem("Hôm nay", "today")
        self.staff_report_period_combo.addItem("7 ngày gần nhất", "7d")
        self.staff_report_period_combo.addItem("30 ngày gần nhất", "30d")
        self.staff_report_period_combo.addItem("Tất cả dữ liệu", "all")

        self.staff_report_doctor_combo = QtWidgets.QComboBox()
        self.staff_report_doctor_combo.setMinimumHeight(40)
        self.staff_report_doctor_combo.addItem("Tất cả bác sĩ", "__all__")

        self.staff_report_metric_combo = QtWidgets.QComboBox()
        self.staff_report_metric_combo.setMinimumHeight(40)
        self.staff_report_metric_combo.addItem("Theo tab đang chọn", "active_tab")
        self.staff_report_metric_combo.addItem("Ưu tiên doanh thu", "revenue")
        self.staff_report_metric_combo.addItem("Ưu tiên lịch hẹn", "appointments")
        self.staff_report_metric_combo.addItem("Ưu tiên bệnh nhân", "patients")

        filter_apply_btn = QtWidgets.QPushButton("Áp dụng")
        filter_apply_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        filter_apply_btn.setMinimumHeight(40)
        filter_apply_btn.setStyleSheet(
            "QPushButton { background: #2563eb; color: white; border: none; border-radius: 8px; padding: 8px 14px; font-weight: 700; }"
            "QPushButton:hover { background: #1d4ed8; }"
        )
        filter_apply_btn.clicked.connect(self._handle_staff_report_apply_filters)

        filter_clear_btn = QtWidgets.QPushButton("Đặt lại")
        filter_clear_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        filter_clear_btn.setMinimumHeight(40)
        filter_clear_btn.clicked.connect(self._handle_staff_report_reset_filters)

        filter_row.addWidget(self.staff_report_period_combo)
        filter_row.addWidget(self.staff_report_doctor_combo)
        filter_row.addWidget(self.staff_report_metric_combo)
        filter_row.addWidget(filter_apply_btn)
        filter_row.addWidget(filter_clear_btn)
        filter_card.layout().addLayout(filter_row)
        layout.addWidget(filter_card)

        reports_actions = QtWidgets.QHBoxLayout()
        reports_actions.setSpacing(8)
        refresh_btn = QtWidgets.QPushButton("🔄 Cập nhật")
        refresh_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        refresh_btn.setStyleSheet(
            "QPushButton { background: #0ea5e9; color: white; padding: 8px 12px; border-radius: 8px; font-weight: 700; border: none; }"
            "QPushButton:hover { background: #0284c7; }"
        )
        refresh_btn.clicked.connect(self._refresh_staff_reports)

        self.staff_report_export_btn = QtWidgets.QPushButton("⬇ Xuất báo cáo")
        self.staff_report_export_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.staff_report_export_btn.setStyleSheet(
            "QPushButton { background: #ffffff; color: #334155; padding: 8px 12px; border-radius: 8px; font-weight: 800; border: 1px solid #cbd5e1; }"
            "QPushButton:hover { border-color: #94a3b8; }"
        )
        self.staff_report_export_btn.clicked.connect(self._handle_staff_report_export)

        reports_actions.addWidget(refresh_btn)
        reports_actions.addWidget(self.staff_report_export_btn)
        reports_actions.addStretch()
        layout.addLayout(reports_actions)

        self.staff_report_feedback = QtWidgets.QLabel("Báo cáo sẽ được tải ngay khi mở trang.")
        self.staff_report_feedback.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 600;")
        layout.addWidget(self.staff_report_feedback)

        self.staff_report_kpi_row = QtWidgets.QHBoxLayout()
        self.staff_report_kpi_row.setSpacing(12)
        layout.addLayout(self.staff_report_kpi_row)

        summary_card = self._build_section_card("Tóm tắt ca trực")
        self.staff_report_summary_lbl = QtWidgets.QLabel("Dữ liệu báo cáo sẽ hiển thị sau khi tải.")
        self.staff_report_summary_lbl.setWordWrap(True)
        self.staff_report_summary_lbl.setStyleSheet("font-size: 13px; color: #334155; font-weight: 700;")
        summary_card.layout().addWidget(self.staff_report_summary_lbl)
        layout.addWidget(summary_card)

        content_row = QtWidgets.QHBoxLayout()
        content_row.setSpacing(16)

        left_col = QtWidgets.QVBoxLayout()
        left_col.setSpacing(12)

        placeholder_card = self._build_section_card("Biểu đồ tổng quan (placeholder trung thực)")
        self.staff_report_placeholder_title = QtWidgets.QLabel("Đang chờ dữ liệu...")
        self.staff_report_placeholder_title.setStyleSheet("font-size: 13px; color: #0f172a; font-weight: 900;")
        self.staff_report_placeholder_title.setWordWrap(True)
        self.staff_report_placeholder_hint = QtWidgets.QLabel(
            "Màn hình hiện dùng summary bars để minh họa tỷ trọng, chưa tích hợp chart engine chuyên dụng."
        )
        self.staff_report_placeholder_hint.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        self.staff_report_placeholder_hint.setWordWrap(True)
        placeholder_card.layout().addWidget(self.staff_report_placeholder_title)
        placeholder_card.layout().addWidget(self.staff_report_placeholder_hint)

        self.staff_report_ratio_paid = QtWidgets.QProgressBar()
        self.staff_report_ratio_paid.setRange(0, 100)
        self.staff_report_ratio_paid.setValue(0)
        self.staff_report_ratio_paid.setFormat("Đã thu: %p%")
        self.staff_report_ratio_paid.setStyleSheet(
            "QProgressBar { border: 1px solid #dbe4ee; border-radius: 8px; text-align: center; background: #f8fafc; font-weight: 800; color: #0f172a; }"
            "QProgressBar::chunk { background: #16a34a; border-radius: 8px; }"
        )
        self.staff_report_ratio_unpaid = QtWidgets.QProgressBar()
        self.staff_report_ratio_unpaid.setRange(0, 100)
        self.staff_report_ratio_unpaid.setValue(0)
        self.staff_report_ratio_unpaid.setFormat("Chưa thu: %p%")
        self.staff_report_ratio_unpaid.setStyleSheet(
            "QProgressBar { border: 1px solid #dbe4ee; border-radius: 8px; text-align: center; background: #f8fafc; font-weight: 800; color: #0f172a; }"
            "QProgressBar::chunk { background: #f97316; border-radius: 8px; }"
        )
        placeholder_card.layout().addWidget(self.staff_report_ratio_paid)
        placeholder_card.layout().addWidget(self.staff_report_ratio_unpaid)
        left_col.addWidget(placeholder_card)

        status_card = self._build_section_card("Bảng trạng thái lịch hẹn")
        self.staff_report_status_table = QtWidgets.QTableWidget(0, 3)
        self.staff_report_status_table.setHorizontalHeaderLabels(["Trạng thái", "Số lượng", "Tỷ trọng"])
        self.staff_report_status_table.verticalHeader().setVisible(False)
        self.staff_report_status_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.staff_report_status_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_report_status_table.setShowGrid(False)
        self.staff_report_status_table.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.staff_report_status_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staff_report_status_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_report_status_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_report_status_table.setMinimumHeight(190)
        self.staff_report_status_table.setStyleSheet(
            "QTableWidget { border: 1px solid #e7edf5; border-radius: 12px; background: #ffffff; }"
            "QHeaderView::section { background: #f8fafc; color: #1f2937; font-size: 12px; font-weight: 800; border: none; padding: 10px; }"
            "QTableWidget::item { border-bottom: 1px solid #edf2f7; padding: 8px; color: #0f172a; font-weight: 600; }"
        )
        status_card.layout().addWidget(self.staff_report_status_table)
        left_col.addWidget(status_card)

        unpaid_card = self._build_section_card("Hóa đơn chờ thu")
        self.staff_report_unpaid_table = QtWidgets.QTableWidget(0, 4)
        self.staff_report_unpaid_table.setHorizontalHeaderLabels(["Mã HD", "Bệnh nhân", "Số tiền", "Thời điểm"])
        self.staff_report_unpaid_table.verticalHeader().setVisible(False)
        self.staff_report_unpaid_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.staff_report_unpaid_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_report_unpaid_table.setShowGrid(False)
        self.staff_report_unpaid_table.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.staff_report_unpaid_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staff_report_unpaid_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_report_unpaid_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_report_unpaid_table.setMinimumHeight(200)
        self.staff_report_unpaid_table.setStyleSheet(
            "QTableWidget { border: 1px solid #e7edf5; border-radius: 12px; background: #ffffff; }"
            "QHeaderView::section { background: #f8fafc; color: #1f2937; font-size: 12px; font-weight: 800; border: none; padding: 10px; }"
            "QTableWidget::item { border-bottom: 1px solid #edf2f7; padding: 8px; color: #0f172a; font-weight: 600; }"
        )
        unpaid_card.layout().addWidget(self.staff_report_unpaid_table)
        left_col.addWidget(unpaid_card)

        right_col = QtWidgets.QVBoxLayout()
        right_col.setSpacing(12)

        shortcuts_card = self._build_section_card("Quick shortcuts")
        shortcuts_grid = QtWidgets.QGridLayout()
        shortcuts_grid.setHorizontalSpacing(10)
        shortcuts_grid.setVerticalSpacing(10)
        shortcuts_grid.addWidget(self._build_quick_action_button("Mở lịch hẹn", "📅", 2, "#eaf2ff", "#2563eb"), 0, 0)
        shortcuts_grid.addWidget(self._build_quick_action_button("Mở thanh toán", "💳", 4, "#fff3e4", "#f97316"), 0, 1)
        shortcuts_grid.addWidget(self._build_quick_action_button("Mở dịch vụ", "🩺", 5, "#e8f8ef", "#16a34a"), 1, 0)
        shortcuts_grid.addWidget(self._build_quick_action_button("Mở thông báo", "🔔", 6, "#f0eaff", "#7c3aed"), 1, 1)
        shortcuts_card.layout().addLayout(shortcuts_grid)
        right_col.addWidget(shortcuts_card)

        info_card = self._build_section_card("Ghi chú dữ liệu")
        self.staff_report_updated_at_lbl = QtWidgets.QLabel("Cập nhật gần nhất: --")
        self.staff_report_updated_at_lbl.setStyleSheet("font-size: 12px; color: #334155; font-weight: 800;")
        self.staff_report_dataset_note_lbl = QtWidgets.QLabel(
            "Dữ liệu đang tổng hợp từ Appointments, Payments và ReportController (core totals)."
        )
        self.staff_report_dataset_note_lbl.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        self.staff_report_dataset_note_lbl.setWordWrap(True)
        info_card.layout().addWidget(self.staff_report_updated_at_lbl)
        info_card.layout().addWidget(self.staff_report_dataset_note_lbl)
        right_col.addWidget(info_card)
        right_col.addStretch()

        content_row.addLayout(left_col, 7)
        content_row.addLayout(right_col, 3)
        layout.addLayout(content_row, 1)

        footer_note = QtWidgets.QLabel(
            "Ghi chú: chức năng xuất file đang ở chế độ placeholder trung thực. Khi có backend export thật, nút xuất sẽ chuyển sang tạo tệp thay vì thông báo." 
        )
        footer_note.setWordWrap(True)
        footer_note.setStyleSheet("font-size: 12px; color: #64748b; font-style: italic;")
        layout.addWidget(footer_note)

        self._refresh_staff_reports()
        return page

    def _build_staff_settings_page(self):
        page = QtWidgets.QFrame()
        page.setStyleSheet("background: #f8fbff; border: none;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        settings_data = self._load_staff_settings_data()

        header = QtWidgets.QFrame()
        header.setStyleSheet("background: transparent; border: none;")
        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(4, 0, 4, 0)
        header_layout.setSpacing(14)

        header_left = QtWidgets.QVBoxLayout()
        header_left.setSpacing(5)
        heading = QtWidgets.QLabel("Cài đặt")
        heading.setStyleSheet("font-size: 25px; color: #0f172a; font-weight: 900;")
        breadcrumb = QtWidgets.QLabel("Trang chủ  ›  Cài đặt")
        breadcrumb.setStyleSheet("font-size: 14px; color: #64748b; font-weight: 700;")
        header_left.addWidget(heading)
        header_left.addWidget(breadcrumb)
        header_layout.addLayout(header_left)
        header_layout.addStretch()

        bell_wrap = QtWidgets.QWidget()
        bell_wrap.setFixedSize(36, 36)
        bell_layout = QtWidgets.QGridLayout(bell_wrap)
        bell_layout.setContentsMargins(0, 0, 0, 0)
        bell = QtWidgets.QLabel("🔔")
        bell.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        bell.setStyleSheet("border: none; background: transparent; font-size: 21px; color: #64748b;")
        bell_layout.addWidget(bell, 0, 0)
        badge = QtWidgets.QLabel("3")
        badge.setFixedSize(16, 16)
        badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet("background: #ef4444; color: white; border-radius: 8px; font-size: 10px; font-weight: 900;")
        bell_layout.addWidget(badge, 0, 0, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)

        avatar = QtWidgets.QLabel("👤")
        avatar.setFixedSize(42, 42)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("background: #eaf2ff; border-radius: 21px; font-size: 22px;")
        self.staff_settings_header_user_label = QtWidgets.QLabel(f"{self.username}  ▾")
        self.staff_settings_header_user_label.setStyleSheet(
            "border: none; background: transparent; font-size: 13px; color: #0f172a; font-weight: 900;"
        )
        header_layout.addWidget(bell_wrap)
        header_layout.addWidget(avatar)
        header_layout.addWidget(self.staff_settings_header_user_label)
        layout.addWidget(header)

        content_row = QtWidgets.QHBoxLayout()
        content_row.setSpacing(22)

        menu_card = self._build_section_card("")
        menu_card.setFixedWidth(270)
        menu_layout = menu_card.layout()
        menu_title = QtWidgets.QLabel("Menu cài đặt")
        menu_title.setStyleSheet("font-size: 16px; color: #0f172a; font-weight: 900;")
        menu_hint = QtWidgets.QLabel(
            "Shell issue #23 đang ưu tiên luồng hồ sơ, mật khẩu và các vùng placeholder trung thực cho staff."
        )
        menu_hint.setWordWrap(True)
        menu_hint.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        menu_layout.addWidget(menu_title)
        menu_layout.addWidget(menu_hint)

        menu_items = [
            ("👤", "Thông tin cá nhân", True),
            ("🏥", "Thông tin phòng khám", False),
            ("👥", "Quản lý người dùng", False),
            ("🛡️", "Phân quyền", False),
            ("📅", "Cài đặt lịch hẹn", False),
            ("🔔", "Cài đặt thông báo", False),
            ("🧾", "Cài đặt hóa đơn", False),
            ("💾", "Sao lưu & Khôi phục", False),
            ("📜", "Nhật ký hệ thống", False),
        ]
        for icon, text, is_active in menu_items:
            btn = QtWidgets.QPushButton(f"{icon}   {text}")
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setMinimumHeight(52)
            btn.setStyleSheet(self._staff_settings_menu_button_style(is_active=is_active))
            if is_active:
                btn.setEnabled(False)
            else:
                btn.clicked.connect(
                    lambda checked, section=text: self._show_staff_settings_placeholder(
                        section,
                        f"Khu vực '{section}' mới được dựng shell định hướng trong task này. Nội dung thao tác chi tiết sẽ mở ở task chuyên trách tiếp theo.",
                    )
                )
            menu_layout.addWidget(btn)

        menu_status = QtWidgets.QLabel(
            "Các mục ngoài 'Thông tin cá nhân' hiện đóng vai trò điều hướng thị giác để staff nhìn rõ phạm vi cài đặt, chưa mở workflow độc lập trong foundation này."
        )
        menu_status.setWordWrap(True)
        menu_status.setStyleSheet("font-size: 12px; color: #475569; font-style: italic;")
        menu_layout.addWidget(menu_status)
        menu_layout.addStretch()
        content_row.addWidget(menu_card)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        scroll_content = QtWidgets.QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 2, 0)
        scroll_layout.setSpacing(16)

        profile_card = self._build_section_card("")
        profile_layout = profile_card.layout()
        profile_header = QtWidgets.QHBoxLayout()
        profile_header.setSpacing(12)
        profile_title_col = QtWidgets.QVBoxLayout()
        profile_title_col.setSpacing(4)
        profile_title = QtWidgets.QLabel("Thông tin cá nhân")
        profile_title.setStyleSheet("font-size: 17px; color: #0f172a; font-weight: 900;")
        profile_subtitle = QtWidgets.QLabel(
            "Staff có thể cập nhật họ tên/SĐT/email của chính mình cùng giới tính/ngày sinh theo đường persistence an toàn, không phụ thuộc doctor_id."
        )
        profile_subtitle.setWordWrap(True)
        profile_subtitle.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        profile_title_col.addWidget(profile_title)
        profile_title_col.addWidget(profile_subtitle)
        profile_header.addLayout(profile_title_col, 1)
        save_profile_btn = QtWidgets.QPushButton("💾 Lưu thay đổi")
        save_profile_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        save_profile_btn.setStyleSheet(self._staff_settings_button_style(primary=True))
        save_profile_btn.clicked.connect(self._handle_staff_profile_update)
        profile_header.addWidget(save_profile_btn, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        profile_layout.addLayout(profile_header)

        profile_body = QtWidgets.QHBoxLayout()
        profile_body.setSpacing(18)
        avatar_col = QtWidgets.QVBoxLayout()
        avatar_col.setSpacing(8)
        avatar_col.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        avatar_shell = QtWidgets.QFrame()
        avatar_shell.setFixedSize(118, 118)
        avatar_shell.setStyleSheet("background: #f8fbff; border: 1px dashed #cbd5e1; border-radius: 59px;")
        avatar_shell_layout = QtWidgets.QGridLayout(avatar_shell)
        avatar_shell_layout.setContentsMargins(0, 0, 0, 0)
        avatar_lbl = QtWidgets.QLabel("👤")
        avatar_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar_lbl.setStyleSheet("border: none; background: transparent; font-size: 52px;")
        avatar_shell_layout.addWidget(avatar_lbl, 0, 0)
        camera_btn = QtWidgets.QPushButton("📷")
        camera_btn.setFixedSize(32, 32)
        camera_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        camera_btn.setStyleSheet(
            "QPushButton { background: #ffffff; border: 1px solid #dbe4ee; border-radius: 16px; font-size: 15px; }"
            "QPushButton:hover { background: #f8fafc; }"
        )
        camera_btn.clicked.connect(
            lambda checked: self._show_staff_settings_placeholder(
                "Ảnh đại diện",
                "Task này mới dựng shell ảnh đại diện. Chức năng upload/persist avatar staff sẽ được nối hoàn chỉnh ở bước sau.",
            )
        )
        avatar_shell_layout.addWidget(
            camera_btn,
            0,
            0,
            alignment=QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight,
        )
        avatar_note = QtWidgets.QLabel("Ảnh đại diện đang ở chế độ minh họa shell.")
        avatar_note.setWordWrap(True)
        avatar_note.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar_note.setStyleSheet("font-size: 11px; color: #64748b; font-weight: 700;")
        avatar_col.addWidget(avatar_shell, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        avatar_col.addWidget(avatar_note)
        profile_body.addLayout(avatar_col)

        self.staff_settings_name_input = QtWidgets.QLineEdit(str(self.user_data.get("name") or self.user_data.get("username") or ""))
        self.staff_settings_name_input.setPlaceholderText("Nhập họ và tên")
        self.staff_settings_name_input.setStyleSheet(self._intake_input_style())

        self.staff_settings_role_combo = QtWidgets.QComboBox()
        self.staff_settings_role_combo.addItems(["Nhân viên lễ tân"])
        self.staff_settings_role_combo.setEnabled(False)
        self.staff_settings_role_combo.setStyleSheet(self._intake_input_style())

        self.staff_settings_email_input = QtWidgets.QLineEdit(str(self.user_data.get("email") or ""))
        self.staff_settings_email_input.setPlaceholderText("lan.nguyen@careplus.vn")
        self.staff_settings_email_input.setStyleSheet(self._intake_input_style())

        self.staff_settings_phone_input = QtWidgets.QLineEdit(str(self.user_data.get("phone") or ""))
        self.staff_settings_phone_input.setPlaceholderText("0987 654 321")
        self.staff_settings_phone_input.setStyleSheet(self._intake_input_style())

        dob_display = str(settings_data.get("dob") or self.user_data.get("dob") or "").strip()
        if re.match(r"^\d{4}-\d{2}-\d{2}$", dob_display):
            yyyy, mm, dd = dob_display.split("-")
            dob_display = f"{dd}/{mm}/{yyyy}"
        self.staff_settings_dob_input = QtWidgets.QLineEdit(dob_display)
        self.staff_settings_dob_input.setPlaceholderText("dd/mm/yyyy")
        self.staff_settings_dob_input.setStyleSheet(self._intake_input_style())

        self.staff_settings_gender_combo = QtWidgets.QComboBox()
        self.staff_settings_gender_combo.addItems(["Nam", "Nữ"])
        current_gender = str(settings_data.get("gender") or self.user_data.get("gender") or "Nam")
        gender_index = self.staff_settings_gender_combo.findText(current_gender)
        self.staff_settings_gender_combo.setCurrentIndex(gender_index if gender_index >= 0 else 0)
        self.staff_settings_gender_combo.setStyleSheet(self._intake_input_style())

        profile_grid = QtWidgets.QGridLayout()
        profile_grid.setHorizontalSpacing(14)
        profile_grid.setVerticalSpacing(12)
        profile_grid.addWidget(self._build_intake_field("Họ và tên", self.staff_settings_name_input), 0, 0)
        profile_grid.addWidget(self._build_intake_field("Chức vụ", self.staff_settings_role_combo), 0, 1)
        profile_grid.addWidget(self._build_intake_field("Email", self.staff_settings_email_input), 0, 2)
        profile_grid.addWidget(self._build_intake_field("Số điện thoại", self.staff_settings_phone_input), 1, 0)
        profile_grid.addWidget(self._build_intake_field("Ngày sinh", self.staff_settings_dob_input), 1, 1)
        profile_grid.addWidget(self._build_intake_field("Giới tính", self.staff_settings_gender_combo), 1, 2)
        profile_body.addLayout(profile_grid, 1)
        profile_layout.addLayout(profile_body)

        self.staff_settings_profile_feedback = QtWidgets.QLabel(
            "Chưa có thay đổi mới. Khi lưu thành công, dữ liệu sẽ được cập nhật xuống persistence path của staff."
        )
        self.staff_settings_profile_feedback.setWordWrap(True)
        self.staff_settings_profile_feedback.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 600;")
        profile_layout.addWidget(self.staff_settings_profile_feedback)
        scroll_layout.addWidget(profile_card)

        password_card = self._build_section_card("")
        password_layout = password_card.layout()
        password_title = QtWidgets.QLabel("Đổi mật khẩu")
        password_title.setStyleSheet("font-size: 17px; color: #0f172a; font-weight: 900;")
        password_layout.addWidget(password_title)

        password_row = QtWidgets.QHBoxLayout()
        password_row.setSpacing(14)
        self.staff_settings_current_password_input = QtWidgets.QLineEdit()
        self.staff_settings_current_password_input.setPlaceholderText("Nhập mật khẩu hiện tại")
        self.staff_settings_current_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.staff_settings_current_password_input.setStyleSheet(self._intake_input_style())
        self.staff_settings_new_password_input = QtWidgets.QLineEdit()
        self.staff_settings_new_password_input.setPlaceholderText("Nhập mật khẩu mới")
        self.staff_settings_new_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.staff_settings_new_password_input.setStyleSheet(self._intake_input_style())
        self.staff_settings_confirm_password_input = QtWidgets.QLineEdit()
        self.staff_settings_confirm_password_input.setPlaceholderText("Nhập lại mật khẩu mới")
        self.staff_settings_confirm_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.staff_settings_confirm_password_input.setStyleSheet(self._intake_input_style())
        password_row.addWidget(self._build_intake_field("Mật khẩu hiện tại", self.staff_settings_current_password_input), 1)
        password_row.addWidget(self._build_intake_field("Mật khẩu mới", self.staff_settings_new_password_input), 1)
        password_row.addWidget(self._build_intake_field("Xác nhận mật khẩu mới", self.staff_settings_confirm_password_input), 1)

        change_password_btn = QtWidgets.QPushButton("🔒 Đổi mật khẩu")
        change_password_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        change_password_btn.setMinimumWidth(142)
        change_password_btn.setStyleSheet(self._staff_settings_button_style(primary=True, accent="#2563eb"))
        change_password_btn.clicked.connect(self._handle_staff_password_change)
        password_row.addWidget(change_password_btn, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        password_layout.addLayout(password_row)

        self.staff_settings_password_feedback = QtWidgets.QLabel("Mật khẩu mới cần tối thiểu 8 ký tự và không được trùng mật khẩu cũ.")
        self.staff_settings_password_feedback.setWordWrap(True)
        self.staff_settings_password_feedback.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 600;")
        password_layout.addWidget(self.staff_settings_password_feedback)
        scroll_layout.addWidget(password_card)

        options_logo_row = QtWidgets.QHBoxLayout()
        options_logo_row.setSpacing(16)

        options_card = self._build_section_card("")
        options_layout = options_card.layout()
        options_header = QtWidgets.QHBoxLayout()
        options_title_col = QtWidgets.QVBoxLayout()
        options_title_col.setSpacing(4)
        options_title = QtWidgets.QLabel("Tùy chọn hệ thống")
        options_title.setStyleSheet("font-size: 17px; color: #0f172a; font-weight: 900;")
        options_subtitle = QtWidgets.QLabel(
            "Các tùy chọn cá nhân khả dụng (ngôn ngữ, giao diện, thông báo) được lưu ngay theo user_id của staff."
        )
        options_subtitle.setWordWrap(True)
        options_subtitle.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        options_title_col.addWidget(options_title)
        options_title_col.addWidget(options_subtitle)
        options_header.addLayout(options_title_col, 1)
        options_badge = QtWidgets.QLabel("Áp dụng tức thì")
        options_badge.setStyleSheet("background: #e8f8ef; color: #0f9f6e; border-radius: 10px; padding: 5px 10px; font-size: 11px; font-weight: 900;")
        options_header.addWidget(options_badge, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        options_layout.addLayout(options_header)

        options_body = QtWidgets.QHBoxLayout()
        options_body.setSpacing(16)
        checkbox_col = QtWidgets.QVBoxLayout()
        checkbox_col.setSpacing(12)
        self.staff_settings_auto_confirm_checkbox = QtWidgets.QCheckBox("Tự động xác nhận lịch hẹn sau khi tạo (chưa hỗ trợ)")
        self.staff_settings_auto_confirm_checkbox.setChecked(False)
        self.staff_settings_auto_confirm_checkbox.setEnabled(False)
        self.staff_settings_auto_confirm_checkbox.setToolTip(
            "Workflow tự động xác nhận sau khi tạo chưa có backend riêng cho staff nên đang bị khóa để tránh lưu nhầm sang cờ thông báo."
        )
        self.staff_settings_screen_notify_checkbox = QtWidgets.QCheckBox("Hiển thị thông báo trên màn hình")
        self.staff_settings_screen_notify_checkbox.setChecked(bool(settings_data.get("notify_reminder", True)))
        self.staff_settings_sound_notify_checkbox = QtWidgets.QCheckBox("Âm thanh khi có thông báo mới")
        self.staff_settings_sound_notify_checkbox.setChecked(bool(settings_data.get("notify_system", True)))
        for checkbox in (
            self.staff_settings_auto_confirm_checkbox,
            self.staff_settings_screen_notify_checkbox,
            self.staff_settings_sound_notify_checkbox,
        ):
            checkbox.setStyleSheet(
                "QCheckBox { color: #0f172a; font-size: 13px; font-weight: 700; spacing: 10px; }"
                "QCheckBox::indicator { width: 16px; height: 16px; border: 1px solid #cbd5e1; border-radius: 4px; background: #ffffff; }"
                "QCheckBox::indicator:checked { background: #10b981; border: 1px solid #10b981; }"
            )
            checkbox_col.addWidget(checkbox)
        self.staff_settings_language_combo = QtWidgets.QComboBox()
        self.staff_settings_language_combo.addItems(["Tiếng Việt", "English"])
        language_index = self.staff_settings_language_combo.findText(str(settings_data.get("language") or "Tiếng Việt"))
        self.staff_settings_language_combo.setCurrentIndex(language_index if language_index >= 0 else 0)
        self.staff_settings_language_combo.setStyleSheet(self._intake_input_style())
        self.staff_settings_theme_combo = QtWidgets.QComboBox()
        self.staff_settings_theme_combo.addItems(["Sáng", "Tối", "Theo hệ thống"])
        theme_index = self.staff_settings_theme_combo.findText(str(settings_data.get("theme_mode") or "Sáng"))
        self.staff_settings_theme_combo.setCurrentIndex(theme_index if theme_index >= 0 else 0)
        self.staff_settings_theme_combo.setStyleSheet(self._intake_input_style())
        checkbox_col.addWidget(self._build_intake_field("Ngôn ngữ", self.staff_settings_language_combo))
        checkbox_col.addWidget(self._build_intake_field("Giao diện", self.staff_settings_theme_combo))

        system_col = QtWidgets.QVBoxLayout()
        system_col.setSpacing(12)
        self.staff_settings_date_format_combo = QtWidgets.QComboBox()
        self.staff_settings_date_format_combo.addItems(["dd/mm/yyyy", "mm/dd/yyyy", "yyyy-mm-dd"])
        self.staff_settings_date_format_combo.setStyleSheet(self._intake_input_style())
        self.staff_settings_time_format_combo = QtWidgets.QComboBox()
        self.staff_settings_time_format_combo.addItems(["24 giờ", "12 giờ"])
        self.staff_settings_time_format_combo.setStyleSheet(self._intake_input_style())
        self.staff_settings_page_size_combo = QtWidgets.QComboBox()
        self.staff_settings_page_size_combo.addItems(["10 bản ghi", "20 bản ghi", "50 bản ghi", "100 bản ghi"])
        self.staff_settings_page_size_combo.setStyleSheet(self._intake_input_style())
        system_col.addWidget(self._build_intake_field("Định dạng ngày", self.staff_settings_date_format_combo))
        system_col.addWidget(self._build_intake_field("Định dạng giờ", self.staff_settings_time_format_combo))
        system_col.addWidget(self._build_intake_field("Số bản ghi trên trang", self.staff_settings_page_size_combo))
        options_body.addLayout(checkbox_col, 1)
        options_body.addLayout(system_col, 1)
        options_layout.addLayout(options_body)
        options_note = QtWidgets.QLabel(
            "Lưu ý: chỉ các tùy chọn cá nhân khả dụng được persist trong task này. Các cấu hình lõi/hệ thống khác vẫn giữ ở chế độ placeholder trung thực."
        )
        options_note.setWordWrap(True)
        options_note.setStyleSheet("font-size: 12px; color: #475569; font-style: italic;")
        options_layout.addWidget(options_note)
        auto_confirm_note = QtWidgets.QLabel(
            "Mục 'Tự động xác nhận lịch hẹn sau khi tạo' đang hiển thị để phản ánh đúng spec UI, nhưng chưa có persistence/behavior staff-safe nên được khóa trung thực."
        )
        auto_confirm_note.setWordWrap(True)
        auto_confirm_note.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        options_layout.addWidget(auto_confirm_note)
        self.staff_settings_options_feedback = QtWidgets.QLabel(
            "Các thay đổi ở card này sẽ lưu tự động khi bạn điều chỉnh từng tùy chọn."
        )
        self.staff_settings_options_feedback.setWordWrap(True)
        self.staff_settings_options_feedback.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 600;")
        options_layout.addWidget(self.staff_settings_options_feedback)
        self._bind_staff_settings_option_handlers()
        options_logo_row.addWidget(options_card, 3)

        logo_card = self._build_section_card("")
        logo_layout = logo_card.layout()
        logo_title = QtWidgets.QLabel("Logo phòng khám")
        logo_title.setStyleSheet("font-size: 17px; color: #0f172a; font-weight: 900;")
        logo_layout.addWidget(logo_title)
        logo_preview = QtWidgets.QFrame()
        logo_preview.setFixedSize(150, 150)
        logo_preview.setStyleSheet("background: #ffffff; border: 1px solid #10b981; border-radius: 12px;")
        logo_preview_layout = QtWidgets.QVBoxLayout(logo_preview)
        logo_preview_layout.setContentsMargins(12, 12, 12, 12)
        logo_preview_layout.setSpacing(6)
        logo_icon = QtWidgets.QLabel("✚")
        logo_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        logo_icon.setStyleSheet("font-size: 42px; color: #10b981; font-weight: 900;")
        logo_name = QtWidgets.QLabel("CarePlus")
        logo_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        logo_name.setStyleSheet("font-size: 22px; color: #10b981; font-weight: 900;")
        logo_preview_layout.addStretch()
        logo_preview_layout.addWidget(logo_icon)
        logo_preview_layout.addWidget(logo_name)
        logo_preview_layout.addStretch()
        logo_layout.addWidget(logo_preview, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        logo_actions = QtWidgets.QHBoxLayout()
        logo_actions.setSpacing(10)
        change_logo_btn = QtWidgets.QPushButton("⬆ Thay đổi logo")
        change_logo_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        change_logo_btn.setStyleSheet(self._staff_settings_button_style())
        change_logo_btn.clicked.connect(lambda checked: self._handle_staff_logo_scope_notice("thay đổi"))
        remove_logo_btn = QtWidgets.QPushButton("🗑 Xóa")
        remove_logo_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        remove_logo_btn.setStyleSheet(self._staff_settings_button_style(danger=True))
        remove_logo_btn.clicked.connect(lambda checked: self._handle_staff_logo_scope_notice("xóa"))
        logo_actions.addWidget(change_logo_btn)
        logo_actions.addWidget(remove_logo_btn)
        logo_layout.addLayout(logo_actions)
        logo_note = QtWidgets.QLabel(
            "Card logo hiện chỉ đóng vai trò trình bày cấu trúc issue #23. Chưa có backend duyệt file, lưu asset hay đồng bộ toàn phòng khám."
        )
        logo_note.setWordWrap(True)
        logo_note.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        logo_layout.addWidget(logo_note)
        options_logo_row.addWidget(logo_card, 2)
        scroll_layout.addLayout(options_logo_row)

        backup_restore_row = QtWidgets.QHBoxLayout()
        backup_restore_row.setSpacing(16)

        backup_card = self._build_section_card("")
        backup_layout = backup_card.layout()
        backup_title = QtWidgets.QLabel("Sao lưu dữ liệu")
        backup_title.setStyleSheet("font-size: 17px; color: #0f172a; font-weight: 900;")
        backup_desc = QtWidgets.QLabel("Sao lưu dữ liệu để bảo vệ thông tin phòng khám của bạn.")
        backup_desc.setWordWrap(True)
        backup_desc.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        self.staff_settings_backup_mode_combo = QtWidgets.QComboBox()
        self.staff_settings_backup_mode_combo.addItem("Cloud", "cloud")
        self.staff_settings_backup_mode_combo.addItem("Local", "local")
        self.staff_settings_backup_mode_combo.setStyleSheet(self._intake_input_style())
        self.staff_settings_backup_mode_combo.setMinimumHeight(40)

        mode_row = QtWidgets.QHBoxLayout()
        mode_row.setSpacing(8)
        mode_row.addWidget(QtWidgets.QLabel("Chế độ sao lưu:"))
        mode_row.addWidget(self.staff_settings_backup_mode_combo)

        last_backup = str(settings_data.get("last_backup_at") or "Chưa có")
        last_sync = str(settings_data.get("last_sync_at") or "Chưa có")
        self.staff_settings_backup_status_label = QtWidgets.QLabel(f"Lần sao lưu gần nhất: {last_backup}")
        self.staff_settings_backup_status_label.setWordWrap(True)
        self.staff_settings_backup_status_label.setStyleSheet("font-size: 12px; color: #334155; font-weight: 800;")
        self.staff_settings_sync_status_label = QtWidgets.QLabel(f"Lần đồng bộ gần nhất: {last_sync}")
        self.staff_settings_sync_status_label.setWordWrap(True)
        self.staff_settings_sync_status_label.setStyleSheet("font-size: 12px; color: #334155; font-weight: 800;")
        backup_layout.addWidget(backup_title)
        backup_layout.addWidget(backup_desc)
        backup_layout.addLayout(mode_row)
        backup_layout.addWidget(self.staff_settings_backup_status_label)
        backup_layout.addWidget(self.staff_settings_sync_status_label)
        backup_actions = QtWidgets.QHBoxLayout()
        backup_actions.setSpacing(10)
        backup_now_btn = QtWidgets.QPushButton("💾 Sao lưu ngay")
        backup_now_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        backup_now_btn.setStyleSheet(self._staff_settings_button_style(primary=True))
        backup_now_btn.clicked.connect(self._handle_staff_backup_now)
        sync_now_btn = QtWidgets.QPushButton("🔄 Đồng bộ cloud")
        sync_now_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        sync_now_btn.setStyleSheet(self._staff_settings_button_style())
        sync_now_btn.clicked.connect(self._handle_staff_sync_now)
        backup_actions.addWidget(backup_now_btn)
        backup_actions.addWidget(sync_now_btn)
        backup_actions.addStretch()
        backup_layout.addLayout(backup_actions)
        self.staff_settings_backup_feedback = QtWidgets.QLabel(
            "Chức năng backup/sync đang dùng backend hiện có của SettingsController; restore vẫn bị khóa vì chưa có workflow an toàn cho staff."
        )
        self.staff_settings_backup_feedback.setWordWrap(True)
        self.staff_settings_backup_feedback.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 600;")
        backup_layout.addWidget(self.staff_settings_backup_feedback)
        backup_restore_row.addWidget(backup_card, 1)

        restore_card = self._build_section_card("")
        restore_layout = restore_card.layout()
        restore_title = QtWidgets.QLabel("Khôi phục dữ liệu")
        restore_title.setStyleSheet("font-size: 17px; color: #0f172a; font-weight: 900;")
        restore_desc = QtWidgets.QLabel("Khôi phục dữ liệu từ tệp sao lưu khi cần thiết.")
        restore_desc.setWordWrap(True)
        restore_desc.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        restore_warning = QtWidgets.QLabel(
            "Cảnh báo: restore là thao tác nguy hiểm và hiện chưa được cấp backend an toàn cho staff trong task foundation này."
        )
        restore_warning.setWordWrap(True)
        restore_warning.setStyleSheet("font-size: 12px; color: #b91c1c; font-weight: 800;")
        restore_layout.addWidget(restore_title)
        restore_layout.addWidget(restore_desc)
        restore_layout.addWidget(restore_warning)
        restore_actions = QtWidgets.QHBoxLayout()
        restore_actions.setSpacing(10)
        restore_pick_btn = QtWidgets.QPushButton("📁 Chọn tệp sao lưu")
        restore_pick_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        restore_pick_btn.setStyleSheet(self._staff_settings_button_style())
        restore_pick_btn.clicked.connect(lambda checked: self._handle_staff_restore_blocked("chọn tệp"))
        restore_btn = QtWidgets.QPushButton("♻ Khôi phục")
        restore_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        restore_btn.setStyleSheet(self._staff_settings_button_style(danger=True))
        restore_btn.setEnabled(False)
        restore_btn.clicked.connect(lambda checked: self._handle_staff_restore_blocked("khôi phục"))
        restore_actions.addWidget(restore_pick_btn)
        restore_actions.addWidget(restore_btn)
        restore_actions.addStretch()
        restore_layout.addLayout(restore_actions)
        backup_restore_row.addWidget(restore_card, 1)
        scroll_layout.addLayout(backup_restore_row)

        system_card = self._build_section_card("")
        system_layout = system_card.layout()
        system_header = QtWidgets.QHBoxLayout()
        system_title_col = QtWidgets.QVBoxLayout()
        system_title_col.setSpacing(4)
        system_title = QtWidgets.QLabel("Thông tin hệ thống")
        system_title.setStyleSheet("font-size: 17px; color: #0f172a; font-weight: 900;")
        system_subtitle = QtWidgets.QLabel(
            "Một số chỉ số đang dùng dữ liệu minh họa an toàn để staff nhìn rõ cấu trúc card trước khi utility backend hoàn thiện."
        )
        system_subtitle.setWordWrap(True)
        system_subtitle.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        system_title_col.addWidget(system_title)
        system_title_col.addWidget(system_subtitle)
        system_header.addLayout(system_title_col, 1)
        check_update_btn = QtWidgets.QPushButton("🔄 Kiểm tra cập nhật")
        check_update_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        check_update_btn.setStyleSheet(self._staff_settings_button_style())
        check_update_btn.clicked.connect(self._handle_staff_check_update)
        system_header.addWidget(check_update_btn, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        system_layout.addLayout(system_header)

        system_info_row = QtWidgets.QHBoxLayout()
        system_info_row.setSpacing(12)
        self.staff_settings_system_version_card = self._build_staff_settings_info_card("Phiên bản phần mềm", "Đang tải")
        self.staff_settings_system_db_card = self._build_staff_settings_info_card("Cơ sở dữ liệu", "Đang tải")
        self.staff_settings_system_server_card = self._build_staff_settings_info_card("Máy chủ", "Đang tải")
        self.staff_settings_system_size_card = self._build_staff_settings_info_card("Dung lượng dữ liệu", "Đang tải")
        system_info_row.addWidget(self.staff_settings_system_version_card)
        system_info_row.addWidget(self.staff_settings_system_db_card)
        system_info_row.addWidget(self.staff_settings_system_server_card)
        system_info_row.addWidget(self.staff_settings_system_size_card)
        system_layout.addLayout(system_info_row)

        session_card = self._build_section_card("")
        session_layout = session_card.layout()
        session_title = QtWidgets.QLabel("Phiên đăng nhập")
        session_title.setStyleSheet("font-size: 17px; color: #0f172a; font-weight: 900;")
        session_hint = QtWidgets.QLabel(
            "Nút đăng xuất bên trái vẫn là luồng chuẩn của MainView. Card này chỉ đưa thao tác ra vùng settings để staff dễ nhận biết trong shell mới."
        )
        session_hint.setWordWrap(True)
        session_hint.setStyleSheet("font-size: 12px; color: #475569; font-weight: 700;")
        trigger_logout_btn = QtWidgets.QPushButton("🚪 Đăng xuất ngay")
        trigger_logout_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        trigger_logout_btn.setStyleSheet(self._staff_settings_button_style(primary=True, accent="#ef4444"))
        trigger_logout_btn.clicked.connect(self.btn_logout.click)
        session_layout.addWidget(session_title)
        session_layout.addWidget(session_hint)
        session_layout.addWidget(trigger_logout_btn, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        system_layout.addWidget(session_card)
        scroll_layout.addWidget(system_card)
        scroll_layout.addStretch()

        self._refresh_staff_settings_utilities_status(settings_data)
        self._refresh_staff_settings_system_info()

        scroll.setWidget(scroll_content)
        content_row.addWidget(scroll, 1)
        layout.addLayout(content_row, 1)
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
        page.setStyleSheet("background: #f8fbff; border: none;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        heading = QtWidgets.QLabel("Dịch vụ & Gói khám")
        heading.setStyleSheet("font-size: 24px; color: #0f172a; font-weight: 900;")
        sub = QtWidgets.QLabel(
            "Tra cứu danh mục dịch vụ và gói khám để tư vấn, chọn nhanh vào luồng đặt lịch/thanh toán, đồng thời xem rõ mô tả, quy trình và lưu ý áp dụng."
        )
        sub.setStyleSheet("font-size: 13px; color: #64748b;")
        sub.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(sub)

        self.staff_service_tab_buttons = {}

        kpi_row = QtWidgets.QHBoxLayout()
        kpi_row.setSpacing(16)
        self.staff_service_kpi_total = self._build_kpi_card("Dịch vụ đang áp dụng", "0", "Đang đồng bộ từ danh mục Services", "#14b8a6", "#e6fffb", "🩺")
        self.staff_service_kpi_packages = self._build_kpi_card("Gói khám hiển thị", "0", "Fallback từ nhóm dịch vụ hiện có", "#2563eb", "#eaf2ff", "📦")
        self.staff_service_kpi_featured = self._build_kpi_card("Dịch vụ nổi bật", "0", "Ưu tiên tư vấn tại quầy", "#f97316", "#fff3e4", "⭐")
        self.staff_service_kpi_revenue = self._build_kpi_card("Doanh thu tham chiếu", "0 đ", "Ước tính theo giá danh mục đang hiển thị", "#7c3aed", "#f3e8ff", "₫")
        kpi_row.addWidget(self.staff_service_kpi_total)
        kpi_row.addWidget(self.staff_service_kpi_packages)
        kpi_row.addWidget(self.staff_service_kpi_featured)
        kpi_row.addWidget(self.staff_service_kpi_revenue)
        layout.addLayout(kpi_row)

        tab_row = QtWidgets.QHBoxLayout()
        tab_row.setSpacing(10)
        self.staff_service_tab_buttons["service"] = self._build_staff_service_tab_button("Dịch vụ", "service", True)
        self.staff_service_tab_buttons["package"] = self._build_staff_service_tab_button("Gói khám", "package", False)
        tab_row.addWidget(self.staff_service_tab_buttons["service"])
        tab_row.addWidget(self.staff_service_tab_buttons["package"])
        tab_row.addStretch()
        layout.addLayout(tab_row)

        filter_card = self._build_section_card("Tìm kiếm & lọc")
        filter_row = QtWidgets.QHBoxLayout()
        filter_row.setSpacing(10)

        self.staff_service_search_input = QtWidgets.QLineEdit()
        self.staff_service_search_input.setPlaceholderText("Tìm theo tên dịch vụ hoặc gói khám...")
        self.staff_service_search_input.setMinimumHeight(40)

        self.staff_service_type_combo = QtWidgets.QComboBox()
        self.staff_service_type_combo.setMinimumHeight(40)

        self.staff_service_status_combo = QtWidgets.QComboBox()
        self.staff_service_status_combo.setMinimumHeight(40)
        self.staff_service_status_combo.addItem("Tất cả trạng thái", "__all__")
        self.staff_service_status_combo.addItem("Đang áp dụng", "active")
        self.staff_service_status_combo.addItem("Tạm ngưng", "inactive")

        search_btn = QtWidgets.QPushButton("Tìm kiếm")
        search_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        search_btn.clicked.connect(self._refresh_staff_service_lookup)
        search_btn.setStyleSheet(
            "QPushButton { background: #0ea5e9; color: white; border: none; border-radius: 8px; padding: 8px 14px; font-weight: 700; }"
            "QPushButton:hover { background: #0284c7; }"
        )
        search_btn.setMinimumHeight(40)

        clear_btn = QtWidgets.QPushButton("Xóa lọc")
        clear_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        clear_btn.clicked.connect(self._handle_clear_staff_service_filters)
        clear_btn.setMinimumHeight(40)

        add_btn = QtWidgets.QPushButton("＋ Thêm dịch vụ")
        add_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        add_btn.clicked.connect(lambda checked=False: self._handle_staff_service_shell_action("add"))
        add_btn.setStyleSheet(
            "QPushButton { background: #10b981; color: white; border: none; border-radius: 8px; padding: 8px 16px; font-weight: 800; }"
            "QPushButton:hover { background: #059669; }"
            "QPushButton:disabled { background: #d1d5db; color: #6b7280; }"
        )
        add_btn.setMinimumHeight(40)
        add_btn.setEnabled(False)
        add_btn.setToolTip("Nhân viên chỉ có quyền tra cứu/chọn dịch vụ. Thêm mới danh mục do admin quản lý.")

        filter_row.addWidget(self.staff_service_search_input, 1)
        filter_row.addWidget(self.staff_service_type_combo)
        filter_row.addWidget(self.staff_service_status_combo)
        filter_row.addWidget(search_btn)
        filter_row.addWidget(clear_btn)
        filter_row.addWidget(add_btn)
        filter_card.layout().addLayout(filter_row)
        layout.addWidget(filter_card)

        content_row = QtWidgets.QHBoxLayout()
        content_row.setSpacing(18)

        table_card = self._build_section_card("Danh sách danh mục")
        self.staff_service_table = QtWidgets.QTableWidget(0, 7)
        self.staff_service_table.setHorizontalHeaderLabels(["STT", "Tên dịch vụ", "Phân loại", "Giá", "Thời lượng", "Trạng thái", "Thao tác"])
        self.staff_service_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.staff_service_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.staff_service_table.itemSelectionChanged.connect(self._handle_staff_service_selection)
        self.staff_service_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staff_service_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_service_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_service_table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_service_table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_service_table.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_service_table.verticalHeader().setVisible(False)
        self.staff_service_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_service_table.setShowGrid(False)
        self.staff_service_table.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.staff_service_table.setMinimumHeight(360)
        self.staff_service_table.setStyleSheet(
            "QTableWidget { border: 1px solid #e7edf5; border-radius: 12px; background: #ffffff; }"
            "QHeaderView::section { background: #f8fafc; color: #1f2937; font-size: 12px; font-weight: 800; border: none; padding: 10px; }"
            "QTableWidget::item { border-bottom: 1px solid #edf2f7; padding: 8px; color: #0f172a; font-weight: 600; }"
        )
        table_card.layout().addWidget(self.staff_service_table)

        self.staff_service_lookup_empty = QtWidgets.QLabel("Chưa có dữ liệu dịch vụ để hiển thị.")
        self.staff_service_lookup_empty.setWordWrap(True)
        self.staff_service_lookup_empty.setStyleSheet(
            "font-size: 13px; color: #64748b; padding: 10px 12px; background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 10px;"
        )
        table_card.layout().addWidget(self.staff_service_lookup_empty)
        self.staff_service_table_summary = QtWidgets.QLabel("Danh mục hiện có sẽ hiển thị tại đây.")
        self.staff_service_table_summary.setWordWrap(True)
        self.staff_service_table_summary.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        table_card.layout().addWidget(self.staff_service_table_summary)

        content_row.addWidget(table_card, 5)

        detail_card = self._build_section_card("Chi tiết dịch vụ / gói khám")
        self.staff_service_selected_label = QtWidgets.QLabel("Chưa chọn dịch vụ nào.")
        self.staff_service_selected_label.setWordWrap(True)
        self.staff_service_selected_label.setStyleSheet("font-size: 18px; color: #0f172a; font-weight: 900;")

        self.staff_service_selected_meta = QtWidgets.QLabel("Chọn một dòng ở bảng bên trái để xem trạng thái, giá và thông tin triển khai.")
        self.staff_service_selected_meta.setWordWrap(True)
        self.staff_service_selected_meta.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")

        self.staff_service_selected_status_badge = QtWidgets.QLabel("Chưa chọn")
        self.staff_service_selected_status_badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.staff_service_selected_status_badge.setStyleSheet(
            "background: #eef2f7; color: #475569; border-radius: 12px; padding: 6px 12px; font-size: 11px; font-weight: 900;"
        )

        price_duration_row = QtWidgets.QHBoxLayout()
        price_duration_row.setSpacing(10)
        self.staff_service_price_info = self._build_staff_service_info_chip("Giá", "Chưa có dữ liệu")
        self.staff_service_duration_info = self._build_staff_service_info_chip("Thời lượng", "Chưa có dữ liệu")
        price_duration_row.addWidget(self.staff_service_price_info)
        price_duration_row.addWidget(self.staff_service_duration_info)

        self.staff_service_description_label = self._build_staff_service_text_panel(
            "Mô tả",
            "Mô tả dịch vụ sẽ hiển thị ở đây. Nếu cơ sở dữ liệu chưa có nội dung, hệ thống sẽ dùng placeholder rõ ràng để nhân viên vẫn có ngữ cảnh tư vấn.",
        )
        self.staff_service_process_label = self._build_staff_service_text_panel(
            "Quy trình thực hiện",
            "Chưa có quy trình chi tiết từ dữ liệu hiện tại. Hệ thống sẽ hiển thị quy trình tham chiếu theo loại dịch vụ/gói khám.",
        )
        self.staff_service_notes_label = self._build_staff_service_text_panel(
            "Lưu ý",
            "Chưa có lưu ý chuyên biệt. Vui lòng xác nhận lại với bác sĩ/phòng cận lâm sàng khi tư vấn dịch vụ có chuẩn bị đặc biệt.",
        )

        related_title = QtWidgets.QLabel("Dịch vụ thường được chọn kèm")
        related_title.setStyleSheet("font-size: 13px; color: #0f172a; font-weight: 900;")
        self.staff_service_related_list = QtWidgets.QListWidget()
        self.staff_service_related_list.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.staff_service_related_list.setMinimumHeight(132)
        self.staff_service_related_list.setStyleSheet(
            "QListWidget { border: 1px solid #e4ebf4; border-radius: 12px; background: #ffffff; padding: 6px; }"
            "QListWidget::item { padding: 8px 10px; border-bottom: 1px solid #edf2f7; color: #0f172a; font-size: 12px; font-weight: 700; }"
        )

        detail_actions = QtWidgets.QHBoxLayout()
        detail_actions.setSpacing(8)

        select_btn = QtWidgets.QPushButton("Chọn dịch vụ cho luồng làm việc")
        select_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        select_btn.clicked.connect(self._apply_selected_staff_service_context)
        select_btn.setStyleSheet(
            "QPushButton { background: #10b981; color: white; border: none; border-radius: 8px; padding: 8px 14px; font-weight: 700; }"
            "QPushButton:hover { background: #059669; }"
        )
        select_btn.setMinimumHeight(40)

        edit_btn = QtWidgets.QPushButton("Sửa dịch vụ")
        edit_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        edit_btn.clicked.connect(lambda checked=False: self._handle_staff_service_shell_action("edit"))
        edit_btn.setStyleSheet(
            "QPushButton { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; border-radius: 8px; padding: 8px 14px; font-weight: 800; }"
            "QPushButton:hover { background: #dbeafe; }"
            "QPushButton:disabled { background: #f1f5f9; color: #94a3b8; border-color: #e2e8f0; }"
        )
        edit_btn.setMinimumHeight(40)
        edit_btn.setEnabled(False)
        edit_btn.setToolTip("Nhân viên không có quyền sửa danh mục dịch vụ thật.")

        status_btn = QtWidgets.QPushButton("Tạm ngưng / kích hoạt")
        status_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        status_btn.clicked.connect(lambda checked=False: self._handle_staff_service_shell_action("toggle"))
        status_btn.setStyleSheet(
            "QPushButton { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; border-radius: 8px; padding: 8px 14px; font-weight: 800; }"
            "QPushButton:hover { background: #ffedd5; }"
            "QPushButton:disabled { background: #f1f5f9; color: #94a3b8; border-color: #e2e8f0; }"
        )
        status_btn.setMinimumHeight(40)
        status_btn.setEnabled(False)
        status_btn.setToolTip("Nhân viên không có quyền đổi trạng thái danh mục dịch vụ thật.")

        detail_actions.addWidget(select_btn)
        detail_actions.addWidget(edit_btn)
        detail_actions.addWidget(status_btn)

        self.staff_service_feedback = QtWidgets.QLabel("")
        self.staff_service_feedback.setWordWrap(True)
        self.staff_service_feedback.setStyleSheet("font-size: 13px; color: #0f766e; font-weight: 600;")

        detail_layout = detail_card.layout()
        detail_layout.addWidget(self.staff_service_selected_label)
        detail_layout.addWidget(self.staff_service_selected_meta)
        detail_layout.addWidget(self.staff_service_selected_status_badge, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        detail_layout.addLayout(price_duration_row)
        detail_layout.addWidget(self.staff_service_description_label)
        detail_layout.addWidget(self.staff_service_process_label)
        detail_layout.addWidget(self.staff_service_notes_label)
        detail_layout.addWidget(related_title)
        detail_layout.addWidget(self.staff_service_related_list)
        detail_layout.addLayout(detail_actions)
        detail_layout.addWidget(self.staff_service_feedback)
        detail_layout.addStretch()

        content_row.addWidget(detail_card, 3)
        layout.addLayout(content_row, 1)

        self._load_staff_service_type_options()
        self._refresh_staff_service_lookup()
        self.staff_service_search_input.returnPressed.connect(self._refresh_staff_service_lookup)
        self.staff_service_type_combo.currentIndexChanged.connect(self._refresh_staff_service_lookup)
        self.staff_service_status_combo.currentIndexChanged.connect(self._refresh_staff_service_lookup)
        return page

    def _load_staff_service_type_options(self):
        services = ServiceController.get_all() or []
        self.staff_service_source_rows = services
        self.staff_service_rows = self._build_staff_service_view_rows(services)
        self.staff_service_package_rows = self._build_staff_service_package_rows(self.staff_service_rows)

        if not hasattr(self, "staff_service_type_combo"):
            return

        self.staff_service_type_combo.blockSignals(True)
        self.staff_service_type_combo.clear()
        self.staff_service_type_combo.addItem("Tất cả phân loại", "__all__")
        seen_types = set()
        for s in self.staff_service_rows + self.staff_service_package_rows:
            service_type = self._extract_staff_service_type(s)
            if service_type and service_type not in seen_types:
                seen_types.add(service_type)
                self.staff_service_type_combo.addItem(service_type, service_type)
        self.staff_service_type_combo.blockSignals(False)

    def _extract_staff_service_type(self, service):
        return str(
            service.get("service_type")
            or service.get("type")
            or service.get("category")
            or "Chưa phân loại"
        ).strip()

    def _build_staff_service_view_rows(self, services):
        rows = []
        for index, service in enumerate(services, start=1):
            normalized = dict(service or {})
            service_id = normalized.get("service_id") or index
            service_name = str(normalized.get("service_name") or normalized.get("name") or f"Dịch vụ #{service_id}").strip()
            description = str(normalized.get("description") or "").strip()
            service_type = self._infer_staff_service_category(service_name, description)
            duration = self._infer_staff_service_duration(service_name, description)
            status = self._infer_staff_service_status(normalized, index)
            normalized.update(
                {
                    "service_id": service_id,
                    "service_name": service_name,
                    "service_type": service_type,
                    "category": service_type,
                    "duration": duration,
                    "status": status,
                    "detail_kind": "service",
                    "is_package": False,
                    "summary": self._summarize_staff_service(description, service_name, service_type),
                    "description": description or self._build_staff_service_description_fallback(service_name, service_type),
                    "process_text": self._build_staff_service_process_fallback(service_name, service_type),
                    "notes_text": self._build_staff_service_notes_fallback(service_name, service_type),
                }
            )
            rows.append(normalized)
        return rows

    def _build_staff_service_package_rows(self, services):
        grouped = {}
        for service in services:
            category = self._extract_staff_service_type(service)
            grouped.setdefault(category, []).append(service)

        packages = []
        for index, (category, items) in enumerate(grouped.items(), start=1):
            package_name = self._build_staff_service_package_name(category, index)
            total_price = sum(self._coerce_staff_service_price(item.get("price")) for item in items)
            package_price = total_price * 0.92 if total_price > 0 else 0
            price_text = package_price if package_price else total_price
            active_count = sum(1 for item in items if self._normalize_staff_service_status(item.get("status")) == "active")
            package_status = "active" if active_count >= max(1, len(items) / 2) else "inactive"
            included_names = [str(item.get("service_name") or item.get("name") or "").strip() for item in items if str(item.get("service_name") or item.get("name") or "").strip()]
            package_description = (
                f"Gói tham chiếu gồm {len(included_names)} dịch vụ thuộc nhóm {category.lower()}, giúp lễ tân tư vấn nhanh khi bệnh nhân cần làm trọn bộ cùng một lượt."
            )
            packages.append(
                {
                    "service_id": f"PKG-{index:02d}",
                    "service_name": package_name,
                    "service_type": category,
                    "category": category,
                    "price": round(price_text, 2) if isinstance(price_text, float) else price_text,
                    "duration": self._build_staff_service_package_duration(items),
                    "status": package_status,
                    "detail_kind": "package",
                    "is_package": True,
                    "service_count": len(items),
                    "included_services": included_names,
                    "summary": f"{len(included_names)} dịch vụ đi kèm • ưu đãi tư vấn tại quầy",
                    "description": package_description,
                    "process_text": self._build_staff_service_package_process(category, included_names),
                    "notes_text": self._build_staff_service_package_notes(category),
                }
            )
        return packages

    @staticmethod
    def _coerce_staff_service_price(value):
        try:
            return float(value or 0)
        except (TypeError, ValueError):
            return 0.0

    def _infer_staff_service_category(self, service_name, description):
        text = f"{service_name} {description}".lower()
        if any(keyword in text for keyword in ["xét nghiệm", "máu", "nước tiểu", "test"]):
            return "Xét nghiệm"
        if any(keyword in text for keyword in ["siêu âm", "x-quang", "x quang", "ct", "mri", "hình ảnh"]):
            return "Chẩn đoán hình ảnh"
        if any(keyword in text for keyword in ["gói", "combo", "tổng quát nâng cao"]):
            return "Gói khám"
        return "Khám bệnh"

    def _infer_staff_service_duration(self, service_name, description):
        text = f"{service_name} {description}".lower()
        if "gói" in text or "combo" in text:
            return "90-120 phút"
        if any(keyword in text for keyword in ["xét nghiệm", "máu", "nước tiểu", "test"]):
            return "20-30 phút"
        if any(keyword in text for keyword in ["siêu âm", "x-quang", "ct", "mri", "hình ảnh"]):
            return "30-45 phút"
        return "15-20 phút"

    def _infer_staff_service_status(self, service, index):
        raw_status = service.get("status")
        if raw_status is not None:
            return self._normalize_staff_service_status(raw_status)
        is_active = service.get("is_active")
        if is_active is not None:
            return "active" if bool(is_active) else "inactive"
        return "inactive" if index % 5 == 0 else "active"

    @staticmethod
    def _normalize_staff_service_status(status):
        raw = str(status or "").strip().lower()
        if raw in {"active", "enabled", "available", "đang áp dụng", "dang ap dung", "1", "true"}:
            return "active"
        if raw in {"inactive", "disabled", "suspended", "tạm ngưng", "tam ngung", "0", "false"}:
            return "inactive"
        return "active"

    def _summarize_staff_service(self, description, service_name, service_type):
        if description:
            cleaned = " ".join(description.split())
            if len(cleaned) > 88:
                return cleaned[:85].rstrip() + "..."
            return cleaned
        return f"{service_name} thuộc nhóm {service_type.lower()}, đang dùng mô tả tham chiếu do dữ liệu gốc còn tối giản."

    def _build_staff_service_description_fallback(self, service_name, service_type):
        return (
            f"{service_name} hiện chưa có mô tả chi tiết trong cơ sở dữ liệu. "
            f"Hệ thống đang dùng mô tả tham chiếu theo nhóm {service_type.lower()} để nhân viên vẫn có thể tư vấn đúng ngữ cảnh."
        )

    def _build_staff_service_process_fallback(self, service_name, service_type):
        if service_type == "Xét nghiệm":
            return (
                "1. Xác nhận thông tin bệnh nhân và chỉ định.\n"
                "2. Hướng dẫn bệnh nhân tới khu lấy mẫu.\n"
                "3. Ghi nhận hoàn tất lấy mẫu và thời gian trả kết quả."
            )
        if service_type == "Chẩn đoán hình ảnh":
            return (
                "1. Kiểm tra chỉ định và lưu ý an toàn trước khi chụp/siêu âm.\n"
                "2. Điều phối bệnh nhân tới phòng cận lâm sàng phù hợp.\n"
                "3. Xác nhận thời gian bác sĩ đọc kết quả."
            )
        if service_type == "Gói khám":
            return (
                "1. Xác nhận danh sách hạng mục trong gói.\n"
                "2. Sắp xếp thứ tự thực hiện để tránh chờ lâu.\n"
                "3. Hướng dẫn bệnh nhân quay lại quầy sau khi hoàn tất toàn bộ hạng mục."
            )
        return (
            "1. Tiếp nhận nhu cầu khám và xác nhận loại dịch vụ.\n"
            "2. Chọn bác sĩ/phòng khám phù hợp để đặt lịch.\n"
            "3. Nhắc bệnh nhân theo dõi thông báo thanh toán và thời gian hẹn."
        )

    def _build_staff_service_notes_fallback(self, service_name, service_type):
        if service_type == "Xét nghiệm":
            return "Có thể cần nhịn ăn hoặc mang theo chỉ định cũ. Nếu dữ liệu chưa ghi rõ, lễ tân cần nhắc bệnh nhân xác nhận lại với điều dưỡng."
        if service_type == "Chẩn đoán hình ảnh":
            return "Kiểm tra chống chỉ định, giấy tờ liên quan và tình trạng mang thai khi phù hợp trước khi điều phối."
        if service_type == "Gói khám":
            return "Giá gói đang là giá tham chiếu gom từ các dịch vụ thành phần; lễ tân cần báo lại rằng chi tiết có thể thay đổi theo chỉ định bác sĩ."
        return f"{service_name} chưa có lưu ý chuyên biệt trong dữ liệu gốc. Dùng nội dung này như placeholder minh bạch, không thay thế hướng dẫn chuyên môn."

    def _build_staff_service_package_name(self, category, index):
        labels = {
            "Khám bệnh": "Gói khám cơ bản",
            "Xét nghiệm": "Gói xét nghiệm tổng quát",
            "Chẩn đoán hình ảnh": "Gói chẩn đoán hình ảnh",
            "Gói khám": "Gói khám tổng hợp",
        }
        base_name = labels.get(category, f"Gói dịch vụ {category}")
        return base_name if index == 1 else f"{base_name} {index}"

    def _build_staff_service_package_duration(self, items):
        count = max(1, len(items))
        minimum = 30 * count
        maximum = 40 * count
        return f"{minimum}-{maximum} phút"

    def _build_staff_service_package_process(self, category, included_names):
        service_list = ", ".join(included_names[:3]) if included_names else "các dịch vụ thành phần"
        return (
            "1. Xác nhận bệnh nhân muốn dùng gói trọn bộ thay vì từng dịch vụ lẻ.\n"
            f"2. Điều phối lần lượt các hạng mục chính: {service_list}.\n"
            "3. Tổng hợp kết quả/thông tin thanh toán sau khi hoàn tất toàn bộ hạng mục trong gói."
        )

    def _build_staff_service_package_notes(self, category):
        return (
            f"Gói khám nhóm {category.lower()} đang được dựng theo fallback UI từ danh mục hiện có, chưa phải cấu hình package chính thức trong cơ sở dữ liệu. "
            "Nhân viên cần giải thích đây là gợi ý tư vấn nhanh khi bệnh nhân hỏi combo dịch vụ."
        )

    def _build_staff_service_tab_button(self, label, tab_key, is_active):
        btn = QtWidgets.QPushButton(label)
        btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        btn.setMinimumHeight(40)
        btn.clicked.connect(lambda checked=False, key=tab_key: self._set_staff_service_active_tab(key))
        btn.setProperty("activeTab", is_active)
        btn.setStyleSheet(self._staff_service_tab_button_style(is_active))
        return btn

    @staticmethod
    def _staff_service_tab_button_style(is_active):
        if is_active:
            return (
                "QPushButton { background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; border-radius: 10px; padding: 10px 18px; font-size: 13px; font-weight: 900; }"
            )
        return (
            "QPushButton { background: #ffffff; color: #475569; border: 1px solid #dbe6f3; border-radius: 10px; padding: 10px 18px; font-size: 13px; font-weight: 800; }"
            "QPushButton:hover { background: #f8fafc; color: #0f172a; }"
        )

    def _sync_staff_service_tab_styles(self):
        for key, button in self.staff_service_tab_buttons.items():
            is_active = key == self.staff_service_active_tab
            button.setStyleSheet(self._staff_service_tab_button_style(is_active))

    def _build_staff_service_info_chip(self, title, value):
        frame = QtWidgets.QFrame()
        frame.setStyleSheet("QFrame { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; }")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("font-size: 11px; color: #64748b; font-weight: 800;")
        value_label = QtWidgets.QLabel(value)
        value_label.setWordWrap(True)
        value_label.setStyleSheet("font-size: 13px; color: #0f172a; font-weight: 900;")
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        frame.value_label = value_label
        frame.title_label = title_label
        return frame

    def _update_staff_service_info_chip(self, chip, title, value):
        chip.title_label.setText(title)
        chip.value_label.setText(value)

    def _build_staff_service_text_panel(self, title, content):
        label = QtWidgets.QLabel(self._build_staff_service_text_block(title, content))
        label.setWordWrap(True)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        label.setStyleSheet(
            "background: #ffffff; border: 1px solid #e4ebf4; border-radius: 12px; padding: 12px; font-size: 12px; color: #334155; font-weight: 700;"
        )
        return label

    @staticmethod
    def _build_staff_service_text_block(title, content):
        return f"{title}\n{content}"

    def _build_staff_service_status_badge(self, status):
        label = QtWidgets.QLabel()
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._set_staff_service_status_badge(label, status)
        return label

    def _set_staff_service_status_badge(self, label, status):
        raw_status = str(status or "").strip().lower()
        normalized = self._normalize_staff_service_status(status) if raw_status else "unknown"
        styles = {
            "active": ("Đang áp dụng", "#dcfce7", "#15803d"),
            "inactive": ("Tạm ngưng", "#fee2e2", "#b91c1c"),
            "unknown": ("Chưa chọn", "#eef2f7", "#475569"),
        }
        text, bg, fg = styles.get(normalized, ("Chưa chọn", "#eef2f7", "#475569"))
        label.setText(text)
        label.setStyleSheet(
            f"background: {bg}; color: {fg}; border-radius: 10px; padding: 4px 10px; font-size: 11px; font-weight: 900;"
        )

    def _build_staff_service_table_actions(self, row_index, service):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        for label, bg, action_key, tooltip in [
            ("👁", "#eff6ff", "view", "Xem"),
            ("✎", "#f8fafc", "edit", "Sửa"),
            ("⏻", "#fff7ed", "toggle", "Tạm ngưng/kích hoạt"),
        ]:
            btn = QtWidgets.QPushButton(label)
            btn.setFixedSize(32, 28)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setToolTip(tooltip)
            btn.setStyleSheet(f"background: {bg}; color: #2563eb; border: none; border-radius: 8px; font-weight: 900;")
            if action_key in {"edit", "toggle"}:
                btn.setEnabled(False)
                if action_key == "edit":
                    btn.setToolTip("Nhân viên không có quyền sửa danh mục dịch vụ thật.")
                else:
                    btn.setToolTip("Nhân viên không có quyền đổi trạng thái danh mục dịch vụ thật.")
            btn.clicked.connect(
                lambda checked=False, key=action_key, idx=row_index, row_service=service:
                self._handle_staff_service_shell_action(key, idx, row_service)
            )
            layout.addWidget(btn)
        return wrapper

    @staticmethod
    def _is_staff_service_catalog_mutation_action(action):
        return action in {"add", "edit", "toggle"}

    def _set_staff_service_catalog_permission_feedback(self):
        self._set_staff_service_feedback(
            "Staff chỉ có quyền tra cứu/chọn dịch vụ cho booking/billing; thao tác thêm/sửa/tạm ngưng danh mục Services do admin quản lý.",
            is_error=False,
        )

    def _handle_staff_service_shell_action(self, action_key="view", row_index=None, service=None):
        action = str(action_key or "view").strip().lower()

        if self._is_staff_service_catalog_mutation_action(action):
            self._set_staff_service_catalog_permission_feedback()
            return

        if action == "add":
            self._handle_staff_service_add_action()
            return

        target_service = self._resolve_staff_service_action_target(row_index, service)
        if not target_service:
            self._set_staff_service_feedback("Vui lòng chọn một dịch vụ trước khi thao tác.", is_error=True)
            return

        detail_kind = str(target_service.get("detail_kind") or "service")
        service_name = str(target_service.get("service_name") or target_service.get("name") or "").strip()

        if action == "view":
            self.staff_service_selected = target_service
            self._populate_staff_service_detail(target_service)
            self._set_staff_service_feedback(f"Đã mở chi tiết {service_name}.", is_error=False)
            return

        if detail_kind != "service":
            self._set_staff_service_feedback(
                "Mục đang chọn là gói khám fallback tư vấn; hệ thống chưa có persistence package chính thức nên không hỗ trợ sửa/tạm ngưng.",
                is_error=True,
            )
            return

        if action == "edit":
            self._handle_staff_service_edit_action(target_service)
            return

        if action == "toggle":
            self._handle_staff_service_toggle_action(target_service)
            return

        self._set_staff_service_feedback("Thao tác chưa được hỗ trợ.", is_error=True)

    def _resolve_staff_service_action_target(self, row_index=None, service=None):
        if isinstance(row_index, int) and 0 <= row_index < len(self.staff_service_filtered_rows):
            self._select_staff_service_row(row_index)
            return self.staff_service_filtered_rows[row_index]

        if isinstance(service, dict):
            target_id = service.get("service_id")
            target_name = str(service.get("service_name") or service.get("name") or "").strip()
            matched_row = self._find_staff_service_row_index(target_id=target_id, target_name=target_name)
            if matched_row >= 0:
                self._select_staff_service_row(matched_row)
                return self.staff_service_filtered_rows[matched_row]
            return service

        return self.staff_service_selected

    def _find_staff_service_row_index(self, target_id=None, target_name=""):
        target_name_norm = str(target_name or "").strip().lower()
        for idx, row in enumerate(self.staff_service_filtered_rows):
            row_id = row.get("service_id")
            row_name = str(row.get("service_name") or row.get("name") or "").strip().lower()
            if target_id is not None and str(row_id) == str(target_id):
                return idx
            if target_name_norm and row_name == target_name_norm:
                return idx
        return -1

    def _select_staff_service_row(self, row_index):
        if row_index < 0 or row_index >= self.staff_service_table.rowCount():
            return False
        self.staff_service_table.selectRow(row_index)
        return True

    def _reload_staff_service_data(self, preferred_service_id=None, preferred_service_name=""):
        self._load_staff_service_type_options()
        self._refresh_staff_service_lookup()

        preferred_row = self._find_staff_service_row_index(
            target_id=preferred_service_id,
            target_name=preferred_service_name,
        )
        if preferred_row >= 0:
            self._select_staff_service_row(preferred_row)
            return

        if self.staff_service_table.rowCount() > 0:
            self._select_staff_service_row(0)

    def _handle_staff_service_add_action(self):
        self._set_staff_service_catalog_permission_feedback()

    def _handle_staff_service_edit_action(self, service):
        self._set_staff_service_catalog_permission_feedback()

    def _handle_staff_service_toggle_action(self, service):
        self._set_staff_service_catalog_permission_feedback()

    @staticmethod
    def _staff_service_tab_label(tab_key):
        if tab_key == "package":
            return "Gói khám"
        return "Dịch vụ"

    def _update_staff_service_kpi_card(self, card, title, value, note, accent):
        if hasattr(card, "kpi_title_label") and hasattr(card, "kpi_value_label") and hasattr(card, "kpi_note_label"):
            card.kpi_title_label.setText(title)
            card.kpi_value_label.setText(value)
            card.kpi_value_label.setStyleSheet(f"font-size: 32px; color: {accent}; font-weight: 900;")
            card.kpi_note_label.setText(note)

    def _format_staff_service_currency(self, value):
        amount = self._coerce_staff_service_price(value)
        if amount <= 0:
            return "0 đ"
        return f"{amount:,.0f} đ".replace(",", ".")

    def _refresh_staff_service_lookup(self):
        if not hasattr(self, "staff_service_table"):
            return

        if not self.staff_service_rows and not self.staff_service_package_rows:
            self._load_staff_service_type_options()

        keyword = str(self.staff_service_search_input.text() or "").strip().lower()
        selected_type = str(self.staff_service_type_combo.currentData() or "__all__")
        selected_status = str(self.staff_service_status_combo.currentData() or "__all__")

        current_rows = self.staff_service_rows if self.staff_service_active_tab == "service" else self.staff_service_package_rows

        filtered = []
        for s in current_rows:
            service_name = str(s.get("service_name") or s.get("name") or "").strip()
            service_type = self._extract_staff_service_type(s)
            type_ok = selected_type == "__all__" or service_type == selected_type
            name_ok = not keyword or keyword in service_name.lower()
            status_ok = selected_status == "__all__" or self._normalize_staff_service_status(s.get("status")) == selected_status
            if type_ok and name_ok and status_ok:
                filtered.append(s)

        self.staff_service_filtered_rows = filtered
        self.staff_service_table.setRowCount(len(filtered))
        self.staff_service_table.clearSelection()

        for row, s in enumerate(filtered):
            service_name = str(s.get("service_name") or s.get("name") or "")
            service_type = self._extract_staff_service_type(s)
            price = self._format_staff_service_currency(s.get("price"))
            duration = str(s.get("duration") or "Chưa cập nhật")
            status = self._normalize_staff_service_status(s.get("status"))

            self.staff_service_table.setRowHeight(row, 54)
            self.staff_service_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row + 1)))
            self.staff_service_table.setItem(row, 1, QtWidgets.QTableWidgetItem(service_name))
            self.staff_service_table.setItem(row, 2, QtWidgets.QTableWidgetItem(service_type))
            self.staff_service_table.setItem(row, 3, QtWidgets.QTableWidgetItem(price))
            self.staff_service_table.setItem(row, 4, QtWidgets.QTableWidgetItem(duration))
            self.staff_service_table.setCellWidget(row, 5, self._build_staff_service_status_badge(status))
            self.staff_service_table.setCellWidget(row, 6, self._build_staff_service_table_actions(row, s))

        if not filtered:
            tab_label = "dịch vụ" if self.staff_service_active_tab == "service" else "gói khám"
            self.staff_service_lookup_empty.setText(f"Không có {tab_label} phù hợp bộ lọc hiện tại.")
            self.staff_service_table_summary.setText("Hãy đổi từ khóa, phân loại hoặc trạng thái để xem lại danh mục.")
            self.staff_service_lookup_empty.setVisible(True)
            self.staff_service_selected = None
            self._reset_staff_service_detail()
        else:
            total_rows = len(current_rows)
            self.staff_service_lookup_empty.setText(f"Hiển thị {len(filtered)}/{total_rows} mục trong danh mục hiện tại.")
            self.staff_service_table_summary.setText(
                f"Tab {self._staff_service_tab_label(self.staff_service_active_tab)} đang có {len(filtered)} mục sau khi lọc. Chọn một dòng để xem chi tiết và áp dụng nhanh sang luồng làm việc."
            )
            self.staff_service_lookup_empty.setVisible(True)

        self._refresh_staff_service_kpis()

    def _handle_clear_staff_service_filters(self):
        self.staff_service_search_input.clear()
        self.staff_service_type_combo.setCurrentIndex(0)
        self.staff_service_status_combo.setCurrentIndex(0)
        self._refresh_staff_service_lookup()
        self._set_staff_service_feedback("Đã xóa bộ lọc tra cứu.", is_error=False)

    def _handle_staff_service_selection(self):
        selected = self.staff_service_table.selectedItems()
        if not selected:
            if self.staff_service_table.selectionModel() is None or not self.staff_service_table.selectionModel().hasSelection():
                self.staff_service_selected = None
                self._reset_staff_service_detail()
            return

        row = selected[0].row()
        if row < 0 or row >= len(self.staff_service_filtered_rows):
            return

        service = self.staff_service_filtered_rows[row]
        self.staff_service_selected = service
        self._populate_staff_service_detail(service)

    def _apply_selected_staff_service_context(self):
        if not self.staff_service_selected:
            self._set_staff_service_feedback("Vui lòng chọn một dịch vụ trước khi áp dụng.", is_error=True)
            return

        detail_kind = str(self.staff_service_selected.get("detail_kind") or "service")
        service_name = str(self.staff_service_selected.get("service_name") or self.staff_service_selected.get("name") or "").strip()
        service_price = self.staff_service_selected.get("price")
        mapped_service_name = self._resolve_staff_package_context_service_name(self.staff_service_selected)

        # Use a real service name for downstream DB-backed flows.
        context_service_name = mapped_service_name if detail_kind == "package" else service_name

        if context_service_name and hasattr(self, "staff_appt_service_combo") and self.staff_appt_service_combo.count() > 0:
            service_index = self.staff_appt_service_combo.findData(context_service_name)
            if service_index < 0:
                service_index = self.staff_appt_service_combo.findText(context_service_name)
            if service_index >= 0:
                self.staff_appt_service_combo.setCurrentIndex(service_index)

        if hasattr(self, "staff_bill_amount_input") and service_price is not None:
            current_amount = str(self.staff_bill_amount_input.text() or "").strip()
            if not current_amount:
                self.staff_bill_amount_input.setText(str(service_price))

        if context_service_name and hasattr(self, "staff_bill_amount_input"):
            current_amount = str(self.staff_bill_amount_input.text() or "").strip()
            if not current_amount:
                suggested_amount = self._get_service_price_suggestion(context_service_name)
                if suggested_amount is not None:
                    self.staff_bill_amount_input.setText(str(suggested_amount))

        self.shared_selected_service_name = context_service_name
        self._apply_shared_context_to_appointment_form()
        self._apply_shared_context_to_billing_form()

        if detail_kind == "package":
            if context_service_name:
                self._set_staff_service_feedback(
                    f"Đã áp dụng gói fallback '{service_name}' theo ngữ cảnh tư vấn. Luồng đặt lịch dùng dịch vụ thành phần '{context_service_name}' để bám dữ liệu DB thật.",
                    is_error=False,
                )
                return

            self._set_staff_service_feedback(
                "Gói khám đang là fallback tư vấn và chưa ánh xạ được dịch vụ DB thật. Hệ thống chỉ giữ ngữ cảnh tham chiếu/gợi ý giá, không gán service persistence cho lịch hẹn.",
                is_error=False,
            )
            return

        self._set_staff_service_feedback(
            "Đã áp dụng dịch vụ đã chọn vào ngữ cảnh đặt lịch/thanh toán (dịch vụ lịch hẹn + gợi ý tổng tiền).",
            is_error=False,
        )

    def _resolve_staff_package_context_service_name(self, service):
        if not isinstance(service, dict):
            return ""
        if str(service.get("detail_kind") or "service") != "package":
            return str(service.get("service_name") or service.get("name") or "").strip()

        included_services = service.get("included_services") or []
        db_services = {}
        for row in self.staff_service_rows:
            row_name = str(row.get("service_name") or row.get("name") or "").strip()
            if row_name:
                db_services[row_name.lower()] = row_name

        for included_name in included_services:
            candidate = str(included_name or "").strip().lower()
            if candidate in db_services:
                return db_services[candidate]
        return ""

    def _set_staff_service_active_tab(self, tab_key):
        if tab_key not in {"service", "package"} or self.staff_service_active_tab == tab_key:
            return
        self.staff_service_active_tab = tab_key
        self._sync_staff_service_tab_styles()
        self._refresh_staff_service_lookup()
        self._set_staff_service_feedback(
            f"Đã chuyển sang tab {self._staff_service_tab_label(tab_key).lower()}.",
            is_error=False,
        )

    def _refresh_staff_service_kpis(self):
        service_count = len([row for row in self.staff_service_rows if self._normalize_staff_service_status(row.get("status")) == "active"])
        package_count = len(self.staff_service_package_rows)
        featured_rows = self.staff_service_rows[:6]
        active_revenue = sum(self._coerce_staff_service_price(row.get("price")) for row in self.staff_service_rows if self._normalize_staff_service_status(row.get("status")) == "active")

        self._update_staff_service_kpi_card(
            self.staff_service_kpi_total,
            "Dịch vụ đang áp dụng",
            str(service_count),
            "Dịch vụ active lấy từ danh mục Services hiện có",
            "#14b8a6",
        )
        self._update_staff_service_kpi_card(
            self.staff_service_kpi_packages,
            "Gói khám hiển thị",
            str(package_count),
            "Fallback theo nhóm dịch vụ, chưa ghi thành package thật trong DB",
            "#2563eb",
        )
        self._update_staff_service_kpi_card(
            self.staff_service_kpi_featured,
            "Dịch vụ nổi bật",
            str(len(featured_rows)),
            "Top mục ưu tiên tư vấn theo thứ tự danh mục hiện tại",
            "#f97316",
        )
        self._update_staff_service_kpi_card(
            self.staff_service_kpi_revenue,
            "Doanh thu tham chiếu",
            self._format_staff_service_currency(active_revenue),
            "Tổng giá active dùng làm KPI tham chiếu cho quầy lễ tân",
            "#7c3aed",
        )

    def _populate_staff_service_detail(self, service):
        service_name = str(service.get("service_name") or service.get("name") or "")
        service_type = self._extract_staff_service_type(service)
        detail_kind = service.get("detail_kind") or "service"
        status = self._normalize_staff_service_status(service.get("status"))
        price_text = self._format_staff_service_currency(service.get("price"))
        duration_text = str(service.get("duration") or "Chưa cập nhật")

        prefix = "Gói khám" if detail_kind == "package" else "Dịch vụ"
        self.staff_service_selected_label.setText(f"{prefix}: {service_name}")
        self.staff_service_selected_meta.setText(
            f"Mã: {service.get('service_id', '-') } • Phân loại: {service_type} • Hình thức: {self._staff_service_tab_label(detail_kind if detail_kind == 'package' else 'service')}"
        )
        self._set_staff_service_status_badge(self.staff_service_selected_status_badge, status)
        self._update_staff_service_info_chip(self.staff_service_price_info, "Giá", price_text)
        self._update_staff_service_info_chip(self.staff_service_duration_info, "Thời lượng", duration_text)
        self.staff_service_description_label.setText(self._build_staff_service_text_block("Mô tả", str(service.get("description") or "Chưa có mô tả.")))
        self.staff_service_process_label.setText(self._build_staff_service_text_block("Quy trình thực hiện", str(service.get("process_text") or "Chưa có quy trình.")))
        self.staff_service_notes_label.setText(self._build_staff_service_text_block("Lưu ý", str(service.get("notes_text") or "Chưa có lưu ý.")))
        self._populate_staff_service_related(service)
        self._set_staff_service_feedback(
            f"Đang xem chi tiết {service_name}. Có thể áp dụng nhanh sang luồng đặt lịch/thanh toán nếu phù hợp.",
            is_error=False,
        )

    def _reset_staff_service_detail(self):
        if not hasattr(self, "staff_service_selected_label"):
            return
        self.staff_service_selected_label.setText("Chưa chọn dịch vụ nào.")
        self.staff_service_selected_meta.setText("Chọn một dòng ở bảng bên trái để xem trạng thái, giá và thông tin triển khai.")
        self._set_staff_service_status_badge(self.staff_service_selected_status_badge, "unknown")
        self._update_staff_service_info_chip(self.staff_service_price_info, "Giá", "Chưa có dữ liệu")
        self._update_staff_service_info_chip(self.staff_service_duration_info, "Thời lượng", "Chưa có dữ liệu")
        self.staff_service_description_label.setText(
            self._build_staff_service_text_block(
                "Mô tả",
                "Mô tả dịch vụ sẽ hiển thị ở đây. Nếu cơ sở dữ liệu chưa có nội dung, hệ thống sẽ dùng placeholder rõ ràng để nhân viên vẫn có ngữ cảnh tư vấn.",
            )
        )
        self.staff_service_process_label.setText(
            self._build_staff_service_text_block(
                "Quy trình thực hiện",
                "Chưa có quy trình chi tiết từ dữ liệu hiện tại. Hệ thống sẽ hiển thị quy trình tham chiếu theo loại dịch vụ/gói khám.",
            )
        )
        self.staff_service_notes_label.setText(
            self._build_staff_service_text_block(
                "Lưu ý",
                "Chưa có lưu ý chuyên biệt. Vui lòng xác nhận lại với bác sĩ/phòng cận lâm sàng khi tư vấn dịch vụ có chuẩn bị đặc biệt.",
            )
        )
        self.staff_service_related_list.clear()
        self.staff_service_related_list.addItem("Chọn một dịch vụ để xem danh sách thường được chọn kèm.")

    def _populate_staff_service_related(self, service):
        self.staff_service_related_list.clear()
        related_items = self._build_staff_service_related_rows(service)
        for item in related_items:
            self.staff_service_related_list.addItem(item)

    def _build_staff_service_related_rows(self, service):
        if service.get("detail_kind") == "package":
            included = service.get("included_services") or []
            if included:
                return [f"☑ {name}" for name in included]
            return ["☑ Gói khám này chưa có danh sách thành phần chi tiết."]

        service_type = self._extract_staff_service_type(service)
        current_name = str(service.get("service_name") or "").strip().lower()
        candidates = []
        for row in self.staff_service_rows:
            if str(row.get("service_name") or "").strip().lower() == current_name:
                continue
            if self._extract_staff_service_type(row) == service_type:
                candidates.append(f"☑ {row.get('service_name')} • {self._format_staff_service_currency(row.get('price'))}")
            if len(candidates) == 3:
                break
        if candidates:
            return candidates
        return [
            "☑ Chưa có dữ liệu liên kết thật trong DB. Dùng nhóm cùng phân loại làm gợi ý tư vấn an toàn.",
        ]

    def _apply_shared_context_to_appointment_form(self):
        if not hasattr(self, "staff_appt_patient_id_input") or not hasattr(self, "staff_appt_service_combo"):
            return

        self._apply_shared_line_edit_value(
            self.staff_appt_patient_id_input,
            self.shared_selected_patient_id,
            self._shared_appt_context_patient_id,
        )
        self._apply_shared_service_selection(
            self.staff_appt_service_combo,
            self.shared_selected_service_name,
            self._shared_appt_context_service_name,
        )

        self._shared_appt_context_patient_id = self.shared_selected_patient_id
        self._shared_appt_context_service_name = self.shared_selected_service_name

    def _apply_shared_context_to_billing_form(self):
        if not hasattr(self, "staff_bill_patient_id_input") or not hasattr(self, "staff_bill_appointment_id_input"):
            return

        self._apply_shared_line_edit_value(
            self.staff_bill_patient_id_input,
            self.shared_selected_patient_id,
            self._shared_billing_context_patient_id,
        )
        self._apply_shared_line_edit_value(
            self.staff_bill_appointment_id_input,
            self.shared_selected_appointment_id,
            self._shared_billing_context_appointment_id,
        )

        suggested_amount = None
        if self.shared_selected_service_name:
            suggested_amount = self._get_service_price_suggestion(self.shared_selected_service_name)
        self._apply_shared_line_edit_value(
            self.staff_bill_amount_input,
            suggested_amount,
            self._shared_billing_context_amount,
        )

        self._shared_billing_context_patient_id = self.shared_selected_patient_id
        self._shared_billing_context_appointment_id = self.shared_selected_appointment_id
        self._shared_billing_context_service_name = self.shared_selected_service_name
        self._shared_billing_context_amount = suggested_amount

    @staticmethod
    def _apply_shared_line_edit_value(widget, shared_value, previous_shared_value):
        current_text = str(widget.text() or "").strip()
        previous_text = str(previous_shared_value or "").strip()
        next_text = str(shared_value or "").strip()
        current_matches_previous = current_text == previous_text

        # Only override fields that are empty or still reflect the previous auto-filled context.
        if next_text:
            if not current_text or current_matches_previous:
                widget.setText(next_text)
            return

        if current_matches_previous:
            widget.clear()

    @staticmethod
    def _apply_shared_service_selection(combo_box, shared_service_name, previous_shared_service_name):
        previous_service = str(previous_shared_service_name or "").strip()
        current_data = str(combo_box.currentData() or "").strip()
        current_text = str(combo_box.currentText() or "").strip()
        current_matches_previous = bool(previous_service) and (current_data == previous_service or current_text == previous_service)
        next_service = str(shared_service_name or "").strip()

        if next_service:
            service_index = combo_box.findData(next_service)
            if service_index < 0:
                service_index = combo_box.findText(next_service)
            if service_index >= 0 and (not current_text or current_matches_previous):
                combo_box.setCurrentIndex(service_index)
            elif service_index < 0 and current_matches_previous and combo_box.count() > 0:
                combo_box.setCurrentIndex(0)
            return

        if current_matches_previous and combo_box.count() > 0:
            combo_box.setCurrentIndex(0)

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
        try:
            doctors = DoctorController.get_all() or []
        except Exception:
            doctors = []
        for doctor in doctors:
            name = str(doctor.get("name") or doctor.get("doctor_name") or doctor.get("full_name") or "").strip()
            if name and name not in options:
                options.append(name)
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
            self.staff_patient_feedback.setText(
                f"Hiển thị {start + 1}-{end} / {total} bệnh nhân"
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

        emergency = str(patient.get("emergency_contact") or "Chưa cập nhật")
        blood = str(patient.get("blood_type") or "Chưa cập nhật")
        allergy = str(patient.get("allergies") or "Chưa cập nhật")
        occupation = str(patient.get("job") or patient.get("occupation") or "Chưa cập nhật")

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
        self.staff_patient_note_text.setPlainText(note or "Chưa có ghi chú.")

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

    @staticmethod
    def _build_staff_patient_mock_data():
        return []

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
        if not payload:
            self._set_staff_appt_feedback("Không thể chuẩn bị dữ liệu tạo lịch hẹn.", is_error=True)
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

        if not isinstance(result, dict):
            result = {"status": False, "message": "Không thể tạo lịch hẹn."}

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
        if not payload:
            self._set_staff_appt_feedback("Không thể chuẩn bị dữ liệu cập nhật lịch hẹn.", is_error=True)
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

        if not isinstance(result, dict):
            result = {"status": False, "message": "Không thể cập nhật lịch hẹn."}

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
        page.setStyleSheet("background: #f8fbff; border: none;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        heading = QtWidgets.QLabel("Thanh toán & Hóa đơn")
        heading.setStyleSheet("font-size: 24px; color: #0f172a; font-weight: 900;")
        sub = QtWidgets.QLabel(
            "Theo dõi hóa đơn tại quầy theo trạng thái, tìm nhanh lịch hẹn cần thu tiền và xem chi tiết biên nhận an toàn ngay trên cùng một màn hình."
        )
        sub.setStyleSheet("font-size: 13px; color: #64748b;")
        sub.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(sub)

        self.staff_bill_kpi_row = QtWidgets.QHBoxLayout()
        self.staff_bill_kpi_row.setSpacing(12)
        layout.addLayout(self.staff_bill_kpi_row)

        shell_row = QtWidgets.QHBoxLayout()
        shell_row.setSpacing(12)

        center_panel = QtWidgets.QFrame()
        center_panel.setStyleSheet("background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;")
        center_layout = QtWidgets.QVBoxLayout(center_panel)
        center_layout.setContentsMargins(16, 16, 16, 16)
        center_layout.setSpacing(12)

        header_row = QtWidgets.QHBoxLayout()
        header_row.setSpacing(10)
        header_col = QtWidgets.QVBoxLayout()
        header_col.setSpacing(3)
        header_title = QtWidgets.QLabel("Danh sách hóa đơn")
        header_title.setStyleSheet("font-size: 16px; color: #0f172a; font-weight: 900;")
        header_sub = QtWidgets.QLabel("Tập trung vào các hóa đơn cần thu ngay trong ca trực, có sẵn trạng thái, tìm kiếm và lọc theo thời gian.")
        header_sub.setWordWrap(True)
        header_sub.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        header_col.addWidget(header_title)
        header_col.addWidget(header_sub)
        header_row.addLayout(header_col, 1)

        refresh_btn = QtWidgets.QPushButton("↻ Làm mới")
        refresh_btn.clicked.connect(self._refresh_staff_billing_table)
        refresh_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        refresh_btn.setStyleSheet(
            "QPushButton { background: #ffffff; color: #334155; border: 1px solid #cbd5e1; border-radius: 8px; padding: 8px 14px; font-weight: 800; }"
            "QPushButton:hover { border-color: #94a3b8; background: #f8fafc; }"
        )
        header_row.addWidget(refresh_btn)
        center_layout.addLayout(header_row)

        tabs_row = QtWidgets.QHBoxLayout()
        tabs_row.setSpacing(8)
        self.staff_bill_status_buttons = {}
        self.staff_bill_status_group = QtWidgets.QButtonGroup(self)
        self.staff_bill_status_group.setExclusive(True)
        for index, (label, status_key) in enumerate([
            ("Tất cả hóa đơn", "__all__"),
            ("Chờ thanh toán", "unpaid"),
            ("Đã thanh toán", "paid"),
            ("Đã hủy", "cancelled"),
            ("Hoàn tiền", "refunded"),
        ]):
            btn = QtWidgets.QPushButton(label)
            btn.setCheckable(True)
            btn.setChecked(index == 0)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(
                "QPushButton { background: #f8fafc; color: #475569; border: 1px solid #e2e8f0; border-radius: 10px; padding: 8px 14px; font-size: 12px; font-weight: 800; }"
                "QPushButton:checked { background: #e7f8ef; color: #0f9f6e; border-color: #b7ebd0; }"
            )
            btn.clicked.connect(lambda checked, key=status_key: self._set_staff_billing_status_filter(key) if checked else None)
            self.staff_bill_status_group.addButton(btn)
            self.staff_bill_status_buttons[status_key] = btn
            tabs_row.addWidget(btn)
        tabs_row.addStretch()
        center_layout.addLayout(tabs_row)

        filter_row = QtWidgets.QHBoxLayout()
        filter_row.setSpacing(8)
        self.staff_bill_search_input = QtWidgets.QLineEdit()
        self.staff_bill_search_input.setPlaceholderText("Tìm theo mã hóa đơn, bệnh nhân, lịch hẹn, dịch vụ...")
        self.staff_bill_search_input.setStyleSheet(
            "QLineEdit { padding: 8px 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 12px; }"
            "QLineEdit:focus { border-color: #1A9B6C; }"
        )
        self.staff_bill_search_input.returnPressed.connect(self._refresh_staff_billing_table)

        self.staff_bill_period_combo = QtWidgets.QComboBox()
        self.staff_bill_period_combo.addItem("Tất cả thời gian", "__all__")
        self.staff_bill_period_combo.addItem("Hôm nay", "today")
        self.staff_bill_period_combo.addItem("7 ngày gần đây", "7d")
        self.staff_bill_period_combo.addItem("30 ngày gần đây", "30d")
        self.staff_bill_period_combo.setMinimumWidth(160)
        self.staff_bill_period_combo.setStyleSheet("QComboBox { padding: 7px 8px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 12px; }")
        self.staff_bill_period_combo.currentIndexChanged.connect(self._refresh_staff_billing_table)

        search_btn = QtWidgets.QPushButton("Tìm kiếm")
        search_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        search_btn.clicked.connect(self._refresh_staff_billing_table)
        search_btn.setStyleSheet(
            "QPushButton { background: #1A9B6C; color: white; border: none; border-radius: 8px; padding: 8px 14px; font-weight: 800; }"
            "QPushButton:hover { background: #168a60; }"
        )

        clear_btn = QtWidgets.QPushButton("Xóa lọc")
        clear_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        clear_btn.clicked.connect(self._handle_clear_staff_billing_filters)
        clear_btn.setStyleSheet(
            "QPushButton { background: #ffffff; color: #475569; border: 1px solid #cbd5e1; border-radius: 8px; padding: 8px 14px; font-weight: 800; }"
            "QPushButton:hover { background: #f8fafc; border-color: #94a3b8; }"
        )

        filter_row.addWidget(self.staff_bill_search_input, 1)
        filter_row.addWidget(self.staff_bill_period_combo)
        filter_row.addWidget(search_btn)
        filter_row.addWidget(clear_btn)
        center_layout.addLayout(filter_row)

        self.staff_bill_table = QtWidgets.QTableWidget()
        self.staff_bill_table.setColumnCount(7)
        self.staff_bill_table.setHorizontalHeaderLabels(
            ["Mã hóa đơn", "Bệnh nhân", "Lịch hẹn", "Thời điểm", "Tổng tiền", "Trạng thái", "Biên nhận"]
        )
        self.staff_bill_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staff_bill_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_bill_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_bill_table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_bill_table.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.staff_bill_table.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self.staff_bill_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.staff_bill_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_bill_table.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.staff_bill_table.setShowGrid(False)
        self.staff_bill_table.verticalHeader().setVisible(False)
        self.staff_bill_table.setMinimumHeight(360)
        self.staff_bill_table.setStyleSheet(
            "QTableWidget { background: #ffffff; border: 1px solid #e7edf5; border-radius: 12px; }"
            "QHeaderView::section { background: #f8fafc; color: #1f2937; font-size: 12px; font-weight: 800; border: none; padding: 10px; }"
            "QTableWidget::item { border-bottom: 1px solid #edf2f7; padding: 8px; color: #0f172a; font-weight: 600; }"
        )
        self.staff_bill_table.itemSelectionChanged.connect(self._on_staff_billing_row_selected)
        center_layout.addWidget(self.staff_bill_table, 1)

        self.staff_bill_empty_state = QtWidgets.QLabel("Chưa có hóa đơn nào khớp với bộ lọc hiện tại.")
        self.staff_bill_empty_state.setWordWrap(True)
        self.staff_bill_empty_state.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.staff_bill_empty_state.setStyleSheet(
            "font-size: 12px; color: #64748b; font-weight: 700; padding: 16px;"
            "background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 10px;"
        )
        center_layout.addWidget(self.staff_bill_empty_state)

        self.staff_bill_feedback = QtWidgets.QLabel("Sẵn sàng xử lý thanh toán tại quầy.")
        self.staff_bill_feedback.setWordWrap(True)
        self.staff_bill_feedback.setStyleSheet("font-size: 12px; color: #475569; font-weight: 700;")
        center_layout.addWidget(self.staff_bill_feedback)

        right_panel = QtWidgets.QFrame()
        right_panel.setStyleSheet("background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px;")
        right_layout = QtWidgets.QVBoxLayout(right_panel)
        right_layout.setContentsMargins(14, 14, 14, 14)
        right_layout.setSpacing(10)

        detail_title = QtWidgets.QLabel("Chi tiết hóa đơn")
        detail_title.setStyleSheet("font-size: 15px; color: #0f172a; font-weight: 900;")
        right_layout.addWidget(detail_title)

        self.staff_bill_detail_placeholder = QtWidgets.QLabel(
            "Chọn một hóa đơn trong bảng để xem bệnh nhân, trạng thái thanh toán và thông tin biên nhận chi tiết."
        )
        self.staff_bill_detail_placeholder.setWordWrap(True)
        self.staff_bill_detail_placeholder.setStyleSheet(
            "font-size: 12px; color: #64748b; padding: 10px; background: #ffffff; border: 1px dashed #cbd5e1; border-radius: 10px;"
        )
        right_layout.addWidget(self.staff_bill_detail_placeholder)

        patient_card = QtWidgets.QFrame()
        patient_card.setStyleSheet("QFrame { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; }")
        patient_layout = QtWidgets.QVBoxLayout(patient_card)
        patient_layout.setContentsMargins(12, 12, 12, 12)
        patient_layout.setSpacing(6)
        patient_title = QtWidgets.QLabel("Bệnh nhân & ca khám")
        patient_title.setStyleSheet("font-size: 12px; color: #334155; font-weight: 800;")
        patient_layout.addWidget(patient_title)
        self.staff_bill_detail_patient_name = QtWidgets.QLabel("Chưa chọn hóa đơn")
        self.staff_bill_detail_patient_name.setWordWrap(True)
        self.staff_bill_detail_patient_name.setStyleSheet("font-size: 14px; color: #0f172a; font-weight: 900;")
        patient_layout.addWidget(self.staff_bill_detail_patient_name)
        self.staff_bill_detail_patient_meta = QtWidgets.QLabel("Mã BN: -  •  SĐT: -")
        self.staff_bill_detail_patient_meta.setWordWrap(True)
        self.staff_bill_detail_patient_meta.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 700;")
        patient_layout.addWidget(self.staff_bill_detail_patient_meta)
        self.staff_bill_detail_status_badge = QtWidgets.QLabel("Chưa chọn")
        self.staff_bill_detail_status_badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.staff_bill_detail_status_badge.setStyleSheet(
            "background: #f1f5f9; color: #64748b; border-radius: 10px; padding: 5px 10px; font-size: 11px; font-weight: 900;"
        )
        patient_layout.addWidget(self.staff_bill_detail_status_badge, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        right_layout.addWidget(patient_card)

        info_card = QtWidgets.QFrame()
        info_card.setStyleSheet("QFrame { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; }")
        info_grid = QtWidgets.QGridLayout(info_card)
        info_grid.setContentsMargins(12, 12, 12, 12)
        info_grid.setHorizontalSpacing(8)
        info_grid.setVerticalSpacing(8)
        billing_detail_headers = [
            ("Mã hóa đơn", "staff_bill_detail_code_label"),
            ("Lịch hẹn", "staff_bill_detail_appointment_label"),
            ("Dịch vụ", "staff_bill_detail_service_label"),
            ("Thời điểm", "staff_bill_detail_date_label"),
            ("Tổng tiền", "staff_bill_detail_amount_label"),
            ("Nhân viên thu", "staff_bill_detail_collector_label"),
            ("Ghi chú", "staff_bill_detail_note_label"),
        ]
        for row_idx, (title_text, attr_name) in enumerate(billing_detail_headers):
            title_lb = QtWidgets.QLabel(f"{title_text}:")
            title_lb.setStyleSheet("font-size: 12px; color: #334155; font-weight: 800;")
            value_lb = QtWidgets.QLabel("-")
            value_lb.setWordWrap(True)
            value_lb.setStyleSheet("font-size: 12px; color: #0f172a; font-weight: 700;")
            setattr(self, attr_name, value_lb)
            info_grid.addWidget(title_lb, row_idx, 0)
            info_grid.addWidget(value_lb, row_idx, 1)
        right_layout.addWidget(info_card)

        timeline_card = QtWidgets.QFrame()
        timeline_card.setStyleSheet("QFrame { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; }")
        timeline_layout = QtWidgets.QVBoxLayout(timeline_card)
        timeline_layout.setContentsMargins(12, 12, 12, 12)
        timeline_layout.setSpacing(4)
        timeline_title = QtWidgets.QLabel("Timeline thanh toán")
        timeline_title.setStyleSheet("font-size: 12px; color: #334155; font-weight: 800;")
        timeline_layout.addWidget(timeline_title)
        self.staff_bill_timeline_labels = []
        for _ in range(3):
            lb = QtWidgets.QLabel("• Chưa có dữ liệu")
            lb.setWordWrap(True)
            lb.setStyleSheet("font-size: 12px; color: #475569; font-weight: 700;")
            timeline_layout.addWidget(lb)
            self.staff_bill_timeline_labels.append(lb)
        right_layout.addWidget(timeline_card)

        quick_form_card = QtWidgets.QFrame()
        quick_form_card.setStyleSheet("QFrame { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; }")
        quick_form_layout = QtWidgets.QVBoxLayout(quick_form_card)
        quick_form_layout.setContentsMargins(12, 12, 12, 12)
        quick_form_layout.setSpacing(8)
        quick_form_title = QtWidgets.QLabel("Tạo hóa đơn nhanh")
        quick_form_title.setStyleSheet("font-size: 13px; color: #0f172a; font-weight: 900;")
        quick_form_layout.addWidget(quick_form_title)

        self.staff_bill_patient_id_input = QtWidgets.QLineEdit()
        self.staff_bill_patient_id_input.setPlaceholderText("Patient ID")
        self.staff_bill_patient_id_input.setStyleSheet(
            "QLineEdit { padding: 8px 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 12px; }"
            "QLineEdit:focus { border-color: #1A9B6C; }"
        )

        self.staff_bill_appointment_id_input = QtWidgets.QLineEdit()
        self.staff_bill_appointment_id_input.setPlaceholderText("Appointment ID")
        self.staff_bill_appointment_id_input.setStyleSheet(
            "QLineEdit { padding: 8px 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 12px; }"
            "QLineEdit:focus { border-color: #1A9B6C; }"
        )

        self.staff_bill_amount_input = QtWidgets.QLineEdit()
        self.staff_bill_amount_input.setPlaceholderText("Tổng tiền (VND)")
        self.staff_bill_amount_input.setStyleSheet(
            "QLineEdit { padding: 8px 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 12px; }"
            "QLineEdit:focus { border-color: #1A9B6C; }"
        )

        form_grid = QtWidgets.QGridLayout()
        form_grid.setHorizontalSpacing(8)
        form_grid.setVerticalSpacing(8)
        form_grid.addWidget(QtWidgets.QLabel("Patient ID:"), 0, 0)
        form_grid.addWidget(self.staff_bill_patient_id_input, 0, 1)
        form_grid.addWidget(QtWidgets.QLabel("Appointment ID:"), 1, 0)
        form_grid.addWidget(self.staff_bill_appointment_id_input, 1, 1)
        form_grid.addWidget(QtWidgets.QLabel("Tổng tiền:"), 2, 0)
        form_grid.addWidget(self.staff_bill_amount_input, 2, 1)
        quick_form_layout.addLayout(form_grid)

        create_btn = QtWidgets.QPushButton("+ Tạo hóa đơn")
        create_btn.clicked.connect(self._handle_staff_create_invoice)
        create_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        create_btn.setStyleSheet(
            "QPushButton { background: #2563eb; color: white; border: none; border-radius: 8px; padding: 9px 14px; font-weight: 800; }"
            "QPushButton:hover { background: #1d4ed8; }"
        )
        quick_form_layout.addWidget(create_btn)
        right_layout.addWidget(quick_form_card)

        action_block = QtWidgets.QHBoxLayout()
        action_block.setSpacing(8)
        self.staff_bill_confirm_btn = QtWidgets.QPushButton("✓ Xác nhận thu tiền")
        self.staff_bill_print_btn = QtWidgets.QPushButton("🖨 In biên nhận")
        for btn in [self.staff_bill_confirm_btn, self.staff_bill_print_btn]:
            btn.setEnabled(False)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(
                "QPushButton { padding: 8px 10px; border: 1px solid #cbd5e1; border-radius: 8px; background: #ffffff; font-size: 11px; font-weight: 800; color: #334155; }"
                "QPushButton:hover { border-color: #94a3b8; }"
                "QPushButton:disabled { background: #f1f5f9; color: #94a3b8; border-color: #e2e8f0; }"
            )
        self.staff_bill_confirm_btn.clicked.connect(self._handle_staff_confirm_payment)
        self.staff_bill_print_btn.clicked.connect(self._handle_staff_print_receipt)
        action_block.addWidget(self.staff_bill_confirm_btn)
        action_block.addWidget(self.staff_bill_print_btn)
        right_layout.addLayout(action_block)
        right_layout.addStretch()

        shell_row.addWidget(center_panel, 65)
        shell_row.addWidget(right_panel, 35)
        layout.addLayout(shell_row, 1)

        self._refresh_staff_billing_table()
        return page

    def _refresh_staff_billing_table(self):
        selected_id = self.staff_billing_selected_id
        try:
            payments = PaymentController.get_all() or []
        except Exception:
            payments = []
            self._set_staff_billing_feedback("Không thể tải danh sách hóa đơn tạm thời. Vui lòng thử lại.", is_error=True)

        try:
            patient_rows = PatientController.get_all() or []
        except Exception:
            patient_rows = []

        try:
            appointment_rows = AppointmentController.get_all() or []
        except Exception:
            appointment_rows = []

        patient_map = {str(row.get("patient_id") or row.get("id") or ""): row for row in patient_rows}
        appointment_map = {str(row.get("appointment_id") or row.get("id") or ""): row for row in appointment_rows}

        enriched_rows = []
        for payment in payments:
            patient_id = payment.get("patient_id")
            appointment_id = payment.get("appointment_id")
            patient = patient_map.get(str(patient_id or ""), {})
            appointment = appointment_map.get(str(appointment_id or ""), {})
            normalized_status = self._normalize_staff_billing_status(payment.get("status"))
            time_value = (
                payment.get("payment_date")
                or payment.get("created_at")
                or payment.get("appointment_date")
                or appointment.get("appointment_date")
                or ""
            )
            service_name = str(
                payment.get("service_name")
                or self._extract_service_name_from_note(str(appointment.get("note") or ""))
                or appointment.get("service_name")
                or "Chưa gán dịch vụ"
            ).strip()
            fallback_patient_name = f"Bệnh nhân #{patient_id}" if patient_id not in (None, "") else "Chưa rõ bệnh nhân"
            patient_name = str(
                payment.get("patient_name")
                or patient.get("name")
                or patient.get("full_name")
                or fallback_patient_name
            ).strip()
            patient_phone = str(payment.get("patient_phone") or patient.get("phone") or "Chưa có SĐT").strip()
            collector_name = str(
                payment.get("staff_name")
                or payment.get("collected_by")
                or payment.get("updated_by")
                or (self.username if normalized_status == "paid" else "Chưa ghi nhận")
            ).strip()
            detail_note = str(
                payment.get("note")
                or appointment.get("reason")
                or appointment.get("note")
                or "Không có ghi chú thêm"
            ).strip()
            total_amount = payment.get("total_amount") or payment.get("amount") or 0
            enriched_rows.append({
                **payment,
                "status": normalized_status,
                "invoice_code": self._staff_billing_code(payment.get("payment_id")),
                "patient_name": patient_name,
                "patient_phone": patient_phone,
                "appointment_code": self._staff_appointment_code(appointment_id),
                "service_name": service_name,
                "collector_name": collector_name,
                "time_value": time_value,
                "time_display": self._format_staff_billing_datetime(time_value),
                "appointment_time_display": self._format_staff_billing_datetime(appointment.get("appointment_date") or time_value),
                "detail_note": detail_note,
                "total_amount": total_amount,
            })

        self.staff_billing_rows = enriched_rows
        self.staff_billing_filtered_rows = []
        self.staff_billing_selected_id = None
        self.staff_billing_selected_payment = None
        self.staff_billing_selected_status = ""
        self._update_staff_billing_kpis(enriched_rows)

        keyword = str(self.staff_bill_search_input.text() or "").strip().lower() if hasattr(self, "staff_bill_search_input") else ""
        period_key = str(self.staff_bill_period_combo.currentData() or "__all__") if hasattr(self, "staff_bill_period_combo") else "__all__"
        filtered_rows = []
        for payment in enriched_rows:
            if self.staff_billing_status_filter != "__all__" and payment.get("status") != self.staff_billing_status_filter:
                continue
            if keyword and keyword not in self._build_staff_billing_search_text(payment):
                continue
            if not self._staff_billing_matches_period(payment.get("time_value"), period_key):
                continue
            filtered_rows.append(payment)

        self.staff_billing_filtered_rows = filtered_rows
        self.staff_bill_table.setRowCount(len(filtered_rows))
        matched_row_index = -1
        for row_idx, payment in enumerate(filtered_rows):
            self.staff_bill_table.setRowHeight(row_idx, 56)
            self.staff_bill_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(payment.get("invoice_code") or "-")))
            self.staff_bill_table.setItem(
                row_idx,
                1,
                QtWidgets.QTableWidgetItem(
                    f"{payment.get('patient_name') or 'Chưa rõ bệnh nhân'}\n{payment.get('patient_phone') or 'Chưa có SĐT'}"
                ),
            )
            self.staff_bill_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(payment.get("appointment_code") or "-")))
            self.staff_bill_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(payment.get("time_display") or "-")))
            self.staff_bill_table.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(self._format_staff_billing_amount(payment.get("total_amount"))))
            self.staff_bill_table.setCellWidget(row_idx, 5, self._build_staff_billing_status_badge(str(payment.get("status") or "unpaid")))
            receipt_text = "Sẵn sàng in" if payment.get("status") == "paid" else "Chờ xác nhận"
            self.staff_bill_table.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(receipt_text))
            if str(payment.get("payment_id")) == str(selected_id):
                matched_row_index = row_idx

        has_rows = bool(filtered_rows)
        self.staff_bill_empty_state.setVisible(not has_rows)
        if has_rows:
            target_row_index = 0
            if matched_row_index >= 0:
                target_row_index = matched_row_index
            self.staff_bill_table.selectRow(target_row_index)
            self._sync_staff_billing_selection_by_row(target_row_index, set_feedback=False)
        else:
            empty_message = "Chưa có hóa đơn nào trong hệ thống." if not enriched_rows else "Không có hóa đơn khớp với từ khóa hoặc bộ lọc thời gian hiện tại."
            self._update_staff_billing_detail(None, empty_message)
            self._set_staff_billing_feedback(empty_message, is_error=False)

    def _on_staff_billing_row_selected(self):
        selected_rows = self.staff_bill_table.selectionModel().selectedRows()
        if not selected_rows:
            current_row = self.staff_bill_table.currentRow()
            if current_row >= 0:
                self._sync_staff_billing_selection_by_row(current_row)
                return
            self._reset_staff_billing_selection_state()
            return

        row = selected_rows[0].row()
        self._sync_staff_billing_selection_by_row(row)

    def _reset_staff_billing_selection_state(self):
        self.staff_billing_selected_id = None
        self.staff_billing_selected_payment = None
        self.staff_billing_selected_status = ""
        self._update_staff_billing_detail(None)

    def _sync_staff_billing_selection_by_row(self, row, set_feedback=True):
        if row < 0 or row >= len(self.staff_billing_filtered_rows):
            self._reset_staff_billing_selection_state()
            return

        selected_payment = self.staff_billing_filtered_rows[row]
        self.staff_billing_selected_id = selected_payment.get("payment_id")
        self.staff_billing_selected_payment = selected_payment
        self.staff_billing_selected_status = str(selected_payment.get("status", "unpaid"))
        self.shared_selected_patient_id = selected_payment.get("patient_id")
        self.shared_selected_appointment_id = selected_payment.get("appointment_id")
        self._update_staff_billing_detail(selected_payment)
        if set_feedback:
            self._set_staff_billing_feedback(
                f"Đã chọn {selected_payment.get('invoice_code') or self.staff_billing_selected_id} - {self._staff_billing_status_label(self.staff_billing_selected_status).lower()}.",
                is_error=False,
            )

    def _handle_staff_create_invoice(self):
        if self.staff_billing_action_in_progress:
            self._set_staff_billing_feedback("Hệ thống đang xử lý thao tác trước đó. Vui lòng chờ một chút.", is_error=True)
            return

        patient_raw = self.staff_bill_patient_id_input.text().strip()
        appointment_raw = self.staff_bill_appointment_id_input.text().strip()
        amount_raw = self.staff_bill_amount_input.text().strip()

        if not patient_raw or not appointment_raw or not amount_raw:
            self._set_staff_billing_feedback("Vui lòng nhập đủ Patient ID, Appointment ID và tổng tiền.", is_error=True)
            return

        normalized_amount = amount_raw.replace(",", "").replace(".", "")
        try:
            patient_id = int(patient_raw)
            appointment_id = int(appointment_raw)
            total_amount = float(normalized_amount)
        except ValueError:
            self._set_staff_billing_feedback("Patient ID, Appointment ID phải là số và tổng tiền phải hợp lệ.", is_error=True)
            return

        if total_amount <= 0:
            self._set_staff_billing_feedback("Tổng tiền phải lớn hơn 0.", is_error=True)
            return

        try:
            appts = AppointmentController.get_by_patient(patient_id) or []
        except Exception:
            appts = []
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

        duplicate_payment = self._find_staff_billing_duplicate_by_appointment(appointment_id)
        if duplicate_payment is not None:
            self._set_staff_billing_feedback(
                f"Lịch hẹn #{appointment_id} đã có hóa đơn #{duplicate_payment.get('payment_id')}. Không thể tạo trùng.",
                is_error=True,
            )
            return

        self.staff_billing_action_in_progress = True
        self._sync_staff_billing_action_buttons()
        try:
            ok = PaymentController.create(patient_id, appointment_id, total_amount)
        except Exception:
            self._set_staff_billing_feedback(
                "Tạo hóa đơn bị gián đoạn tạm thời. Vui lòng thử lại.",
                is_error=True,
            )
            self.staff_billing_action_in_progress = False
            self._sync_staff_billing_action_buttons()
            return
        self.staff_billing_action_in_progress = False
        self._sync_staff_billing_action_buttons()
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

    def _find_staff_billing_duplicate_by_appointment(self, appointment_id):
        candidate_rows = list(self.staff_billing_rows or [])
        if not candidate_rows:
            try:
                payments = PaymentController.get_all() or []
            except Exception:
                payments = []
            candidate_rows = [row for row in payments if isinstance(row, dict)]

        for payment in candidate_rows:
            try:
                current_appt_id = int(payment.get("appointment_id", -1))
            except (TypeError, ValueError):
                continue
            if current_appt_id == int(appointment_id):
                return payment
        return None

    def _handle_clear_staff_billing_filters(self):
        if hasattr(self, "staff_bill_search_input"):
            self.staff_bill_search_input.clear()
        if hasattr(self, "staff_bill_period_combo"):
            self.staff_bill_period_combo.setCurrentIndex(0)
        self._set_staff_billing_status_filter("__all__")

    def _set_staff_billing_status_filter(self, status_key):
        self.staff_billing_status_filter = status_key or "__all__"
        button = getattr(self, "staff_bill_status_buttons", {}).get(self.staff_billing_status_filter)
        if button and not button.isChecked():
            button.setChecked(True)
        self._refresh_staff_billing_table()

    def _update_staff_billing_kpis(self, payments):
        if not hasattr(self, "staff_bill_kpi_row"):
            return

        while self.staff_bill_kpi_row.count():
            item = self.staff_bill_kpi_row.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        unpaid_rows = [row for row in payments if row.get("status") == "unpaid"]
        paid_rows = [row for row in payments if row.get("status") == "paid"]
        unpaid_total = sum(self._staff_billing_amount_value(row.get("total_amount")) for row in unpaid_rows)
        paid_total = sum(self._staff_billing_amount_value(row.get("total_amount")) for row in paid_rows)
        total_rows = len(payments)
        completion_rate = round((len(paid_rows) / total_rows) * 100) if total_rows else 0

        cards = [
            self._build_kpi_card("Hóa đơn toàn ca", str(total_rows), "Tổng số hóa đơn đã ghi nhận trong hệ thống", "#2563eb", "#eaf2ff", "🧾"),
            self._build_kpi_card("Chờ thanh toán", str(len(unpaid_rows)), self._format_staff_billing_amount(unpaid_total), "#f97316", "#fff3e4", "⏳"),
            self._build_kpi_card("Đã thanh toán", str(len(paid_rows)), self._format_staff_billing_amount(paid_total), "#16a34a", "#e7f8ef", "✓"),
            self._build_kpi_card("Tỷ lệ hoàn tất", f"{completion_rate}%", "Theo số lượng hóa đơn đã được xác nhận thu tiền", "#6d48d8", "#f0eaff", "📈"),
        ]
        for card in cards:
            self.staff_bill_kpi_row.addWidget(card)

    def _update_staff_billing_detail(self, payment=None, empty_message=None):
        if not hasattr(self, "staff_bill_detail_placeholder"):
            return

        if not payment:
            self.staff_bill_detail_placeholder.setText(
                empty_message or "Chọn một hóa đơn trong bảng để xem bệnh nhân, trạng thái thanh toán và thông tin biên nhận chi tiết."
            )
            self.staff_bill_detail_patient_name.setText("Chưa chọn hóa đơn")
            self.staff_bill_detail_patient_meta.setText("Mã BN: -  •  SĐT: -")
            self.staff_bill_detail_status_badge.setText("Chưa chọn")
            self.staff_bill_detail_status_badge.setStyleSheet(
                "background: #f1f5f9; color: #64748b; border-radius: 10px; padding: 5px 10px; font-size: 11px; font-weight: 900;"
            )
            self.staff_bill_detail_code_label.setText("-")
            self.staff_bill_detail_appointment_label.setText("-")
            self.staff_bill_detail_service_label.setText("-")
            self.staff_bill_detail_date_label.setText("-")
            self.staff_bill_detail_amount_label.setText("-")
            self.staff_bill_detail_collector_label.setText("-")
            self.staff_bill_detail_note_label.setText("-")
            for lb in self.staff_bill_timeline_labels:
                lb.setText("• Chưa có dữ liệu")
            self.staff_bill_confirm_btn.setEnabled(False)
            self.staff_bill_print_btn.setEnabled(False)
            self._sync_staff_billing_action_buttons()
            return

        status_key = str(payment.get("status") or "unpaid")
        status_label = self._staff_billing_status_label(status_key)
        patient_id = payment.get("patient_id")
        appointment_id = payment.get("appointment_id")
        self.staff_bill_detail_placeholder.setText(f"Đang xem {payment.get('invoice_code') or self._staff_billing_code(payment.get('payment_id'))}")
        self.staff_bill_detail_patient_name.setText(str(payment.get("patient_name") or "Chưa rõ bệnh nhân"))
        self.staff_bill_detail_patient_meta.setText(
            f"Mã BN: {patient_id if patient_id not in (None, '') else '-'}  •  SĐT: {payment.get('patient_phone') or 'Chưa có SĐT'}"
        )
        self.staff_bill_detail_status_badge.setText(status_label)
        self.staff_bill_detail_status_badge.setStyleSheet(self._staff_billing_badge_style(status_key))
        self.staff_bill_detail_code_label.setText(str(payment.get("invoice_code") or "-"))
        self.staff_bill_detail_appointment_label.setText(
            f"{payment.get('appointment_code') or self._staff_appointment_code(appointment_id)} • {payment.get('appointment_time_display') or '-'}"
        )
        self.staff_bill_detail_service_label.setText(str(payment.get("service_name") or "Chưa gán dịch vụ"))
        self.staff_bill_detail_date_label.setText(str(payment.get("time_display") or "-"))
        self.staff_bill_detail_amount_label.setText(self._format_staff_billing_amount(payment.get("total_amount")))
        self.staff_bill_detail_collector_label.setText(str(payment.get("collector_name") or "Chưa ghi nhận"))
        self.staff_bill_detail_note_label.setText(str(payment.get("detail_note") or "Không có ghi chú"))

        timeline_entries = [
            f"• {payment.get('time_display') or '--'} | Hóa đơn tạo cho {payment.get('appointment_code') or self._staff_appointment_code(appointment_id)}",
            f"• {payment.get('appointment_time_display') or '--'} | Dịch vụ: {payment.get('service_name') or 'Chưa gán dịch vụ'}",
            f"• {payment.get('collector_name') or 'Chưa ghi nhận'} | Trạng thái hiện tại: {status_label}",
        ]
        for index, lb in enumerate(self.staff_bill_timeline_labels):
            lb.setText(timeline_entries[index] if index < len(timeline_entries) else "• Chưa có dữ liệu")

        self.staff_bill_confirm_btn.setEnabled(status_key != "paid")
        self.staff_bill_print_btn.setEnabled(status_key == "paid")
        self._sync_staff_billing_action_buttons()

    def _sync_staff_billing_action_buttons(self):
        if not hasattr(self, "staff_bill_confirm_btn") or not hasattr(self, "staff_bill_print_btn"):
            return
        if self.staff_billing_action_in_progress:
            self.staff_bill_confirm_btn.setEnabled(False)
            self.staff_bill_print_btn.setEnabled(False)

    @staticmethod
    def _staff_billing_amount_value(value):
        try:
            return float(value or 0)
        except (TypeError, ValueError):
            return 0.0

    def _format_staff_billing_amount(self, amount):
        value = self._staff_billing_amount_value(amount)
        return f"{value:,.0f} đ".replace(",", ".")

    @staticmethod
    def _staff_billing_code(payment_id):
        try:
            return f"HD{int(payment_id):06d}"
        except (TypeError, ValueError):
            return str(payment_id or "HD------")

    @staticmethod
    def _staff_appointment_code(appointment_id):
        try:
            return f"LH{int(appointment_id):06d}"
        except (TypeError, ValueError):
            return str(appointment_id or "LH------")

    @staticmethod
    def _normalize_staff_billing_status(status):
        value = str(status or "unpaid").strip().lower()
        mapping = {
            "pending": "unpaid",
            "unpaid": "unpaid",
            "waiting": "unpaid",
            "paid": "paid",
            "completed": "paid",
            "success": "paid",
            "cancelled": "cancelled",
            "canceled": "cancelled",
            "void": "cancelled",
            "refunded": "refunded",
            "refund": "refunded",
            "returned": "refunded",
        }
        return mapping.get(value, value or "unpaid")

    @staticmethod
    def _staff_billing_status_label(status):
        return {
            "unpaid": "Chờ thanh toán",
            "paid": "Đã thanh toán",
            "cancelled": "Đã hủy",
            "refunded": "Đã hoàn tiền",
        }.get(status, status or "Không rõ")

    def _staff_billing_badge_style(self, status):
        styles = {
            "unpaid": ("#fff0df", "#f97316"),
            "paid": ("#dcfce7", "#16a34a"),
            "cancelled": ("#fee2e2", "#ef4444"),
            "refunded": ("#ede9fe", "#7c3aed"),
        }
        bg, fg = styles.get(status, ("#eef2f7", "#334155"))
        return f"background: {bg}; color: {fg}; border-radius: 10px; padding: 5px 10px; font-size: 11px; font-weight: 900;"

    def _build_staff_billing_status_badge(self, status):
        label = QtWidgets.QLabel(self._staff_billing_status_label(status))
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(self._staff_billing_badge_style(status))
        return label

    def _build_staff_billing_search_text(self, payment):
        search_parts = [
            payment.get("invoice_code"),
            payment.get("patient_name"),
            payment.get("patient_phone"),
            payment.get("appointment_code"),
            payment.get("service_name"),
            payment.get("collector_name"),
            payment.get("payment_id"),
            payment.get("patient_id"),
            payment.get("appointment_id"),
        ]
        return " ".join(str(part or "").lower() for part in search_parts)

    def _staff_billing_matches_period(self, value, period_key):
        if period_key == "__all__":
            return True

        dt_value = self._parse_staff_billing_datetime(value)
        if not dt_value.isValid():
            return False

        today = QtCore.QDate.currentDate()
        payment_date = dt_value.date()
        if period_key == "today":
            return payment_date == today
        if period_key == "7d":
            return payment_date >= today.addDays(-6)
        if period_key == "30d":
            return payment_date >= today.addDays(-29)
        return True

    def _parse_staff_billing_datetime(self, value):
        raw_text = str(value or "").strip()
        if not raw_text:
            return QtCore.QDateTime()

        normalized = raw_text.replace("T", " ").split(".", 1)[0]
        datetime_formats = [
            "yyyy-MM-dd HH:mm:ss",
            "yyyy-MM-dd HH:mm",
            "yyyy/MM/dd HH:mm:ss",
            "yyyy/MM/dd HH:mm",
            "dd/MM/yyyy HH:mm:ss",
            "dd/MM/yyyy HH:mm",
        ]
        for fmt in datetime_formats:
            parsed = QtCore.QDateTime.fromString(normalized, fmt)
            if parsed.isValid():
                return parsed

        date_formats = ["yyyy-MM-dd", "yyyy/MM/dd", "dd/MM/yyyy"]
        for fmt in date_formats:
            parsed_date = QtCore.QDate.fromString(normalized, fmt)
            if parsed_date.isValid():
                return QtCore.QDateTime(parsed_date, QtCore.QTime(0, 0))
        return QtCore.QDateTime()

    def _format_staff_billing_datetime(self, value):
        parsed = self._parse_staff_billing_datetime(value)
        if parsed.isValid():
            return parsed.toString("dd/MM/yyyy HH:mm")
        text = str(value or "").strip()
        return text or "Chưa có thời gian"

    @staticmethod
    def _normalize_staff_notification_appointment_status(status):
        normalized = str(status or "").strip().lower().replace("-", "_").replace(" ", "_")
        alias_map = {
            "scheduled": "pending",
            "waiting": "pending",
            "pending": "pending",
            "confirmed": "confirmed",
            "in_progress": "in_progress",
            "inprogress": "in_progress",
            "ongoing": "in_progress",
            "done": "done",
            "completed": "done",
            "complete": "done",
            "cancelled": "cancelled",
            "canceled": "cancelled",
            "cancel": "cancelled",
        }
        return alias_map.get(normalized, normalized)

    def _resolve_staff_notification_payment_time(self, payment):
        if not isinstance(payment, dict):
            return ""

        # Prefer payment_date because it reflects actual payment workflow time.
        candidate_fields = ["payment_date", "created_at", "appointment_date", "date"]
        for field_name in candidate_fields:
            value = payment.get(field_name)
            if value not in (None, ""):
                return value
        return ""

    def _staff_notification_sort_key(self, row):
        dt_value = self._parse_staff_billing_datetime(row.get("time_raw"))
        if dt_value.isValid():
            return (
                1,
                dt_value.toString("yyyyMMddHHmmss"),
                str(row.get("id") or ""),
            )
        return (
            0,
            str(row.get("time_raw") or row.get("time_display") or ""),
            str(row.get("id") or ""),
        )

    def _handle_staff_confirm_payment(self):
        if self.staff_billing_action_in_progress:
            self._set_staff_billing_feedback("Hệ thống đang xử lý thao tác trước đó. Vui lòng chờ một chút.", is_error=True)
            return

        if not self.staff_billing_selected_id:
            self._set_staff_billing_feedback("Vui lòng chọn hóa đơn trước khi xác nhận thanh toán.", is_error=True)
            return

        if self.staff_billing_selected_status == "paid":
            self._set_staff_billing_feedback(
                f"Hóa đơn #{self.staff_billing_selected_id} đã ở trạng thái paid. Không thể xác nhận lần nữa.",
                is_error=True,
            )
            return

        selected_payment = self.staff_billing_selected_payment if isinstance(self.staff_billing_selected_payment, dict) else {}
        invoice_amount_value = self._staff_billing_amount_value(selected_payment.get("total_amount"))
        if invoice_amount_value <= 0:
            self._set_staff_billing_feedback(
                "Không thể xác nhận thu tiền vì tổng tiền hóa đơn không hợp lệ.",
                is_error=True,
            )
            return

        paid_input, accepted = QtWidgets.QInputDialog.getText(
            self,
            "Xác nhận thu tiền",
            "Nhập số tiền khách đưa (VND):",
            text=f"{invoice_amount_value:.0f}",
        )
        if not accepted:
            self._set_staff_billing_feedback("Đã hủy thao tác xác nhận thanh toán.", is_error=False)
            return

        paid_text = str(paid_input or "").strip().replace(",", "").replace(".", "")
        if not paid_text:
            self._set_staff_billing_feedback("Vui lòng nhập số tiền khách đưa để xác nhận thu tiền.", is_error=True)
            return

        try:
            paid_value = float(paid_text)
        except ValueError:
            self._set_staff_billing_feedback("Số tiền khách đưa không hợp lệ.", is_error=True)
            return

        if paid_value < invoice_amount_value:
            missing_amount = invoice_amount_value - paid_value
            self._set_staff_billing_feedback(
                f"Khách đưa thiếu {self._format_staff_billing_amount(missing_amount)}. Không thể xác nhận paid.",
                is_error=True,
            )
            return

        self.staff_billing_action_in_progress = True
        self._sync_staff_billing_action_buttons()
        try:
            ok = PaymentController.update_status(self.staff_billing_selected_id, "paid")
        except Exception:
            self._set_staff_billing_feedback(
                "Xác nhận thanh toán bị gián đoạn tạm thời. Vui lòng thử lại.",
                is_error=True,
            )
            self.staff_billing_action_in_progress = False
            self._sync_staff_billing_action_buttons()
            return
        self.staff_billing_action_in_progress = False
        self._sync_staff_billing_action_buttons()
        if not ok:
            self._set_staff_billing_feedback("Xác nhận thanh toán thất bại. Vui lòng thử lại.", is_error=True)
            return

        change_amount = paid_value - invoice_amount_value
        paid_id = self.staff_billing_selected_id
        self._refresh_staff_billing_table()
        self._set_staff_billing_feedback(
            f"Đã xác nhận thanh toán hóa đơn #{paid_id}. Tiền thừa cần trả: {self._format_staff_billing_amount(change_amount)}.",
            is_error=False,
        )

    def _handle_staff_print_receipt(self):
        if self.staff_billing_action_in_progress:
            self._set_staff_billing_feedback("Hệ thống đang xử lý thao tác trước đó. Vui lòng chờ một chút.", is_error=True)
            return

        if not self.staff_billing_selected_id:
            self._set_staff_billing_feedback("Vui lòng chọn hóa đơn để in biên nhận.", is_error=True)
            return

        normalized_status = self._normalize_staff_billing_status(self.staff_billing_selected_status)
        if normalized_status != "paid":
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
        if not hasattr(self, "staff_appt_detail_placeholder"):
            return
        self._update_staff_appt_right_panel(None)

    def _set_staff_appointment_detail(self, appt):
        if not hasattr(self, "staff_appt_detail_placeholder"):
            return
        self._update_staff_appt_right_panel(appt)
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
        selected_id = self.staff_notification_selected_id
        read_state_by_id = {
            str(row.get("id")): bool(row.get("read"))
            for row in self.staff_notification_rows
            if isinstance(row, dict) and row.get("id") is not None
        }
        rows = []
        try:
            appts = AppointmentController.get_all() or []
        except Exception:
            appts = []
        try:
            payments = PaymentController.get_all() or []
        except Exception:
            payments = []

        for appt in appts:
            appt_id = appt.get("appointment_id")
            patient_id = appt.get("patient_id")
            doctor_name = str(appt.get("doctor_name") or "(chưa phân công)").strip()
            fallback_patient = f"Bệnh nhân #{patient_id}" if patient_id not in (None, "") else "Chưa rõ bệnh nhân"
            patient_name = str(appt.get("patient_name") or fallback_patient).strip()
            status = self._normalize_staff_notification_appointment_status(appt.get("status") or "pending")
            when_raw = appt.get("appointment_date") or appt.get("date") or ""
            when_display = self._format_staff_billing_datetime(when_raw)

            if status in {"pending", "confirmed"}:
                title = "Lịch hẹn cần xác nhận"
                message = f"Lịch hẹn #{appt_id or '-'} của {patient_name} với BS {doctor_name} cần theo dõi xác nhận."
                priority = "new"
            elif status == "cancelled":
                title = "Lịch hẹn đã hủy"
                message = f"Lịch hẹn #{appt_id or '-'} của {patient_name} đã bị hủy, cần gọi xác nhận lại nếu cần."
                priority = "urgent"
            elif status == "in_progress":
                title = "Bệnh nhân đang chờ khám"
                message = f"{patient_name} đang trong luồng khám của lịch hẹn #{appt_id or '-'} (BS {doctor_name})."
                priority = "watch"
            elif status == "done":
                title = "Lịch hẹn đã hoàn tất"
                message = f"Lịch hẹn #{appt_id or '-'} của {patient_name} đã hoàn tất với BS {doctor_name}."
                priority = "watch"
            else:
                continue

            row_id = f"appointment:{appt_id or len(rows)}:{status}"
            rows.append({
                "id": row_id,
                "category": "appointment",
                "title": title,
                "message": message,
                "time_raw": when_raw,
                "time_display": when_display,
                "priority": priority,
                "read": read_state_by_id.get(row_id, False),
                "source_page": 2,
                "source_id": appt_id,
            })

        for payment in payments:
            payment_id = payment.get("payment_id")
            patient_id = payment.get("patient_id")
            payment_status = str(payment.get("status") or "unpaid").lower().strip()
            if payment_status == "paid":
                continue

            when_raw = self._resolve_staff_notification_payment_time(payment)
            when_display = self._format_staff_billing_datetime(when_raw)
            amount_text = self._format_staff_billing_amount(payment.get("total_amount") or payment.get("amount") or 0)
            message = (
                f"Hóa đơn #{payment_id or '-'} của bệnh nhân #{patient_id if patient_id not in (None, '') else '-'} "
                f"chưa thanh toán ({amount_text})."
            )
            row_id = f"payment:{payment_id or len(rows)}:{payment_status}"
            rows.append({
                "id": row_id,
                "category": "payment",
                "title": "Hóa đơn chưa thu",
                "message": message,
                "time_raw": when_raw,
                "time_display": when_display,
                "priority": "urgent",
                "read": read_state_by_id.get(row_id, False),
                "source_page": 4,
                "source_id": payment_id,
            })

        # Keep deterministic ordering by parsed datetime first, then text fallback.
        rows.sort(key=self._staff_notification_sort_key, reverse=True)
        self.staff_notification_rows = rows
        self._apply_staff_notification_filters(preferred_selected_id=selected_id)

    def _set_staff_notification_tab(self, tab_key):
        self.staff_notification_active_tab = tab_key or "all"
        self._refresh_staff_notification_tab_styles()
        self._apply_staff_notification_filters(preferred_selected_id=self.staff_notification_selected_id)

    def _refresh_staff_notification_tab_styles(self):
        styles = {
            "active": (
                "QPushButton { background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; border-radius: 8px; padding: 8px 12px; font-size: 12px; font-weight: 900; }"
                "QPushButton:hover { background: #dbeafe; }"
            ),
            "inactive": (
                "QPushButton { background: #ffffff; color: #334155; border: 1px solid #dbe4ee; border-radius: 8px; padding: 8px 12px; font-size: 12px; font-weight: 800; }"
                "QPushButton:hover { background: #f8fafc; }"
            ),
        }
        for tab_key, button in getattr(self, "staff_notification_tab_buttons", {}).items():
            is_active = tab_key == self.staff_notification_active_tab
            button.blockSignals(True)
            button.setChecked(is_active)
            button.blockSignals(False)
            button.setStyleSheet(styles["active"] if is_active else styles["inactive"])

    @staticmethod
    def _staff_notification_priority_label(priority_key):
        return {
            "new": "Mới",
            "watch": "Theo dõi",
            "urgent": "Cần xử lý",
        }.get(priority_key, "Không rõ")

    @staticmethod
    def _staff_notification_category_label(category_key):
        return {
            "appointment": "Lịch hẹn",
            "payment": "Thanh toán",
            "system": "Hệ thống",
        }.get(category_key, "Hệ thống")

    def _build_staff_notification_search_text(self, row):
        parts = [
            row.get("id"),
            row.get("title"),
            row.get("message"),
            row.get("time_display"),
            row.get("category"),
            row.get("priority"),
            row.get("source_id"),
        ]
        return " ".join(str(part or "").lower() for part in parts)

    def _update_staff_notification_kpis(self, rows):
        total_count = len(rows)
        appointment_count = len([row for row in rows if row.get("category") == "appointment"])
        payment_count = len([row for row in rows if row.get("category") == "payment"])
        system_count = len([row for row in rows if row.get("category") == "system"])
        unread_count = len([row for row in rows if not row.get("read")])

        self.staff_notification_kpi_total.kpi_value_label.setText(str(total_count))
        self.staff_notification_kpi_appointment.kpi_value_label.setText(str(appointment_count))
        self.staff_notification_kpi_payment.kpi_value_label.setText(str(payment_count))
        self.staff_notification_kpi_system.kpi_value_label.setText(str(system_count))

        self.staff_notification_kpi_total.kpi_note_label.setText(f"{unread_count} chưa đọc")
        self.staff_notification_kpi_appointment.kpi_note_label.setText("Nguồn: AppointmentController.get_all")
        self.staff_notification_kpi_payment.kpi_note_label.setText("Nguồn: PaymentController.get_all")
        self.staff_notification_kpi_system.kpi_note_label.setText("Dùng cho fallback thông báo nội bộ")

    def _apply_staff_notification_filters(self, preferred_selected_id=None):
        keyword = str(self.staff_notification_search_input.text() or "").strip().lower() if hasattr(self, "staff_notification_search_input") else ""
        if hasattr(self, "staff_notification_priority_combo"):
            self.staff_notification_priority_filter = str(self.staff_notification_priority_combo.currentData() or "__all__")
        else:
            self.staff_notification_priority_filter = "__all__"

        filtered_rows = []
        for row in self.staff_notification_rows:
            category = str(row.get("category") or "system")
            is_read = bool(row.get("read"))
            if self.staff_notification_active_tab == "unread" and is_read:
                continue
            if self.staff_notification_active_tab in {"appointment", "payment", "system"} and category != self.staff_notification_active_tab:
                continue
            if self.staff_notification_priority_filter != "__all__" and row.get("priority") != self.staff_notification_priority_filter:
                continue
            if keyword and keyword not in self._build_staff_notification_search_text(row):
                continue
            filtered_rows.append(row)

        self.staff_notification_filtered_rows = filtered_rows
        self._update_staff_notification_kpis(self.staff_notification_rows)
        self._render_staff_notification_table(preferred_selected_id=preferred_selected_id)

    def _clear_staff_notification_filters(self):
        if hasattr(self, "staff_notification_search_input"):
            self.staff_notification_search_input.clear()
        if hasattr(self, "staff_notification_priority_combo"):
            self.staff_notification_priority_combo.setCurrentIndex(0)
        self.staff_notification_active_tab = "all"
        self._refresh_staff_notification_tab_styles()
        self._apply_staff_notification_filters(preferred_selected_id=self.staff_notification_selected_id)

    def _render_staff_notification_table(self, preferred_selected_id=None):
        rows = self.staff_notification_filtered_rows
        self.staff_notification_table.setRowCount(len(rows))
        selected_row_index = -1

        for row_idx, row in enumerate(rows):
            self.staff_notification_table.setRowHeight(row_idx, 54)
            self.staff_notification_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(self._staff_notification_category_label(row.get("category"))))
            self.staff_notification_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(row.get("message") or "-")))
            self.staff_notification_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(row.get("time_display") or "Chưa có thời gian")))
            priority_item = QtWidgets.QTableWidgetItem(self._staff_notification_priority_label(row.get("priority")))
            if row.get("priority") == "urgent":
                priority_item.setForeground(QtGui.QColor("#b91c1c"))
            elif row.get("priority") == "watch":
                priority_item.setForeground(QtGui.QColor("#b45309"))
            else:
                priority_item.setForeground(QtGui.QColor("#1d4ed8"))
            priority_font = priority_item.font()
            priority_font.setBold(True)
            priority_item.setFont(priority_font)
            self.staff_notification_table.setItem(row_idx, 3, priority_item)
            self.staff_notification_table.setItem(row_idx, 4, QtWidgets.QTableWidgetItem("Đã đọc" if row.get("read") else "Chưa đọc"))

            if str(row.get("id")) == str(preferred_selected_id):
                selected_row_index = row_idx

        has_rows = bool(rows)
        self.staff_notification_empty_state.setVisible(not has_rows)
        self.staff_notification_table_summary.setText(
            f"Đang hiển thị {len(rows)}/{len(self.staff_notification_rows)} thông báo theo tab và bộ lọc hiện tại."
        )

        if has_rows:
            if selected_row_index < 0:
                selected_row_index = 0
            self.staff_notification_table.selectRow(selected_row_index)
            self._handle_staff_notification_selection()
            self._set_staff_notification_feedback(f"Đã tải {len(rows)} thông báo hiển thị ({len(self.staff_notification_rows)} tổng).", is_error=False)
        else:
            self.staff_notification_selected_id = None
            self._update_staff_notification_detail(None)
            self._set_staff_notification_feedback("Không có thông báo khớp bộ lọc hiện tại.", is_error=False)

    def _handle_staff_notification_selection(self):
        selected_row = self.staff_notification_table.currentRow()
        if selected_row < 0 or selected_row >= len(self.staff_notification_filtered_rows):
            self.staff_notification_selected_id = None
            self._update_staff_notification_detail(None)
            return

        selected_data = self.staff_notification_filtered_rows[selected_row]
        self.staff_notification_selected_id = selected_data.get("id")
        self._update_staff_notification_detail(selected_data)

    def _update_staff_notification_detail(self, row=None):
        if not row:
            self.staff_notification_detail_placeholder.setText(
                "Chọn thông báo trong danh sách để xem nội dung, nguồn dữ liệu và thao tác xử lý."
            )
            self.staff_notification_detail_type.setText("Loại: -")
            self.staff_notification_detail_priority.setText("Mức độ: -")
            self.staff_notification_detail_time.setText("Thời điểm: -")
            self.staff_notification_detail_source.setText("Nguồn dữ liệu: -")
            self.staff_notification_detail_message.setText("Nội dung: -")
            self.staff_notification_open_source_btn.setEnabled(False)
            self.staff_notification_mark_read_btn.setEnabled(False)
            return

        self.staff_notification_detail_placeholder.setText(f"Đang xem: {row.get('title') or 'Thông báo'}")
        self.staff_notification_detail_type.setText(f"Loại: {self._staff_notification_category_label(row.get('category'))}")
        self.staff_notification_detail_priority.setText(
            f"Mức độ: {self._staff_notification_priority_label(row.get('priority'))} • {'Đã đọc' if row.get('read') else 'Chưa đọc'}"
        )
        self.staff_notification_detail_time.setText(f"Thời điểm: {row.get('time_display') or 'Chưa có thời gian'}")
        self.staff_notification_detail_source.setText(
            f"Nguồn dữ liệu: page index {row.get('source_page')} • id: {row.get('source_id') or '-'}"
        )
        self.staff_notification_detail_message.setText(f"Nội dung: {row.get('message') or '-'}")
        self.staff_notification_open_source_btn.setEnabled(True)
        self.staff_notification_mark_read_btn.setEnabled(not bool(row.get("read")))

    def _handle_staff_notification_open_source(self):
        if not self.staff_notification_selected_id:
            self._set_staff_notification_feedback("Vui lòng chọn một thông báo để mở nguồn dữ liệu.", is_error=True)
            return

        selected = None
        for row in self.staff_notification_filtered_rows:
            if str(row.get("id")) == str(self.staff_notification_selected_id):
                selected = row
                break

        if not selected:
            self._set_staff_notification_feedback("Không tìm thấy dữ liệu nguồn cho thông báo đã chọn.", is_error=True)
            return

        source_page = selected.get("source_page")
        if isinstance(source_page, int):
            self.switch_page(source_page)
            focus_ok = self._focus_staff_notification_source(selected)
            if focus_ok:
                self._set_staff_notification_feedback("Đã mở đúng bản ghi nguồn dữ liệu liên quan.", is_error=False)
            else:
                self._set_staff_notification_feedback(
                    "Đã chuyển sang màn hình nguồn nhưng không focus được đúng bản ghi. Vui lòng kiểm tra danh sách đầy đủ theo bộ lọc hiện tại.",
                    is_error=True,
                )
        else:
            self._set_staff_notification_feedback("Thông báo này chưa có liên kết nguồn dữ liệu cụ thể.", is_error=True)

    def _focus_staff_notification_source(self, row):
        if not isinstance(row, dict):
            return False

        source_page = row.get("source_page")
        source_id = row.get("source_id")
        if source_id in (None, ""):
            return False

        if source_page == 2 and hasattr(self, "staff_appt_table"):
            self._refresh_staff_appointment_table()
            visible_rows = self.staff_appointment_rows[: self.staff_appt_table.rowCount()]
            for row_idx, appt in enumerate(visible_rows):
                if str(appt.get("appointment_id")) == str(source_id):
                    self.staff_appt_table.selectRow(row_idx)
                    self._handle_staff_appointment_selection()
                    return True
        elif source_page == 4 and hasattr(self, "staff_bill_table"):
            self._refresh_staff_billing_table()
            for row_idx, payment in enumerate(self.staff_billing_filtered_rows):
                if str(payment.get("payment_id")) == str(source_id):
                    self.staff_bill_table.selectRow(row_idx)
                    self._sync_staff_billing_selection_by_row(row_idx, set_feedback=False)
                    return True
            if self.staff_billing_status_filter != "__all__":
                self.staff_billing_status_filter = "__all__"
                button = getattr(self, "staff_bill_status_buttons", {}).get("__all__")
                if button and not button.isChecked():
                    button.setChecked(True)
                self._refresh_staff_billing_table()
                for row_idx, payment in enumerate(self.staff_billing_filtered_rows):
                    if str(payment.get("payment_id")) == str(source_id):
                        self.staff_bill_table.selectRow(row_idx)
                        self._sync_staff_billing_selection_by_row(row_idx, set_feedback=False)
                        return True
        return False

    def _mark_notification_as_handled(self):
        if not self.staff_notification_selected_id:
            self._set_staff_notification_feedback("Vui lòng chọn một thông báo để đánh dấu đã xử lý.", is_error=True)
            return

        selected_data = None
        for row in self.staff_notification_rows:
            if str(row.get("id")) == str(self.staff_notification_selected_id):
                selected_data = row
                break

        if not selected_data:
            self._set_staff_notification_feedback("Không thể xác định thông báo để cập nhật trạng thái đọc.", is_error=True)
            return

        if selected_data.get("read"):
            self._set_staff_notification_feedback("Thông báo đã ở trạng thái đã đọc.", is_error=False)
            return

        selected_data["read"] = True
        message_preview = str(selected_data.get("message") or "Thông báo")
        self._apply_staff_notification_filters(preferred_selected_id=self.staff_notification_selected_id)
        self._set_staff_notification_feedback(f"Đã đánh dấu đã đọc: {message_preview}", is_error=False)

    def _set_staff_notification_feedback(self, message, is_error=False):
        self.staff_notification_feedback.setText(message)
        color = "#b91c1c" if is_error else "#166534"
        self.staff_notification_feedback.setStyleSheet(f"font-size: 12px; color: {color}; font-weight: 600;")

    def _refresh_staff_reports(self):
        total_patients = 0
        total_appointments = 0
        paid_total = 0.0
        data_warning = False

        try:
            core_totals = ReportController.get_core_totals() or {}
        except Exception:
            core_totals = {}

        if isinstance(core_totals, dict):
            total_patients = int(self._staff_billing_amount_value(core_totals.get("total_patients")))
            total_appointments = int(self._staff_billing_amount_value(core_totals.get("total_appointments")))
            paid_total = self._staff_billing_amount_value(core_totals.get("total_revenue"))

        total_patients = max(total_patients, 0)
        total_appointments = max(total_appointments, 0)
        paid_total = max(paid_total, 0.0)

        try:
            appointments = AppointmentController.get_all() or []
        except Exception:
            appointments = []
            data_warning = True
        if not isinstance(appointments, list):
            appointments = []
            data_warning = True
        try:
            payments = PaymentController.get_all() or []
        except Exception:
            payments = []
            data_warning = True
        if not isinstance(payments, list):
            payments = []
            data_warning = True

        period_key = self._staff_report_selected_period()
        doctor_key = self._staff_report_selected_doctor()
        metric_mode = self._staff_report_selected_metric_mode()
        self.staff_report_metric_mode = metric_mode

        filtered_appts = self._filter_staff_report_appointments(appointments, period_key, doctor_key)
        filtered_payments = self._filter_staff_report_payments(payments, period_key)

        unpaid_total = 0.0
        unpaid_rows = []
        paid_rows_count = 0
        for payment in filtered_payments:
            if not isinstance(payment, dict):
                continue
            amount = max(self._staff_billing_amount_value(payment.get("total_amount")), 0.0)
            status_key = self._normalize_staff_billing_status(payment.get("status"))
            if status_key == "paid":
                paid_rows_count += 1
                continue
            unpaid_total += amount
            unpaid_rows.append(payment)

        status_counts = {
            "pending": 0,
            "confirmed": 0,
            "in_progress": 0,
            "done": 0,
            "cancelled": 0,
            "other": 0,
        }
        for appt in filtered_appts:
            if not isinstance(appt, dict):
                continue
            normalized_status = self._normalize_staff_notification_appointment_status(appt.get("status"))
            if normalized_status in status_counts:
                status_counts[normalized_status] += 1
            else:
                status_counts["other"] += 1

        self._refresh_staff_report_doctor_filter_options(filtered_appts)
        self._render_staff_report_kpis(
            total_patients,
            total_appointments,
            paid_total,
            unpaid_total,
            len(filtered_appts),
            paid_rows_count,
            metric_mode,
        )
        self._render_staff_report_status_table(status_counts)
        self._render_staff_report_unpaid_table(unpaid_rows)
        self._render_staff_report_placeholder(total_appointments, paid_total, unpaid_total, len(filtered_appts), period_key, metric_mode)

        if total_appointments == 0 and total_patients == 0 and paid_total == 0 and unpaid_total == 0:
            self.staff_report_summary_lbl.setText("Chưa có dữ liệu vận hành để tổng hợp. Vui lòng kiểm tra sau khi phát sinh lịch hẹn/hóa đơn.")
        else:
            period_label = self.staff_report_period_combo.currentText() if hasattr(self, "staff_report_period_combo") else "bộ lọc hiện tại"
            doctor_label = self.staff_report_doctor_combo.currentText() if hasattr(self, "staff_report_doctor_combo") else "Tất cả bác sĩ"
            metric_label = self._staff_report_metric_label(metric_mode).lower()
            self.staff_report_summary_lbl.setText(
                f"Bộ lọc {period_label.lower()} • {doctor_label.lower()}: hệ thống theo dõi {total_patients} hồ sơ bệnh nhân, "
                f"{len(filtered_appts)} lịch hẹn phù hợp, đã thu {int(paid_total):,} đ và còn {int(unpaid_total):,} đ chờ thanh toán. "
                f"Chế độ nhấn mạnh hiện tại: {metric_label}."
            )

        self.staff_report_updated_at_lbl.setText(
            f"Cập nhật gần nhất: {QtCore.QDateTime.currentDateTime().toString('dd/MM/yyyy HH:mm:ss')}"
        )
        if data_warning:
            self._set_staff_report_feedback(
                "Một phần dữ liệu báo cáo tạm thời không tải được. Màn hình đang hiển thị phần dữ liệu đọc được mà không làm gián đoạn điều hướng.",
                is_error=True,
            )
        else:
            self._set_staff_report_feedback("Đã đồng bộ dữ liệu báo cáo theo bộ lọc hiện tại.", is_error=False)

    def _render_staff_report_kpis(self, total_patients, total_appointments, paid_total, unpaid_total, filtered_appt_count, paid_rows_count, metric_mode):
        while self.staff_report_kpi_row.count():
            item = self.staff_report_kpi_row.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        patient_note = "Tổng hồ sơ đang quản lý"
        appointment_note = f"Core tổng: {total_appointments}"
        paid_note = f"Phiếu paid theo lọc: {paid_rows_count}"
        unpaid_note = "Tính từ hóa đơn chưa paid/cancelled/refunded"
        if metric_mode == "revenue":
            paid_note = f"Đang là KPI được ưu tiên hiển thị theo chế độ {self._staff_report_metric_label(metric_mode).lower()}"
        elif metric_mode == "appointments":
            appointment_note = f"Đang là KPI được ưu tiên hiển thị theo chế độ {self._staff_report_metric_label(metric_mode).lower()}"
        elif metric_mode == "patients":
            patient_note = f"Đang là KPI được ưu tiên hiển thị theo chế độ {self._staff_report_metric_label(metric_mode).lower()}"

        kpi_cards = [
            self._build_kpi_card("Bệnh nhân", str(total_patients), patient_note, "#0ea5e9", "#e0f2fe", "👥"),
            self._build_kpi_card("Lịch hẹn (lọc)", str(filtered_appt_count), appointment_note, "#3b82f6", "#eaf2ff", "📅"),
            self._build_kpi_card("Đã thu", f"{int(paid_total):,} đ", paid_note, "#16a34a", "#e7f8ef", "✓"),
            self._build_kpi_card("Chờ thu", f"{int(unpaid_total):,} đ", unpaid_note, "#f97316", "#fff3e4", "⏳"),
        ]
        for card in self._staff_report_order_kpis(kpi_cards, metric_mode):
            self.staff_report_kpi_row.addWidget(card)

    def _render_staff_report_status_table(self, status_counts):
        rows = [
            ("Đang chờ", status_counts.get("pending", 0)),
            ("Đã xác nhận", status_counts.get("confirmed", 0)),
            ("Đang khám", status_counts.get("in_progress", 0)),
            ("Hoàn tất", status_counts.get("done", 0)),
            ("Đã hủy", status_counts.get("cancelled", 0)),
        ]
        other_count = status_counts.get("other", 0)
        if other_count > 0:
            rows.append(("Khác", other_count))

        total = sum(count for _, count in rows)
        self.staff_report_status_table.setRowCount(len(rows))
        for row_idx, (label, count) in enumerate(rows):
            ratio = f"{(count * 100 / total):.0f}%" if total > 0 else "0%"
            self.staff_report_status_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(label))
            self.staff_report_status_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(count)))
            self.staff_report_status_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(ratio))
            self.staff_report_status_table.setRowHeight(row_idx, 36)

    def _render_staff_report_unpaid_table(self, unpaid_rows):
        top_rows = unpaid_rows[:5]
        self.staff_report_unpaid_table.setRowCount(len(top_rows))
        for row_idx, payment in enumerate(top_rows):
            if not isinstance(payment, dict):
                continue
            invoice_code = payment.get("invoice_code") or self._staff_billing_code(payment.get("payment_id"))
            patient_name = str(payment.get("patient_name") or f"BN #{payment.get('patient_id') or '-'}")
            amount_text = self._format_staff_billing_amount(payment.get("total_amount"))
            time_raw = payment.get("payment_date") or payment.get("created_at") or payment.get("appointment_date") or payment.get("date")
            time_display = self._format_staff_billing_datetime(time_raw)

            self.staff_report_unpaid_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(invoice_code)))
            self.staff_report_unpaid_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(patient_name))
            self.staff_report_unpaid_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(amount_text))
            self.staff_report_unpaid_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(time_display))
            self.staff_report_unpaid_table.setRowHeight(row_idx, 36)

        if not top_rows:
            self.staff_report_unpaid_table.setRowCount(1)
            self.staff_report_unpaid_table.setItem(0, 0, QtWidgets.QTableWidgetItem("Không có"))
            self.staff_report_unpaid_table.setItem(0, 1, QtWidgets.QTableWidgetItem("Không có hóa đơn chờ thu theo bộ lọc"))
            self.staff_report_unpaid_table.setItem(0, 2, QtWidgets.QTableWidgetItem("0 đ"))
            self.staff_report_unpaid_table.setItem(0, 3, QtWidgets.QTableWidgetItem("-"))
            self.staff_report_unpaid_table.setRowHeight(0, 36)

    def _render_staff_report_placeholder(self, total_appointments, paid_total, unpaid_total, filtered_appt_count, period_key, metric_mode):
        tab_label = self._staff_report_tab_label(getattr(self, "staff_report_active_tab", "overview"))
        period_label = self.staff_report_period_combo.currentText() if hasattr(self, "staff_report_period_combo") else "Hiện tại"
        self.staff_report_placeholder_title.setText(
            f"{tab_label} • {period_label}: {filtered_appt_count}/{total_appointments} lịch hẹn phù hợp"
        )

        total_money = max(paid_total + unpaid_total, 0.0)
        if total_money <= 0:
            paid_ratio = 0
            unpaid_ratio = 0
        else:
            # Clamp percentages to avoid UI overflow with unexpected numeric noise.
            paid_ratio = max(0, min(100, int((paid_total / total_money) * 100)))
            unpaid_ratio = max(0, min(100, 100 - paid_ratio))

        self.staff_report_ratio_paid.setValue(paid_ratio)
        self.staff_report_ratio_unpaid.setValue(unpaid_ratio)

        emphasis_text = self._staff_report_metric_label(metric_mode).lower()
        if getattr(self, "staff_report_active_tab", "overview") == "patients":
            self.staff_report_placeholder_hint.setText(
                f"Tab bệnh nhân đang dùng shell trung thực: chưa có breakdown sâu theo hồ sơ, nên panel này chỉ nhấn mạnh KPI/filter hiện có ({emphasis_text})."
            )
        elif getattr(self, "staff_report_active_tab", "overview") == "staff":
            self.staff_report_placeholder_hint.setText(
                f"Tab nhân viên đang dùng shell trung thực: chưa có nguồn chấm công/phân ca riêng, nên chỉ phản ánh dữ liệu vận hành hiện có ({emphasis_text})."
            )
        elif period_key == "today":
            self.staff_report_placeholder_hint.setText(
                f"Dạng hiển thị hôm nay: tập trung trạng thái lịch hẹn và tỷ trọng đã thu/chưa thu trong ngày, ưu tiên {emphasis_text}."
            )
        elif period_key == "7d":
            self.staff_report_placeholder_hint.setText(
                f"Dạng hiển thị 7 ngày: ưu tiên theo dõi xu hướng vận hành ngắn hạn và nhấn mạnh {emphasis_text}, chưa phải biểu đồ chuyên sâu."
            )
        elif period_key == "30d":
            self.staff_report_placeholder_hint.setText(
                f"Dạng hiển thị 30 ngày: phù hợp review tháng, đang là summary placeholders để đảm bảo trung thực dữ liệu và nhấn mạnh {emphasis_text}."
            )
        else:
            self.staff_report_placeholder_hint.setText(
                f"Dạng hiển thị toàn kỳ: dùng tóm tắt KPI + bảng trạng thái, chưa tích hợp chart engine chuyên dụng; chế độ ưu tiên hiện tại là {emphasis_text}."
            )

    def _refresh_staff_report_doctor_filter_options(self, appointments):
        if not hasattr(self, "staff_report_doctor_combo"):
            return

        current_value = self.staff_report_doctor_combo.currentData()
        unique_doctors = {}
        for appt in appointments:
            if not isinstance(appt, dict):
                continue
            doctor_id = appt.get("doctor_id")
            doctor_name = str(appt.get("doctor_name") or "").strip()
            if doctor_id in (None, "") and not doctor_name:
                continue
            key = str(doctor_id if doctor_id not in (None, "") else doctor_name)
            label = doctor_name or f"BS #{doctor_id}"
            unique_doctors[key] = label

        self.staff_report_doctor_combo.blockSignals(True)
        self.staff_report_doctor_combo.clear()
        self.staff_report_doctor_combo.addItem("Tất cả bác sĩ", "__all__")
        for key in sorted(unique_doctors.keys(), key=lambda v: str(unique_doctors.get(v) or "")):
            self.staff_report_doctor_combo.addItem(unique_doctors[key], key)

        restore_index = self.staff_report_doctor_combo.findData(current_value)
        if restore_index >= 0:
            self.staff_report_doctor_combo.setCurrentIndex(restore_index)
        self.staff_report_doctor_combo.blockSignals(False)

    def _filter_staff_report_appointments(self, appointments, period_key, doctor_key):
        rows = []
        for appt in appointments:
            if not isinstance(appt, dict):
                continue

            if doctor_key not in {None, "", "__all__"}:
                candidate_key = str(appt.get("doctor_id") if appt.get("doctor_id") not in (None, "") else appt.get("doctor_name") or "")
                if str(doctor_key) != candidate_key:
                    continue

            if not self._staff_report_matches_period(appt.get("appointment_date") or appt.get("date"), period_key):
                continue
            rows.append(appt)
        return rows

    def _filter_staff_report_payments(self, payments, period_key):
        rows = []
        for payment in payments:
            if not isinstance(payment, dict):
                continue
            date_value = payment.get("payment_date") or payment.get("created_at") or payment.get("appointment_date") or payment.get("date")
            if not self._staff_report_matches_period(date_value, period_key):
                continue
            rows.append(payment)
        return rows

    def _staff_report_matches_period(self, value, period_key):
        if period_key in {None, "", "all"}:
            return True

        dt_value = self._parse_staff_billing_datetime(value)
        if not dt_value.isValid():
            return False

        target_date = dt_value.date()
        today = QtCore.QDate.currentDate()
        if period_key == "today":
            return target_date == today
        if period_key == "7d":
            return target_date >= today.addDays(-6)
        if period_key == "30d":
            return target_date >= today.addDays(-29)
        return True

    def _handle_staff_report_apply_filters(self):
        self._refresh_staff_reports()

    def _handle_staff_report_reset_filters(self):
        if hasattr(self, "staff_report_period_combo"):
            self.staff_report_period_combo.setCurrentIndex(0)
        if hasattr(self, "staff_report_doctor_combo"):
            self.staff_report_doctor_combo.setCurrentIndex(0)
        if hasattr(self, "staff_report_metric_combo"):
            self.staff_report_metric_combo.setCurrentIndex(0)
        self._refresh_staff_reports()
        self._set_staff_report_feedback("Đã đặt lại bộ lọc báo cáo về mặc định.", is_error=False)

    def _set_staff_report_tab(self, tab_key):
        valid_tabs = {"overview", "revenue", "appointments", "patients", "staff", "services"}
        if tab_key not in valid_tabs:
            tab_key = "overview"
        self.staff_report_active_tab = tab_key
        self._refresh_staff_report_tab_styles()
        self._refresh_staff_reports()

    def _refresh_staff_report_tab_styles(self):
        styles = {
            "active": (
                "QPushButton { background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; border-radius: 8px; padding: 8px 12px; font-size: 12px; font-weight: 900; }"
                "QPushButton:hover { background: #dbeafe; }"
            ),
            "inactive": (
                "QPushButton { background: #ffffff; color: #334155; border: 1px solid #dbe4ee; border-radius: 8px; padding: 8px 12px; font-size: 12px; font-weight: 800; }"
                "QPushButton:hover { background: #f8fafc; }"
            ),
        }
        for tab_key, button in getattr(self, "staff_report_tab_buttons", {}).items():
            is_active = tab_key == self.staff_report_active_tab
            button.blockSignals(True)
            button.setChecked(is_active)
            button.blockSignals(False)
            button.setStyleSheet(styles["active"] if is_active else styles["inactive"])

    def _handle_staff_report_export(self):
        period_label = self.staff_report_period_combo.currentText() if hasattr(self, "staff_report_period_combo") else "mặc định"
        tab_label = self._staff_report_tab_label(getattr(self, "staff_report_active_tab", "overview")).lower()
        message = (
            "Chức năng export file (PDF/Excel) chưa được triển khai backend trong phạm vi hiện tại.\n"
            f"Bạn đang xem tab '{tab_label}' với bộ lọc '{period_label}'.\n"
            "Hiện hệ thống chỉ hỗ trợ xem/tổng hợp trực tiếp trên màn hình báo cáo."
        )
        QtWidgets.QMessageBox.information(self, "Xuất báo cáo", message)
        self._set_staff_report_feedback("Export đang ở chế độ placeholder trung thực (chưa tạo file).", is_error=False)

    def _set_staff_report_feedback(self, message, is_error=False):
        if not hasattr(self, "staff_report_feedback"):
            return
        self.staff_report_feedback.setText(message)
        color = "#b91c1c" if is_error else "#166534"
        self.staff_report_feedback.setStyleSheet(f"font-size: 12px; color: {color}; font-weight: 600;")

    def _staff_report_selected_period(self):
        if not hasattr(self, "staff_report_period_combo"):
            return "today"
        return str(self.staff_report_period_combo.currentData() or "today")

    def _staff_report_selected_doctor(self):
        if not hasattr(self, "staff_report_doctor_combo"):
            return "__all__"
        return self.staff_report_doctor_combo.currentData()

    def _staff_report_selected_metric_mode(self):
        if not hasattr(self, "staff_report_metric_combo"):
            return "active_tab"
        selected = str(self.staff_report_metric_combo.currentData() or "active_tab")
        if selected == "active_tab":
            active_tab = getattr(self, "staff_report_active_tab", "overview")
            if active_tab in {"revenue", "appointments", "patients"}:
                return active_tab
            return "active_tab"
        return selected

    @staticmethod
    def _staff_report_metric_label(metric_mode):
        return {
            "active_tab": "Theo tab đang chọn",
            "revenue": "Ưu tiên doanh thu",
            "appointments": "Ưu tiên lịch hẹn",
            "patients": "Ưu tiên bệnh nhân",
        }.get(metric_mode, "Theo tab đang chọn")

    @staticmethod
    def _staff_report_order_kpis(kpi_cards, metric_mode):
        if not isinstance(kpi_cards, list):
            return []

        priority_index = {
            "patients": 0,
            "appointments": 1,
            "revenue": 2,
        }.get(metric_mode)
        if priority_index is None or priority_index >= len(kpi_cards):
            return kpi_cards

        ordered_cards = list(kpi_cards)
        prioritized = ordered_cards.pop(priority_index)
        return [prioritized, *ordered_cards]

    @staticmethod
    def _staff_report_tab_label(tab_key):
        return {
            "overview": "Tổng quan",
            "revenue": "Doanh thu",
            "appointments": "Lịch hẹn",
            "patients": "Bệnh nhân",
            "staff": "Nhân viên",
            "services": "Dịch vụ",
        }.get(tab_key, "Tổng quan")

    def _handle_staff_profile_update(self):
        user_id = self.user_data.get("user_id")
        if not user_id:
            self._set_staff_profile_feedback("Không tìm thấy user_id để cập nhật hồ sơ staff.", is_error=True)
            return

        name = self.staff_settings_name_input.text().strip()
        phone = self.staff_settings_phone_input.text().strip()
        email = self.staff_settings_email_input.text().strip().lower()
        dob_display = self.staff_settings_dob_input.text().strip() if hasattr(self, "staff_settings_dob_input") else ""
        gender = self.staff_settings_gender_combo.currentText().strip() if hasattr(self, "staff_settings_gender_combo") else "Nam"

        if not name:
            self._set_staff_profile_feedback("Họ tên không được để trống.", is_error=True)
            return

        if phone and len(phone) < 8:
            self._set_staff_profile_feedback("Số điện thoại phải có tối thiểu 8 ký tự số.", is_error=True)
            return

        if email and ("@" not in email or "." not in email):
            self._set_staff_profile_feedback("Email không hợp lệ.", is_error=True)
            return

        if dob_display:
            if not re.match(r"^\d{2}/\d{2}/\d{4}$", dob_display):
                self._set_staff_profile_feedback("Ngày sinh phải theo định dạng dd/mm/yyyy.", is_error=True)
                return
            parsed_dob = QtCore.QDate.fromString(dob_display, "dd/MM/yyyy")
            if not parsed_dob.isValid():
                self._set_staff_profile_feedback("Ngày sinh không hợp lệ.", is_error=True)
                return
            dob_iso = parsed_dob.toString("yyyy-MM-dd")
        else:
            dob_iso = None

        ok, message = SettingsController.update_staff_personal_info(
            user_id,
            {
                "name": name,
                "phone": phone,
                "email": email,
                "gender": gender,
                "dob": dob_iso,
                "address": str(self.user_data.get("address") or ""),
            },
        )
        if not ok:
            self._set_staff_profile_feedback(message, is_error=True)
            return

        self.user_data["name"] = name
        self.user_data["phone"] = phone
        self.user_data["email"] = email
        self.user_data["dob"] = dob_display
        self.user_data["gender"] = gender
        self.username = name
        self._update_staff_identity_labels()
        self._set_staff_profile_feedback(message, is_error=False)

    def _bind_staff_settings_option_handlers(self):
        if hasattr(self, "staff_settings_language_combo"):
            self.staff_settings_language_combo.currentTextChanged.connect(self._handle_staff_language_changed)
        if hasattr(self, "staff_settings_theme_combo"):
            self.staff_settings_theme_combo.currentTextChanged.connect(self._handle_staff_theme_changed)
        if hasattr(self, "staff_settings_screen_notify_checkbox"):
            self.staff_settings_screen_notify_checkbox.toggled.connect(
                lambda checked: self._handle_staff_notification_option_changed("notify_reminder", bool(checked))
            )
        if hasattr(self, "staff_settings_sound_notify_checkbox"):
            self.staff_settings_sound_notify_checkbox.toggled.connect(
                lambda checked: self._handle_staff_notification_option_changed("notify_system", bool(checked))
            )
        if hasattr(self, "staff_settings_date_format_combo"):
            self.staff_settings_date_format_combo.currentTextChanged.connect(
                lambda _: self._set_staff_settings_options_feedback(
                    "Định dạng ngày hiện chưa có backend lưu riêng cho staff. Thay đổi chỉ áp dụng ở mức giao diện shell.",
                    is_error=True,
                )
            )
        if hasattr(self, "staff_settings_time_format_combo"):
            self.staff_settings_time_format_combo.currentTextChanged.connect(
                lambda _: self._set_staff_settings_options_feedback(
                    "Định dạng giờ hiện chưa có backend lưu riêng cho staff. Thay đổi chỉ áp dụng ở mức giao diện shell.",
                    is_error=True,
                )
            )
        if hasattr(self, "staff_settings_page_size_combo"):
            self.staff_settings_page_size_combo.currentTextChanged.connect(
                lambda _: self._set_staff_settings_options_feedback(
                    "Số bản ghi mỗi trang chưa có backing field riêng trong UserSettings. Thay đổi chưa được persist.",
                    is_error=True,
                )
            )

    def _set_staff_settings_backup_feedback(self, message, is_error=False):
        if not hasattr(self, "staff_settings_backup_feedback"):
            return
        self.staff_settings_backup_feedback.setText(message)
        color = "#b91c1c" if is_error else "#166534"
        self.staff_settings_backup_feedback.setStyleSheet(f"font-size: 12px; color: {color}; font-weight: 600;")

    def _refresh_staff_settings_utilities_status(self, settings_data=None):
        if not isinstance(settings_data, dict):
            settings_data = self._load_staff_settings_data()

        last_backup = str(settings_data.get("last_backup_at") or "Chưa có")
        last_sync = str(settings_data.get("last_sync_at") or "Chưa có")
        backup_mode = str(settings_data.get("backup_mode") or "cloud")

        if hasattr(self, "staff_settings_backup_status_label"):
            self.staff_settings_backup_status_label.setText(f"Lần sao lưu gần nhất: {last_backup}")
        if hasattr(self, "staff_settings_sync_status_label"):
            self.staff_settings_sync_status_label.setText(f"Lần đồng bộ gần nhất: {last_sync}")
        if hasattr(self, "staff_settings_backup_mode_combo"):
            mode_index = self.staff_settings_backup_mode_combo.findData(backup_mode)
            if mode_index >= 0:
                self.staff_settings_backup_mode_combo.setCurrentIndex(mode_index)

    def _handle_staff_backup_now(self):
        user_id = self.user_data.get("user_id")
        if not user_id:
            self._set_staff_settings_backup_feedback("Không tìm thấy user_id để sao lưu dữ liệu.", is_error=True)
            return

        backup_mode = "cloud"
        if hasattr(self, "staff_settings_backup_mode_combo"):
            backup_mode = str(self.staff_settings_backup_mode_combo.currentData() or "cloud")

        ok, result = SettingsController.backup_now(user_id, backup_mode)
        if not ok:
            self._set_staff_settings_backup_feedback(str(result), is_error=True)
            QtWidgets.QMessageBox.warning(self, "Sao lưu dữ liệu", str(result))
            return

        self._refresh_staff_settings_utilities_status()
        self._refresh_staff_settings_system_info()
        self._set_staff_settings_backup_feedback("Đã sao lưu dữ liệu thành công.", is_error=False)
        QtWidgets.QMessageBox.information(
            self,
            "Sao lưu dữ liệu",
            f"Sao lưu thành công ({backup_mode}).\nTệp: {result}",
        )

    def _handle_staff_sync_now(self):
        user_id = self.user_data.get("user_id")
        if not user_id:
            self._set_staff_settings_backup_feedback("Không tìm thấy user_id để đồng bộ dữ liệu.", is_error=True)
            return

        ok, result = SettingsController.sync_now(user_id)
        if not ok:
            self._set_staff_settings_backup_feedback(str(result), is_error=True)
            QtWidgets.QMessageBox.warning(self, "Đồng bộ backup", str(result))
            return

        self._refresh_staff_settings_utilities_status()
        self._set_staff_settings_backup_feedback(str(result), is_error=False)
        QtWidgets.QMessageBox.information(self, "Đồng bộ backup", str(result))

    def _handle_staff_restore_blocked(self, action_name):
        QtWidgets.QMessageBox.warning(
            self,
            "Khôi phục dữ liệu",
            "Restore đang bị khóa cho staff vì backend an toàn (xác nhận, rollback, audit) chưa sẵn sàng.\n"
            f"Thao tác '{action_name}' chỉ hiển thị ở mức giao diện để phản ánh đúng phạm vi hỗ trợ hiện tại.",
        )

    def _handle_staff_logo_scope_notice(self, action_name):
        QtWidgets.QMessageBox.information(
            self,
            "Logo phòng khám",
            "Tùy chọn logo mới dừng ở mức preview. Hệ thống chưa có backend staff-safe để áp dụng logo system-wide.\n"
            f"Yêu cầu '{action_name}' chưa thể ghi xuống cấu hình dùng chung.",
        )

    @staticmethod
    def _format_staff_storage_size(total_bytes):
        if total_bytes <= 0:
            return "0 B"

        units = ["B", "KB", "MB", "GB", "TB"]
        value = float(total_bytes)
        unit_index = 0
        while value >= 1024 and unit_index < len(units) - 1:
            value /= 1024
            unit_index += 1
        return f"{value:.1f} {units[unit_index]}"

    def _refresh_staff_settings_system_info(self):
        version = "Chưa cấu hình"
        database_name = "Chưa cấu hình"
        database_server = "Chưa cấu hình"
        try:
            config_module = __import__("config")
            app_config = getattr(config_module, "APP_CONFIG", {})
            db_config = getattr(config_module, "DB_CONFIG", {})
            if isinstance(app_config, dict):
                version = str(app_config.get("VERSION") or version)
            if isinstance(db_config, dict):
                database_name = str(db_config.get("DATABASE") or database_name)
                database_server = str(db_config.get("SERVER") or database_server)
        except Exception:
            pass

        backup_dir = Path(__file__).resolve().parents[1] / "backups" / "local"
        size_text = "Chưa có dữ liệu dung lượng (chưa tạo backups/local)."
        if backup_dir.exists() and backup_dir.is_dir():
            try:
                total_size = 0
                for file_path in backup_dir.rglob("*"):
                    if file_path.is_file():
                        total_size += file_path.stat().st_size
                size_text = f"{self._format_staff_storage_size(total_size)} (backups/local)"
            except OSError:
                size_text = "Không đọc được dung lượng thư mục backups/local."

        if hasattr(self, "staff_settings_system_version_card"):
            self.staff_settings_system_version_card.value_label.setText(version)
        if hasattr(self, "staff_settings_system_db_card"):
            self.staff_settings_system_db_card.value_label.setText(database_name)
        if hasattr(self, "staff_settings_system_server_card"):
            self.staff_settings_system_server_card.value_label.setText(database_server)
        if hasattr(self, "staff_settings_system_size_card"):
            self.staff_settings_system_size_card.value_label.setText(size_text)

    def _handle_staff_check_update(self):
        current_version = "không rõ"
        try:
            config_module = __import__("config")
            app_config = getattr(config_module, "APP_CONFIG", {})
            if isinstance(app_config, dict):
                current_version = str(app_config.get("VERSION") or current_version)
        except Exception:
            pass
        QtWidgets.QMessageBox.information(
            self,
            "Kiểm tra cập nhật",
            "Hiện chưa có service backend để kiểm tra phiên bản online trong staff scope.\n"
            f"Phiên bản cấu hình hiện tại: {current_version}.\n"
            "Nút này chỉ cung cấp trạng thái trung thực, không giả lập kết quả cập nhật.",
        )

    def _set_staff_settings_options_feedback(self, message, is_error=False):
        if not hasattr(self, "staff_settings_options_feedback"):
            return
        self.staff_settings_options_feedback.setText(message)
        color = "#b91c1c" if is_error else "#166534"
        self.staff_settings_options_feedback.setStyleSheet(f"font-size: 12px; color: {color}; font-weight: 600;")

    def _handle_staff_language_changed(self, language):
        if self._staff_settings_options_sync_in_progress:
            return
        user_id = self.user_data.get("user_id")
        if not user_id:
            self._set_staff_settings_options_feedback("Không tìm thấy user_id để lưu ngôn ngữ.", is_error=True)
            return

        saved = SettingsController.update_language(user_id, str(language))
        if saved:
            self._set_staff_settings_options_feedback("Đã lưu ngôn ngữ cá nhân thành công.", is_error=False)
            return

        fallback_language = "Tiếng Việt"
        try:
            settings_data = SettingsController.get_settings(user_id) or {}
        except Exception:
            settings_data = {}
        if isinstance(settings_data, dict):
            candidate = str(settings_data.get("language") or "Tiếng Việt")
            if candidate in {"Tiếng Việt", "English"}:
                fallback_language = candidate

        # Keep UI consistent with persisted value when save fails.
        self._staff_settings_options_sync_in_progress = True
        self.staff_settings_language_combo.setCurrentText(fallback_language)
        self._staff_settings_options_sync_in_progress = False
        self._set_staff_settings_options_feedback("Không thể lưu ngôn ngữ. Đã khôi phục theo cấu hình đang lưu.", is_error=True)

    def _handle_staff_theme_changed(self, theme_mode):
        if self._staff_settings_options_sync_in_progress:
            return
        user_id = self.user_data.get("user_id")
        if not user_id:
            self._set_staff_settings_options_feedback("Không tìm thấy user_id để lưu giao diện.", is_error=True)
            return

        theme_mode = str(theme_mode)
        if theme_mode == "Theo hệ thống":
            self._restore_staff_theme_option(user_id, error_message=(
                "Tùy chọn 'Theo hệ thống' chưa có backend phù hợp trong UserSettings. "
                "Hệ thống đã giữ lại giá trị giao diện đang lưu."
            ))
            return

        saved = SettingsController.update_display_option(user_id, "theme_mode", theme_mode)
        if saved:
            self._set_staff_settings_options_feedback("Đã lưu giao diện cá nhân thành công.", is_error=False)
            return

        self._restore_staff_theme_option(
            user_id,
            error_message="Không thể lưu giao diện. Đã khôi phục theo cấu hình đang lưu.",
        )

    def _restore_staff_theme_option(self, user_id, error_message):
        fallback_theme = "Sáng"
        try:
            settings_data = SettingsController.get_settings(user_id) or {}
        except Exception:
            settings_data = {}
        if isinstance(settings_data, dict):
            candidate = str(settings_data.get("theme_mode") or "Sáng")
            if candidate in {"Sáng", "Tối"}:
                fallback_theme = candidate

        self._staff_settings_options_sync_in_progress = True
        self.staff_settings_theme_combo.setCurrentText(fallback_theme)
        self._staff_settings_options_sync_in_progress = False
        self._set_staff_settings_options_feedback(error_message, is_error=True)

    def _handle_staff_notification_option_changed(self, option_key, option_value):
        if self._staff_settings_options_sync_in_progress:
            return

        user_id = self.user_data.get("user_id")
        if not user_id:
            self._set_staff_settings_options_feedback("Không tìm thấy user_id để lưu tùy chọn thông báo.", is_error=True)
            return

        saved = SettingsController.update_notification(user_id, option_key, option_value)
        if saved:
            self._set_staff_settings_options_feedback("Đã lưu tùy chọn thông báo cá nhân thành công.", is_error=False)
            return

        # Re-sync checkboxes from persisted settings when update fails.
        try:
            settings_data = SettingsController.get_settings(user_id) or {}
        except Exception:
            settings_data = {}
        if not isinstance(settings_data, dict):
            settings_data = {}

        self._staff_settings_options_sync_in_progress = True
        if hasattr(self, "staff_settings_auto_confirm_checkbox"):
            self.staff_settings_auto_confirm_checkbox.setChecked(False)
        if hasattr(self, "staff_settings_screen_notify_checkbox"):
            self.staff_settings_screen_notify_checkbox.setChecked(bool(settings_data.get("notify_reminder", True)))
        if hasattr(self, "staff_settings_sound_notify_checkbox"):
            self.staff_settings_sound_notify_checkbox.setChecked(bool(settings_data.get("notify_system", True)))
        self._staff_settings_options_sync_in_progress = False
        self._set_staff_settings_options_feedback("Không thể lưu tùy chọn thông báo. Đã khôi phục theo cấu hình đang lưu.", is_error=True)

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

    def _load_staff_settings_data(self):
        user_id = self.user_data.get("user_id")
        if not user_id:
            return {}
        try:
            settings = SettingsController.get_settings(user_id)
        except Exception:
            settings = {}
        return settings if isinstance(settings, dict) else {}

    @staticmethod
    def _staff_settings_button_style(primary=False, danger=False, accent="#10b981"):
        if primary:
            return (
                "QPushButton {"
                f" background: {accent}; color: #ffffff; border: 1px solid {accent}; border-radius: 8px;"
                " padding: 10px 14px; font-size: 13px; font-weight: 900; }"
                "QPushButton:hover { opacity: 0.92; }"
            )
        border_color = "#fecaca" if danger else "#dbe4ee"
        text_color = "#ef4444" if danger else "#475569"
        hover_bg = "#fef2f2" if danger else "#f8fafc"
        return (
            "QPushButton {"
            f" background: #ffffff; color: {text_color}; border: 1px solid {border_color}; border-radius: 8px;"
            " padding: 10px 14px; font-size: 13px; font-weight: 800; }"
            f"QPushButton:hover {{ background: {hover_bg}; }}"
        )

    @staticmethod
    def _staff_settings_menu_button_style(is_active=False):
        base = (
            "QPushButton {"
            " background: #ffffff; border: none; text-align: left; border-radius: 10px;"
            " padding: 14px 16px; font-size: 13px; font-weight: 800; color: #334155; }"
        )
        if is_active:
            return base + "QPushButton { background: #e9f8f1; color: #0f9f6e; font-weight: 900; }"
        return base + "QPushButton:hover { background: #f1f5f9; }"

    def _build_staff_settings_info_card(self, label_text, value_text):
        card = QtWidgets.QFrame()
        card.setStyleSheet("QFrame { background: #f8fbff; border: 1px solid #e4ebf4; border-radius: 12px; }")
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(5)
        label = QtWidgets.QLabel(label_text)
        label.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 800;")
        value = QtWidgets.QLabel(value_text)
        value.setWordWrap(True)
        value.setStyleSheet("font-size: 13px; color: #0f172a; font-weight: 900;")
        card.value_label = value
        layout.addWidget(label)
        layout.addWidget(value)
        return card

    def _show_staff_settings_placeholder(self, title, message):
        QtWidgets.QMessageBox.information(self, title, message)

    def _update_staff_identity_labels(self):
        if hasattr(self, "dashboard_welcome_label"):
            self.dashboard_welcome_label.setText(f"Xin chào, {self.username}!")
        if hasattr(self, "dashboard_user_label"):
            self.dashboard_user_label.setText(f"{self.username}  ▾")
        if hasattr(self, "staff_settings_header_user_label"):
            self.staff_settings_header_user_label.setText(f"{self.username}  ▾")

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

        card.kpi_title_label = title_lbl
        card.kpi_value_label = value_lbl
        card.kpi_note_label = note_lbl

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
        elif index == 8:
            self._update_staff_identity_labels()
            self._refresh_staff_settings_utilities_status()
            self._refresh_staff_settings_system_info()

        self.content_stack.setCurrentIndex(index)
