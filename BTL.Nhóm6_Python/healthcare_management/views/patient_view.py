from PyQt6 import QtWidgets, QtCore
from controllers.service_controller import ServiceController
from controllers.doctor_controller import DoctorController


class DetailDialog(QtWidgets.QDialog):
    def __init__(self, title, fields, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(520)

        layout = QtWidgets.QVBoxLayout(self)
        card = QtWidgets.QFrame()
        card.setStyleSheet(
            "background: white; border: 1px solid #e2e8f0; border-radius: 14px;"
        )
        form = QtWidgets.QFormLayout(card)
        form.setContentsMargins(20, 20, 20, 20)
        form.setHorizontalSpacing(24)
        form.setVerticalSpacing(14)

        for label, value in fields:
            key_label = QtWidgets.QLabel(label)
            key_label.setStyleSheet("font-weight: 700; color: #334155;")

            val_label = QtWidgets.QLabel(str(value) if value is not None else "")
            val_label.setWordWrap(True)
            val_label.setStyleSheet("color: #0f172a;")
            form.addRow(key_label, val_label)

        layout.addWidget(card)

        close_btn = QtWidgets.QPushButton("Đóng")
        close_btn.setStyleSheet(
            "background: #69c0a5; color: white; border-radius: 8px; padding: 8px 16px; font-weight: 700;"
        )
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, 0, QtCore.Qt.AlignmentFlag.AlignRight)

# --- TRANG DỊCH VỤ (VIEW MỚI) ---
class LegacyServiceTablePage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20) # Thêm lề cho thoáng
        
        title = QtWidgets.QLabel("Danh sách dịch vụ y tế")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)

        desc = QtWidgets.QLabel("Nhấn vào từng dịch vụ để xem thông tin chi tiết.")
        desc.setStyleSheet("color: #64748b; font-size: 14px; margin-bottom: 8px;")
        layout.addWidget(desc)

        # Bảng danh sách dịch vụ
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Tên dịch vụ", "Giá tiền", "Mô tả"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        # Style bảng cho chuyên nghiệp giống image_ade63a.png
        self.table.setStyleSheet("""
            QTableWidget { 
                background: white; border-radius: 12px; border: 1px solid #eef0f2; 
                gridline-color: #f1f5f9; font-size: 14px;
            }
            QHeaderView::section { 
                background-color: #f8f9fa; padding: 12px; font-weight: bold; 
                border: none; border-bottom: 2px solid #69c0a5; color: #1e293b;
            }
            QTableWidget::item { padding: 15px; border-bottom: 1px solid #f1f5f9; }
        """)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        
        services_data = ServiceController.get_all()
        self.services_data = services_data
        self.table.setRowCount(len(services_data))
        for i, s in enumerate(services_data):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(s.get("service_name", ""))))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(s.get("price", ""))))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(s.get("description", ""))))
            self.table.setRowHeight(i, 50)

        self.table.cellDoubleClicked.connect(self.show_detail)
            
        layout.addWidget(self.table)
        layout.addStretch()

    def show_detail(self, row, _col):
        if row < 0 or row >= len(self.services_data):
            return

        service = self.services_data[row]
        fields = [
            ("Mã dịch vụ", service.get("service_id", "")),
            ("Tên dịch vụ", service.get("service_name", "")),
            ("Giá", service.get("price", "")),
            ("Mô tả", service.get("description", "")),
        ]
        dialog = DetailDialog("Chi tiết dịch vụ", fields, self)
        dialog.exec()


class ServicePage(QtWidgets.QWidget):
    def __init__(self, on_navigate=None):
        super().__init__()
        self.on_navigate = on_navigate
        self.setStyleSheet("background: #f8fbff; color: #0f172a;")

        root = QtWidgets.QHBoxLayout(self)
        root.setContentsMargins(24, 14, 24, 14)
        root.setSpacing(14)

        sidebar = QtWidgets.QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("QFrame { background: #ffffff; border: 1px solid #eef2f7; border-radius: 14px; }")
        sidebar_layout = QtWidgets.QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 16, 16, 16)
        sidebar_layout.setSpacing(6)

        side_items = [
            ("▦", "Tất cả dịch vụ", "all"),
            ("🩺", "Khám bệnh", "booking"),
            ("⚗", "Xét nghiệm", "lab_results"),
            ("▧", "Chẩn đoán hình ảnh", "imaging"),
            ("💉", "Tiêm chủng", "vaccination"),
            ("◎", "Tư vấn sức khỏe", "consulting"),
            ("▤", "Đơn thuốc", "prescriptions"),
            ("▭", "Thanh toán", "billing"),
            ("ⓘ", "Hỗ trợ khách hàng", "support"),
        ]
        for index, (icon, text, action) in enumerate(side_items):
            btn = QtWidgets.QPushButton(f"{icon}   {text}")
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(36)
            btn.setStyleSheet(self._service_side_button_style(index == 0))
            btn.clicked.connect(lambda _, key=action: self.handle_action(key))
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        emergency = QtWidgets.QFrame()
        emergency.setStyleSheet(
            "QFrame { background: #f0faf6; border: 1px solid #e5f5ef; border-radius: 12px; }"
            "QLabel { border: none; background: transparent; }"
        )
        emergency_layout = QtWidgets.QVBoxLayout(emergency)
        emergency_layout.setContentsMargins(14, 12, 14, 12)
        emergency_layout.setSpacing(5)
        emergency_title = QtWidgets.QLabel("Hỗ trợ khẩn cấp")
        emergency_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        emergency_title.setStyleSheet("color: #334155; font-size: 13px; font-weight: 700;")
        emergency_phone = QtWidgets.QLabel("📞  1900 1234")
        emergency_phone.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        emergency_phone.setStyleSheet("color: #49b87d; font-size: 18px; font-weight: 900;")
        emergency_note = QtWidgets.QLabel("24/7 - Miễn phí cước")
        emergency_note.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        emergency_note.setStyleSheet("color: #334155; font-size: 12px; font-weight: 600;")
        emergency_layout.addWidget(emergency_title)
        emergency_layout.addWidget(emergency_phone)
        emergency_layout.addWidget(emergency_note)
        sidebar_layout.addWidget(emergency)
        root.addWidget(sidebar)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        content = QtWidgets.QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QtWidgets.QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        top_row = QtWidgets.QHBoxLayout()
        top_row.setSpacing(14)
        banner = QtWidgets.QFrame()
        banner.setMinimumHeight(160)
        banner.setStyleSheet(
            "QFrame { background: #ffffff; border: 1px solid #eef2f7; border-radius: 14px; }"
            "QLabel { border: none; background: transparent; }"
        )
        banner_layout = QtWidgets.QHBoxLayout(banner)
        banner_layout.setContentsMargins(22, 16, 22, 16)
        banner_layout.setSpacing(14)
        banner_text = QtWidgets.QVBoxLayout()
        banner_text.setSpacing(8)
        banner_title = QtWidgets.QLabel("Dịch vụ chăm sóc sức khỏe")
        banner_title.setStyleSheet("font-size: 22px; font-weight: 900; color: #0f2a55;")
        banner_desc = QtWidgets.QLabel("Đặt lịch khám, tư vấn và quản lý sức khỏe\ndễ dàng và nhanh chóng")
        banner_desc.setStyleSheet("font-size: 13px; line-height: 140%; color: #334155;")
        banner_text.addStretch()
        banner_text.addWidget(banner_title)
        banner_text.addWidget(banner_desc)
        banner_text.addStretch()
        hero = QtWidgets.QLabel("🛡\n✚  🗓  🩺")
        hero.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        hero.setStyleSheet("font-size: 42px; color: #4fbf9f;")
        banner_layout.addLayout(banner_text, 1)
        banner_layout.addWidget(hero, 1)
        top_row.addWidget(banner, 3)

        quick = QtWidgets.QFrame()
        quick.setMinimumHeight(160)
        quick.setStyleSheet(
            "QFrame { background: #ffffff; border: 1px solid #eef2f7; border-radius: 14px; }"
            "QLabel { border: none; background: transparent; }"
        )
        quick_layout = QtWidgets.QVBoxLayout(quick)
        quick_layout.setContentsMargins(16, 14, 16, 14)
        quick_layout.setSpacing(8)
        quick_title = QtWidgets.QLabel("Truy cập nhanh")
        quick_title.setStyleSheet("font-size: 15px; font-weight: 900; color: #0f2a55;")
        quick_layout.addWidget(quick_title)
        quick_grid = QtWidgets.QGridLayout()
        quick_grid.setHorizontalSpacing(12)
        quick_grid.setVerticalSpacing(12)
        quick_items = [
            ("▣", "Đặt lịch khám", "booking", "#eaf8ef", "#47ba77"),
            ("◷", "Lịch hẹn của tôi", "appointments", "#edf2ff", "#6178ff"),
            ("⚗", "Kết quả xét nghiệm", "lab_results", "#eaf8fb", "#18a6b5"),
            ("▤", "Đơn thuốc của tôi", "prescriptions", "#eaf8fb", "#18a6b5"),
        ]
        for idx, item in enumerate(quick_items):
            quick_grid.addWidget(self._build_quick_tile(*item), idx // 2, idx % 2)
        quick_layout.addLayout(quick_grid)
        top_row.addWidget(quick, 2)
        content_layout.addLayout(top_row)

        content_layout.addWidget(self._section_title("Nhóm dịch vụ"))
        service_grid = QtWidgets.QGridLayout()
        service_grid.setHorizontalSpacing(12)
        service_grid.setVerticalSpacing(12)
        service_cards = [
            ("🩺", "Khám bệnh", "Đặt lịch khám với bác sĩ\nchuyên khoa", "Đặt lịch ngay", "booking", "#eef3ff", "#5b72f2"),
            ("⚗", "Xét nghiệm", "Đặt lịch xét nghiệm và\nxem kết quả online", "Đặt lịch ngay", "lab_results", "#f5ebff", "#b35be2"),
            ("▧", "Chẩn đoán hình ảnh", "Đặt lịch chụp X-quang,\nMRI, CT, siêu âm...", "Đặt lịch ngay", "imaging", "#eaf9ef", "#4bbd63"),
            ("💉", "Tiêm chủng", "Đặt lịch tiêm chủng cho\nbản thân và gia đình", "Đặt lịch ngay", "vaccination", "#eaf4ff", "#349adf"),
            ("💬", "Tư vấn sức khỏe", "Tư vấn trực tuyến với bác sĩ\nchuyên khoa", "Tư vấn ngay", "consulting", "#eaf4ff", "#35a4de"),
            ("▣", "Đơn thuốc", "Xem và quản lý đơn thuốc\ncủa bạn", "Xem ngay", "prescriptions", "#eaf9ef", "#34b978"),
            ("▭", "Thanh toán", "Thanh toán viện phí, dịch vụ\nnhanh chóng", "Thanh toán ngay", "billing", "#f2eaff", "#a855f7"),
            ("☎", "Hỗ trợ khách hàng", "Liên hệ hỗ trợ và giải đáp\nthắc mắc", "Liên hệ ngay", "support", "#fff0f2", "#ef5d76"),
        ]
        db_services = ServiceController.get_visible_active() or []
        if db_services:
            service_cards = []
            palette = [
                ("🩺", "#eef3ff", "#5b72f2"),
                ("⚗", "#f5ebff", "#b35be2"),
                ("▧", "#eaf9ef", "#4bbd63"),
                ("💉", "#eaf4ff", "#349adf"),
                ("▣", "#fff7ed", "#f97316"),
            ]
            for idx, service in enumerate(db_services[:12]):
                icon, bg, fg = palette[idx % len(palette)]
                name = str(service.get("service_name") or "Dịch vụ").strip()
                category = str(service.get("category") or "Chưa phân loại").strip()
                duration = service.get("duration") or 30
                price = service.get("price") or 0
                desc = f"{category}\n{duration} phút - {float(price):,.0f} đ".replace(",", ".")
                service_cards.append((icon, name, desc, "Đặt lịch ngay", "booking", bg, fg))
        for idx, item in enumerate(service_cards):
            service_grid.addWidget(self._build_service_card(*item), idx // 4, idx % 4)
        content_layout.addLayout(service_grid)

        content_layout.addWidget(self._section_title("Tiện ích khác"))
        utility_grid = QtWidgets.QGridLayout()
        utility_grid.setHorizontalSpacing(10)
        utility_items = [
            ("▰", "Hồ sơ sức khỏe", "Xem và quản lý hồ sơ\nsức khỏe của bạn", "profile", "#eaf4ff", "#2e9dde"),
            ("▦", "Lịch sử khám bệnh", "Xem lịch sử khám\nvà điều trị", "history", "#eaf4ff", "#2e9dde"),
            ("⚗", "Kết quả xét nghiệm", "Xem kết quả xét nghiệm\nvà chỉ số sức khỏe", "lab_results", "#eaf4ff", "#2e9dde"),
            ("🛡", "Bảo hiểm y tế", "Thông tin bảo hiểm y tế\nvà quyền lợi", "insurance", "#eaf4ff", "#2e9dde"),
            ("🔔", "Thông báo", "Xem thông báo và cập nhật\ntừ hệ thống", "notifications", "#eaf8ef", "#45ba72"),
        ]
        for idx, item in enumerate(utility_items):
            utility_grid.addWidget(self._build_utility_tile(*item), 0, idx)
        content_layout.addLayout(utility_grid)
        content_layout.addStretch()

        scroll.setWidget(content)
        root.addWidget(scroll, 1)

    def _service_side_button_style(self, active=False):
        if active:
            return (
                "QPushButton { background: #49b87d; color: white; border: none; border-radius: 8px;"
                " text-align: left; padding: 8px 10px; font-size: 12px; font-weight: 900; }"
            )
        return (
            "QPushButton { background: transparent; color: #0f172a; border: none; border-radius: 8px;"
            " text-align: left; padding: 8px 10px; font-size: 12px; font-weight: 700; }"
            "QPushButton:hover { background: #f1f5f9; color: #49b87d; }"
        )

    def _section_title(self, text):
        label = QtWidgets.QLabel(text)
        label.setStyleSheet("font-size: 17px; font-weight: 900; color: #0f2a55; margin-top: 2px;")
        return label

    def _build_quick_tile(self, icon, title, action, bg, fg):
        btn = QtWidgets.QPushButton(f"{icon}   {title}")
        btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(52)
        btn.setStyleSheet(
            "QPushButton { background: #ffffff; border: 1px solid #eef2f7; border-radius: 10px;"
            f" color: #0f2a55; font-size: 12px; font-weight: 900; text-align: left; padding: 9px 12px; }}"
            f"QPushButton:hover {{ background: {bg}; color: {fg}; border-color: {bg}; }}"
        )
        btn.clicked.connect(lambda: self.handle_action(action))
        return btn

    def _build_service_card(self, icon, title, desc, button_text, action, icon_bg, icon_fg):
        card = QtWidgets.QFrame()
        card.setMinimumHeight(130)
        card.setStyleSheet(
            "QFrame { background: #ffffff; border: 1px solid #eef2f7; border-radius: 12px; }"
            "QLabel { border: none; background: transparent; }"
        )
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 10)
        layout.setSpacing(6)

        top = QtWidgets.QHBoxLayout()
        icon_label = QtWidgets.QLabel(icon)
        icon_label.setFixedSize(44, 44)
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"background: {icon_bg}; color: {icon_fg}; border-radius: 9px; font-size: 22px;")
        text_col = QtWidgets.QVBoxLayout()
        text_col.setSpacing(4)
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("font-size: 13px; font-weight: 900; color: #0f2a55;")
        desc_label = QtWidgets.QLabel(desc)
        desc_label.setStyleSheet("font-size: 11px; color: #334155; line-height: 130%;")
        text_col.addWidget(title_label)
        text_col.addWidget(desc_label)
        top.addWidget(icon_label)
        top.addLayout(text_col, 1)
        layout.addLayout(top)

        action_btn = QtWidgets.QPushButton(f"{button_text}     →")
        action_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        action_btn.setMinimumHeight(30)
        action_btn.setStyleSheet(
            "QPushButton { background: #edf6f2; color: #35a978; border: none; border-radius: 8px;"
            " font-size: 11px; font-weight: 900; }"
            "QPushButton:hover { background: #dff3eb; }"
        )
        action_btn.clicked.connect(lambda: self.handle_action(action))
        layout.addWidget(action_btn)
        return card

    def _build_utility_tile(self, icon, title, desc, action, icon_bg, icon_fg):
        tile = QtWidgets.QPushButton(f"{icon}   {title}\n      {desc}")
        tile.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        tile.setMinimumHeight(72)
        tile.setStyleSheet(
            "QPushButton { background: #ffffff; border: 1px solid #eef2f7; border-radius: 10px;"
            " color: #0f2a55; font-size: 11px; font-weight: 800; text-align: left; padding: 9px; }"
            f"QPushButton:hover {{ background: {icon_bg}; color: {icon_fg}; }}"
        )
        tile.clicked.connect(lambda: self.handle_action(action))
        return tile

    def handle_action(self, action_key):
        mapped = {
            "all": "service",
            "imaging": "booking",
            "vaccination": "booking",
            "consulting": "doctor",
            "support": "support",
            "billing": "billing",
            "insurance": "insurance",
            "notifications": "notifications",
        }.get(action_key, action_key)

        if callable(self.on_navigate):
            self.on_navigate(mapped)
            return

        messages = {
            "booking": "Mở trang chủ để đặt lịch khám.",
            "appointments": "Lịch hẹn của bạn hiển thị ở trang chủ.",
            "history": "Mở lịch sử khám bệnh.",
            "doctor": "Mở danh sách bác sĩ để tư vấn.",
            "lab_results": "Kết quả xét nghiệm đang được hoàn thiện.",
            "prescriptions": "Đơn thuốc đang được hoàn thiện.",
            "billing": "Thanh toán online đang được hoàn thiện.",
            "support": "Vui lòng liên hệ hotline 1900 1234 để được hỗ trợ.",
            "profile": "Mở hồ sơ sức khỏe cá nhân.",
            "insurance": "Thông tin bảo hiểm y tế đang được hoàn thiện.",
            "notifications": "Thông báo đang được hoàn thiện.",
        }
        QtWidgets.QMessageBox.information(self, "CarePlus", messages.get(mapped, "Chức năng đang được phát triển."))


class DoctorPage(QtWidgets.QWidget):
    def __init__(
        self,
        on_navigate=None,
        on_logout=None,
        on_open_profile=None,
        on_update_profile=None,
        on_change_password=None,
        on_open_doctor_profile=None,
        on_book_doctor=None,
    ):
        super().__init__()
        self.on_navigate = on_navigate
        self.on_logout = on_logout
        self.on_open_profile = on_open_profile
        self.on_update_profile = on_update_profile
        self.on_change_password = on_change_password
        self.on_open_doctor_profile = on_open_doctor_profile
        self.on_book_doctor = on_book_doctor

        self.page_size = 6
        self.card_width = 210
        self.card_height = 255
        self._rendered_col_count = 0
        self.current_page = 1
        self.all_doctors = []
        self.filtered_doctors = []
        self.doctors_data = []
        self.last_error_message = ""

        self.facility_by_specialty = {
            "Nội khoa": "Bệnh viện Đa khoa CarePlus",
            "Nội tổng quát": "Bệnh viện Đa khoa CarePlus",
            "Ngoại khoa": "Bệnh viện Đa khoa CarePlus",
            "Tim mạch": "Bệnh viện Đa khoa CarePlus",
            "Nhi khoa": "Phòng khám Nhi CarePlus",
            "Da liễu": "Phòng khám Da liễu CarePlus",
            "Tai Mũi Họng": "Phòng khám Tai Mũi Họng",
            "Sản phụ khoa": "Bệnh viện Đa khoa CarePlus",
        }

        self.specialty_icons = {
            "Nội khoa": "🧬",
            "Nội tổng quát": "🧬",
            "Tim mạch": "❤️",
            "Nhi khoa": "👶",
            "Sản phụ khoa": "🤰",
            "Ngoại khoa": "🦴",
            "Da liễu": "✨",
            "Tai Mũi Họng": "👂",
        }

        self.filter_timer = QtCore.QTimer(self)
        self.filter_timer.setSingleShot(True)
        self.filter_timer.timeout.connect(lambda: self.apply_filters(reset_page=True))

        self.init_ui()
        self.load_doctors()

    def init_ui(self):
        root_layout = QtWidgets.QVBoxLayout(self)
        root_layout.setContentsMargins(34, 14, 34, 14)
        root_layout.setSpacing(10)

        header_layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("Đội ngũ bác sĩ")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #2c3e50;")
        header_layout.addWidget(title)

        desc = QtWidgets.QLabel(
            "Tìm kiếm và đặt lịch hẹn với các bác sĩ chuyên khoa giàu kinh nghiệm"
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #64748b; font-size: 13px;")
        header_layout.addWidget(desc)
        root_layout.addLayout(header_layout)

        body_layout = QtWidgets.QHBoxLayout()
        body_layout.setSpacing(16)
        root_layout.addLayout(body_layout, 1)

        # LEFT SIDEBAR
        left_sidebar = QtWidgets.QFrame()
        left_sidebar.setFixedWidth(230)
        left_sidebar.setStyleSheet(
            "background: white; border-radius: 12px; border: 1px solid #eef0f2;"
        )
        left_layout = QtWidgets.QVBoxLayout(left_sidebar)
        left_layout.setContentsMargins(14, 14, 14, 14)
        left_layout.setSpacing(8)

        left_title = QtWidgets.QLabel("Tìm kiếm bác sĩ")
        left_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #1e293b;")
        left_layout.addWidget(left_title)

        search_row = QtWidgets.QHBoxLayout()
        search_row.setSpacing(8)

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Tìm theo tên bác sĩ...")
        self.search_input.setStyleSheet(
            "padding: 8px; border-radius: 6px; border: 1px solid #cbd5e1;"
            "font-size: 13px; background: #f8fafc;"
        )
        search_row.addWidget(self.search_input, 1)

        self.search_icon_btn = QtWidgets.QPushButton("🔍")
        self.search_icon_btn.setFixedWidth(40)
        self.search_icon_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.search_icon_btn.setStyleSheet(
            "background: #69c0a5; color: white; border-radius: 6px;"
            "font-size: 14px; border: none;"
        )
        search_row.addWidget(self.search_icon_btn)
        left_layout.addLayout(search_row)

        specialty_options = ["Tất cả chuyên khoa"]
        hospital_options = ["Tất cả cơ sở"]
        experience_options = ["Tất cả", "Trên 10 năm", "Trên 5 năm", "Dưới 5 năm"]

        self.specialty_combo = self.create_filter_combo(
            left_layout, "Chuyên khoa", specialty_options
        )
        self.hospital_combo = self.create_filter_combo(
            left_layout, "Bệnh viện / Phòng khám", hospital_options
        )
        self.experience_combo = self.create_filter_combo(
            left_layout, "Kinh nghiệm", experience_options
        )

        self.search_btn = QtWidgets.QPushButton("Tìm kiếm")
        self.search_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.search_btn.setStyleSheet(
            "background: #69c0a5; color: white; padding: 8px; border-radius: 6px;"
            "font-weight: bold; font-size: 13px; margin-top: 6px; border: none;"
        )
        left_layout.addWidget(self.search_btn)

        self.reset_btn = QtWidgets.QPushButton("Xóa bộ lọc")
        self.reset_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.reset_btn.setStyleSheet(
            "background: white; color: #475569; padding: 8px; border-radius: 6px;"
            "font-weight: bold; font-size: 13px; border: 1px solid #cbd5e1;"
        )
        left_layout.addWidget(self.reset_btn)
        left_layout.addStretch()
        body_layout.addWidget(left_sidebar)

        # CENTER
        center_widget = QtWidgets.QWidget()
        center_layout = QtWidgets.QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(8)

        center_header = QtWidgets.QHBoxLayout()
        center_title = QtWidgets.QLabel("Danh sách bác sĩ")
        center_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e293b;")

        self.center_info = QtWidgets.QLabel("Đang tải danh sách bác sĩ...")
        self.center_info.setStyleSheet("font-size: 13px; color: #64748b;")

        self.filter_state = QtWidgets.QLabel("Đang áp dụng bộ lọc")
        self.filter_state.setStyleSheet(
            "font-size: 12px; color: #166534; background: #dcfce7;"
            "padding: 4px 8px; border-radius: 8px;"
        )
        self.filter_state.setVisible(False)

        self.sort_combo = QtWidgets.QComboBox()
        self.sort_combo.setStyleSheet(
            "padding: 6px 10px; border-radius: 6px; border: 1px solid #cbd5e1;"
            "font-size: 13px; background: white;"
        )
        self.sort_combo.addItem("Mới nhất", "newest")
        self.sort_combo.addItem("Đánh giá cao nhất", "rating")
        self.sort_combo.addItem("Nhiều đánh giá nhất", "reviews")
        self.sort_combo.addItem("Kinh nghiệm nhiều nhất", "experience")
        self.sort_combo.addItem("Tên A-Z", "name_asc")

        center_header.addWidget(center_title)
        center_header.addStretch()
        center_header.addWidget(self.filter_state)
        center_header.addWidget(self.center_info)
        center_header.addSpacing(10)
        center_header.addWidget(self.sort_combo)
        center_layout.addLayout(center_header)

        self.content_stack = QtWidgets.QStackedWidget()

        self.list_page = QtWidgets.QWidget()
        list_layout = QtWidgets.QVBoxLayout(self.list_page)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(10)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent;")

        self.grid_widget = QtWidgets.QWidget()
        self.grid_widget.setStyleSheet("background: transparent;")
        self.grid_layout = QtWidgets.QGridLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(12)
        self.scroll_area.setWidget(self.grid_widget)
        list_layout.addWidget(self.scroll_area)

        pagination_layout = QtWidgets.QHBoxLayout()
        self.prev_page_btn = QtWidgets.QPushButton("← Trang trước")
        self.next_page_btn = QtWidgets.QPushButton("Trang sau →")
        self.prev_page_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.next_page_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.prev_page_btn.setStyleSheet(
            "padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 6px;"
            "background: white; color: #334155;"
        )
        self.next_page_btn.setStyleSheet(self.prev_page_btn.styleSheet())
        self.page_label = QtWidgets.QLabel("Trang 1/1")
        self.page_label.setStyleSheet("font-size: 12px; color: #64748b;")

        pagination_layout.addWidget(self.prev_page_btn)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.next_page_btn)
        list_layout.addLayout(pagination_layout)

        self.state_page = QtWidgets.QFrame()
        self.state_page.setStyleSheet(
            "background: white; border: 1px solid #e2e8f0; border-radius: 12px;"
        )
        state_layout = QtWidgets.QVBoxLayout(self.state_page)
        state_layout.setContentsMargins(24, 24, 24, 24)
        state_layout.setSpacing(10)
        state_layout.addStretch()

        self.state_title = QtWidgets.QLabel("Đang tải danh sách bác sĩ...")
        self.state_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.state_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #334155;")

        self.state_desc = QtWidgets.QLabel("")
        self.state_desc.setWordWrap(True)
        self.state_desc.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.state_desc.setStyleSheet("font-size: 13px; color: #64748b;")

        self.retry_btn = QtWidgets.QPushButton("Tải lại")
        self.retry_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.retry_btn.setStyleSheet(
            "background: #69c0a5; color: white; padding: 10px 18px; border-radius: 8px;"
            "font-weight: bold; border: none;"
        )

        self.state_action_btn = QtWidgets.QPushButton("Đăng nhập lại")
        self.state_action_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.state_action_btn.setStyleSheet(
            "background: white; color: #2563eb; padding: 8px 16px; border-radius: 8px;"
            "font-weight: bold; border: 1px solid #93c5fd;"
        )

        state_layout.addWidget(self.state_title)
        state_layout.addWidget(self.state_desc)
        state_layout.addWidget(self.retry_btn, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        state_layout.addWidget(self.state_action_btn, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        state_layout.addStretch()

        self.content_stack.addWidget(self.list_page)
        self.content_stack.addWidget(self.state_page)
        center_layout.addWidget(self.content_stack)
        body_layout.addWidget(center_widget, 1)

        # RIGHT SIDEBAR
        right_sidebar_layout = QtWidgets.QVBoxLayout()
        right_sidebar_layout.setSpacing(12)

        quick_items = [
            ("📅", "Đặt lịch khám", "booking"),
            ("🗓️", "Lịch hẹn của tôi", "appointments"),
            ("🏥", "Lịch sử khám bệnh", "history"),
            ("🔬", "Kết quả xét nghiệm", "lab_results"),
            ("📄", "Đơn thuốc của tôi", "prescriptions"),
        ]
        right_sidebar_layout.addWidget(self.create_right_panel("Truy cập nhanh", quick_items))

        self.specialty_panel_host = QtWidgets.QWidget()
        self.specialty_panel_layout = QtWidgets.QVBoxLayout(self.specialty_panel_host)
        self.specialty_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.specialty_panel_layout.setSpacing(0)
        self.specialty_panel = None
        self.render_specialty_panel([])
        right_sidebar_layout.addWidget(self.specialty_panel_host)
        right_sidebar_layout.addStretch()

        right_widget = QtWidgets.QWidget()
        right_widget.setFixedWidth(250)
        right_widget.setLayout(right_sidebar_layout)
        body_layout.addWidget(right_widget)

        self.bind_events()

    def create_filter_combo(self, parent_layout, label_text, items):
        label = QtWidgets.QLabel(label_text)
        label.setStyleSheet(
            "font-size: 12px; font-weight: bold; color: #475569; margin-top: 2px;"
        )
        combo = QtWidgets.QComboBox()
        combo.addItems(items)
        combo.setStyleSheet(
            "padding: 7px; border-radius: 6px; border: 1px solid #cbd5e1;"
            "font-size: 13px; background: white;"
        )
        parent_layout.addWidget(label)
        parent_layout.addWidget(combo)
        return combo

    def create_right_panel(self, title_text, items, is_specialty=False):
        panel = QtWidgets.QFrame()
        panel.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #eef0f2;")
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        title = QtWidgets.QLabel(title_text)
        title.setStyleSheet("font-size: 13px; font-weight: bold; color: #1e293b; margin-bottom: 4px;")
        layout.addWidget(title)

        visible_items = items[:6] if is_specialty else items
        for item in visible_items:
            icon, text = item[0], item[1]
            meta = item[2] if len(item) > 2 else ""
            suffix = f" ({meta})" if is_specialty and meta else ""

            arrow = "" if is_specialty else "   ›"
            button = QtWidgets.QPushButton(f"{icon}  {text}{suffix}{arrow}")
            button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            button.setToolTip(f"{text}{suffix}")
            button.setMinimumHeight(26)
            button.setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Fixed,
            )
            button.setStyleSheet(
                "QPushButton {"
                " text-align: left; padding: 5px 6px; border-radius: 8px;"
                " border: 1px solid transparent; background: transparent;"
                " color: #475569; font-size: 10px;"
                "}"
                "QPushButton:hover {"
                " background: #f8fafc; border-color: #e2e8f0;"
                "}"
            )

            if is_specialty:
                button.clicked.connect(
                    lambda _, value=text: self.apply_specialty_from_sidebar(value)
                )
            else:
                button.clicked.connect(
                    lambda _, action_key=meta: self.handle_quick_access(action_key)
                )

            layout.addWidget(button)

        if is_specialty:
            view_all = QtWidgets.QPushButton("Xem tất cả →")
            view_all.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            view_all.setStyleSheet(
                "QPushButton { text-align: left; border: none; color: #2563eb;"
                " font-size: 11px; font-weight: bold; padding: 5px 2px; }"
                "QPushButton:hover { color: #1d4ed8; }"
            )
            view_all.clicked.connect(self.reset_specialty_filter)
            layout.addWidget(view_all)

        return panel

    def bind_events(self):
        self.search_btn.clicked.connect(lambda: self.apply_filters(reset_page=True))
        self.search_icon_btn.clicked.connect(lambda: self.apply_filters(reset_page=True))
        self.search_input.returnPressed.connect(lambda: self.apply_filters(reset_page=True))
        self.search_input.textChanged.connect(self.schedule_auto_filter)

        self.specialty_combo.currentIndexChanged.connect(
            lambda _: self.apply_filters(reset_page=True)
        )
        self.hospital_combo.currentIndexChanged.connect(
            lambda _: self.apply_filters(reset_page=True)
        )
        self.experience_combo.currentIndexChanged.connect(
            lambda _: self.apply_filters(reset_page=True)
        )
        self.sort_combo.currentIndexChanged.connect(lambda _: self.apply_filters())

        self.reset_btn.clicked.connect(self.reset_filters)
        self.prev_page_btn.clicked.connect(self.go_to_previous_page)
        self.next_page_btn.clicked.connect(self.go_to_next_page)
        self.retry_btn.clicked.connect(self.load_doctors)

    def schedule_auto_filter(self):
        self.filter_timer.start(300)

    def load_doctors(self):
        self.show_state(
            "loading",
            "Đang tải danh sách bác sĩ...",
            "Vui lòng đợi trong giây lát.",
        )
        QtCore.QTimer.singleShot(80, self.fetch_doctors)

    def fetch_doctors(self):
        try:
            doctors = DoctorController.get_available_for_patient()
        except PermissionError:
            self.show_state(
                "unauthorized",
                "Phiên đăng nhập đã hết hạn",
                "Vui lòng đăng nhập lại để tiếp tục sử dụng hệ thống.",
            )
            return
        except Exception as error:
            self.last_error_message = str(error)
            self.show_state(
                "error",
                "Không thể tải danh sách bác sĩ",
                "Đã xảy ra lỗi khi kết nối dữ liệu. Vui lòng thử lại.",
            )
            return

        if doctors is None:
            doctors = []

        self.all_doctors = self.decorate_doctors(doctors)
        self.refresh_filter_options()
        self.apply_filters(reset_page=True)

    def decorate_doctors(self, doctors):
        decorated = []
        for index, doctor in enumerate(doctors):
            doctor_id = doctor.get("doctor_id", 0)
            try:
                doctor_id_int = int(doctor_id)
            except (TypeError, ValueError):
                doctor_id_int = 0

            specialty = str(doctor.get("specialty", "")).strip()
            if not specialty:
                specialty = "Chưa cập nhật"

            hospital = (
                doctor.get("hospital")
                or doctor.get("facility")
                or doctor.get("workplace")
                or "Chưa cập nhật"
            )
            try:
                experience_years = int(doctor.get("experience_years") or doctor.get("experience") or 0)
            except (TypeError, ValueError):
                experience_years = 0
            try:
                rating = float(doctor.get("rating")) if doctor.get("rating") is not None else None
            except (TypeError, ValueError):
                rating = None
            try:
                reviews = int(doctor.get("reviews") or doctor.get("review_count") or 0)
            except (TypeError, ValueError):
                reviews = 0

            decorated.append(
                {
                    **doctor,
                    "specialty": specialty,
                    "experience_years": experience_years,
                    "experience_label": f"{experience_years} năm KN" if experience_years else "Chưa cập nhật",
                    "rating": rating,
                    "reviews": reviews,
                    "hospital": hospital,
                    "order": doctor_id_int,
                }
            )
        return decorated

    def refresh_filter_options(self):
        selected_specialty = self.specialty_combo.currentText()
        selected_hospital = self.hospital_combo.currentText()

        specialties = sorted(
            {
                str(doctor.get("specialty", "")).strip()
                for doctor in self.all_doctors
                if str(doctor.get("specialty", "")).strip()
            }
        )
        hospitals = sorted(
            {
                str(doctor.get("hospital", "")).strip()
                for doctor in self.all_doctors
                if str(doctor.get("hospital", "")).strip()
            }
        )

        self.replace_combo_items(
            self.specialty_combo,
            ["Tất cả chuyên khoa", *specialties],
            selected_specialty,
        )
        self.replace_combo_items(
            self.hospital_combo,
            ["Tất cả cơ sở", *hospitals],
            selected_hospital,
        )

        specialty_count = {}
        for doctor in self.all_doctors:
            specialty = str(doctor.get("specialty", "")).strip()
            if specialty:
                specialty_count[specialty] = specialty_count.get(specialty, 0) + 1

        specialty_items = [
            (
                self.specialty_icons.get(name, "🩺"),
                name,
                str(count),
            )
            for name, count in sorted(
                specialty_count.items(),
                key=lambda item: (-item[1], item[0]),
            )
        ]
        self.render_specialty_panel(specialty_items)

    def replace_combo_items(self, combo, items, selected_value):
        combo.blockSignals(True)
        combo.clear()
        combo.addItems(items)
        target_index = combo.findText(selected_value)
        combo.setCurrentIndex(target_index if target_index >= 0 else 0)
        combo.blockSignals(False)

    def render_specialty_panel(self, specialty_items):
        if self.specialty_panel is not None:
            self.specialty_panel_layout.removeWidget(self.specialty_panel)
            self.specialty_panel.deleteLater()

        self.specialty_panel = self.create_right_panel(
            "Chuyên khoa",
            specialty_items,
            is_specialty=True,
        )
        self.specialty_panel_layout.addWidget(self.specialty_panel)

    def apply_filters(self, reset_page=False):
        if reset_page:
            self.current_page = 1

        keyword = self.search_input.text().strip().lower()
        selected_specialty = self.specialty_combo.currentText()
        selected_hospital = self.hospital_combo.currentText()
        selected_experience = self.experience_combo.currentText()

        filtered = list(self.all_doctors)

        if keyword:
            filtered = [
                doctor
                for doctor in filtered
                if keyword in str(doctor.get("name", "")).lower()
            ]

        if selected_specialty != "Tất cả chuyên khoa":
            filtered = [
                doctor
                for doctor in filtered
                if str(doctor.get("specialty", "")) == selected_specialty
            ]

        if selected_hospital != "Tất cả cơ sở":
            filtered = [
                doctor
                for doctor in filtered
                if str(doctor.get("hospital", "")) == selected_hospital
            ]

        if selected_experience == "Trên 10 năm":
            filtered = [
                doctor for doctor in filtered if doctor.get("experience_years", 0) > 10
            ]
        elif selected_experience == "Trên 5 năm":
            filtered = [
                doctor for doctor in filtered if doctor.get("experience_years", 0) > 5
            ]
        elif selected_experience == "Dưới 5 năm":
            filtered = [
                doctor for doctor in filtered if doctor.get("experience_years", 0) < 5
            ]

        sort_key = self.sort_combo.currentData()
        if sort_key == "newest":
            filtered.sort(key=lambda doctor: doctor.get("order", 0), reverse=True)
        elif sort_key == "rating":
            filtered.sort(key=lambda doctor: doctor.get("rating") or 0, reverse=True)
        elif sort_key == "reviews":
            filtered.sort(key=lambda doctor: doctor.get("reviews", 0), reverse=True)
        elif sort_key == "experience":
            filtered.sort(
                key=lambda doctor: doctor.get("experience_years", 0), reverse=True
            )
        elif sort_key == "name_asc":
            filtered.sort(key=lambda doctor: str(doctor.get("name", "")).lower())

        self.filtered_doctors = filtered
        self.update_filter_state()
        self.render_current_page()

    def update_filter_state(self):
        has_filter = (
            bool(self.search_input.text().strip())
            or self.specialty_combo.currentIndex() > 0
            or self.hospital_combo.currentIndex() > 0
            or self.experience_combo.currentIndex() > 0
        )
        self.filter_state.setVisible(has_filter)

    def render_current_page(self):
        total = len(self.filtered_doctors)
        if total == 0:
            self.center_info.setText("Không tìm thấy bác sĩ")
            self.page_label.setText("Trang 0/0")
            self.prev_page_btn.setEnabled(False)
            self.next_page_btn.setEnabled(False)
            self.show_state(
                "empty",
                "Không tìm thấy bác sĩ phù hợp",
                "Vui lòng thử từ khóa hoặc bộ lọc khác.",
            )
            return

        total_pages = max((total + self.page_size - 1) // self.page_size, 1)
        if self.current_page > total_pages:
            self.current_page = total_pages

        start = (self.current_page - 1) * self.page_size
        end = min(start + self.page_size, total)
        self.doctors_data = self.filtered_doctors[start:end]

        self.clear_grid_layout()
        col_count = self._doctor_column_count()
        self._rendered_col_count = col_count
        for index, doctor in enumerate(self.doctors_data):
            card = self.create_doctor_card(doctor)
            self.grid_layout.addWidget(card, index // col_count, index % col_count)

        self.grid_layout.setRowStretch(self.grid_layout.rowCount(), 1)

        self.center_info.setText(f"Hiển thị {start + 1} - {end} trong {total} bác sĩ")
        self.page_label.setText(f"Trang {self.current_page}/{total_pages}")
        self.prev_page_btn.setEnabled(self.current_page > 1)
        self.next_page_btn.setEnabled(self.current_page < total_pages)
        self.content_stack.setCurrentWidget(self.list_page)

    def clear_grid_layout(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _doctor_column_count(self):
        viewport_width = self.scroll_area.viewport().width() if hasattr(self, "scroll_area") else 0
        card_width = self.card_width + self.grid_layout.horizontalSpacing()
        if viewport_width <= 0 or card_width <= 0:
            return 3

        return max(1, min(3, viewport_width // card_width))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not getattr(self, "doctors_data", None):
            return

        new_col_count = self._doctor_column_count()
        if new_col_count != self._rendered_col_count:
            QtCore.QTimer.singleShot(0, self.render_current_page)

    def show_state(self, state, title, description):
        self.state_title.setText(title)
        self.state_desc.setText(description)
        self.retry_btn.setVisible(state in {"loading", "error", "empty"})
        self.retry_btn.setEnabled(state != "loading")
        self.state_action_btn.setVisible(state == "unauthorized")

        try:
            self.state_action_btn.clicked.disconnect()
        except TypeError:
            pass

        if state == "unauthorized":
            if callable(self.on_logout):
                self.state_action_btn.clicked.connect(self.on_logout)
            else:
                self.state_action_btn.clicked.connect(
                    lambda: QtWidgets.QMessageBox.information(
                        self,
                        "Thông báo",
                        "Vui lòng đăng nhập lại để tiếp tục.",
                    )
                )

        self.content_stack.setCurrentWidget(self.state_page)

    def create_doctor_card(self, doctor):
        card = QtWidgets.QFrame()
        card.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #eef0f2;")
        card.setFixedSize(self.card_width, self.card_height)

        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(4)

        top_layout = QtWidgets.QHBoxLayout()

        avatar_btn = QtWidgets.QPushButton("🧑‍⚕️")
        avatar_btn.setFixedSize(44, 44)
        avatar_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        avatar_btn.setStyleSheet(
            "background: #f1f5f9; border-radius: 22px; font-size: 20px;"
            "border: 2px solid #e2e8f0;"
        )
        avatar_btn.clicked.connect(lambda: self.open_doctor_profile(doctor))

        badge = QtWidgets.QLabel(doctor.get("experience_label", "0 năm KN"))
        badge.setStyleSheet(
            "background: #d1fae5; color: #059669; border-radius: 8px; padding: 4px 8px;"
            "font-size: 10px; font-weight: bold;"
        )
        badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        top_layout.addWidget(avatar_btn)
        top_layout.addStretch()
        top_layout.addWidget(badge, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addLayout(top_layout)

        name_btn = QtWidgets.QPushButton(f"BS. {doctor.get('name', 'N/A')}")
        name_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        name_btn.setStyleSheet(
            "QPushButton {"
            " text-align: left; border: none; padding: 0;"
            " font-size: 13px; font-weight: bold; color: #1e293b;"
            "}"
            "QPushButton:hover { color: #0f766e; }"
        )
        name_btn.clicked.connect(lambda: self.open_doctor_profile(doctor))
        layout.addWidget(name_btn)

        specialty = QtWidgets.QLabel(doctor.get("specialty", "Chuyên khoa"))
        specialty.setStyleSheet("font-size: 11px; color: #059669; font-weight: bold;")
        layout.addWidget(specialty)

        hospital = QtWidgets.QLabel(doctor.get("hospital", "Bệnh viện CarePlus"))
        hospital.setStyleSheet("font-size: 10px; color: #64748b;")
        hospital.setWordWrap(True)
        layout.addWidget(hospital)

        rating = doctor.get("rating")
        rating_text = f"⭐ {rating:.1f} ({doctor.get('reviews', 0)} đánh giá)" if rating else "⭐ Chưa cập nhật"
        rating_btn = QtWidgets.QPushButton(rating_text)
        rating_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        rating_btn.setStyleSheet(
            "QPushButton { text-align: left; border: none; padding: 0;"
            " font-size: 10px; color: #d97706; }"
            "QPushButton:hover { color: #b45309; }"
        )
        rating_btn.clicked.connect(lambda: self.open_doctor_profile(doctor, open_reviews=True))
        layout.addWidget(rating_btn)

        layout.addStretch()

        view_profile_btn = QtWidgets.QPushButton("Xem hồ sơ")
        view_profile_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        view_profile_btn.setStyleSheet(
            "QPushButton {"
            " background: white; border: 1px solid #69c0a5; color: #69c0a5;"
            " border-radius: 6px; padding: 5px; font-weight: bold; font-size: 11px;"
            "}"
            "QPushButton:hover { background: #f0fdf4; }"
        )
        view_profile_btn.clicked.connect(lambda: self.open_doctor_profile(doctor))
        layout.addWidget(view_profile_btn)

        book_btn = QtWidgets.QPushButton("Đặt lịch")
        book_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        book_btn.setStyleSheet(
            "QPushButton {"
            " background: #69c0a5; border: none; color: white;"
            " border-radius: 6px; padding: 5px; font-weight: bold; font-size: 11px;"
            "}"
            "QPushButton:hover { background: #58a68e; }"
        )
        book_btn.clicked.connect(lambda: self.book_with_doctor(doctor))
        layout.addWidget(book_btn)

        view_slots_btn = QtWidgets.QPushButton("Xem lịch trống")
        view_slots_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        view_slots_btn.setStyleSheet(
            "QPushButton {"
            " background: transparent; border: none; color: #2563eb;"
            " font-size: 11px; font-weight: bold;"
            "}"
            "QPushButton:hover { color: #1d4ed8; }"
        )
        view_slots_btn.clicked.connect(lambda: self.book_with_doctor(doctor, only_view_slots=True))
        layout.addWidget(view_slots_btn)

        return card

    def open_doctor_profile(self, doctor, open_reviews=False):
        if open_reviews:
            rating = doctor.get("rating")
            review_message = (
                f"BS. {doctor.get('name', '')} hiện có {doctor.get('reviews', 0)} đánh giá, điểm trung bình {rating:.1f} sao."
                if rating
                else f"BS. {doctor.get('name', '')} chưa có dữ liệu đánh giá."
            )
            QtWidgets.QMessageBox.information(
                self,
                "Đánh giá bác sĩ",
                review_message,
            )
            return

        if callable(self.on_open_doctor_profile):
            self.on_open_doctor_profile(doctor)
            return

        self.show_detail_by_doctor(doctor)

    def show_detail_by_doctor(self, doctor):
        fields = [
            ("Mã bác sĩ", doctor.get("doctor_id", "")),
            ("Họ tên", doctor.get("name", "")),
            ("Chuyên khoa", doctor.get("specialty", "")),
            ("Cơ sở khám", doctor.get("hospital", "")),
            ("Kinh nghiệm", doctor.get("experience_label", "")),
            ("SĐT", doctor.get("phone", "")),
            ("Email", doctor.get("email", "")),
        ]
        dialog = DetailDialog("Chi tiết bác sĩ", fields, self)
        dialog.exec()

    def book_with_doctor(self, doctor, only_view_slots=False):
        if only_view_slots and callable(self.on_navigate):
            self.on_navigate("view_slots", doctor)
            return

        if callable(self.on_book_doctor):
            self.on_book_doctor(doctor)
            return

        if callable(self.on_navigate):
            self.on_navigate("booking", doctor)
            return

        message = (
            f"Mở lịch trống của BS. {doctor.get('name', '')}."
            if only_view_slots
            else f"Bắt đầu đặt lịch với BS. {doctor.get('name', '')}."
        )
        QtWidgets.QMessageBox.information(self, "Thông báo", message)

    def handle_quick_access(self, action_key):
        if action_key in {"booking", "appointments", "history"} and callable(self.on_navigate):
            self.on_navigate(action_key)
            return

        if action_key == "lab_results":
            QtWidgets.QMessageBox.information(
                self,
                "Kết quả xét nghiệm",
                "Chức năng xem kết quả xét nghiệm đang được hoàn thiện.",
            )
            return

        if action_key == "prescriptions":
            QtWidgets.QMessageBox.information(
                self,
                "Đơn thuốc của tôi",
                "Chức năng xem đơn thuốc đang được hoàn thiện.",
            )
            return

        QtWidgets.QMessageBox.information(
            self,
            "Thông báo",
            "Chức năng đang được cập nhật.",
        )

    def apply_specialty_from_sidebar(self, specialty_name):
        index = self.specialty_combo.findText(specialty_name)
        if index >= 0:
            self.specialty_combo.setCurrentIndex(index)

    def reset_specialty_filter(self):
        self.specialty_combo.setCurrentIndex(0)

    def reset_filters(self):
        self.search_input.clear()
        self.specialty_combo.setCurrentIndex(0)
        self.hospital_combo.setCurrentIndex(0)
        self.experience_combo.setCurrentIndex(0)
        self.sort_combo.setCurrentIndex(0)
        self.apply_filters(reset_page=True)

    def go_to_previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.render_current_page()

    def go_to_next_page(self):
        total_pages = max((len(self.filtered_doctors) + self.page_size - 1) // self.page_size, 1)
        if self.current_page < total_pages:
            self.current_page += 1
            self.render_current_page()

    def show_detail(self, row, _col):
        if row < 0 or row >= len(self.doctors_data):
            return
        self.show_detail_by_doctor(self.doctors_data[row])


class NewsPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)

        title = QtWidgets.QLabel("Tin tức & tư vấn sức khỏe")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #2c3e50;")
        layout.addWidget(title)

        self.news_items = [
            {
                "title": "5 dấu hiệu cần đi khám tổng quát định kỳ",
                "summary": "Những biểu hiện cơ thể cảnh báo bạn nên kiểm tra sức khỏe sớm.",
                "content": "Nếu bạn thường xuyên mệt mỏi, rối loạn giấc ngủ, giảm tập trung hoặc thay đổi cân nặng bất thường, hãy đi khám sớm để phát hiện nguy cơ tiềm ẩn.",
            },
            {
                "title": "Lưu ý trước khi xét nghiệm máu",
                "summary": "Chuẩn bị đúng giúp kết quả xét nghiệm chính xác hơn.",
                "content": "Bạn nên nhịn ăn từ 8-12 giờ tùy loại xét nghiệm, ngủ đủ giấc và hạn chế dùng chất kích thích trước ngày khám.",
            },
            {
                "title": "Chương trình tiêm chủng theo độ tuổi",
                "summary": "Cập nhật lịch tiêm chủng giúp phòng bệnh hiệu quả.",
                "content": "Người lớn cần tiêm nhắc một số vaccine định kỳ. Trẻ em cần bám sát lịch tiêm để tăng miễn dịch cộng đồng.",
            },
        ]

        desc = QtWidgets.QLabel(
            "Nhấn vào từng mục để xem chi tiết. Một số chuyên mục nâng cao đang được bổ sung nội dung."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #64748b; font-size: 14px; margin-bottom: 8px;")
        layout.addWidget(desc)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setStyleSheet(
            """
            QListWidget { background: white; border: 1px solid #eef0f2; border-radius: 12px; padding: 6px; }
            QListWidget::item { padding: 12px; border-bottom: 1px solid #f1f5f9; }
            QListWidget::item:selected { background: #e1f2ee; color: #1f2937; border-radius: 8px; }
            """
        )

        for item in self.news_items:
            self.list_widget.addItem(f"📰 {item['title']}\n{item['summary']}")

        self.list_widget.itemDoubleClicked.connect(self.show_detail)
        layout.addWidget(self.list_widget)

        note = QtWidgets.QLabel(
            "Chuyên mục video tư vấn và livestream bác sĩ đang trong quá trình phát triển."
        )
        note.setStyleSheet(
            "color: #92400e; background: #fffbeb; border: 1px solid #fde68a; border-radius: 10px; padding: 10px;"
        )
        layout.addWidget(note)
        layout.addStretch()

    def show_detail(self, item):
        row = self.list_widget.row(item)
        if row < 0 or row >= len(self.news_items):
            return

        news = self.news_items[row]
        fields = [
            ("Tiêu đề", news["title"]),
            ("Tóm tắt", news["summary"]),
            ("Nội dung", news["content"]),
        ]
        dialog = DetailDialog("Chi tiết tin tức", fields, self)
        dialog.exec()

# --- TRANG LỊCH SỬ KHÁM ---
class HistoryPage(QtWidgets.QWidget):
    def __init__(self, patient_id, user_context=None):
        super().__init__()
        self.patient_id = patient_id
        self.user_context = user_context
        self.patient_data = {}
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)
        
        title = QtWidgets.QLabel("Lịch sử khám bệnh")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Ngày khám", "Bác sĩ", "Chẩn đoán", "Điều trị"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget { background: white; border-radius: 12px; border: 1px solid #eef0f2; font-size: 14px; color: #1f2937; }
            QHeaderView::section { background-color: #f8f9fa; padding: 12px; font-weight: bold; border: none; border-bottom: 2px solid #69c0a5; }
            QTableWidget::item { padding: 15px; border-bottom: 1px solid #f1f5f9; }
        """)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        
        from controllers.patient_controller import PatientController
        records = PatientController.get_medical_history(self.patient_id, self.user_context)
        
        self.table.setRowCount(len(records))
        for i, r in enumerate(records):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(r.get("created_at", ""))))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(r.get("doctor_name", ""))))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(r.get("diagnosis", ""))))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(r.get("treatment", ""))))
            self.table.setRowHeight(i, 50)
            
        layout.addWidget(self.table)
        layout.addStretch()

# --- TRANG HỒ SƠ CÁ NHÂN ---
class ProfilePage(QtWidgets.QWidget):
    def __init__(self, patient_id, user_context=None):
        super().__init__()
        self.patient_id = patient_id
        self.user_context = user_context
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)
        
        title = QtWidgets.QLabel("Hồ sơ cá nhân")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        form_widget = QtWidgets.QWidget()
        form_widget.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #eef0f2; padding: 20px;")
        form_layout = QtWidgets.QFormLayout(form_widget)
        
        self.name_input = QtWidgets.QLineEdit()
        self.dob_input = QtWidgets.QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.gender_input = QtWidgets.QComboBox()
        self.gender_input.addItems(["Nam", "Nữ"])
        self.phone_input = QtWidgets.QLineEdit()
        self.address_input = QtWidgets.QLineEdit()
        
        for w in [self.name_input, self.dob_input, self.gender_input, self.phone_input, self.address_input]:
            w.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #ddd; font-size: 14px;")
        
        form_layout.addRow("Họ tên:", self.name_input)
        form_layout.addRow("Ngày sinh:", self.dob_input)
        form_layout.addRow("Giới tính:", self.gender_input)
        form_layout.addRow("SĐT:", self.phone_input)
        form_layout.addRow("Địa chỉ:", self.address_input)
        
        self.load_data()
        
        save_btn = QtWidgets.QPushButton("Cập nhật thông tin")
        save_btn.setStyleSheet("background: #69c0a5; color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold; font-size: 14px;")
        save_btn.clicked.connect(self.save_data)
        
        layout.addWidget(form_widget)
        layout.addWidget(save_btn, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addStretch()
        
    def load_data(self):
        from controllers.patient_controller import PatientController
        p = PatientController.get_by_id(self.patient_id, self.user_context)
        if p:
            self.patient_data = dict(p)
            self.name_input.setText(str(p.get("name", "")))
            self.phone_input.setText(str(p.get("phone", "")))
            self.address_input.setText(str(p.get("address", "")))
            self.gender_input.setCurrentText(str(p.get("gender", "Nam")))
            if p.get("dob"):
                self.dob_input.setDate(QtCore.QDate.fromString(str(p.get("dob")), "yyyy-MM-dd"))
                
    def save_data(self):
        from controllers.patient_controller import PatientController

        payload = dict(self.patient_data or {})
        payload.update(
            {
                "name": self.name_input.text().strip(),
                "dob": self.dob_input.date().toString("yyyy-MM-dd"),
                "gender": self.gender_input.currentText(),
                "phone": self.phone_input.text().strip(),
                "address": self.address_input.text().strip(),
            }
        )
        result = PatientController.update_with_status(self.patient_id, payload, self.user_context)
        if result.get("status"):
            self.patient_data.update(payload)
            QtWidgets.QMessageBox.information(self, "Thành công", "Đã cập nhật thông tin cá nhân!")
        else:
            QtWidgets.QMessageBox.warning(self, "Thất bại", result.get("message") or "Không thể cập nhật thông tin. Vui lòng thử lại.")

# --- TRANG CHỦ (GIỮ NGUYÊN NỘI DUNG CỦA BẠN) ---
class HomePage(QtWidgets.QWidget):
    def __init__(self, username, parent_view):
        super().__init__()
        self.username = username
        self.parent_view = parent_view 
        self.selected_time = None
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)

        # ===== HERO =====
        hero = QtWidgets.QFrame()
        hero.setStyleSheet("background: #e1f2ee; border-radius: 20px;")
        hero_layout = QtWidgets.QVBoxLayout(hero)
        hero_layout.setContentsMargins(30, 30, 30, 30)
        
        title = QtWidgets.QLabel("Chăm sóc sức khỏe chuyên nghiệp")
        title.setStyleSheet("font-size: 30px; font-weight: 800; color: #2c3e50;")
        hero_layout.addWidget(title)
        
        sub_title = QtWidgets.QLabel("Đặt lịch khám nhanh chóng với bác sĩ hàng đầu")
        sub_title.setStyleSheet("font-size: 16px; color: #64748b;")
        hero_layout.addWidget(sub_title)
        layout.addWidget(hero)

        # ===== BOOKING =====
        card = QtWidgets.QFrame()
        card.setStyleSheet("background:white; border-radius:15px; border:1px solid #eef0f2;")
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        
        row = QtWidgets.QHBoxLayout()
        self.doctor = QtWidgets.QComboBox()
        self.refresh_doctor_choices()
        self.doctor.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #ddd;")
        
        self.date = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.date.setCalendarPopup(True)
        self.date.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #ddd;")
        
        row.addWidget(self.doctor)
        row.addWidget(self.date)
        card_layout.addLayout(row)

        time_layout = QtWidgets.QGridLayout()
        self.buttons = []
        from controllers.appointment_controller import AppointmentController
        for idx, t in enumerate(AppointmentController._default_slot_times()):
            btn = QtWidgets.QPushButton(t)
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, b=btn: self.parent_view.select_time(b, self))
            btn.setStyleSheet("QPushButton { background:#f1f5f9; border-radius:8px; padding:12px; font-weight: bold; border: none; } QPushButton:hover { background: #e2e8f0; }")
            self.buttons.append(btn)
            row_idx = idx // 4
            col_idx = idx % 4
            time_layout.addWidget(btn, row_idx, col_idx)
        card_layout.addLayout(time_layout)

        book = QtWidgets.QPushButton("Đặt lịch ngay")
        book.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        book.setStyleSheet("QPushButton { background: #69c0a5; color:white; padding:12px; border-radius:10px; font-weight: 800; font-size: 15px; border: none; } QPushButton:hover { background: #58a68e; }")
        book.clicked.connect(lambda: self.parent_view.book(self))
        card_layout.addWidget(book)
        layout.addWidget(card)

        # ===== FEATURES =====
        feature_layout = QtWidgets.QHBoxLayout()
        for text in ["📅 Đặt lịch dễ dàng", "📜 Lịch sử khám", "💊 Đơn thuốc"]:
            box = QtWidgets.QFrame()
            box.setStyleSheet("background:white; border:1px solid #eef0f2; border-radius:12px;")
            v = QtWidgets.QVBoxLayout(box)
            lbl_title = QtWidgets.QLabel(text)
            lbl_title.setStyleSheet("font-weight: 800; font-size: 14px; color: #1e293b;")
            v.addWidget(lbl_title)
            v.addWidget(QtWidgets.QLabel("Mô tả chức năng chi tiết..."))
            feature_layout.addWidget(box)
        layout.addLayout(feature_layout)

    @staticmethod
    def _is_active_doctor(doctor):
        value = doctor.get("is_active", True)
        if isinstance(value, str):
            return value.lower() not in {"0", "false", "no", "ngung", "inactive"}
        return bool(value)

    @staticmethod
    def _normalize_work_status(doctor):
        raw = str(doctor.get("work_status") or "").strip().upper()
        mapping = {
            "WORKING": "ĐANG LÀM VIỆC",
            "ON_LEAVE": "NGHỈ PHÉP",
            "LEFT": "ĐÃ NGHỈ VIỆC",
            "ACTIVE": "ĐANG LÀM VIỆC",
            "TEMPORARILY_INACTIVE": "TẠM NGHỈ",
            "RESIGNED": "ĐÃ NGHỈ VIỆC",
            "ĐANG LÀM VIỆC": "ĐANG LÀM VIỆC",
            "NGHỈ PHÉP": "NGHỈ PHÉP",
            "TẠM NGHỈ": "TẠM NGHỈ",
            "ĐÃ NGHỈ VIỆC": "ĐÃ NGHỈ VIỆC",
        }
        return mapping.get(raw, raw)

    def refresh_doctor_choices(self):
        selected_doctor_id = self.doctor.currentData() if hasattr(self, "doctor") else None
        self.doctor.clear()

        doctor_rows = DoctorController.get_all() or []
        available = []
        for doctor in doctor_rows:
            if not doctor.get("name"):
                continue
            if not self._is_active_doctor(doctor):
                continue
            work_status = self._normalize_work_status(doctor)
            if work_status in {"NGHỈ PHÉP", "TẠM NGHỈ", "ĐÃ NGHỈ VIỆC"}:
                continue
            available.append(doctor)

        for doctor in available:
            self.doctor.addItem(f"BS {doctor.get('name')}", doctor.get("doctor_id"))

        if self.doctor.count() == 0:
            self.doctor.addItem("Chưa có bác sĩ khả dụng", None)
            self.doctor.setEnabled(False)
        else:
            self.doctor.setEnabled(True)

        if selected_doctor_id is not None:
            idx = self.doctor.findData(selected_doctor_id)
            if idx >= 0:
                self.doctor.setCurrentIndex(idx)

    def select_doctor_by_id(self, doctor_id):
        self.refresh_doctor_choices()
        idx = self.doctor.findData(doctor_id)
        if idx >= 0:
            self.doctor.setCurrentIndex(idx)
            return True
        return False

# --- VIEW CHÍNH ĐIỀU HƯỚNG ---
class PatientView(QtWidgets.QWidget):
    def __init__(self, parent=None, username="Guest"):
        super().__init__(parent)
        self.username = username
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # ===== NAVBAR =====
        navbar = QtWidgets.QFrame()
        navbar.setFixedHeight(70)
        navbar.setStyleSheet("background:white; border-bottom: 1px solid #f1f5f9;")
        nav_layout = QtWidgets.QHBoxLayout(navbar)
        nav_layout.setContentsMargins(40, 0, 40, 0)

        logo = QtWidgets.QPushButton("⊕ CarePlus")
        logo.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        logo.setStyleSheet(
            "QPushButton {"
            " color: #69c0a5; font-size: 24px; font-weight: 900;"
            " border: none; background: transparent; padding: 0;"
            "}"
            "QPushButton:hover { color: #58a68e; }"
        )
        logo.clicked.connect(lambda: self.switch_page(0))
        nav_layout.addWidget(logo)
        nav_layout.addStretch()

        # Tạo các nút điều hướng
        self.btn_home = QtWidgets.QPushButton("Trang chủ")
        self.btn_service = QtWidgets.QPushButton("Dịch vụ")
        self.btn_doctor = QtWidgets.QPushButton("Bác sĩ")
        self.btn_news = QtWidgets.QPushButton("Tin tức")

        self.nav_buttons = [self.btn_home, self.btn_service, self.btn_doctor, self.btn_news]
        for btn in self.nav_buttons:
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton { border:none; background:transparent; font-size: 15px; font-weight: 700; color: #64748b; padding: 10px 15px; }
                QPushButton:hover { color: #69c0a5; }
            """)
            nav_layout.addWidget(btn)

        nav_layout.addStretch()
        self.user_info_btn = QtWidgets.QPushButton(f"👤 {username} ▿")
        self.user_info_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.user_info_btn.setStyleSheet(
            "QPushButton {"
            " border: none; background: #f0f7f6; border-radius: 12px;"
            " padding: 8px 12px; font-weight: 700; color: #1e293b;"
            "}"
            "QPushButton:hover { background: #e1f2ee; }"
        )
        self.user_info_btn.clicked.connect(self.show_user_menu)
        nav_layout.addWidget(self.user_info_btn)
        
        self.logout_btn = QtWidgets.QPushButton("Đăng xuất")
        self.logout_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.logout_btn.setStyleSheet("background:#ff7875; color:white; border-radius:8px; padding: 8px 18px; font-weight: bold; border: none;")
        self.logout_btn.clicked.connect(self.logout)
        nav_layout.addWidget(self.logout_btn)
        
        self.main_layout.addWidget(navbar)

        # ===== STACKED WIDGET (Quản lý các trang) =====
        self.content_stack = QtWidgets.QStackedWidget()
        
        self.home_page = HomePage(self.username, self)
        self.service_page = ServicePage(on_navigate=self.handle_doctor_navigation)
        self.doctor_page = DoctorPage(
            on_navigate=self.handle_doctor_navigation,
            on_logout=self.logout,
            on_open_profile=lambda: self.show_account_placeholder("Hồ sơ cá nhân"),
            on_update_profile=lambda: self.show_account_placeholder("Cập nhật thông tin"),
            on_change_password=lambda: self.show_account_placeholder("Đổi mật khẩu"),
        )
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
        if index == 0 and hasattr(self, "home_page"):
            self.home_page.refresh_doctor_choices()
        # Đổi màu text để người dùng biết mình đang ở trang nào
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.setStyleSheet("border:none; background:transparent; font-size: 15px; font-weight: 800; color: #69c0a5; border-bottom: 2px solid #69c0a5;")
            else:
                btn.setStyleSheet("border:none; background:transparent; font-size: 15px; font-weight: 700; color: #64748b;")

    def handle_doctor_navigation(self, action_key, doctor=None):
        if action_key == "home":
            self.switch_page(0)
            return
        if action_key == "service":
            self.switch_page(1)
            return
        if action_key == "doctor":
            self.switch_page(2)
            return
        if action_key == "news":
            self.switch_page(3)
            return

        if action_key == "booking":
            self.switch_page(0)
            doctor_name = doctor.get("name", "") if isinstance(doctor, dict) else ""
            if isinstance(doctor, dict) and doctor.get("doctor_id") is not None:
                self.home_page.select_doctor_by_id(doctor.get("doctor_id"))
            message = (
                f"Đã chuyển về Trang chủ để bạn đặt lịch với BS. {doctor_name}."
                if doctor_name
                else "Đã chuyển về Trang chủ để bạn đặt lịch khám."
            )
            QtWidgets.QMessageBox.information(self, "Đặt lịch khám", message)
            return

        if action_key == "view_slots":
            self.switch_page(0)
            doctor_name = doctor.get("name", "") if isinstance(doctor, dict) else ""
            QtWidgets.QMessageBox.information(
                self,
                "Lịch trống bác sĩ",
                f"Đã chuyển về Trang chủ để xem lịch trống của BS. {doctor_name}.",
            )
            return

        if action_key in {"appointments", "history"}:
            QtWidgets.QMessageBox.information(
                self,
                "Thông báo",
                "Danh sách lịch hẹn và lịch sử khám đầy đủ đang có trên giao diện bệnh nhân chính.",
            )
            return

        if action_key == "profile":
            self.show_account_placeholder("Hồ sơ cá nhân")
            return
        if action_key == "update_profile":
            self.show_account_placeholder("Cập nhật thông tin")
            return
        if action_key == "change_password":
            self.show_account_placeholder("Đổi mật khẩu")
            return

        service_messages = {
            "lab_results": ("Kết quả xét nghiệm", "Kết quả xét nghiệm online đang được hoàn thiện."),
            "prescriptions": ("Đơn thuốc", "Đơn thuốc của bạn đang được hoàn thiện."),
            "billing": ("Thanh toán", "Thanh toán online đang trong quá trình phát triển."),
            "support": ("Hỗ trợ khách hàng", "Hotline hỗ trợ khẩn cấp: 1900 1234."),
            "insurance": ("Bảo hiểm y tế", "Thông tin bảo hiểm y tế và quyền lợi đang được cập nhật."),
            "notifications": ("Thông báo", "Thông báo lịch khám, kết quả và thanh toán sẽ được hiển thị trong phiên bản tiếp theo."),
        }
        if action_key in service_messages:
            title, message = service_messages[action_key]
            QtWidgets.QMessageBox.information(self, title, message)
            return

    def show_user_menu(self):
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet(
            "QMenu { background: white; color: #333; border: 1px solid #eee; }"
            "QMenu::item { padding: 10px 24px; }"
            "QMenu::item:selected { background: #f8faff; color: #69c0a5; }"
        )

        profile_act = menu.addAction("👤 Hồ sơ cá nhân")
        update_act = menu.addAction("🛠️ Cập nhật thông tin")
        password_act = menu.addAction("🔒 Đổi mật khẩu")
        menu.addSeparator()
        logout_act = menu.addAction("🚪 Đăng xuất")

        profile_act.triggered.connect(lambda: self.handle_doctor_navigation("profile"))
        update_act.triggered.connect(lambda: self.handle_doctor_navigation("update_profile"))
        password_act.triggered.connect(lambda: self.handle_doctor_navigation("change_password"))
        logout_act.triggered.connect(self.logout)

        menu.exec(self.user_info_btn.mapToGlobal(QtCore.QPoint(0, self.user_info_btn.height() + 5)))

    def show_account_placeholder(self, title):
        QtWidgets.QMessageBox.information(
            self,
            title,
            f"Chức năng '{title}' đang được triển khai chi tiết trên giao diện bệnh nhân chính.",
        )

    def logout(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "Đăng xuất",
            "Bạn có chắc muốn đăng xuất không?",
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No,
        )

        if reply != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        self.close()
        from views.login_view import LoginView

        self.login_window = LoginView()
        self.login_window.show()

    # Logic cũ giữ nguyên
    def select_time(self, btn, page):
        for b in page.buttons:
            b.setStyleSheet("QPushButton { background:#f1f5f9; border-radius:8px; padding:12px; font-weight: bold; border: none; } QPushButton:hover { background: #e2e8f0; }")
        btn.setStyleSheet("background:#69c0a5; color:white; border-radius:8px; padding:12px; font-weight: bold; border: none;")
        page.selected_time = btn.text()

    def book(self, page):
        QtWidgets.QMessageBox.information(
            self,
            "Thông báo",
            "Luồng đặt lịch đã được nâng cấp trên giao diện bệnh nhân chính. Vui lòng sử dụng menu mới để đặt lịch chính xác.",
        )
