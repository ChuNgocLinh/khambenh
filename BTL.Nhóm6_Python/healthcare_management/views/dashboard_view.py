from PyQt6 import QtWidgets, QtCore, QtGui
import sys
from importlib import import_module
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
        self._settings_nav_buttons = []
        self._settings_section_frames = {}
        self._settings_notification_toggles = {}
        self._settings_display_value_labels = {}
        self._settings_scroll = None
        self._settings_avatar_icon = None
        self._settings_cached_values = {}
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # SideBar Bác Sĩ
        self.sidebar = QtWidgets.QFrame()
        self.sidebar.setFixedWidth(268)
        self.sidebar.setStyleSheet("background-color: #ffffff; border-right: 1px solid #edf2f7;")
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(18, 28, 18, 26)
        self.sidebar_layout.setSpacing(10)

        self.logo = QtWidgets.QLabel("⊕ CarePlus")
        self.logo.setStyleSheet(
            "color: #22c55e; font-size: 26px; font-weight: 900; margin-bottom: 28px; margin-left: 8px;"
        )
        self.sidebar_layout.addWidget(self.logo)

        menu_items = [
            ("🏠", "Trang chủ"),
            ("📅", "Lịch khám"),
            ("👥", "Danh sách bệnh nhân"),
            ("🩺", "Khám bệnh"),
            ("📂", "Hồ sơ bệnh nhân"),
            ("💊", "Đơn thuốc của tôi"),
            ("🔔", "Thông báo"),
            ("⚙️", "Cài đặt"),
        ]
        self.nav_buttons = []
        for i, (icon, text) in enumerate(menu_items):
            btn = QtWidgets.QPushButton(f"   {icon}     {text}")
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setFixedHeight(58)
            btn.setStyleSheet(self._doctor_sidebar_button_style(i == 0))
            btn.clicked.connect(lambda checked, idx=i: self.switch_page(idx))
            self.nav_buttons.append(btn)
            self.sidebar_layout.addWidget(btn)

        self.sidebar_layout.addStretch()

        self.btn_logout = QtWidgets.QPushButton("   ⎋     Đăng xuất")
        self.btn_logout.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_logout.setFixedHeight(54)
        self.btn_logout.setStyleSheet(
            "QPushButton { border: none; text-align: left; padding: 14px; padding-left: 20px; padding-right: 20px; border-radius: 16px; "
            "color: #ef4444; font-size: 14px; font-weight: 800; background: transparent; }"
            "QPushButton:hover { background: #fef2f2; }"
        )
        self.sidebar_layout.addWidget(self.btn_logout)
        self.main_layout.addWidget(self.sidebar)

        # Content Bác Sĩ
        self.content_container = QtWidgets.QWidget()
        self.content_container.setStyleSheet("background-color: #fbfdff;")
        self.content_layout = QtWidgets.QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(28, 22, 28, 22)
        self.content_layout.setSpacing(18)
        self.main_layout.addWidget(self.content_container)

        self.header_layout = QtWidgets.QHBoxLayout()
        self.header_title = QtWidgets.QLabel("")
        self.header_title.setStyleSheet("font-size: 1px; color: transparent;")
        self.header_title.setFixedWidth(1)
        self.header_layout.addWidget(self.header_title)
        self.header_layout.addStretch()

        bell_wrapper = QtWidgets.QWidget()
        bell_grid = QtWidgets.QGridLayout(bell_wrapper)
        bell_grid.setContentsMargins(0, 0, 0, 0)
        bell_grid.setHorizontalSpacing(0)
        bell_grid.setVerticalSpacing(0)

        self.header_notification_button = QtWidgets.QPushButton("🔔")
        self.header_notification_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.header_notification_button.setFixedSize(38, 38)
        self.header_notification_button.setStyleSheet(
            "QPushButton { background: transparent; border: none; font-size: 20px; color: #94a3b8; }"
            "QPushButton:hover { background: #f8fafc; border-radius: 19px; }"
        )
        bell_grid.addWidget(
            self.header_notification_button,
            0,
            0,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )

        self.bell_badge = QtWidgets.QLabel("0")
        self.bell_badge.setFixedSize(18, 18)
        self.bell_badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.bell_badge.setStyleSheet(
            "background: #ff2d20; color: white; border-radius: 9px; font-size: 10px; font-weight: 800;"
        )
        bell_grid.addWidget(
            self.bell_badge,
            0,
            0,
            alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight,
        )
        self.header_notification_button.clicked.connect(lambda: self.switch_page(6))

        self.user_info_layout = QtWidgets.QHBoxLayout()
        self.user_info_layout.setContentsMargins(0, 0, 0, 0)
        self.user_info_layout.setSpacing(14)

        profile_frame = QtWidgets.QFrame()
        profile_frame.setStyleSheet("background: transparent; border: none;")
        profile_layout = QtWidgets.QHBoxLayout(profile_frame)
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.setSpacing(10)

        self.user_avatar = QtWidgets.QLabel("👨‍⚕️")
        self.user_avatar.setFixedSize(42, 42)
        self.user_avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.user_avatar.setStyleSheet("background: #eef2ff; border-radius: 21px; font-size: 20px;")
        self.user_name_lbl = QtWidgets.QLabel(f"Bác sĩ {self.user_data.get('name')} ▿")
        self.user_name_lbl.setStyleSheet("font-weight: 800; color: #0f172a; font-size: 14px;")
        profile_layout.addWidget(self.user_avatar)
        profile_layout.addWidget(self.user_name_lbl)
        self.user_info_layout.addWidget(bell_wrapper)
        self.user_info_layout.addWidget(profile_frame)
        self.header_layout.addLayout(self.user_info_layout)
        self.content_layout.addLayout(self.header_layout)

        # QStackedWidget cho các trang
        self.content_stack = QtWidgets.QStackedWidget()
        self.content_layout.addWidget(self.content_stack)

        # ==========================================
        # TRANG 0: DASHBOARD
        # ==========================================
        self.page_dashboard = QtWidgets.QWidget()
        outer_layout = QtWidgets.QVBoxLayout(self.page_dashboard)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        self.dashboard_scroll = QtWidgets.QScrollArea()
        self.dashboard_scroll.setWidgetResizable(True)
        self.dashboard_scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.dashboard_scroll.setStyleSheet("background: transparent; border: none;")

        self.dashboard_container = QtWidgets.QWidget()
        self.dashboard_container.setStyleSheet("background-color: transparent;")

        self.page_dashboard_layout = QtWidgets.QVBoxLayout(self.dashboard_container)
        self.page_dashboard_layout.setContentsMargins(0, 0, 0, 0)
        self.page_dashboard_layout.setSpacing(20)

        self.dashboard_scroll.setWidget(self.dashboard_container)
        outer_layout.addWidget(self.dashboard_scroll)

        self.dashboard_filter_state = {
            "range_key": "30d",
            "from_date": QtCore.QDate.currentDate().addDays(-29),
            "to_date": QtCore.QDate.currentDate(),
        }
        self.dashboard_data = {}
        self._render_dashboard_page()

        self.content_stack.addWidget(self.page_dashboard)

        # Các trang placeholder khác
        from views.doctor_management_views import PrescriptionView, DoctorPatientListView
        from views.doctor_examination_view import DoctorExaminationView
        from views.doctor_patient_record_view import DoctorPatientRecordView
        from views.doctor_schedule_view import DoctorScheduleView
        
        self.page_patient_list = DoctorPatientListView(self.user_data.get("doctor_id"))
        self.page_doctor_appts = DoctorScheduleView(self.user_data.get("doctor_id"))
        self.page_medical_record = DoctorExaminationView(self.user_data.get("doctor_id"))
        self.page_patient_record = DoctorPatientRecordView(self.user_data.get("doctor_id"))
        self.page_prescription = PrescriptionView(self.user_data.get("doctor_id"))

        role = str(self.user_data.get("role") or "doctor").lower().strip()
        self.page_patient_list.role = role
        self.page_doctor_appts.role = role
        self.page_medical_record.role = role
        self.page_patient_record.role = role
        self.page_prescription.role = role
        
        self.content_stack.addWidget(self.page_doctor_appts)   # 1: Lịch khám
        self.content_stack.addWidget(self.page_patient_list)    # 2: Danh sách bệnh nhân
        self.content_stack.addWidget(self.page_medical_record)  # 3: Khám bệnh
        self.content_stack.addWidget(self.page_patient_record)  # 4: Hồ sơ bệnh nhân
        self.content_stack.addWidget(self.page_prescription)    # 5: Đơn thuốc
        self.content_stack.addWidget(self._build_persisted_notification_center_page())  # 6: Thông báo
        self.content_stack.addWidget(self._build_settings_page())  # 7: Cài đặt
        self.refresh_notification_badge()

    def _build_doctor_dashboard_data(self, doctor_id):
        from controllers.appointment_controller import AppointmentController
        from database.db import fetch_all

        now_dt = datetime.now()
        from_date = self.dashboard_filter_state.get("from_date", QtCore.QDate.currentDate().addDays(-29))
        to_date = self.dashboard_filter_state.get("to_date", QtCore.QDate.currentDate())
        from_dt = datetime(from_date.year(), from_date.month(), from_date.day(), 0, 0, 0)
        to_dt = datetime(to_date.year(), to_date.month(), to_date.day(), 23, 59, 59)
        day_span = max(1, from_dt.date().toordinal() - from_dt.date().toordinal() + (to_dt.date() - from_dt.date()).days + 1)

        appointments = AppointmentController.get_by_doctor(doctor_id)
        status_counts = {"pending": 0, "confirmed": 0, "in_progress": 0, "done": 0, "cancelled": 0}
        filtered_appointments = []
        today_appointments = []
        upcoming_appointments = []
        appointments_per_day = {}
        unique_patients_per_day = {}
        time_slot_counts = {"Sáng": 0, "Trưa": 0, "Chiều": 0, "Tối": 0}
        week_status_counts = {"done": 0, "in_progress": 0, "pending": 0, "confirmed": 0, "cancelled": 0}

        current_day = from_dt.date()
        while current_day <= to_dt.date():
            appointments_per_day[current_day] = 0
            unique_patients_per_day[current_day] = set()
            current_day += timedelta(days=1)

        for appointment in appointments:
            appt_dt = self._to_datetime(appointment.get("appointment_date"))
            if not appt_dt:
                continue

            status = str(appointment.get("status", "pending") or "pending").lower()
            if status in status_counts:
                status_counts[status] += 1

            if from_dt <= appt_dt <= to_dt:
                filtered_appointments.append(appointment)
                appointments_per_day.setdefault(appt_dt.date(), 0)
                appointments_per_day[appt_dt.date()] += 1
                if appointment.get("patient_id") is not None:
                    unique_patients_per_day.setdefault(appt_dt.date(), set()).add(appointment.get("patient_id"))

                slot_label = self._get_time_slot_label(appt_dt)
                time_slot_counts[slot_label] = time_slot_counts.get(slot_label, 0) + 1

            if appt_dt.date() == now_dt.date() and status in {"pending", "confirmed", "in_progress"}:
                today_appointments.append(appointment)

            if appt_dt >= now_dt and status in {"pending", "confirmed", "in_progress"}:
                upcoming_appointments.append(appointment)

            if appt_dt.isocalendar()[:2] == now_dt.isocalendar()[:2] and status in week_status_counts:
                week_status_counts[status] += 1

        record_rows = fetch_all(
            """
            SELECT mr.record_id, mr.created_at, mr.diagnosis, mr.treatment,
                   p.patient_id, p.name AS patient_name,
                   a.status AS appointment_status, a.appointment_date,
                   pr.prescription_id, pr.quantity,
                   m.name AS medicine_name,
                   m.description AS medicine_description,
                   CASE
                       WHEN a.note IS NULL OR a.note = '' THEN 'Khám tổng quát'
                       WHEN a.note LIKE 'Dịch vụ:%' THEN TRIM(SUBSTRING(a.note, 9))
                       ELSE a.note
                   END AS visit_type
            FROM MedicalRecords mr
            JOIN Patients p ON p.patient_id = mr.patient_id
            LEFT JOIN Appointments a ON a.appointment_id = mr.appointment_id
            LEFT JOIN Prescriptions pr ON pr.record_id = mr.record_id
            LEFT JOIN Medicines m ON m.medicine_id = pr.medicine_id
            WHERE mr.doctor_id = ?
            ORDER BY mr.created_at DESC, pr.prescription_id DESC
            """,
            (doctor_id,),
        )

        diagnosis_counts = {}
        prescription_type_counts = {}
        prescriptions_per_day = {}
        exam_duration_samples = []
        diagnosis_counted_records = set()
        exam_duration_counted_records = set()
        prescription_counted_records_by_day = {}
        monthly_appointment_count = 0
        monthly_done_count = 0
        month_start = now_dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        for row in record_rows:
            created_at = self._to_datetime(row.get("created_at"))
            if not created_at or not (from_dt <= created_at <= to_dt):
                continue

            record_id = row.get("record_id")
            if record_id not in diagnosis_counted_records:
                diagnosis_counted_records.add(record_id)
                diagnosis = str(row.get("diagnosis", "") or "Chưa cập nhật chẩn đoán").strip()
                diagnosis_counts[diagnosis] = diagnosis_counts.get(diagnosis, 0) + 1

            prescriptions_per_day.setdefault(created_at.date(), 0)
            prescription_counted_records_by_day.setdefault(created_at.date(), set())
            if row.get("prescription_id") and record_id not in prescription_counted_records_by_day[created_at.date()]:
                prescription_counted_records_by_day[created_at.date()].add(record_id)
                prescriptions_per_day[created_at.date()] += 1

            if row.get("prescription_id"):
                prescription_label = self._categorize_prescription_item(
                    row.get("medicine_name"),
                    row.get("medicine_description"),
                )
                prescription_type_counts[prescription_label] = prescription_type_counts.get(prescription_label, 0) + 1

            appt_time = self._to_datetime(row.get("appointment_date"))
            if appt_time and created_at >= appt_time and record_id not in exam_duration_counted_records:
                exam_duration_counted_records.add(record_id)
                duration_minutes = int((created_at - appt_time).total_seconds() // 60)
                if 1 <= duration_minutes <= 360:
                    exam_duration_samples.append(duration_minutes)

        for day_key in appointments_per_day.keys():
            prescriptions_per_day.setdefault(day_key, 0)

        for appointment in appointments:
            appt_dt = self._to_datetime(appointment.get("appointment_date"))
            if not appt_dt:
                continue
            if appt_dt >= month_start and appt_dt.month == now_dt.month and appt_dt.year == now_dt.year:
                monthly_appointment_count += 1
                if str(appointment.get("status", "")).lower() == "done":
                    monthly_done_count += 1

        filtered_patient_ids = {
            appointment.get("patient_id")
            for appointment in filtered_appointments
            if appointment.get("patient_id") is not None
        }

        patient_visit_counts = {}
        done_patient_ids = set()
        for appt in filtered_appointments:
            patient_id = appt.get("patient_id")
            if patient_id is None:
                continue
            patient_visit_counts[patient_id] = patient_visit_counts.get(patient_id, 0) + 1
            if str(appt.get("status", "")).lower() == "done":
                done_patient_ids.add(patient_id)

        revisit_patients = sum(1 for count in patient_visit_counts.values() if count >= 2)
        revisit_rate = (revisit_patients / len(patient_visit_counts) * 100) if patient_visit_counts else 0.0

        avg_exam_minutes = (
            sum(exam_duration_samples) / len(exam_duration_samples)
            if exam_duration_samples
            else 18.0
        )

        completed_filtered = sum(1 for appt in filtered_appointments if str(appt.get("status", "")).lower() == "done")
        pending_filtered = sum(1 for appt in filtered_appointments if str(appt.get("status", "")).lower() in {"pending", "confirmed"})

        week_total = sum(week_status_counts.values())
        week_avg_per_day = week_total / 7 if week_total else 0
        week_completion_rate = (week_status_counts.get("done", 0) / week_total * 100) if week_total else 0

        notifications = []
        if pending_filtered > 0:
            notifications.append(f"Có {pending_filtered} lịch cần xác nhận hoặc chuẩn bị khám trong khoảng thời gian đang xem")
        if today_appointments:
            notifications.append(f"Hôm nay còn {len(today_appointments)} lịch hẹn hoạt động")
        if not notifications:
            notifications = ["Không có cảnh báo nổi bật trong giai đoạn đã chọn"]

        sorted_upcoming = sorted(
            upcoming_appointments,
            key=lambda a: self._to_datetime(a.get("appointment_date")) or now_dt,
        )[:5]

        trend_labels = [day.strftime("%d/%m") for day in appointments_per_day.keys()]
        patient_trend_values = [len(unique_patients_per_day.get(day, set())) for day in appointments_per_day.keys()]
        prescription_trend_values = [prescriptions_per_day.get(day, 0) for day in appointments_per_day.keys()]
        top_diseases = sorted(diagnosis_counts.items(), key=lambda item: (-item[1], item[0]))[:5]
        time_slot_distribution = [(label, time_slot_counts.get(label, 0)) for label in ["Sáng", "Trưa", "Chiều", "Tối"]]
        visit_type_data = sorted(prescription_type_counts.items(), key=lambda item: (-item[1], item[0]))[:5]

        current_month_label = now_dt.strftime("%m/%Y")
        month_completion_rate = (monthly_done_count / monthly_appointment_count * 100) if monthly_appointment_count else 0

        return {
            "today_appointments": sorted(today_appointments, key=lambda a: self._to_datetime(a.get("appointment_date")) or now_dt),
            "upcoming_appointments": sorted_upcoming,
            "notifications": notifications,
            "notification_count": len(notifications),
            "kpis": {
                "total_examined_patients": len(done_patient_ids),
                "total_appointments": len(filtered_appointments),
                "prescriptions": sum(prescriptions_per_day.values()),
                "avg_exam_minutes": avg_exam_minutes,
                "revisit_rate": revisit_rate,
                "unique_patients": len(filtered_patient_ids),
                "completed": completed_filtered,
            },
            "status_counts": status_counts,
            "patient_trend_labels": trend_labels,
            "patient_trend_values": patient_trend_values,
            "prescription_trend_labels": trend_labels,
            "prescription_trend_values": prescription_trend_values,
            "top_diseases": top_diseases,
            "prescription_category_distribution": visit_type_data,
            "time_slot_distribution": time_slot_distribution,
            "weekly_summary": {
                "done": week_status_counts.get("done", 0),
                "active": week_status_counts.get("in_progress", 0),
                "waiting": week_status_counts.get("pending", 0) + week_status_counts.get("confirmed", 0),
                "cancelled": week_status_counts.get("cancelled", 0),
                "avg_per_day": week_avg_per_day,
                "completion_rate": week_completion_rate,
            },
            "month_summary": {
                "label": current_month_label,
                "appointments": monthly_appointment_count,
                "completed": monthly_done_count,
                "completion_rate": month_completion_rate,
            },
            "updated_at": now_dt.strftime("%H:%M %d/%m/%Y"),
        }

    def _render_dashboard_page(self):
        while self.page_dashboard_layout.count():
            item = self.page_dashboard_layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self._clear_layout(child_layout)

        # MAIN HORIZONTAL LAYOUT
        main_h_layout = QtWidgets.QHBoxLayout()
        main_h_layout.setSpacing(20)

        # LEFT SIDE
        left_v_layout = QtWidgets.QVBoxLayout()
        left_v_layout.setSpacing(20)

        # Top 4 cards row
        cards_layout = QtWidgets.QHBoxLayout()
        cards_layout.setSpacing(15)
        
        cards = [
            ("Lịch hẹn hôm nay", "12", "Ca khám", "📅", "#ecfdf5", "#10b981", "#10b981"),
            ("Đang khám", "1", "Bệnh nhân", "🩺", "#eff6ff", "#3b82f6", "#3b82f6"),
            ("Hoàn thành", "8", "Ca khám", "📋", "#fff7ed", "#f97316", "#f97316"),
            ("Tổng bệnh nhân", "156", "Bệnh nhân", "👥", "#f5f3ff", "#8b5cf6", "#8b5cf6"),
        ]
        
        for title, value, unit, icon, bg_color, icon_color, text_color in cards:
            card = QtWidgets.QFrame()
            card.setStyleSheet(f"background-color: white; border-radius: 16px; border: 1px solid #f1f5f9;")
            card.setFixedHeight(110)
            card_l = QtWidgets.QHBoxLayout(card)
            card_l.setContentsMargins(20, 20, 20, 20)
            
            icon_lbl = QtWidgets.QLabel(icon)
            icon_lbl.setFixedSize(50, 50)
            icon_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            icon_lbl.setStyleSheet(f"background-color: {bg_color}; color: {icon_color}; font-size: 24px; border-radius: 12px;")
            card_l.addWidget(icon_lbl)
            
            text_l = QtWidgets.QVBoxLayout()
            text_l.setSpacing(2)
            title_lbl = QtWidgets.QLabel(title)
            title_lbl.setStyleSheet("font-size: 13px; color: #64748b; font-weight: bold; background: transparent; border: none;")
            val_lbl = QtWidgets.QLabel(value)
            val_lbl.setStyleSheet(f"font-size: 28px; color: {text_color}; font-weight: 800; background: transparent; border: none;")
            unit_lbl = QtWidgets.QLabel(unit)
            unit_lbl.setStyleSheet("font-size: 12px; color: #94a3b8; background: transparent; border: none;")
            
            text_l.addWidget(title_lbl)
            
            val_unit_l = QtWidgets.QHBoxLayout()
            val_unit_l.addWidget(val_lbl)
            val_unit_l.addWidget(unit_lbl)
            val_unit_l.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignBottom)
            text_l.addLayout(val_unit_l)
            
            card_l.addLayout(text_l)
            card_l.addStretch()
            cards_layout.addWidget(card)

        left_v_layout.addLayout(cards_layout)

        # Table Section
        table_card = QtWidgets.QFrame()
        table_card.setStyleSheet("background-color: white; border-radius: 16px; border: 1px solid #f1f5f9;")
        table_l = QtWidgets.QVBoxLayout(table_card)
        table_l.setContentsMargins(20, 20, 20, 20)
        table_l.setSpacing(15)
        
        table_title = QtWidgets.QLabel("Lịch khám hôm nay")
        table_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e293b; background: transparent; border: none;")
        table_l.addWidget(table_title)
        
        table = QtWidgets.QTableWidget(5, 5)
        table.setHorizontalHeaderLabels(["Giờ hẹn", "Bệnh nhân", "Lý do khám", "Trạng thái", "Thao tác"])
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        table.setStyleSheet("""
            QTableWidget { border: none; background: white; }
            QHeaderView::section { background-color: white; color: #1e293b; font-weight: bold; font-size: 13px; border: none; border-bottom: 1px solid #e2e8f0; padding: 10px; text-align: left; }
            QTableWidget::item { border-bottom: 1px solid #f8fafc; padding: 5px; }
        """)
        
        rows_data = [
            ("08:00", "Trần Văn Nam", "Nam - 35 tuổi", "Khám tổng quát", "Đã khám", "#10b981", "#ecfdf5", "👁"),
            ("09:00", "Lê Thị Hoa", "Nữ - 29 tuổi", "Tư vấn sức khỏe", "Đang khám", "#3b82f6", "#eff6ff", "🩺"),
            ("10:00", "Nguyễn Hoàng Anh", "Nam - 42 tuổi", "Đau đầu, chóng mặt", "Đang chờ", "#f97316", "#fff7ed", "👁"),
            ("10:30", "Phạm Minh Đức", "Nam - 31 tuổi", "Khám nhi", "Đang chờ", "#f97316", "#fff7ed", "👁"),
            ("11:00", "Vũ Thị Mai", "Nữ - 28 tuổi", "Khám tổng quát", "Đã đặt lịch", "#64748b", "#f1f5f9", "👁"),
        ]
        
        for r, (time_val, name_val, detail_val, reason, status, status_color, status_bg, action_icon) in enumerate(rows_data):
            # Time
            time_item = QtWidgets.QTableWidgetItem(time_val)
            time_item.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Weight.Bold))
            time_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            table.setItem(r, 0, time_item)
            
            # Patient Info
            patient_w = QtWidgets.QWidget()
            patient_l = QtWidgets.QHBoxLayout(patient_w)
            patient_l.setContentsMargins(0, 0, 0, 0)
            patient_l.setSpacing(10)
            avt = QtWidgets.QLabel("👤")
            avt.setFixedSize(32, 32)
            avt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            if "Nữ" in detail_val:
                avt.setStyleSheet("background-color: #fce7f3; color: #db2777; border-radius: 16px;")
            else:
                avt.setStyleSheet("background-color: #e0f2fe; color: #0284c7; border-radius: 16px;")
            
            info_l = QtWidgets.QVBoxLayout()
            info_l.setSpacing(0)
            n_lbl = QtWidgets.QLabel(name_val)
            n_lbl.setStyleSheet("color: #1e293b; font-weight: bold; font-size: 13px; background: transparent; border: none;")
            d_lbl = QtWidgets.QLabel(detail_val)
            d_lbl.setStyleSheet("color: #64748b; font-size: 11px; background: transparent; border: none;")
            info_l.addWidget(n_lbl)
            info_l.addWidget(d_lbl)
            
            patient_l.addWidget(avt)
            patient_l.addLayout(info_l)
            patient_l.addStretch()
            table.setCellWidget(r, 1, patient_w)
            
            # Reason
            reason_item = QtWidgets.QTableWidgetItem(reason)
            reason_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            reason_item.setForeground(QtGui.QBrush(QtGui.QColor("#475569")))
            table.setItem(r, 2, reason_item)
            
            # Status
            status_w = QtWidgets.QWidget()
            status_l = QtWidgets.QHBoxLayout(status_w)
            status_l.setContentsMargins(0, 0, 0, 0)
            status_l.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            status_lbl = QtWidgets.QLabel(status)
            status_lbl.setStyleSheet(f"background-color: {status_bg}; color: {status_color}; font-weight: bold; font-size: 11px; padding: 4px 10px; border-radius: 10px;")
            status_l.addWidget(status_lbl)
            table.setCellWidget(r, 3, status_w)
            
            # Action
            action_w = QtWidgets.QWidget()
            action_l = QtWidgets.QHBoxLayout(action_w)
            action_l.setContentsMargins(0, 0, 0, 0)
            action_l.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            action_btn = QtWidgets.QPushButton(action_icon)
            action_btn.setFixedSize(32, 32)
            action_btn.setStyleSheet("background-color: #eff6ff; color: #3b82f6; border-radius: 16px; font-size: 14px; border: none;")
            action_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            action_l.addWidget(action_btn)
            table.setCellWidget(r, 4, action_w)
            
            table.setRowHeight(r, 60)
            
        table.setFixedHeight(350)
        table_l.addWidget(table)
        
        btn_view_all_appts = QtWidgets.QPushButton("Xem tất cả lịch hẹn >")
        btn_view_all_appts.setStyleSheet("color: #3b82f6; font-weight: bold; font-size: 13px; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px; background: white;")
        btn_view_all_appts.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        table_l.addWidget(btn_view_all_appts)
        
        left_v_layout.addWidget(table_card)

        # Bottom row (Recent patients & To-do)
        bottom_h_layout = QtWidgets.QHBoxLayout()
        bottom_h_layout.setSpacing(20)

        # Recent Patients
        recent_card = QtWidgets.QFrame()
        recent_card.setStyleSheet("background-color: white; border-radius: 16px; border: 1px solid #f1f5f9;")
        recent_l = QtWidgets.QVBoxLayout(recent_card)
        recent_l.setContentsMargins(20, 20, 20, 20)
        recent_l.setSpacing(15)
        
        recent_header = QtWidgets.QHBoxLayout()
        recent_title = QtWidgets.QLabel("Bệnh nhân gần đây")
        recent_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e293b; background: transparent; border: none;")
        recent_view_all = QtWidgets.QPushButton("Xem tất cả")
        recent_view_all.setStyleSheet("color: #3b82f6; font-size: 13px; font-weight: bold; border: none; background: transparent;")
        recent_view_all.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        recent_header.addWidget(recent_title)
        recent_header.addStretch()
        recent_header.addWidget(recent_view_all)
        recent_l.addLayout(recent_header)
        
        recent_data = [
            ("Nguyễn Thanh Tùng", "Nam - 28 tuổi", "07/05/2026", "Khám tổng quát", False),
            ("Đỗ Thị Phương", "Nữ - 34 tuổi", "06/05/2026", "Tư vấn sức khỏe", True),
            ("Lý Minh Tuấn", "Nam - 42 tuổi", "05/05/2026", "Đau lưng", False),
            ("Hoàng Văn Dũng", "Nam - 50 tuổi", "04/05/2026", "Kiểm tra sức khỏe", False),
        ]
        
        for name, detail, date_str, reason, is_female in recent_data:
            item_w = QtWidgets.QWidget()
            item_l = QtWidgets.QHBoxLayout(item_w)
            item_l.setContentsMargins(0, 5, 0, 5)
            
            avt = QtWidgets.QLabel("👤")
            avt.setFixedSize(36, 36)
            avt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            if is_female:
                avt.setStyleSheet("background-color: #fce7f3; color: #db2777; border-radius: 18px;")
            else:
                avt.setStyleSheet("background-color: #e0f2fe; color: #0284c7; border-radius: 18px;")
            item_l.addWidget(avt)
            
            info_l = QtWidgets.QVBoxLayout()
            info_l.setSpacing(2)
            n_lbl = QtWidgets.QLabel(name)
            n_lbl.setStyleSheet("color: #1e293b; font-weight: bold; font-size: 13px; background: transparent; border: none;")
            d_lbl = QtWidgets.QLabel(detail)
            d_lbl.setStyleSheet("color: #64748b; font-size: 12px; background: transparent; border: none;")
            info_l.addWidget(n_lbl)
            info_l.addWidget(d_lbl)
            item_l.addLayout(info_l)
            
            item_l.addStretch()
            
            date_l = QtWidgets.QVBoxLayout()
            date_l.setSpacing(2)
            dt_lbl = QtWidgets.QLabel(date_str)
            dt_lbl.setStyleSheet("color: #64748b; font-size: 12px; background: transparent; border: none;")
            dt_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            r_lbl = QtWidgets.QLabel(reason)
            r_lbl.setStyleSheet("color: #94a3b8; font-size: 12px; background: transparent; border: none;")
            r_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            date_l.addWidget(dt_lbl)
            date_l.addWidget(r_lbl)
            item_l.addLayout(date_l)
            
            recent_l.addWidget(item_w)
        
        recent_l.addStretch()
        bottom_h_layout.addWidget(recent_card)

        # To-Do List
        todo_card = QtWidgets.QFrame()
        todo_card.setStyleSheet("background-color: white; border-radius: 16px; border: 1px solid #f1f5f9;")
        todo_l = QtWidgets.QVBoxLayout(todo_card)
        todo_l.setContentsMargins(20, 20, 20, 20)
        todo_l.setSpacing(15)
        
        todo_title = QtWidgets.QLabel("Công việc cần làm")
        todo_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e293b; background: transparent; border: none;")
        todo_l.addWidget(todo_title)
        
        todo_data = [
            ("Xem kết quả xét nghiệm", "3", "#fef2f2", "#ef4444"),
            ("Ký đơn thuốc", "2", "#fff7ed", "#f97316"),
            ("Hoàn thiện hồ sơ bệnh án", "4", "#fef2f2", "#ef4444"),
            ("Nhắc lịch tái khám", "1", "#fdf2f8", "#ec4899"),
        ]
        
        for text, badge, badge_bg, badge_color in todo_data:
            item_w = QtWidgets.QWidget()
            item_l = QtWidgets.QHBoxLayout(item_w)
            item_l.setContentsMargins(0, 10, 0, 10)
            
            icon = QtWidgets.QLabel("📋")
            icon.setStyleSheet("color: #3b82f6; font-size: 18px; background: transparent; border: none;")
            item_l.addWidget(icon)
            
            t_lbl = QtWidgets.QLabel(text)
            t_lbl.setStyleSheet("color: #334155; font-size: 14px; font-weight: 500; background: transparent; border: none;")
            item_l.addWidget(t_lbl)
            
            item_l.addStretch()
            
            b_lbl = QtWidgets.QLabel(badge)
            b_lbl.setFixedSize(24, 24)
            b_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            b_lbl.setStyleSheet(f"background-color: {badge_bg}; color: {badge_color}; border-radius: 12px; font-weight: bold; font-size: 12px;")
            item_l.addWidget(b_lbl)
            
            todo_l.addWidget(item_w)
            
            line = QtWidgets.QFrame()
            line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
            line.setStyleSheet("color: #f1f5f9; background-color: #f1f5f9;")
            todo_l.addWidget(line)
        
        todo_l.addStretch()
        
        btn_view_all_todo = QtWidgets.QPushButton("Xem tất cả công việc >")
        btn_view_all_todo.setStyleSheet("color: #3b82f6; font-weight: bold; font-size: 13px; border: none; background: transparent;")
        btn_view_all_todo.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        todo_l.addWidget(btn_view_all_todo)
        
        bottom_h_layout.addWidget(todo_card)

        left_v_layout.addLayout(bottom_h_layout)
        
        main_h_layout.addLayout(left_v_layout, 7)

        # RIGHT SIDE
        right_v_layout = QtWidgets.QVBoxLayout()
        right_v_layout.setSpacing(20)

        # Calendar placeholder
        cal_card = QtWidgets.QFrame()
        cal_card.setStyleSheet("background-color: white; border-radius: 16px; border: 1px solid #f1f5f9;")
        cal_l = QtWidgets.QVBoxLayout(cal_card)
        cal_l.setContentsMargins(20, 20, 20, 20)
        cal_title = QtWidgets.QLabel("Lịch làm việc")
        cal_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e293b; background: transparent; border: none;")
        cal_l.addWidget(cal_title)
        
        # Fake calendar header
        cal_header = QtWidgets.QHBoxLayout()
        cal_prev = QtWidgets.QLabel("<")
        cal_prev.setStyleSheet("color: #64748b; font-weight: bold; background: transparent; border: none;")
        cal_month = QtWidgets.QLabel("Tháng 5, 2026")
        cal_month.setStyleSheet("font-weight: bold; color: #1e293b; background: transparent; border: none;")
        cal_month.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        cal_next = QtWidgets.QLabel(">")
        cal_next.setStyleSheet("color: #64748b; font-weight: bold; background: transparent; border: none;")
        cal_header.addWidget(cal_prev)
        cal_header.addWidget(cal_month)
        cal_header.addWidget(cal_next)
        cal_l.addLayout(cal_header)
        cal_l.addSpacing(10)
        
        # Fake calendar grid
        cal_grid = QtWidgets.QGridLayout()
        days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
        for i, d in enumerate(days):
            l = QtWidgets.QLabel(d)
            l.setStyleSheet("font-weight: bold; color: #1e293b; font-size: 12px; background: transparent; border: none;")
            l.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            cal_grid.addWidget(l, 0, i)
        
        dates = [
            [28, 29, 30, 1, 2, 3, 4],
            [5, 6, 7, 8, 9, 10, 11],
            [12, 13, 14, 15, 16, 17, 18],
            [19, 20, 21, 22, 23, 24, 25],
            [26, 27, 28, 29, 30, 31, 1]
        ]
        
        for r_idx, row_dates in enumerate(dates):
            for c_idx, d in enumerate(row_dates):
                l = QtWidgets.QLabel(str(d))
                l.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                if d == 8 and r_idx == 1:
                    l.setStyleSheet("background-color: #10b981; color: white; border-radius: 12px; font-weight: bold;")
                    l.setFixedSize(24, 24)
                elif (r_idx == 0 and d > 20) or (r_idx == 4 and d < 10):
                    l.setStyleSheet("color: #cbd5e1; font-size: 13px; background: transparent; border: none;")
                else:
                    l.setStyleSheet("color: #334155; font-size: 13px; background: transparent; border: none;")
                
                cell_w = QtWidgets.QWidget()
                cell_l = QtWidgets.QVBoxLayout(cell_w)
                cell_l.setContentsMargins(0,0,0,0)
                cell_l.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                cell_l.addWidget(l)
                
                if d in [8, 5, 15, 22] and not (r_idx == 0 and d > 20) and not (r_idx == 4 and d < 10):
                    dot = QtWidgets.QLabel("•")
                    dot.setStyleSheet("color: #10b981; font-size: 16px; margin-top: -10px; background: transparent; border: none;")
                    dot.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    cell_l.addWidget(dot)
                    
                cal_grid.addWidget(cell_w, r_idx+1, c_idx)
                
        cal_l.addLayout(cal_grid)
        right_v_layout.addWidget(cal_card)

        # Timeline
        timeline_card = QtWidgets.QFrame()
        timeline_card.setStyleSheet("background-color: white; border-radius: 16px; border: 1px solid #f1f5f9;")
        timeline_l = QtWidgets.QVBoxLayout(timeline_card)
        timeline_l.setContentsMargins(20, 20, 20, 20)
        timeline_l.setSpacing(15)
        timeline_title = QtWidgets.QLabel("Lịch làm việc hôm nay")
        timeline_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e293b; background: transparent; border: none;")
        timeline_l.addWidget(timeline_title)
        
        timeline_data = [
            ("08:00", "Trần Văn Nam", "✔ Đã khám", "#10b981"),
            ("09:00", "Lê Thị Hoa", "• Đang khám", "#3b82f6"),
            ("10:00", "Nguyễn Hoàng Anh", "• Đang chờ", "#f97316"),
            ("10:30", "Phạm Minh Đức", "• Đang chờ", "#f97316"),
            ("11:00", "Vũ Thị Mai", "• Đã đặt lịch", "#64748b"),
        ]
        
        for time_str, name, status, color in timeline_data:
            t_w = QtWidgets.QWidget()
            t_l = QtWidgets.QHBoxLayout(t_w)
            t_l.setContentsMargins(0, 5, 0, 5)
            
            time_lbl = QtWidgets.QLabel(time_str)
            time_lbl.setStyleSheet("color: #1e293b; font-weight: bold; font-size: 13px; min-width: 40px; background: transparent; border: none;")
            t_l.addWidget(time_lbl)
            
            name_lbl = QtWidgets.QLabel(name)
            name_lbl.setStyleSheet("color: #475569; font-size: 13px; background: transparent; border: none;")
            t_l.addWidget(name_lbl)
            
            t_l.addStretch()
            
            status_lbl = QtWidgets.QLabel(status)
            status_lbl.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: bold; background: transparent; border: none;")
            t_l.addWidget(status_lbl)
            
            timeline_l.addWidget(t_w)
            
            line = QtWidgets.QFrame()
            line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
            line.setStyleSheet("color: #f8fafc; background-color: #f8fafc;")
            timeline_l.addWidget(line)
            
        btn_view_full = QtWidgets.QPushButton("📅 Xem lịch đầy đủ")
        btn_view_full.setStyleSheet("color: #3b82f6; font-weight: bold; font-size: 13px; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px; background: white;")
        btn_view_full.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        timeline_l.addWidget(btn_view_full)
        
        right_v_layout.addWidget(timeline_card)
        right_v_layout.addStretch()

        main_h_layout.addLayout(right_v_layout, 3)

        self.page_dashboard_layout.addLayout(main_h_layout)

    def _build_dashboard_filter_bar(self):
        wrapper = QtWidgets.QFrame()
        wrapper.setStyleSheet("background: white; border-radius: 18px; border: 1px solid #e2e8f0;")
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(14)

        self.range_combo = QtWidgets.QComboBox()
        self.range_combo.addItem("7 ngày gần nhất", "7d")
        self.range_combo.addItem("30 ngày gần nhất", "30d")
        self.range_combo.addItem("90 ngày gần nhất", "90d")
        self.range_combo.addItem("Tháng này", "month")

        current_key = self.dashboard_filter_state.get("range_key", "30d")
        range_idx = self.range_combo.findData(current_key)
        if range_idx >= 0:
            self.range_combo.setCurrentIndex(range_idx)

        self.range_from_input = QtWidgets.QDateEdit(self.dashboard_filter_state.get("from_date"))
        self.range_from_input.setCalendarPopup(True)
        self.range_from_input.setDisplayFormat("dd/MM/yyyy")
        self.range_to_input = QtWidgets.QDateEdit(self.dashboard_filter_state.get("to_date"))
        self.range_to_input.setCalendarPopup(True)
        self.range_to_input.setDisplayFormat("dd/MM/yyyy")

        for label_text, widget in [
            ("Khoảng thời gian", self.range_combo),
            ("Từ ngày", self.range_from_input),
            ("Đến ngày", self.range_to_input),
        ]:
            col = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel(label_text)
            label.setStyleSheet("font-size: 12px; font-weight: 700; color: #475569;")
            widget.setStyleSheet(
                "padding: 8px 10px; border-radius: 8px; border: 1px solid #dbe2ea; background: white; color: #1f2937;"
            )
            col.addWidget(label)
            col.addWidget(widget)
            layout.addLayout(col)

        apply_btn = QtWidgets.QPushButton("Cập nhật")
        apply_btn.setStyleSheet(
            "background: #69c0a5; color: white; border-radius: 8px; padding: 10px 16px; font-weight: 800;"
        )
        apply_btn.clicked.connect(self._apply_dashboard_filters)
        layout.addStretch()
        layout.addWidget(apply_btn)
        self.range_combo.currentIndexChanged.connect(self._sync_dashboard_dates_from_preset)
        return wrapper

    def _build_dashboard_kpi_row(self):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(18)
        kpis = self.dashboard_data.get("kpis", {})
        cards = [
            ("👥", "Tổng bệnh nhân đã khám", str(kpis.get("total_examined_patients", 0)), "#e6f2ff", "#2563eb"),
            ("🗓️", "Tổng lịch hẹn", str(kpis.get("total_appointments", 0)), "#fff7ed", "#ea580c"),
            ("💊", "Tổng đơn thuốc đã kê", str(kpis.get("prescriptions", 0)), "#ecfdf3", "#15803d"),
            (
                "⏱️",
                "Độ trễ ghi nhận bệnh án TB",
                f"{kpis.get('avg_exam_minutes', 0):.1f} phút",
                "#f5f3ff",
                "#7c3aed",
            ),
            (
                "🔁",
                "Tỷ lệ tái khám",
                f"{kpis.get('revisit_rate', 0):.1f}%",
                "#fef2f2",
                "#be123c",
            ),
        ]
        for icon, title, value, bg, color in cards:
            row.addWidget(self.create_stat_card(icon, title, value, bg, color))
        return row

    def _build_dashboard_analytics_row(self):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(20)
        row.addWidget(self._build_status_analytics_card(), 5)
        row.addWidget(self._build_top_diseases_card(), 5)
        return row

    def _build_dashboard_trend_row(self):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(20)
        row.addWidget(
            self._build_chart_card(
                "Xu hướng bệnh nhân theo ngày",
                DoctorLineChartWidget(
                    self.dashboard_data.get("patient_trend_labels", []),
                    self.dashboard_data.get("patient_trend_values", []),
                ),
            ),
            1,
        )
        row.addWidget(
            self._build_chart_card(
                "Xu hướng kê đơn theo ngày",
                DoctorLineChartWidget(
                    self.dashboard_data.get("prescription_trend_labels", []),
                    self.dashboard_data.get("prescription_trend_values", []),
                ),
            ),
            1,
        )
        return row

    def _build_dashboard_distribution_row(self):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(20)
        row.addWidget(
            self._build_chart_card(
                "Phân loại thuốc đã kê",
                DoctorPieChartWidget(self.dashboard_data.get("prescription_category_distribution", [])),
            ),
            1,
        )
        row.addWidget(
            self._build_chart_card(
                "Phân bố lịch hẹn theo khung giờ",
                DoctorPieChartWidget(self.dashboard_data.get("time_slot_distribution", [])),
            ),
            1,
        )
        return row

    def _build_dashboard_summary_row(self):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(20)
        row.addWidget(self._build_weekly_summary_card(), 1)
        row.addWidget(self._build_month_summary_card(), 1)
        return row

    def _build_chart_card(self, title_text, widget):
        frame = QtWidgets.QFrame()
        frame.setStyleSheet("background: white; border-radius: 20px; border: 1px solid #e2e8f0;")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(18, 18, 18, 18)
        title = QtWidgets.QLabel(title_text)
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #1e293b;")
        layout.addWidget(title)
        layout.addWidget(widget)
        return frame

    def _build_status_analytics_card(self):
        frame = QtWidgets.QFrame()
        frame.setStyleSheet("background: white; border-radius: 20px; border: 1px solid #e2e8f0;")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        title = QtWidgets.QLabel("Phân tích trạng thái lịch hẹn")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #1e293b;")
        layout.addWidget(title)

        table = QtWidgets.QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Trạng thái", "Số lượng", "Ghi chú"])
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setStyleSheet(
            "QTableWidget { color: #1f2937; background: white; }"
            "QHeaderView::section { background-color: #f8f9fa; padding: 10px; border: none; font-weight: 700; }"
            "QTableWidget::item { padding: 8px; border-bottom: 1px solid #f1f5f9; }"
        )

        status_counts = self.dashboard_data.get("status_counts", {})
        rows = [
            ("Chờ xác nhận", status_counts.get("pending", 0), "Lịch mới tạo hoặc chưa phản hồi"),
            ("Đã xác nhận", status_counts.get("confirmed", 0), "Sẵn sàng tiếp nhận"),
            ("Đang khám", status_counts.get("in_progress", 0), "Bệnh nhân đang được xử lý"),
            ("Đã khám", status_counts.get("done", 0), "Ca đã hoàn tất"),
            ("Đã hủy", status_counts.get("cancelled", 0), "Lịch không còn hiệu lực"),
        ]
        table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, text in enumerate(row):
                table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(text)))
            table.setRowHeight(row_idx, 42)
        layout.addWidget(table)
        return frame

    def _build_top_diseases_card(self):
        frame = QtWidgets.QFrame()
        frame.setStyleSheet("background: white; border-radius: 20px; border: 1px solid #e2e8f0;")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        title = QtWidgets.QLabel("Top 5 bệnh thường gặp")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #1e293b;")
        layout.addWidget(title)

        disease_rows = self.dashboard_data.get("top_diseases", [])
        if not disease_rows:
            empty = QtWidgets.QLabel("Chưa có dữ liệu chẩn đoán trong khoảng thời gian đã chọn.")
            empty.setStyleSheet("font-size: 13px; color: #94a3b8;")
            layout.addWidget(empty)
        else:
            for index, (label, count) in enumerate(disease_rows, start=1):
                card = QtWidgets.QFrame()
                card.setStyleSheet("background: #f8fafc; border-radius: 12px;")
                row = QtWidgets.QHBoxLayout(card)
                row.setContentsMargins(12, 10, 12, 10)
                name_lbl = QtWidgets.QLabel(f"#{index} {label}")
                name_lbl.setStyleSheet("font-size: 13px; font-weight: 700; color: #1e293b;")
                count_lbl = QtWidgets.QLabel(f"{count} ca")
                count_lbl.setStyleSheet("font-size: 13px; font-weight: 800; color: #0f766e;")
                row.addWidget(name_lbl)
                row.addStretch()
                row.addWidget(count_lbl)
                layout.addWidget(card)

        layout.addStretch()
        return frame

    def _build_weekly_summary_card(self):
        summary = self.dashboard_data.get("weekly_summary", {})
        frame = QtWidgets.QFrame()
        frame.setStyleSheet("background: white; border-radius: 20px; border: 1px solid #e2e8f0;")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        title = QtWidgets.QLabel("Hiệu suất khám theo tuần")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #1e293b;")
        layout.addWidget(title)

        items = [
            f"• Hoàn tất: {summary.get('done', 0)} ca",
            f"• Đang khám: {summary.get('active', 0)} ca",
            f"• Chờ xử lý: {summary.get('waiting', 0)} ca",
            f"• Hủy lịch: {summary.get('cancelled', 0)} ca",
            f"• Trung bình: {summary.get('avg_per_day', 0):.1f} lịch/ngày",
            f"• Tỷ lệ hoàn tất: {summary.get('completion_rate', 0):.1f}%",
        ]
        for text in items:
            label = QtWidgets.QLabel(text)
            label.setStyleSheet("font-size: 13px; color: #334155;")
            layout.addWidget(label)
        layout.addStretch()
        return frame

    def _build_month_summary_card(self):
        summary = self.dashboard_data.get("month_summary", {})
        frame = QtWidgets.QFrame()
        frame.setStyleSheet("background: #ecfdf3; border-radius: 20px; border: 1px solid #bbf7d0;")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(8)

        title = QtWidgets.QLabel(f"Tổng tháng này ({summary.get('label', '')})")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #166534;")
        layout.addWidget(title)

        total_lbl = QtWidgets.QLabel(str(summary.get("appointments", 0)))
        total_lbl.setStyleSheet("font-size: 42px; font-weight: 900; color: #166534;")
        layout.addWidget(total_lbl)

        detail = QtWidgets.QLabel(
            f"{summary.get('completed', 0)} lịch đã hoàn tất • Tỷ lệ xử lý {summary.get('completion_rate', 0):.1f}%"
        )
        detail.setWordWrap(True)
        detail.setStyleSheet("font-size: 13px; color: #166534;")
        layout.addWidget(detail)

        footer = QtWidgets.QLabel("Thẻ này phản ánh tình hình tháng hiện tại, không phụ thuộc hoàn toàn vào filter hiển thị.")
        footer.setWordWrap(True)
        footer.setStyleSheet("font-size: 12px; color: #15803d;")
        layout.addWidget(footer)
        layout.addStretch()
        return frame

    def _apply_dashboard_filters(self):
        from_date = self.range_from_input.date()
        to_date = self.range_to_input.date()
        if from_date > to_date:
            QtWidgets.QMessageBox.warning(self, "Khoảng thời gian không hợp lệ", "Ngày bắt đầu không được lớn hơn ngày kết thúc.")
            return

        self.dashboard_filter_state = {
            "range_key": self.range_combo.currentData() or "custom",
            "from_date": from_date,
            "to_date": to_date,
        }
        self._render_dashboard_page()

    def _sync_dashboard_dates_from_preset(self):
        key = self.range_combo.currentData() or "30d"
        today = QtCore.QDate.currentDate()
        if key == "7d":
            self.range_from_input.setDate(today.addDays(-6))
            self.range_to_input.setDate(today)
        elif key == "30d":
            self.range_from_input.setDate(today.addDays(-29))
            self.range_to_input.setDate(today)
        elif key == "90d":
            self.range_from_input.setDate(today.addDays(-89))
            self.range_to_input.setDate(today)
        elif key == "month":
            self.range_from_input.setDate(QtCore.QDate(today.year(), today.month(), 1))
            self.range_to_input.setDate(today)

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self._clear_layout(child_layout)

    @staticmethod
    def _get_time_slot_label(dt_value):
        hour = dt_value.hour
        if hour < 11:
            return "Sáng"
        if hour < 14:
            return "Trưa"
        if hour < 18:
            return "Chiều"
        return "Tối"

    @staticmethod
    def _categorize_prescription_item(medicine_name, medicine_description):
        payload = f"{medicine_name or ''} {medicine_description or ''}".lower()
        if any(keyword in payload for keyword in ["kháng sinh", "antibiotic"]):
            return "Kháng sinh"
        if any(keyword in payload for keyword in ["vitamin", "bổ sung"]):
            return "Vitamin"
        if any(keyword in payload for keyword in ["giảm đau", "hạ sốt"]):
            return "Giảm đau / hạ sốt"
        if any(keyword in payload for keyword in ["tiêu hóa", "dạ dày"]):
            return "Tiêu hóa"
        return "Khác"

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

    def _build_schedule_page(self):
        page = QtWidgets.QWidget()
        page_layout = QtWidgets.QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(12)

        # --- FILTER BAR ---
        filter_frame = QtWidgets.QFrame()
        filter_frame.setStyleSheet("background: white; border-radius: 10px; border: 1px solid #e2e8f0;")
        fl = QtWidgets.QHBoxLayout(filter_frame)
        fl.setContentsMargins(12, 8, 12, 8)
        fl.setSpacing(8)
        nav_s = ("QPushButton { background: white; border: 1px solid #e2e8f0; border-radius: 6px;"
                 " padding: 6px 10px; font-size: 13px; color: #334155; }"
                 " QPushButton:hover { background: #f8fafc; }")
        for txt, w in [("‹", 32), ("  23/05/2026  📅", 0), ("›", 32)]:
            b = QtWidgets.QPushButton(txt)
            if w: b.setFixedSize(w, 32)
            b.setStyleSheet(nav_s + (" QPushButton { font-weight: 600; }" if w == 0 else ""))
            b.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            fl.addWidget(b)
        fl.addSpacing(4)
        btn_today = QtWidgets.QPushButton("Hôm nay")
        btn_today.setStyleSheet(nav_s + " QPushButton { font-weight: 600; }")
        btn_today.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        fl.addWidget(btn_today)
        fl.addStretch()
        combo_s = ("QComboBox { background: white; border: 1px solid #e2e8f0; border-radius: 6px;"
                   " padding: 6px 12px; font-size: 13px; color: #334155; min-width: 130px; }"
                   " QComboBox::drop-down { border: none; width: 20px; }"
                   " QComboBox::down-arrow { image: none; border: none; }")
        for items in [["Tất cả trạng thái"], ["Tất cả dịch vụ"], ["Tất cả phòng khám"]]:
            cb = QtWidgets.QComboBox()
            cb.addItems(items)
            cb.setStyleSheet(combo_s)
            fl.addWidget(cb)
        btn_add = QtWidgets.QPushButton("  + Thêm lịch khám")
        btn_add.setStyleSheet("QPushButton { background: #16a34a; color: white; border: none; border-radius: 8px;"
                              " padding: 8px 16px; font-size: 13px; font-weight: 700; }"
                              " QPushButton:hover { background: #15803d; }")
        btn_add.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        fl.addWidget(btn_add)
        page_layout.addWidget(filter_frame)

        # --- MAIN CONTENT ---
        content_h = QtWidgets.QHBoxLayout()
        content_h.setSpacing(16)

        # ===== LEFT: TIMELINE =====
        left_card = QtWidgets.QFrame()
        left_card.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #e8ecf1;")
        left_vl = QtWidgets.QVBoxLayout(left_card)
        left_vl.setContentsMargins(20, 16, 20, 16)
        left_vl.setSpacing(8)
        t_lbl = QtWidgets.QLabel("Lịch khám trong ngày - Thứ Sáu, 23/05/2026")
        t_lbl.setStyleSheet("font-size: 16px; font-weight: 700; color: #1e293b; background: transparent; border: none;")
        left_vl.addWidget(t_lbl)
        # Legend
        leg = QtWidgets.QHBoxLayout()
        leg.setSpacing(16)
        for dot_c, txt in [("#16a34a","Đã khám"),("#3b82f6","Đang khám"),("#f59e0b","Đang chờ"),("#ef4444","Đã hủy"),("#94a3b8","Đã đặt lịch")]:
            hl = QtWidgets.QHBoxLayout(); hl.setSpacing(4)
            d = QtWidgets.QLabel("●"); d.setStyleSheet(f"color: {dot_c}; font-size: 10px; background: transparent; border: none;")
            tl = QtWidgets.QLabel(txt); tl.setStyleSheet("font-size: 12px; color: #64748b; background: transparent; border: none;")
            hl.addWidget(d); hl.addWidget(tl); leg.addLayout(hl)
        leg.addStretch()
        left_vl.addLayout(leg)
        # Timeline scroll
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        tw = QtWidgets.QWidget(); tw.setStyleSheet("background: transparent;")
        tl_layout = QtWidgets.QVBoxLayout(tw)
        tl_layout.setContentsMargins(0, 8, 0, 8)
        tl_layout.setSpacing(0)
        # Mock appointments: (hour_label, time_range, name, info, service, status_key, is_selected)
        appts = [
            ("07:00", "07:00 - 07:30", "Trần Văn Hùng", "Nam, 40 tuổi", "Khám tổng quát", "booked", False),
            ("08:00", "08:00 - 08:30", "Nguyễn Thị Lan", "Nữ, 32 tuổi", "Khám phụ khoa", "done", False),
            ("09:00", "09:00 - 09:30", "Lê Minh Tuấn", "Nam, 35 tuổi", "Tư vấn sức khỏe", "in_progress", True),
            ("10:00", "10:00 - 10:30", "Phạm Thị Mai", "Nữ, 28 tuổi", "Đau đầu, chóng mặt", "waiting", False),
            ("11:00", "10:30 - 11:00", "Hoàng Văn Nam", "Nam, 45 tuổi", "Khám tim mạch", "waiting", False),
            ("12:00", "11:00 - 11:30", "Vũ Thị Hương", "Nữ, 30 tuổi", "Khám thai định kỳ", "done", False),
            ("13:00", "13:30 - 14:00", "Đỗ Quốc Bảo", "Nam, 50 tuổi", "Khám cơ xương khớp", "booked", False),
            ("14:00", "14:00 - 14:30", "Trần Thị Thu", "Nữ, 26 tuổi", "Dị ứng, mẩn ngứa", "waiting", False),
            ("15:00", "15:00 - 15:30", "Nguyễn Văn Đạt", "Nam, 33 tuổi", "Khám da liễu", "cancelled", False),
            ("16:00", "16:00 - 16:30", "Lý Thị Nga", "Nữ, 29 tuổi", "Khám tổng quát", "booked", False),
            ("17:00", None, None, None, None, None, False),
        ]
        status_map = {
            "done": ("Đã khám", "#16a34a", "#f0fdf4", "  ✓"),
            "in_progress": ("Đang khám", "#3b82f6", "#eff6ff", "  🩺"),
            "waiting": ("Đang chờ", "#f59e0b", "#fffbeb", "  ✕"),
            "cancelled": ("Đã hủy", "#ef4444", "#fef2f2", "  ✕"),
            "booked": ("Đã đặt lịch", "#94a3b8", "#f8fafc", ""),
        }
        for hour, t_range, name, info, service, st_key, selected in appts:
            row = QtWidgets.QHBoxLayout()
            row.setSpacing(12)
            row.setContentsMargins(0, 0, 0, 0)
            h_lbl = QtWidgets.QLabel(hour)
            h_lbl.setFixedWidth(50)
            h_lbl.setStyleSheet("font-size: 13px; color: #94a3b8; font-weight: 600; background: transparent; border: none;")
            h_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
            row.addWidget(h_lbl)
            if t_range and st_key:
                st_text, st_color, st_bg, st_icon = status_map[st_key]
                border_color = st_color
                card_bg = "#eef6fc" if selected else "white"
                card = QtWidgets.QFrame()
                card.setStyleSheet(f"background: {card_bg}; border-left: 3px solid {border_color};"
                                   f" border-radius: 8px; border-top: 1px solid #f1f5f9;"
                                   f" border-right: 1px solid #f1f5f9; border-bottom: 1px solid #f1f5f9;")
                card.setFixedHeight(58)
                cl = QtWidgets.QHBoxLayout(card)
                cl.setContentsMargins(12, 8, 12, 8)
                cl.setSpacing(8)
                info_vl = QtWidgets.QVBoxLayout()
                info_vl.setSpacing(1)
                tr_lbl = QtWidgets.QLabel(t_range)
                tr_lbl.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {st_color}; background: transparent; border: none;")
                nm_lbl = QtWidgets.QLabel(f"<b>{name}</b> - {info}")
                nm_lbl.setStyleSheet("font-size: 13px; color: #334155; background: transparent; border: none;")
                sv_lbl = QtWidgets.QLabel(service)
                sv_lbl.setStyleSheet("font-size: 12px; color: #64748b; background: transparent; border: none;")
                info_vl.addWidget(tr_lbl); info_vl.addWidget(nm_lbl); info_vl.addWidget(sv_lbl)
                cl.addLayout(info_vl)
                cl.addStretch()
                badge = QtWidgets.QLabel(st_text)
                badge.setStyleSheet(f"background: {st_bg}; color: {st_color}; font-size: 11px; font-weight: 700;"
                                    f" padding: 3px 10px; border-radius: 10px; border: none;")
                badge.setFixedHeight(22)
                cl.addWidget(badge)
                if st_icon.strip():
                    ic = QtWidgets.QLabel(st_icon.strip())
                    ic.setStyleSheet(f"font-size: 14px; color: {st_color}; background: transparent; border: none;")
                    cl.addWidget(ic)
                row.addWidget(card)
            else:
                line = QtWidgets.QFrame()
                line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
                line.setStyleSheet("background: #f1f5f9; border: none; max-height: 1px;")
                row.addWidget(line)
            tl_layout.addLayout(row)
            sep = QtWidgets.QFrame()
            sep.setFixedHeight(1)
            sep.setStyleSheet("background: #f1f5f9; border: none; margin-left: 62px;")
            tl_layout.addWidget(sep)
            tl_layout.addSpacing(4)
        tl_layout.addStretch()
        scroll.setWidget(tw)
        left_vl.addWidget(scroll)
        content_h.addWidget(left_card, 65)

        # ===== RIGHT PANEL =====
        right_w = QtWidgets.QWidget()
        right_w.setStyleSheet("background: transparent;")
        rv = QtWidgets.QVBoxLayout(right_w)
        rv.setContentsMargins(0, 0, 0, 0)
        rv.setSpacing(12)
        # Calendar
        cal_card = QtWidgets.QFrame()
        cal_card.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #e8ecf1;")
        cal_vl = QtWidgets.QVBoxLayout(cal_card)
        cal_vl.setContentsMargins(16, 12, 16, 12)
        cal_vl.setSpacing(8)
        cal_header = QtWidgets.QHBoxLayout()
        cal_prev = QtWidgets.QPushButton("‹")
        cal_prev.setFixedSize(28, 28)
        cal_prev.setStyleSheet("QPushButton { background: transparent; border: none; font-size: 16px; color: #64748b; }")
        cal_title = QtWidgets.QLabel("Lịch tháng 5, 2026")
        cal_title.setStyleSheet("font-size: 14px; font-weight: 700; color: #1e293b; background: transparent; border: none;")
        cal_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        cal_next = QtWidgets.QPushButton("›")
        cal_next.setFixedSize(28, 28)
        cal_next.setStyleSheet("QPushButton { background: transparent; border: none; font-size: 16px; color: #64748b; }")
        cal_header.addWidget(cal_prev); cal_header.addStretch(); cal_header.addWidget(cal_title); cal_header.addStretch(); cal_header.addWidget(cal_next)
        cal_vl.addLayout(cal_header)
        # Day headers
        dh = QtWidgets.QHBoxLayout()
        for d in ["T2","T3","T4","T5","T6","T7","CN"]:
            dl = QtWidgets.QLabel(d)
            dl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            dl.setStyleSheet("font-size: 12px; font-weight: 600; color: #94a3b8; background: transparent; border: none;")
            dh.addWidget(dl)
        cal_vl.addLayout(dh)
        # Calendar grid (May 2026 starts on Friday)
        cal_days = [
            [28,29,30,1,2,3,4],[5,6,7,8,9,10,11],[12,13,14,15,16,17,18],
            [19,20,21,22,23,24,25],[26,27,28,29,30,31,1]
        ]
        for week in cal_days:
            wl = QtWidgets.QHBoxLayout()
            for i, day in enumerate(week):
                dl = QtWidgets.QLabel(str(day))
                dl.setFixedSize(32, 32)
                dl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                is_other = (week == cal_days[0] and day > 7) or (week == cal_days[-1] and day < 7)
                is_other = (week == cal_days[0] and day >= 28) or (week == cal_days[-1] and day <= 1)
                if day == 23 and week == cal_days[3]:
                    dl.setStyleSheet("background: #16a34a; color: white; border-radius: 16px; font-size: 13px; font-weight: 700; border: none;")
                elif is_other:
                    dl.setStyleSheet("color: #cbd5e1; font-size: 13px; background: transparent; border: none;")
                else:
                    dl.setStyleSheet("color: #334155; font-size: 13px; background: transparent; border: none;")
                wl.addWidget(dl)
            cal_vl.addLayout(wl)
        rv.addWidget(cal_card)

        # Detail card
        det_card = QtWidgets.QFrame()
        det_card.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #e8ecf1;")
        det_vl = QtWidgets.QVBoxLayout(det_card)
        det_vl.setContentsMargins(16, 16, 16, 16)
        det_vl.setSpacing(10)
        det_title = QtWidgets.QLabel("Thông tin lịch khám")
        det_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #1e293b; background: transparent; border: none;")
        det_vl.addWidget(det_title)
        # Patient info row
        pi = QtWidgets.QHBoxLayout(); pi.setSpacing(10)
        avt = QtWidgets.QLabel("👤")
        avt.setFixedSize(48, 48)
        avt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avt.setStyleSheet("background: #e0f2fe; color: #0284c7; border-radius: 24px; font-size: 22px;")
        pi.addWidget(avt)
        pi_info = QtWidgets.QVBoxLayout(); pi_info.setSpacing(2)
        nm_row = QtWidgets.QHBoxLayout(); nm_row.setSpacing(6)
        nm = QtWidgets.QLabel("Lê Minh Tuấn"); nm.setStyleSheet("font-size: 15px; font-weight: 700; color: #1e293b; background: transparent; border: none;")
        badge_g = QtWidgets.QLabel("Nam"); badge_g.setStyleSheet("background: #dcfce7; color: #16a34a; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 8px; border: none;")
        nm_row.addWidget(nm); nm_row.addWidget(badge_g); nm_row.addStretch()
        pi_info.addLayout(nm_row)
        sub = QtWidgets.QLabel("35 tuổi  ·  0987 654 321"); sub.setStyleSheet("font-size: 12px; color: #64748b; background: transparent; border: none;")
        pi_info.addWidget(sub)
        code = QtWidgets.QLabel("Mã BN: BN000123"); code.setStyleSheet("font-size: 12px; color: #94a3b8; background: transparent; border: none;")
        pi_info.addWidget(code)
        pi.addLayout(pi_info)
        det_vl.addLayout(pi)
        # Detail fields
        det_sep = QtWidgets.QFrame(); det_sep.setFixedHeight(1); det_sep.setStyleSheet("background: #f1f5f9; border: none;")
        det_vl.addWidget(det_sep)
        fields = [
            ("🕐  Thời gian", "09:00 - 09:30", False),
            ("🏥  Dịch vụ", "Tư vấn sức khỏe", False),
            ("📍  Phòng khám", "Phòng khám 1", False),
            ("📋  Trạng thái", "Đang khám", True),
            ("📝  Ghi chú", "Không có", False),
        ]
        for icon_txt, val, is_badge in fields:
            fr = QtWidgets.QHBoxLayout()
            fl_lbl = QtWidgets.QLabel(icon_txt)
            fl_lbl.setStyleSheet("font-size: 13px; color: #64748b; background: transparent; border: none;")
            fr.addWidget(fl_lbl)
            fr.addStretch()
            if is_badge:
                vl = QtWidgets.QLabel(val)
                vl.setStyleSheet("background: #dcfce7; color: #16a34a; font-size: 12px; font-weight: 700; padding: 2px 10px; border-radius: 8px; border: none;")
            else:
                vl = QtWidgets.QLabel(val)
                vl.setStyleSheet("font-size: 13px; color: #1e293b; font-weight: 600; background: transparent; border: none;")
            fr.addWidget(vl)
            det_vl.addLayout(fr)
        # Actions
        act_sep = QtWidgets.QFrame(); act_sep.setFixedHeight(1); act_sep.setStyleSheet("background: #f1f5f9; border: none;")
        det_vl.addWidget(act_sep)
        act_title = QtWidgets.QLabel("Hành động")
        act_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #1e293b; background: transparent; border: none;")
        det_vl.addWidget(act_title)
        actions = [
            ("🩺  Bắt đầu khám", "#16a34a", "white", "#16a34a"),
            ("👁  Xem hồ sơ bệnh nhân", "white", "#334155", "#e2e8f0"),
            ("✏  Chỉnh sửa lịch", "white", "#334155", "#e2e8f0"),
            ("🗑  Hủy lịch khám", "white", "#ef4444", "#fecaca"),
        ]
        for txt, bg, fg, bd in actions:
            ab = QtWidgets.QPushButton(txt)
            ab.setStyleSheet(f"QPushButton {{ background: {bg}; color: {fg}; border: 1px solid {bd};"
                             f" border-radius: 8px; padding: 9px 16px; font-size: 13px; font-weight: 600; }}"
                             f" QPushButton:hover {{ opacity: 0.9; }}")
            ab.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            det_vl.addWidget(ab)
        rv.addWidget(det_card)
        rv.addStretch()
        content_h.addWidget(right_w, 35)
        page_layout.addLayout(content_h)
        return page

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

    def _build_doctor_notification_mock_data(self):
        return [
            {
                "title": "Lịch hẹn mới",
                "message": "Bạn có lịch hẹn khám mới với bệnh nhân Lê Văn Nam vào 24/05/2026 10:00.",
                "time": "10:30",
                "date": "23/05/2026 10:30",
                "category": "Lịch hẹn",
                "status": "Chưa đọc",
                "icon": "📅",
                "icon_bg": "#e8f8ee",
                "icon_color": "#18b66d",
                "highlight": True,
                "details": [
                    ("Bệnh nhân:", "Lê Văn Nam"),
                    ("Ngày khám:", "24/05/2026"),
                    ("Giờ khám:", "10:00"),
                    ("Dịch vụ:", "Khám tổng quát"),
                    ("Phòng khám:", "Phòng khám 1"),
                    ("Ghi chú:", "Khám định kỳ"),
                ],
                "footer": "Vui lòng chuẩn bị để tiếp đón bệnh nhân.",
            },
            {
                "title": "Kết quả xét nghiệm mới",
                "message": "Kết quả xét nghiệm máu của bệnh nhân Trần Thị Mai đã có.",
                "time": "09:15",
                "date": "23/05/2026 09:15",
                "category": "Kết quả",
                "status": "Chưa đọc",
                "icon": "🧪",
                "icon_bg": "#edf4ff",
                "icon_color": "#2f80ff",
                "highlight": False,
            },
            {
                "title": "Bệnh nhân đến khám",
                "message": "Bệnh nhân Nguyễn Hoàng Anh (09:00) đã đến phòng khám.",
                "time": "09:05",
                "date": "23/05/2026 09:05",
                "category": "Lịch hẹn",
                "status": "Chưa đọc",
                "icon": "📋",
                "icon_bg": "#fff4e8",
                "icon_color": "#ff9f1a",
                "highlight": False,
            },
            {
                "title": "Đơn thuốc chờ duyệt",
                "message": "Bạn có 2 đơn thuốc mới cần duyệt.",
                "time": "08:45",
                "date": "23/05/2026 08:45",
                "category": "Khác",
                "status": "Chưa đọc",
                "icon": "💊",
                "icon_bg": "#f3ebff",
                "icon_color": "#8b5cf6",
                "highlight": False,
            },
            {
                "title": "Cập nhật hệ thống",
                "message": "Phiên bản CarePlus 1.2.1 đã được cập nhật. Vui lòng khởi động lại ứng dụng.",
                "time": "Hôm qua",
                "date": "22/05/2026 17:20",
                "category": "Hệ thống",
                "status": "Đã đọc",
                "icon": "🔔",
                "icon_bg": "#ebf8ef",
                "icon_color": "#18b66d",
                "highlight": False,
            },
            {
                "title": "Nhắc lịch tái khám",
                "message": "3 bệnh nhân có lịch tái khám trong ngày hôm nay.",
                "time": "Hôm qua",
                "date": "22/05/2026 11:40",
                "category": "Lịch hẹn",
                "status": "Đã đọc",
                "icon": "⚠️",
                "icon_bg": "#fff0f0",
                "icon_color": "#ff4d4f",
                "highlight": False,
            },
            {
                "title": "Bệnh nhân mới",
                "message": "Bệnh nhân Phạm Thị Lan vừa được đăng ký hồ sơ.",
                "time": "21/05/2026",
                "date": "21/05/2026 15:10",
                "category": "Khác",
                "status": "Đã đọc",
                "icon": "👤",
                "icon_bg": "#eef5ff",
                "icon_color": "#2f80ff",
                "highlight": False,
            },
            {
                "title": "Hồ sơ bệnh nhân cập nhật",
                "message": "Hồ sơ bệnh án của bệnh nhân Vũ Thị Hương đã được cập nhật.",
                "time": "21/05/2026",
                "date": "21/05/2026 10:05",
                "category": "Kết quả",
                "status": "Đã đọc",
                "icon": "📄",
                "icon_bg": "#fff4e8",
                "icon_color": "#ff9f1a",
                "highlight": False,
            },
            {
                "title": "Sao lưu dữ liệu thành công",
                "message": "Dữ liệu đã được sao lưu tự động lúc 02:00 AM.",
                "time": "20/05/2026",
                "date": "20/05/2026 02:00",
                "category": "Hệ thống",
                "status": "Đã đọc",
                "icon": "🛡️",
                "icon_bg": "#edf9f0",
                "icon_color": "#18b66d",
                "highlight": False,
            },
            {
                "title": "Thông báo từ phòng khám",
                "message": "Phòng khám sẽ nghỉ vào Chủ nhật ngày 25/05/2026.",
                "time": "20/05/2026",
                "date": "20/05/2026 08:30",
                "category": "Khác",
                "status": "Đã đọc",
                "icon": "📣",
                "icon_bg": "#f3ebff",
                "icon_color": "#8b5cf6",
                "highlight": False,
            },
        ]

    def _build_doctor_notification_tab(self, text, is_active=False):
        btn = QtWidgets.QPushButton(text)
        btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        btn.setFixedHeight(42)
        if is_active:
            btn.setStyleSheet(
                "QPushButton { background: #e8f8ee; color: #18b66d; border: 1px solid #d6f2e1; "
                "border-radius: 12px; padding-left: 18px; padding-right: 18px; font-size: 13px; font-weight: 800; }"
            )
        else:
            btn.setStyleSheet(
                "QPushButton { background: white; color: #334155; border: 1px solid #e8edf3; "
                "border-radius: 12px; padding-left: 18px; padding-right: 18px; font-size: 13px; font-weight: 700; }"
            )
        return btn

    def _build_doctor_notification_action_button(self, text, icon_text, is_danger=False):
        btn = QtWidgets.QPushButton(f"{icon_text}  {text}")
        btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        btn.setMinimumHeight(44)
        border = "#ffd4d4" if is_danger else "#e8edf3"
        color = "#ff4d4f" if is_danger else "#475569"
        btn.setStyleSheet(
            f"QPushButton {{ background: white; color: {color}; border: 1px solid {border}; "
            "border-radius: 12px; padding-left: 18px; padding-right: 18px; font-size: 13px; font-weight: 700; text-align: center; }}"
        )
        return btn

    def _build_doctor_notification_list_item(self, item):
        card = QtWidgets.QFrame()
        background = "#f1fbf4" if item.get("highlight") else "#ffffff"
        card.setStyleSheet(
            f"background: {background}; border: 1px solid #edf2f7; border-radius: 18px;"
        )
        card.setMinimumHeight(96)
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(14)

        icon_wrap = QtWidgets.QLabel(str(item.get("icon") or "🔔"))
        icon_wrap.setFixedSize(52, 52)
        icon_wrap.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        icon_wrap.setStyleSheet(
            f"background: {item.get('icon_bg', '#eef2ff')}; color: {item.get('icon_color', '#334155')}; "
            "border-radius: 26px; font-size: 22px; border: none;"
        )
        layout.addWidget(icon_wrap)

        text_col = QtWidgets.QVBoxLayout()
        text_col.setSpacing(6)
        title = QtWidgets.QLabel(str(item.get("title") or "Thông báo"))
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #0f172a; border: none;")
        message = QtWidgets.QLabel(str(item.get("message") or ""))
        message.setWordWrap(True)
        message.setStyleSheet("font-size: 13px; color: #475569; border: none;")
        text_col.addWidget(title)
        text_col.addWidget(message)
        layout.addLayout(text_col, 1)

        right_col = QtWidgets.QVBoxLayout()
        right_col.setSpacing(10)
        right_col.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)
        time_label = QtWidgets.QLabel(str(item.get("time") or ""))
        time_label.setStyleSheet("font-size: 15px; color: #475569; font-weight: 700; border: none;")
        right_col.addWidget(time_label, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        status_dot = QtWidgets.QLabel("●")
        dot_color = "#2f80ff" if item.get("status") == "Chưa đọc" else "#94a3b8"
        status_dot.setStyleSheet(f"font-size: 14px; color: {dot_color}; border: none;")
        right_col.addWidget(status_dot, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addLayout(right_col)
        return card

    def _build_notification_center_page(self, notifications):
        items = self._build_doctor_notification_mock_data()
        selected = items[0]
        page = QtWidgets.QWidget()
        page.setStyleSheet("background: transparent;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        header = QtWidgets.QHBoxLayout()
        header.setSpacing(16)
        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(6)
        title = QtWidgets.QLabel("Thông báo")
        title.setStyleSheet("font-size: 28px; font-weight: 900; color: #0f172a; border: none;")
        breadcrumb = QtWidgets.QLabel("Trang chủ   ›   Thông báo")
        breadcrumb.setStyleSheet("font-size: 14px; color: #64748b; font-weight: 700; border: none;")
        title_col.addWidget(title)
        title_col.addWidget(breadcrumb)
        header.addLayout(title_col)
        header.addStretch()

        bell_wrap = QtWidgets.QFrame()
        bell_wrap.setFixedSize(40, 40)
        bell_wrap.setStyleSheet("background: transparent; border: none;")
        bell_grid = QtWidgets.QGridLayout(bell_wrap)
        bell_grid.setContentsMargins(0, 0, 0, 0)
        bell_icon = QtWidgets.QLabel("🔔")
        bell_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        bell_icon.setStyleSheet("font-size: 20px; color: #94a3b8; border: none;")
        bell_grid.addWidget(bell_icon, 0, 0)
        bell_badge = QtWidgets.QLabel("2")
        bell_badge.setFixedSize(18, 18)
        bell_badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        bell_badge.setStyleSheet(
            "background: #ff2d2f; color: white; border-radius: 9px; font-size: 10px; font-weight: 800; border: none;"
        )
        bell_grid.addWidget(
            bell_badge,
            0,
            0,
            QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight,
        )
        header.addWidget(bell_wrap)

        avatar = QtWidgets.QLabel("👨‍⚕️")
        avatar.setFixedSize(44, 44)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("background: #eef2f7; border-radius: 22px; font-size: 24px; border: none;")
        header.addWidget(avatar)

        doctor_name = str(self.user_data.get("name") or "Minh").strip() or "Minh"
        profile_label = QtWidgets.QLabel(f"Bác sĩ {doctor_name}")
        profile_label.setStyleSheet("font-size: 14px; color: #0f172a; font-weight: 800; border: none;")
        header.addWidget(profile_label)

        caret = QtWidgets.QLabel("⌄")
        caret.setStyleSheet("font-size: 16px; color: #94a3b8; font-weight: 700; border: none;")
        header.addWidget(caret)
        layout.addLayout(header)

        tabs = QtWidgets.QHBoxLayout()
        tabs.setSpacing(12)
        for index, text in enumerate(
            ["Tất cả (24)", "Chưa đọc (2)", "Lịch hẹn (6)", "Kết quả (7)", "Hệ thống (5)", "Khác (4)"]
        ):
            tabs.addWidget(self._build_doctor_notification_tab(text, index == 0))
        tabs.addStretch()
        layout.addLayout(tabs)

        content = QtWidgets.QHBoxLayout()
        content.setSpacing(16)

        left_card = QtWidgets.QFrame()
        left_card.setStyleSheet("background: white; border: 1px solid #edf2f7; border-radius: 20px;")
        left_layout = QtWidgets.QVBoxLayout(left_card)
        left_layout.setContentsMargins(18, 18, 18, 18)
        left_layout.setSpacing(16)

        left_header = QtWidgets.QHBoxLayout()
        left_header.setSpacing(12)
        left_title = QtWidgets.QLabel("Danh sách thông báo")
        left_title.setStyleSheet("font-size: 18px; font-weight: 900; color: #0f172a; border: none;")
        left_header.addWidget(left_title)
        left_header.addStretch()

        search_box = QtWidgets.QFrame()
        search_box.setFixedWidth(240)
        search_box.setStyleSheet("background: white; border: 1px solid #e8edf3; border-radius: 12px;")
        search_layout = QtWidgets.QHBoxLayout(search_box)
        search_layout.setContentsMargins(14, 0, 14, 0)
        search_layout.setSpacing(8)
        search_icon = QtWidgets.QLabel("⌕")
        search_icon.setStyleSheet("font-size: 18px; color: #94a3b8; border: none;")
        search_text = QtWidgets.QLabel("Tìm kiếm thông báo...")
        search_text.setStyleSheet("font-size: 13px; color: #94a3b8; border: none;")
        search_layout.addWidget(search_icon)
        search_layout.addWidget(search_text)
        left_header.addWidget(search_box)
        left_header.addWidget(self._build_doctor_notification_action_button("Đánh dấu tất cả đã đọc", "✓"))
        left_header.addWidget(self._build_doctor_notification_action_button("Cài đặt thông báo", "⚙"))
        left_layout.addLayout(left_header)

        for item in items:
            left_layout.addWidget(self._build_doctor_notification_list_item(item))

        pagination = QtWidgets.QHBoxLayout()
        pagination.setSpacing(8)
        display_label = QtWidgets.QLabel("Hiển thị")
        display_label.setStyleSheet("font-size: 13px; color: #475569; font-weight: 700; border: none;")
        pagination.addWidget(display_label)

        page_size = QtWidgets.QFrame()
        page_size.setFixedSize(64, 38)
        page_size.setStyleSheet("background: white; border: 1px solid #e8edf3; border-radius: 10px;")
        page_size_layout = QtWidgets.QHBoxLayout(page_size)
        page_size_layout.setContentsMargins(12, 0, 12, 0)
        page_size_layout.setSpacing(6)
        page_size_value = QtWidgets.QLabel("10")
        page_size_value.setStyleSheet("font-size: 13px; color: #334155; font-weight: 700; border: none;")
        page_size_layout.addWidget(page_size_value)
        arrow_label = QtWidgets.QLabel("⌄")
        arrow_label.setStyleSheet("font-size: 13px; color: #64748b; border: none;")
        page_size_layout.addWidget(arrow_label)
        pagination.addWidget(page_size)

        records_label = QtWidgets.QLabel("bản ghi")
        records_label.setStyleSheet("font-size: 13px; color: #475569; font-weight: 700; border: none;")
        pagination.addWidget(records_label)
        pagination.addStretch()

        for text, active in [("‹", False), ("1", True), ("2", False), ("3", False), ("›", False)]:
            btn = QtWidgets.QPushButton(text)
            btn.setFixedSize(38, 38)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            if active:
                btn.setStyleSheet(
                    "QPushButton { background: #18b66d; color: white; border: none; border-radius: 10px; font-size: 14px; font-weight: 800; }"
                )
            else:
                btn.setStyleSheet(
                    "QPushButton { background: white; color: #64748b; border: 1px solid #e8edf3; border-radius: 10px; font-size: 14px; font-weight: 700; }"
                )
            pagination.addWidget(btn)
        left_layout.addLayout(pagination)

        content.addWidget(left_card, 66)

        right_card = QtWidgets.QFrame()
        right_card.setStyleSheet("background: white; border: 1px solid #edf2f7; border-radius: 20px;")
        right_layout = QtWidgets.QVBoxLayout(right_card)
        right_layout.setContentsMargins(22, 18, 22, 18)
        right_layout.setSpacing(16)

        detail_title = QtWidgets.QLabel("Chi tiết thông báo")
        detail_title.setStyleSheet("font-size: 18px; font-weight: 900; color: #0f172a; border: none;")
        right_layout.addWidget(detail_title)

        summary_row = QtWidgets.QHBoxLayout()
        summary_row.setSpacing(14)
        detail_icon = QtWidgets.QLabel(str(selected.get("icon") or "📅"))
        detail_icon.setFixedSize(84, 84)
        detail_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        detail_icon.setStyleSheet(
            f"background: {selected.get('icon_bg', '#e8f8ee')}; color: {selected.get('icon_color', '#18b66d')}; "
            "border-radius: 42px; font-size: 34px; border: none;"
        )
        summary_row.addWidget(detail_icon)

        summary_text = QtWidgets.QVBoxLayout()
        summary_text.setSpacing(8)
        detail_name = QtWidgets.QLabel(str(selected.get("title") or "Thông báo"))
        detail_name.setStyleSheet("font-size: 18px; font-weight: 900; color: #0f172a; border: none;")
        category = QtWidgets.QLabel(str(selected.get("category") or "Khác"))
        category.setStyleSheet(
            "background: #e8f8ee; color: #18b66d; border-radius: 10px; font-size: 12px; font-weight: 800; padding: 4px 10px;"
        )
        summary_text.addWidget(detail_name)
        summary_text.addWidget(category, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        summary_row.addLayout(summary_text, 1)
        right_layout.addLayout(summary_row)

        meta_row = QtWidgets.QHBoxLayout()
        meta_row.setSpacing(10)
        meta_date = QtWidgets.QLabel(f"🕒  {selected.get('date')}")
        meta_date.setStyleSheet("font-size: 13px; color: #64748b; font-weight: 700; border: none;")
        meta_row.addWidget(meta_date)
        meta_row.addStretch()
        meta_dot = QtWidgets.QLabel("●")
        meta_dot.setStyleSheet("font-size: 14px; color: #2f80ff; border: none;")
        meta_status = QtWidgets.QLabel(str(selected.get("status") or "Chưa đọc"))
        meta_status.setStyleSheet("font-size: 13px; color: #64748b; font-weight: 700; border: none;")
        meta_row.addWidget(meta_dot)
        meta_row.addWidget(meta_status)
        right_layout.addLayout(meta_row)

        detail_message = QtWidgets.QLabel("Bạn có lịch hẹn khám mới với thông tin chi tiết như sau:")
        detail_message.setWordWrap(True)
        detail_message.setStyleSheet("font-size: 13px; color: #475569; font-weight: 700; border: none;")
        right_layout.addWidget(detail_message)

        detail_grid = QtWidgets.QGridLayout()
        detail_grid.setHorizontalSpacing(12)
        detail_grid.setVerticalSpacing(10)
        for row, (label_text, value_text) in enumerate(selected.get("details", [])):
            field_label = QtWidgets.QLabel(label_text)
            field_label.setStyleSheet("font-size: 13px; color: #64748b; font-weight: 700; border: none;")
            field_value = QtWidgets.QLabel(value_text)
            field_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
            field_value.setStyleSheet("font-size: 13px; color: #475569; font-weight: 800; border: none;")
            detail_grid.addWidget(field_label, row, 0)
            detail_grid.addWidget(field_value, row, 1)
        right_layout.addLayout(detail_grid)

        footer = QtWidgets.QLabel(str(selected.get("footer") or ""))
        footer.setWordWrap(True)
        footer.setStyleSheet("font-size: 13px; color: #475569; font-weight: 700; border: none; padding-top: 10px;")
        right_layout.addWidget(footer)
        right_layout.addStretch()

        primary_btn = QtWidgets.QPushButton("👜  Xem lịch hẹn")
        primary_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        primary_btn.setMinimumHeight(46)
        primary_btn.setStyleSheet(
            "QPushButton { background: #18b66d; color: white; border: none; border-radius: 12px; font-size: 14px; font-weight: 800; }"
        )
        right_layout.addWidget(primary_btn)

        secondary_btn = QtWidgets.QPushButton("📄  Xem hồ sơ bệnh nhân")
        secondary_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        secondary_btn.setMinimumHeight(46)
        secondary_btn.setStyleSheet(
            "QPushButton { background: white; color: #475569; border: 1px solid #e8edf3; border-radius: 12px; font-size: 14px; font-weight: 800; }"
        )
        right_layout.addWidget(secondary_btn)

        delete_btn = QtWidgets.QPushButton("🗑  Xóa thông báo")
        delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        delete_btn.setMinimumHeight(46)
        delete_btn.setStyleSheet(
            "QPushButton { background: white; color: #ff4d4f; border: 1px solid #ffd4d4; border-radius: 12px; font-size: 14px; font-weight: 800; }"
        )
        right_layout.addWidget(delete_btn)

        content.addWidget(right_card, 34)
        layout.addLayout(content)
        return page

    def _build_settings_page(self):
        page = QtWidgets.QWidget()
        page_layout = QtWidgets.QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0)

        header_widget = QtWidgets.QWidget()
        header_layout = QtWidgets.QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 18)
        header_layout.setSpacing(6)

        title = QtWidgets.QLabel("Cài đặt")
        title.setStyleSheet("font-size: 26px; font-weight: 900; color: #0f172a; border: none;")
        header_layout.addWidget(title)

        breadcrumb = QtWidgets.QLabel("Trang chủ   ›   Cài đặt")
        breadcrumb.setStyleSheet("font-size: 13px; color: #64748b; font-weight: 600; border: none;")
        header_layout.addWidget(breadcrumb)
        page_layout.addWidget(header_widget)

        content_wrapper = QtWidgets.QHBoxLayout()
        content_wrapper.setSpacing(18)

        left_nav = QtWidgets.QFrame()
        left_nav.setFixedWidth(288)
        left_nav.setStyleSheet("background: white; border-radius: 18px; border: 1px solid #e8eef5;")
        left_nav_layout = QtWidgets.QVBoxLayout(left_nav)
        left_nav_layout.setContentsMargins(14, 16, 14, 16)
        left_nav_layout.setSpacing(8)

        settings_menu_items = [
            ("profile", "👤", "Thông tin cá nhân", True),
            ("security", "🛡️", "Tài khoản & bảo mật", False),
            ("notification", "🔔", "Thông báo", False),
            ("schedule", "🗓️", "Lịch làm việc", False),
            ("prescription_templates", "℞", "Mẫu đơn thuốc", False),
            ("conclusion_templates", "📄", "Mẫu kết luận", False),
            ("signature", "✎", "Quản lý chữ ký", False),
            ("backup_restore", "☁️", "Sao lưu & khôi phục", False),
            ("language", "🌐", "Ngôn ngữ", False),
            ("display", "🎨", "Giao diện", False),
            ("intro", "ⓘ", "Giới thiệu", False),
        ]

        self._settings_nav_buttons = []
        for key, icon, text, is_active in settings_menu_items:
            btn = QtWidgets.QPushButton(f"  {icon}   {text}")
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setFixedHeight(48)
            btn.setStyleSheet(self._settings_nav_style(is_active))
            btn.clicked.connect(lambda _, selected_key=key: self._handle_settings_nav_action(selected_key))
            self._settings_nav_buttons.append((key, btn))
            left_nav_layout.addWidget(btn)

        left_nav_layout.addStretch()
        content_wrapper.addWidget(left_nav)

        right_scroll = QtWidgets.QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        right_scroll.setStyleSheet("background: transparent; border: none;")
        self._settings_scroll = right_scroll

        right_content = QtWidgets.QWidget()
        right_content.setStyleSheet("background: transparent;")
        right_layout = QtWidgets.QVBoxLayout(right_content)
        right_layout.setContentsMargins(0, 0, 8, 20)
        right_layout.setSpacing(18)

        card_style = "background: white; border-radius: 18px; border: 1px solid #e8eef5;"
        section_title_style = "font-size: 16px; font-weight: 900; color: #0f172a; border: none;"
        label_style = "font-size: 12px; color: #64748b; font-weight: 700; border: none;"
        input_style = (
            "QLineEdit, QComboBox, QDateEdit { background: white; border: 1px solid #dbe4ee; "
            "border-radius: 10px; padding: 10px; padding-left: 14px; padding-right: 14px; min-height: 22px; font-size: 13px; color: #334155; }"
            "QLineEdit:focus, QComboBox:focus, QDateEdit:focus { border-color: #10b981; }"
        )
        small_input_style = (
            "QComboBox { background: white; border: 1px solid #dbe4ee; border-radius: 8px; "
            "padding: 8px; padding-left: 12px; padding-right: 12px; min-height: 20px; font-size: 13px; color: #334155; }"
            "QComboBox:focus { border-color: #10b981; }"
        )

        def build_field(label_text, widget):
            field_widget = QtWidgets.QWidget()
            field_layout = QtWidgets.QVBoxLayout(field_widget)
            field_layout.setContentsMargins(0, 0, 0, 0)
            field_layout.setSpacing(6)
            label = QtWidgets.QLabel(label_text)
            label.setStyleSheet(label_style)
            field_layout.addWidget(label)
            field_layout.addWidget(widget)
            return field_widget

        personal_card = QtWidgets.QFrame()
        personal_card.setStyleSheet(card_style)
        self._settings_section_frames["profile"] = personal_card
        personal_layout = QtWidgets.QVBoxLayout(personal_card)
        personal_layout.setContentsMargins(24, 22, 24, 22)
        personal_layout.setSpacing(18)

        top_bar = QtWidgets.QHBoxLayout()
        section_title_1 = QtWidgets.QLabel("Thông tin cá nhân")
        section_title_1.setStyleSheet(section_title_style)
        top_bar.addWidget(section_title_1)
        top_bar.addStretch()
        btn_save = QtWidgets.QPushButton("🗂  Lưu thay đổi")
        btn_save.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        btn_save.setFixedHeight(42)
        btn_save.setStyleSheet(
            "QPushButton { background: #16a34a; color: white; border-radius: 10px; padding-left: 18px; padding-right: 18px; "
            "font-size: 13px; font-weight: 800; border: none; }"
            "QPushButton:hover { background: #15803d; }"
        )
        btn_save.clicked.connect(self._save_settings_personal_info)
        top_bar.addWidget(btn_save)
        personal_layout.addLayout(top_bar)

        avatar_form_layout = QtWidgets.QHBoxLayout()
        avatar_form_layout.setSpacing(20)

        avatar_panel = QtWidgets.QWidget()
        avatar_panel.setFixedWidth(136)
        avatar_grid = QtWidgets.QGridLayout(avatar_panel)
        avatar_grid.setContentsMargins(0, 8, 0, 0)
        avatar_grid.setHorizontalSpacing(0)
        avatar_grid.setVerticalSpacing(0)

        avatar_frame = QtWidgets.QFrame()
        avatar_frame.setFixedSize(108, 108)
        avatar_frame.setStyleSheet("background: #f1f5f9; border-radius: 54px; border: 1px solid #e2e8f0;")
        avatar_inner_layout = QtWidgets.QVBoxLayout(avatar_frame)
        avatar_inner_layout.setContentsMargins(0, 0, 0, 0)
        avatar_inner_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar_icon = QtWidgets.QLabel("👨‍⚕️")
        avatar_icon.setStyleSheet("font-size: 54px; background: transparent; border: none;")
        avatar_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar_inner_layout.addWidget(avatar_icon)
        self._settings_avatar_icon = avatar_icon
        avatar_grid.addWidget(avatar_frame, 0, 0, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        btn_camera = QtWidgets.QPushButton("📷")
        btn_camera.setFixedSize(30, 30)
        btn_camera.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        btn_camera.setStyleSheet(
            "QPushButton { background: white; border: 1px solid #dbe4ee; border-radius: 15px; font-size: 13px; }"
            "QPushButton:hover { background: #f1f5f9; }"
        )
        btn_camera.clicked.connect(self._upload_settings_avatar)
        avatar_grid.addWidget(
            btn_camera,
            0,
            0,
            alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignBottom,
        )
        avatar_form_layout.addWidget(avatar_panel, 0, QtCore.Qt.AlignmentFlag.AlignTop)

        doctor_name = str(self.user_data.get("name", "Bác sĩ Minh"))
        doctor_phone = str(self.user_data.get("phone", "0988 111 222"))
        doctor_email = str(self.user_data.get("email", "bs.minh@careplus.vn"))
        doctor_specialty = str(self.user_data.get("specialty", "Nội tổng quát"))
        if doctor_name.lower().startswith("bác sĩ "):
            doctor_name = doctor_name[7:].strip()

        form_grid = QtWidgets.QGridLayout()
        form_grid.setHorizontalSpacing(18)
        form_grid.setVerticalSpacing(12)
        form_grid.setColumnStretch(0, 3)
        form_grid.setColumnStretch(1, 3)
        form_grid.setColumnStretch(2, 3)

        self._settings_name_input = QtWidgets.QLineEdit(f"Bác sĩ {doctor_name}" if doctor_name else "Bác sĩ Minh")
        self._settings_name_input.setStyleSheet(input_style)
        form_grid.addWidget(build_field("Họ và tên", self._settings_name_input), 0, 0)

        self._settings_email_input = QtWidgets.QLineEdit(doctor_email)
        self._settings_email_input.setStyleSheet(input_style)
        form_grid.addWidget(build_field("Email", self._settings_email_input), 0, 1)

        self._settings_gender_combo = QtWidgets.QComboBox()
        self._settings_gender_combo.addItems(["Nam", "Nữ"])
        self._settings_gender_combo.setStyleSheet(input_style)
        form_grid.addWidget(build_field("Giới tính", self._settings_gender_combo), 0, 2)

        self._settings_dob_input = QtWidgets.QDateEdit()
        self._settings_dob_input.setCalendarPopup(True)
        self._settings_dob_input.setDisplayFormat("dd/MM/yyyy")
        self._settings_dob_input.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self._settings_dob_input.setSpecialValueText("Chưa cập nhật")
        self._settings_dob_input.setDate(QtCore.QDate(1985, 4, 15))
        self._settings_dob_input.setStyleSheet(input_style)
        form_grid.addWidget(build_field("Ngày sinh", self._settings_dob_input), 1, 1)

        self._settings_phone_input = QtWidgets.QLineEdit(doctor_phone)
        self._settings_phone_input.setStyleSheet(input_style)
        form_grid.addWidget(build_field("Số điện thoại", self._settings_phone_input), 1, 0)

        self._settings_specialty_combo = QtWidgets.QComboBox()
        specialties = [
            "Nội tổng quát", "Ngoại khoa", "Nhi khoa", "Sản khoa",
            "Da liễu", "Tim mạch", "Thần kinh", "Mắt"
        ]
        self._settings_specialty_combo.addItems(specialties)
        idx = self._settings_specialty_combo.findText(doctor_specialty)
        if idx >= 0:
            self._settings_specialty_combo.setCurrentIndex(idx)
        self._settings_specialty_combo.setStyleSheet(input_style)
        form_grid.addWidget(build_field("Chuyên khoa", self._settings_specialty_combo), 2, 0)

        self._settings_license_input = QtWidgets.QLineEdit("001234/HCM-CCHN")
        self._settings_license_input.setStyleSheet(input_style)
        form_grid.addWidget(build_field("Số chứng chỉ hành nghề", self._settings_license_input), 2, 1)

        self._settings_address_input = QtWidgets.QLineEdit("123 Đường Lê Lợi, P.1, Q.1, TP.HCM")
        self._settings_address_input.setStyleSheet(input_style)
        form_grid.addWidget(build_field("Địa chỉ phòng khám", self._settings_address_input), 2, 2)

        avatar_form_layout.addLayout(form_grid)
        personal_layout.addLayout(avatar_form_layout)
        right_layout.addWidget(personal_card)

        middle_row = QtWidgets.QHBoxLayout()
        middle_row.setSpacing(18)

        security_card = QtWidgets.QFrame()
        security_card.setStyleSheet(card_style)
        self._settings_section_frames["security"] = security_card
        security_layout = QtWidgets.QVBoxLayout(security_card)
        security_layout.setContentsMargins(24, 22, 24, 22)
        security_layout.setSpacing(16)

        section_title_security = QtWidgets.QLabel("Tài khoản & bảo mật")
        section_title_security.setStyleSheet(section_title_style)
        security_layout.addWidget(section_title_security)

        self._settings_username_input = QtWidgets.QLineEdit("bsminh")
        self._settings_username_input.setStyleSheet(input_style)
        security_layout.addWidget(build_field("Tên đăng nhập", self._settings_username_input))

        password_row = QtWidgets.QHBoxLayout()
        password_row.setSpacing(12)
        self._settings_password_input = QtWidgets.QLineEdit("12345678")
        self._settings_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self._settings_password_input.setStyleSheet(input_style)
        password_row.addWidget(build_field("Mật khẩu", self._settings_password_input), 1)

        password_btn_box = QtWidgets.QWidget()
        password_btn_layout = QtWidgets.QVBoxLayout(password_btn_box)
        password_btn_layout.setContentsMargins(0, 22, 0, 0)
        password_btn_layout.setSpacing(0)
        change_password_btn = QtWidgets.QPushButton("Đổi mật khẩu")
        change_password_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        change_password_btn.setFixedHeight(40)
        change_password_btn.setStyleSheet(
            "QPushButton { background: white; border: 1px solid #dbe4ee; border-radius: 10px; "
            "padding-left: 18px; padding-right: 18px; font-size: 13px; color: #334155; font-weight: 700; }"
            "QPushButton:hover { background: #f8fafc; }"
        )
        change_password_btn.clicked.connect(self._open_change_password_dialog)
        password_btn_layout.addWidget(change_password_btn)
        password_btn_layout.addStretch()
        password_row.addWidget(password_btn_box)
        security_layout.addLayout(password_row)

        two_factor_row = QtWidgets.QHBoxLayout()
        two_factor_row.setSpacing(12)
        two_factor_text = QtWidgets.QVBoxLayout()
        two_factor_text.setSpacing(2)
        two_factor_title = QtWidgets.QLabel("Xác thực 2 lớp")
        two_factor_title.setStyleSheet("font-size: 14px; font-weight: 800; color: #0f172a; border: none;")
        two_factor_desc = QtWidgets.QLabel("Tăng cường bảo mật cho tài khoản của bạn")
        two_factor_desc.setStyleSheet("font-size: 12px; color: #64748b; border: none;")
        two_factor_text.addWidget(two_factor_title)
        two_factor_text.addWidget(two_factor_desc)
        two_factor_row.addLayout(two_factor_text)
        two_factor_row.addStretch()
        self._settings_two_factor_toggle = QtWidgets.QCheckBox()
        self._settings_two_factor_toggle.setChecked(True)
        self._settings_two_factor_toggle.setStyleSheet(self._doctor_settings_switch_style())
        two_factor_row.addWidget(self._settings_two_factor_toggle)
        security_layout.addLayout(two_factor_row)
        middle_row.addWidget(security_card, 7)

        notification_card = QtWidgets.QFrame()
        notification_card.setStyleSheet(card_style)
        self._settings_section_frames["notification"] = notification_card
        notif_layout = QtWidgets.QVBoxLayout(notification_card)
        notif_layout.setContentsMargins(24, 22, 24, 22)
        notif_layout.setSpacing(14)

        section_title_2 = QtWidgets.QLabel("Thông báo")
        section_title_2.setStyleSheet(section_title_style)
        notif_layout.addWidget(section_title_2)

        notification_items = [
            ("notify_new_appointment", "📅", "#e9f8ef", "#16a34a", "Thông báo lịch hẹn mới", "Nhận thông báo khi có lịch hẹn mới", True, True),
            ("notify_reminder", "🧪", "#eaf1ff", "#2563eb", "Thông báo kết quả xét nghiệm", "Nhận thông báo khi có kết quả xét nghiệm mới", True, True),
            ("patient_arrival", "🧑", "#fff4df", "#f59e0b", "Thông báo bệnh nhân đến khám", "Nhận thông báo khi bệnh nhân đến phòng khám", True, False),
            ("notify_system", "⚙️", "#f2ecff", "#8b5cf6", "Thông báo hệ thống", "Cập nhật tính năng, bảo trì hệ thống", False, True),
        ]

        for notif_key, icon_text, icon_bg, icon_color, notif_title, notif_desc_text, is_checked, should_bind in notification_items:
            notif_row = QtWidgets.QFrame()
            notif_row.setStyleSheet("background: transparent; border: none;")
            notif_row_layout = QtWidgets.QHBoxLayout(notif_row)
            notif_row_layout.setContentsMargins(0, 0, 0, 0)
            notif_row_layout.setSpacing(12)

            icon_box = QtWidgets.QLabel(icon_text)
            icon_box.setFixedSize(38, 38)
            icon_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            icon_box.setStyleSheet(
                f"background: {icon_bg}; color: {icon_color}; border-radius: 10px; font-size: 18px; border: none;"
            )
            notif_row_layout.addWidget(icon_box)

            text_box = QtWidgets.QVBoxLayout()
            text_box.setSpacing(2)
            notif_title_lbl = QtWidgets.QLabel(notif_title)
            notif_title_lbl.setStyleSheet("font-size: 14px; color: #0f172a; font-weight: 800; border: none;")
            notif_desc_lbl = QtWidgets.QLabel(notif_desc_text)
            notif_desc_lbl.setStyleSheet("font-size: 12px; color: #64748b; border: none;")
            text_box.addWidget(notif_title_lbl)
            text_box.addWidget(notif_desc_lbl)
            notif_row_layout.addLayout(text_box)
            notif_row_layout.addStretch()

            toggle = QtWidgets.QCheckBox()
            toggle.setChecked(is_checked)
            toggle.setStyleSheet(self._doctor_settings_switch_style())
            if should_bind:
                toggle.toggled.connect(
                    lambda checked, selected_key=notif_key: self._update_notification_setting(selected_key, checked)
                )
                self._settings_notification_toggles[notif_key] = toggle
            notif_row_layout.addWidget(toggle)
            notif_layout.addWidget(notif_row)
        middle_row.addWidget(notification_card, 6)
        right_layout.addLayout(middle_row)

        bottom_row = QtWidgets.QHBoxLayout()
        bottom_row.setSpacing(18)

        schedule_card = QtWidgets.QFrame()
        schedule_card.setStyleSheet(card_style)
        self._settings_section_frames["schedule"] = schedule_card
        schedule_layout = QtWidgets.QVBoxLayout(schedule_card)
        schedule_layout.setContentsMargins(24, 22, 24, 22)
        schedule_layout.setSpacing(14)

        schedule_title = QtWidgets.QLabel("Lịch làm việc")
        schedule_title.setStyleSheet(section_title_style)
        schedule_layout.addWidget(schedule_title)

        schedule_subtitle = QtWidgets.QLabel("Thiết lập lịch làm việc trong tuần")
        schedule_subtitle.setStyleSheet("font-size: 12px; color: #64748b; border: none;")
        schedule_layout.addWidget(schedule_subtitle)

        schedule_grid = QtWidgets.QGridLayout()
        schedule_grid.setHorizontalSpacing(10)
        schedule_grid.setVerticalSpacing(10)
        schedule_grid.setColumnStretch(0, 2)
        schedule_grid.setColumnStretch(1, 2)
        schedule_grid.setColumnStretch(2, 1)
        schedule_grid.setColumnStretch(3, 2)

        time_choices = ["-- : --", "07:00", "07:30", "08:00", "12:00", "17:00"]
        schedule_rows = [
            ("Thứ 2", "07:30", "17:00", True),
            ("Thứ 3", "07:30", "17:00", True),
            ("Thứ 4", "07:30", "17:00", True),
            ("Thứ 5", "07:30", "17:00", True),
            ("Thứ 6", "07:30", "17:00", True),
            ("Thứ 7", "07:30", "12:00", True),
            ("Chủ nhật", "-- : --", "-- : --", False),
        ]

        self._settings_schedule_start_inputs = []
        self._settings_schedule_end_inputs = []
        self._settings_schedule_checkboxes = []
        for row_index, (day_label, start_value, end_value, working) in enumerate(schedule_rows):
            day_lbl = QtWidgets.QLabel(day_label)
            day_lbl.setStyleSheet("font-size: 13px; color: #334155; border: none;")
            schedule_grid.addWidget(day_lbl, row_index, 0)

            start_combo = QtWidgets.QComboBox()
            start_combo.addItems(time_choices)
            start_combo.setCurrentText(start_value)
            start_combo.setEnabled(working)
            start_combo.setStyleSheet(small_input_style)
            schedule_grid.addWidget(start_combo, row_index, 1)
            self._settings_schedule_start_inputs.append(start_combo)

            dash_lbl = QtWidgets.QLabel("-")
            dash_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            dash_lbl.setStyleSheet("font-size: 14px; color: #64748b; border: none;")
            schedule_grid.addWidget(dash_lbl, row_index, 2)

            end_combo = QtWidgets.QComboBox()
            end_combo.addItems(time_choices)
            end_combo.setCurrentText(end_value)
            end_combo.setEnabled(working)
            end_combo.setStyleSheet(small_input_style)
            schedule_grid.addWidget(end_combo, row_index, 3)
            self._settings_schedule_end_inputs.append(end_combo)

            status_checkbox = QtWidgets.QCheckBox("Làm việc" if working else "Nghỉ")
            status_checkbox.setChecked(working)
            status_checkbox.setStyleSheet(self._doctor_settings_day_checkbox_style())
            schedule_grid.addWidget(status_checkbox, row_index, 4)
            self._settings_schedule_checkboxes.append(status_checkbox)

        schedule_layout.addLayout(schedule_grid)

        schedule_save_btn = QtWidgets.QPushButton("Lưu lịch làm việc")
        schedule_save_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        schedule_save_btn.setFixedHeight(42)
        schedule_save_btn.setStyleSheet(
            "QPushButton { background: #16a34a; color: white; border-radius: 10px; padding-left: 18px; padding-right: 18px; "
            "font-size: 13px; font-weight: 800; border: none; }"
            "QPushButton:hover { background: #15803d; }"
        )
        schedule_layout.addWidget(schedule_save_btn, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        bottom_row.addWidget(schedule_card, 7)

        options_card = QtWidgets.QFrame()
        options_card.setStyleSheet(card_style)
        self._settings_section_frames["display"] = options_card
        self._settings_section_frames["prescription_templates"] = options_card
        self._settings_section_frames["conclusion_templates"] = options_card
        self._settings_section_frames["signature"] = options_card
        self._settings_section_frames["backup_restore"] = options_card
        self._settings_section_frames["language"] = options_card
        self._settings_section_frames["intro"] = options_card
        options_layout = QtWidgets.QVBoxLayout(options_card)
        options_layout.setContentsMargins(24, 22, 24, 22)
        options_layout.setSpacing(14)

        options_title = QtWidgets.QLabel("Tùy chọn khác")
        options_title.setStyleSheet(section_title_style)
        options_layout.addWidget(options_title)

        display_options = [
            ("theme_mode", "℞", "Mẫu đơn thuốc", "Quản lý các mẫu đơn thuốc thường dùng"),
            ("font_size", "📄", "Mẫu kết luận", "Quản lý các mẫu kết luận khám bệnh"),
            ("display_density", "✎", "Quản lý chữ ký", "Cập nhật chữ ký điện tử của bác sĩ"),
            ("backup_option", "☁️", "Sao lưu & khôi phục", "Sao lưu và khôi phục dữ liệu cài đặt"),
        ]

        self._settings_display_value_labels = {}
        for opt_key, icon_text, opt_title, opt_desc in display_options:
            opt_row = QtWidgets.QFrame()
            opt_row.setStyleSheet("background: transparent; border: none;")
            opt_row_layout = QtWidgets.QHBoxLayout(opt_row)
            opt_row_layout.setContentsMargins(0, 2, 0, 2)
            opt_row_layout.setSpacing(12)

            icon_label = QtWidgets.QLabel(icon_text)
            icon_label.setFixedWidth(22)
            icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet("font-size: 18px; color: #64748b; border: none;")
            opt_row_layout.addWidget(icon_label)

            opt_text_layout = QtWidgets.QVBoxLayout()
            opt_text_layout.setSpacing(1)
            opt_title_lbl = QtWidgets.QLabel(opt_title)
            opt_title_lbl.setStyleSheet("font-size: 14px; font-weight: 800; color: #0f172a; border: none;")
            opt_desc_lbl = QtWidgets.QLabel(opt_desc)
            opt_desc_lbl.setStyleSheet("font-size: 12px; color: #64748b; border: none;")
            opt_text_layout.addWidget(opt_title_lbl)
            opt_text_layout.addWidget(opt_desc_lbl)
            opt_row_layout.addLayout(opt_text_layout)
            opt_row_layout.addStretch()

            arrow_display = QtWidgets.QLabel("›")
            arrow_display.setStyleSheet("font-size: 18px; color: #94a3b8; border: none;")
            opt_row_layout.addWidget(arrow_display)
            options_layout.addWidget(opt_row)

            value_label = QtWidgets.QLabel("")
            value_label.hide()
            self._settings_display_value_labels[opt_key] = value_label

        options_layout.addStretch()

        reset_btn = QtWidgets.QPushButton("⟲  Đặt lại cài đặt")
        reset_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        reset_btn.setFixedHeight(44)
        reset_btn.setStyleSheet(
            "QPushButton { background: white; color: #ff4d4f; border-radius: 10px; border: 1px solid #fca5a5; "
            "font-size: 13px; font-weight: 800; }"
            "QPushButton:hover { background: #fff5f5; }"
        )
        options_layout.addWidget(reset_btn)
        bottom_row.addWidget(options_card, 6)
        right_layout.addLayout(bottom_row)

        footer_row = QtWidgets.QHBoxLayout()
        footer_row.setContentsMargins(0, 10, 0, 0)
        footer_row.setSpacing(12)
        footer_left = QtWidgets.QLabel("© 2026 CarePlus. Phiên bản 1.2.1")
        footer_left.setStyleSheet("font-size: 12px; color: #94a3b8; font-weight: 600; border: none;")
        footer_right = QtWidgets.QLabel("Chính sách bảo mật   •   Điều khoản sử dụng")
        footer_right.setStyleSheet("font-size: 12px; color: #94a3b8; font-weight: 600; border: none;")
        footer_row.addWidget(footer_left)
        footer_row.addStretch()
        footer_row.addWidget(footer_right)
        right_layout.addLayout(footer_row)

        right_scroll.setWidget(right_content)
        content_wrapper.addWidget(right_scroll)

        page_layout.addLayout(content_wrapper)
        self._load_settings_data()
        return page

    def _save_settings_personal_info(self):
        """Lưu thông tin cá nhân bác sĩ từ trang cài đặt."""
        SettingsController = import_module("controllers.settings_controller").SettingsController

        user_id = self.user_data.get("user_id")
        doctor_id = self.user_data.get("doctor_id")
        if not doctor_id or not user_id:
            QtWidgets.QMessageBox.warning(None, "Lỗi", "Không xác định được tài khoản bác sĩ.")
            return

        name = self._settings_name_input.text().strip()
        if name.startswith("Bác sĩ "):
            name = name[len("Bác sĩ "):]

        payload = {
            "name": name,
            "gender": self._settings_gender_combo.currentText(),
            "dob": None
            if self._settings_dob_input.date() == self._settings_dob_input.minimumDate()
            else self._settings_dob_input.date().toString("yyyy-MM-dd"),
            "phone": self._settings_phone_input.text().strip(),
            "email": self._settings_email_input.text().strip(),
            "specialty": self._settings_specialty_combo.currentText(),
            "address": self._settings_address_input.text().strip(),
        }

        try:
            ok, message = SettingsController.update_personal_info(doctor_id, user_id, payload)
            if not ok:
                QtWidgets.QMessageBox.warning(None, "Không thể lưu", message)
                return

            self.user_data["name"] = str(payload.get("name", ""))
            self.user_data["phone"] = str(payload.get("phone", ""))
            self.user_data["specialty"] = str(payload.get("specialty", ""))
            self.user_data["email"] = str(payload.get("email", ""))
            self.user_name_lbl.setText(f"Bác sĩ {str(payload.get('name', ''))} ▿")
            QtWidgets.QMessageBox.information(None, "Thành công", message)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                None,
                "Lỗi hệ thống",
                f"Không thể lưu thông tin: {e}",
            )

    @staticmethod
    def _doctor_sidebar_button_style(is_active):
        if is_active:
            return (
                "QPushButton { background: #edf9f1; color: #16a34a; border: none; text-align: left; "
                "padding: 16px; padding-left: 20px; padding-right: 20px; border-radius: 16px; font-size: 14px; font-weight: 800; }"
            )

        return (
            "QPushButton { background: transparent; color: #0f172a; border: none; text-align: left; "
            "padding: 16px; padding-left: 20px; padding-right: 20px; border-radius: 16px; font-size: 14px; font-weight: 700; }"
            "QPushButton:hover { background: #f8fafc; }"
        )

    @staticmethod
    def _doctor_settings_switch_style():
        return (
            "QCheckBox { spacing: 0px; }"
            "QCheckBox::indicator { width: 42px; height: 24px; border-radius: 12px; "
            "border: 1px solid #cbd5e1; background: #cbd5e1; }"
            "QCheckBox::indicator:checked { background: #16a34a; border-color: #16a34a; }"
            "QCheckBox::indicator:unchecked { background: #cbd5e1; border-color: #cbd5e1; }"
        )

    @staticmethod
    def _doctor_settings_day_checkbox_style():
        return (
            "QCheckBox { font-size: 13px; color: #334155; spacing: 8px; }"
            "QCheckBox::indicator { width: 16px; height: 16px; border-radius: 4px; "
            "border: 1px solid #cbd5e1; background: white; }"
            "QCheckBox::indicator:checked { background: #16a34a; border-color: #16a34a; }"
            "QCheckBox::indicator:unchecked { background: white; }"
        )

    @staticmethod
    def _settings_nav_style(is_active):
        if is_active:
            return (
                "QPushButton { border: none; text-align: left; padding: 12px; padding-left: 16px; padding-right: 16px; border-radius: 12px; "
                "background: #edf9f1; color: #16a34a; font-size: 13px; font-weight: 800; }"
            )

        return (
            "QPushButton { border: none; text-align: left; padding: 12px; padding-left: 16px; padding-right: 16px; border-radius: 12px; "
            "color: #64748b; font-size: 13px; font-weight: 700; background: transparent; }"
            "QPushButton:hover { background: #f8fafc; }"
        )

    def _set_active_settings_nav(self, active_key):
        for key, button in self._settings_nav_buttons:
            button.setStyleSheet(self._settings_nav_style(key == active_key))

    def _handle_settings_nav_action(self, key):
        self._set_active_settings_nav(key)
        self._scroll_to_settings_section(key)

    def _scroll_to_settings_section(self, key):
        if not self._settings_scroll:
            return

        section_widget = self._settings_section_frames.get(key)
        if section_widget is None:
            return

        scroll_bar = self._settings_scroll.verticalScrollBar()
        scroll_bar.setValue(max(0, section_widget.y() - 8))

    @staticmethod
    def _to_bool(value, default=False):
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(value)
        text = str(value).strip().lower()
        return text in {"1", "true", "yes", "on"}

    def _load_settings_data(self):
        SettingsController = import_module("controllers.settings_controller").SettingsController
        DoctorModel = import_module("models.doctor_model").DoctorModel

        user_id = self.user_data.get("user_id")
        doctor_id = self.user_data.get("doctor_id")
        if not user_id or not doctor_id:
            return

        doctor_data = DoctorModel.get_by_id(doctor_id) or {}
        settings_data = SettingsController.get_settings(user_id) or {}

        if not isinstance(doctor_data, dict):
            doctor_data = {}
        if not isinstance(settings_data, dict):
            settings_data = {}

        name = str(doctor_data.get("name") or self.user_data.get("name") or "").strip()
        if name.lower().startswith("bác sĩ "):
            name = name[7:].strip()
        self._settings_name_input.setText(f"Bác sĩ {name}" if name else "")

        gender = str(settings_data.get("gender") or "Nam")
        gender_index = self._settings_gender_combo.findText(gender)
        if gender_index >= 0:
            self._settings_gender_combo.setCurrentIndex(gender_index)

        dob_value = settings_data.get("dob")
        if dob_value:
            dob_date = QtCore.QDate.fromString(str(dob_value), "yyyy-MM-dd")
            if dob_date.isValid():
                self._settings_dob_input.setDate(dob_date)
        else:
            self._settings_dob_input.setDate(self._settings_dob_input.minimumDate())

        self._settings_phone_input.setText(str(doctor_data.get("phone") or ""))
        self._settings_email_input.setText(str(doctor_data.get("email") or ""))
        self._settings_address_input.setText(str(settings_data.get("address") or ""))

        specialty = str(doctor_data.get("specialty") or "")
        specialty_index = self._settings_specialty_combo.findText(specialty)
        if specialty_index >= 0:
            self._settings_specialty_combo.setCurrentIndex(specialty_index)

        self._settings_cached_values = {
            "language": str(settings_data.get("language") or "Tiếng Việt"),
            "backup_mode": str(settings_data.get("backup_mode") or "cloud"),
            "last_backup_at": settings_data.get("last_backup_at"),
            "last_sync_at": settings_data.get("last_sync_at"),
            "dob": settings_data.get("dob"),
        }

        toggle_mapping = {
            "notify_new_appointment": self._settings_notification_toggles.get("notify_new_appointment"),
            "notify_reminder": self._settings_notification_toggles.get("notify_reminder"),
            "notify_system": self._settings_notification_toggles.get("notify_system"),
        }
        for key, toggle in toggle_mapping.items():
            if toggle is None:
                continue
            toggle.blockSignals(True)
            toggle.setChecked(self._to_bool(settings_data.get(key), True))
            toggle.blockSignals(False)

        for field, label in self._settings_display_value_labels.items():
            value = str(settings_data.get(field) or label.text())
            label.setText(value)

        self._apply_settings_avatar(str(settings_data.get("avatar_path") or "").strip())

    def _apply_settings_avatar(self, avatar_path):
        if not self._settings_avatar_icon:
            return

        if avatar_path:
            pixmap = QtGui.QPixmap(avatar_path)
            if not pixmap.isNull():
                self._settings_avatar_icon.setPixmap(
                    pixmap.scaled(
                        84,
                        84,
                        QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        QtCore.Qt.TransformationMode.SmoothTransformation,
                    )
                )
                self._settings_avatar_icon.setText("")
                return

        self._settings_avatar_icon.setPixmap(QtGui.QPixmap())
        self._settings_avatar_icon.setText("👤")

    def _upload_settings_avatar(self):
        SettingsController = import_module("controllers.settings_controller").SettingsController

        user_id = self.user_data.get("user_id")
        if not user_id:
            return

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Chọn ảnh đại diện",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)",
        )
        if not file_path:
            return

        saved = SettingsController.update_avatar(user_id, file_path)
        if not saved:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Không thể lưu ảnh đại diện.")
            return

        self._apply_settings_avatar(file_path)
        QtWidgets.QMessageBox.information(self, "Thành công", "Đã cập nhật ảnh đại diện.")

    def _update_notification_setting(self, key, checked):
        SettingsController = import_module("controllers.settings_controller").SettingsController

        user_id = self.user_data.get("user_id")
        if not user_id:
            return

        saved = SettingsController.update_notification(user_id, key, checked)
        if not saved:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Không thể cập nhật cài đặt thông báo.")

    def _choose_display_option(self, key):
        SettingsController = import_module("controllers.settings_controller").SettingsController

        user_id = self.user_data.get("user_id")
        value_label = self._settings_display_value_labels.get(key)
        if not user_id or value_label is None:
            return

        option_map = SettingsController.DISPLAY_OPTION_MAP
        options = option_map.get(key, [])
        if not options:
            return

        current_value = value_label.text().strip()
        current_index = options.index(current_value) if current_value in options else 0
        next_index = (current_index + 1) % len(options)
        next_value = options[next_index]

        updated = SettingsController.update_display_option(user_id, key, next_value)
        if not updated:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Không thể lưu tùy chọn hiển thị.")
            return

        value_label.setText(next_value)

    def _open_change_password_dialog(self):
        SettingsController = import_module("controllers.settings_controller").SettingsController

        user_id = self.user_data.get("user_id")
        if not user_id:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Không xác định được người dùng hiện tại.")
            return

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Đổi mật khẩu")
        dialog.setModal(True)
        dialog.resize(420, 220)

        layout = QtWidgets.QVBoxLayout(dialog)
        form_layout = QtWidgets.QFormLayout()

        current_input = QtWidgets.QLineEdit()
        current_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        new_input = QtWidgets.QLineEdit()
        new_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        confirm_input = QtWidgets.QLineEdit()
        confirm_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        form_layout.addRow("Mật khẩu cũ", current_input)
        form_layout.addRow("Mật khẩu mới", new_input)
        form_layout.addRow("Xác nhận", confirm_input)
        layout.addLayout(form_layout)

        button_row = QtWidgets.QHBoxLayout()
        button_row.addStretch()
        cancel_btn = QtWidgets.QPushButton("Hủy")
        save_btn = QtWidgets.QPushButton("Lưu")
        button_row.addWidget(cancel_btn)
        button_row.addWidget(save_btn)
        layout.addLayout(button_row)

        cancel_btn.clicked.connect(dialog.reject)

        def _submit_password_change():
            ok, message = SettingsController.change_password(
                user_id,
                current_input.text(),
                new_input.text(),
                confirm_input.text(),
            )
            if not ok:
                QtWidgets.QMessageBox.warning(dialog, "Không thể đổi mật khẩu", message)
                return
            QtWidgets.QMessageBox.information(dialog, "Thành công", message)
            dialog.accept()

        save_btn.clicked.connect(_submit_password_change)
        dialog.exec()

    def _open_language_dialog(self):
        SettingsController = import_module("controllers.settings_controller").SettingsController

        user_id = self.user_data.get("user_id")
        if not user_id:
            return

        current_language = self._settings_cached_values.get("language", "Tiếng Việt")
        language, ok = QtWidgets.QInputDialog.getItem(
            self,
            "Ngôn ngữ",
            "Chọn ngôn ngữ hiển thị:",
            SettingsController.LANGUAGES,
            SettingsController.LANGUAGES.index(current_language)
            if current_language in SettingsController.LANGUAGES
            else 0,
            False,
        )
        if not ok:
            return

        updated = SettingsController.update_language(user_id, language)
        if not updated:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Không thể cập nhật ngôn ngữ.")
            return

        self._settings_cached_values["language"] = language
        QtWidgets.QMessageBox.information(
            self,
            "Đã cập nhật",
            f"Ngôn ngữ hiển thị đã chuyển sang: {language}.",
        )

    def _open_backup_sync_dialog(self):
        SettingsController = import_module("controllers.settings_controller").SettingsController

        user_id = self.user_data.get("user_id")
        if not user_id:
            return

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Sao lưu & đồng bộ")
        dialog.setModal(True)
        dialog.resize(460, 250)

        layout = QtWidgets.QVBoxLayout(dialog)

        mode_row = QtWidgets.QHBoxLayout()
        mode_label = QtWidgets.QLabel("Chế độ sao lưu:")
        mode_combo = QtWidgets.QComboBox()
        mode_combo.addItem("Cloud", userData="cloud")
        mode_combo.addItem("Local", userData="local")

        current_mode = self._settings_cached_values.get("backup_mode", "cloud")
        mode_index = mode_combo.findData(current_mode)
        if mode_index >= 0:
            mode_combo.setCurrentIndex(mode_index)

        mode_row.addWidget(mode_label)
        mode_row.addWidget(mode_combo)
        layout.addLayout(mode_row)

        last_backup = self._settings_cached_values.get("last_backup_at")
        last_sync = self._settings_cached_values.get("last_sync_at")
        info_label = QtWidgets.QLabel(
            f"Lần backup gần nhất: {last_backup or 'Chưa có'}\nLần đồng bộ gần nhất: {last_sync or 'Chưa có'}"
        )
        info_label.setStyleSheet("color: #64748b;")
        layout.addWidget(info_label)

        button_row = QtWidgets.QHBoxLayout()
        backup_btn = QtWidgets.QPushButton("Backup ngay")
        sync_btn = QtWidgets.QPushButton("Đồng bộ ngay")
        close_btn = QtWidgets.QPushButton("Đóng")
        button_row.addWidget(backup_btn)
        button_row.addWidget(sync_btn)
        button_row.addStretch()
        button_row.addWidget(close_btn)
        layout.addLayout(button_row)

        def _refresh_status_text():
            last_backup_text = self._settings_cached_values.get("last_backup_at") or "Chưa có"
            last_sync_text = self._settings_cached_values.get("last_sync_at") or "Chưa có"
            info_label.setText(
                f"Lần backup gần nhất: {last_backup_text}\nLần đồng bộ gần nhất: {last_sync_text}"
            )

        def _backup_now():
            selected_mode = mode_combo.currentData()
            ok, result = SettingsController.backup_now(user_id, selected_mode)
            if not ok:
                QtWidgets.QMessageBox.warning(dialog, "Lỗi", str(result))
                return

            self._settings_cached_values["backup_mode"] = selected_mode
            self._settings_cached_values["last_backup_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _refresh_status_text()
            QtWidgets.QMessageBox.information(
                dialog,
                "Thành công",
                f"Backup dữ liệu thành công.\nFile: {result}",
            )

        def _sync_now():
            ok, result = SettingsController.sync_now(user_id)
            if not ok:
                QtWidgets.QMessageBox.warning(dialog, "Lỗi", str(result))
                return

            self._settings_cached_values["last_sync_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _refresh_status_text()
            QtWidgets.QMessageBox.information(dialog, "Thành công", str(result))

        backup_btn.clicked.connect(_backup_now)
        sync_btn.clicked.connect(_sync_now)
        close_btn.clicked.connect(dialog.accept)

        dialog.exec()

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
            
    def _build_persisted_notification_center_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QtWidgets.QLabel("Thông báo")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0f172a;")
        layout.addWidget(title)

        mark_all_btn = QtWidgets.QPushButton("Đánh dấu tất cả đã đọc")
        mark_all_btn.clicked.connect(self.mark_all_notifications_read)
        layout.addWidget(mark_all_btn)

        self.notification_list = QtWidgets.QListWidget()
        self.notification_list.itemClicked.connect(self._open_notification_item)
        layout.addWidget(self.notification_list, 1)
        self.load_notifications()
        return page

    def load_notifications(self):
        from controllers.notification_controller import NotificationController

        if not hasattr(self, "notification_list"):
            return
        self.notification_list.clear()
        user_id = self.user_data.get("user_id")
        self.notifications = NotificationController.list_for_user(user_id)
        if not self.notifications:
            self.notification_list.addItem("Không có thông báo.")
            self.refresh_notification_badge()
            return

        for row in self.notifications:
            status = "●" if not row.get("is_read") else "○"
            item = QtWidgets.QListWidgetItem(f"{status} {row.get('title', '')} - {row.get('content', '')}")
            item.setData(QtCore.Qt.ItemDataRole.UserRole, row)
            self.notification_list.addItem(item)
        self.refresh_notification_badge()

    def refresh_notification_badge(self):
        from controllers.notification_controller import NotificationController

        count = NotificationController.unread_count(self.user_data.get("user_id"))
        if hasattr(self, "bell_badge"):
            self.bell_badge.setText(str(count))
            self.bell_badge.setVisible(count > 0)
        return count

    def mark_all_notifications_read(self):
        from controllers.notification_controller import NotificationController

        NotificationController.mark_all_read(self.user_data.get("user_id"))
        self.load_notifications()

    def _open_notification_item(self, item):
        from controllers.notification_controller import NotificationController

        row = item.data(QtCore.Qt.ItemDataRole.UserRole)
        if not isinstance(row, dict):
            return
        NotificationController.mark_read(row.get("notification_id"), self.user_data.get("user_id"))
        self.switch_page(NotificationController.target_index(row.get("target_page")))
        self.refresh_notification_badge()

    def _build_persisted_notification_center_page(self):
        page = QtWidgets.QWidget()
        page.setStyleSheet("background: #f8fbff;")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        title = QtWidgets.QLabel("Thông báo")
        title.setStyleSheet("font-size: 30px; font-weight: 900; color: #0f172a;")
        breadcrumb = QtWidgets.QLabel("Trang chủ  >  Thông báo")
        breadcrumb.setStyleSheet("font-size: 14px; color: #667085;")
        layout.addWidget(title)
        layout.addWidget(breadcrumb)

        self.active_notification_tab = "all"
        self.notification_tabs = QtWidgets.QHBoxLayout()
        self.notification_tabs.setSpacing(8)
        layout.addLayout(self.notification_tabs)

        body = QtWidgets.QHBoxLayout()
        body.setSpacing(16)
        left_card = QtWidgets.QFrame()
        left_card.setStyleSheet("background: white; border: 1px solid #EAECF0; border-radius: 16px;")
        left_layout = QtWidgets.QVBoxLayout(left_card)
        left_layout.setContentsMargins(16, 16, 16, 16)
        left_layout.setSpacing(12)

        top = QtWidgets.QHBoxLayout()
        self.notification_search = QtWidgets.QLineEdit()
        self.notification_search.setPlaceholderText("Tìm kiếm thông báo...")
        self.notification_search.setMinimumHeight(42)
        self.notification_search.setStyleSheet(
            "background: white; color: #344054; border: 1px solid #D0D5DD; border-radius: 10px; padding: 8px 12px;"
        )
        self.notification_search.textChanged.connect(self.load_notifications)
        mark_all_btn = QtWidgets.QPushButton("Đánh dấu tất cả đã đọc")
        settings_btn = QtWidgets.QPushButton("Cài đặt thông báo")
        for btn in [mark_all_btn, settings_btn]:
            btn.setMinimumHeight(42)
            btn.setStyleSheet("background: white; color: #344054; border: 1px solid #D0D5DD; border-radius: 10px; padding: 8px 12px; font-weight: 800;")
        mark_all_btn.clicked.connect(self.mark_all_notifications_read)
        settings_btn.clicked.connect(lambda: self.switch_page(7))
        top.addWidget(self.notification_search, 1)
        top.addWidget(mark_all_btn)
        top.addWidget(settings_btn)
        left_layout.addLayout(top)

        self.notification_list = QtWidgets.QListWidget()
        self.notification_list.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.notification_list.setSpacing(8)
        self.notification_list.setStyleSheet(
            "QListWidget { background: white; border: none; color: #344054; }"
            "QListWidget::item { border: 1px solid #EAECF0; border-radius: 12px; padding: 12px; margin: 2px; }"
            "QListWidget::item:selected { background: #ECFDF3; color: #101828; border-color: #16B364; }"
        )
        self.notification_list.itemClicked.connect(self._open_notification_item)
        left_layout.addWidget(self.notification_list, 1)
        self.notification_page_label = QtWidgets.QLabel("Hiển thị 10 bản ghi   < 1 2 3 >")
        self.notification_page_label.setStyleSheet("color: #667085; font-size: 13px;")
        left_layout.addWidget(self.notification_page_label)
        body.addWidget(left_card, 7)

        right_card = QtWidgets.QFrame()
        right_card.setStyleSheet("background: white; border: 1px solid #EAECF0; border-radius: 16px;")
        right_layout = QtWidgets.QVBoxLayout(right_card)
        right_layout.setContentsMargins(18, 18, 18, 18)
        right_layout.setSpacing(12)
        detail_title = QtWidgets.QLabel("Chi tiết thông báo")
        detail_title.setStyleSheet("font-size: 18px; font-weight: 900; color: #101828;")
        self.notification_detail_title = QtWidgets.QLabel("Chưa chọn thông báo")
        self.notification_detail_title.setWordWrap(True)
        self.notification_detail_title.setStyleSheet("font-size: 16px; font-weight: 900; color: #101828;")
        self.notification_detail_body = QtWidgets.QLabel("Chọn thông báo trong danh sách để xem chi tiết.")
        self.notification_detail_body.setWordWrap(True)
        self.notification_detail_body.setStyleSheet("color: #475467; font-size: 13px;")
        self.notification_detail_actions = QtWidgets.QHBoxLayout()
        right_layout.addWidget(detail_title)
        right_layout.addWidget(self.notification_detail_title)
        right_layout.addWidget(self.notification_detail_body)
        right_layout.addStretch()
        right_layout.addLayout(self.notification_detail_actions)
        body.addWidget(right_card, 3)
        layout.addLayout(body, 1)

        self.load_notifications()
        return page

    def load_notifications(self):
        from controllers.notification_controller import NotificationController

        if not hasattr(self, "notification_list"):
            return
        self.notification_list.clear()
        user_id = self.user_data.get("user_id")
        self.notifications = NotificationController.list_for_user(user_id)
        self._render_notification_tabs()
        keyword = self.notification_search.text().strip().lower() if hasattr(self, "notification_search") else ""
        rows = [dict(row) for row in self.notifications]
        tab = getattr(self, "active_notification_tab", "all")
        if tab == "unread":
            rows = [row for row in rows if not row.get("is_read")]
        elif tab not in {"all", "other"}:
            rows = [row for row in rows if str(row.get("type") or "system") == tab]
        elif tab == "other":
            known = {"appointment", "result", "patient", "prescription", "warning", "system"}
            rows = [row for row in rows if str(row.get("type") or "") not in known]
        if keyword:
            rows = [row for row in rows if keyword in f"{row.get('title', '')} {row.get('content', '')}".lower()]
        if not rows:
            self.notification_list.addItem("Không có thông báo.")
            self._render_notification_detail(None)
            self.refresh_notification_badge()
            return
        for row in rows:
            status = "●" if not row.get("is_read") else "○"
            item = QtWidgets.QListWidgetItem(f"{status} [{self._notification_type_label(row.get('type'))}] {row.get('title', '')}\n{row.get('content', '')}")
            item.setData(QtCore.Qt.ItemDataRole.UserRole, row)
            self.notification_list.addItem(item)
        self.notification_list.setCurrentRow(0)
        self._render_notification_detail(rows[0])
        self.refresh_notification_badge()

    def _render_notification_tabs(self):
        if not hasattr(self, "notification_tabs"):
            return
        while self.notification_tabs.count():
            item = self.notification_tabs.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        rows = getattr(self, "notifications", []) or []
        tab_defs = [
            ("all", f"Tất cả ({len(rows)})"),
            ("unread", f"Chưa đọc ({len([r for r in rows if not r.get('is_read')])})"),
            ("appointment", f"Lịch hẹn ({len([r for r in rows if r.get('type') == 'appointment'])})"),
            ("result", f"Kết quả ({len([r for r in rows if r.get('type') == 'result'])})"),
            ("system", f"Hệ thống ({len([r for r in rows if r.get('type') == 'system'])})"),
            ("other", "Khác"),
        ]
        for key, text in tab_defs:
            btn = QtWidgets.QPushButton(text)
            btn.setMinimumHeight(38)
            active = key == getattr(self, "active_notification_tab", "all")
            btn.setStyleSheet(
                "QPushButton { "
                + ("background: #ECFDF3; color: #16B364; border: none;" if active else "background: white; color: #667085; border: 1px solid #EAECF0;")
                + " border-radius: 10px; padding: 0 14px; font-weight: 800; }"
            )
            btn.clicked.connect(lambda checked=False, tab=key: self._set_notification_tab(tab))
            self.notification_tabs.addWidget(btn)
        self.notification_tabs.addStretch()

    def _set_notification_tab(self, tab):
        self.active_notification_tab = tab
        self.load_notifications()

    def _notification_type_label(self, value):
        return {
            "appointment": "Lịch hẹn",
            "result": "Kết quả",
            "patient": "Bệnh nhân",
            "prescription": "Đơn thuốc",
            "warning": "Cảnh báo",
            "system": "Hệ thống",
        }.get(str(value or "system"), "Khác")

    def _render_notification_detail(self, row):
        if not hasattr(self, "notification_detail_title"):
            return
        while self.notification_detail_actions.count():
            item = self.notification_detail_actions.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        if not row:
            self.notification_detail_title.setText("Chưa chọn thông báo")
            self.notification_detail_body.setText("Chọn thông báo trong danh sách để xem chi tiết.")
            return
        status = "Chưa đọc" if not row.get("is_read") else "Đã đọc"
        self.notification_detail_title.setText(str(row.get("title") or "Thông báo"))
        self.notification_detail_body.setText(
            f"Loại: {self._notification_type_label(row.get('type'))}\n"
            f"Trạng thái: {status}\n"
            f"Thời gian: {row.get('created_at') or 'Chưa cập nhật'}\n\n"
            f"{row.get('content') or ''}\n\n"
            f"Nguồn liên kết: {row.get('target_page') or 'dashboard'} #{row.get('target_id') or ''}"
        )
        open_btn = QtWidgets.QPushButton("Mở liên kết")
        delete_btn = QtWidgets.QPushButton("Xóa thông báo")
        for btn in [open_btn, delete_btn]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet("background: white; color: #344054; border: 1px solid #D0D5DD; border-radius: 10px; padding: 8px 12px; font-weight: 800;")
            self.notification_detail_actions.addWidget(btn)
        open_btn.clicked.connect(lambda checked=False, r=row: self._open_notification_row(r))

    def mark_all_notifications_read(self):
        from controllers.notification_controller import NotificationController

        NotificationController.mark_all_read(self.user_data.get("user_id"))
        self.load_notifications()

    def _open_notification_item(self, item):
        row = item.data(QtCore.Qt.ItemDataRole.UserRole)
        if not isinstance(row, dict):
            return
        self._render_notification_detail(row)
        self._open_notification_row(row)

    def _open_notification_row(self, row):
        from controllers.notification_controller import NotificationController

        NotificationController.mark_read(row.get("notification_id"), self.user_data.get("user_id"))
        self.switch_page(NotificationController.target_index(row.get("target_page")))
        self.refresh_notification_badge()

    def switch_page(self, index):
        self.content_stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setStyleSheet(self._doctor_sidebar_button_style(i == index))

    def open_patient_record(self, patient_id):
        profile = getattr(self, "page_patient_record", None)
        if hasattr(profile, "set_patient"):
            profile.set_patient(patient_id)
        if profile is not None:
            index = self.content_stack.indexOf(profile)
            if index >= 0:
                self.switch_page(index)

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

        role = str(self.user_data.get("role") or "admin").lower().strip()
        self.page_patient_mgmt.role = role
        self.page_doctor_mgmt.role = role
        self.page_appt_mgmt.role = role
        self.page_service_mgmt.role = role
        self.page_med_mgmt.role = role
        self.page_pay_mgmt.role = role
        
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
