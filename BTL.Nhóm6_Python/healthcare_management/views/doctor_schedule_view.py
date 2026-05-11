from datetime import datetime, timedelta

from PyQt6 import QtCore, QtGui, QtWidgets

from controllers.appointment_controller import AppointmentController


class DoctorScheduleView(QtWidgets.QWidget):
    STATUS_META = {
        "done": ("Đã khám", "#16a34a", "#ecfdf5"),
        "in_progress": ("Đang khám", "#2563eb", "#eff6ff"),
        "confirmed": ("Đang chờ", "#f59e0b", "#fff7ed"),
        "pending": ("Đã đặt lịch", "#64748b", "#f8fafc"),
        "cancelled": ("Đã hủy", "#ef4444", "#fef2f2"),
    }

    STATUS_ORDER = ["done", "in_progress", "confirmed", "cancelled", "pending"]

    def __init__(self, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        self.role = "doctor"
        self.selected_schedule = None
        self._syncing_calendar = False
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

        self._select_initial_date_with_data()
        self._apply_filters()

    def _build_header(self):
        header = QtWidgets.QHBoxLayout()
        title_col = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("Lịch khám")
        title.setStyleSheet("border: none; background: transparent; font-size: 25px; color: #0f172a; font-weight: 900;")
        crumb = QtWidgets.QLabel("Trang chủ  >  Lịch khám")
        crumb.setStyleSheet("border: none; background: transparent; font-size: 14px; color: #64748b; font-weight: 700;")
        title_col.addWidget(title)
        title_col.addWidget(crumb)
        header.addLayout(title_col, 1)
        return header

    def _build_filter_bar(self):
        card = QtWidgets.QFrame()
        card.setStyleSheet("background: #ffffff; border: 1px solid #e7edf5; border-radius: 14px;")
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(12)

        prev_btn = self._small_button("<")
        next_btn = self._small_button(">")
        today_btn = self._small_button("Hôm nay", 116)
        self.date_input = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        self.date_input.setMinimumWidth(148)

        self.status_filter = QtWidgets.QComboBox()
        self.status_filter.addItem("Tất cả trạng thái", None)
        for status in ["done", "in_progress", "confirmed", "pending", "cancelled"]:
            self.status_filter.addItem(self.STATUS_META[status][0], status)

        self.service_filter = QtWidgets.QComboBox()
        self.service_filter.addItem("Tất cả dịch vụ", None)
        self.room_filter = QtWidgets.QComboBox()
        self.room_filter.addItem("Tất cả phòng khám", None)

        for row in self.all_rows:
            service = str(row.get("service_name") or "").strip()
            room = str(row.get("room") or "").strip()
            if service and self.service_filter.findData(service) < 0:
                self.service_filter.addItem(service, service)
            if room and self.room_filter.findData(room) < 0:
                self.room_filter.addItem(room, room)

        for widget in [self.date_input, self.status_filter, self.service_filter, self.room_filter]:
            widget.setStyleSheet(self._input_style())
            widget.setMinimumHeight(42)
        for combo in [self.status_filter, self.service_filter, self.room_filter]:
            combo.setMinimumWidth(170)

        self.date_input.dateChanged.connect(self._on_date_input_changed)
        self.status_filter.currentIndexChanged.connect(self._apply_filters)
        self.service_filter.currentIndexChanged.connect(self._apply_filters)
        self.room_filter.currentIndexChanged.connect(self._apply_filters)
        today_btn.clicked.connect(lambda: self.date_input.setDate(QtCore.QDate.currentDate()))
        prev_btn.clicked.connect(lambda: self.date_input.setDate(self.date_input.date().addDays(-1)))
        next_btn.clicked.connect(lambda: self.date_input.setDate(self.date_input.date().addDays(1)))

        for widget in [prev_btn, self.date_input, next_btn, today_btn, self.status_filter, self.service_filter, self.room_filter]:
            layout.addWidget(widget)
        layout.addStretch()
        add_btn = QtWidgets.QPushButton("+ Thêm lịch khám")
        add_btn.setMinimumHeight(44)
        add_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        add_btn.setStyleSheet(
            "QPushButton { background: #16B364; color: white; border: none; border-radius: 10px; "
            "padding: 0 18px; font-size: 14px; font-weight: 800; }"
            "QPushButton:hover { background: #12A061; }"
        )
        add_btn.clicked.connect(self._add_appointment)
        layout.addWidget(add_btn)
        return card

    def _build_timeline_card(self):
        card = QtWidgets.QFrame()
        card.setStyleSheet("background: #ffffff; border: 1px solid #e7edf5; border-radius: 14px;")
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(22, 20, 22, 20)
        top = QtWidgets.QHBoxLayout()
        self.timeline_title = QtWidgets.QLabel("")
        self.timeline_title.setStyleSheet("border: none; background: transparent; font-size: 18px; color: #0f172a; font-weight: 900;")
        top.addWidget(self.timeline_title, 1)
        for status in self.STATUS_ORDER:
            label, color, _ = self.STATUS_META[status]
            top.addWidget(self._legend(label, color))
        layout.addLayout(top)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll.setStyleSheet(self._scrollbar_style())
        timeline_body = QtWidgets.QWidget()
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
        self.detail_patient.setMinimumHeight(96)
        self.detail_patient.setWordWrap(True)
        self.detail_patient.setStyleSheet("background: #f8fafc; border: 1px solid #e7edf5; border-radius: 10px; padding: 12px; color: #0f172a; font-size: 13px; font-weight: 800;")
        self.detail_info = QtWidgets.QLabel("Chọn một lịch trong timeline để xem chi tiết.")
        self.detail_info.setMinimumHeight(150)
        self.detail_info.setWordWrap(True)
        self.detail_info.setStyleSheet("border: none; background: transparent; color: #334155; font-size: 13px; font-weight: 800;")
        layout.addWidget(title)
        layout.addWidget(self.detail_patient)
        layout.addWidget(self.detail_info)

        self.start_btn = self._detail_button("Bắt đầu khám", self._primary_style(), self._start_selected_exam)
        self.patient_btn = self._detail_button("Xem hồ sơ bệnh nhân", self._outline_style("#475569"), self._view_selected_patient)
        self.edit_btn = self._detail_button("Chỉnh sửa lịch", self._outline_style("#475569"), self._edit_selected_appointment)
        self.cancel_btn = self._detail_button("Hủy lịch khám", self._outline_style("#ef4444"), self._cancel_selected_appointment)

        for btn in [self.start_btn, self.patient_btn, self.edit_btn, self.cancel_btn]:
            layout.addWidget(btn)
        return card

    def _build_month_card(self):
        self.calendar = QtWidgets.QCalendarWidget()
        self.calendar.setMaximumHeight(330)
        self.calendar.setSelectedDate(self.date_input.date())
        self.calendar.setStyleSheet(
            "QCalendarWidget { background: white; border: 1px solid #EAECF0; border-radius: 14px; color: #344054; }"
            "QCalendarWidget QWidget#qt_calendar_navigationbar { background: white; border: none; }"
            "QCalendarWidget QToolButton { color: #101828; background: white; border: none; font-weight: 800; padding: 6px; }"
            "QCalendarWidget QAbstractItemView { selection-background-color: #16B364; selection-color: white; "
            "outline: none; border: none; font-size: 13px; }"
        )
        self.calendar.selectionChanged.connect(self._on_calendar_changed)
        return self.calendar

    def _input_style(self):
        return "background: #ffffff; border: 1px solid #dbe4ee; border-radius: 8px; padding: 9px 12px; color: #0f172a; font-weight: 800;"

    def _primary_style(self):
        return "QPushButton { background: #13a66b; color: #ffffff; border: none; border-radius: 9px; padding: 11px 16px; font-weight: 900; } QPushButton:disabled { background: #cbd5e1; color: #ffffff; }"

    def _outline_style(self, color):
        return f"QPushButton {{ background: #ffffff; color: {color}; border: 1px solid #dbe4ee; border-radius: 9px; padding: 11px 16px; font-weight: 900; }} QPushButton:disabled {{ color: #94a3b8; border-color: #e2e8f0; }}"

    def _scrollbar_style(self):
        return (
            "QScrollArea { border: none; background: transparent; }"
            "QScrollBar:vertical { background: transparent; width: 8px; margin: 2px 0; }"
            "QScrollBar::handle:vertical { background: #cbd5e1; border-radius: 4px; min-height: 36px; }"
            "QScrollBar::handle:vertical:hover { background: #94a3b8; }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def _small_button(self, text, width=46):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedSize(width, 42)
        btn.setStyleSheet(self._outline_style("#475569"))
        return btn

    def _detail_button(self, text, style, callback):
        btn = QtWidgets.QPushButton(text)
        btn.setMinimumHeight(44)
        btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        btn.setStyleSheet(style)
        btn.clicked.connect(callback)
        return btn

    def _legend(self, text, color):
        label = QtWidgets.QLabel(f"● {text}")
        label.setStyleSheet(f"border: none; background: transparent; color: {color}; font-size: 12px; font-weight: 900;")
        return label

    def _build_schedule_rows(self):
        try:
            rows = AppointmentController.get_management_rows_by_doctor(self.doctor_id) or []
        except Exception:
            rows = []

        catalog = []
        for idx, row in enumerate(rows):
            item = dict(row)
            item["room"] = item.get("room") or "Phòng khám 1"
            item["service_name"] = item.get("service_name") or self._extract_service(item.get("note"))
            item["gender"] = item.get("gender") or ("Nam" if idx % 2 == 0 else "Nữ")
            item["age"] = item.get("age") or self._estimate_age(item.get("date_of_birth")) or ""
            item["patient_phone"] = item.get("patient_phone") or item.get("phone") or "Chưa cập nhật"
            item["patient_name"] = item.get("patient_name") or "Chưa có tên"
            item["status"] = item.get("status") or "pending"
            catalog.append(item)
        return catalog

    def _extract_service(self, note):
        text = str(note or "")
        if text.startswith("Dịch vụ:"):
            return text.replace("Dịch vụ:", "", 1).split("|", 1)[0].strip() or "Khám tổng quát"
        return text or "Khám tổng quát"

    def _estimate_age(self, date_of_birth):
        if not date_of_birth:
            return None
        try:
            born = datetime.fromisoformat(str(date_of_birth)).date()
        except ValueError:
            return None
        today = datetime.now().date()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def _to_datetime(self, value):
        if isinstance(value, datetime):
            return value
        text = str(value or "").strip()
        if not text:
            return None
        try:
            return datetime.fromisoformat(text.replace("Z", "+00:00")).replace(tzinfo=None)
        except ValueError:
            pass
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M"):
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                continue
        return None

    def _select_initial_date_with_data(self):
        today = QtCore.QDate.currentDate()
        available_dates = []
        for row in self.all_rows:
            dt_value = self._to_datetime(row.get("appointment_date"))
            if dt_value:
                available_dates.append(dt_value.date())
        if not available_dates or today.toPyDate() in available_dates:
            return

        selected = min(available_dates, key=lambda d: abs((d - today.toPyDate()).days))
        self.date_input.setDate(QtCore.QDate(selected.year, selected.month, selected.day))

    def _on_date_input_changed(self):
        if self._syncing_calendar:
            return
        if hasattr(self, "calendar") and not self._syncing_calendar:
            self._syncing_calendar = True
            self.calendar.setSelectedDate(self.date_input.date())
            self._syncing_calendar = False
        self._apply_filters()

    def _on_calendar_changed(self):
        if self._syncing_calendar:
            return
        self._syncing_calendar = True
        self.date_input.setDate(self.calendar.selectedDate())
        self._syncing_calendar = False
        self._apply_filters()

    def _apply_filters(self):
        selected_date = self.date_input.date().toPyDate()
        status_key = self.status_filter.currentData()
        service_key = self.service_filter.currentData()
        room_key = self.room_filter.currentData()
        filtered = []
        for row in self.all_rows:
            dt_value = self._to_datetime(row.get("appointment_date"))
            if not dt_value or dt_value.date() != selected_date:
                continue
            if status_key and str(row.get("status") or "") != status_key:
                continue
            if service_key and str(row.get("service_name") or "") != service_key:
                continue
            if room_key and str(row.get("room") or "") != room_key:
                continue
            filtered.append(row)
        filtered.sort(key=lambda r: self._to_datetime(r.get("appointment_date")) or datetime.max)
        self.filtered_rows = filtered
        count_text = f"{len(filtered)} lịch" if filtered else "Không có lịch"
        self.timeline_title.setText(f"Lịch khám trong ngày - {self.date_input.date().toString('dd/MM/yyyy')} ({count_text})")
        self._render_timeline()

    def _render_timeline(self):
        while self.timeline_list.count():
            item = self.timeline_list.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        grouped = {hour: [] for hour in range(7, 18)}
        for appt in self.filtered_rows:
            dt_value = self._to_datetime(appt.get("appointment_date"))
            if dt_value and dt_value.hour in grouped:
                grouped[dt_value.hour].append(appt)

        for hour in range(7, 18):
            row = QtWidgets.QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(10)
            hour_lbl = QtWidgets.QLabel(f"{hour:02d}:00")
            hour_lbl.setFixedWidth(84)
            hour_lbl.setStyleSheet("border: none; background: transparent; color: #334155; font-size: 15px; font-weight: 900;")
            row.addWidget(hour_lbl)

            matches = grouped[hour]
            slot = QtWidgets.QWidget()
            slot_layout = QtWidgets.QVBoxLayout(slot)
            slot_layout.setContentsMargins(0, 0, 0, 0)
            slot_layout.setSpacing(6)
            if matches:
                for appt in matches:
                    slot_layout.addWidget(self._appointment_block(appt))
            else:
                slot_layout.addWidget(self._empty_slot())

            row.addWidget(slot, 1)
            holder = QtWidgets.QWidget()
            holder.setMinimumHeight(max(56, len(matches) * 78 if matches else 56))
            holder.setLayout(row)
            self.timeline_list.addWidget(holder)

        self.timeline_list.addStretch()
        if self.filtered_rows:
            self._select_schedule(self.filtered_rows[0])
        else:
            self.selected_schedule = None
            self.detail_patient.setText("Chưa có lịch khám")
            self.detail_info.setText("Không có lịch khám phù hợp với ngày và bộ lọc đang chọn.")
            self._update_action_buttons(None)

    def _empty_slot(self):
        empty = QtWidgets.QFrame()
        empty.setFixedHeight(48)
        empty.setStyleSheet("background: transparent; border-bottom: 1px solid #edf2f7;")
        return empty

    def _appointment_block(self, appt):
        status = str(appt.get("status") or "pending")
        label, color, bg = self.STATUS_META.get(status, self.STATUS_META["pending"])
        card = QtWidgets.QFrame()
        card.setFixedHeight(72)
        card.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        card.setStyleSheet(f"background: {bg}; border: 1px solid {color}55; border-left: 3px solid {color}; border-radius: 9px;")
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(16, 8, 12, 8)
        dt_value = self._to_datetime(appt.get("appointment_date"))
        start = dt_value.strftime("%H:%M") if dt_value else "--:--"
        end = (dt_value + timedelta(minutes=30)).strftime("%H:%M") if dt_value else "--:--"
        gender_age = self._gender_age_text(appt)
        info = QtWidgets.QLabel(
            f"<b>{appt.get('patient_name', '')}</b> - {gender_age}<br>"
            f"{appt.get('service_name', '')}<br>"
            f"{start} - {end} · {appt.get('room', 'Phòng khám 1')}"
        )
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
        label, color, bg = self.STATUS_META.get(str(appt.get("status") or "pending"), self.STATUS_META["pending"])
        dt_value = self._to_datetime(appt.get("appointment_date"))
        start = dt_value.strftime("%H:%M") if dt_value else "--:--"
        end = (dt_value + timedelta(minutes=30)).strftime("%H:%M") if dt_value else "--:--"
        patient_id = int(appt.get("patient_id") or 0)
        self.detail_patient.setText(
            f"👤 {appt.get('patient_name', '')}\n"
            f"{self._gender_age_text(appt)} · {appt.get('patient_phone', 'Chưa cập nhật')}\n"
            f"Mã BN: BN{patient_id:06d}"
        )
        self.detail_info.setText(
            f"⏱ Thời gian: {start} - {end}\n"
            f"🩺 Dịch vụ: {appt.get('service_name')}\n"
            f"🏥 Phòng khám: {appt.get('room', 'Phòng khám 1')}\n"
            f"● Trạng thái: {label}\n"
            f"📝 Ghi chú: {appt.get('note') or 'Không có'}"
        )
        self.detail_info.setStyleSheet(f"border: none; background: transparent; color: #334155; font-size: 13px; font-weight: 800;")
        self.detail_patient.setStyleSheet(f"background: {bg}; border: 1px solid {color}55; border-radius: 10px; padding: 12px; color: #0f172a; font-size: 13px; font-weight: 800;")
        self._update_action_buttons(str(appt.get("status") or "pending"))

    def _gender_age_text(self, appt):
        gender = appt.get("gender") or "Chưa cập nhật"
        age = appt.get("age")
        age_text = f"{age} tuổi" if age not in (None, "") else "Chưa cập nhật tuổi"
        return f"{gender}, {age_text}"

    def _update_action_buttons(self, status):
        has_selection = bool(self.selected_schedule)
        can_start = has_selection and status not in {"done", "cancelled"}
        can_cancel = has_selection and status != "done" and status != "cancelled"
        self.start_btn.setEnabled(can_start)
        self.cancel_btn.setEnabled(can_cancel)
        self.patient_btn.setEnabled(has_selection)
        self.edit_btn.setEnabled(has_selection)
        self.start_btn.setText("Tiếp tục khám" if status == "in_progress" else "Bắt đầu khám")

    def _controller_success(self, result):
        if isinstance(result, dict):
            return bool(result.get("status"))
        return bool(result)

    def _start_selected_exam(self):
        if not self.selected_schedule:
            return
        current_status = str(self.selected_schedule.get("status") or "")
        if current_status in {"done", "cancelled"}:
            QtWidgets.QMessageBox.warning(self, "Không thể bắt đầu khám", "Lịch khám đã hoàn tất hoặc đã hủy.")
            return

        appointment_id = self.selected_schedule.get("appointment_id")
        if current_status != "in_progress":
            result = AppointmentController.update_status(appointment_id, "in_progress")
            if not self._controller_success(result):
                QtWidgets.QMessageBox.warning(self, "Không thể bắt đầu khám", "Cập nhật trạng thái lịch khám thất bại.")
                return
            self.selected_schedule["status"] = "in_progress"

        dashboard = self._find_dashboard()
        if dashboard:
            exam_page = getattr(dashboard, "page_medical_record", None)
            if hasattr(exam_page, "set_appointment"):
                exam_page.set_appointment(appointment_id)
            dashboard.switch_page(3)
        self.all_rows = self._build_schedule_rows()
        self._apply_filters()

    def _view_selected_patient(self):
        if not self.selected_schedule:
            return
        dashboard = self._find_dashboard()
        if dashboard:
            profile = getattr(dashboard, "page_patient_record", None)
            if hasattr(profile, "set_patient"):
                profile.set_patient(self.selected_schedule.get("patient_id"))
            dashboard.switch_page(4)

    def _add_appointment(self):
        try:
            from views.doctor_management_views import AppointmentUpsertDialog

            dialog = AppointmentUpsertDialog(self.doctor_id, parent=self)
            if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
                return
            payload = dialog.get_payload()
            result = AppointmentController.create_with_details(
                payload.get("patient_id"),
                payload.get("doctor_id"),
                payload.get("date"),
                payload.get("time"),
                payload.get("status"),
                payload.get("service_name") or "Khám tổng quát",
                payload.get("note"),
            )
            if not result.get("status"):
                QtWidgets.QMessageBox.warning(self, "Không thể tạo lịch", result.get("message", "Lỗi không xác định"))
                return
            self.all_rows = self._build_schedule_rows()
            self._apply_filters()
        except Exception as exc:
            QtWidgets.QMessageBox.warning(self, "Không thể tạo lịch", str(exc))

    def _edit_selected_appointment(self):
        if not self.selected_schedule:
            return
        try:
            from views.doctor_management_views import AppointmentUpsertDialog

            detail = AppointmentController.get_by_id(self.selected_schedule.get("appointment_id"))
            if not detail:
                return
            dialog = AppointmentUpsertDialog(self.doctor_id, appointment=detail, parent=self)
            if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
                return
            payload = dialog.get_payload()
            result = AppointmentController.update_full(
                detail.get("appointment_id"),
                payload.get("patient_id"),
                payload.get("doctor_id"),
                payload.get("date"),
                payload.get("time"),
                payload.get("status"),
                payload.get("service_name"),
                payload.get("note"),
            )
            if not result.get("status"):
                QtWidgets.QMessageBox.warning(self, "Không thể cập nhật", result.get("message", "Lỗi không xác định"))
                return
            self.all_rows = self._build_schedule_rows()
            self._apply_filters()
        except Exception as exc:
            QtWidgets.QMessageBox.warning(self, "Không thể chỉnh sửa", str(exc))

    def _cancel_selected_appointment(self):
        if not self.selected_schedule:
            return
        current_status = str(self.selected_schedule.get("status") or "")
        if current_status in {"done", "cancelled"}:
            QtWidgets.QMessageBox.warning(self, "Không thể hủy lịch", "Lịch khám đã hoàn tất hoặc đã hủy.")
            return

        result = AppointmentController.update_status(self.selected_schedule.get("appointment_id"), "cancelled")
        if not self._controller_success(result):
            QtWidgets.QMessageBox.warning(self, "Không thể hủy lịch", "Cập nhật trạng thái lịch khám thất bại.")
            return

        self.selected_schedule["status"] = "cancelled"
        self.all_rows = self._build_schedule_rows()
        self._apply_filters()

    def _find_dashboard(self):
        parent = self.parent()
        while parent and not hasattr(parent, "content_stack"):
            parent = parent.parent()
        return parent
