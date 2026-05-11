from PyQt6 import QtWidgets, QtCore


class DoctorPatientRecordView(QtWidgets.QWidget):
    def __init__(self, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        self.selected_visit = None
        self.visits = self._sample_visits()
        self.setStyleSheet("background: #f8fbff; border: none;")

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)
        root.addLayout(self._build_header())
        root.addWidget(self._build_patient_card())
        root.addWidget(self._build_tabs())

        content = QtWidgets.QHBoxLayout()
        content.setSpacing(16)
        content.addWidget(self._build_history_panel(), 3)
        content.addWidget(self._build_visit_detail_panel(), 5)
        content.addWidget(self._build_summary_panel(), 3)
        root.addLayout(content, 1)
        self._select_visit(self.visits[0])

    def _build_header(self):
        row = QtWidgets.QHBoxLayout()
        title_col = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("Hồ sơ bệnh nhân")
        title.setStyleSheet("font-size: 25px; color: #0f172a; font-weight: 900; border: none; background: transparent;")
        crumb = QtWidgets.QLabel("Trang chủ  ›  Hồ sơ bệnh nhân  ›  Chi tiết hồ sơ")
        crumb.setStyleSheet("font-size: 14px; color: #64748b; font-weight: 700; border: none; background: transparent;")
        title_col.addWidget(title)
        title_col.addWidget(crumb)
        row.addLayout(title_col, 1)
        for text, style in [("🔔 2", "font-size: 20px; color: #64748b;"), ("👨‍⚕️", "background: #eaf2ff; border-radius: 21px; font-size: 20px;")]:
            label = QtWidgets.QLabel(text)
            label.setFixedSize(48, 42)
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("border: none; " + style)
            row.addWidget(label)
        name = QtWidgets.QLabel("Bác sĩ Minh  ▾")
        name.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 13px; font-weight: 900;")
        row.addWidget(name)
        return row

    def _build_patient_card(self):
        card = self._card()
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(24)

        avatar = QtWidgets.QLabel("👤")
        avatar.setFixedSize(92, 92)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("background: #eaf2ff; border-radius: 46px; font-size: 42px; border: none;")
        info = QtWidgets.QLabel(
            "<b style='font-size:20px;color:#0f172a'>Nguyễn Văn Nam</b>  "
            "<span style='background:#dbeafe;color:#2563eb;border-radius:10px;padding:3px 10px'>Nam</span><br>"
            "35 tuổi (15/02/1990)  -  Mã BN: BN000123<br><br>"
            "☎ 0987 654 321     ✉ nam.nguyen@gmail.com<br><br>"
            "⌖ 123 Đường Lê Lợi, P.1, Q.1, TP.HCM"
        )
        info.setStyleSheet("border: none; background: transparent; color: #475569; font-size: 13px; font-weight: 700;")
        medical = QtWidgets.QLabel(
            "<b>Nhóm máu:</b>        O+<br><br>"
            "<b>Nghề nghiệp:</b>     Nhân viên văn phòng<br><br>"
            "<b>Bảo hiểm:</b>        Có (BHYT)<br><br>"
            "<b>Người liên hệ:</b>   Nguyễn Thị Lan (Vợ)<br>                         0988 111 222"
        )
        medical.setStyleSheet("border: none; background: transparent; color: #475569; font-size: 13px; font-weight: 700;")
        note_box = QtWidgets.QFrame()
        note_box.setStyleSheet("background: #ffffff; border: none;")
        note_layout = QtWidgets.QVBoxLayout(note_box)
        note_title = QtWidgets.QLabel("Ghi chú                                      ✎")
        note_title.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 15px; font-weight: 900;")
        note = QtWidgets.QLabel("Bệnh nhân có tiền sử đau dạ dày.\nCần nhắc nhở kiêng đồ cay nóng.")
        note.setMinimumHeight(86)
        note.setWordWrap(True)
        note.setStyleSheet("background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; color: #475569; font-size: 13px; font-weight: 700;")
        note_layout.addWidget(note_title)
        note_layout.addWidget(note)

        layout.addWidget(avatar)
        layout.addWidget(info, 3)
        layout.addWidget(self._separator())
        layout.addWidget(medical, 2)
        layout.addWidget(self._separator())
        layout.addWidget(note_box, 3)
        return card

    def _build_tabs(self):
        card = self._card()
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(18, 0, 18, 0)
        for index, text in enumerate(["Lịch sử khám", "Thông tin cá nhân", "Bệnh sử", "Kết quả xét nghiệm", "Đơn thuốc", "Chỉ định", "Tài liệu đính kèm"]):
            btn = QtWidgets.QPushButton(text)
            btn.setCheckable(True)
            btn.setChecked(index == 0)
            btn.setStyleSheet(
                "QPushButton { border: none; background: transparent; padding: 14px 10px; color: #64748b; font-size: 13px; font-weight: 900; }"
                "QPushButton:checked { color: #13a66b; border-bottom: 3px solid #13a66b; }"
            )
            layout.addWidget(btn)
        layout.addStretch()
        return card

    def _build_history_panel(self):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        search = QtWidgets.QLineEdit()
        search.setPlaceholderText("Tìm kiếm lịch sử khám...")
        search.setMinimumHeight(42)
        search.setStyleSheet(self._input_style())
        layout.addWidget(search)
        self.history_list = QtWidgets.QVBoxLayout()
        self.history_list.setSpacing(10)
        for visit in self.visits:
            self.history_list.addWidget(self._visit_item(visit))
        layout.addLayout(self.history_list)
        layout.addStretch()
        all_btn = QtWidgets.QPushButton("▣  Xem tất cả lịch sử  ›")
        all_btn.setMinimumHeight(46)
        all_btn.setStyleSheet(self._outline_style("#2563eb"))
        layout.addWidget(all_btn)
        return card

    def _build_visit_detail_panel(self):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(14)
        self.visit_title = QtWidgets.QLabel("")
        self.visit_title.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 17px; font-weight: 900;")
        self.visit_body = QtWidgets.QLabel("")
        self.visit_body.setWordWrap(True)
        self.visit_body.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 13px; font-weight: 700; line-height: 155%;")
        layout.addWidget(self.visit_title)
        layout.addWidget(self.visit_body)
        layout.addStretch()
        return card

    def _build_summary_panel(self):
        panel = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)
        layout.addWidget(self._summary_card())
        layout.addWidget(self._small_info_card("Bệnh mãn tính", "Không có bệnh mãn tính."))
        layout.addWidget(self._small_info_card("Dị ứng", "Không ghi nhận dị ứng."))
        quick = self._card()
        ql = QtWidgets.QVBoxLayout(quick)
        ql.setContentsMargins(18, 16, 18, 16)
        title = QtWidgets.QLabel("Thao tác nhanh")
        title.setStyleSheet("font-size: 15px; font-weight: 900; color: #0f172a; border: none; background: transparent;")
        ql.addWidget(title)
        grid = QtWidgets.QGridLayout()
        for idx, text in enumerate(["+  Tạo lịch hẹn", "🩺  Khám bệnh", "Rx  Kê đơn thuốc", "🖨  In hồ sơ"]):
            btn = QtWidgets.QPushButton(text)
            btn.setMinimumHeight(46)
            btn.setStyleSheet(self._outline_style("#13a66b" if idx % 2 else "#2563eb"))
            grid.addWidget(btn, idx // 2, idx % 2)
        ql.addLayout(grid)
        layout.addWidget(quick)
        layout.addStretch()
        return panel

    def _summary_card(self):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        title = QtWidgets.QLabel("Tóm tắt hồ sơ")
        title.setStyleSheet("font-size: 15px; font-weight: 900; color: #0f172a; border: none; background: transparent;")
        layout.addWidget(title)
        for label, value in [("Tổng số lần khám", "12"), ("Tổng đơn thuốc", "9"), ("Tổng xét nghiệm", "5"), ("Tổng chỉ định", "4"), ("Tài liệu đính kèm", "3")]:
            row = QtWidgets.QHBoxLayout()
            left = QtWidgets.QLabel("▣  " + label)
            left.setStyleSheet("border: none; color: #64748b; font-size: 13px; font-weight: 800;")
            right = QtWidgets.QLabel(value)
            right.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            right.setStyleSheet("border: none; color: #0f172a; font-size: 13px; font-weight: 900;")
            row.addWidget(left, 1)
            row.addWidget(right)
            layout.addLayout(row)
        return card

    def _small_info_card(self, title, body):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        head = QtWidgets.QLabel(f"{title}                                      +")
        head.setStyleSheet("font-size: 15px; font-weight: 900; color: #0f172a; border: none; background: transparent;")
        text = QtWidgets.QLabel(body)
        text.setStyleSheet("border: none; color: #64748b; font-size: 13px; font-weight: 700;")
        layout.addWidget(head)
        layout.addWidget(text)
        return card

    def _visit_item(self, visit):
        frame = QtWidgets.QFrame()
        frame.setMinimumHeight(104)
        frame.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        frame.setStyleSheet("background: #ecfdf5; border: 1px solid #34d399; border-radius: 10px;" if visit["active"] else "background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px;")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(14, 12, 14, 12)
        date = QtWidgets.QLabel(f"<b>{visit['date']}  -  {visit['time']}</b>     <span style='color:#16a34a'>Đã hoàn tất</span>")
        desc = QtWidgets.QLabel(f"Phòng khám 1 - Bác sĩ Minh<br>{visit['reason']}")
        date.setStyleSheet("border: none; background: transparent; color: #0f172a; font-size: 13px;")
        desc.setStyleSheet("border: none; background: transparent; color: #475569; font-size: 13px; font-weight: 700;")
        layout.addWidget(date)
        layout.addWidget(desc)
        frame.mousePressEvent = lambda event, v=visit: self._select_visit(v)
        return frame

    def _select_visit(self, visit):
        self.selected_visit = visit
        self.visit_title.setText(f"Chi tiết lần khám - {visit['date']} {visit['time']}        Đã hoàn tất     🖨  ⋮")
        self.visit_body.setText(
            f"<b>Lý do khám</b><br>{visit['reason']}<br><br>"
            f"<b>Triệu chứng</b><br>{visit['symptoms']}<br><br>"
            "<b>Khám lâm sàng</b><br>"
            "<table cellspacing='0' cellpadding='8' width='100%'>"
            "<tr><td>Mạch</td><td>78 lần/phút</td><td>Huyết áp</td><td>120/80 mmHg</td></tr>"
            "<tr><td>Nhiệt độ</td><td>36.7 °C</td><td>Nhịp thở</td><td>18 lần/phút</td></tr>"
            "<tr><td>Cân nặng</td><td>65 kg</td><td>Chiều cao</td><td>170 cm</td></tr>"
            "</table><br>"
            "<b>Chẩn đoán</b><br>R51 - Đau đầu<br><br>"
            "<b>Kết luận</b><br>Bệnh nhân sức khỏe ổn định, không phát hiện bất thường.<br><br>"
            "<b>Hướng dẫn</b><br>Nghỉ ngơi hợp lý, uống đủ nước, tái khám nếu triệu chứng kéo dài.<br><br>"
            "<b>Bác sĩ khám</b><br>👨‍⚕️  Bác sĩ Minh"
        )

    def _sample_visits(self):
        return [
            {"date": "23/05/2026", "time": "09:00", "reason": "Khám tổng quát", "symptoms": "Đau đầu nhẹ, mệt mỏi, ăn uống bình thường.", "active": True},
            {"date": "18/05/2026", "time": "10:30", "reason": "Đau mỏi vai gáy", "symptoms": "Đau vai gáy sau khi làm việc lâu.", "active": False},
            {"date": "10/04/2026", "time": "14:00", "reason": "Khám tai mũi họng", "symptoms": "Nghẹt mũi, đau họng nhẹ.", "active": False},
            {"date": "15/02/2026", "time": "11:15", "reason": "Mệt mỏi, khó ngủ", "symptoms": "Khó ngủ kéo dài một tuần.", "active": False},
            {"date": "20/12/2025", "time": "08:30", "reason": "Khám tổng quát", "symptoms": "Theo dõi sức khỏe định kỳ.", "active": False},
        ]

    def _card(self):
        card = QtWidgets.QFrame()
        card.setStyleSheet("background: #ffffff; border: 1px solid #e7edf5; border-radius: 14px;")
        return card

    def _separator(self):
        line = QtWidgets.QFrame()
        line.setFixedWidth(1)
        line.setStyleSheet("background: #e7edf5; border: none;")
        return line

    def _input_style(self):
        return "background: #ffffff; border: 1px solid #dbe4ee; border-radius: 9px; padding: 10px 12px; color: #0f172a; font-weight: 800;"

    def _outline_style(self, color):
        return f"QPushButton {{ background: #ffffff; color: {color}; border: 1px solid #dbe4ee; border-radius: 9px; padding: 10px 12px; font-weight: 900; }} QPushButton:hover {{ border-color: {color}; }}"
