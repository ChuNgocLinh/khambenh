from datetime import date, datetime
from PyQt6 import QtWidgets, QtCore, QtGui
from controllers.medical_record_controller import MedicalRecordController
from controllers.prescription_controller import PrescriptionController
from controllers.appointment_controller import AppointmentController
from controllers.patient_controller import PatientController
from controllers.medicine_controller import MedicineController
from controllers.service_controller import ServiceController

class BaseDoctorView(QtWidgets.QWidget):
    def __init__(self, title_text, headers, doctor_id, parent=None):
        super().__init__(parent)
        self.doctor_id = doctor_id
        self.layout = QtWidgets.QVBoxLayout(self)
        
        title = QtWidgets.QLabel(title_text)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        self.layout.addWidget(title)
        
        toolbar = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm...")
        self.search_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #ddd; font-size: 14px;")
        toolbar.addWidget(self.search_input)
        
        self.btn_search = QtWidgets.QPushButton("🔍 Tìm kiếm")
        self.btn_search.setStyleSheet("background: #f1f5f9; padding: 8px 15px; border-radius: 5px; font-weight: bold;")
        self.btn_search.clicked.connect(self.load_data)
        toolbar.addWidget(self.btn_search)
        
        toolbar.addStretch()
        
        self.btn_add = QtWidgets.QPushButton("➕ Thêm mới")
        self.btn_add.setStyleSheet("background: #69c0a5; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold;")
        self.btn_add.clicked.connect(self.add_new)
        toolbar.addWidget(self.btn_add)
        
        self.layout.addLayout(toolbar)
        
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setStyleSheet("""
            QTableWidget { border: 1px solid #e2e8f0; border-radius: 10px; background: white; font-size: 14px; color: #333; }
            QHeaderView::section { background-color: #f8fafc; padding: 12px; font-weight: bold; border: none; border-bottom: 2px solid #e2e8f0; }
            QTableWidget::item { padding: 10px; border-bottom: 1px solid #f1f5f9; }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.layout.addWidget(self.table)
        
    def load_data(self):
        pass
        
    def add_new(self):
        pass


class PatientCreateDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Bệnh Nhân")
        self.setMinimumWidth(460)

        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Nhập họ tên bệnh nhân")

        self.dob_input = QtWidgets.QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDisplayFormat("dd/MM/yyyy")
        self.dob_input.setDate(QtCore.QDate.currentDate().addYears(-18))

        self.gender_input = QtWidgets.QComboBox()
        self.gender_input.addItems(["Nam", "Nữ"])

        self.phone_input = QtWidgets.QLineEdit()
        self.phone_input.setPlaceholderText("VD: 0912345678")

        self.address_input = QtWidgets.QLineEdit()
        self.address_input.setPlaceholderText("Địa chỉ liên hệ")

        self.email_input = QtWidgets.QLineEdit()
        self.email_input.setPlaceholderText("email@example.com")

        self.bhyt_input = QtWidgets.QLineEdit()
        self.bhyt_input.setPlaceholderText("Mã BHYT (nếu có)")

        widgets = [
            self.name_input,
            self.dob_input,
            self.gender_input,
            self.phone_input,
            self.address_input,
            self.email_input,
            self.bhyt_input,
        ]
        for widget in widgets:
            widget.setStyleSheet(
                "padding: 8px; border-radius: 6px; border: 1px solid #dbe2ea; font-size: 13px;"
            )

        form.addRow("Họ tên:", self.name_input)
        form.addRow("Ngày sinh:", self.dob_input)
        form.addRow("Giới tính:", self.gender_input)
        form.addRow("SĐT:", self.phone_input)
        form.addRow("Địa chỉ:", self.address_input)
        form.addRow("Email:", self.email_input)
        form.addRow("BHYT:", self.bhyt_input)
        layout.addLayout(form)

        note = QtWidgets.QLabel(
            "Lưu ý: Email và BHYT là thông tin bổ sung trong form để đồng bộ nghiệp vụ tiếp nhận bệnh nhân."
        )
        note.setWordWrap(True)
        note.setStyleSheet("color: #64748b; font-size: 12px;")
        layout.addWidget(note)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QtWidgets.QPushButton("Hủy")
        cancel_btn.setStyleSheet("padding: 8px 14px; border-radius: 6px; background: #f1f5f9;")
        cancel_btn.clicked.connect(self.reject)

        save_btn = QtWidgets.QPushButton("Lưu bệnh nhân")
        save_btn.setStyleSheet(
            "padding: 8px 14px; border-radius: 6px; background: #69c0a5; color: white; font-weight: 700;"
        )
        save_btn.clicked.connect(self._validate_and_accept)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def _validate_and_accept(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        bhyt = self.bhyt_input.text().strip()

        if not name:
            QtWidgets.QMessageBox.warning(self, "Thiếu dữ liệu", "Vui lòng nhập họ tên bệnh nhân.")
            return

        if not phone:
            QtWidgets.QMessageBox.warning(self, "Thiếu dữ liệu", "Vui lòng nhập số điện thoại.")
            return

        digits = "".join(ch for ch in phone if ch.isdigit())
        if len(digits) < 9 or len(digits) > 11:
            QtWidgets.QMessageBox.warning(self, "SĐT không hợp lệ", "Số điện thoại cần từ 9 đến 11 chữ số.")
            return

        if email and ("@" not in email or email.startswith("@") or email.endswith("@")):
            QtWidgets.QMessageBox.warning(self, "Email không hợp lệ", "Vui lòng nhập đúng định dạng email.")
            return

        if bhyt and len(bhyt) < 6:
            QtWidgets.QMessageBox.warning(self, "BHYT không hợp lệ", "Mã BHYT quá ngắn, vui lòng kiểm tra lại.")
            return

        self.accept()

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "dob": self.dob_input.date().toString("yyyy-MM-dd"),
            "gender": self.gender_input.currentText(),
            "phone": self.phone_input.text().strip(),
            "address": self.address_input.text().strip(),
            "email": self.email_input.text().strip(),
            "bhyt": self.bhyt_input.text().strip(),
        }


class PatientRecordDialog(QtWidgets.QDialog):
    def __init__(self, title, rows, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(680)
        self.resize(720, 420)

        layout = QtWidgets.QVBoxLayout(self)

        table = QtWidgets.QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Ngày khám", "Chẩn đoán", "Điều trị", "Bác sĩ"])
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        table.setStyleSheet(
            "QTableWidget { border: 1px solid #e2e8f0; border-radius: 10px; background: white; }"
            "QHeaderView::section { background-color: #f8fafc; padding: 10px; font-weight: 700; }"
            "QTableWidget::item { padding: 8px; border-bottom: 1px solid #f1f5f9; }"
        )

        table.setRowCount(len(rows))
        for row_idx, item in enumerate(rows):
            table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(item.get("visit_date", ""))))
            table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(item.get("diagnosis", ""))))
            table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(item.get("treatment", ""))))
            table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(item.get("doctor_name", ""))))
            table.setRowHeight(row_idx, 40)

        if not rows:
            empty = QtWidgets.QLabel("Chưa có dữ liệu hồ sơ bệnh án cho bệnh nhân này.")
            empty.setStyleSheet("color: #64748b; font-size: 13px;")
            layout.addWidget(empty)

        layout.addWidget(table)

        close_btn = QtWidgets.QPushButton("Đóng")
        close_btn.setStyleSheet(
            "background: #69c0a5; color: white; padding: 8px 14px; border-radius: 6px; font-weight: 700;"
        )
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, 0, QtCore.Qt.AlignmentFlag.AlignRight)


class MedicalRecordDialog(QtWidgets.QDialog):
    def __init__(self, doctor_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tạo Bệnh Án")
        self.setMinimumWidth(400)
        self.doctor_id = doctor_id
        
        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        
        self.appt_combo = QtWidgets.QComboBox()
        # Load pending/in-progress appointments for this doctor
        self.appts = AppointmentController.get_by_doctor(self.doctor_id)
        for a in self.appts:
            if a["status"] in ["pending", "in_progress", "confirmed"]:
                self.appt_combo.addItem(f"{a['appointment_id']} - {a['patient_name']} ({a['appointment_date']})", a)
                
        self.diag_input = QtWidgets.QTextEdit()
        self.treat_input = QtWidgets.QTextEdit()
        
        form.addRow("Chọn Lịch Hẹn:", self.appt_combo)
        form.addRow("Chẩn đoán:", self.diag_input)
        form.addRow("Điều trị:", self.treat_input)
        
        layout.addLayout(form)
        
        btn_layout = QtWidgets.QHBoxLayout()
        save_btn = QtWidgets.QPushButton("Lưu Bệnh Án")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QtWidgets.QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn); btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
    def get_data(self):
        appt = self.appt_combo.currentData()
        return {
            "patient_id": appt["patient_id"] if appt else None,
            "appointment_id": appt["appointment_id"] if appt else None,
            "diagnosis": self.diag_input.toPlainText(),
            "treatment": self.treat_input.toPlainText()
        }


class PrescriptionDialog(QtWidgets.QDialog):
    def __init__(self, record_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kê Đơn Thuốc")
        self.setMinimumWidth(400)
        self.record_id = record_id
        
        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        
        self.med_combo = QtWidgets.QComboBox()
        self.meds = MedicineController.get_all()
        for m in self.meds:
            if m.get("is_active", True) and m.get("quantity", 0) > 0:
                self.med_combo.addItem(f"{m['name']} (Còn: {m['quantity']})", m)
                
        self.qty_input = QtWidgets.QSpinBox()
        self.qty_input.setMinimum(1)
        self.qty_input.setMaximum(100)
        
        form.addRow("Chọn Thuốc:", self.med_combo)
        form.addRow("Số lượng:", self.qty_input)
        
        layout.addLayout(form)
        
        btn_layout = QtWidgets.QHBoxLayout()
        save_btn = QtWidgets.QPushButton("Thêm")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QtWidgets.QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn); btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
    def get_data(self):
        med = self.med_combo.currentData()
        return {
            "record_id": self.record_id,
            "medicine_id": med["medicine_id"] if med else None,
            "quantity": self.qty_input.value()
        }


class MedicalRecordView(BaseDoctorView):
    def __init__(self, doctor_id):
        super().__init__("Hồ sơ Bệnh Án", ["ID", "Ngày Khám", "Bệnh Nhân", "Chẩn Đoán", "Điều Trị", "Hành động"], doctor_id)
        self.load_data()

    def load_data(self):
        # We need to get all records for this doctor. The model currently gets by patient.
        # So we fetch all appointments for doctor, then get records. 
        # For simplicity, we just fetch all appointments and their records or use a direct query.
        from database.db import fetch_all
        records = fetch_all("SELECT r.*, p.name as patient_name FROM MedicalRecords r JOIN Patients p ON r.patient_id = p.patient_id WHERE r.doctor_id = ?", (self.doctor_id,))
        
        query = self.search_input.text().lower()
        if query:
            records = [r for r in records if query in str(r.get("patient_name", "")).lower() or query in str(r.get("diagnosis", "")).lower()]
            
        self.table.setRowCount(len(records))
        for row, r in enumerate(records):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(r["record_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(r.get("created_at", ""))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(r.get("patient_name", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(r.get("diagnosis", ""))))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(r.get("treatment", ""))))
            
            btn_presc = QtWidgets.QPushButton("Kê đơn")
            btn_presc.clicked.connect(lambda _, r_id=r["record_id"]: self.add_prescription(r_id))
            self.table.setCellWidget(row, 5, btn_presc)

    def add_new(self):
        dialog = MedicalRecordDialog(self.doctor_id, self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data["patient_id"]:
                MedicalRecordController.create(data["patient_id"], self.doctor_id, data["appointment_id"], data["diagnosis"], data["treatment"])
                # Mark appt as done
                AppointmentController.update_status(data["appointment_id"], "done")
                self.load_data()
                
    def add_prescription(self, record_id):
        dialog = PrescriptionDialog(record_id, self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data["medicine_id"]:
                PrescriptionController.add(data["record_id"], data["medicine_id"], data["quantity"])
                QtWidgets.QMessageBox.information(self, "Thành công", "Đã kê đơn thuốc thành công!")


class PrescriptionView(BaseDoctorView):
    def __init__(self, doctor_id):
        super().__init__("Quản lý Đơn Thuốc", ["ID Đơn", "ID Bệnh Án", "Bệnh Nhân", "Thuốc", "Số Lượng"], doctor_id)
        self.btn_add.hide()
        self.load_data()

    def load_data(self):
        from database.db import fetch_all
        presc = fetch_all("""
            SELECT pr.*, m.name as med_name, p.name as patient_name
            FROM Prescriptions pr
            JOIN MedicalRecords mr ON pr.record_id = mr.record_id
            JOIN Patients p ON mr.patient_id = p.patient_id
            JOIN Medicines m ON pr.medicine_id = m.medicine_id
            WHERE mr.doctor_id = ?
        """, (self.doctor_id,))
        
        self.table.setRowCount(len(presc))
        for row, p in enumerate(presc):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(p["prescription_id"])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(p["record_id"])))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(p.get("patient_name", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(p.get("med_name", ""))))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(p.get("quantity", ""))))


class DoctorPatientListView(BaseDoctorView):
    def __init__(self, doctor_id):
        super().__init__(
            "Danh Sách Bệnh Nhân",
            [
                "ID bệnh nhân",
                "Họ tên",
                "Giới tính",
                "Ngày sinh",
                "SĐT",
                "Lần khám gần nhất",
                "Hành động",
            ],
            doctor_id,
        )

        desc = QtWidgets.QLabel("Quản lý thông tin và lịch sử khám của bệnh nhân")
        desc.setStyleSheet("color: #64748b; font-size: 13px; margin-bottom: 8px;")
        self.layout.insertWidget(1, desc)

        self.page_size = 8
        self.current_page = 1
        self.filtered_patients = []

        self.search_input.setPlaceholderText("Tìm kiếm bệnh nhân...")
        self.search_input.textChanged.connect(self._handle_filter_changed)

        self.gender_filter = QtWidgets.QComboBox()
        self.gender_filter.addItems(["Tất cả giới tính", "Nam", "Nữ"])
        self.gender_filter.setStyleSheet(
            "padding: 8px; border-radius: 5px; border: 1px solid #ddd; font-size: 14px;"
        )
        self.gender_filter.currentIndexChanged.connect(self._handle_filter_changed)

        self.age_filter = QtWidgets.QComboBox()
        self.age_filter.addItems(["Tất cả độ tuổi", "Trẻ em", "Người lớn", "Người cao tuổi"])
        self.age_filter.setStyleSheet(
            "padding: 8px; border-radius: 5px; border: 1px solid #ddd; font-size: 14px;"
        )
        self.age_filter.currentIndexChanged.connect(self._handle_filter_changed)

        toolbar = self.layout.itemAt(2).layout()
        toolbar.insertWidget(2, self.gender_filter)
        toolbar.insertWidget(3, self.age_filter)

        self.btn_add.setText("➕ Thêm Bệnh Nhân")

        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setColumnWidth(6, 280)

        self.pagination_layout = QtWidgets.QHBoxLayout()
        self.pagination_layout.addStretch()

        self.btn_prev = QtWidgets.QPushButton("← Trước")
        self.btn_prev.setStyleSheet("padding: 6px 12px; border-radius: 6px; background: #f1f5f9;")
        self.btn_prev.clicked.connect(self._prev_page)

        self.page_label = QtWidgets.QLabel("Trang 1/1")
        self.page_label.setStyleSheet("font-weight: 700; color: #334155; padding: 0 10px;")

        self.btn_next = QtWidgets.QPushButton("Sau →")
        self.btn_next.setStyleSheet("padding: 6px 12px; border-radius: 6px; background: #f1f5f9;")
        self.btn_next.clicked.connect(self._next_page)

        self.pagination_layout.addWidget(self.btn_prev)
        self.pagination_layout.addWidget(self.page_label)
        self.pagination_layout.addWidget(self.btn_next)
        self.pagination_layout.addStretch()
        self.layout.addLayout(self.pagination_layout)

        self.stats_layout = QtWidgets.QHBoxLayout()
        self.stats_layout.setSpacing(12)
        self.layout.insertLayout(2, self.stats_layout)

        self.total_patients_card = self._build_stat_card("👥", "Tổng bệnh nhân", "0")
        self.today_card = self._build_stat_card("📅", "Hôm nay", "0")
        self.follow_up_card = self._build_stat_card("🔁", "Tái khám", "0")

        self.stats_layout.addWidget(self.total_patients_card)
        self.stats_layout.addWidget(self.today_card)
        self.stats_layout.addWidget(self.follow_up_card)
        self.load_data()

    def load_data(self):
        from database.db import fetch_all

        patients = fetch_all(
            """
            SELECT p.patient_id, p.name, p.dob, p.phone, COUNT(a.appointment_id) as visits
                   , p.gender
                   , MAX(a.appointment_date) as last_visit
            FROM Patients p
            JOIN Appointments a ON p.patient_id = a.patient_id
            WHERE a.doctor_id = ?
            GROUP BY p.patient_id, p.name, p.dob, p.phone, p.gender
            ORDER BY MAX(a.appointment_date) DESC
            """,
            (self.doctor_id,),
        )

        self.filtered_patients = self._apply_filters(patients)
        self._update_stats_cards(self.filtered_patients)
        self._render_current_page()

    def add_new(self):
        dialog = PatientCreateDialog(self)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()
        created = PatientController.create(data)
        if not created:
            QtWidgets.QMessageBox.warning(
                self,
                "Không thể thêm",
                "Không thể tạo bệnh nhân mới. Vui lòng kiểm tra dữ liệu hoặc kết nối cơ sở dữ liệu.",
            )
            return

        QtWidgets.QMessageBox.information(
            self,
            "Thành công",
            "Đã thêm bệnh nhân mới. Bệnh nhân sẽ xuất hiện trong danh sách này khi có lịch hẹn với bác sĩ hiện tại.",
        )
        self.load_data()

    def _build_stat_card(self, icon, title, value):
        card = QtWidgets.QFrame()
        card.setStyleSheet("background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;")
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(12, 10, 12, 10)
        top = QtWidgets.QLabel(f"{icon} {title}")
        top.setStyleSheet("font-size: 13px; color: #475569; font-weight: 700;")
        value_lbl = QtWidgets.QLabel(value)
        value_lbl.setStyleSheet("font-size: 24px; font-weight: 900; color: #1e293b;")
        layout.addWidget(top)
        layout.addWidget(value_lbl)
        card._value_label = value_lbl
        return card

    def _update_stats_cards(self, rows):
        total = len(rows)
        today = date.today()
        today_count = 0
        follow_up_count = 0

        for patient in rows:
            last_visit_date = self._parse_datetime(patient.get("last_visit"))
            if last_visit_date and last_visit_date.date() == today:
                today_count += 1
            if int(patient.get("visits", 0) or 0) >= 2:
                follow_up_count += 1

        self.total_patients_card._value_label.setText(str(total))
        self.today_card._value_label.setText(str(today_count))
        self.follow_up_card._value_label.setText(str(follow_up_count))

    def _apply_filters(self, rows):
        keyword = self.search_input.text().strip().lower()
        selected_gender = self.gender_filter.currentText()
        selected_age = self.age_filter.currentText()

        filtered = []
        for item in rows:
            patient_id_text = f"BN{int(item.get('patient_id', 0)):04d}"
            name = str(item.get("name", "") or "")
            phone = str(item.get("phone", "") or "")

            if keyword:
                # Include normalized patient code to support searching by business ID (BN0001 style).
                haystack = f"{patient_id_text} {name} {phone}".lower()
                if keyword not in haystack:
                    continue

            gender = str(item.get("gender", "") or "")
            if selected_gender != "Tất cả giới tính" and gender != selected_gender:
                continue

            age = self._calculate_age(item.get("dob"))
            if selected_age == "Trẻ em" and (age is None or age >= 18):
                continue
            if selected_age == "Người lớn" and (age is None or age < 18 or age >= 60):
                continue
            if selected_age == "Người cao tuổi" and (age is None or age < 60):
                continue

            filtered.append(item)

        return filtered

    def _render_current_page(self):
        total_rows = len(self.filtered_patients)
        total_pages = max(1, (total_rows + self.page_size - 1) // self.page_size)
        self.current_page = max(1, min(self.current_page, total_pages))

        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        page_rows = self.filtered_patients[start:end]

        self.table.setRowCount(len(page_rows))
        for row, patient in enumerate(page_rows):
            patient_id = int(patient.get("patient_id", 0) or 0)
            patient_code = f"BN{patient_id:04d}"

            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(patient_code))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(patient.get("name", ""))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(patient.get("gender", ""))))

            dob_text = self._format_dob(patient.get("dob"))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(dob_text))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(patient.get("phone", ""))))

            last_visit_text = self._format_last_visit(patient.get("last_visit"))
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(last_visit_text))

            self.table.setCellWidget(row, 6, self._build_action_buttons(patient))
            self.table.setRowHeight(row, 46)

        self.page_label.setText(f"Trang {self.current_page}/{total_pages}")
        self.btn_prev.setEnabled(self.current_page > 1)
        self.btn_next.setEnabled(self.current_page < total_pages)

    def _build_action_buttons(self, patient):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(4)

        actions = [
            ("👁 XEM", "#e2e8f0", lambda checked=False, p=patient: self._view_patient(p)),
            ("📄 HỒ SƠ", "#d9f99d", lambda checked=False, p=patient: self._open_record(p)),
            ("🗑 XÓA", "#fecaca", lambda checked=False, p=patient: self._delete_patient(p)),
        ]

        for text, color, callback in actions:
            btn = QtWidgets.QPushButton(text)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(
                f"QPushButton {{ background: {color}; border: none; border-radius: 6px; padding: 5px 8px; font-weight: 700; font-size: 11px; }}"
                "QPushButton:hover { opacity: 0.9; }"
            )
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        return wrapper

    def _view_patient(self, patient):
        age = self._calculate_age(patient.get("dob"))
        fields = [
            ("Mã bệnh nhân", f"BN{int(patient.get('patient_id', 0) or 0):04d}"),
            ("Họ tên", patient.get("name", "")),
            ("Giới tính", patient.get("gender", "")),
            ("Ngày sinh", self._format_dob(patient.get("dob"))),
            ("Tuổi", "" if age is None else str(age)),
            ("SĐT", patient.get("phone", "")),
            ("Lần khám gần nhất", self._format_last_visit(patient.get("last_visit"))),
            ("Số lượt khám", patient.get("visits", 0)),
        ]

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Chi tiết bệnh nhân")
        dialog.setMinimumWidth(520)

        layout = QtWidgets.QVBoxLayout(dialog)
        form = QtWidgets.QFormLayout()
        for key, value in fields:
            label = QtWidgets.QLabel(str(value))
            label.setStyleSheet("color: #1e293b;")
            form.addRow(f"{key}:", label)
        layout.addLayout(form)

        close_btn = QtWidgets.QPushButton("Đóng")
        close_btn.setStyleSheet(
            "background: #69c0a5; color: white; padding: 8px 14px; border-radius: 6px; font-weight: 700;"
        )
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        dialog.exec()

    def _open_record(self, patient):
        from database.db import fetch_all

        rows = fetch_all(
            """
            SELECT r.record_id,
                   r.created_at as visit_date,
                   r.diagnosis,
                   r.treatment,
                   d.name as doctor_name,
                   a.note as appointment_note,
                   a.status as appointment_status
            FROM MedicalRecords r
            JOIN Doctors d ON d.doctor_id = r.doctor_id
            LEFT JOIN Appointments a ON a.appointment_id = r.appointment_id
            WHERE r.patient_id = ?
            ORDER BY r.created_at DESC
            """,
            (patient.get("patient_id"),),
        )

        detail_dialog = QtWidgets.QDialog(self)
        detail_dialog.setWindowTitle("Hồ sơ bệnh án (toàn bộ bệnh sử)")
        detail_dialog.resize(860, 560)

        layout = QtWidgets.QVBoxLayout(detail_dialog)

        header = QtWidgets.QLabel(
            f"Bệnh nhân: {patient.get('name', '')} • Mã BN{int(patient.get('patient_id', 0) or 0):04d}"
        )
        header.setStyleSheet("font-size: 15px; font-weight: 800; color: #1e293b;")
        layout.addWidget(header)

        tabs = QtWidgets.QTabWidget()
        tabs.setStyleSheet(
            "QTabWidget::pane { border: 1px solid #e2e8f0; border-radius: 10px; background: white; }"
            "QTabBar::tab { padding: 8px 12px; background: #f8fafc; margin-right: 4px; border-top-left-radius: 6px; border-top-right-radius: 6px; }"
            "QTabBar::tab:selected { background: #e2f7ef; font-weight: 700; }"
        )

        # Tab 1: Lịch sử khám
        history_tab = QtWidgets.QWidget()
        history_layout = QtWidgets.QVBoxLayout(history_tab)
        history_table = QtWidgets.QTableWidget()
        history_table.setColumnCount(6)
        history_table.setHorizontalHeaderLabels(
            ["Ngày khám", "Chẩn đoán", "Điều trị", "Bác sĩ", "Triệu chứng", "Trạng thái lịch hẹn"]
        )
        history_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        history_table.verticalHeader().setVisible(False)
        history_table.setShowGrid(False)
        history_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        history_table.setStyleSheet(
            "QTableWidget { border: 1px solid #e2e8f0; border-radius: 10px; background: white; }"
            "QHeaderView::section { background-color: #f8fafc; padding: 10px; font-weight: 700; }"
            "QTableWidget::item { padding: 8px; border-bottom: 1px solid #f1f5f9; }"
        )

        history_table.setRowCount(len(rows))
        prescription_lines = []
        for idx, record in enumerate(rows):
            record_id = record.get("record_id")
            visit_text = self._format_last_visit(record.get("visit_date"))
            history_table.setItem(idx, 0, QtWidgets.QTableWidgetItem(visit_text))
            history_table.setItem(idx, 1, QtWidgets.QTableWidgetItem(str(record.get("diagnosis", ""))))
            history_table.setItem(idx, 2, QtWidgets.QTableWidgetItem(str(record.get("treatment", ""))))
            history_table.setItem(idx, 3, QtWidgets.QTableWidgetItem(str(record.get("doctor_name", ""))))
            history_table.setItem(idx, 4, QtWidgets.QTableWidgetItem(str(record.get("appointment_note", ""))))
            history_table.setItem(idx, 5, QtWidgets.QTableWidgetItem(str(record.get("appointment_status", ""))))
            history_table.setRowHeight(idx, 42)

            if record_id is not None:
                prescriptions = fetch_all(
                    """
                    SELECT m.name as medicine_name, pr.quantity
                    FROM Prescriptions pr
                    JOIN Medicines m ON m.medicine_id = pr.medicine_id
                    WHERE pr.record_id = ?
                    """,
                    (record_id,),
                )
                if prescriptions:
                    meds = ", ".join(
                        f"{item.get('medicine_name', '')} x{item.get('quantity', 0)}"
                        for item in prescriptions
                    )
                    prescription_lines.append(f"• {visit_text}: {meds}")

        if not rows:
            empty_history = QtWidgets.QLabel("Chưa có dữ liệu lịch sử khám bệnh.")
            empty_history.setStyleSheet("color: #64748b; font-size: 13px;")
            history_layout.addWidget(empty_history)
        history_layout.addWidget(history_table)

        # Tab 2: Đơn thuốc và dữ liệu liên quan
        prescription_tab = QtWidgets.QWidget()
        prescription_layout = QtWidgets.QVBoxLayout(prescription_tab)

        prescription_label = QtWidgets.QLabel("Danh sách đơn thuốc theo hồ sơ")
        prescription_label.setStyleSheet("font-size: 14px; font-weight: 700; color: #1e293b;")
        prescription_layout.addWidget(prescription_label)

        prescription_text = QtWidgets.QTextEdit()
        prescription_text.setReadOnly(True)
        prescription_text.setStyleSheet(
            "border: 1px solid #e2e8f0; border-radius: 10px; background: white; padding: 10px;"
        )
        if prescription_lines:
            prescription_text.setPlainText("\n".join(prescription_lines))
        else:
            prescription_text.setPlainText("Chưa có dữ liệu đơn thuốc cho các lần khám hiện tại.")
        prescription_layout.addWidget(prescription_text)

        warning = QtWidgets.QLabel(
            "Ghi chú: Dữ liệu xét nghiệm, hình ảnh và dị ứng thuốc chưa có bảng chuyên biệt trong phiên bản hiện tại."
        )
        warning.setWordWrap(True)
        warning.setStyleSheet(
            "color: #92400e; background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 8px;"
        )
        prescription_layout.addWidget(warning)

        tabs.addTab(history_tab, "Lịch sử khám")
        tabs.addTab(prescription_tab, "Đơn thuốc")
        layout.addWidget(tabs)

        action_layout = QtWidgets.QHBoxLayout()
        action_layout.addStretch()

        print_btn = QtWidgets.QPushButton("In PDF (sắp có)")
        print_btn.setEnabled(False)
        print_btn.setStyleSheet("padding: 8px 14px; border-radius: 6px; background: #e2e8f0;")

        close_btn = QtWidgets.QPushButton("Đóng")
        close_btn.setStyleSheet(
            "background: #69c0a5; color: white; padding: 8px 14px; border-radius: 6px; font-weight: 700;"
        )
        close_btn.clicked.connect(detail_dialog.accept)

        action_layout.addWidget(print_btn)
        action_layout.addWidget(close_btn)
        layout.addLayout(action_layout)

        detail_dialog.exec()

    def _delete_patient(self, patient):
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Yêu cầu xóa",
            f"Bạn đang yêu cầu xóa bệnh nhân {patient.get('name', '')}. Tiếp tục xem hướng dẫn quyền hạn?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No,
        )
        if confirm != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        QtWidgets.QMessageBox.information(
            self,
            "Giới hạn quyền",
            "Theo nghiệp vụ hiện tại, chỉ quản trị viên mới được phép xóa bệnh nhân khỏi hệ thống.",
        )

    def _handle_filter_changed(self):
        self.current_page = 1
        self.load_data()

    def _prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self._render_current_page()

    def _next_page(self):
        total_pages = max(1, (len(self.filtered_patients) + self.page_size - 1) // self.page_size)
        if self.current_page < total_pages:
            self.current_page += 1
            self._render_current_page()

    @staticmethod
    def _parse_datetime(value):
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
        return None

    def _calculate_age(self, dob_value):
        parsed = self._parse_datetime(dob_value)
        if not parsed:
            return None
        today = date.today()
        years = today.year - parsed.date().year
        if (today.month, today.day) < (parsed.date().month, parsed.date().day):
            years -= 1
        return max(0, years)

    def _format_dob(self, dob_value):
        parsed = self._parse_datetime(dob_value)
        if parsed:
            return parsed.strftime("%d/%m/%Y")
        return ""

    def _format_last_visit(self, last_visit_value):
        parsed = self._parse_datetime(last_visit_value)
        if parsed:
            return parsed.strftime("%d/%m/%Y")
        return ""


class AppointmentUpsertDialog(QtWidgets.QDialog):
    def __init__(self, doctor_id, appointment=None, parent=None):
        super().__init__(parent)
        self.doctor_id = doctor_id
        self.appointment = appointment or {}
        self.setWindowTitle("Chỉnh sửa lịch hẹn" if appointment else "Thêm lịch hẹn")
        self.setMinimumWidth(520)

        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.patient_input = QtWidgets.QComboBox()
        self.patients = PatientController.get_all()
        for patient in self.patients:
            label = f"{patient.get('name', 'N/A')} - {patient.get('phone', '')}"
            self.patient_input.addItem(label, patient)

        self.date_input = QtWidgets.QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd/MM/yyyy")

        self.time_input = QtWidgets.QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm")

        self.service_input = QtWidgets.QComboBox()
        self.services = ServiceController.get_all()
        self.service_input.addItem("", "")
        for service in self.services:
            name = str(service.get("service_name", "")).strip()
            if name:
                self.service_input.addItem(name, name)

        self.status_input = QtWidgets.QComboBox()
        self.status_input.addItems([
            "pending",
            "confirmed",
            "in_progress",
            "done",
            "cancelled",
        ])

        self.note_input = QtWidgets.QTextEdit()
        self.note_input.setPlaceholderText("Ghi chú (triệu chứng, tái khám, khám lần đầu...)")
        self.note_input.setFixedHeight(90)

        for widget in [
            self.patient_input,
            self.date_input,
            self.time_input,
            self.service_input,
            self.status_input,
            self.note_input,
        ]:
            widget.setStyleSheet(
                "padding: 8px; border-radius: 6px; border: 1px solid #dbe2ea; font-size: 13px;"
            )

        form.addRow("Bệnh nhân:", self.patient_input)
        form.addRow("Ngày khám:", self.date_input)
        form.addRow("Giờ khám:", self.time_input)
        form.addRow("Dịch vụ:", self.service_input)
        form.addRow("Trạng thái:", self.status_input)
        form.addRow("Ghi chú:", self.note_input)
        layout.addLayout(form)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch()

        btn_cancel = QtWidgets.QPushButton("Hủy")
        btn_cancel.setStyleSheet("padding: 8px 14px; border-radius: 6px; background: #f1f5f9;")
        btn_cancel.clicked.connect(self.reject)

        btn_save = QtWidgets.QPushButton("Lưu")
        btn_save.setStyleSheet(
            "padding: 8px 14px; border-radius: 6px; background: #69c0a5; color: white; font-weight: 700;"
        )
        btn_save.clicked.connect(self._validate_and_accept)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

        self._prefill_data()

    def _prefill_data(self):
        if not self.appointment:
            now = datetime.now()
            self.date_input.setDate(QtCore.QDate(now.year, now.month, now.day))
            # Round to the next 30-minute slot to avoid preselecting past times.
            if now.minute < 30:
                minute = 30
                hour = now.hour
            else:
                minute = 0
                hour = min(now.hour + 1, 23)
            self.time_input.setTime(QtCore.QTime(hour, minute))
            self.status_input.setCurrentText("pending")
            return

        patient_id = int(self.appointment.get("patient_id", 0) or 0)
        for idx in range(self.patient_input.count()):
            patient = self.patient_input.itemData(idx) or {}
            if int(patient.get("patient_id", 0) or 0) == patient_id:
                self.patient_input.setCurrentIndex(idx)
                break

        dt_value = self._parse_datetime(self.appointment.get("appointment_date"))
        if dt_value:
            self.date_input.setDate(QtCore.QDate(dt_value.year, dt_value.month, dt_value.day))
            self.time_input.setTime(QtCore.QTime(dt_value.hour, dt_value.minute))

        status_value = str(self.appointment.get("status", "pending"))
        self.status_input.setCurrentText(status_value)

        service_name = self._extract_service(self.appointment.get("note"))
        if service_name:
            idx = self.service_input.findData(service_name)
            if idx >= 0:
                self.service_input.setCurrentIndex(idx)

        self.note_input.setPlainText(self._extract_plain_note(self.appointment.get("note")))

    @staticmethod
    def _parse_datetime(value):
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
        return None

    @staticmethod
    def _extract_service(note):
        if not note:
            return ""
        text = str(note)
        if not text.startswith("Dịch vụ:"):
            return ""
        payload = text.replace("Dịch vụ:", "", 1).strip()
        parts = payload.split("|", 1)
        return parts[0].strip()

    @staticmethod
    def _extract_plain_note(note):
        if not note:
            return ""
        text = str(note).strip()
        if not text.startswith("Dịch vụ:"):
            return text
        payload = text.replace("Dịch vụ:", "", 1).strip()
        parts = payload.split("|", 1)
        if len(parts) == 2:
            return parts[1].strip()
        return ""

    def _validate_and_accept(self):
        patient = self.patient_input.currentData() or {}
        if not patient.get("patient_id"):
            QtWidgets.QMessageBox.warning(self, "Thiếu dữ liệu", "Vui lòng chọn bệnh nhân.")
            return

        selected_datetime = datetime(
            self.date_input.date().year(),
            self.date_input.date().month(),
            self.date_input.date().day(),
            self.time_input.time().hour(),
            self.time_input.time().minute(),
            0,
        )

        # Keep active appointments in the future to avoid accidental backdated slots.
        selected_status = self.status_input.currentText()
        if selected_datetime < datetime.now() and selected_status in {"pending", "confirmed", "in_progress"}:
            QtWidgets.QMessageBox.warning(self, "Dữ liệu không hợp lệ", "Không thể tạo lịch trong quá khứ.")
            return

        self.accept()

    def get_payload(self):
        patient = self.patient_input.currentData() or {}
        date_value = self.date_input.date().toString("yyyy-MM-dd")
        time_value = self.time_input.time().toString("HH:mm")
        return {
            "patient_id": patient.get("patient_id"),
            "doctor_id": self.doctor_id,
            "date": date_value,
            "time": time_value,
            "service_name": self.service_input.currentData() or "",
            "status": self.status_input.currentText(),
            "note": self.note_input.toPlainText().strip(),
        }


class DoctorAppointmentView(BaseDoctorView):
    STATUS_LABELS = {
        "pending": "Chờ xác nhận",
        "confirmed": "Đã xác nhận",
        "in_progress": "Đang khám",
        "done": "Đã khám",
        "cancelled": "Đã hủy",
    }

    STATUS_COLORS = {
        "pending": "#f59f00",
        "confirmed": "#2b8a3e",
        "in_progress": "#5f3dc4",
        "done": "#0c8599",
        "cancelled": "#e03131",
    }

    def __init__(self, doctor_id):
        super().__init__(
            "Quản lý lịch hẹn",
            [
                "Thời gian",
                "Bệnh nhân",
                "Dịch vụ",
                "Trạng thái",
                "Ghi chú",
                "Mức ưu tiên",
                "Thao tác",
            ],
            doctor_id,
        )
        self.page_size = 6
        self.current_page = 1
        self.filtered_rows = []
        self.all_rows = []

        self.btn_add.setText("+ Thêm lịch hẹn")
        self.btn_search.setText("Áp dụng lọc")
        self.search_input.setPlaceholderText("Tìm theo tên hoặc SDT")
        self.search_input.textChanged.connect(self._on_filter_changed)

        self.description = QtWidgets.QLabel("Xem và quản lý các lịch hẹn khám của bệnh nhân")
        self.description.setStyleSheet("color: #64748b; font-size: 13px; margin-bottom: 8px;")
        self.layout.insertWidget(1, self.description)

        self._setup_filters()
        self._setup_stats()
        self._setup_reminder()
        self._setup_pagination()

        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setColumnWidth(1, 260)
        self.table.setColumnWidth(4, 220)
        self.table.setColumnWidth(6, 300)

        self.load_data()

    def _setup_filters(self):
        today = QtCore.QDate.currentDate()
        self.from_date = QtWidgets.QDateEdit(today)
        self.from_date.setCalendarPopup(True)
        self.from_date.setDisplayFormat("dd/MM/yyyy")

        self.to_date = QtWidgets.QDateEdit(today.addMonths(1))
        self.to_date.setCalendarPopup(True)
        self.to_date.setDisplayFormat("dd/MM/yyyy")

        self.status_filter = QtWidgets.QComboBox()
        self.status_filter.addItems(
            [
                "Tất cả trạng thái",
                "Chờ xác nhận",
                "Đã xác nhận",
                "Đang khám",
                "Đã khám",
                "Đã hủy",
            ]
        )

        self.specialty_filter = QtWidgets.QComboBox()
        self.specialty_filter.addItems(["Tất cả chuyên khoa", "Nội khoa", "Tim mạch", "Thần kinh", "Tiêu hóa"])

        filter_row = QtWidgets.QHBoxLayout()
        filter_row.setSpacing(10)

        for title, widget in [
            ("Từ ngày", self.from_date),
            ("Đến ngày", self.to_date),
            ("Trạng thái", self.status_filter),
            ("Chuyên khoa", self.specialty_filter),
        ]:
            group = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel(title)
            label.setStyleSheet("color: #475569; font-size: 12px; font-weight: 700;")
            widget.setStyleSheet(
                "padding: 7px 8px; border-radius: 6px; border: 1px solid #dbe2ea; background: white;"
            )
            group.addWidget(label)
            group.addWidget(widget)
            holder = QtWidgets.QWidget()
            holder.setLayout(group)
            filter_row.addWidget(holder)

        filter_row.addStretch()
        self.layout.insertLayout(2, filter_row)

        self.from_date.dateChanged.connect(self._on_filter_changed)
        self.to_date.dateChanged.connect(self._on_filter_changed)
        self.status_filter.currentIndexChanged.connect(self._on_filter_changed)
        self.specialty_filter.currentIndexChanged.connect(self._on_filter_changed)

    def _setup_stats(self):
        self.stats_row = QtWidgets.QHBoxLayout()
        self.stats_row.setSpacing(10)
        self.layout.insertLayout(3, self.stats_row)

        self.total_card = self._build_stat_card("📋 Tổng lịch", "0", "#eff6ff", "#1d4ed8")
        self.pending_card = self._build_stat_card("⏳ Chờ xác nhận", "0", "#fff7ed", "#c2410c")
        self.confirmed_card = self._build_stat_card("✅ Đã xác nhận", "0", "#ecfdf3", "#15803d")
        self.done_card = self._build_stat_card("🩺 Đã khám", "0", "#ecfeff", "#0e7490")
        self.cancelled_card = self._build_stat_card("❌ Đã hủy", "0", "#fef2f2", "#b91c1c")

        for card in [
            self.total_card,
            self.pending_card,
            self.confirmed_card,
            self.done_card,
            self.cancelled_card,
        ]:
            self.stats_row.addWidget(card)

    def _setup_reminder(self):
        self.reminder_banner = QtWidgets.QLabel("Không có lịch hẹn gần giờ khám")
        self.reminder_banner.setStyleSheet(
            "padding: 8px 10px; border-radius: 8px; background: #fffbea; color: #92400e; border: 1px solid #fde68a;"
        )
        self.layout.insertWidget(4, self.reminder_banner)

    def _setup_pagination(self):
        self.pagination_row = QtWidgets.QHBoxLayout()
        self.pagination_row.setSpacing(6)
        self.layout.addLayout(self.pagination_row)

    def _build_stat_card(self, title, value, bg_color, text_color):
        card = QtWidgets.QFrame()
        card.setStyleSheet(f"background: {bg_color}; border: 1px solid #e2e8f0; border-radius: 10px;")
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(10, 8, 10, 8)

        title_lbl = QtWidgets.QLabel(title)
        title_lbl.setStyleSheet("font-size: 12px; color: #475569; font-weight: 700;")
        value_lbl = QtWidgets.QLabel(value)
        value_lbl.setStyleSheet(f"font-size: 24px; color: {text_color}; font-weight: 900;")

        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)
        card._value_label = value_lbl
        return card

    def _extract_service(self, note):
        if not note:
            return "Khám tổng quát"
        text = str(note)
        if text.startswith("Dịch vụ:"):
            payload = text.replace("Dịch vụ:", "", 1).strip()
            parts = payload.split("|", 1)
            return parts[0].strip() or "Khám tổng quát"
        return "Khám tổng quát"

    def _extract_plain_note(self, note):
        if not note:
            return ""
        text = str(note).strip()
        if not text.startswith("Dịch vụ:"):
            return text
        payload = text.replace("Dịch vụ:", "", 1).strip()
        parts = payload.split("|", 1)
        if len(parts) == 2:
            return parts[1].strip()
        return ""

    @staticmethod
    def _parse_datetime(value):
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
        return None

    def _calculate_age_text(self, dob_value):
        parsed = self._parse_datetime(dob_value)
        if not parsed:
            return "N/A"
        today = date.today()
        years = today.year - parsed.date().year
        if (today.month, today.day) < (parsed.date().month, parsed.date().day):
            years -= 1
        return str(max(0, years))

    def _status_code_from_filter(self):
        selected = self.status_filter.currentText()
        mapping = {
            "Chờ xác nhận": "pending",
            "Đã xác nhận": "confirmed",
            "Đang khám": "in_progress",
            "Đã khám": "done",
            "Đã hủy": "cancelled",
        }
        return mapping.get(selected)

    def _compute_priority(self, row):
        status = str(row.get("status", "pending"))
        if status == "cancelled":
            return "Bình thường", "#64748b"

        dt_value = self._parse_datetime(row.get("appointment_date"))
        if not dt_value:
            return "Bình thường", "#16a34a"

        delta_minutes = (dt_value - datetime.now()).total_seconds() / 60
        if delta_minutes < 0 and status in {"pending", "confirmed"}:
            return "Khẩn cấp", "#dc2626"
        if 0 <= delta_minutes <= 30 and status in {"pending", "confirmed"}:
            return "Sắp tới giờ", "#d97706"
        return "Bình thường", "#16a34a"

    def _matches_filters(self, row):
        dt_value = self._parse_datetime(row.get("appointment_date"))
        if not dt_value:
            return False

        from_dt = datetime(
            self.from_date.date().year(),
            self.from_date.date().month(),
            self.from_date.date().day(),
            0,
            0,
            0,
        )
        to_dt = datetime(
            self.to_date.date().year(),
            self.to_date.date().month(),
            self.to_date.date().day(),
            23,
            59,
            59,
        )
        if dt_value < from_dt or dt_value > to_dt:
            return False

        status_code = self._status_code_from_filter()
        if status_code and str(row.get("status", "")) != status_code:
            return False

        specialty_selected = self.specialty_filter.currentText()
        doctor_specialty = str(row.get("doctor_specialty", "") or "").strip()
        if specialty_selected != "Tất cả chuyên khoa" and doctor_specialty != specialty_selected:
            return False

        keyword = self.search_input.text().strip().lower()
        if keyword:
            haystack = (
                f"{row.get('patient_name', '')} {row.get('patient_phone', '')}"
            ).lower()
            if keyword not in haystack:
                return False

        return True

    def _update_stats(self):
        total = len(self.filtered_rows)
        pending = 0
        confirmed = 0
        done = 0
        cancelled = 0

        for row in self.filtered_rows:
            status = str(row.get("status", ""))
            if status == "pending":
                pending += 1
            elif status == "confirmed":
                confirmed += 1
            elif status == "done":
                done += 1
            elif status == "cancelled":
                cancelled += 1

        self.total_card._value_label.setText(str(total))
        self.pending_card._value_label.setText(str(pending))
        self.confirmed_card._value_label.setText(str(confirmed))
        self.done_card._value_label.setText(str(done))
        self.cancelled_card._value_label.setText(str(cancelled))

    def _update_reminder(self):
        nearest_minutes = None
        nearest_name = ""

        for row in self.filtered_rows:
            status = str(row.get("status", ""))
            if status not in {"pending", "confirmed"}:
                continue
            dt_value = self._parse_datetime(row.get("appointment_date"))
            if not dt_value:
                continue
            delta = int((dt_value - datetime.now()).total_seconds() // 60)
            if delta < 0:
                continue
            if nearest_minutes is None or delta < nearest_minutes:
                nearest_minutes = delta
                nearest_name = str(row.get("patient_name", ""))

        if nearest_minutes is None:
            self.reminder_banner.setText("Không có lịch hẹn gần giờ khám")
            return

        self.reminder_banner.setText(
            f"🔔 Còn {nearest_minutes} phút tới lịch khám của {nearest_name}"
        )

    def _build_action_buttons(self, row):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(4)

        buttons = [
            ("👁 Xem", "#e2e8f0", lambda checked=False, r=row: self._view_appointment(r)),
            ("✏ Sửa", "#dbeafe", lambda checked=False, r=row: self._edit_appointment(r)),
            ("🗑 Xóa", "#fee2e2", lambda checked=False, r=row: self._cancel_appointment(r)),
            ("🩺 Khám ngay", "#dcfce7", lambda checked=False, r=row: self._start_exam(r)),
        ]

        for text, bg, callback in buttons:
            btn = QtWidgets.QPushButton(text)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(
                f"QPushButton {{ background: {bg}; border: none; border-radius: 6px; padding: 5px 8px; font-size: 11px; font-weight: 700; }}"
                "QPushButton:hover { opacity: 0.92; }"
            )
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        return wrapper

    def _render_page(self):
        total_rows = len(self.filtered_rows)
        total_pages = max(1, (total_rows + self.page_size - 1) // self.page_size)
        self.current_page = max(1, min(self.current_page, total_pages))

        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        page_rows = self.filtered_rows[start:end]

        self.table.setRowCount(len(page_rows))
        for row_idx, row in enumerate(page_rows):
            dt_value = self._parse_datetime(row.get("appointment_date"))
            dt_text = dt_value.strftime("%d/%m/%Y - %H:%M") if dt_value else ""

            age_text = self._calculate_age_text(row.get("patient_dob"))
            patient_text = f"{row.get('patient_name', '')} ({age_text} tuổi, {row.get('patient_phone', '')})"
            service_text = self._extract_service(row.get("note"))
            status_code = str(row.get("status", "pending"))
            status_text = self.STATUS_LABELS.get(status_code, status_code)
            note_text = self._extract_plain_note(row.get("note"))
            priority_text, priority_color = self._compute_priority(row)

            cells = [
                dt_text,
                patient_text,
                service_text,
                status_text,
                note_text,
                priority_text,
            ]

            for col, text in enumerate(cells):
                item = QtWidgets.QTableWidgetItem(str(text))
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.table.setItem(row_idx, col, item)

            status_item = self.table.item(row_idx, 3)
            status_item.setForeground(QtGui.QBrush(QtGui.QColor(self.STATUS_COLORS.get(status_code, "#475569"))))

            priority_item = self.table.item(row_idx, 5)
            priority_item.setForeground(QtGui.QBrush(QtGui.QColor(priority_color)))

            self.table.setCellWidget(row_idx, 6, self._build_action_buttons(row))
            self.table.setRowHeight(row_idx, 52)

        self._render_pagination_buttons(total_pages)

    def _render_pagination_buttons(self, total_pages):
        while self.pagination_row.count() > 0:
            item = self.pagination_row.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.pagination_row.addStretch()

        visible = []
        if total_pages <= 5:
            visible = list(range(1, total_pages + 1))
        else:
            visible = [1, 2, 3, total_pages]

        last = None
        for page in visible:
            if last is not None and page - last > 1:
                ellipsis = QtWidgets.QLabel("...")
                ellipsis.setStyleSheet("color: #64748b; padding: 0 6px;")
                self.pagination_row.addWidget(ellipsis)

            btn = QtWidgets.QPushButton(str(page))
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            if page == self.current_page:
                btn.setStyleSheet(
                    "background: #69c0a5; color: white; border: none; border-radius: 6px; padding: 6px 10px; font-weight: 800;"
                )
            else:
                btn.setStyleSheet(
                    "background: #f1f5f9; color: #334155; border: none; border-radius: 6px; padding: 6px 10px;"
                )
            btn.clicked.connect(lambda checked=False, p=page: self._go_page(p))
            self.pagination_row.addWidget(btn)
            last = page

        self.pagination_row.addStretch()

    def _go_page(self, page):
        self.current_page = page
        self._render_page()

    def _on_filter_changed(self):
        self.current_page = 1
        self._apply_filters()

    def _apply_filters(self):
        self.filtered_rows = [row for row in self.all_rows if self._matches_filters(row)]
        self._update_stats()
        self._update_reminder()
        self._render_page()

    def load_data(self):
        self.all_rows = AppointmentController.get_management_rows_by_doctor(self.doctor_id)
        self._apply_filters()

    def _view_appointment(self, row):
        dt_value = self._parse_datetime(row.get("appointment_date"))
        dt_text = dt_value.strftime("%d/%m/%Y %H:%M") if dt_value else ""

        fields = [
            ("Mã lịch", row.get("appointment_id", "")),
            ("Thời gian", dt_text),
            ("Bệnh nhân", row.get("patient_name", "")),
            ("Số điện thoại", row.get("patient_phone", "")),
            ("Dịch vụ", self._extract_service(row.get("note"))),
            ("Trạng thái", self.STATUS_LABELS.get(str(row.get("status", "")), row.get("status", ""))),
            ("Ghi chú", self._extract_plain_note(row.get("note"))),
            ("Chuyên khoa", row.get("doctor_specialty", "")),
        ]

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Chi tiết lịch hẹn")
        dialog.setMinimumWidth(520)
        layout = QtWidgets.QVBoxLayout(dialog)

        form = QtWidgets.QFormLayout()
        for key, value in fields:
            label = QtWidgets.QLabel(str(value))
            label.setStyleSheet("color: #1e293b;")
            label.setWordWrap(True)
            form.addRow(f"{key}:", label)
        layout.addLayout(form)

        close_btn = QtWidgets.QPushButton("Đóng")
        close_btn.setStyleSheet(
            "background: #69c0a5; color: white; padding: 8px 14px; border-radius: 6px; font-weight: 700;"
        )
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        dialog.exec()

    def add_new(self):
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

        QtWidgets.QMessageBox.information(self, "Thành công", "Đã thêm lịch hẹn mới.")
        self.load_data()

    def _edit_appointment(self, row):
        detail = AppointmentController.get_by_id(row.get("appointment_id"))
        if not detail:
            QtWidgets.QMessageBox.warning(self, "Không tìm thấy", "Không thể đọc lịch hẹn để chỉnh sửa.")
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

        QtWidgets.QMessageBox.information(self, "Thành công", "Đã cập nhật lịch hẹn.")
        self.load_data()

    def _cancel_appointment(self, row):
        appointment_id = row.get("appointment_id")
        current_status = str(row.get("status", ""))

        if current_status == "done":
            QtWidgets.QMessageBox.information(
                self,
                "Không thể hủy",
                "Không thể hủy lịch hẹn đã hoàn tất.",
            )
            return

        if current_status == "cancelled":
            QtWidgets.QMessageBox.information(
                self,
                "Đã hủy trước đó",
                "Lịch hẹn này đã ở trạng thái Đã hủy.",
            )
            return

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Xác nhận hủy",
            "Bạn có chắc muốn hủy lịch hẹn này?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No,
        )
        if confirm != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        is_ok = AppointmentController.update_status(appointment_id, "cancelled")
        if not is_ok:
            QtWidgets.QMessageBox.warning(self, "Không thể hủy", "Không thể cập nhật trạng thái hủy.")
            return

        QtWidgets.QMessageBox.information(self, "Đã hủy", "Lịch hẹn đã được chuyển sang trạng thái Đã hủy.")
        self.load_data()

    def _start_exam(self, row):
        appointment_id = row.get("appointment_id")
        current_status = str(row.get("status", ""))

        if current_status in {"done", "cancelled"}:
            QtWidgets.QMessageBox.information(
                self,
                "Không thể bắt đầu",
                "Lịch hẹn đã hoàn tất hoặc đã hủy, không thể bắt đầu khám.",
            )
            return

        if current_status in {"pending", "confirmed"}:
            is_ok = AppointmentController.update_status(appointment_id, "in_progress")
            if not is_ok:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Không thể bắt đầu",
                    "Không thể cập nhật trạng thái lịch hẹn để bắt đầu khám.",
                )
                return

        QtWidgets.QMessageBox.information(
            self,
            "Bắt đầu khám",
            f"🩺 Đã sẵn sàng khám ngay cho bệnh nhân {row.get('patient_name', '')}.",
        )
        self.load_data()
