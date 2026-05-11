from PyQt6 import QtWidgets, QtCore, QtGui


class DoctorPatientRecordView(QtWidgets.QWidget):
    def __init__(self, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        self.setStyleSheet("background: #f8fbff; border: none;")

        self.patient = {
            "name": "Nguyễn Văn Nam",
            "gender": "Nam",
            "meta": "35 tuổi (15/02/1990)  -  Mã BN: BN000123",
            "phone": "0987 654 321",
            "email": "nam.nguyen@gmail.com",
            "address": "123 Đường Lê Lợi, P.1, Q.1, TP.HCM",
            "blood_type": "O+",
            "job": "Nhân viên văn phòng",
            "insurance": "Có (BHYT)",
            "contact_name": "Nguyễn Thị Lan (Vợ)",
            "contact_phone": "0988 111 222",
            "note": (
                "Bệnh nhân có tiền sử đau dạ dày.\n"
                "Cần nhắc nhở kiêng đồ cay nóng."
            ),
        }
        self.tabs = [
            "Lịch sử khám",
            "Thông tin cá nhân",
            "Bệnh sử",
            "Kết quả xét nghiệm",
            "Đơn thuốc",
            "Chỉ định",
            "Tài liệu đính kèm",
        ]
        self.history_items = [
            {
                "datetime": "23/05/2026 - 09:00",
                "doctor": "Phòng khám 1 - Bác sĩ Minh",
                "reason": "Khám tổng quát",
                "status": "Đã hoàn tất",
                "selected": True,
                "cancelled": False,
            },
            {
                "datetime": "18/05/2026 - 10:30",
                "doctor": "Phòng khám 1 - Bác sĩ Minh",
                "reason": "Đau mỏi vai gáy",
                "status": "Đã hoàn tất",
                "selected": False,
                "cancelled": False,
            },
            {
                "datetime": "10/04/2026 - 14:00",
                "doctor": "Phòng khám 1 - Bác sĩ Minh",
                "reason": "Khám tai mũi họng",
                "status": "Đã hoàn tất",
                "selected": False,
                "cancelled": False,
            },
            {
                "datetime": "15/02/2026 - 11:15",
                "doctor": "Phòng khám 1 - Bác sĩ Minh",
                "reason": "Mệt mỏi, khó ngủ",
                "status": "Đã hoàn tất",
                "selected": False,
                "cancelled": False,
            },
            {
                "datetime": "20/12/2025 - 08:30",
                "doctor": "Phòng khám 1 - Bác sĩ Minh",
                "reason": "Khám tổng quát",
                "status": "Đã hủy",
                "selected": False,
                "cancelled": True,
            },
        ]
        self.summary_rows = [
            ("Tổng số lần khám", "12"),
            ("Tổng đơn thuốc", "9"),
            ("Tổng xét nghiệm", "5"),
            ("Tổng chỉ định", "4"),
            ("Tài liệu đính kèm", "3"),
        ]
        self.vital_rows = [
            ("Mạch", "78 lần/phút"),
            ("Huyết áp", "120/80 mmHg"),
            ("Nhiệt độ", "36.7 °C"),
            ("Nhịp thở", "18 lần/phút"),
            ("Cân nặng", "65 kg"),
            ("Chiều cao", "170 cm"),
        ]

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")

        page = QtWidgets.QWidget()
        page.setStyleSheet("background: transparent;")
        page_layout = QtWidgets.QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 16)
        page_layout.setSpacing(18)
        page_layout.addLayout(self._build_header())
        page_layout.addWidget(self._build_profile_card())
        page_layout.addWidget(self._build_tabs_card())

        content_row = QtWidgets.QHBoxLayout()
        content_row.setSpacing(18)
        content_row.addWidget(self._build_history_panel(), 31)
        content_row.addWidget(self._build_detail_panel(), 43)
        content_row.addWidget(self._build_sidebar_panel(), 26)
        page_layout.addLayout(content_row)

        scroll.setWidget(page)
        root.addWidget(scroll)

    def _build_header(self):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(14)

        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(5)

        title = QtWidgets.QLabel("Hồ sơ bệnh nhân")
        title.setStyleSheet(
            "color: #0f172a; font-size: 25px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        crumb = QtWidgets.QLabel("Trang chủ  ›  Hồ sơ bệnh nhân  ›  Chi tiết hồ sơ")
        crumb.setStyleSheet(
            "color: #7d8ca2; font-size: 14px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        title_col.addWidget(title)
        title_col.addWidget(crumb)
        row.addLayout(title_col, 1)

        row.addWidget(self._build_notification_widget())

        avatar = QtWidgets.QLabel("👨")
        avatar.setFixedSize(44, 44)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            "background: #eef3fb; border-radius: 22px; color: #1d4ed8; "
            "font-size: 22px; border: none;"
        )
        row.addWidget(avatar)

        name = QtWidgets.QLabel("Bác sĩ Minh")
        name.setStyleSheet(
            "color: #0f172a; font-size: 14px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        row.addWidget(name)

        caret = QtWidgets.QLabel("▾")
        caret.setStyleSheet(
            "color: #64748b; font-size: 14px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        row.addWidget(caret)
        return row

    def _build_notification_widget(self):
        wrapper = QtWidgets.QFrame()
        wrapper.setFixedSize(40, 40)
        wrapper.setStyleSheet("background: transparent; border: none;")

        icon = QtWidgets.QLabel("🔔", wrapper)
        icon.setGeometry(6, 7, 26, 26)
        icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet(
            "background: transparent; border: none; color: #64748b; font-size: 18px;"
        )

        badge = QtWidgets.QLabel("2", wrapper)
        badge.setGeometry(20, 0, 18, 18)
        badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            "background: #ff3b30; color: white; border-radius: 9px; "
            "font-size: 10px; font-weight: 900; border: none;"
        )
        return wrapper

    def _build_profile_card(self):
        card = self._card()
        card_layout = QtWidgets.QHBoxLayout(card)
        card_layout.setContentsMargins(20, 18, 20, 18)
        card_layout.setSpacing(0)

        card_layout.addWidget(self._build_profile_main(), 39)
        card_layout.addWidget(self._build_vertical_separator())
        card_layout.addWidget(self._build_profile_details(), 25)
        card_layout.addWidget(self._build_vertical_separator())
        card_layout.addWidget(self._build_profile_note(), 24)
        return card

    def _build_profile_main(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 18, 0)
        layout.setSpacing(16)

        avatar = QtWidgets.QLabel("👨")
        avatar.setFixedSize(86, 86)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            "background: #edf3fb; border-radius: 43px; color: #1d4ed8; "
            "font-size: 42px; border: none;"
        )
        layout.addWidget(avatar, 0, QtCore.Qt.AlignmentFlag.AlignTop)

        info = QtWidgets.QVBoxLayout()
        info.setSpacing(10)

        name_row = QtWidgets.QHBoxLayout()
        name_row.setSpacing(10)

        name = QtWidgets.QLabel(self.patient["name"])
        name.setStyleSheet(
            "color: #0f172a; font-size: 20px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        gender = QtWidgets.QLabel(self.patient["gender"])
        gender.setStyleSheet(
            "background: #eef4ff; color: #4c88ff; border-radius: 12px; "
            "padding: 5px 12px; font-size: 12px; font-weight: 900; border: none;"
        )
        name_row.addWidget(name)
        name_row.addWidget(gender, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        name_row.addStretch()

        meta = QtWidgets.QLabel(self.patient["meta"])
        meta.setStyleSheet(
            "color: #6b7a90; font-size: 13px; font-weight: 700; "
            "background: transparent; border: none;"
        )

        contact_row = QtWidgets.QHBoxLayout()
        contact_row.setSpacing(22)
        contact_row.addWidget(self._icon_text("☎", self.patient["phone"]))
        contact_row.addWidget(self._icon_text("✉", self.patient["email"]))
        contact_row.addStretch()

        address = self._icon_text("⌖", self.patient["address"])
        address.setWordWrap(True)

        info.addLayout(name_row)
        info.addWidget(meta)
        info.addLayout(contact_row)
        info.addWidget(address)

        layout.addLayout(info, 1)
        return widget

    def _build_profile_details(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        layout.setContentsMargins(22, 8, 22, 8)
        layout.setHorizontalSpacing(18)
        layout.setVerticalSpacing(14)

        rows = [
            ("Nhóm máu:", self.patient["blood_type"]),
            ("Nghề nghiệp:", self.patient["job"]),
            ("Bảo hiểm:", self.patient["insurance"]),
            ("Người liên hệ:", f"{self.patient['contact_name']}\n{self.patient['contact_phone']}"),
        ]
        for row_index, (label_text, value_text) in enumerate(rows):
            label = QtWidgets.QLabel(label_text)
            label.setStyleSheet(
                "color: #6b7a90; font-size: 13px; font-weight: 800; "
                "background: transparent; border: none;"
            )
            value = QtWidgets.QLabel(value_text)
            value.setWordWrap(True)
            value.setStyleSheet(
                "color: #334155; font-size: 13px; font-weight: 900; "
                "background: transparent; border: none;"
            )
            layout.addWidget(label, row_index, 0, QtCore.Qt.AlignmentFlag.AlignTop)
            layout.addWidget(value, row_index, 1)
        layout.setColumnStretch(1, 1)
        return widget

    def _build_profile_note(self):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(22, 8, 0, 0)
        layout.setSpacing(12)

        header = QtWidgets.QHBoxLayout()

        title = QtWidgets.QLabel("Ghi chú")
        title.setStyleSheet(
            "color: #1e293b; font-size: 15px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        edit_btn = QtWidgets.QPushButton("✎")
        edit_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        edit_btn.setStyleSheet(
            "QPushButton { background: transparent; color: #2f80ff; border: none; "
            "font-size: 18px; font-weight: 900; }"
        )
        header.addWidget(title)
        header.addStretch()
        header.addWidget(edit_btn)

        note_box = QtWidgets.QFrame()
        note_box.setStyleSheet(
            "background: white; border: 1px solid #e6edf6; border-radius: 14px;"
        )
        note_layout = QtWidgets.QVBoxLayout(note_box)
        note_layout.setContentsMargins(18, 16, 18, 16)
        note = QtWidgets.QLabel(self.patient["note"])
        note.setWordWrap(True)
        note.setStyleSheet(
            "color: #526176; font-size: 13px; font-weight: 700; "
            "background: transparent; border: none; line-height: 1.5;"
        )
        note_layout.addWidget(note)
        layout.addLayout(header)
        layout.addWidget(note_box)
        return wrapper

    def _build_tabs_card(self):
        card = self._card()
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(26)

        for index, tab_text in enumerate(self.tabs):
            button = QtWidgets.QPushButton(tab_text)
            button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            button.setFlat(True)
            button.setMinimumHeight(64)
            button.setStyleSheet(
                "QPushButton { background: transparent; color: #10b981; border: none; "
                "border-bottom: 3px solid #10b981; font-size: 14px; font-weight: 900; "
                "padding: 0 4px; text-align: center; }"
                if index == 0 else
                "QPushButton { background: transparent; color: #64748b; border: none; "
                "font-size: 14px; font-weight: 800; padding: 0 4px; text-align: center; }"
            )
            layout.addWidget(button, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        layout.addStretch()
        return card

    def _build_history_panel(self):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        tools = QtWidgets.QHBoxLayout()
        tools.setSpacing(10)

        search = QtWidgets.QLineEdit()
        search.setPlaceholderText("Tìm kiếm lịch sử khám...")
        search.setReadOnly(True)
        search.setMinimumHeight(44)
        search.setStyleSheet(
            "QLineEdit { background: white; color: #94a3b8; border: 1px solid #e4ebf5; "
            "border-radius: 12px; padding: 0 16px; font-size: 14px; font-weight: 700; }"
        )
        tools.addWidget(search, 1)

        filter_btn = self._icon_square_button("⚗", 44)
        tools.addWidget(filter_btn)
        layout.addLayout(tools)

        for item in self.history_items:
            layout.addWidget(self._build_history_item(item))

        view_all = QtWidgets.QPushButton("⌄  Xem tất cả lịch sử   ›")
        view_all.setMinimumHeight(52)
        view_all.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        view_all.setStyleSheet(
            "QPushButton { background: white; color: #2f80ff; border: 1px solid #e4ebf5; "
            "border-radius: 12px; font-size: 14px; font-weight: 900; }"
        )
        layout.addSpacing(2)
        layout.addWidget(view_all)
        return card

    def _build_history_item(self, item):
        frame = QtWidgets.QFrame()
        border_color = "#7ee7b2" if item["selected"] else "#edf2f7"
        background = "#f4fff8" if item["selected"] else "#ffffff"
        frame.setStyleSheet(
            f"background: {background}; border: 1px solid {border_color}; border-radius: 14px;"
        )

        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        top = QtWidgets.QHBoxLayout()
        top.setSpacing(10)

        date = QtWidgets.QLabel(item["datetime"])
        date.setStyleSheet(
            "color: #1e3a5f; font-size: 14px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        badge = QtWidgets.QLabel(item["status"])
        badge_bg = "#eafbf1" if not item["cancelled"] else "#e8f1ff"
        badge_fg = "#25b468" if not item["cancelled"] else "#5b92ff"
        badge.setStyleSheet(
            f"background: {badge_bg}; color: {badge_fg}; border-radius: 11px; "
            "padding: 4px 10px; font-size: 11px; font-weight: 900; border: none;"
        )
        top.addWidget(date)
        top.addStretch()
        top.addWidget(badge)

        doctor = QtWidgets.QLabel(item["doctor"])
        doctor.setStyleSheet(
            "color: #637289; font-size: 13px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        reason = QtWidgets.QLabel(item["reason"])
        reason.setStyleSheet(
            "color: #334155; font-size: 13px; font-weight: 700; "
            "background: transparent; border: none;"
        )

        layout.addLayout(top)
        layout.addWidget(doctor)
        layout.addWidget(reason)
        return frame

    def _build_detail_panel(self):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(16)

        header = QtWidgets.QHBoxLayout()
        header.setSpacing(10)

        title = QtWidgets.QLabel("Chi tiết lần khám - 23/05/2026 09:00")
        title.setStyleSheet(
            "color: #0f172a; font-size: 17px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        badge = QtWidgets.QLabel("Đã hoàn tất")
        badge.setStyleSheet(
            "background: #eafbf1; color: #23b067; border-radius: 11px; "
            "padding: 4px 10px; font-size: 11px; font-weight: 900; border: none;"
        )
        header.addWidget(title)
        header.addStretch()
        header.addWidget(badge)
        header.addWidget(self._icon_square_button("⎙", 34, "#ffffff", "#64748b", "#e6edf6"))
        header.addWidget(self._icon_square_button("⋮", 34, "#ffffff", "#64748b", "#e6edf6"))
        layout.addLayout(header)

        layout.addWidget(self._text_section("Lý do khám", "Khám tổng quát"))
        layout.addWidget(
            self._text_section(
                "Triệu chứng",
                "Đau đầu nhẹ, mệt mỏi, ăn uống bình thường.",
            )
        )

        clinical_title = QtWidgets.QLabel("Khám lâm sàng")
        clinical_title.setStyleSheet(
            "color: #0f172a; font-size: 15px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        layout.addWidget(clinical_title)
        layout.addWidget(self._build_vitals_grid())

        layout.addWidget(self._text_section("Chẩn đoán", "R51 - Đau đầu"))
        layout.addWidget(
            self._text_section(
                "Kết luận",
                "Bệnh nhân sức khỏe ổn định, không phát hiện bất thường.",
            )
        )
        layout.addWidget(
            self._text_section(
                "Hướng dẫn",
                "Nghỉ ngơi hợp lý, uống đủ nước, tái khám nếu triệu chứng kéo dài.",
            )
        )

        doctor_title = QtWidgets.QLabel("Bác sĩ khám")
        doctor_title.setStyleSheet(
            "color: #0f172a; font-size: 15px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        layout.addWidget(doctor_title)
        layout.addWidget(self._build_doctor_signature())
        layout.addStretch()
        return card

    def _build_vitals_grid(self):
        frame = QtWidgets.QFrame()
        frame.setStyleSheet(
            "background: white; border: 1px solid #e6edf6; border-radius: 12px;"
        )
        grid = QtWidgets.QGridLayout(frame)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)

        for index, (label_text, value_text) in enumerate(self.vital_rows):
            label = QtWidgets.QLabel(label_text)
            value = QtWidgets.QLabel(value_text)
            label.setMinimumHeight(46)
            value.setMinimumHeight(46)
            label.setStyleSheet(
                "background: #ffffff; color: #56657a; font-size: 13px; font-weight: 800; "
                "padding: 0 16px; border-right: 1px solid #e6edf6; border-bottom: 1px solid #e6edf6;"
            )
            value.setStyleSheet(
                "background: #ffffff; color: #334155; font-size: 13px; font-weight: 900; "
                "padding: 0 16px; border-bottom: 1px solid #e6edf6;"
            )
            if index % 2 == 1:
                label.setStyleSheet(
                    label.styleSheet().replace("border-right: 1px solid #e6edf6;", "")
                )
            if index >= 4:
                label.setStyleSheet(
                    label.styleSheet().replace("border-bottom: 1px solid #e6edf6;", "")
                )
                value.setStyleSheet(
                    value.styleSheet().replace("border-bottom: 1px solid #e6edf6;", "")
                )
            row = index // 2
            col = (index % 2) * 2
            grid.addWidget(label, row, col)
            grid.addWidget(value, row, col + 1)

        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)
        return frame

    def _build_doctor_signature(self):
        frame = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        avatar = QtWidgets.QLabel("👨")
        avatar.setFixedSize(38, 38)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            "background: #eef3fb; border-radius: 19px; color: #1d4ed8; "
            "font-size: 20px; border: none;"
        )
        name = QtWidgets.QLabel("Bác sĩ Minh")
        name.setStyleSheet(
            "color: #0f172a; font-size: 14px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        layout.addWidget(avatar)
        layout.addWidget(name)
        layout.addStretch()
        return frame

    def _build_sidebar_panel(self):
        wrapper = QtWidgets.QWidget()
        wrapper.setStyleSheet("background: transparent;")
        wrapper.setMinimumWidth(292)

        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        layout.addWidget(self._build_summary_card())
        layout.addWidget(self._build_info_box("Bệnh mãn tính", "Không có bệnh mãn tính."))
        layout.addWidget(self._build_info_box("Dị ứng", "Không ghi nhận dị ứng."))
        layout.addWidget(self._build_quick_actions_card())
        layout.addStretch()
        return wrapper

    def _build_summary_card(self):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(16)

        title = QtWidgets.QLabel("Tóm tắt hồ sơ")
        title.setStyleSheet(
            "color: #0f172a; font-size: 16px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        layout.addWidget(title)

        for label_text, value_text in self.summary_rows:
            row = QtWidgets.QHBoxLayout()
            row.setSpacing(10)
            icon = QtWidgets.QLabel("◧")
            icon.setStyleSheet(
                "color: #8aa0bb; font-size: 13px; background: transparent; border: none;"
            )
            label = QtWidgets.QLabel(label_text)
            label.setStyleSheet(
                "color: #6b7a90; font-size: 13px; font-weight: 700; "
                "background: transparent; border: none;"
            )
            value = QtWidgets.QLabel(value_text)
            value.setStyleSheet(
                "color: #1e293b; font-size: 13px; font-weight: 900; "
                "background: transparent; border: none;"
            )
            row.addWidget(icon)
            row.addWidget(label)
            row.addStretch()
            row.addWidget(value)
            layout.addLayout(row)
        return card

    def _build_info_box(self, title_text, body_text):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)

        header = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel(title_text)
        title.setStyleSheet(
            "color: #0f172a; font-size: 15px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        add_btn = self._icon_square_button("+", 34, "#ffffff", "#8aa0bb", "#e6edf6")
        header.addWidget(title)
        header.addStretch()
        header.addWidget(add_btn)

        body = QtWidgets.QLabel(body_text)
        body.setWordWrap(True)
        body.setStyleSheet(
            "color: #64748b; font-size: 13px; font-weight: 700; "
            "background: transparent; border: none;"
        )

        layout.addLayout(header)
        layout.addWidget(body)
        return card

    def _build_quick_actions_card(self):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        title = QtWidgets.QLabel("Thao tác nhanh")
        title.setStyleSheet(
            "color: #0f172a; font-size: 16px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        layout.addWidget(title)

        grid = QtWidgets.QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)
        actions = [
            ("＋  Tạo lịch hẹn", "#2f80ff"),
            ("⚕  Khám bệnh", "#23b067"),
            ("℞  Kê đơn thuốc", "#4f6bff"),
            ("⎙  In hồ sơ", "#23b067"),
        ]

        for index, (text, color) in enumerate(actions):
            button = QtWidgets.QPushButton(text)
            button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            button.setMinimumHeight(52)
            button.setStyleSheet(
                f"QPushButton {{ background: white; color: {color}; border: 1px solid #e6edf6; "
                "border-radius: 12px; font-size: 14px; font-weight: 900; text-align: left; padding: 0 18px; }}"
            )
            grid.addWidget(button, index // 2, index % 2)
        layout.addLayout(grid)
        return card

    def _text_section(self, title_text, body_text):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        title = QtWidgets.QLabel(title_text)
        title.setStyleSheet(
            "color: #0f172a; font-size: 15px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        body = QtWidgets.QLabel(body_text)
        body.setWordWrap(True)
        body.setStyleSheet(
            "color: #334155; font-size: 13px; font-weight: 700; "
            "background: transparent; border: none; line-height: 1.5;"
        )
        layout.addWidget(title)
        layout.addWidget(body)
        return widget

    def _icon_text(self, icon_text, body_text):
        label = QtWidgets.QLabel(f"{icon_text}  {body_text}")
        label.setStyleSheet(
            "color: #5f6f85; font-size: 13px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        return label

    def _icon_square_button(self, text, size, bg="#ffffff", fg="#64748b", border="#e6edf6"):
        button = QtWidgets.QPushButton(text)
        button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        button.setFixedSize(size, size)
        button.setStyleSheet(
            f"QPushButton {{ background: {bg}; color: {fg}; border: 1px solid {border}; "
            "border-radius: 11px; font-size: 15px; font-weight: 900; }}"
        )
        return button

    def _build_vertical_separator(self):
        line = QtWidgets.QFrame()
        line.setFixedWidth(1)
        line.setStyleSheet("background: #edf2f7; border: none;")
        return line

    def _card(self):
        card = QtWidgets.QFrame()
        card.setStyleSheet(
            "background: white; border: 1px solid #e8eef6; border-radius: 18px;"
        )
        return card
