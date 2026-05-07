from PyQt6 import QtWidgets, QtCore, QtGui
import sys

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

        menu_items = [("🏠", "Dashboard"), ("👥", "Bệnh nhân"), ("📅", "Lịch hẹn"), ("📂", "Hồ sơ bệnh án"), ("💊", "Đơn thuốc"), ("📊", "Báo cáo"), ("⚙️", "Cài đặt")]
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

        from controllers.appointment_controller import AppointmentController
        from database.db import fetch_one
        appointments = AppointmentController.get_by_doctor(self.user_data.get("doctor_id"))
        today_count = len(appointments)
        
        doctor_id = self.user_data.get("doctor_id")
        tp_query = fetch_one("SELECT COUNT(DISTINCT patient_id) as c FROM Appointments WHERE doctor_id=?", (doctor_id,))
        total_patients = tp_query["c"] if isinstance(tp_query, dict) else (tp_query[0] if tp_query else 0)
        
        ta_query = fetch_one("SELECT COUNT(*) as c FROM Appointments WHERE doctor_id=?", (doctor_id,))
        total_appts = ta_query["c"] if isinstance(ta_query, dict) else (ta_query[0] if ta_query else 0)

        self.stats_layout = QtWidgets.QHBoxLayout(); self.stats_layout.setSpacing(25)
        stats_data = [("📄", "Hẹn khám", f"{today_count:02d}", "#e6f2ff", "#007bff"), ("👥", "Bệnh nhân", f"{total_patients:02d}", "#fff4e6", "#fd7e14"), ("🗓️", "Tổng lịch hẹn", f"{total_appts:02d}", "#e6f9f1", "#28a745"), ("🔔", "Thông báo", "0", "#f9e6e6", "#dc3545")]
        for icon, title, value, bg, txt in stats_data:
            card = self.create_stat_card(icon, title, value, bg, txt)
            self.stats_layout.addWidget(card)
        page_dashboard_layout.addLayout(self.stats_layout)

        # Container bảng
        self.table_container = QtWidgets.QFrame()
        self.table_container.setStyleSheet("background: white; border-radius: 20px;")
        self.table_main_layout = QtWidgets.QVBoxLayout(self.table_container)
        self.table_main_layout.setContentsMargins(20, 20, 20, 20)

        self.lbl_table_title = QtWidgets.QLabel("Danh sách lịch hẹn hôm nay")
        self.lbl_table_title.setStyleSheet("font-size: 18px; font-weight: 800; color: #2c3e50; margin-bottom: 10px;")
        self.table_main_layout.addWidget(self.lbl_table_title)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Giờ", "Bệnh nhân", "Triệu chứng", "Bác sĩ", "Trạng thái"])
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

        self.table.setRowCount(len(appointments))
        for row, appt in enumerate(appointments):
            import datetime
            if isinstance(appt["appointment_date"], datetime.datetime):
                dt_str = appt["appointment_date"].strftime("%d/%m/%Y %H:%M")
            else:
                dt_str = str(appt["appointment_date"])
                
            ten = appt.get("patient_name", "")
            tc = appt.get("patient_phone", "")
            bs = self.user_data.get("name", "")
            tt = appt.get("status", "pending")
            
            for col, text in enumerate([dt_str, ten, tc, bs]):
                item = QtWidgets.QTableWidgetItem(str(text))
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.table.setItem(row, col, item)
            
            cb_status = QtWidgets.QComboBox()
            cb_status.addItems(["pending", "completed", "cancelled"])
            cb_status.setCurrentText(tt)
            
            if tt == "completed":
                cb_status.setStyleSheet("background: #e1f2ee; color: #69c0a5; font-weight: bold; border-radius: 5px;")
            elif tt == "cancelled":
                cb_status.setStyleSheet("background: #fde8e8; color: #e02424; font-weight: bold; border-radius: 5px;")
            else:
                cb_status.setStyleSheet("background: #fff4e6; color: #fd7e14; font-weight: bold; border-radius: 5px;")
                
            cb_status.currentTextChanged.connect(lambda text, a_id=appt["appointment_id"]: AppointmentController.update_status(a_id, text))
            self.table.setCellWidget(row, 4, cb_status)

        for i in range(self.table.rowCount()): self.table.setRowHeight(i, 55)
        self.table_main_layout.addWidget(self.table)
        page_dashboard_layout.addWidget(self.table_container)
        page_dashboard_layout.addStretch()

        self.content_stack.addWidget(self.page_dashboard)

        # Các trang placeholder khác
        from views.doctor_management_views import MedicalRecordView, PrescriptionView
        
        self.page_medical_record = MedicalRecordView(self.user_data.get("doctor_id"))
        self.page_prescription = PrescriptionView(self.user_data.get("doctor_id"))
        
        for i in range(1, 7):
            if i == 3:
                self.content_stack.addWidget(self.page_medical_record)
            elif i == 4:
                self.content_stack.addWidget(self.page_prescription)
            else:
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
        from views.admin_management_views import PatientManagementView, DoctorManagementView
        self.page_patient_mgmt = PatientManagementView()
        self.page_doctor_mgmt = DoctorManagementView()
        
        self.content_stack.addWidget(self.page_patient_mgmt) # Index 1: Quản lý bệnh nhân
        self.content_stack.addWidget(self.page_doctor_mgmt) # Index 2: Quản lý bác sĩ
        
        for i in range(3, 9):
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