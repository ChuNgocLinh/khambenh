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
        self.page_dashboard_layout = QtWidgets.QVBoxLayout(self.page_dashboard)
        self.page_dashboard_layout.setContentsMargins(0, 0, 0, 0)
        self.page_dashboard_layout.setSpacing(20)
        self.dashboard_filter_state = {
            "range_key": "30d",
            "from_date": QtCore.QDate.currentDate().addDays(-29),
            "to_date": QtCore.QDate.currentDate(),
        }
        self.dashboard_data = {}
        self._render_dashboard_page()

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
        self.content_stack.addWidget(self._build_notification_center_page(self.dashboard_data.get("notifications", [])))  # 6: Thông báo
        self.content_stack.addWidget(self._build_settings_page())  # 7: Cài đặt

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

        self.dashboard_data = self._build_doctor_dashboard_data(self.user_data.get("doctor_id"))

        self.lbl_page_title = QtWidgets.QLabel("Thống kê khám bệnh")
        self.lbl_page_title.setStyleSheet("font-size: 30px; font-weight: 800; color: #2c3e50;")
        self.page_dashboard_layout.addWidget(self.lbl_page_title)

        description = QtWidgets.QLabel(
            "Theo dõi toàn cảnh hiệu suất khám bệnh, xu hướng bệnh nhân và hoạt động kê đơn trong khoảng thời gian bạn chọn."
        )
        description.setWordWrap(True)
        description.setStyleSheet("font-size: 14px; color: #64748b; margin-top: -6px;")
        self.page_dashboard_layout.addWidget(description)

        self.page_dashboard_layout.addWidget(self._build_dashboard_filter_bar())
        self.page_dashboard_layout.addLayout(self._build_dashboard_kpi_row())
        self.page_dashboard_layout.addLayout(self._build_dashboard_analytics_row())
        self.page_dashboard_layout.addLayout(self._build_dashboard_trend_row())
        self.page_dashboard_layout.addLayout(self._build_dashboard_distribution_row())
        self.page_dashboard_layout.addLayout(self._build_dashboard_summary_row())

        updated_label = QtWidgets.QLabel(
            f"Dữ liệu được cập nhật lúc {self.dashboard_data.get('updated_at', '')} • Tổng hợp theo khoảng thời gian đang chọn."
        )
        updated_label.setStyleSheet("font-size: 12px; color: #64748b; font-style: italic;")
        self.page_dashboard_layout.addWidget(updated_label)
        self.page_dashboard_layout.addStretch()

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
                "padding: 8px 10px; border-radius: 8px; border: 1px solid #dbe2ea; background: white;"
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
