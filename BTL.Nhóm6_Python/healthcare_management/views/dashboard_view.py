from PyQt6 import QtWidgets, QtCore, QtGui
import sys
from datetime import datetime, timedelta

# =================================================================
# 1. WIDGET BIỂU ĐỒ (Dùng cho Admin Dashboard - Area Chart)
# =================================================================
class ChartWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(300)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        w, h = self.width(), self.height()
        padding = 50
        chart_w = w - 2 * padding
        chart_h = h - 2 * padding
        
        # Vẽ các trục xám nhạt và nhãn trục Y
        pen = QtGui.QPen(QtGui.QColor("#eee"), 1)
        painter.setPen(pen)
        for i in range(6):
            y_pos = h - padding - (i * chart_h // 5)
            painter.drawLine(padding, y_pos, w - padding, y_pos)
            painter.setPen(QtGui.QColor("#888"))
            painter.drawText(padding - 35, y_pos + 5, str(i * 10))
            painter.setPen(pen)

        # Dữ liệu mẫu (Thứ 2 -> Chủ nhật)
        points = [12, 25, 20, 32, 45, 30, 42]
        x_step = chart_w // (len(points) - 1)
        
        point_coords = []
        for i, val in enumerate(points):
            x = padding + i * x_step
            y = h - padding - (val * chart_h // 50)
            point_coords.append(QtCore.QPointF(x, y))

        # --- VẼ AREA (Vùng màu Gradient dưới đường kẻ) ---
        path_area = QtGui.QPainterPath()
        path_area.moveTo(point_coords[0].x(), h - padding)
        for pt in point_coords:
            path_area.lineTo(pt)
        path_area.lineTo(point_coords[-1].x(), h - padding)
        path_area.closeSubpath()

        gradient = QtGui.QLinearGradient(0, padding, 0, h - padding)
        gradient.setColorAt(0, QtGui.QColor(105, 192, 165, 150)) 
        gradient.setColorAt(1, QtGui.QColor(105, 192, 165, 0))
        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawPath(path_area)

        # --- VẼ ĐƯỜNG KẺ CHÍNH ---
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.setPen(QtGui.QPen(QtGui.QColor("#69c0a5"), 4))
        path_line = QtGui.QPainterPath()
        path_line.moveTo(point_coords[0])
        for pt in point_coords[1:]:
            path_line.lineTo(pt)
        painter.drawPath(path_line)
        
        # Vẽ các điểm nút (Nodes)
        painter.setBrush(QtGui.QColor("white"))
        painter.setPen(QtGui.QPen(QtGui.QColor("#69c0a5"), 2))
        for pt in point_coords:
            painter.drawEllipse(pt, 5, 5)

        # Vẽ nhãn thứ dưới trục X
        days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "CN"]
        painter.setPen(QtGui.QColor("#333"))
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        for i, day in enumerate(days):
            painter.drawText(int(padding + i * x_step - 20), h - 15, day)


class DoctorLineChartWidget(QtWidgets.QWidget):
    def __init__(self, labels=None, values=None, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(250)
        self.labels = labels or []
        self.values = values or []

    def set_data(self, labels, values):
        self.labels = labels
        self.values = values
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        left_pad, right_pad, top_pad, bottom_pad = 45, 20, 18, 32
        chart_w = max(1, w - left_pad - right_pad)
        chart_h = max(1, h - top_pad - bottom_pad)

        pen_grid = QtGui.QPen(QtGui.QColor("#edf2f7"), 1)
        for i in range(5):
            y = top_pad + i * chart_h // 4
            painter.setPen(pen_grid)
            painter.drawLine(left_pad, y, w - right_pad, y)

        if not self.values:
            painter.setPen(QtGui.QColor("#94a3b8"))
            painter.drawText(self.rect(), QtCore.Qt.AlignmentFlag.AlignCenter, "Chưa có dữ liệu")
            return

        max_value = max(self.values) if max(self.values) > 0 else 1
        x_step = chart_w // max(1, len(self.values) - 1)

        points = []
        for idx, value in enumerate(self.values):
            x = left_pad + idx * x_step
            y = top_pad + int((1 - (value / max_value)) * chart_h)
            points.append(QtCore.QPointF(x, y))

        fill_path = QtGui.QPainterPath()
        fill_path.moveTo(points[0].x(), top_pad + chart_h)
        for point in points:
            fill_path.lineTo(point)
        fill_path.lineTo(points[-1].x(), top_pad + chart_h)
        fill_path.closeSubpath()

        gradient = QtGui.QLinearGradient(0, top_pad, 0, top_pad + chart_h)
        gradient.setColorAt(0.0, QtGui.QColor(105, 192, 165, 130))
        gradient.setColorAt(1.0, QtGui.QColor(105, 192, 165, 5))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(gradient)
        painter.drawPath(fill_path)

        line_path = QtGui.QPainterPath()
        line_path.moveTo(points[0])
        for point in points[1:]:
            line_path.lineTo(point)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.setPen(QtGui.QPen(QtGui.QColor("#69c0a5"), 3))
        painter.drawPath(line_path)

        painter.setBrush(QtGui.QColor("white"))
        painter.setPen(QtGui.QPen(QtGui.QColor("#2f9e86"), 2))
        for point in points:
            painter.drawEllipse(point, 4, 4)

        painter.setPen(QtGui.QColor("#64748b"))
        for idx, label in enumerate(self.labels):
            x = left_pad + idx * x_step - 12
            painter.drawText(x, h - 8, label)


class DoctorPieChartWidget(QtWidgets.QWidget):
    def __init__(self, chart_data=None, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(250)
        self.chart_data = chart_data or []
        self.colors = [
            QtGui.QColor("#69c0a5"),
            QtGui.QColor("#5b8def"),
            QtGui.QColor("#f59f00"),
            QtGui.QColor("#e8590c"),
            QtGui.QColor("#845ef7"),
            QtGui.QColor("#0ca678"),
        ]

    def set_data(self, chart_data):
        self.chart_data = chart_data
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        if not self.chart_data:
            painter.setPen(QtGui.QColor("#94a3b8"))
            painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Chưa có dữ liệu")
            return

        total = sum(item[1] for item in self.chart_data)
        if total <= 0:
            painter.setPen(QtGui.QColor("#94a3b8"))
            painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Chưa có dữ liệu")
            return

        pie_size = min(rect.width() * 0.45, rect.height() * 0.7)
        pie_rect = QtCore.QRectF(20, 30, pie_size, pie_size)
        start_angle = 0

        # Use integer degree units (16 * degree) to keep arc rendering deterministic.
        for idx, (_, value) in enumerate(self.chart_data):
            span_angle = int(round((value / total) * 360 * 16))
            painter.setBrush(self.colors[idx % len(self.colors)])
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawPie(pie_rect, start_angle, span_angle)
            start_angle += span_angle

        legend_x = int(pie_rect.right()) + 24
        legend_y = 30
        painter.setPen(QtGui.QColor("#334155"))
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)

        for idx, (label, value) in enumerate(self.chart_data):
            color = self.colors[idx % len(self.colors)]
            painter.setBrush(color)
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(legend_x, legend_y + idx * 28, 14, 14, 3, 3)

            percent = (value / total) * 100
            painter.setPen(QtGui.QColor("#334155"))
            painter.drawText(
                legend_x + 22,
                legend_y + 12 + idx * 28,
                f"{label}: {value} ({percent:.0f}%)",
            )

# =================================================================
# 2. GIAO DIỆN BÁC SĨ (Dashboard Bác Sĩ)
# =================================================================
class DashboardView(QtWidgets.QWidget):
    def __init__(self, user_data=None):
        super().__init__()
        self.user_data = user_data or {"doctor_id": 1, "name": "Unknown"}
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # SideBar Bác Sĩ
        self.sidebar = QtWidgets.QFrame()
        self.sidebar.setFixedWidth(240)
        self.sidebar.setStyleSheet("background-color: white; border-right: 1px solid #e0e0e0;")
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(15, 20, 15, 20)
        self.sidebar_layout.setSpacing(8)

        self.logo = QtWidgets.QLabel("⊕ CarePlus")
        self.logo.setStyleSheet("color: #69c0a5; font-size: 24px; font-weight: 800; margin-bottom: 25px; margin-left: 10px;")
        self.sidebar_layout.addWidget(self.logo)

        menu_items = [
            ("🏠", "Dashboard"),
            ("📅", "Lịch hẹn"),
            ("👥", "Bệnh nhân của tôi"),
            ("📂", "Hồ sơ khám bệnh"),
            ("💬", "Tư vấn & lịch sử chăm sóc"),
            ("💊", "Đơn thuốc"),
            ("🔔", "Thông báo"),
            ("⚙️", "Cài đặt"),
        ]
        self.nav_buttons = []
        for i, (icon, text) in enumerate(menu_items):
            btn = QtWidgets.QPushButton(f"   {icon}     {text}")
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            style = "QPushButton { border: none; text-align: left; padding: 13px 20px; border-radius: 12px; color: #333; font-size: 14px; font-weight: 600; }"
            if text == "Dashboard": style += "QPushButton { background-color: #e1f2ee; color: #69c0a5; font-weight: 800; }"
            else: style += "QPushButton:hover { background-color: #f8f9fa; }"
            btn.setStyleSheet(style)
            btn.clicked.connect(lambda checked, idx=i: self.switch_page(idx))
            self.nav_buttons.append(btn)
            self.sidebar_layout.addWidget(btn)

        self.sidebar_layout.addStretch()
        self.main_layout.addWidget(self.sidebar)

        # Content Bác Sĩ
        self.content_container = QtWidgets.QWidget()
        self.content_container.setStyleSheet("background-color: #f0f7f9;")
        self.content_layout = QtWidgets.QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(40, 25, 40, 25)
        self.content_layout.setSpacing(25)
        self.main_layout.addWidget(self.content_container)

        self.header_layout = QtWidgets.QHBoxLayout()
        self.header_title = QtWidgets.QLabel("Hệ thống quản trị CarePlus")
        self.header_title.setStyleSheet("font-size: 14px; color: #333; font-weight: bold;")
        self.header_layout.addWidget(self.header_title)
        self.header_layout.addStretch()

        self.user_info_layout = QtWidgets.QHBoxLayout()
        self.user_avatar = QtWidgets.QLabel("👤")
        self.user_avatar.setFixedSize(35, 35)
        self.user_avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.user_avatar.setStyleSheet("background: #d1e9e7; border-radius: 17px; font-size: 16px;")
        self.user_name_lbl = QtWidgets.QLabel(f"Bác sĩ {self.user_data.get('name')} ▿")
        self.user_name_lbl.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        self.btn_logout = QtWidgets.QPushButton("Đăng xuất")
        self.btn_logout.setStyleSheet("QPushButton { background: #ff7875; color: white; border-radius: 8px; padding: 7px 15px; font-weight: bold; border: none; } QPushButton:hover { background: #ff4d4f; }")
        self.user_info_layout.addWidget(self.user_avatar); self.user_info_layout.addWidget(self.user_name_lbl); self.user_info_layout.addSpacing(10); self.user_info_layout.addWidget(self.btn_logout)
        self.header_layout.addLayout(self.user_info_layout)
        self.content_layout.addLayout(self.header_layout)

        # QStackedWidget cho các trang
        self.content_stack = QtWidgets.QStackedWidget()
        self.content_layout.addWidget(self.content_stack)

        # ==========================================
        # TRANG 0: DASHBOARD
        # ==========================================
        self.page_dashboard = QtWidgets.QWidget()
        page_dashboard_layout = QtWidgets.QVBoxLayout(self.page_dashboard)
        page_dashboard_layout.setContentsMargins(0, 0, 0, 0)
        page_dashboard_layout.setSpacing(25)

        self.lbl_page_title = QtWidgets.QLabel("Dashboard")
        self.lbl_page_title.setStyleSheet("font-size: 30px; font-weight: 800; color: #2c3e50;")
        page_dashboard_layout.addWidget(self.lbl_page_title)

        self.dashboard_data = self._build_doctor_dashboard_data(self.user_data.get("doctor_id"))

        raw_today = self.dashboard_data.get("today_appointments", [])
        appointments_today = raw_today if isinstance(raw_today, list) else []
        today_count = len(appointments_today)

        total_patients_raw = self.dashboard_data.get("total_patients", 0)
        total_patients = int(total_patients_raw) if isinstance(total_patients_raw, (int, float)) else 0

        week_count_raw = self.dashboard_data.get("week_count", 0)
        week_count = int(week_count_raw) if isinstance(week_count_raw, (int, float)) else 0

        raw_notifications = self.dashboard_data.get("notifications", [])
        notifications = raw_notifications if isinstance(raw_notifications, list) else []

        notification_count_raw = self.dashboard_data.get("notification_count", 0)
        notification_count = int(notification_count_raw) if isinstance(notification_count_raw, (int, float)) else 0

        self.stats_layout = QtWidgets.QHBoxLayout(); self.stats_layout.setSpacing(25)
        stats_data = [
            ("📄", "Lịch hẹn hôm nay", f"{today_count:02d}", "#e6f2ff", "#007bff"),
            ("👥", "Bệnh nhân đã khám", f"{total_patients:02d}", "#fff4e6", "#fd7e14"),
            ("🗓️", "Lịch hẹn tuần này", f"{week_count:02d}", "#e6f9f1", "#28a745"),
            ("🔔", "Thông báo mới", f"{notification_count:02d}", "#f9e6e6", "#dc3545"),
        ]
        for icon, title, value, bg, txt in stats_data:
            card = self.create_stat_card(icon, title, value, bg, txt)
            self.stats_layout.addWidget(card)
        page_dashboard_layout.addLayout(self.stats_layout)

        top_content_layout = QtWidgets.QHBoxLayout()
        top_content_layout.setSpacing(20)

        self.table_container = QtWidgets.QFrame()
        self.table_container.setStyleSheet("background: white; border-radius: 20px;")
        self.table_main_layout = QtWidgets.QVBoxLayout(self.table_container)
        self.table_main_layout.setContentsMargins(20, 20, 20, 20)

        self.lbl_table_title = QtWidgets.QLabel("Danh sách lịch hẹn hôm nay")
        self.lbl_table_title.setStyleSheet("font-size: 18px; font-weight: 800; color: #2c3e50; margin-bottom: 10px;")
        self.table_main_layout.addWidget(self.lbl_table_title)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Giờ", "Bệnh nhân", "Triệu chứng", "Loại khám", "Trạng thái", "Hành động"])
        self.table.setStyleSheet("""
            QTableWidget { border: none; font-size: 14px; color: #333; }
            QHeaderView::section {
                background-color: #f8f9fa; padding: 12px;
                border: none; border-bottom: 2px solid #eef0f2;
                font-weight: 800; color: #1e293b;
            }
            QTableWidget::item { padding: 10px; border-bottom: 1px solid #f1f5f9; }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self._populate_today_appointments_table(appointments_today)
        self.table_main_layout.addWidget(self.table)

        top_content_layout.addWidget(self.table_container, 7)

        side_panels = QtWidgets.QVBoxLayout()
        side_panels.setSpacing(15)
        side_panels.addWidget(self._build_notification_panel(notifications))
        side_panels.addWidget(self._build_upcoming_panel(self.dashboard_data.get("upcoming_appointments", [])))
        top_content_layout.addLayout(side_panels, 3)

        page_dashboard_layout.addLayout(top_content_layout)

        charts_layout = QtWidgets.QHBoxLayout()
        charts_layout.setSpacing(20)

        trend_frame = QtWidgets.QFrame()
        trend_frame.setStyleSheet("background: white; border-radius: 20px;")
        trend_layout = QtWidgets.QVBoxLayout(trend_frame)
        trend_layout.setContentsMargins(20, 20, 20, 20)
        trend_title = QtWidgets.QLabel("Biểu đồ bệnh nhân theo ngày (7 ngày)")
        trend_title.setStyleSheet("font-size: 16px; font-weight: 800; color: #1e293b;")
        trend_layout.addWidget(trend_title)
        trend_widget = DoctorLineChartWidget(
            self.dashboard_data.get("trend_labels", []),
            self.dashboard_data.get("trend_values", []),
        )
        trend_layout.addWidget(trend_widget)

        type_frame = QtWidgets.QFrame()
        type_frame.setStyleSheet("background: white; border-radius: 20px;")
        type_layout = QtWidgets.QVBoxLayout(type_frame)
        type_layout.setContentsMargins(20, 20, 20, 20)
        type_title = QtWidgets.QLabel("Biểu đồ cơ cấu loại khám")
        type_title.setStyleSheet("font-size: 16px; font-weight: 800; color: #1e293b;")
        type_layout.addWidget(type_title)
        type_widget = DoctorPieChartWidget(self.dashboard_data.get("visit_type_data", []))
        type_layout.addWidget(type_widget)

        charts_layout.addWidget(trend_frame)
        charts_layout.addWidget(type_frame)
        page_dashboard_layout.addLayout(charts_layout)

        new_patient_frame = QtWidgets.QFrame()
        new_patient_frame.setStyleSheet("background: white; border-radius: 20px;")
        new_patient_layout = QtWidgets.QVBoxLayout(new_patient_frame)
        new_patient_layout.setContentsMargins(20, 20, 20, 20)
        new_patient_title = QtWidgets.QLabel("Bệnh nhân mới")
        new_patient_title.setStyleSheet("font-size: 16px; font-weight: 800; color: #1e293b;")
        new_patient_layout.addWidget(new_patient_title)

        self.new_patient_table = QtWidgets.QTableWidget()
        self.new_patient_table.setColumnCount(4)
        self.new_patient_table.setHorizontalHeaderLabels(["Bệnh nhân", "SĐT", "Lần khám đầu", "Ghi chú"])
        self.new_patient_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.new_patient_table.verticalHeader().setVisible(False)
        self.new_patient_table.setShowGrid(False)
        self.new_patient_table.setStyleSheet(
            "QHeaderView::section { background-color: #f8f9fa; padding: 10px; border: none; font-weight: 700; }"
            "QTableWidget::item { padding: 8px; border-bottom: 1px solid #f1f5f9; }"
        )
        self._populate_new_patient_table(self.dashboard_data.get("new_patients", []))
        new_patient_layout.addWidget(self.new_patient_table)
        page_dashboard_layout.addWidget(new_patient_frame)

        page_dashboard_layout.addStretch()

        self.content_stack.addWidget(self.page_dashboard)

        # Các trang placeholder khác
        from views.doctor_management_views import MedicalRecordView, PrescriptionView, DoctorPatientListView, DoctorAppointmentView
        
        self.page_patient_list = DoctorPatientListView(self.user_data.get("doctor_id"))
        self.page_doctor_appts = DoctorAppointmentView(self.user_data.get("doctor_id"))
        self.page_medical_record = MedicalRecordView(self.user_data.get("doctor_id"))
        self.page_prescription = PrescriptionView(self.user_data.get("doctor_id"))
        
        self.content_stack.addWidget(self.page_doctor_appts)   # 1: Lịch hẹn
        self.content_stack.addWidget(self.page_patient_list)    # 2: Bệnh nhân của tôi
        self.content_stack.addWidget(self.page_medical_record)  # 3: Hồ sơ khám bệnh
        self.content_stack.addWidget(self._build_consultation_page())  # 4: Tư vấn & lịch sử chăm sóc
        self.content_stack.addWidget(self.page_prescription)    # 5: Đơn thuốc
        self.content_stack.addWidget(self._build_notification_center_page(notifications))  # 6: Thông báo
        self.content_stack.addWidget(self._build_settings_page())  # 7: Cài đặt

    def _build_doctor_dashboard_data(self, doctor_id):
        from controllers.appointment_controller import AppointmentController
        from database.db import fetch_one, fetch_all

        now_dt = datetime.now()
        today_start = now_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_start = today_start + timedelta(days=1)
        week_end = today_start + timedelta(days=7)

        appointments = AppointmentController.get_by_doctor(doctor_id)

        today_appointments = []
        upcoming_appointments = []
        week_count = 0
        trend_map = {}
        unique_patient_map = {}

        for i in range(7):
            date_key = (today_start + timedelta(days=i)).date()
            trend_map[date_key] = 0
            unique_patient_map[date_key] = set()

        active_statuses = {"pending", "confirmed", "in_progress"}

        for appointment in appointments:
            appt_dt = self._to_datetime(appointment.get("appointment_date"))
            if not appt_dt:
                continue

            appt_status = str(appointment.get("status", "")).lower()

            if appt_status in active_statuses and today_start <= appt_dt < tomorrow_start:
                today_appointments.append(appointment)

            if appt_status in active_statuses and today_start <= appt_dt < week_end:
                week_count += 1

            if appt_status in active_statuses and appt_dt >= now_dt:
                upcoming_appointments.append(appointment)

            appt_date = appt_dt.date()
            if appt_date in trend_map:
                patient_id = appointment.get("patient_id")
                if patient_id is not None:
                    unique_patient_map[appt_date].add(patient_id)
                else:
                    trend_map[appt_date] += 1

        total_patients_query = fetch_one(
            "SELECT COUNT(DISTINCT patient_id) as c FROM Appointments WHERE doctor_id=? AND status='done'",
            (doctor_id,),
        )
        total_patients = self._extract_count(total_patients_query)

        pending_query = fetch_one(
            "SELECT COUNT(*) as c FROM Appointments WHERE doctor_id=? AND status IN ('pending','confirmed')",
            (doctor_id,),
        )
        pending_count = self._extract_count(pending_query)

        type_rows = fetch_all(
            """
            SELECT
                CASE
                    WHEN note IS NULL OR note = '' THEN 'Khám tổng quát'
                    WHEN note LIKE 'Dịch vụ:%' THEN TRIM(SUBSTRING(note, 9))
                    ELSE note
                END AS visit_type,
                COUNT(*) AS total
            FROM Appointments
            WHERE doctor_id = ?
            GROUP BY
                CASE
                    WHEN note IS NULL OR note = '' THEN 'Khám tổng quát'
                    WHEN note LIKE 'Dịch vụ:%' THEN TRIM(SUBSTRING(note, 9))
                    ELSE note
                END
            ORDER BY total DESC
            LIMIT 5
            """,
            (doctor_id,),
        )

        # Normalize raw note values into stable labels for chart grouping.
        visit_type_data = []
        for row in type_rows:
            visit_type_data.append((str(row.get("visit_type", "Khám tổng quát")), int(row.get("total", 0))))

        new_patients = fetch_all(
            """
            SELECT p.name, p.phone, MIN(a.appointment_date) as first_visit
            FROM Patients p
            JOIN Appointments a ON p.patient_id = a.patient_id
            WHERE a.doctor_id = ?
            GROUP BY p.patient_id, p.name, p.phone
            ORDER BY first_visit DESC
            LIMIT 5
            """,
            (doctor_id,),
        )

        notifications = []
        if pending_count > 0:
            notifications.append(f"Có {pending_count} bệnh nhân đang chờ xác nhận")
        if today_appointments:
            notifications.append(f"Bạn có {len(today_appointments)} lịch khám trong hôm nay")

        notification_count = len(notifications)
        if notification_count == 0:
            notifications = ["Không có thông báo quan trọng"]

        sorted_upcoming = sorted(
            upcoming_appointments,
            key=lambda a: self._to_datetime(a.get("appointment_date")) or now_dt,
        )[:5]

        trend_labels = []
        trend_values = []
        for i in range(7):
            date_key = (today_start + timedelta(days=i)).date()
            trend_labels.append((today_start + timedelta(days=i)).strftime("%d/%m"))
            if unique_patient_map[date_key]:
                trend_values.append(len(unique_patient_map[date_key]))
            else:
                trend_values.append(trend_map[date_key])

        return {
            "today_appointments": sorted(today_appointments, key=lambda a: self._to_datetime(a.get("appointment_date")) or now_dt),
            "upcoming_appointments": sorted_upcoming,
            "total_patients": total_patients,
            "week_count": week_count,
            "notifications": notifications,
            "notification_count": notification_count,
            "trend_labels": trend_labels,
            "trend_values": trend_values,
            "visit_type_data": visit_type_data,
            "new_patients": new_patients,
        }

    def _populate_today_appointments_table(self, appointments):
        self.table.setRowCount(len(appointments))
        for row, appointment in enumerate(appointments):
            dt_str = self._format_datetime(appointment.get("appointment_date"), "%H:%M")
            patient_name = appointment.get("patient_name", "")
            symptom = self._extract_symptom(appointment.get("note"))
            visit_type = self._extract_visit_type(appointment.get("note"))
            status = appointment.get("status", "pending")

            for col, text in enumerate([dt_str, patient_name, symptom, visit_type, status]):
                item = QtWidgets.QTableWidgetItem(str(text))
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.table.setItem(row, col, item)

            action_layout = QtWidgets.QHBoxLayout()
            action_layout.setContentsMargins(4, 0, 4, 0)
            action_layout.setSpacing(4)

            actions = [
                ("view", "👁 Xem"),
                ("start_exam", "🩺 Bắt đầu khám"),
                ("record", "📄 Hồ sơ"),
            ]

            for action_key, label in actions:
                btn = QtWidgets.QPushButton(label)
                btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                btn.setStyleSheet("QPushButton { background: #f1f5f9; border: none; border-radius: 6px; padding: 4px 6px; font-size: 11px; } QPushButton:hover { background: #e2e8f0; }")
                btn.clicked.connect(
                    lambda _, key=action_key, appt=appointment: self._handle_appointment_action(key, appt)
                )
                action_layout.addWidget(btn)

            wrapper = QtWidgets.QWidget()
            wrapper.setLayout(action_layout)
            self.table.setCellWidget(row, 5, wrapper)
            self.table.setRowHeight(row, 52)

    def _build_notification_panel(self, notifications):
        panel = QtWidgets.QFrame()
        panel.setStyleSheet("background: white; border-radius: 16px;")
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QtWidgets.QLabel("Thông báo")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #1e293b;")
        layout.addWidget(title)

        for message in notifications[:4]:
            label = QtWidgets.QLabel(f"• {message}")
            label.setWordWrap(True)
            label.setStyleSheet("font-size: 13px; color: #475569;")
            layout.addWidget(label)

        layout.addStretch()
        return panel

    def _build_upcoming_panel(self, upcoming_appointments):
        panel = QtWidgets.QFrame()
        panel.setStyleSheet("background: white; border-radius: 16px;")
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        title = QtWidgets.QLabel("Lịch hẹn sắp tới")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #1e293b;")
        layout.addWidget(title)

        if not upcoming_appointments:
            empty = QtWidgets.QLabel("Không có lịch hẹn sắp tới")
            empty.setStyleSheet("font-size: 13px; color: #94a3b8;")
            layout.addWidget(empty)
        else:
            for appointment in upcoming_appointments:
                dt_text = self._format_datetime(appointment.get("appointment_date"), "%H:%M %d/%m")
                name = appointment.get("patient_name", "")
                label = QtWidgets.QLabel(f"{dt_text} - {name}")
                label.setStyleSheet("font-size: 13px; color: #475569;")
                layout.addWidget(label)

        layout.addStretch()
        return panel

    def _populate_new_patient_table(self, rows):
        self.new_patient_table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            name = row.get("name", "")
            phone = row.get("phone", "")
            first_visit_raw = row.get("first_visit")
            first_visit = self._format_datetime(first_visit_raw, "%d/%m/%Y")
            note = "Theo dõi"
            first_visit_dt = self._to_datetime(first_visit_raw)
            if first_visit_dt and (datetime.now() - first_visit_dt).days <= 30:
                note = "Bệnh nhân mới"
            for col, text in enumerate([name, phone, first_visit, note]):
                self.new_patient_table.setItem(row_idx, col, QtWidgets.QTableWidgetItem(str(text)))
            self.new_patient_table.setRowHeight(row_idx, 40)

    def _show_action_message(self, action_name, patient_name):
        QtWidgets.QMessageBox.information(
            self,
            "Thông tin",
            f"{action_name} cho bệnh nhân {patient_name} sẽ được mở ở module tương ứng.",
        )

    def _handle_appointment_action(self, action_key, appointment):
        from controllers.appointment_controller import AppointmentController

        patient_name = appointment.get("patient_name", "")
        appointment_id = appointment.get("appointment_id")
        status = str(appointment.get("status", "")).lower()

        if action_key == "start_exam":
            if status in {"pending", "confirmed"} and appointment_id is not None:
                AppointmentController.update_status(appointment_id, "in_progress")
            self.switch_page(3)
            QtWidgets.QMessageBox.information(
                self,
                "Bắt đầu khám",
                f"Đã chuyển tới hồ sơ khám bệnh cho {patient_name}.",
            )
            return

        if action_key == "record":
            self.switch_page(3)
            QtWidgets.QMessageBox.information(
                self,
                "Hồ sơ",
                f"Đã mở trang hồ sơ khám bệnh của bác sĩ cho {patient_name}.",
            )
            return

        if action_key == "view":
            self.switch_page(1)
            QtWidgets.QMessageBox.information(
                self,
                "Lịch hẹn",
                f"Đã mở danh sách lịch hẹn để xem chi tiết ca của {patient_name}.",
            )
            return

    def _build_consultation_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        title = QtWidgets.QLabel("Tư vấn & lịch sử chăm sóc")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #1e293b;")
        layout.addWidget(title)

        desc = QtWidgets.QLabel(
            "Trang này hỗ trợ bác sĩ theo dõi quá trình tư vấn, lịch sử chăm sóc và kế hoạch follow-up cho bệnh nhân."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 14px; color: #64748b;")
        layout.addWidget(desc)

        card = QtWidgets.QFrame()
        card.setStyleSheet("background: white; border-radius: 14px;")
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        for item in [
            "• Ghi chú sau khám và nhắc tái khám",
            "• Theo dõi tiến triển điều trị theo từng bệnh nhân",
            "• Đánh dấu ca cần tư vấn ưu tiên",
        ]:
            line = QtWidgets.QLabel(item)
            line.setStyleSheet("font-size: 13px; color: #334155;")
            card_layout.addWidget(line)
        layout.addWidget(card)
        layout.addStretch()
        return page

    def _build_notification_center_page(self, notifications):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        title = QtWidgets.QLabel("Trung tâm thông báo")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #1e293b;")
        layout.addWidget(title)

        table = QtWidgets.QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Mức độ", "Nội dung thông báo"])
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setStyleSheet(
            "QHeaderView::section { background-color: #f8f9fa; padding: 10px; border: none; font-weight: 700; }"
            "QTableWidget::item { padding: 8px; border-bottom: 1px solid #f1f5f9; }"
        )

        table.setRowCount(len(notifications))
        for row, message in enumerate(notifications):
            severity = "Quan trọng" if "đang chờ" in message else "Thông tin"
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(severity))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(message))
            table.setRowHeight(row, 44)

        layout.addWidget(table)
        layout.addStretch()
        return page

    def _build_settings_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        title = QtWidgets.QLabel("Cài đặt tài khoản")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #1e293b;")
        layout.addWidget(title)

        card = QtWidgets.QFrame()
        card.setStyleSheet("background: white; border-radius: 14px;")
        card_layout = QtWidgets.QFormLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.addRow("Họ tên:", QtWidgets.QLabel(str(self.user_data.get("name", ""))))
        card_layout.addRow("Vai trò:", QtWidgets.QLabel("Bác sĩ"))
        card_layout.addRow("Ghi chú:", QtWidgets.QLabel("Cấu hình chi tiết sẽ được mở rộng ở phiên bản tiếp theo."))
        layout.addWidget(card)
        layout.addStretch()
        return page

    @staticmethod
    def _extract_count(row):
        if isinstance(row, dict):
            return int(row.get("c", 0))
        if isinstance(row, (list, tuple)) and row:
            return int(row[0])
        return 0

    @staticmethod
    def _to_datetime(value):
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
        return None

    def _format_datetime(self, value, output_format):
        parsed = self._to_datetime(value)
        if parsed:
            return parsed.strftime(output_format)
        return ""

    @staticmethod
    def _extract_visit_type(note):
        if not note:
            return "Khám tổng quát"
        text = str(note)
        if text.startswith("Dịch vụ:"):
            return text.replace("Dịch vụ:", "", 1).strip() or "Khám tổng quát"
        return text

    @staticmethod
    def _extract_symptom(note):
        if not note:
            return "Chưa cập nhật"
        text = str(note)
        if text.startswith("Dịch vụ:"):
            return "Chưa cập nhật"
        return text
            
    def switch_page(self, index):
        self.content_stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            style = "QPushButton { border: none; text-align: left; padding: 13px 20px; border-radius: 12px; color: #333; font-size: 14px; font-weight: 600; }"
            if i == index:
                style += "QPushButton { background-color: #e1f2ee; color: #69c0a5; font-weight: 800; }"
            else:
                style += "QPushButton:hover { background-color: #f8f9fa; }"
            btn.setStyleSheet(style)

    def create_stat_card(self, icon, title, value, bg_color, text_color):
        card = QtWidgets.QFrame(); card.setMinimumHeight(130); card.setStyleSheet(f"background-color: {bg_color}; border-radius: 20px; border: none;")
        layout = QtWidgets.QHBoxLayout(card); layout.setContentsMargins(25, 25, 25, 25)
        icon_lbl = QtWidgets.QLabel(icon); icon_lbl.setStyleSheet(f"font-size: 35px; color: {text_color}; background: transparent;")
        text_v = QtWidgets.QVBoxLayout(); title_lbl = QtWidgets.QLabel(title); title_lbl.setStyleSheet(f"color: #475569; font-weight: 700; font-size: 14px;")
        value_lbl = QtWidgets.QLabel(value); value_lbl.setStyleSheet(f"color: {text_color}; font-size: 38px; font-weight: 900;")
        text_v.addWidget(title_lbl); text_v.addWidget(value_lbl); layout.addWidget(icon_lbl); layout.addSpacing(15); layout.addLayout(text_v); layout.addStretch()
        return card

# =================================================================
# 3. GIAO DIỆN ADMIN (Dashboard Admin)
# =================================================================
class AdminDashboardView(QtWidgets.QWidget):
    def __init__(self, user_data=None):
        super().__init__()
        self.user_data = user_data or {"name": "Admin"}
        self.username = self.user_data.get("name")
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Sidebar Admin
        self.sidebar = QtWidgets.QFrame()
        self.sidebar.setFixedWidth(260)
        self.sidebar.setStyleSheet("background-color: white; border-right: 1px solid #e2e8f0;")
        sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 25, 15, 25)
        sidebar_layout.setSpacing(5)

        logo = QtWidgets.QLabel("⊕ CarePlus Admin")
        logo.setStyleSheet("color: #69c0a5; font-size: 22px; font-weight: 900; margin-bottom: 20px;")
        sidebar_layout.addWidget(logo)

        menu_items = [
            ("🏠", "Dashboard Admin", True), 
            ("👥", "Quản lý bệnh nhân", False),
            ("👨‍⚕️", "Quản lý bác sĩ", False), 
            ("📅", "Quản lý lịch hẹn", False),
            ("🩺", "Quản lý khám bệnh", False),
            ("💊", "Quản lý thuốc", False), 
            ("💳", "Quản lý doanh thu", False),
            ("📊", "Báo cáo thống kê", False),
            ("⚙️", "Cấu hình hệ thống", False)
        ]

        self.nav_buttons = []
        for i, (icon, text, is_active) in enumerate(menu_items):
            btn = QtWidgets.QPushButton(f"   {icon}     {text}")
            style = "QPushButton { border: none; text-align: left; padding: 12px 15px; border-radius: 10px; font-size: 14px; color: #1e293b; font-weight: 600; }"
            if is_active: style += "QPushButton { background-color: #e1f2ee; color: #69c0a5; font-weight: 800; }"
            else: style += "QPushButton:hover { background-color: #f1f5f9; }"
            btn.setStyleSheet(style)
            btn.clicked.connect(lambda checked, idx=i: self.switch_page(idx))
            self.nav_buttons.append(btn)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        self.btn_logout = QtWidgets.QPushButton("🚪    Đăng xuất")
        self.btn_logout.setStyleSheet("QPushButton { border: none; text-align: left; padding: 12px 15px; color: #ef4444; font-weight: 800; font-size: 14px; } QPushButton:hover { background: #fee2e2; border-radius: 10px; }")
        sidebar_layout.addWidget(self.btn_logout)
        self.main_layout.addWidget(self.sidebar)

        # Content Admin
        self.content_container = QtWidgets.QWidget()
        self.content_container.setStyleSheet("background-color: #f8fafc;")
        content_layout = QtWidgets.QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(35, 25, 35, 35)
        content_layout.setSpacing(25)
        self.main_layout.addWidget(self.content_container)

        # Header Admin
        header = QtWidgets.QHBoxLayout()
        header_title = QtWidgets.QLabel("HỆ THỐNG QUẢN TRỊ TOÀN DIỆN")
        header_title.setStyleSheet("font-weight: 900; color: #1e293b; font-size: 14px; letter-spacing: 1px;")
        header.addWidget(header_title)
        header.addStretch()
        name_lbl = QtWidgets.QLabel(f"👤 {self.username} (Quản trị viên) ▿")
        name_lbl.setStyleSheet("font-weight: 700; color: #1e293b; font-size: 14px;")
        header.addWidget(name_lbl)
        content_layout.addLayout(header)

        # QStackedWidget cho các trang
        self.content_stack = QtWidgets.QStackedWidget()
        content_layout.addWidget(self.content_stack)

        # ==========================================
        # TRANG 0: DASHBOARD
        # ==========================================
        self.page_dashboard = QtWidgets.QWidget()
        page_dashboard_layout = QtWidgets.QVBoxLayout(self.page_dashboard)
        page_dashboard_layout.setContentsMargins(0, 0, 0, 0)
        page_dashboard_layout.setSpacing(25)

        # Stats Admin
        from database.db import fetch_one
        total_patients = fetch_one("SELECT COUNT(*) as c FROM Patients")
        tp = total_patients["c"] if isinstance(total_patients, dict) else (total_patients[0] if total_patients else 0)
        
        total_doctors = fetch_one("SELECT COUNT(*) as c FROM Doctors")
        td = total_doctors["c"] if isinstance(total_doctors, dict) else (total_doctors[0] if total_doctors else 0)
        
        total_appts = fetch_one("SELECT COUNT(*) as c FROM Appointments")
        ta = total_appts["c"] if isinstance(total_appts, dict) else (total_appts[0] if total_appts else 0)

        stats_layout = QtWidgets.QHBoxLayout(); stats_layout.setSpacing(20)
        stats_data = [("👥", "Tổng bệnh nhân", str(tp), "#eff6ff", "#2563eb"), ("🩺", "Tổng bác sĩ", str(td), "#f0fdf4", "#16a34a"), ("📅", "Tổng lịch hẹn", str(ta), "#fff7ed", "#ea580c")]
        for icon, title, val, bg, color in stats_data:
            card = self.create_stat_card(icon, title, val, bg, color)
            stats_layout.addWidget(card)
        page_dashboard_layout.addLayout(stats_layout)

        # Biểu đồ Admin
        chart_frame = QtWidgets.QFrame()
        chart_frame.setStyleSheet("background: white; border-radius: 20px; border: 1px solid #e2e8f0;")
        chart_layout = QtWidgets.QVBoxLayout(chart_frame)
        chart_layout.setContentsMargins(25, 25, 25, 25)
        
        chart_title = QtWidgets.QLabel("Biểu đồ lượt khám bệnh hàng tuần")
        chart_title.setStyleSheet("font-size: 18px; font-weight: 800; color: #1e293b; margin-bottom: 10px;")
        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(ChartWidget())
        page_dashboard_layout.addWidget(chart_frame)
        page_dashboard_layout.addStretch()

        self.content_stack.addWidget(self.page_dashboard)

        # Các trang placeholder khác
        from views.admin_management_views import (
            PatientManagementView, DoctorManagementView, 
            AppointmentManagementView, ServiceManagementView, 
            MedicineManagementView, PaymentManagementView,
            ReportStatsView
        )
        self.page_patient_mgmt = PatientManagementView()
        self.page_doctor_mgmt = DoctorManagementView()
        self.page_appt_mgmt = AppointmentManagementView()
        self.page_service_mgmt = ServiceManagementView()
        self.page_med_mgmt = MedicineManagementView()
        self.page_pay_mgmt = PaymentManagementView()
        self.page_report = ReportStatsView()
        
        self.content_stack.addWidget(self.page_patient_mgmt) # Index 1: Quản lý bệnh nhân
        self.content_stack.addWidget(self.page_doctor_mgmt) # Index 2: Quản lý bác sĩ
        self.content_stack.addWidget(self.page_appt_mgmt) # Index 3: Quản lý lịch hẹn
        self.content_stack.addWidget(self.page_service_mgmt) # Index 4: Quản lý dịch vụ
        self.content_stack.addWidget(self.page_med_mgmt) # Index 5: Quản lý thuốc
        self.content_stack.addWidget(self.page_pay_mgmt) # Index 6: Quản lý doanh thu
        self.content_stack.addWidget(self.page_report) # Index 7: Báo cáo thống kê
        
        # Các trang còn lại (Cấu hình)
        for i in range(8, 9):
            page = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout(page)
            lbl = QtWidgets.QLabel(f"Trang đang phát triển: {menu_items[i][1]}")
            lbl.setStyleSheet("font-size: 24px; color: #888;")
            lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl)
            self.content_stack.addWidget(page)
            
    def switch_page(self, index):
        self.content_stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            style = "QPushButton { border: none; text-align: left; padding: 12px 15px; border-radius: 10px; font-size: 14px; color: #1e293b; font-weight: 600; }"
            if i == index:
                style += "QPushButton { background-color: #e1f2ee; color: #69c0a5; font-weight: 800; }"
            else:
                style += "QPushButton:hover { background-color: #f1f5f9; }"
            btn.setStyleSheet(style)

    def create_stat_card(self, icon, title, value, bg, color):
        card = QtWidgets.QFrame(); card.setStyleSheet(f"background-color: {bg}; border-radius: 15px; border: 1px solid #e2e8f0;")
        l = QtWidgets.QHBoxLayout(card); l.setContentsMargins(20, 20, 20, 20)
        ico = QtWidgets.QLabel(icon); ico.setStyleSheet(f"font-size: 30px; color: white; background: {color}; border-radius: 12px; padding: 8px;")
        v_l = QtWidgets.QVBoxLayout(); 
        t_lbl = QtWidgets.QLabel(title); t_lbl.setStyleSheet("color: #475569; font-weight: 700; font-size: 13px;")
        v_val = QtWidgets.QLabel(value); v_val.setStyleSheet(f"font-size: 28px; font-weight: 900; color: {color};")
        v_l.addWidget(t_lbl); v_l.addWidget(v_val); l.addWidget(ico); l.addLayout(v_l); l.addStretch()
        return card

# Để chạy thử nghiệm ứng dụng này:
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Thay đổi DashboardView() thành AdminDashboardView() để xem giao diện Admin
    window = AdminDashboardView() 
    window.setWindowTitle("CarePlus Management System")
    window.resize(1200, 850)
    window.show()
    sys.exit(app.exec())
