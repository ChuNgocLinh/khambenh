from datetime import datetime, timedelta
from PyQt6 import QtWidgets, QtCore, QtGui
from controllers.appointment_controller import AppointmentController


class DoctorScheduleView(QtWidgets.QWidget):
    STATUS_META = {
        "done": ("Đã khám", "#16a34a", "#ecfdf5"),
        "in_progress": ("Đang khám", "#2563eb", "#eff6ff"),
        "confirmed": ("Đang chờ", "#f59e0b", "#fff7ed"),
        "pending": ("Đã đặt lịch", "#94a3b8", "#f8fafc"),
        "cancelled": ("Đã hủy", "#ef4444", "#fef2f2"),
    }

    def __init__(self, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        self.role = "doctor"
        self.selected_schedule = None
        self.all_rows = self._build_schedule_rows()
        self.filtered_rows = []
        self.setStyleSheet("background: #f8fbff; border: none;")

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)
        root.addLayout(self._build_header())
        root.addWidget(self._build_filter_bar())

        body = QtWidgets.QHBoxLayout()
        body.setSpacing(18)
        body.addWidget(self._build_timeline_card(), 7)
        right = QtWidgets.QVBoxLayout()
        right.setSpacing(16)
        right.addWidget(self._build_month_card())
        right.addWidget(self._build_detail_card(), 1)
        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right)
        body.addWidget(right_widget, 3)
        root.addLayout(body, 1)
        self._apply_filters()

    def _build_header(self):
        header = QtWidgets.QHBoxLayout()
        title_col = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("Lịch khám")
        title.setStyleSheet("border: none; background: transparent; font-size: 25px; color: #0f172a; font-weight: 900;")
        crumb = QtWidgets.QLabel("Trang chủ  ›  Lịch khám")
        crumb.setStyleSheet("border: none; background: transparent; font-size: 14px; color: #64748b; font-weight: 700;")
        title_col.addWidget(title)
        title_col.addWidget(crumb)
        header.addLayout(title_col, 1)
        for text, style in [("🔔 2", "font-size: 20px; color: #64748b;"), ("👨‍⚕️", "background: #eaf2ff; border-radius: 21px; font-size: 20px;")]:
            label = QtWidgets.QLabel(text)
            label.setFixedSize(48, 42)
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("border: none; " + style)
            header.addWidget(label)
        name = QtWidgets.QLabel("Bác sĩ Minh  ▾")
        name.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 13px; font-weight: 900;")
        header.addWidget(name)
        return header

    def _build_filter_bar(self):
        card = QtWidgets.QFrame()
        card.setStyleSheet("background: #ffffff; border: 1px solid #e7edf5; border-radius: 14px;")
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(12)
        prev_btn = self._small_button("‹")
        next_btn = self._small_button("›")
        today_btn = self._small_button("Hôm nay", 116)
        add_btn = QtWidgets.QPushButton("+  Thêm lịch khám")
        add_btn.setStyleSheet(self._primary_style())
        add_btn.clicked.connect(self.add_new)
        self.date_input = QtWidgets.QDateEdit(QtCore.QDate(2026, 5, 23))
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        self.date_input.setMinimumWidth(148)
        self.status_filter = QtWidgets.QComboBox()
        self.status_filter.addItems(["Tất cả trạng thái", "Đã khám", "Đang khám", "Đang chờ", "Đã hủy", "Đã đặt lịch"])
        self.service_filter = QtWidgets.QComboBox()
        self.service_filter.addItems(["Tất cả dịch vụ", "Khám tổng quát", "Khám tim mạch", "Tư vấn sức khỏe", "Khám phụ khoa"])
        self.room_filter = QtWidgets.QComboBox()
        self.room_filter.addItems(["Tất cả phòng khám", "Phòng khám 1", "Phòng khám 2"])
        for widget in [self.date_input, self.status_filter, self.service_filter, self.room_filter]:
            widget.setStyleSheet(self._input_style())
            widget.setMinimumHeight(42)
        for combo in [self.status_filter, self.service_filter, self.room_filter]:
            combo.setMinimumWidth(170)
        self.date_input.dateChanged.connect(self._apply_filters)
        self.status_filter.currentIndexChanged.connect(self._apply_filters)
        self.service_filter.currentIndexChanged.connect(self._apply_filters)
        self.room_filter.currentIndexChanged.connect(self._apply_filters)
        today_btn.clicked.connect(lambda: self.date_input.setDate(QtCore.QDate.currentDate()))
        prev_btn.clicked.connect(lambda: self.date_input.setDate(self.date_input.date().addDays(-1)))
        next_btn.clicked.connect(lambda: self.date_input.setDate(self.date_input.date().addDays(1)))
        for widget in [prev_btn, self.date_input, next_btn, today_btn, self.status_filter, self.service_filter, self.room_filter]:
            layout.addWidget(widget)
        layout.addStretch()
        layout.addWidget(add_btn)
        return card

    def _build_timeline_card(self):
        card = QtWidgets.QFrame()
        card.setStyleSheet("background: #ffffff; border: 1px solid #e7edf5; border-radius: 14px;")
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(22, 20, 22, 20)
        top = QtWidgets.QHBoxLayout()
        self.timeline_title = QtWidgets.QLabel("Lịch khám trong ngày - Thứ Sáu, 23/05/2026")
        self.timeline_title.setStyleSheet("border: none; background: transparent; font-size: 18px; color: #0f172a; font-weight: 900;")
        top.addWidget(self.timeline_title, 1)
        for status in ["done", "in_progress", "confirmed", "cancelled", "pending"]:
            label, color, _ = self.STATUS_META[status]
            top.addWidget(self._legend(label, color))
        layout.addLayout(top)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")
        timeline_body = QtWidgets.QWidget()
        timeline_body.setStyleSheet("background: transparent; border: none;")
        self.timeline_list = QtWidgets.QVBoxLayout(timeline_body)
        self.timeline_list.setContentsMargins(0, 8, 0, 0)
        self.timeline_list.setSpacing(6)
        scroll.setWidget(timeline_body)
        layout.addWidget(scroll, 1)
        return card

    def _build_detail_card(self):
        card = QtWidgets.QFrame()
        card.setStyleSheet("background: #ffffff; border: 1px solid #e7edf5; border-radius: 14px;")
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        title = QtWidgets.QLabel("Thông tin lịch khám")
        title.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 17px; font-weight: 900;")
        self.detail_patient = QtWidgets.QLabel("Chưa chọn lịch khám")
        self.detail_patient.setMinimumHeight(92)
        self.detail_patient.setWordWrap(True)
        self.detail_patient.setStyleSheet("background: #f8fafc; border: 1px solid #e7edf5; border-radius: 10px; padding: 12px; color: #0f172a; font-size: 13px; font-weight: 800;")
        self.detail_info = QtWidgets.QLabel("Chọn một lịch trong timeline để xem chi tiết.")
        self.detail_info.setMinimumHeight(132)
        self.detail_info.setWordWrap(True)
        self.detail_info.setStyleSheet("border: none; background: transparent; color: #334155; font-size: 13px; font-weight: 800;")
        layout.addWidget(title)
        layout.addWidget(self.detail_patient)
        layout.addWidget(self.detail_info)
        action_title = QtWidgets.QLabel("Hành động")
        action_title.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 16px; font-weight: 900;")
        layout.addWidget(action_title)
        for text, style, callback in [
            ("🩺  Bắt đầu khám", self._primary_style(), self._start_selected_exam),
            ("👁  Xem hồ sơ bệnh nhân", self._outline_style("#475569"), self._view_selected_patient),
            ("✎  Chỉnh sửa lịch", self._outline_style("#475569"), self._edit_selected_appointment),
            ("🗑  Hủy lịch khám", self._outline_style("#ef4444"), self._cancel_selected_appointment),
        ]:
            btn = QtWidgets.QPushButton(text)
            btn.setMinimumHeight(44)
            btn.setStyleSheet(style)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        return card

    def _input_style(self):
        return "background: #ffffff; border: 1px solid #dbe4ee; border-radius: 8px; padding: 9px 12px; color: #0f172a; font-weight: 800;"

    def _primary_style(self):
        return "QPushButton { background: #13a66b; color: #ffffff; border: none; border-radius: 9px; padding: 11px 16px; font-weight: 900; } QPushButton:hover { background: #0f8f5c; }"

    def _outline_style(self, color):
        return f"QPushButton {{ background: #ffffff; color: {color}; border: 1px solid #dbe4ee; border-radius: 9px; padding: 11px 16px; font-weight: 900; }} QPushButton:hover {{ border-color: {color}; }}"

    def _small_button(self, text, width=46):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedSize(width, 42)
        btn.setStyleSheet(self._outline_style("#475569"))
        return btn

    def _legend(self, text, color):
        label = QtWidgets.QLabel(f"●  {text}")
        label.setStyleSheet(f"border: none; background: transparent; color: {color}; font-size: 12px; font-weight: 900;")
        return label

    def _build_schedule_rows(self):
        sample = [
            ("07:00", "Trần Văn Hùng", "Nam", 40, "Khám tổng quát", "pending"),
            ("08:00", "Nguyễn Thị Lan", "Nữ", 32, "Khám phụ khoa", "done"),
            ("09:00", "Lê Minh Tuấn", "Nam", 35, "Tư vấn sức khỏe", "in_progress"),
            ("10:00", "Phạm Thị Mai", "Nữ", 28, "Đau đầu, chóng mặt", "confirmed"),
            ("10:30", "Hoàng Văn Nam", "Nam", 45, "Khám tim mạch", "confirmed"),
            ("11:00", "Vũ Thị Hương", "Nữ", 30, "Khám thai định kỳ", "done"),
            ("13:30", "Đỗ Quốc Bảo", "Nam", 50, "Khám cơ xương khớp", "pending"),
            ("14:00", "Trần Thị Thu", "Nữ", 26, "Dị ứng, mẩn ngứa", "confirmed"),
            ("15:00", "Nguyễn Văn Đạt", "Nam", 33, "Khám da liễu", "cancelled"),
            ("16:00", "Lý Thị Nga", "Nữ", 29, "Khám tổng quát", "pending"),
        ]
        catalog = []
        try:
            rows = AppointmentController.get_management_rows_by_doctor(self.doctor_id) or []
        except Exception:
            rows = []
        for idx, row in enumerate(rows):
            item = dict(row)
            item.setdefault("room", "Phòng khám 1")
            item.setdefault("service_name", self._extract_service(item.get("note")))
            item.setdefault("gender", "Nam" if idx % 2 == 0 else "Nữ")
            item.setdefault("age", 30 + idx)
            catalog.append(item)
        if len(catalog) < 8:
            for idx, (time_text, name, gender, age, service, status) in enumerate(sample, start=1):
                catalog.append({
                    "appointment_id": 1000 + idx,
                    "patient_id": idx,
                    "patient_name": name,
                    "patient_phone": "0987 654 321",
                    "gender": gender,
                    "age": age,
                    "service_name": service,
                    "room": "Phòng khám 1",
                    "status": status,
                    "note": "Không có",
                    "appointment_date": f"2026-05-23 {time_text}:00",
                })
        return catalog

    def _extract_service(self, note):
        text = str(note or "")
        if text.startswith("Dịch vụ:"):
            return text.replace("Dịch vụ:", "", 1).split("|", 1)[0].strip() or "Khám tổng quát"
        return "Khám tổng quát" if text.startswith("Dá»‹ch") else (text or "Khám tổng quát")

    def _to_datetime(self, value):
        if isinstance(value, datetime):
            return value
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M"):
            try:
                return datetime.strptime(str(value), fmt)
            except ValueError:
                continue
        return None

    def _apply_filters(self):
        selected_date = self.date_input.date().toPyDate()
        status_text = self.status_filter.currentText()
        service_text = self.service_filter.currentText()
        room_text = self.room_filter.currentText()
        filtered = []
        for row in self.all_rows:
            dt_value = self._to_datetime(row.get("appointment_date"))
            if dt_value and dt_value.date() != selected_date and not str(row.get("appointment_id", "")).startswith("100"):
                continue
            status_label = self.STATUS_META.get(str(row.get("status")), ("", "", ""))[0]
            if status_text != "Tất cả trạng thái" and status_label != status_text:
                continue
            if service_text != "Tất cả dịch vụ" and str(row.get("service_name") or "") != service_text:
                continue
            if room_text != "Tất cả phòng khám" and str(row.get("room") or "") != room_text:
                continue
            filtered.append(row)
        filtered.sort(key=lambda r: str(r.get("appointment_date") or ""))
        self.filtered_rows = filtered
        self.timeline_title.setText(self._timeline_title_text())
        self._render_timeline()

    def _timeline_title_text(self):
        day_names = {
            1: "Thứ Hai",
            2: "Thứ Ba",
            3: "Thứ Tư",
            4: "Thứ Năm",
            5: "Thứ Sáu",
            6: "Thứ Bảy",
            7: "Chủ Nhật",
        }
        qdate = self.date_input.date()
        return f"Lịch khám trong ngày - {day_names.get(qdate.dayOfWeek(), '')}, {qdate.toString('dd/MM/yyyy')}"

    def _render_timeline(self):
        while self.timeline_list.count():
            item = self.timeline_list.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        for hour in ["07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]:
            row = QtWidgets.QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(10)
            hour_lbl = QtWidgets.QLabel(hour)
            hour_lbl.setFixedWidth(84)
            hour_lbl.setStyleSheet("border: none; background: transparent; color: #334155; font-size: 15px; font-weight: 900;")
            row.addWidget(hour_lbl)
            matches = [appt for appt in self.filtered_rows if str(appt.get("appointment_date", ""))[11:16].startswith(hour[:2])]
            row.addWidget(self._appointment_block(matches[0]) if matches else self._empty_slot(), 1)
            holder = QtWidgets.QWidget()
            holder.setMinimumHeight(74 if matches else 56)
            holder.setLayout(row)
            self.timeline_list.addWidget(holder)
        self.timeline_list.addStretch()
        if self.filtered_rows:
            self._select_schedule(self.filtered_rows[min(2, len(self.filtered_rows) - 1)])

    def _empty_slot(self):
        empty = QtWidgets.QFrame()
        empty.setFixedHeight(48)
        empty.setStyleSheet("background: transparent; border-bottom: 1px solid #edf2f7;")
        return empty

    def _appointment_block(self, appt):
        status = str(appt.get("status") or "pending")
        label, color, bg = self.STATUS_META.get(status, self.STATUS_META["pending"])
        card = QtWidgets.QFrame()
        card.setFixedHeight(70)
        card.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        card.setStyleSheet(f"background: {bg}; border: 1px solid {color}55; border-left: 3px solid {color}; border-radius: 9px;")
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(16, 8, 12, 8)
        dt_value = self._to_datetime(appt.get("appointment_date"))
        start = dt_value.strftime("%H:%M") if dt_value else "--:--"
        end = (dt_value + timedelta(minutes=30)).strftime("%H:%M") if dt_value else "--:--"
        info = QtWidgets.QLabel(f"<b style='color:{color}'>{start} - {end}</b><br><b>{appt.get('patient_name')}</b> - {appt.get('gender', 'Nam')}, {appt.get('age', 35)} tuổi<br>{appt.get('service_name')}")
        info.setMinimumHeight(52)
        info.setStyleSheet("border: none; background: transparent; color: #334155; font-size: 13px;")
        badge = QtWidgets.QLabel(label)
        badge.setMinimumWidth(108)
        badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(f"background: {color}18; color: {color}; border: none; border-radius: 10px; padding: 5px 12px; font-weight: 900;")
        layout.addWidget(info, 1)
        layout.addWidget(badge)
        card.mousePressEvent = lambda event, a=appt: self._select_schedule(a)
        return card

    def _select_schedule(self, appt):
        self.selected_schedule = appt
        label, _, _ = self.STATUS_META.get(str(appt.get("status") or "pending"), self.STATUS_META["pending"])
        self.detail_patient.setText(
            f"👤  {appt.get('patient_name')}   {appt.get('gender', 'Nam')}\n"
            f"{appt.get('age', 35)} tuổi  •  {appt.get('patient_phone', '0987 654 321')}\n"
            f"Mã BN: BN{int(appt.get('patient_id') or 123):06d}"
        )
        dt_value = self._to_datetime(appt.get("appointment_date"))
        time_text = dt_value.strftime("%H:%M") if dt_value else "--:--"
        self.detail_info.setText(
            f"⏱ Thời gian                         {time_text} - {((dt_value + timedelta(minutes=30)).strftime('%H:%M') if dt_value else '--:--')}\n"
            f"🩺 Dịch vụ                           {appt.get('service_name')}\n"
            f"📍 Phòng khám                        {appt.get('room', 'Phòng khám 1')}\n"
            f"● Trạng thái                         {label}\n"
            f"📝 Ghi chú                            {appt.get('note') or 'Không có'}"
        )

    def _build_month_card(self):
        card = QtWidgets.QFrame()
        card.setMaximumHeight(330)
        card.setStyleSheet("background: #ffffff; border: 1px solid #e7edf5; border-radius: 14px;")
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        title = QtWidgets.QLabel("‹              Lịch tháng 5, 2026              ›")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 14px; font-weight: 900;")
        layout.addWidget(title)
        grid = QtWidgets.QGridLayout()
        for col, day_name in enumerate(["T2", "T3", "T4", "T5", "T6", "T7", "CN"]):
            grid.addWidget(QtWidgets.QLabel(day_name, alignment=QtCore.Qt.AlignmentFlag.AlignCenter), 0, col)
        nums = [28, 29, 30, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 1]
        for idx, num in enumerate(nums):
            label = QtWidgets.QLabel(str(num), alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            label.setFixedSize(34, 30)
            label.setStyleSheet("background: #13a66b; color: white; border-radius: 15px; font-weight: 900;" if num == 23 else "border: none; color: #334155; font-weight: 800;")
            grid.addWidget(label, idx // 7 + 1, idx % 7)
        layout.addLayout(grid)
        return card

    def add_new(self):
        QtWidgets.QMessageBox.information(self, "Thêm lịch khám", "Mở form thêm lịch khám cho bác sĩ.")

    def _start_selected_exam(self):
        if not self.selected_schedule:
            return
        self.selected_schedule["status"] = "in_progress"
        try:
            AppointmentController.update_status(self.selected_schedule.get("appointment_id"), "in_progress")
        except Exception:
            pass
        self._apply_filters()

    def _view_selected_patient(self):
        if self.selected_schedule:
            QtWidgets.QMessageBox.information(self, "Hồ sơ bệnh nhân", f"Mở hồ sơ của {self.selected_schedule.get('patient_name')}.")

    def _edit_selected_appointment(self):
        if self.selected_schedule:
            QtWidgets.QMessageBox.information(self, "Chỉnh sửa lịch", f"Mở chỉnh sửa lịch #{self.selected_schedule.get('appointment_id')}.")

    def _cancel_selected_appointment(self):
        if not self.selected_schedule:
            return
        self.selected_schedule["status"] = "cancelled"
        try:
            AppointmentController.update_status(self.selected_schedule.get("appointment_id"), "cancelled")
        except Exception:
            pass
        self._apply_filters()
