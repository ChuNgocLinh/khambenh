from PyQt6 import QtWidgets, QtCore


class DoctorPatientRecordView(QtWidgets.QWidget):
    def __init__(self, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        self.setStyleSheet("background: #f5f8fc; border: none;")

        self.patient = {
            "name": "Nguyễn Văn Nam",
            "gender": "Nam",
            "age": "35 tuổi (15/02/1990)",
            "code": "Mã BN: BN000123",
            "phone": "0987 654 321",
            "address": "123 Đường Lê Lợi, P.1, Q.1, TP.HCM",
            "date": "23/05/2026 09:00",
            "reason": "Khám tổng quát",
        }
        self.quick_info = [
            ("Nhóm máu:", "O+"),
            ("Nghề nghiệp:", "Nhân viên văn phòng"),
            ("Bảo hiểm:", "Có (BHYT)"),
            ("Ngày khám gần nhất:", "18/05/2026"),
            ("Bác sĩ khám gần nhất:", "Bác sĩ Minh"),
        ]
        self.history_items = [
            ("18/05/2026", "Khám tổng quát", "Đau mỏi vai gáy", "Bác sĩ Minh"),
            ("10/04/2026", "Khám tai mũi họng", "Viêm họng cấp", "Bác sĩ Minh"),
            ("15/02/2026", "Khám tổng quát", "Mệt mỏi, khó ngủ", "Bác sĩ Minh"),
        ]
        self.test_results = [
            ("Xét nghiệm máu", "18/05/2026", "Bình thường", "#eafaf1", "#21b36a"),
            ("X-quang ngực", "18/05/2026", "Chưa có kết quả", "#fff4e8", "#f59e0b"),
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
        page_layout.setContentsMargins(0, 0, 0, 18)
        page_layout.setSpacing(16)
        page_layout.addLayout(self._build_header())
        page_layout.addWidget(self._build_stepper_card())

        content = QtWidgets.QHBoxLayout()
        content.setSpacing(16)
        content.addLayout(self._build_main_column(), 7)
        content.addWidget(self._build_sidebar(), 3)
        page_layout.addLayout(content)

        scroll.setWidget(page)
        root.addWidget(scroll)

    def _build_header(self):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(14)

        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(4)
        title = QtWidgets.QLabel("Khám bệnh")
        title.setStyleSheet(
            "color: #0f172a; font-size: 25px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        crumb = QtWidgets.QLabel("Trang chủ  ›  Khám bệnh  ›  Thông tin khám")
        crumb.setStyleSheet(
            "color: #7c8aa0; font-size: 14px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        title_col.addWidget(title)
        title_col.addWidget(crumb)
        row.addLayout(title_col, 1)

        row.addWidget(self._build_notification_widget())

        avatar = QtWidgets.QLabel("👨‍⚕️")
        avatar.setFixedSize(42, 42)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            "background: #eef3fb; border-radius: 21px; border: none; font-size: 20px;"
        )
        row.addWidget(avatar)

        user_name = QtWidgets.QLabel("Bác sĩ Minh")
        user_name.setStyleSheet(
            "color: #0f172a; font-size: 14px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        row.addWidget(user_name)

        caret = QtWidgets.QLabel("▾")
        caret.setStyleSheet(
            "color: #64748b; font-size: 14px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        row.addWidget(caret)
        return row

    def _build_notification_widget(self):
        wrapper = QtWidgets.QFrame()
        wrapper.setFixedSize(38, 38)
        wrapper.setStyleSheet("background: transparent; border: none;")

        icon = QtWidgets.QLabel("🔔", wrapper)
        icon.setGeometry(6, 6, 26, 26)
        icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet(
            "background: transparent; border: none; color: #64748b; font-size: 18px;"
        )

        badge = QtWidgets.QLabel("2", wrapper)
        badge.setGeometry(20, 0, 18, 18)
        badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            "background: #ff3b30; color: white; border-radius: 9px; "
            "font-size: 10px; font-weight: 900;"
        )
        return wrapper

    def _build_stepper_card(self):
        card = self._card()
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(28, 20, 28, 20)
        layout.setSpacing(10)

        steps = [
            ("1", "Thông tin khám", True),
            ("2", "Chẩn đoán - Kết luận", False),
            ("3", "Chỉ định - Kê đơn", False),
            ("4", "Hoàn tất", False),
        ]

        for index, (number, text, active) in enumerate(steps):
            if index:
                line = QtWidgets.QFrame()
                line.setFixedHeight(2)
                line.setStyleSheet(
                    "background: #d6e7db; border: none;" if index == 1
                    else "background: #e7edf5; border: none;"
                )
                layout.addWidget(line, 1)
            layout.addWidget(self._build_step(number, text, active))

        return card

    def _build_step(self, number, text, active):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        circle = QtWidgets.QLabel(number)
        circle.setFixedSize(34, 34)
        circle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        circle.setStyleSheet(
            "background: #18b86d; color: white; border-radius: 17px; "
            "font-size: 14px; font-weight: 900;"
            if active else
            "background: white; color: #6b7a90; border: 1px solid #d9e3ef; "
            "border-radius: 17px; font-size: 14px; font-weight: 900;"
        )
        text_label = QtWidgets.QLabel(text)
        text_label.setStyleSheet(
            "color: #1b8f5c; font-size: 14px; font-weight: 900; "
            "background: transparent; border: none;"
            if active else
            "color: #66758d; font-size: 14px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        layout.addWidget(circle)
        layout.addWidget(text_label)
        return widget

    def _build_main_column(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(16)
        layout.addWidget(self._build_patient_card())

        form_row = QtWidgets.QHBoxLayout()
        form_row.setSpacing(16)
        form_row.addWidget(self._build_symptom_card(), 1)
        form_row.addWidget(self._build_exam_card(), 1)
        layout.addLayout(form_row)

        layout.addWidget(self._build_diagnosis_card())
        layout.addLayout(self._build_footer_actions())
        return layout

    def _build_sidebar(self):
        widget = QtWidgets.QWidget()
        widget.setStyleSheet("background: transparent;")
        widget.setMinimumWidth(330)

        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        layout.addWidget(self._build_quick_info_card())
        layout.addWidget(self._build_history_card())
        layout.addWidget(self._build_result_card())
        layout.addStretch()
        return widget

    def _build_patient_card(self):
        card = self._card()
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(16)

        avatar = QtWidgets.QLabel("👨")
        avatar.setFixedSize(78, 78)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            "background: #eef4fb; border-radius: 39px; border: none; font-size: 38px;"
        )
        layout.addWidget(avatar, 0, QtCore.Qt.AlignmentFlag.AlignTop)

        info_col = QtWidgets.QVBoxLayout()
        info_col.setSpacing(6)
        name_row = QtWidgets.QHBoxLayout()
        name_row.setSpacing(8)

        name = QtWidgets.QLabel(self.patient["name"])
        name.setStyleSheet(
            "color: #0f172a; font-size: 18px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        gender = QtWidgets.QLabel(self.patient["gender"])
        gender.setStyleSheet(
            "background: #eaf2ff; color: #3d7ef3; border-radius: 12px; "
            "padding: 4px 10px; font-size: 12px; font-weight: 900;"
        )
        name_row.addWidget(name)
        name_row.addWidget(gender)
        name_row.addStretch()

        meta = QtWidgets.QLabel(f"{self.patient['age']} - {self.patient['code']}")
        meta.setStyleSheet(
            "color: #74839a; font-size: 13px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        contact = QtWidgets.QLabel(
            f"SĐT: {self.patient['phone']} - Địa chỉ: {self.patient['address']}"
        )
        contact.setWordWrap(True)
        contact.setStyleSheet(
            "color: #637289; font-size: 13px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        info_col.addLayout(name_row)
        info_col.addWidget(meta)
        info_col.addWidget(contact)
        layout.addLayout(info_col, 1)

        summary_col = QtWidgets.QVBoxLayout()
        summary_col.setSpacing(8)
        date = QtWidgets.QLabel(f"Ngày khám: {self.patient['date']}")
        date.setStyleSheet(
            "color: #526176; font-size: 13px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        reason = QtWidgets.QLabel(f"Lý do khám: {self.patient['reason']}")
        reason.setStyleSheet(
            "color: #526176; font-size: 13px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        button = QtWidgets.QPushButton("👁  Xem hồ sơ bệnh nhân   ▾")
        button.setMinimumHeight(42)
        button.setStyleSheet(self._ghost_button_style())
        summary_col.addStretch()
        summary_col.addWidget(date, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        summary_col.addWidget(reason, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        summary_col.addWidget(button, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addLayout(summary_col)
        return card

    def _build_quick_info_card(self):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)

        title = QtWidgets.QLabel("Thông tin nhanh")
        title.setStyleSheet(self._section_title_style())
        layout.addWidget(title)

        for label_text, value_text in self.quick_info:
            row = QtWidgets.QHBoxLayout()
            row.setSpacing(10)
            label = QtWidgets.QLabel(label_text)
            label.setStyleSheet(
                "color: #64748b; font-size: 13px; font-weight: 800; "
                "background: transparent; border: none;"
            )
            value = QtWidgets.QLabel(value_text)
            value.setWordWrap(True)
            value.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter
            )
            value.setStyleSheet(
                "color: #3f4f65; font-size: 13px; font-weight: 900; "
                "background: transparent; border: none;"
            )
            row.addWidget(label, 1)
            row.addWidget(value, 1)
            layout.addLayout(row)

        return card

    def _build_symptom_card(self):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        title = QtWidgets.QLabel("1. Triệu chứng - Hỏi bệnh")
        title.setStyleSheet(self._section_title_style())
        layout.addWidget(title)
        layout.addWidget(self._field_block("Triệu chứng chính", self._text_input("Đau đầu, chóng mặt, mệt mỏi")))
        layout.addWidget(
            self._field_block(
                "Triệu chứng kèm theo",
                self._chip_input(["Nhức đầu", "Buồn nôn", "Mất ngủ"]),
            )
        )
        layout.addWidget(self._field_block("Tiền sử bệnh", self._text_area("Không có bệnh lý nền.")))
        layout.addWidget(self._field_block("Tiền sử dị ứng", self._text_area("Không dị ứng thuốc, thực phẩm.")))
        layout.addWidget(
            self._field_block(
                "Ghi chú",
                self._text_area("Ghi chú thêm (nếu có)...", muted=True),
            )
        )
        return card

    def _build_exam_card(self):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        title = QtWidgets.QLabel("2. Khám lâm sàng")
        title.setStyleSheet(self._section_title_style())
        layout.addWidget(title)

        grid = QtWidgets.QGridLayout()
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(12)
        metrics = [
            ("Mạch", "78", "lần/phút"),
            ("Huyết áp", "120/80", "mmHg"),
            ("Nhiệt độ", "36.7", "°C"),
            ("Nhịp thở", "18", "lần/phút"),
            ("Cân nặng", "65", "kg"),
            ("Chiều cao", "170", "cm"),
        ]

        for index, (label_text, value_text, unit_text) in enumerate(metrics):
            field = self._field_block(label_text, self._metric_input(value_text, unit_text))
            grid.addWidget(field, index // 2, index % 2)

        layout.addLayout(grid)
        layout.addWidget(
            self._field_block(
                "Khám tổng quát",
                self._text_area("Bệnh nhân tỉnh táo, tiếp xúc tốt, không sốt."),
            )
        )
        layout.addWidget(
            self._field_block(
                "Kết quả khám",
                self._text_area("Không phát hiện bất thường."),
            )
        )
        return card

    def _build_diagnosis_card(self):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        title = QtWidgets.QLabel("3. Chẩn đoán sơ bộ")
        title.setStyleSheet(self._section_title_style())
        layout.addWidget(title)

        top_row = QtWidgets.QHBoxLayout()
        top_row.setSpacing(14)
        top_row.addWidget(
            self._field_block("Chẩn đoán sơ bộ", self._text_input("R51 - Đau đầu")),
            3,
        )
        top_row.addWidget(
            self._field_block("Mức độ", self._combo_input(["Nhẹ", "Trung bình", "Nặng"], 0)),
            1,
        )
        layout.addLayout(top_row)
        layout.addWidget(
            self._field_block(
                "Ghi chú chẩn đoán",
                self._text_area("Theo dõi thêm, hẹn tái khám nếu triệu chứng không cải thiện."),
            )
        )
        return card

    def _build_history_card(self):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QtWidgets.QLabel("Lịch sử khám")
        title.setStyleSheet(self._section_title_style())
        layout.addWidget(title)

        for item in self.history_items:
            layout.addWidget(self._history_item(*item))

        view_all = QtWidgets.QPushButton("Xem tất cả lịch sử  ➜")
        view_all.setStyleSheet(
            "QPushButton { background: transparent; color: #2678ff; border: none; "
            "font-size: 13px; font-weight: 900; text-align: right; padding: 8px 0 0 0; }"
        )
        layout.addWidget(view_all, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        return card

    def _history_item(self, date_text, title_text, desc_text, doctor_text):
        item = QtWidgets.QFrame()
        item.setStyleSheet(
            "background: #fbfcfe; border: 1px solid #f0f4f9; border-radius: 14px;"
        )
        layout = QtWidgets.QVBoxLayout(item)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        top_row = QtWidgets.QHBoxLayout()
        date = QtWidgets.QLabel(date_text)
        date.setStyleSheet(
            "color: #9aa8ba; font-size: 12px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        badge = QtWidgets.QLabel("Đã hoàn tất")
        badge.setStyleSheet(
            "background: #ebfbf1; color: #19a861; border-radius: 11px; "
            "padding: 4px 10px; font-size: 11px; font-weight: 900;"
        )
        top_row.addWidget(date)
        top_row.addStretch()
        top_row.addWidget(badge)

        title = QtWidgets.QLabel(title_text)
        title.setStyleSheet(
            "color: #1e2c3d; font-size: 14px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        desc = QtWidgets.QLabel(desc_text)
        desc.setStyleSheet(
            "color: #637289; font-size: 13px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        doctor = QtWidgets.QLabel(doctor_text)
        doctor.setStyleSheet(
            "color: #7b889d; font-size: 13px; font-weight: 800; "
            "background: transparent; border: none;"
        )

        layout.addLayout(top_row)
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addWidget(doctor)
        return item

    def _build_result_card(self):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        title = QtWidgets.QLabel("Kết quả cận lâm sàng gần nhất")
        title.setWordWrap(True)
        title.setStyleSheet(self._section_title_style())
        layout.addWidget(title)

        for name_text, date_text, badge_text, badge_bg, badge_fg in self.test_results:
            row = QtWidgets.QHBoxLayout()
            row.setSpacing(10)

            info = QtWidgets.QVBoxLayout()
            info.setSpacing(4)
            name = QtWidgets.QLabel(name_text)
            name.setStyleSheet(
                "color: #1e2c3d; font-size: 14px; font-weight: 900; "
                "background: transparent; border: none;"
            )
            date = QtWidgets.QLabel(date_text)
            date.setStyleSheet(
                "color: #7b889d; font-size: 12px; font-weight: 800; "
                "background: transparent; border: none;"
            )
            info.addWidget(name)
            info.addWidget(date)

            badge = QtWidgets.QLabel(badge_text)
            badge.setStyleSheet(
                f"background: {badge_bg}; color: {badge_fg}; border-radius: 11px; "
                "padding: 4px 10px; font-size: 11px; font-weight: 900;"
            )

            row.addLayout(info, 1)
            row.addWidget(badge)
            layout.addLayout(row)

        view_all = QtWidgets.QPushButton("Xem tất cả kết quả  ➜")
        view_all.setStyleSheet(
            "QPushButton { background: transparent; color: #2678ff; border: none; "
            "font-size: 13px; font-weight: 900; text-align: right; padding: 8px 0 0 0; }"
        )
        layout.addWidget(view_all, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        return card

    def _build_footer_actions(self):
        row = QtWidgets.QHBoxLayout()
        row.setContentsMargins(0, 6, 0, 0)
        row.setSpacing(14)

        cancel = QtWidgets.QPushButton("✕  Hủy khám")
        cancel.setMinimumHeight(46)
        cancel.setMinimumWidth(170)
        cancel.setStyleSheet(
            "QPushButton { background: white; color: #ff5a5f; border: 1px solid #ffb7b9; "
            "border-radius: 12px; padding: 10px 20px; font-size: 14px; font-weight: 900; }"
        )

        save = QtWidgets.QPushButton("💾  Lưu tạm")
        save.setMinimumHeight(46)
        save.setMinimumWidth(150)
        save.setStyleSheet(
            "QPushButton { background: white; color: #3b82f6; border: 1px solid #d9e8ff; "
            "border-radius: 12px; padding: 10px 20px; font-size: 14px; font-weight: 900; }"
        )

        next_btn = QtWidgets.QPushButton("➜  Tiếp tục")
        next_btn.setMinimumHeight(46)
        next_btn.setMinimumWidth(175)
        next_btn.setStyleSheet(
            "QPushButton { background: #16b96e; color: white; border: none; "
            "border-radius: 12px; padding: 10px 22px; font-size: 14px; font-weight: 900; }"
        )

        row.addWidget(cancel, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        row.addStretch()
        row.addWidget(save)
        row.addWidget(next_btn)
        return row

    def _field_block(self, label_text, field_widget):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        label = QtWidgets.QLabel(label_text)
        label.setStyleSheet(
            "color: #4d5d73; font-size: 13px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        layout.addWidget(label)
        layout.addWidget(field_widget)
        return widget

    def _text_input(self, text):
        input_box = QtWidgets.QLineEdit(text)
        input_box.setReadOnly(True)
        input_box.setMinimumHeight(42)
        input_box.setStyleSheet(self._input_style())
        return input_box

    def _combo_input(self, items, selected_index):
        combo = QtWidgets.QComboBox()
        combo.addItems(items)
        combo.setCurrentIndex(selected_index)
        combo.setMinimumHeight(42)
        combo.setStyleSheet(
            "QComboBox { background: white; color: #1f2d3d; border: 1px solid #dfe6f0; "
            "border-radius: 10px; padding: 0 14px; font-size: 13px; font-weight: 800; } "
            "QComboBox::drop-down { border: none; width: 26px; } "
            "QComboBox::down-arrow { image: none; }"
        )
        return combo

    def _text_area(self, text, muted=False):
        area = QtWidgets.QTextEdit()
        area.setReadOnly(True)
        area.setText(text)
        area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        area.setMinimumHeight(66)
        area.setStyleSheet(
            "QTextEdit { background: white; color: #1f2d3d; border: 1px solid #dfe6f0; "
            "border-radius: 10px; padding: 10px 12px; font-size: 13px; font-weight: 700; }"
            if not muted else
            "QTextEdit { background: white; color: #97a3b4; border: 1px solid #dfe6f0; "
            "border-radius: 10px; padding: 10px 12px; font-size: 13px; font-weight: 700; }"
        )
        return area

    def _chip_input(self, chips):
        frame = QtWidgets.QFrame()
        frame.setMinimumHeight(42)
        frame.setStyleSheet(
            "background: white; border: 1px solid #dfe6f0; border-radius: 10px;"
        )
        layout = QtWidgets.QHBoxLayout(frame)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(8)

        for chip_text in chips:
            chip = QtWidgets.QLabel(f"{chip_text}  ✕")
            chip.setStyleSheet(
                "background: #f1f5f9; color: #46566b; border-radius: 10px; "
                "padding: 6px 10px; font-size: 12px; font-weight: 800;"
            )
            layout.addWidget(chip)

        layout.addStretch()
        arrow = QtWidgets.QLabel("▾")
        arrow.setStyleSheet(
            "color: #728197; font-size: 14px; font-weight: 900; background: transparent; border: none;"
        )
        layout.addWidget(arrow)
        return frame

    def _metric_input(self, value_text, unit_text):
        frame = QtWidgets.QFrame()
        frame.setMinimumHeight(42)
        frame.setStyleSheet(
            "background: white; border: 1px solid #dfe6f0; border-radius: 10px;"
        )
        layout = QtWidgets.QHBoxLayout(frame)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)

        value = QtWidgets.QLabel(value_text)
        value.setStyleSheet(
            "color: #1f2d3d; font-size: 13px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        unit = QtWidgets.QLabel(unit_text)
        unit.setStyleSheet(
            "color: #6d7c91; font-size: 13px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        layout.addWidget(value)
        layout.addStretch()
        layout.addWidget(unit)
        return frame

    def _card(self):
        card = QtWidgets.QFrame()
        card.setStyleSheet(
            "background: white; border: 1px solid #e7edf5; border-radius: 16px;"
        )
        return card

    def _input_style(self):
        return (
            "QLineEdit { background: white; color: #1f2d3d; border: 1px solid #dfe6f0; "
            "border-radius: 10px; padding: 0 14px; font-size: 13px; font-weight: 800; }"
        )

    def _ghost_button_style(self):
        return (
            "QPushButton { background: white; color: #46566b; border: 1px solid #dfe6f0; "
            "border-radius: 10px; padding: 0 16px; font-size: 13px; font-weight: 900; }"
        )

    def _section_title_style(self):
        return (
            "color: #102033; font-size: 16px; font-weight: 900; "
            "background: transparent; border: none;"
        )
