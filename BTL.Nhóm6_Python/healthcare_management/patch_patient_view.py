import sys

def patch_file():
    with open('views/patient_view.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace DoctorPage
    old_doctor_page = """class DoctorPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)

        title = QtWidgets.QLabel("Đội ngũ bác sĩ")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #2c3e50;")
        layout.addWidget(title)

        desc = QtWidgets.QLabel("Danh sách bác sĩ đang khám tại CarePlus. Nhấn đúp để xem chi tiết.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #64748b; font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(desc)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Họ tên", "Chuyên khoa", "SĐT"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setStyleSheet(
            \"\"\"
            QTableWidget { background: white; border-radius: 12px; border: 1px solid #eef0f2; font-size: 14px; color: #1f2937; }
            QHeaderView::section { background-color: #f8f9fa; padding: 12px; font-weight: bold; border: none; border-bottom: 2px solid #69c0a5; }
            QTableWidget::item { padding: 12px; border-bottom: 1px solid #f1f5f9; }
            \"\"\"
        )

        doctors = DoctorController.get_all()
        self.doctors_data = doctors
        self.table.setRowCount(len(doctors))
        for i, doctor in enumerate(doctors):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(doctor.get("name", ""))))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(doctor.get("specialty", ""))))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(doctor.get("phone", ""))))
            self.table.setRowHeight(i, 48)

        self.table.cellDoubleClicked.connect(self.show_detail)
        layout.addWidget(self.table)
        layout.addStretch()

    def show_detail(self, row, _col):
        if row < 0 or row >= len(self.doctors_data):
            return

        doctor = self.doctors_data[row]
        fields = [
            ("Mã bác sĩ", doctor.get("doctor_id", "")),
            ("Họ tên", doctor.get("name", "")),
            ("Chuyên khoa", doctor.get("specialty", "")),
            ("SĐT", doctor.get("phone", "")),
            ("Email", doctor.get("email", "")),
        ]
        dialog = DetailDialog("Chi tiết bác sĩ", fields, self)
        dialog.exec()"""

    new_doctor_page = """class DoctorPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)

        # HEADER
        header_layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("Đội ngũ bác sĩ")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #2c3e50;")
        header_layout.addWidget(title)

        desc = QtWidgets.QLabel("Tìm kiếm và đặt lịch hẹn với các bác sĩ chuyên khoa giàu kinh nghiệm")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #64748b; font-size: 14px; margin-bottom: 20px;")
        header_layout.addWidget(desc)
        layout.addLayout(header_layout)

        # BODY
        body_layout = QtWidgets.QHBoxLayout()
        body_layout.setSpacing(20)

        # 1. LEFT SIDEBAR (Tìm kiếm bác sĩ)
        left_sidebar = QtWidgets.QFrame()
        left_sidebar.setFixedWidth(250)
        left_sidebar.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #eef0f2;")
        left_layout = QtWidgets.QVBoxLayout(left_sidebar)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(15)

        left_title = QtWidgets.QLabel("Tìm kiếm bác sĩ")
        left_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e293b;")
        left_layout.addWidget(left_title)

        search_input = QtWidgets.QLineEdit()
        search_input.setPlaceholderText("Tìm theo tên bác sĩ...")
        search_input.setStyleSheet("padding: 10px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 13px; background: #f8fafc;")
        left_layout.addWidget(search_input)

        filters = [
            ("Chuyên khoa", ["Tất cả chuyên khoa", "Nội tổng quát", "Tim mạch", "Nhi khoa", "Sản phụ khoa", "Ngoại khoa"]),
            ("Bệnh viện / Phòng khám", ["Tất cả cơ sở", "Bệnh viện Đa khoa CarePlus", "Phòng khám Nhi CarePlus", "Phòng khám Da liễu CarePlus", "Phòng khám Tai Mũi Họng"]),
            ("Kinh nghiệm", ["Tất cả", "Trên 10 năm", "Trên 5 năm", "Dưới 5 năm"])
        ]

        for label_text, items in filters:
            lbl = QtWidgets.QLabel(label_text)
            lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #475569; margin-top: 5px;")
            combo = QtWidgets.QComboBox()
            combo.addItems(items)
            combo.setStyleSheet("padding: 8px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 13px; background: white;")
            left_layout.addWidget(lbl)
            left_layout.addWidget(combo)

        search_btn = QtWidgets.QPushButton("Tìm kiếm")
        search_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        search_btn.setStyleSheet("background: #69c0a5; color: white; padding: 12px; border-radius: 6px; font-weight: bold; font-size: 14px; margin-top: 10px; border: none;")
        left_layout.addWidget(search_btn)
        left_layout.addStretch()
        
        body_layout.addWidget(left_sidebar)

        # 2. CENTER CONTENT (Danh sách bác sĩ)
        center_widget = QtWidgets.QWidget()
        center_layout = QtWidgets.QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(15)

        center_header = QtWidgets.QHBoxLayout()
        center_title = QtWidgets.QLabel("Danh sách bác sĩ")
        center_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e293b;")

        doctors = DoctorController.get_all()
        self.doctors_data = doctors
        total_docs = len(doctors)
        
        center_info = QtWidgets.QLabel(f"Hiển thị 1 - {total_docs} trong {total_docs} bác sĩ" if total_docs > 0 else "Không tìm thấy bác sĩ")
        center_info.setStyleSheet("font-size: 13px; color: #64748b;")

        sort_combo = QtWidgets.QComboBox()
        sort_combo.addItems(["Sắp xếp: Mới nhất", "Sắp xếp: Đánh giá cao", "Sắp xếp: Nhiều kinh nghiệm"])
        sort_combo.setStyleSheet("padding: 6px 10px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 13px; background: white;")

        center_header.addWidget(center_title)
        center_header.addStretch()
        center_header.addWidget(center_info)
        center_header.addSpacing(10)
        center_header.addWidget(sort_combo)
        center_layout.addLayout(center_header)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("background: transparent;")

        grid_widget = QtWidgets.QWidget()
        grid_widget.setStyleSheet("background: transparent;")
        grid_layout = QtWidgets.QGridLayout(grid_widget)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(15)

        col_count = 3  # Tùy thuộc vào kích thước, dùng 3 cột để không bị quá chật
        
        # Mảng kinh nghiệm và rating ngẫu nhiên để giống thiết kế
        mock_data = [
            {"kn": "15 năm KN", "rate": "4.9", "reviews": "128", "hosp": "Bệnh viện Đa khoa CarePlus"},
            {"kn": "12 năm KN", "rate": "4.8", "reviews": "96", "hosp": "Bệnh viện Đa khoa CarePlus"},
            {"kn": "10 năm KN", "rate": "4.9", "reviews": "75", "hosp": "Phòng khám Nhi CarePlus"},
            {"kn": "8 năm KN", "rate": "4.7", "reviews": "62", "hosp": "Bệnh viện Đa khoa CarePlus"},
            {"kn": "14 năm KN", "rate": "4.8", "reviews": "110", "hosp": "Bệnh viện Đa khoa CarePlus"},
            {"kn": "9 năm KN", "rate": "4.6", "reviews": "58", "hosp": "Phòng khám Da liễu CarePlus"},
            {"kn": "11 năm KN", "rate": "4.8", "reviews": "93", "hosp": "Bệnh viện Đa khoa CarePlus"},
            {"kn": "7 năm KN", "rate": "4.7", "reviews": "45", "hosp": "Phòng khám Tai Mũi Họng"}
        ]

        for i, doctor in enumerate(doctors):
            meta = mock_data[i % len(mock_data)]
            card = self.create_doctor_card(doctor, i, meta)
            grid_layout.addWidget(card, i // col_count, i % col_count)

        grid_layout.setRowStretch(grid_layout.rowCount(), 1)
        scroll_area.setWidget(grid_widget)
        center_layout.addWidget(scroll_area)
        
        body_layout.addWidget(center_widget, 1)

        # 3. RIGHT SIDEBAR (Truy cập nhanh & Chuyên khoa)
        right_sidebar = QtWidgets.QVBoxLayout()
        right_sidebar.setSpacing(20)

        quick_access = self.create_right_panel("Truy cập nhanh", [
            ("📅", "Đặt lịch khám"),
            ("🗓️", "Lịch hẹn của tôi"),
            ("🏥", "Lịch sử khám bệnh"),
            ("🔬", "Kết quả xét nghiệm"),
            ("📄", "Đơn thuốc của tôi")
        ])

        specialties = self.create_right_panel("Chuyên khoa", [
            ("🧬", "Nội tổng quát", "12"),
            ("❤️", "Tim mạch", "8"),
            ("👶", "Nhi khoa", "10"),
            ("🤰", "Sản phụ khoa", "7"),
            ("🦴", "Ngoại khoa", "9")
        ], is_specialty=True)

        right_sidebar.addWidget(quick_access)
        right_sidebar.addWidget(specialties)
        right_sidebar.addStretch()

        right_widget = QtWidgets.QWidget()
        right_widget.setFixedWidth(240)
        right_widget.setLayout(right_sidebar)
        body_layout.addWidget(right_widget)

        layout.addLayout(body_layout)

    def create_doctor_card(self, doctor, index, meta):
        card = QtWidgets.QFrame()
        card.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #eef0f2;")
        card.setFixedSize(220, 270)
        
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(6)
        
        # Avatar and Badge
        top_layout = QtWidgets.QHBoxLayout()
        
        avatar_label = QtWidgets.QLabel("🧑‍⚕️")
        avatar_label.setFixedSize(50, 50)
        avatar_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar_label.setStyleSheet("background: #f1f5f9; border-radius: 25px; font-size: 25px; border: 2px solid #e2e8f0;")
        
        badge = QtWidgets.QLabel(meta["kn"])
        badge.setStyleSheet("background: #d1fae5; color: #059669; border-radius: 8px; padding: 4px 8px; font-size: 11px; font-weight: bold;")
        badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        top_layout.addWidget(avatar_label)
        top_layout.addStretch()
        top_layout.addWidget(badge, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addLayout(top_layout)
        
        # Doctor info
        name = QtWidgets.QLabel(f"BS. {doctor.get('name', 'N/A')}")
        name.setStyleSheet("font-size: 14px; font-weight: bold; color: #1e293b; margin-top: 8px;")
        name.setWordWrap(True)
        layout.addWidget(name)
        
        specialty = QtWidgets.QLabel(doctor.get('specialty', 'Chuyên khoa'))
        specialty.setStyleSheet("font-size: 12px; color: #059669; font-weight: bold;")
        layout.addWidget(specialty)
        
        hospital = QtWidgets.QLabel(meta["hosp"])
        hospital.setStyleSheet("font-size: 11px; color: #64748b;")
        hospital.setWordWrap(True)
        layout.addWidget(hospital)
        
        rating = QtWidgets.QLabel(f"⭐ {meta['rate']} ({meta['reviews']} đánh giá)")
        rating.setStyleSheet("font-size: 11px; color: #d97706; margin-bottom: 8px;")
        layout.addWidget(rating)
        
        layout.addStretch()
        
        # Button
        btn = QtWidgets.QPushButton("Xem hồ sơ")
        btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(\"\"\"
            QPushButton {
                background: white; border: 1px solid #69c0a5; color: #69c0a5;
                border-radius: 6px; padding: 6px; font-weight: bold; font-size: 12px;
            }
            QPushButton:hover {
                background: #f0fdf4;
            }
        \"\"\")
        btn.clicked.connect(lambda _, r=index: self.show_detail(r, 0))
        layout.addWidget(btn)
        
        return card

    def create_right_panel(self, title_text, items, is_specialty=False):
        panel = QtWidgets.QFrame()
        panel.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #eef0f2;")
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        title = QtWidgets.QLabel(title_text)
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #1e293b; margin-bottom: 5px;")
        layout.addWidget(title)
        
        for item in items:
            row = QtWidgets.QHBoxLayout()
            row.setSpacing(10)
            icon_lbl = QtWidgets.QLabel(item[0])
            icon_lbl.setFixedWidth(24)
            icon_lbl.setStyleSheet("font-size: 14px; color: #64748b; background: #f8fafc; border-radius: 6px; padding: 4px;" if is_specialty else "font-size: 14px;")
            icon_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            
            text_lbl = QtWidgets.QLabel(item[1])
            text_lbl.setStyleSheet("font-size: 12px; color: #475569;")
            
            row.addWidget(icon_lbl)
            row.addWidget(text_lbl)
            
            if is_specialty and len(item) > 2:
                row.addStretch()
                count_lbl = QtWidgets.QLabel(item[2])
                count_lbl.setStyleSheet("font-size: 11px; color: #94a3b8;")
                row.addWidget(count_lbl)
            else:
                arrow = QtWidgets.QLabel("›")
                arrow.setStyleSheet("font-size: 16px; color: #94a3b8; font-weight: bold;")
                row.addStretch()
                row.addWidget(arrow)
            
            # Row container
            row_widget = QtWidgets.QWidget()
            row_layout = QtWidgets.QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.addLayout(row)
            row_widget.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            layout.addWidget(row_widget)
            
        if is_specialty:
            view_all = QtWidgets.QLabel("Xem tất cả →")
            view_all.setStyleSheet("font-size: 12px; color: #3b82f6; font-weight: bold; margin-top: 5px;")
            view_all.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            layout.addWidget(view_all)
            
        return panel

    def show_detail(self, row, _col):
        if row < 0 or row >= len(self.doctors_data):
            return

        doctor = self.doctors_data[row]
        fields = [
            ("Mã bác sĩ", doctor.get("doctor_id", "")),
            ("Họ tên", doctor.get("name", "")),
            ("Chuyên khoa", doctor.get("specialty", "")),
            ("SĐT", doctor.get("phone", "")),
            ("Email", doctor.get("email", "")),
        ]
        dialog = DetailDialog("Chi tiết bác sĩ", fields, self)
        dialog.exec()"""

    content = content.replace(old_doctor_page, new_doctor_page)

    # 2. Replace Nav Buttons
    old_nav = """        # Tạo các nút điều hướng
        self.btn_home = QtWidgets.QPushButton("Trang chủ")
        self.btn_service = QtWidgets.QPushButton("Dịch vụ")
        self.btn_booking = QtWidgets.QPushButton("Đặt lịch khám")

        self.nav_buttons = [self.btn_home, self.btn_service, self.btn_booking]
        for btn in self.nav_buttons:
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(\"\"\"
                QPushButton { border:none; background:transparent; font-size: 15px; font-weight: 700; color: #64748b; padding: 10px 15px; }
                QPushButton:hover { color: #69c0a5; }
            \"\"\")
            nav_layout.addWidget(btn)"""

    new_nav = """        # Tạo các nút điều hướng
        self.btn_home = QtWidgets.QPushButton("Trang chủ")
        self.btn_service = QtWidgets.QPushButton("Dịch vụ")
        self.btn_doctor = QtWidgets.QPushButton("Bác sĩ")
        self.btn_news = QtWidgets.QPushButton("Tin tức")

        self.nav_buttons = [self.btn_home, self.btn_service, self.btn_doctor, self.btn_news]
        for btn in self.nav_buttons:
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(\"\"\"
                QPushButton { border:none; background:transparent; font-size: 15px; font-weight: 700; color: #64748b; padding: 10px 15px; }
                QPushButton:hover { color: #69c0a5; }
            \"\"\")
            nav_layout.addWidget(btn)"""

    content = content.replace(old_nav, new_nav)

    # 3. Replace Stack
    old_stack = """        # ===== STACKED WIDGET (Quản lý các trang) =====
        self.content_stack = QtWidgets.QStackedWidget()
        
        self.home_page = HomePage(self.username, self)
        self.service_page = ServicePage()
        
        self.content_stack.addWidget(self.home_page)    # Index 0
        self.content_stack.addWidget(self.service_page) # Index 1
        
        self.main_layout.addWidget(self.content_stack)

        # Kết nối sự kiện bấm nút để chuyển trang và đổi màu nút tích cực
        self.btn_home.clicked.connect(lambda: self.switch_page(0))
        self.btn_service.clicked.connect(lambda: self.switch_page(1))
        self.btn_booking.clicked.connect(lambda: self.switch_page(0))

        # Mặc định trang chủ được chọn
        self.switch_page(0)

    def switch_page(self, index):
        self.content_stack.setCurrentIndex(index)
        # Đổi màu text để người dùng biết mình đang ở trang nào
        for i, btn in enumerate([self.btn_home, self.btn_service, self.btn_booking]):
            if i == index or (index == 0 and i == 2): # Booking cũng dẫn về trang chủ
                btn.setStyleSheet("border:none; background:transparent; font-size: 15px; font-weight: 800; color: #69c0a5; border-bottom: 2px solid #69c0a5;")
            else:
                btn.setStyleSheet("border:none; background:transparent; font-size: 15px; font-weight: 700; color: #64748b;")"""

    new_stack = """        # ===== STACKED WIDGET (Quản lý các trang) =====
        self.content_stack = QtWidgets.QStackedWidget()
        
        self.home_page = HomePage(self.username, self)
        self.service_page = ServicePage()
        self.doctor_page = DoctorPage()
        self.news_page = NewsPage()
        
        self.content_stack.addWidget(self.home_page)    # Index 0
        self.content_stack.addWidget(self.service_page) # Index 1
        self.content_stack.addWidget(self.doctor_page)  # Index 2
        self.content_stack.addWidget(self.news_page)    # Index 3
        
        self.main_layout.addWidget(self.content_stack)

        # Kết nối sự kiện bấm nút để chuyển trang và đổi màu nút tích cực
        self.btn_home.clicked.connect(lambda: self.switch_page(0))
        self.btn_service.clicked.connect(lambda: self.switch_page(1))
        self.btn_doctor.clicked.connect(lambda: self.switch_page(2))
        self.btn_news.clicked.connect(lambda: self.switch_page(3))

        # Mặc định trang chủ được chọn
        self.switch_page(0)

    def switch_page(self, index):
        self.content_stack.setCurrentIndex(index)
        # Đổi màu text để người dùng biết mình đang ở trang nào
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.setStyleSheet("border:none; background:transparent; font-size: 15px; font-weight: 800; color: #69c0a5; border-bottom: 2px solid #69c0a5;")
            else:
                btn.setStyleSheet("border:none; background:transparent; font-size: 15px; font-weight: 700; color: #64748b;")"""

    content = content.replace(old_stack, new_stack)

    with open('views/patient_view.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    patch_file()
