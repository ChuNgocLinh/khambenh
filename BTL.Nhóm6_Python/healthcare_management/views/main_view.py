from PyQt6 import QtWidgets, QtCore, QtGui
from views.dashboard_view import DashboardView, AdminDashboardView 
from models.doctor_model import DoctorModel
from controllers.appointment_controller import AppointmentController

class MainView(QtWidgets.QMainWindow):
    def __init__(self, role, user_data, login_window=None):
        super().__init__()
        self.role = str(role).lower().strip() 
        self.user_data = user_data if isinstance(user_data, dict) else {"username": "Unknown", "patient_id": 1, "doctor_id": 1}
        self.username = self.user_data.get("name") or self.user_data.get("username")
        
        # QUAN TRỌNG: Lưu tham chiếu cửa sổ đăng nhập
        self.login_window = login_window 
        self.selected_time = "09:00"

        self.setWindowTitle(f"CarePlus - {self.role.upper()}")
        self.resize(1150, 850) 

        central = QtWidgets.QWidget()
        central.setStyleSheet("background-color: #f8faff;") 
        self.setCentralWidget(central)

        self.main_layout = QtWidgets.QVBoxLayout(central)
        self.main_layout.setContentsMargins(0, 0, 0, 0) 
        self.main_layout.setSpacing(0)

        if self.role == "admin":
            self.admin_dashboard = AdminDashboardView(self.user_data)
            self.admin_dashboard.btn_logout.clicked.connect(self.logout)
            self.main_layout.addWidget(self.admin_dashboard)
        elif self.role == "doctor":
            self.doctor_dashboard = DashboardView(self.user_data)
            self.doctor_dashboard.user_name_lbl.setText(f"Bác sĩ {self.username} ▿")
            self.doctor_dashboard.btn_logout.clicked.connect(self.logout)
            self.main_layout.addWidget(self.doctor_dashboard)
        else:
            self.init_patient_ui()

    def init_patient_ui(self):
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        
        container = QtWidgets.QWidget()
        container.setStyleSheet("background-color: #f8faff;")
        container_layout = QtWidgets.QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 40)
        container_layout.setSpacing(20)

        container_layout.addWidget(self.create_navbar())

        main_content_widget = QtWidgets.QWidget()
        main_content_layout = QtWidgets.QVBoxLayout(main_content_widget)
        main_content_layout.setContentsMargins(40, 10, 40, 10)
        main_content_layout.setSpacing(20)

        # 2. Hero Banner
        hero_bg = QtWidgets.QFrame()
        hero_bg.setFixedHeight(300)
        hero_bg.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #eefaf9, stop:1 #ffffff); border-radius: 30px;")
        hero_h_layout = QtWidgets.QHBoxLayout(hero_bg)
        hero_h_layout.setContentsMargins(50, 20, 50, 20)

        txt_layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("Chăm sóc sức khỏe\nchuyên nghiệp")
        title.setStyleSheet("font-size: 38px; font-weight: 900; color: #1a2a3a;")
        sub = QtWidgets.QLabel("Đặt lịch khám bệnh dễ dàng và nhanh chóng\nvới đội ngũ bác sĩ hàng đầu tại CarePlus")
        sub.setStyleSheet("font-size: 16px; color: #5f6c7b;")
        txt_layout.addStretch(); txt_layout.addWidget(title); txt_layout.addWidget(sub); txt_layout.addStretch()
        
        doc_img = QtWidgets.QLabel()
        pix = QtGui.QPixmap("assets/bg.jpg")
        if not pix.isNull():
            doc_img.setPixmap(pix.scaled(400, 400, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
        else:
            doc_img.setText("👨‍⚕️")
            doc_img.setStyleSheet("font-size: 150px;")
        
        hero_h_layout.addLayout(txt_layout)
        hero_h_layout.addWidget(doc_img, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        main_content_layout.addWidget(hero_bg)

        # 3. Grid Dashboard
        grid_layout = QtWidgets.QHBoxLayout()
        grid_layout.setSpacing(25)

        # --- CỘT TRÁI: ĐẶT LỊCH ---
        booking_card = QtWidgets.QFrame()
        booking_card.setFixedWidth(550)
        booking_card.setStyleSheet("background: white; border-radius: 20px; border: 1px solid #f0f0f0;")
        bk_v = QtWidgets.QVBoxLayout(booking_card)
        bk_v.setContentsMargins(25, 25, 25, 25); bk_v.setSpacing(15)

        bk_title = QtWidgets.QLabel("Đặt lịch khám")
        bk_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1a2a3a; border:none;")
        bk_v.addWidget(bk_title)

        row_cb = QtWidgets.QHBoxLayout()
        
        combo_style = """
            QComboBox { 
                padding: 10px; border: 1px solid #eee; border-radius: 10px; 
                background: #f8faff; color: #333; font-size: 14px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #333;
                selection-background-color: #69c0a5;
                selection-color: white;
                outline: none;
                border: 1px solid #eee;
            }
            QDateEdit { 
                padding: 10px; border: 1px solid #eee; border-radius: 10px; 
                background: #f8faff; color: #333; font-size: 14px;
            }
        """
        
        self.cb_doc = QtWidgets.QComboBox()
        docs = DoctorModel.get_all()
        for doc in docs:
            self.cb_doc.addItem(f"BS {doc['name']}", userData=doc["doctor_id"])
        self.cb_doc.setStyleSheet(combo_style)
        
        self.de_date = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.de_date.setCalendarPopup(True)
        self.de_date.setStyleSheet(combo_style)
        
        calendar = self.de_date.calendarWidget()
        calendar.setStyleSheet("""
            QCalendarWidget QWidget { color: #333; }
            QCalendarWidget QToolButton { color: #333; background-color: white; }
            QCalendarWidget QMenu { background-color: white; color: #333; }
            QCalendarWidget QSpinBox { color: #333; }
            QCalendarWidget QAbstractItemView:enabled { color: #333; selection-background-color: #69c0a5; }
        """)

        row_cb.addWidget(self.cb_doc); row_cb.addWidget(self.de_date)
        bk_v.addLayout(row_cb)

        days_box = QtWidgets.QHBoxLayout()
        for d, n in [("T2","22"), ("T3","23"), ("T4","24"), ("T5","25"), ("T6","26"), ("T7","27"), ("CN","28")]:
            day_v = QtWidgets.QVBoxLayout()
            l1 = QtWidgets.QLabel(d); l1.setStyleSheet("color: #888; font-size: 11px; border:none;")
            l2 = QtWidgets.QPushButton(n); l2.setFixedSize(40,40)
            if n == "25": l2.setStyleSheet("background: #e1f2ee; color: #69c0a5; border: 1px solid #69c0a5; border-radius: 8px; font-weight: bold;")
            else: l2.setStyleSheet("background: transparent; color: #333; border: none;")
            day_v.addWidget(l1, 0, QtCore.Qt.AlignmentFlag.AlignCenter); day_v.addWidget(l2)
            days_box.addLayout(day_v)
        bk_v.addLayout(days_box)

        time_grid = QtWidgets.QHBoxLayout()
        for t in ["08:00", "09:00", "10:00", "11:00"]:
            t_btn = QtWidgets.QPushButton(f"{t}\nCòn trống")
            if t == "09:00": t_btn.setStyleSheet("background: #e1f2ee; border: 1px solid #69c0a5; border-radius: 10px; color: #1a2a3a; padding: 10px; font-weight: bold;")
            else: t_btn.setStyleSheet("background: white; border: 1px solid #eee; border-radius: 10px; color: #333; padding: 10px;")
            time_grid.addWidget(t_btn)
        bk_v.addLayout(time_grid)

        btn_book = QtWidgets.QPushButton("Đặt lịch ngay")
        btn_book.setFixedHeight(50)
        btn_book.setStyleSheet("background: #27ae60; color: white; border-radius: 12px; font-size: 18px; font-weight: bold;")
        btn_book.clicked.connect(self.book_appointment)
        bk_v.addWidget(btn_book)
        grid_layout.addWidget(booking_card)

        # --- CỘT PHẢI ---
        right_col = QtWidgets.QVBoxLayout(); right_col.setSpacing(20)

        apt_card = QtWidgets.QFrame(); apt_card.setStyleSheet("background: white; border-radius: 20px; border: 1px solid #eee;")
        apt_v = QtWidgets.QVBoxLayout(apt_card); apt_v.setContentsMargins(20, 20, 20, 20)
        apt_head = QtWidgets.QHBoxLayout()
        apt_head.addWidget(QtWidgets.QLabel("Lịch hẹn sắp tới", styleSheet="font-weight:bold; font-size:18px; color:#1a2a3a; border:none;"))
        apt_head.addStretch(); apt_head.addWidget(QtWidgets.QLabel("Xem tất cả >", styleSheet="color:#3498db; border:none;"))
        apt_v.addLayout(apt_head)
        
        self.load_appointments(apt_v)
        right_col.addWidget(apt_card)

        noti_card = QtWidgets.QFrame(); noti_card.setStyleSheet("background: white; border-radius: 20px; border: 1px solid #eee;")
        noti_v = QtWidgets.QVBoxLayout(noti_card); noti_v.setContentsMargins(20, 20, 20, 20)
        noti_v.addWidget(QtWidgets.QLabel("Thông báo", styleSheet="font-weight:bold; font-size:18px; color:#1a2a3a; border:none;"))
        for icon, txt, time in [("🔔", "Lịch hẹn đã xác nhận", "2 giờ trước"), ("📅", "Vui lòng đến sớm 15p", "1 ngày trước")]:
            n_row = QtWidgets.QHBoxLayout()
            n_row.addWidget(QtWidgets.QLabel(icon))
            n_row.addWidget(QtWidgets.QLabel(txt, styleSheet="color: #333; border:none;"))
            n_row.addStretch(); n_row.addWidget(QtWidgets.QLabel(time, styleSheet="color: #999; font-size: 11px; border:none;"))
            noti_v.addLayout(n_row)
        right_col.addWidget(noti_card)
        grid_layout.addLayout(right_col)

        main_content_layout.addLayout(grid_layout)

        # 4. Feature section
        bottom_layout = QtWidgets.QHBoxLayout(); bottom_layout.setSpacing(20)
        features = [
            ("📅", "Đặt lịch khám dễ dàng", "Chọn bác sĩ và thời gian phù hợp để đặt lịch khám bệnh một cách nhanh chóng"),
            ("📋", "Quản lý lịch sử khám", "Xem lại lịch sử khám bệnh và kết quả chẩn đoán mọi lúc, mọi nơi"),
            ("💊", "Theo dõi đơn thuốc", "Dễ dàng theo dõi đơn thuốc và liệu trình điều trị của bạn")
        ]
        for icon, tit, desc in features:
            f_card = QtWidgets.QFrame()
            f_card.setStyleSheet("background: white; border-radius: 15px; border: 1px solid #eef2f5;")
            f_v = QtWidgets.QHBoxLayout(f_card)
            f_v.setContentsMargins(20, 20, 20, 20)
            
            f_icon = QtWidgets.QLabel(icon)
            f_icon.setStyleSheet("font-size: 32px; color: #3498db; background: #eef7fe; padding: 10px; border-radius: 12px; border:none;")
            f_icon.setFixedSize(65, 65)
            f_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            
            f_text_container = QtWidgets.QVBoxLayout()
            f_tit = QtWidgets.QLabel(tit)
            f_tit.setStyleSheet("font-weight: bold; font-size: 16px; color: #1a2a3a; border: none;")
            f_desc = QtWidgets.QLabel(desc)
            f_desc.setWordWrap(True)
            f_desc.setStyleSheet("color: #7f8c8d; font-size: 13px; border: none; line-height: 18px;")
            
            f_text_container.addWidget(f_tit)
            f_text_container.addWidget(f_desc)
            
            f_v.addWidget(f_icon)
            f_v.addLayout(f_text_container)
            f_v.setStretch(1, 1) 
            bottom_layout.addWidget(f_card)
        
        main_content_layout.addLayout(bottom_layout)

        container_layout.addWidget(main_content_widget)
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

    def create_navbar(self):
        nav = QtWidgets.QWidget(); nav.setFixedHeight(80); nav.setStyleSheet("background: white; border-bottom: 1px solid #eee;")
        nav_layout = QtWidgets.QHBoxLayout(nav); nav_layout.setContentsMargins(40, 0, 40, 0)
        logo = QtWidgets.QLabel("⊕ CarePlus"); logo.setStyleSheet("color: #69c0a5; font-size: 24px; font-weight: bold;")
        nav_layout.addWidget(logo); nav_layout.addStretch()
        for text in ["Trang chủ", "Dịch vụ", "Bác sĩ", "Tin tức"]:
            btn = QtWidgets.QPushButton(text)
            btn.setStyleSheet("QPushButton { border: none; padding: 10px 15px; color: #555; font-size: 15px; }")
            if text == "Trang chủ": btn.setStyleSheet("color: #69c0a5; font-weight: bold; border: none;")
            nav_layout.addWidget(btn)
        nav_layout.addStretch()
        
        self.user_btn = QtWidgets.QPushButton(f"👤 {self.username} ▿")
        self.user_btn.setStyleSheet("background: #f0f7f6; border-radius: 15px; padding: 8px 15px; font-weight: bold; color: #333;")
        self.user_btn.clicked.connect(self.show_menu)
        nav_layout.addWidget(self.user_btn)

        # ĐÃ SỬA: Gán vào biến self để không bị Garbage Collection xóa mất kết nối
        self.btn_logout_nav = QtWidgets.QPushButton("Đăng xuất")
        self.btn_logout_nav.setStyleSheet("background: #ffeded; color: #ff4d4f; border-radius: 10px; padding: 8px 15px; font-weight: bold;")
        self.btn_logout_nav.clicked.connect(self.logout)
        nav_layout.addWidget(self.btn_logout_nav)
        
        return nav

    def show_menu(self):
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet("QMenu { background: white; color: #333; border: 1px solid #eee; } QMenu::item { padding: 10px 30px; } QMenu::item:selected { background: #f8faff; color: #69c0a5; }")
        menu.addAction("📅 Đặt lịch khám"); menu.addAction("📋 Lịch sử khám"); menu.addAction("👤 Hồ sơ cá nhân")
        menu.addSeparator()
        logout_act = menu.addAction("🚪 Đăng xuất")
        logout_act.triggered.connect(self.logout)
        menu.exec(self.user_btn.mapToGlobal(QtCore.QPoint(0, self.user_btn.height() + 5)))

    def book_appointment(self):
        doc_id = self.cb_doc.currentData()
        date = self.de_date.date().toString("yyyy-MM-dd")
        date_time = f"{date} 09:00:00" # Dùng tạm giờ cứng theo UI mock
        patient_id = self.user_data.get("patient_id")
        
        if not doc_id or not patient_id:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Không thể đặt lịch do thiếu dữ liệu Bác sĩ hoặc Bệnh nhân")
            return
            
        success = AppointmentController.create(patient_id, doc_id, date_time)
        if success:
            QtWidgets.QMessageBox.information(self, "Thành công", "Đặt lịch khám thành công!")
        else:
            QtWidgets.QMessageBox.warning(self, "Thất bại", "Lỗi khi lưu lịch hẹn")

    def load_appointments(self, layout):
        patient_id = self.user_data.get("patient_id")
        if not patient_id:
            return
            
        appointments = AppointmentController.get_by_patient(patient_id)
        if not appointments:
            layout.addWidget(QtWidgets.QLabel("Bạn chưa có lịch hẹn nào."))
            return
            
        # Lấy tối đa 3 lịch hẹn
        for appt in appointments[:3]:
            item = QtWidgets.QFrame(); item.setStyleSheet("background: #f9f9f9; border-radius: 12px; border: 1px solid #f0f0f0;")
            item_h = QtWidgets.QHBoxLayout(item)
            item_h.addWidget(QtWidgets.QLabel("📅"))
            
            import datetime
            if isinstance(appt["appointment_date"], datetime.datetime):
                dt_str = appt["appointment_date"].strftime("%d/%m/%Y • %H:%M")
            else:
                dt_str = str(appt["appointment_date"])
                
            info = QtWidgets.QLabel(f"<b style='color:#1a2a3a;'>BS {appt['doctor_name']}</b><br><span style='color:#333;'>{dt_str}</span><br><span style='color:#555;'>{appt.get('specialty', '')}</span>")
            
            stt = QtWidgets.QLabel(appt["status"])
            if appt["status"] == "pending":
                stt.setStyleSheet("background: #fff4e6; color: #fd7e14; padding: 5px 10px; border-radius: 8px; border:none; font-size: 11px;")
            else:
                stt.setStyleSheet("background: #e8f5e9; color: #2e7d32; padding: 5px 10px; border-radius: 8px; border:none; font-size: 11px;")
                
            item_h.addWidget(info); item_h.addStretch(); item_h.addWidget(stt)
            layout.addWidget(item)

    def logout(self):
     reply = QtWidgets.QMessageBox.question(
        self,
        "Đăng xuất",
        "Bạn có chắc muốn đăng xuất không?",
        QtWidgets.QMessageBox.StandardButton.Yes |
        QtWidgets.QMessageBox.StandardButton.No
    )

     if reply == QtWidgets.QMessageBox.StandardButton.Yes:

        # Đóng giao diện hiện tại
        self.close()

        # Import LoginView
        from views.login_view import LoginView

        # Mở lại màn hình đăng nhập
        self.login_window = LoginView()
        self.login_window.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    login_screen = QtWidgets.QLabel("MÀN HÌNH ĐĂNG NHẬP (GIẢ LẬP)")
    login_screen.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    login_screen.resize(400, 300)
    login_screen.setStyleSheet("background: white; font-size: 20px; font-weight: bold;")
    
    window = MainView("patient", "Nguyễn Văn A", login_window=login_screen) 
    window.show()
    
    sys.exit(app.exec())