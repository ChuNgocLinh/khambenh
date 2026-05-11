from datetime import date, datetime
from PyQt6 import QtWidgets, QtCore, QtGui, QtPrintSupport
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
        self.role = "doctor"
        self.layout = QtWidgets.QVBoxLayout(self)
        
        title = QtWidgets.QLabel(title_text)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        self.layout.addWidget(title)
        
        toolbar = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm...")
        self.search_input.setStyleSheet(
            "padding: 8px; border-radius: 5px; border: 1px solid #ddd; font-size: 14px; color: #1f2937; background: white;"
        )
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

    def _has_staff_write_access(self, action_label):
        if str(getattr(self, "role", "") or "").lower().strip() != "staff":
            return True
        QtWidgets.QMessageBox.warning(
            self,
            "Từ chối truy cập",
            f"Nhân viên không có quyền {action_label}. Vui lòng liên hệ bác sĩ hoặc quản trị viên.",
        )
        return False


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
                "padding: 8px; border-radius: 6px; border: 1px solid #dbe2ea; font-size: 13px; color: #1f2937; background: white;"
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


class PatientEditDialog(QtWidgets.QDialog):
    def __init__(self, patient=None, parent=None):
        super().__init__(parent)
        self.patient = patient or {}
        self.setWindowTitle("Cập nhật thông tin bệnh nhân")
        self.setMinimumWidth(480)

        layout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("Cập nhật hồ sơ hành chính bệnh nhân")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #1e293b;")
        layout.addWidget(title)

        note = QtWidgets.QLabel(
            "Bạn có thể cập nhật thông tin nhận diện và liên hệ cơ bản. Email bệnh nhân hiện chưa được lưu trong cơ sở dữ liệu của phiên bản này."
        )
        note.setWordWrap(True)
        note.setStyleSheet(
            "color: #92400e; background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 8px; font-size: 12px;"
        )
        layout.addWidget(note)

        form = QtWidgets.QFormLayout()
        form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.name_input = QtWidgets.QLineEdit(str(self.patient.get("name", "") or ""))
        self.dob_input = QtWidgets.QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDisplayFormat("dd/MM/yyyy")
        parsed_dob = self._parse_datetime(self.patient.get("dob"))
        if parsed_dob:
            self.dob_input.setDate(QtCore.QDate(parsed_dob.year, parsed_dob.month, parsed_dob.day))
        else:
            self.dob_input.setDate(QtCore.QDate.currentDate().addYears(-18))

        self.gender_input = QtWidgets.QComboBox()
        self.gender_input.addItems(["Nam", "Nữ"])
        current_gender = str(self.patient.get("gender", "") or "")
        if current_gender:
            idx = self.gender_input.findText(current_gender)
            if idx >= 0:
                self.gender_input.setCurrentIndex(idx)

        self.phone_input = QtWidgets.QLineEdit(str(self.patient.get("phone", "") or ""))
        self.address_input = QtWidgets.QLineEdit(str(self.patient.get("address", "") or ""))

        for widget in [
            self.name_input,
            self.dob_input,
            self.gender_input,
            self.phone_input,
            self.address_input,
        ]:
            widget.setStyleSheet(
                "padding: 8px; border-radius: 6px; border: 1px solid #dbe2ea; font-size: 13px; color: #1f2937; background: white;"
            )

        form.addRow("Họ tên:", self.name_input)
        form.addRow("Ngày sinh:", self.dob_input)
        form.addRow("Giới tính:", self.gender_input)
        form.addRow("SĐT:", self.phone_input)
        form.addRow("Địa chỉ:", self.address_input)
        layout.addLayout(form)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch()

        cancel_btn = QtWidgets.QPushButton("Hủy")
        cancel_btn.setStyleSheet("padding: 8px 14px; border-radius: 6px; background: #f1f5f9;")
        cancel_btn.clicked.connect(self.reject)

        save_btn = QtWidgets.QPushButton("Lưu cập nhật")
        save_btn.setStyleSheet(
            "padding: 8px 14px; border-radius: 6px; background: #69c0a5; color: white; font-weight: 700;"
        )
        save_btn.clicked.connect(self._validate_and_accept)

        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

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

    def _validate_and_accept(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()

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

        self.accept()

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "dob": self.dob_input.date().toString("yyyy-MM-dd"),
            "gender": self.gender_input.currentText(),
            "phone": self.phone_input.text().strip(),
            "address": self.address_input.text().strip(),
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
            "QTableWidget { border: 1px solid #e2e8f0; border-radius: 10px; background: white; color: #1f2937; }"
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
    def __init__(self, doctor_id, parent=None, preselected_appointment_id=None, lock_appointment=False):
        super().__init__(parent)
        self.setWindowTitle("Tạo Bệnh Án")
        self.setMinimumWidth(400)
        self.doctor_id = doctor_id
        self.preselected_appointment_id = preselected_appointment_id
        self.lock_appointment = lock_appointment
        
        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        
        self.appt_combo = QtWidgets.QComboBox()
        # Load pending/in-progress appointments for this doctor
        self.appts = AppointmentController.get_by_doctor(self.doctor_id)
        for a in self.appts:
            if a["status"] not in ["pending", "in_progress", "confirmed"]:
                continue

            if self.preselected_appointment_id is not None and a.get("appointment_id") != self.preselected_appointment_id:
                continue

            self.appt_combo.addItem(f"{a['appointment_id']} - {a['patient_name']} ({a['appointment_date']})", a)

        if self.lock_appointment:
            self.appt_combo.setEnabled(False)
                
        self.diag_input = QtWidgets.QTextEdit()
        self.treat_input = QtWidgets.QTextEdit()
        
        form.addRow("Chọn Lịch Hẹn:", self.appt_combo)
        form.addRow("Chẩn đoán:", self.diag_input)
        form.addRow("Điều trị:", self.treat_input)
        
        layout.addLayout(form)
        
        btn_layout = QtWidgets.QHBoxLayout()
        save_btn = QtWidgets.QPushButton("Lưu Bệnh Án")
        save_btn.clicked.connect(self._validate_and_accept)
        cancel_btn = QtWidgets.QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn); btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def _validate_and_accept(self):
        if self.appt_combo.count() == 0:
            QtWidgets.QMessageBox.warning(self, "Thiếu lịch hẹn", "Không có lịch hẹn phù hợp để tạo bệnh án.")
            return

        diagnosis = self.diag_input.toPlainText().strip()
        treatment = self.treat_input.toPlainText().strip()
        if not diagnosis:
            QtWidgets.QMessageBox.warning(self, "Thiếu dữ liệu", "Vui lòng nhập chẩn đoán trước khi lưu bệnh án.")
            return
        if not treatment:
            QtWidgets.QMessageBox.warning(self, "Thiếu dữ liệu", "Vui lòng nhập hướng điều trị trước khi lưu bệnh án.")
            return

        self.accept()
        
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

        self.stock_note = QtWidgets.QLabel("")
        self.stock_note.setStyleSheet("color: #64748b; font-size: 12px;")
        
        form.addRow("Chọn Thuốc:", self.med_combo)
        form.addRow("Số lượng:", self.qty_input)
        form.addRow("Tồn kho:", self.stock_note)
        
        layout.addLayout(form)
        
        btn_layout = QtWidgets.QHBoxLayout()
        save_btn = QtWidgets.QPushButton("Thêm")
        save_btn.clicked.connect(self._validate_and_accept)
        cancel_btn = QtWidgets.QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn); btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.med_combo.currentIndexChanged.connect(self._sync_medicine_constraints)
        self._sync_medicine_constraints()

    def _sync_medicine_constraints(self):
        medicine = self.med_combo.currentData() or {}
        stock = int(medicine.get("quantity", 0) or 0)
        max_qty = max(1, stock)
        self.qty_input.setMaximum(max_qty)
        if self.qty_input.value() > max_qty:
            self.qty_input.setValue(max_qty)
        self.stock_note.setText(f"Kho hiện có: {stock}")

    def _validate_and_accept(self):
        medicine = self.med_combo.currentData() or {}
        stock = int(medicine.get("quantity", 0) or 0)
        qty = int(self.qty_input.value() or 0)

        if not medicine.get("medicine_id"):
            QtWidgets.QMessageBox.warning(self, "Thiếu dữ liệu", "Vui lòng chọn thuốc.")
            return

        if qty <= 0:
            QtWidgets.QMessageBox.warning(self, "Số lượng không hợp lệ", "Số lượng thuốc phải lớn hơn 0.")
            return

        if qty > stock:
            QtWidgets.QMessageBox.warning(
                self,
                "Vượt tồn kho",
                f"Số lượng kê ({qty}) vượt tồn kho hiện tại ({stock}).",
            )
            return

        self.accept()
        
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
        if not self._has_staff_write_access("chỉnh sửa hồ sơ bệnh án"):
            return
        dialog = MedicalRecordDialog(self.doctor_id, self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data["patient_id"]:
                created = MedicalRecordController.create(
                    data["patient_id"],
                    self.doctor_id,
                    data["appointment_id"],
                    data["diagnosis"],
                    data["treatment"],
                )
                if not created:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Không thể lưu bệnh án",
                        "Lưu bệnh án thất bại nên trạng thái lịch hẹn chưa bị thay đổi.",
                    )
                    return

                # Only transition to done after medical record was persisted successfully.
                is_status_updated = AppointmentController.update_status(data["appointment_id"], "done")
                if not is_status_updated:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Cần kiểm tra trạng thái lịch",
                        "Đã lưu bệnh án nhưng chưa cập nhật được trạng thái lịch hẹn sang Đã khám.",
                    )
                self.load_data()
                
    def add_prescription(self, record_id):
        if not self._has_staff_write_access("chỉnh sửa đơn thuốc"):
            return
        dialog = PrescriptionDialog(record_id, self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data["medicine_id"]:
                created = PrescriptionController.add(data["record_id"], data["medicine_id"], data["quantity"])
                if not created:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Không thể kê đơn",
                        "Hệ thống không thể lưu đơn thuốc. Tồn kho chưa bị trừ tự động trong phiên bản hiện tại.",
                    )
                    return
                QtWidgets.QMessageBox.information(
                    self,
                    "Thành công",
                    "Đã kê đơn thuốc thành công. Hệ thống chỉ kiểm tra tồn kho và chưa tự động trừ số lượng thuốc.",
                )


class PrescriptionView(BaseDoctorView):
    def __init__(self, doctor_id):
        super().__init__(
            "Đơn thuốc",
            [
                "Mã đơn thuốc",
                "Bệnh nhân / tuổi / giới tính",
                "Ngày giờ kê",
                "Chẩn đoán",
                "Trạng thái",
                "Thao tác",
            ],
            doctor_id,
        )
        self.btn_add.hide()
        self.all_rows = []
        self.filtered_rows = []

        self.search_input.setPlaceholderText("Tìm theo mã đơn, bệnh nhân, thuốc hoặc chẩn đoán...")
        self.btn_search.setText("Áp dụng")

        desc = QtWidgets.QLabel(
            "Tra cứu đơn thuốc theo thời gian, bệnh nhân và trạng thái nghiệp vụ; bác sĩ có thể xem nhanh hoặc in lại phiếu kê đơn khi cần."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #64748b; font-size: 13px; margin-bottom: 8px;")
        self.layout.insertWidget(1, desc)

        self._setup_filters()
        self._setup_stats()
        self._setup_status_note()

        self.search_input.textChanged.connect(self._on_filter_changed)

        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setColumnWidth(0, 130)
        self.table.setColumnWidth(1, 280)
        self.table.setColumnWidth(2, 170)
        self.table.setColumnWidth(3, 250)
        self.table.setColumnWidth(5, 220)
        self.load_data()

    def load_data(self):
        from database.db import fetch_all
        rows = fetch_all(
            """
            SELECT
                pr.prescription_id,
                pr.record_id,
                pr.quantity,
                mr.patient_id,
                mr.diagnosis,
                mr.treatment,
                mr.created_at,
                mr.appointment_id,
                p.name AS patient_name,
                p.gender AS patient_gender,
                p.dob AS patient_dob,
                m.name AS medicine_name,
                m.description AS medicine_description,
                a.status AS appointment_status,
                a.note AS appointment_note,
                a.appointment_date
            FROM Prescriptions pr
            JOIN MedicalRecords mr ON pr.record_id = mr.record_id
            JOIN Patients p ON mr.patient_id = p.patient_id
            JOIN Medicines m ON pr.medicine_id = m.medicine_id
            LEFT JOIN Appointments a ON mr.appointment_id = a.appointment_id
            WHERE mr.doctor_id = ?
            ORDER BY mr.created_at DESC, pr.prescription_id DESC
            """,
            (self.doctor_id,),
        )

        grouped = {}
        for item in rows:
            record_id = int(item.get("record_id", 0) or 0)
            if record_id not in grouped:
                status_code, status_label, status_color = self._derive_business_status(item.get("appointment_status"))
                grouped[record_id] = {
                    "record_id": record_id,
                    "prescription_code": f"DT{record_id:05d}",
                    "patient_id": item.get("patient_id"),
                    "patient_name": item.get("patient_name", ""),
                    "patient_gender": item.get("patient_gender", ""),
                    "patient_dob": item.get("patient_dob"),
                    "diagnosis": item.get("diagnosis", ""),
                    "treatment": item.get("treatment", ""),
                    "created_at": item.get("created_at"),
                    "appointment_id": item.get("appointment_id"),
                    "appointment_status": item.get("appointment_status"),
                    "appointment_note": item.get("appointment_note", ""),
                    "appointment_date": item.get("appointment_date"),
                    "status_code": status_code,
                    "status_label": status_label,
                    "status_color": status_color,
                    "items": [],
                }

            grouped[record_id]["items"].append(
                {
                    "prescription_id": item.get("prescription_id"),
                    "medicine_name": item.get("medicine_name", ""),
                    "medicine_description": item.get("medicine_description", ""),
                    "quantity": item.get("quantity", 0),
                }
            )

        self.all_rows = list(grouped.values())
        self._refresh_patient_filter_options()
        self._apply_filters()

    def _setup_filters(self):
        today = QtCore.QDate.currentDate()
        self.from_date = QtWidgets.QDateEdit(today.addMonths(-1))
        self.from_date.setCalendarPopup(True)
        self.from_date.setDisplayFormat("dd/MM/yyyy")

        self.to_date = QtWidgets.QDateEdit(today)
        self.to_date.setCalendarPopup(True)
        self.to_date.setDisplayFormat("dd/MM/yyyy")

        self.patient_filter = QtWidgets.QComboBox()
        self.patient_filter.addItem("Tất cả bệnh nhân", None)

        self.status_filter = QtWidgets.QComboBox()
        self.status_filter.addItems(
            [
                "Tất cả trạng thái",
                "Chờ khám / đang khám",
                "Đã hoàn tất khám",
                "Đã hủy",
            ]
        )

        filter_row = QtWidgets.QHBoxLayout()
        filter_row.setSpacing(10)

        for title, widget in [
            ("Từ ngày", self.from_date),
            ("Đến ngày", self.to_date),
            ("Bệnh nhân", self.patient_filter),
            ("Trạng thái", self.status_filter),
        ]:
            block = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel(title)
            label.setStyleSheet("color: #475569; font-size: 12px; font-weight: 700;")
            widget.setStyleSheet(
                "padding: 7px 8px; border-radius: 6px; border: 1px solid #dbe2ea; background: white; color: #1f2937;"
            )
            block.addWidget(label)
            block.addWidget(widget)
            holder = QtWidgets.QWidget()
            holder.setLayout(block)
            filter_row.addWidget(holder)

        filter_row.addStretch()
        self.layout.insertLayout(2, filter_row)

        self.from_date.dateChanged.connect(self._on_filter_changed)
        self.to_date.dateChanged.connect(self._on_filter_changed)
        self.patient_filter.currentIndexChanged.connect(self._on_filter_changed)
        self.status_filter.currentIndexChanged.connect(self._on_filter_changed)

    def _setup_stats(self):
        self.stats_row = QtWidgets.QHBoxLayout()
        self.stats_row.setSpacing(10)
        self.layout.insertLayout(3, self.stats_row)

        self.total_card = self._build_stat_card("📋 Tổng đơn", "0", "#eff6ff", "#1d4ed8")
        self.done_card = self._build_stat_card("✅ Đã hoàn tất khám", "0", "#ecfdf3", "#15803d")
        self.waiting_card = self._build_stat_card("⏳ Chờ khám / đang khám", "0", "#fff7ed", "#c2410c")
        self.cancelled_card = self._build_stat_card("❌ Đã hủy", "0", "#fef2f2", "#b91c1c")

        for card in [
            self.total_card,
            self.done_card,
            self.waiting_card,
            self.cancelled_card,
        ]:
            self.stats_row.addWidget(card)

    def _setup_status_note(self):
        self.status_note = QtWidgets.QLabel(
            "Ghi chú nghiệp vụ: Trạng thái trên màn hình đơn thuốc phản ánh tiến trình lịch hẹn liên kết (không phải trạng thái phát thuốc), vì cơ sở dữ liệu hiện chưa có cột prescription_status riêng."
        )
        self.status_note.setWordWrap(True)
        self.status_note.setStyleSheet(
            "padding: 8px 10px; border-radius: 8px; background: #fffbea; color: #92400e; border: 1px solid #fde68a;"
        )
        self.layout.insertWidget(4, self.status_note)

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

    def _refresh_patient_filter_options(self):
        current_patient_id = self.patient_filter.currentData()
        self.patient_filter.blockSignals(True)
        self.patient_filter.clear()
        self.patient_filter.addItem("Tất cả bệnh nhân", None)

        seen = set()
        for row in self.all_rows:
            patient_id = row.get("patient_id")
            if patient_id in seen:
                continue
            seen.add(patient_id)
            self.patient_filter.addItem(str(row.get("patient_name", "")), patient_id)

        if current_patient_id is not None:
            idx = self.patient_filter.findData(current_patient_id)
            if idx >= 0:
                self.patient_filter.setCurrentIndex(idx)
        self.patient_filter.blockSignals(False)

    def _on_filter_changed(self):
        self._apply_filters()

    def _apply_filters(self):
        self.filtered_rows = [row for row in self.all_rows if self._matches_filters(row)]
        self._update_stats()
        self._render_table()

    def _matches_filters(self, row):
        dt_value = self._parse_datetime(row.get("created_at"))
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

        patient_id = self.patient_filter.currentData()
        if patient_id is not None and row.get("patient_id") != patient_id:
            return False

        status_selected = self.status_filter.currentText()
        if status_selected != "Tất cả trạng thái" and row.get("status_label") != status_selected:
            return False

        keyword = self.search_input.text().strip().lower()
        if keyword:
            medicine_text = ", ".join(
                f"{item.get('medicine_name', '')} x{item.get('quantity', 0)}" for item in row.get("items", [])
            )
            haystack = (
                f"{row.get('prescription_code', '')} {row.get('patient_name', '')} {row.get('diagnosis', '')} {medicine_text}"
            ).lower()
            if keyword not in haystack:
                return False

        return True

    def _update_stats(self):
        total = len(self.filtered_rows)
        waiting_count = 0
        done_count = 0
        cancelled_count = 0

        for row in self.filtered_rows:
            status_code = row.get("status_code")
            if status_code == "waiting_exam":
                waiting_count += 1
            elif status_code == "done_exam":
                done_count += 1
            elif status_code == "cancelled":
                cancelled_count += 1

        self.total_card._value_label.setText(str(total))
        self.done_card._value_label.setText(str(done_count))
        self.waiting_card._value_label.setText(str(waiting_count))
        self.cancelled_card._value_label.setText(str(cancelled_count))

    def _render_table(self):
        self.table.setRowCount(len(self.filtered_rows))
        for row_idx, row in enumerate(self.filtered_rows):
            dt_text = self._format_datetime(row.get("created_at"), "%d/%m/%Y - %H:%M")
            age_text = self._calculate_age_text(row.get("patient_dob"))
            patient_text = f"{row.get('patient_name', '')} ({age_text} tuổi • {row.get('patient_gender', 'N/A')})"

            cells = [
                row.get("prescription_code", ""),
                patient_text,
                dt_text,
                row.get("diagnosis", "") or "Chưa cập nhật chẩn đoán",
                row.get("status_label", "Chưa xác định"),
            ]

            for col, text in enumerate(cells):
                item = QtWidgets.QTableWidgetItem(str(text))
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.table.setItem(row_idx, col, item)

            status_item = self.table.item(row_idx, 4)
            status_item.setForeground(QtGui.QBrush(QtGui.QColor(row.get("status_color", "#475569"))))

            self.table.setCellWidget(row_idx, 5, self._build_action_buttons(row))
            self.table.setRowHeight(row_idx, 50)

    def _build_action_buttons(self, row):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(4)

        for text, bg, callback in [
            ("👁 Xem", "#e2e8f0", lambda checked=False, r=row: self._view_prescription(r)),
            ("🖨 In", "#dcfce7", lambda checked=False, r=row: self._print_prescription(r)),
        ]:
            btn = QtWidgets.QPushButton(text)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(
                f"QPushButton {{ background: {bg}; border: none; border-radius: 6px; padding: 5px 8px; font-size: 11px; font-weight: 700; }}"
                "QPushButton:hover { opacity: 0.92; }"
            )
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        return wrapper

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

    def _format_datetime(self, value, output_format):
        parsed = self._parse_datetime(value)
        if parsed:
            return parsed.strftime(output_format)
        return ""

    def _calculate_age_text(self, dob_value):
        parsed = self._parse_datetime(dob_value)
        if not parsed:
            return "N/A"
        today = date.today()
        years = today.year - parsed.date().year
        if (today.month, today.day) < (parsed.date().month, parsed.date().day):
            years -= 1
        return str(max(0, years))

    def _derive_business_status(self, appointment_status):
        status_code = str(appointment_status or "").lower()

        # Derive a safe business-facing prescription status from appointment state
        # because the current schema has no dedicated prescription_status column.
        if status_code == "cancelled":
            return "cancelled", "Đã hủy", "#b91c1c"
        if status_code == "done":
            return "done_exam", "Đã hoàn tất khám", "#15803d"
        if status_code in {"pending", "confirmed", "in_progress"}:
            return "waiting_exam", "Chờ khám / đang khám", "#c2410c"
        return "waiting_exam", "Chờ khám / đang khám", "#c2410c"

    def _view_prescription(self, row):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(f"Chi tiết {row.get('prescription_code', '')}")
        dialog.resize(760, 520)

        layout = QtWidgets.QVBoxLayout(dialog)

        title = QtWidgets.QLabel(f"{row.get('prescription_code', '')} • Đơn thuốc bệnh nhân")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #1e293b;")
        layout.addWidget(title)

        summary = QtWidgets.QLabel(
            f"{row.get('patient_name', '')} • {self._calculate_age_text(row.get('patient_dob'))} tuổi • {row.get('patient_gender', 'N/A')} • {self._format_datetime(row.get('created_at'), '%d/%m/%Y %H:%M')}"
        )
        summary.setStyleSheet("color: #64748b; font-size: 13px;")
        layout.addWidget(summary)

        form = QtWidgets.QFormLayout()
        for key, value in [
            ("Chẩn đoán", row.get("diagnosis", "Chưa cập nhật")),
            ("Hướng điều trị", row.get("treatment", "Chưa cập nhật")),
            ("Trạng thái đơn", row.get("status_label", "Chưa xác định")),
            ("Ghi chú lịch hẹn", row.get("appointment_note", "Chưa có ghi chú")),
        ]:
            label = QtWidgets.QLabel(str(value))
            label.setWordWrap(True)
            label.setStyleSheet("color: #1e293b;")
            form.addRow(f"{key}:", label)
        layout.addLayout(form)

        table = QtWidgets.QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Thuốc", "Số lượng", "Mô tả"])
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setStyleSheet(
            "QTableWidget { border: 1px solid #e2e8f0; border-radius: 10px; background: white; color: #1f2937; }"
            "QHeaderView::section { background-color: #f8fafc; padding: 10px; font-weight: 700; }"
            "QTableWidget::item { padding: 8px; border-bottom: 1px solid #f1f5f9; }"
        )
        items = row.get("items", [])
        table.setRowCount(len(items))
        for idx, item in enumerate(items):
            table.setItem(idx, 0, QtWidgets.QTableWidgetItem(str(item.get("medicine_name", ""))))
            table.setItem(idx, 1, QtWidgets.QTableWidgetItem(str(item.get("quantity", 0))))
            table.setItem(idx, 2, QtWidgets.QTableWidgetItem(str(item.get("medicine_description", "") or "Không có mô tả")))
            table.setRowHeight(idx, 42)
        layout.addWidget(table)

        note = QtWidgets.QLabel(
            "Trạng thái hiển thị trên đơn thuốc là tiến trình lịch hẹn liên kết, không phải trạng thái phát thuốc độc lập của đơn."
        )
        note.setWordWrap(True)
        note.setStyleSheet(
            "color: #92400e; background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 8px; font-size: 12px;"
        )
        layout.addWidget(note)

        close_btn = QtWidgets.QPushButton("Đóng")
        close_btn.setStyleSheet(
            "background: #69c0a5; color: white; padding: 8px 14px; border-radius: 6px; font-weight: 700;"
        )
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        dialog.exec()

    def _print_prescription(self, row):
        document = QtGui.QTextDocument(self)
        document.setHtml(self._build_prescription_print_html(row))

        preview = QtPrintSupport.QPrintPreviewDialog(self)
        preview.setWindowTitle(f"In {row.get('prescription_code', '')}")
        preview.paintRequested.connect(document.print)
        preview.exec()

    def _build_prescription_print_html(self, row):
        item_lines = "".join(
            (
                f"<tr>"
                f"<td style='padding:6px 8px; border:1px solid #dbe2ea;'>{item.get('medicine_name', '')}</td>"
                f"<td style='padding:6px 8px; border:1px solid #dbe2ea; text-align:center;'>{item.get('quantity', 0)}</td>"
                f"<td style='padding:6px 8px; border:1px solid #dbe2ea;'>{item.get('medicine_description', '') or 'Không có mô tả'}</td>"
                f"</tr>"
            )
            for item in row.get("items", [])
        )
        if not item_lines:
            item_lines = (
                "<tr><td colspan='3' style='padding:6px 8px; border:1px solid #dbe2ea;'>"
                "Chưa có dữ liệu thuốc"
                "</td></tr>"
            )

        return f"""
        <h2 style='color:#1e293b;'>Đơn thuốc {row.get('prescription_code', '')}</h2>
        <p><strong>Bệnh nhân:</strong> {row.get('patient_name', '')}</p>
        <p><strong>Thời điểm kê:</strong> {self._format_datetime(row.get('created_at'), '%d/%m/%Y %H:%M')}</p>
        <p><strong>Chẩn đoán:</strong> {row.get('diagnosis', '') or 'Chưa cập nhật'}</p>
        <p><strong>Trạng thái:</strong> {row.get('status_label', 'Chưa xác định')}</p>
        <table cellspacing='0' cellpadding='0' style='border-collapse:collapse; width:100%; margin-top:12px;'>
            <thead>
                <tr>
                    <th style='padding:6px 8px; border:1px solid #dbe2ea; background:#f8fafc;'>Thuốc</th>
                    <th style='padding:6px 8px; border:1px solid #dbe2ea; background:#f8fafc;'>Số lượng</th>
                    <th style='padding:6px 8px; border:1px solid #dbe2ea; background:#f8fafc;'>Mô tả</th>
                </tr>
            </thead>
            <tbody>{item_lines}</tbody>
        </table>
        <p style='margin-top:12px; color:#92400e; font-size:12px;'>
            Lưu ý: Trạng thái đơn thuốc phản ánh tiến trình lịch hẹn liên kết vì schema hiện tại chưa có cột prescription_status riêng.
        </p>
        """


class DoctorPatientListView(QtWidgets.QWidget):
    def __init__(self, doctor_id, parent=None):
        super().__init__(parent)
        self.doctor_id = doctor_id
        self.role = "doctor"
        self._selected_row = 0
        self._active_tab = 0

        # ── Mock data ──
        self._mock_patients = [
            {"stt": 1, "code": "BN000123", "name": "Nguyễn Văn Nam", "gender": "Nam", "dob": "15/02/1990", "phone": "0987 654 321", "last_visit": "23/05/2026", "status": "Đang điều trị", "status_color": "#e67e22", "status_bg": "#fdf2e9", "age": 35},
            {"stt": 2, "code": "BN000124", "name": "Trần Thị Mai", "gender": "Nữ", "dob": "22/08/1988", "phone": "0988 123 456", "last_visit": "20/05/2026", "status": "Tái khám", "status_color": "#3498db", "status_bg": "#ebf5fb", "age": 37},
            {"stt": 3, "code": "BN000125", "name": "Lê Văn Nam", "gender": "Nam", "dob": "03/06/1975", "phone": "0912 345 678", "last_visit": "18/05/2026", "status": "Tái khám", "status_color": "#3498db", "status_bg": "#ebf5fb", "age": 50},
            {"stt": 4, "code": "BN000126", "name": "Phạm Thị Lan", "gender": "Nữ", "dob": "12/11/1992", "phone": "0909 876 543", "last_visit": "23/05/2026", "status": "Bệnh nhân mới", "status_color": "#27ae60", "status_bg": "#eafaf1", "age": 33},
            {"stt": 5, "code": "BN000127", "name": "Hoàng Anh Tuấn", "gender": "Nam", "dob": "30/09/1985", "phone": "0933 456 789", "last_visit": "21/05/2026", "status": "Đang điều trị", "status_color": "#e67e22", "status_bg": "#fdf2e9", "age": 40},
            {"stt": 6, "code": "BN000128", "name": "Vũ Thị Hương", "gender": "Nữ", "dob": "05/04/1991", "phone": "0977 111 222", "last_visit": "17/05/2026", "status": "Tái khám", "status_color": "#3498db", "status_bg": "#ebf5fb", "age": 35},
            {"stt": 7, "code": "BN000129", "name": "Đỗ Minh Quân", "gender": "Nam", "dob": "18/01/2000", "phone": "0966 333 444", "last_visit": "23/05/2026", "status": "Bệnh nhân mới", "status_color": "#27ae60", "status_bg": "#eafaf1", "age": 26},
            {"stt": 8, "code": "BN000130", "name": "Nguyễn Thị Hoa", "gender": "Nữ", "dob": "25/12/1970", "phone": "0908 555 666", "last_visit": "29/05/2026", "status": "Tái khám", "status_color": "#3498db", "status_bg": "#ebf5fb", "age": 55},
            {"stt": 9, "code": "BN000131", "name": "Bùi Văn Dũng", "gender": "Nam", "dob": "02/03/1982", "phone": "0982 777 888", "last_visit": "16/05/2026", "status": "Đang điều trị", "status_color": "#e67e22", "status_bg": "#fdf2e9", "age": 44},
            {"stt": 10, "code": "BN000132", "name": "Trương Thị Kiều", "gender": "Nữ", "dob": "09/07/1995", "phone": "0933 999 000", "last_visit": "22/05/2026", "status": "Bệnh nhân mới", "status_color": "#27ae60", "status_bg": "#eafaf1", "age": 30},
        ]

        self._init_ui()

    def _init_ui(self):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: #f0f4f8; border: none;")

        container = QtWidgets.QWidget()
        container.setStyleSheet("background: #f0f4f8;")
        main = QtWidgets.QVBoxLayout(container)
        main.setContentsMargins(28, 18, 28, 18)
        main.setSpacing(14)

        # ── Title + Breadcrumb ──
        title = QtWidgets.QLabel("Danh sách bệnh nhân")
        title.setStyleSheet("font-size: 22px; font-weight: 800; color: #1e293b; background: transparent;")
        main.addWidget(title)
        bc = QtWidgets.QLabel("Trang chủ  ›  Danh sách bệnh nhân")
        bc.setStyleSheet("font-size: 12px; color: #94a3b8; background: transparent;")
        main.addWidget(bc)
        main.addSpacing(4)

        # ── Search / Filter row ──
        filter_card = QtWidgets.QFrame()
        filter_card.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #e2e8f0;")
        fl = QtWidgets.QHBoxLayout(filter_card)
        fl.setContentsMargins(14, 10, 14, 10)
        fl.setSpacing(10)

        search = QtWidgets.QLineEdit()
        search.setPlaceholderText("🔍  Tìm kiếm bệnh nhân theo tên, SĐT, mã BN...")
        search.setFixedHeight(36)
        search.setStyleSheet("padding: 0 10px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 13px; color: #334155; background: #f8fafc;")
        fl.addWidget(search, 3)

        for text in ["Tất cả giới tính", "Tất cả độ tuổi", "Tất cả trạng thái"]:
            cb = QtWidgets.QComboBox()
            cb.addItem(text)
            cb.setFixedHeight(36)
            cb.setStyleSheet("padding: 0 10px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 13px; color: #334155; background: white;")
            fl.addWidget(cb, 1)

        btn_add = QtWidgets.QPushButton("+  Thêm bệnh nhân")
        btn_add.setFixedHeight(36)
        btn_add.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        btn_add.setStyleSheet("background: #22c55e; color: white; font-weight: 700; font-size: 13px; border: none; border-radius: 8px; padding: 0 18px;")
        fl.addWidget(btn_add)
        main.addWidget(filter_card)

        # ── Tabs row ──
        tabs_row = QtWidgets.QHBoxLayout()
        tabs_row.setSpacing(0)
        tab_data = [
            ("Tất cả (156)", True),
            ("Bệnh nhân mới (23)", False),
            ("Đang điều trị (41)", False),
            ("Tái khám (76)", False),
            ("Khám gần đây (30)", False),
        ]
        for label, active in tab_data:
            tb = QtWidgets.QPushButton(label)
            tb.setFixedHeight(34)
            tb.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            if active:
                tb.setStyleSheet("background: white; color: #22c55e; font-weight: 700; font-size: 13px; border: 2px solid #22c55e; border-radius: 8px; padding: 0 16px; margin-right: 6px;")
            else:
                tb.setStyleSheet("background: white; color: #64748b; font-weight: 600; font-size: 13px; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0 16px; margin-right: 6px;")
            tabs_row.addWidget(tb)
        tabs_row.addStretch()
        btn_export = QtWidgets.QPushButton("⬇  Xuất danh sách")
        btn_export.setFixedHeight(34)
        btn_export.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        btn_export.setStyleSheet("background: white; color: #334155; font-weight: 600; font-size: 13px; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0 16px;")
        tabs_row.addWidget(btn_export)
        main.addLayout(tabs_row)

        # ── Body: Table (left) + Detail panel (right) ──
        body = QtWidgets.QHBoxLayout()
        body.setSpacing(16)

        # ─── TABLE CARD ───
        table_card = QtWidgets.QFrame()
        table_card.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #e2e8f0;")
        tc_l = QtWidgets.QVBoxLayout(table_card)
        tc_l.setContentsMargins(0, 0, 0, 0)
        tc_l.setSpacing(0)

        headers = ["STT", "Mã bệnh nhân", "Họ và tên", "Giới tính", "Ngày sinh", "SĐT", "Lần khám gần nhất", "Trạng thái", "Thao tác"]
        table = QtWidgets.QTableWidget(len(self._mock_patients), len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setStyleSheet("""
            QTableWidget { border: none; background: white; font-size: 13px; color: #334155; }
            QHeaderView::section { background: #f8fafc; color: #64748b; font-weight: 700; font-size: 12px; border: none; border-bottom: 1px solid #e2e8f0; padding: 10px 8px; }
            QTableWidget::item { border-bottom: 1px solid #f1f5f9; padding: 6px 8px; }
        """)
        table.horizontalHeader().setStretchLastSection(True)
        table.setColumnWidth(0, 40)
        table.setColumnWidth(1, 100)
        table.setColumnWidth(2, 150)
        table.setColumnWidth(3, 65)
        table.setColumnWidth(4, 90)
        table.setColumnWidth(5, 105)
        table.setColumnWidth(6, 120)
        table.setColumnWidth(7, 110)

        for r, p in enumerate(self._mock_patients):
            table.setItem(r, 0, QtWidgets.QTableWidgetItem(str(p["stt"])))
            table.setItem(r, 1, QtWidgets.QTableWidgetItem(p["code"]))

            # Name cell with avatar
            name_w = QtWidgets.QWidget()
            name_l = QtWidgets.QHBoxLayout(name_w)
            name_l.setContentsMargins(4, 2, 4, 2)
            name_l.setSpacing(8)
            avt = QtWidgets.QLabel("👤")
            avt.setFixedSize(28, 28)
            avt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            avt_bg = "#dbeafe" if p["gender"] == "Nam" else "#fce7f3"
            avt.setStyleSheet(f"background: {avt_bg}; border-radius: 14px; font-size: 13px;")
            n_lbl = QtWidgets.QLabel(p["name"])
            n_lbl.setStyleSheet("font-weight: 600; color: #1e293b; font-size: 13px; background: transparent; border: none;")
            name_l.addWidget(avt)
            name_l.addWidget(n_lbl)
            name_l.addStretch()
            table.setCellWidget(r, 2, name_w)

            table.setItem(r, 3, QtWidgets.QTableWidgetItem(p["gender"]))
            table.setItem(r, 4, QtWidgets.QTableWidgetItem(p["dob"]))
            table.setItem(r, 5, QtWidgets.QTableWidgetItem(p["phone"]))
            table.setItem(r, 6, QtWidgets.QTableWidgetItem(p["last_visit"]))

            # Status badge
            st_w = QtWidgets.QWidget()
            st_l = QtWidgets.QHBoxLayout(st_w)
            st_l.setContentsMargins(4, 0, 4, 0)
            st_l.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
            badge = QtWidgets.QLabel(p["status"])
            badge.setStyleSheet(f"background: {p['status_bg']}; color: {p['status_color']}; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 10px;")
            st_l.addWidget(badge)
            table.setCellWidget(r, 7, st_w)

            # Action icons
            act_w = QtWidgets.QWidget()
            act_l = QtWidgets.QHBoxLayout(act_w)
            act_l.setContentsMargins(4, 0, 4, 0)
            act_l.setSpacing(4)
            for icon, bg, fg in [("👁", "#e0f2fe", "#0284c7"), ("✏", "#dcfce7", "#16a34a"), ("🗑", "#fee2e2", "#dc2626")]:
                ab = QtWidgets.QPushButton(icon)
                ab.setFixedSize(26, 26)
                ab.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                ab.setStyleSheet(f"background: {bg}; border: none; border-radius: 6px; font-size: 12px;")
                act_l.addWidget(ab)
            dots = QtWidgets.QPushButton("⋮")
            dots.setFixedSize(22, 26)
            dots.setStyleSheet("background: transparent; border: none; font-size: 16px; color: #64748b;")
            act_l.addWidget(dots)
            table.setCellWidget(r, 8, act_w)
            table.setRowHeight(r, 48)

        tc_l.addWidget(table)

        # ── Pagination ──
        pag = QtWidgets.QWidget()
        pag.setStyleSheet("background: white; border-top: 1px solid #f1f5f9;")
        pag_l = QtWidgets.QHBoxLayout(pag)
        pag_l.setContentsMargins(14, 8, 14, 8)
        show_lbl = QtWidgets.QLabel("Hiển thị")
        show_lbl.setStyleSheet("font-size: 12px; color: #64748b;")
        pag_l.addWidget(show_lbl)
        per_page = QtWidgets.QComboBox()
        per_page.addItems(["10", "20", "50"])
        per_page.setFixedWidth(55)
        per_page.setStyleSheet("border: 1px solid #e2e8f0; border-radius: 4px; padding: 2px; font-size: 12px;")
        pag_l.addWidget(per_page)
        rec_lbl = QtWidgets.QLabel("bản ghi")
        rec_lbl.setStyleSheet("font-size: 12px; color: #64748b;")
        pag_l.addWidget(rec_lbl)
        pag_l.addStretch()

        prev_btn = QtWidgets.QPushButton("<")
        prev_btn.setFixedSize(30, 30)
        prev_btn.setStyleSheet("background: white; border: 1px solid #e2e8f0; border-radius: 6px; font-weight: 700; color: #64748b;")
        pag_l.addWidget(prev_btn)
        for pg_num in ["1", "2", "3", "4", "5", "...", "16"]:
            pg = QtWidgets.QPushButton(pg_num)
            pg.setFixedSize(30, 30)
            if pg_num == "1":
                pg.setStyleSheet("background: #22c55e; color: white; border: none; border-radius: 6px; font-weight: 700; font-size: 12px;")
            else:
                pg.setStyleSheet("background: white; border: 1px solid #e2e8f0; border-radius: 6px; color: #334155; font-size: 12px;")
            pag_l.addWidget(pg)
        next_btn = QtWidgets.QPushButton(">")
        next_btn.setFixedSize(30, 30)
        next_btn.setStyleSheet("background: white; border: 1px solid #e2e8f0; border-radius: 6px; font-weight: 700; color: #64748b;")
        pag_l.addWidget(next_btn)
        tc_l.addWidget(pag)

        body.addWidget(table_card, 7)

        # ─── RIGHT DETAIL PANEL ───
        detail = QtWidgets.QFrame()
        detail.setFixedWidth(300)
        detail.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #e2e8f0;")
        dl = QtWidgets.QVBoxLayout(detail)
        dl.setContentsMargins(18, 18, 18, 18)
        dl.setSpacing(10)

        dt = QtWidgets.QLabel("Thông tin bệnh nhân")
        dt.setStyleSheet("font-size: 15px; font-weight: 800; color: #1e293b; background: transparent;")
        dl.addWidget(dt)

        # Profile header
        ph = QtWidgets.QHBoxLayout()
        av = QtWidgets.QLabel("👤")
        av.setFixedSize(52, 52)
        av.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        av.setStyleSheet("background: #e0f2fe; border-radius: 26px; font-size: 24px;")
        ph.addWidget(av)
        pinfo = QtWidgets.QVBoxLayout()
        pinfo.setSpacing(2)

        p_name_row = QtWidgets.QHBoxLayout()
        p_name = QtWidgets.QLabel("Nguyễn Văn Nam")
        p_name.setStyleSheet("font-size: 15px; font-weight: 800; color: #1e293b; background: transparent;")
        p_gender_badge = QtWidgets.QLabel("Nam")
        p_gender_badge.setStyleSheet("background: #dbeafe; color: #2563eb; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 8px;")
        p_name_row.addWidget(p_name)
        p_name_row.addWidget(p_gender_badge)
        p_name_row.addStretch()
        pinfo.addLayout(p_name_row)

        for lbl in ["Mã BN: BN000123", "35 tuổi  ·  15/02/1990", "0987 654 321", "Địa chỉ: 123 Đường Lê Lợi, P1, Q.1, TPHCM"]:
            l = QtWidgets.QLabel(lbl)
            l.setStyleSheet("font-size: 11px; color: #64748b; background: transparent;")
            l.setWordWrap(True)
            pinfo.addWidget(l)
        ph.addLayout(pinfo)
        dl.addLayout(ph)

        # Info tabs row
        info_tabs = QtWidgets.QHBoxLayout()
        for tab_text, is_active in [("Thông tin chung", True), ("Tiền sử bệnh", False), ("Lịch sử khám", False)]:
            t = QtWidgets.QPushButton(tab_text)
            t.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            if is_active:
                t.setStyleSheet("border: none; border-bottom: 2px solid #22c55e; color: #22c55e; font-weight: 700; font-size: 12px; padding: 6px 8px; background: transparent;")
            else:
                t.setStyleSheet("border: none; color: #94a3b8; font-size: 12px; padding: 6px 8px; background: transparent;")
            info_tabs.addWidget(t)
        info_tabs.addStretch()
        dl.addLayout(info_tabs)

        # Detail fields
        for label, val in [("Nghề nghiệp", "Nhân viên văn phòng"), ("Nhóm máu", "O+"), ("Dị ứng", "Không"), ("Số CMND/CCCD", "123456789012"), ("Bảo hiểm y tế", "Có"), ("Người liên hệ", "Nguyễn Thị Lan (Vợ)\n0988 111 222")]:
            row = QtWidgets.QHBoxLayout()
            ll = QtWidgets.QLabel(label)
            ll.setStyleSheet("font-size: 12px; color: #64748b; background: transparent;")
            ll.setFixedWidth(105)
            vl = QtWidgets.QLabel(val)
            vl.setStyleSheet("font-size: 12px; color: #1e293b; font-weight: 600; background: transparent;")
            vl.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            vl.setWordWrap(True)
            row.addWidget(ll)
            row.addStretch()
            row.addWidget(vl)
            dl.addLayout(row)

        # Notes section
        dl.addSpacing(4)
        note_title = QtWidgets.QLabel("Ghi chú")
        note_title.setStyleSheet("font-size: 13px; font-weight: 800; color: #1e293b; background: transparent;")
        dl.addWidget(note_title)
        note_box = QtWidgets.QFrame()
        note_box.setStyleSheet("background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;")
        nb_l = QtWidgets.QVBoxLayout(note_box)
        nb_l.setContentsMargins(10, 8, 10, 8)
        note_text = QtWidgets.QLabel("Bệnh nhân có tiền sử đau dạ dày.\nCần nhắc nhở kiêng đồ cay nóng.")
        note_text.setStyleSheet("font-size: 12px; color: #475569; background: transparent;")
        note_text.setWordWrap(True)
        nb_l.addWidget(note_text)
        dl.addWidget(note_box)

        # Quick actions
        dl.addSpacing(4)
        qa_title = QtWidgets.QLabel("Thao tác nhanh")
        qa_title.setStyleSheet("font-size: 13px; font-weight: 800; color: #1e293b; background: transparent;")
        dl.addWidget(qa_title)
        qa_row = QtWidgets.QHBoxLayout()
        qa_row.setSpacing(8)
        for icon, text, bg, fg in [("👁", "Xem hồ sơ", "#eff6ff", "#2563eb"), ("📅", "Tạo lịch hẹn", "#ecfdf5", "#16a34a"), ("🩺", "Khám bệnh", "#fef3c7", "#d97706")]:
            qa_btn = QtWidgets.QPushButton(f"{icon}\n{text}")
            qa_btn.setFixedSize(80, 60)
            qa_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            qa_btn.setStyleSheet(f"background: {bg}; color: {fg}; border: 1px solid #e2e8f0; border-radius: 10px; font-size: 11px; font-weight: 700;")
            qa_row.addWidget(qa_btn)
        dl.addLayout(qa_row)

        # Delete button
        del_btn = QtWidgets.QPushButton("🗑  Xóa bệnh nhân")
        del_btn.setFixedHeight(36)
        del_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        del_btn.setStyleSheet("background: white; color: #dc2626; border: 1px solid #fca5a5; border-radius: 8px; font-weight: 700; font-size: 13px;")
        dl.addWidget(del_btn)
        dl.addStretch()

        body.addWidget(detail)
        main.addLayout(body)

        scroll.setWidget(container)
        root.addWidget(scroll)

    # Stub so existing callers don't break
    def load_data(self):
        pass



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
                "padding: 8px; border-radius: 6px; border: 1px solid #dbe2ea; font-size: 13px; color: #1f2937; background: white;"
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
                "padding: 7px 8px; border-radius: 6px; border: 1px solid #dbe2ea; background: white; color: #1f2937;"
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
