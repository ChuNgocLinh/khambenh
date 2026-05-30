import csv
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
        from controllers.medical_record_controller import MedicalRecordController
        records = MedicalRecordController.get_by_doctor(self.doctor_id)
        
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


class PrescriptionView(QtWidgets.QWidget):
    def __init__(self, doctor_id, parent=None):
        super().__init__(parent)
        self.doctor_id = doctor_id
        self.role = "doctor"
        self.summary_counts = {
            "total": 156,
            "pending": 8,
            "approved": 120,
            "dispensed": 20,
            "cancelled": 8,
            "revenue": "12.450.000 ₫",
        }
        self.display_rows = []
        self._init_ui()
        self.load_data()

    def _init_ui(self):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: #f7fbff; border: none;")

        container = QtWidgets.QWidget()
        container.setStyleSheet("background: #f7fbff;")
        self.layout = QtWidgets.QVBoxLayout(container)
        self.layout.setContentsMargins(28, 18, 28, 28)
        self.layout.setSpacing(16)

        self._build_header()
        self._build_filter_card()
        self._build_body()

        scroll.setWidget(container)
        root.addWidget(scroll)

    def _build_header(self):
        title = QtWidgets.QLabel("Đơn thuốc của tôi")
        title.setStyleSheet("font-size: 28px; font-weight: 800; color: #0f172a; background: transparent;")
        self.layout.addWidget(title)

        breadcrumb = QtWidgets.QLabel("Trang chủ  ›  Đơn thuốc của tôi")
        breadcrumb.setStyleSheet("font-size: 14px; color: #64748b; background: transparent; font-weight: 500;")
        self.layout.addWidget(breadcrumb)

    def _build_filter_card(self):
        card = QtWidgets.QFrame()
        card.setStyleSheet("background: white; border-radius: 20px; border: 1px solid #eef3f8;")
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 18)
        layout.setSpacing(16)

        filter_row = QtWidgets.QHBoxLayout()
        filter_row.setSpacing(12)

        search_box = QtWidgets.QFrame()
        search_box.setFixedHeight(48)
        search_box.setStyleSheet("background: white; border: 1px solid #e6edf5; border-radius: 12px;")
        search_layout = QtWidgets.QHBoxLayout(search_box)
        search_layout.setContentsMargins(14, 0, 14, 0)
        search_layout.setSpacing(10)
        search_icon = QtWidgets.QLabel("⌕")
        search_icon.setStyleSheet("font-size: 20px; color: #94a3b8; background: transparent;")
        search_layout.addWidget(search_icon)

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm theo tên bệnh nhân, mã BN, số đơn...")
        self.search_input.setStyleSheet(
            "border: none; background: transparent; color: #334155; font-size: 14px; font-weight: 500;"
        )
        search_layout.addWidget(self.search_input)
        filter_row.addWidget(search_box, 3)

        self.from_date = self._create_date_edit()
        self.to_date = self._create_date_edit()
        self.status_filter = self._create_combo_box(
            ["Tất cả trạng thái", "Chờ duyệt", "Đã duyệt", "Đã phát thuốc", "Đã hủy"]
        )
        self.type_filter = self._create_combo_box(["Tất cả loại đơn", "Đơn mới", "Đơn tái khám", "Đơn cấp phát"])
        self.patient_filter = self._create_combo_box(["Tất cả bệnh nhân"])
        self.patient_filter.hide()

        filter_row.addWidget(self._wrap_filter_field("Từ ngày", self.from_date), 1)
        filter_row.addWidget(self._wrap_filter_field("Đến ngày", self.to_date), 1)
        filter_row.addWidget(self._wrap_filter_field("", self.status_filter), 1)
        filter_row.addWidget(self._wrap_filter_field("", self.type_filter), 1)

        create_btn = QtWidgets.QPushButton("+  Tạo đơn thuốc")
        create_btn.setFixedHeight(48)
        create_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        create_btn.setStyleSheet(
            "QPushButton { background: #17b56f; color: white; border: none; border-radius: 12px; "
            "padding: 0 22px; font-size: 14px; font-weight: 700; }"
            "QPushButton:hover { background: #12a361; }"
        )
        filter_row.addWidget(create_btn)
        layout.addLayout(filter_row)

        tab_row = QtWidgets.QHBoxLayout()
        tab_row.setSpacing(10)
        for label, active in [
            ("Tất cả (156)", True),
            ("Chờ duyệt (8)", False),
            ("Đã duyệt (120)", False),
            ("Đã phát thuốc (20)", False),
            ("Đã hủy (8)", False),
        ]:
            tab_btn = QtWidgets.QPushButton(label)
            tab_btn.setFixedHeight(40)
            tab_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            if active:
                tab_btn.setStyleSheet(
                    "QPushButton { background: #e8f7ef; color: #17b56f; border: none; border-radius: 12px; "
                    "padding: 0 18px; font-size: 14px; font-weight: 700; }"
                )
            else:
                tab_btn.setStyleSheet(
                    "QPushButton { background: white; color: #64748b; border: 1px solid #eef3f8; border-radius: 12px; "
                    "padding: 0 18px; font-size: 14px; font-weight: 600; }"
                )
            tab_row.addWidget(tab_btn)
        tab_row.addStretch()
        layout.addLayout(tab_row)

        self.layout.addWidget(card)

    def _build_body(self):
        body = QtWidgets.QHBoxLayout()
        body.setSpacing(18)

        left_card = QtWidgets.QFrame()
        left_card.setStyleSheet("background: white; border-radius: 20px; border: 1px solid #eef3f8;")
        left_layout = QtWidgets.QVBoxLayout(left_card)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["STT", "Số đơn thuốc", "Bệnh nhân", "Ngày kê đơn", "Chẩn đoán", "Tổng tiền", "Trạng thái", "Thao tác"]
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setStyleSheet(
            "QTableWidget { border: none; background: white; color: #334155; font-size: 13px; }"
            "QHeaderView::section { background: white; color: #0f172a; font-weight: 800; font-size: 13px; "
            "border: none; border-bottom: 1px solid #eef3f8; padding: 16px 10px; }"
            "QTableWidget::item { border-bottom: 1px solid #f3f6fa; padding: 8px 10px; }"
        )
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 54)
        self.table.setColumnWidth(1, 136)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(5, 120)
        self.table.setColumnWidth(6, 132)
        self.table.setColumnWidth(7, 128)
        left_layout.addWidget(self.table)
        left_layout.addWidget(self._build_pagination())
        body.addWidget(left_card, 7)

        right_panel = QtWidgets.QWidget()
        right_panel.setFixedWidth(330)
        right_panel.setStyleSheet("background: transparent;")
        right_layout = QtWidgets.QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(16)
        right_layout.addWidget(self._build_overview_card())
        right_layout.addWidget(self._build_quick_actions_card())
        right_layout.addStretch()
        body.addWidget(right_panel, 3)

        self.layout.addLayout(body)

    def _build_pagination(self):
        wrapper = QtWidgets.QWidget()
        wrapper.setStyleSheet("background: white; border-top: 1px solid #f3f6fa;")
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(10)

        show_label = QtWidgets.QLabel("Hiển thị")
        show_label.setStyleSheet("font-size: 13px; color: #475569; background: transparent;")
        layout.addWidget(show_label)

        per_page = self._create_combo_box(["10"])
        per_page.setFixedWidth(64)
        per_page.setFixedHeight(38)
        layout.addWidget(per_page)

        records_label = QtWidgets.QLabel("bản ghi")
        records_label.setStyleSheet("font-size: 13px; color: #475569; background: transparent;")
        layout.addWidget(records_label)
        layout.addStretch()

        layout.addWidget(self._create_page_button("‹"))
        for page_text, active in [("1", True), ("2", False), ("3", False), ("4", False), ("5", False), ("...", False), ("16", False)]:
            layout.addWidget(self._create_page_button(page_text, active))
        layout.addWidget(self._create_page_button("›"))
        return wrapper

    def _build_overview_card(self):
        card = QtWidgets.QFrame()
        card.setStyleSheet("background: white; border-radius: 20px; border: 1px solid #eef3f8;")
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(18)

        title = QtWidgets.QLabel("Tổng quan")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #0f172a; background: transparent;")
        layout.addWidget(title)

        for icon_text, color, label_text, value_text in [
            ("◫", "#94a3b8", "Tổng số đơn thuốc", str(self.summary_counts["total"])),
            ("◌", "#f59e0b", "Chờ duyệt", str(self.summary_counts["pending"])),
            ("○", "#34d399", "Đã duyệt", str(self.summary_counts["approved"])),
            ("◎", "#60a5fa", "Đã phát thuốc", str(self.summary_counts["dispensed"])),
            ("✕", "#fb7185", "Đã hủy", str(self.summary_counts["cancelled"])),
        ]:
            row = QtWidgets.QHBoxLayout()
            row.setSpacing(10)
            icon = QtWidgets.QLabel(icon_text)
            icon.setFixedWidth(16)
            icon.setStyleSheet(f"font-size: 14px; color: {color}; font-weight: 700; background: transparent;")
            row.addWidget(icon)
            label = QtWidgets.QLabel(label_text)
            label.setStyleSheet("font-size: 14px; color: #64748b; background: transparent;")
            row.addWidget(label)
            row.addStretch()
            value = QtWidgets.QLabel(value_text)
            value.setStyleSheet("font-size: 14px; color: #0f172a; font-weight: 800; background: transparent;")
            row.addWidget(value)
            layout.addLayout(row)

        divider = QtWidgets.QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background: #f3f6fa; border: none;")
        layout.addWidget(divider)

        revenue_row = QtWidgets.QHBoxLayout()
        revenue_label = QtWidgets.QLabel("Tổng doanh thu")
        revenue_label.setStyleSheet("font-size: 15px; color: #0f172a; font-weight: 800; background: transparent;")
        revenue_value = QtWidgets.QLabel(self.summary_counts["revenue"])
        revenue_value.setStyleSheet("font-size: 16px; color: #17b56f; font-weight: 900; background: transparent;")
        revenue_row.addWidget(revenue_label)
        revenue_row.addStretch()
        revenue_row.addWidget(revenue_value)
        layout.addLayout(revenue_row)

        return card

    def _build_quick_actions_card(self):
        card = QtWidgets.QFrame()
        card.setStyleSheet("background: white; border-radius: 20px; border: 1px solid #eef3f8;")
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(14)

        title = QtWidgets.QLabel("Thao tác nhanh")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #0f172a; background: transparent;")
        layout.addWidget(title)

        create_btn = QtWidgets.QPushButton("+  Tạo đơn thuốc mới")
        create_btn.setFixedHeight(48)
        create_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        create_btn.setStyleSheet(
            "QPushButton { background: white; color: #17b56f; border: 1px solid #e6edf5; border-radius: 12px; "
            "font-size: 14px; font-weight: 700; }"
            "QPushButton:hover { background: #f8fffb; }"
        )
        layout.addWidget(create_btn)

        for label_text, badge_text, badge_color, badge_bg in [
            ("Đơn thuốc chờ duyệt", "8", "#f59e0b", "#fff4df"),
            ("Đơn thuốc hôm nay", "12", "#fb923c", "#fff1e7"),
            ("In đơn hàng loạt", "", "#64748b", "transparent"),
            ("Xuất excel", "", "#17b56f", "transparent"),
        ]:
            button = QtWidgets.QPushButton(label_text)
            button.setFixedHeight(48)
            button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            button.setStyleSheet(
                "QPushButton { background: white; color: #334155; border: 1px solid #e6edf5; border-radius: 12px; "
                "font-size: 14px; font-weight: 600; text-align: left; padding: 0 16px; }"
                "QPushButton:hover { background: #fafcff; }"
            )
            if badge_text:
                badge = QtWidgets.QLabel(badge_text, button)
                badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                badge.setGeometry(250, 12, 30, 24)
                badge.setStyleSheet(
                    f"background: {badge_bg}; color: {badge_color}; border-radius: 12px; font-size: 12px; font-weight: 800;"
                )
            layout.addWidget(button)

        return card

    def _create_date_edit(self):
        widget = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        widget.setCalendarPopup(True)
        widget.setDisplayFormat("dd/MM/yyyy")
        widget.setFixedHeight(48)
        widget.setStyleSheet(
            "QDateEdit { padding: 0 14px; border: 1px solid #e6edf5; border-radius: 12px; background: white; "
            "color: #64748b; font-size: 14px; font-weight: 600; }"
            "QDateEdit::drop-down { subcontrol-origin: padding; subcontrol-position: top right; width: 26px; border: none; }"
        )
        return widget

    def _create_combo_box(self, items):
        widget = QtWidgets.QComboBox()
        widget.addItems(items)
        widget.setFixedHeight(48)
        widget.setStyleSheet(
            "QComboBox { padding: 0 14px; border: 1px solid #e6edf5; border-radius: 12px; background: white; "
            "color: #334155; font-size: 14px; font-weight: 600; }"
            "QComboBox::drop-down { border: none; width: 26px; }"
            "QComboBox QAbstractItemView { border: 1px solid #e6edf5; background: white; color: #334155; }"
        )
        return widget

    def _wrap_filter_field(self, title, widget):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        if title:
            label = QtWidgets.QLabel(title)
            label.setStyleSheet("font-size: 12px; color: #94a3b8; font-weight: 700; background: transparent;")
            layout.addWidget(label)
        else:
            spacer = QtWidgets.QLabel("")
            spacer.setFixedHeight(18)
            spacer.setStyleSheet("background: transparent; border: none;")
            layout.addWidget(spacer)
        layout.addWidget(widget)
        return wrapper

    def _create_page_button(self, text, active=False):
        button = QtWidgets.QPushButton(text)
        button.setFixedSize(38, 38)
        if active:
            button.setStyleSheet(
                "QPushButton { background: #17b56f; color: white; border: none; border-radius: 10px; font-size: 13px; font-weight: 800; }"
            )
        else:
            button.setStyleSheet(
                "QPushButton { background: white; color: #334155; border: 1px solid #e6edf5; border-radius: 10px; "
                "font-size: 13px; font-weight: 700; }"
            )
        return button

    def load_data(self):
        self.display_rows = self._build_mock_rows()
        self._render_table()

    def _render_table(self):
        self.table.setRowCount(len(self.display_rows))
        for row_idx, row in enumerate(self.display_rows):
            stt_item = QtWidgets.QTableWidgetItem(str(row.get("stt", row_idx + 1)))
            stt_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            stt_item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            stt_item.setForeground(QtGui.QBrush(QtGui.QColor("#0f172a")))
            self.table.setItem(row_idx, 0, stt_item)

            code_item = QtWidgets.QTableWidgetItem(str(row.get("prescription_code", "")))
            code_item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            code_item.setForeground(QtGui.QBrush(QtGui.QColor("#466391")))
            self.table.setItem(row_idx, 1, code_item)

            self.table.setCellWidget(row_idx, 2, self._build_patient_cell(row))

            date_item = QtWidgets.QTableWidgetItem(str(row.get("date_text", "")))
            date_item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            date_item.setForeground(QtGui.QBrush(QtGui.QColor("#334155")))
            self.table.setItem(row_idx, 3, date_item)

            diagnosis_item = QtWidgets.QTableWidgetItem(str(row.get("diagnosis", "")))
            diagnosis_item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            diagnosis_item.setForeground(QtGui.QBrush(QtGui.QColor("#334155")))
            self.table.setItem(row_idx, 4, diagnosis_item)

            amount_item = QtWidgets.QTableWidgetItem(str(row.get("total_amount", "")))
            amount_item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            amount_item.setForeground(QtGui.QBrush(QtGui.QColor("#17b56f")))
            self.table.setItem(row_idx, 5, amount_item)

            self.table.setCellWidget(row_idx, 6, self._build_status_badge(row))
            self.table.setCellWidget(row_idx, 7, self._build_action_buttons(row))
            self.table.setRowHeight(row_idx, 78)

    def _build_patient_cell(self, row):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(6, 8, 6, 8)
        layout.setSpacing(10)

        avatar = QtWidgets.QLabel(row.get("avatar_text", "👤"))
        avatar.setFixedSize(36, 36)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            f"background: {row.get('avatar_bg', '#e0f2fe')}; color: {row.get('avatar_color', '#1d4ed8')}; "
            "border-radius: 18px; font-size: 18px;"
        )
        layout.addWidget(avatar)

        info = QtWidgets.QVBoxLayout()
        info.setContentsMargins(0, 0, 0, 0)
        info.setSpacing(2)
        name_label = QtWidgets.QLabel(row.get("patient_name", ""))
        name_label.setStyleSheet("font-size: 14px; font-weight: 700; color: #1e293b; background: transparent;")
        meta_label = QtWidgets.QLabel(f"{row.get('age_text', '')}  ·  {row.get('gender_text', '')}")
        meta_label.setStyleSheet("font-size: 13px; color: #64748b; background: transparent; font-weight: 500;")
        info.addWidget(name_label)
        info.addWidget(meta_label)
        layout.addLayout(info)
        layout.addStretch()
        return wrapper

    def _build_status_badge(self, row):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        badge = QtWidgets.QLabel(row.get("status_label", ""))
        badge.setStyleSheet(
            f"background: {row.get('status_bg', '#eef2ff')}; color: {row.get('status_color', '#475569')}; "
            "border-radius: 12px; padding: 5px 12px; font-size: 12px; font-weight: 800;"
        )
        layout.addWidget(badge)
        return wrapper

    def _build_action_buttons(self, row):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        for text, callback in [
            ("👁", lambda checked=False, r=row: self._view_prescription(r)),
            ("🖨", lambda checked=False, r=row: self._print_prescription(r)),
            ("⋮", None),
        ]:
            btn = QtWidgets.QPushButton(text)
            btn.setFixedSize(32, 32)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(
                "QPushButton { background: white; color: #5b8def; border: 1px solid #e6edf5; border-radius: 10px; "
                "font-size: 14px; font-weight: 700; }"
                "QPushButton:hover { background: #f8fbff; }"
            )
            if callback is not None:
                btn.clicked.connect(callback)
            layout.addWidget(btn)
        return wrapper

    def _build_mock_rows(self):
        return [
            self._mock_row(1, "RX250523-001", "Nguyễn Văn Nam", 35, "Nam", "23/05/2026 09:30", "R51 - Đau đầu", "125.000 ₫", "Đã duyệt", "#e8f7ef", "#17b56f", "👨", "#e5f1ff", "#3483fa"),
            self._mock_row(2, "RX250523-002", "Trần Thị Mai", 32, "Nữ", "23/05/2026 10:15", "J20 - Viêm phế quản cấp", "85.000 ₫", "Đã phát thuốc", "#edf5ff", "#4a8dff", "👩", "#ffe8f0", "#ff5a9a"),
            self._mock_row(3, "RX250523-003", "Lê Văn Nam", 51, "Nam", "23/05/2026 11:00", "I10 - Tăng huyết áp", "90.000 ₫", "Đã phát thuốc", "#edf5ff", "#4a8dff", "👨", "#e5f1ff", "#3483fa"),
            self._mock_row(4, "RX250522-045", "Phạm Thị Lan", 28, "Nữ", "22/05/2026 15:30", "J01 - Viêm xoang cấp", "105.000 ₫", "Đã duyệt", "#e8f7ef", "#17b56f", "👩", "#ffe8f0", "#ff5a9a"),
            self._mock_row(5, "RX250522-044", "Hoàng Anh Tuấn", 45, "Nam", "22/05/2026 14:20", "K29 - Viêm dạ dày", "130.000 ₫", "Chờ duyệt", "#fff4df", "#f59e0b", "👨", "#e5f1ff", "#3483fa"),
            self._mock_row(6, "RX250521-038", "Vũ Thị Hương", 30, "Nữ", "21/05/2026 10:45", "R05 - Ho", "65.000 ₫", "Đã phát thuốc", "#edf5ff", "#4a8dff", "👩", "#ffe8f0", "#ff5a9a"),
            self._mock_row(7, "RX250521-037", "Đỗ Minh Quân", 26, "Nam", "21/05/2026 09:20", "A09 - Tiêu chảy cấp", "58.000 ₫", "Đã hủy", "#ffe9ea", "#ff5a67", "👨", "#e5f1ff", "#3483fa"),
            self._mock_row(8, "RX250520-031", "Nguyễn Thị Hoa", 55, "Nữ", "20/05/2026 16:10", "E78 - Rối loạn mỡ máu", "110.000 ₫", "Đã duyệt", "#e8f7ef", "#17b56f", "👩", "#ffe8f0", "#ff5a9a"),
            self._mock_row(9, "RX250520-030", "Bùi Văn Dũng", 40, "Nam", "20/05/2026 14:50", "M54 - Đau lưng", "75.000 ₫", "Chờ duyệt", "#fff4df", "#f59e0b", "👨", "#e8f7ef", "#17b56f"),
            self._mock_row(10, "RX250519-025", "Trương Thị Kiều", 33, "Nữ", "19/05/2026 11:25", "N39 - Nhiễm trùng đường tiểu", "88.000 ₫", "Đã phát thuốc", "#edf5ff", "#4a8dff", "👩", "#ffe8f0", "#ff5a9a"),
        ]

    def _mock_row(
        self,
        stt,
        code,
        patient_name,
        age,
        gender,
        date_text,
        diagnosis,
        total_amount,
        status_label,
        status_bg,
        status_color,
        avatar_text,
        avatar_bg,
        avatar_color,
    ):
        return {
            "stt": stt,
            "record_id": stt,
            "prescription_code": code,
            "patient_name": patient_name,
            "patient_gender": gender,
            "patient_dob": None,
            "age_text": f"{age} tuổi",
            "gender_text": gender,
            "date_text": date_text,
            "created_at": date_text,
            "diagnosis": diagnosis,
            "treatment": "Uống thuốc đúng liều, tái khám nếu triệu chứng kéo dài.",
            "total_amount": total_amount,
            "status_label": status_label,
            "status_bg": status_bg,
            "status_color": status_color,
            "appointment_note": "Khám theo lịch hẹn định kỳ.",
            "avatar_text": avatar_text,
            "avatar_bg": avatar_bg,
            "avatar_color": avatar_color,
            "items": [
                {"medicine_name": "Paracetamol 500mg", "quantity": 10, "medicine_description": "Giảm đau, hạ sốt"},
                {"medicine_name": "Vitamin C", "quantity": 20, "medicine_description": "Tăng cường đề kháng"},
            ],
        }

    @staticmethod
    def _parse_datetime(value):
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            for fmt in ("%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
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

    def _view_prescription(self, row):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(f"Chi tiết {row.get('prescription_code', '')}")
        dialog.resize(760, 520)

        layout = QtWidgets.QVBoxLayout(dialog)

        title = QtWidgets.QLabel(f"{row.get('prescription_code', '')} • Đơn thuốc bệnh nhân")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #1e293b;")
        layout.addWidget(title)

        summary = QtWidgets.QLabel(
            f"{row.get('patient_name', '')} • {row.get('age_text', self._calculate_age_text(row.get('patient_dob')) + ' tuổi')} • "
            f"{row.get('patient_gender', 'N/A')} • {row.get('date_text', self._format_datetime(row.get('created_at'), '%d/%m/%Y %H:%M'))}"
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
        <p><strong>Thời điểm kê:</strong> {row.get('date_text', self._format_datetime(row.get('created_at'), '%d/%m/%Y %H:%M'))}</p>
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
        self._mock_patients = []

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
            ("Tất cả (0)", True),
            ("Bệnh nhân mới (0)", False),
            ("Đang điều trị (0)", False),
            ("Tái khám (0)", False),
            ("Khám gần đây (0)", False),
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
        body.setSpacing(12)

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
        p_name = QtWidgets.QLabel("Chưa chọn bệnh nhân")
        p_name.setStyleSheet("font-size: 15px; font-weight: 800; color: #1e293b; background: transparent;")
        p_gender_badge = QtWidgets.QLabel("Nam")
        p_gender_badge.setStyleSheet("background: #dbeafe; color: #2563eb; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 8px;")
        p_name_row.addWidget(p_name)
        p_name_row.addWidget(p_gender_badge)
        p_name_row.addStretch()
        pinfo.addLayout(p_name_row)

        for lbl in ["Mã BN: -", "Tuổi / DOB: -", "SĐT: -", "Địa chỉ: -"]:
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
            role="doctor",
            user_context={"doctor_id": self.doctor_id},
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
            role="doctor",
            user_context={"doctor_id": self.doctor_id},
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


class DoctorPatientListView(QtWidgets.QWidget):
    def __init__(self, doctor_id, parent=None):
        super().__init__(parent)
        self.doctor_id = doctor_id
        self.role = "doctor"
        self.page_size = 10
        self.current_page = 1
        self.all_rows = []
        self.filtered_rows = []
        self.selected_patient_id = None

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QtWidgets.QLabel("Danh sách bệnh nhân")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #1e293b;")
        layout.addWidget(title)

        filters = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Tìm theo tên, SĐT, mã BN...")
        self.gender_filter = QtWidgets.QComboBox()
        self.gender_filter.addItems(["Tất cả giới tính", "Nam", "Nữ"])
        self.status_label = QtWidgets.QLabel("")
        for widget in [self.search_input, self.gender_filter]:
            widget.setMinimumHeight(38)
            widget.setStyleSheet("background: white; color: #1f2937; border: 1px solid #dbe4ee; border-radius: 8px; padding: 6px;")
            filters.addWidget(widget)
        filters.addWidget(self.status_label)
        layout.addLayout(filters)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Mã BN", "Họ tên", "Giới tính", "Ngày sinh", "SĐT", "Thao tác"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.cellDoubleClicked.connect(lambda row, _col: self.open_patient_profile(row))
        layout.addWidget(self.table, 1)

        pagination = QtWidgets.QHBoxLayout()
        self.prev_btn = QtWidgets.QPushButton("<")
        self.next_btn = QtWidgets.QPushButton(">")
        self.page_label = QtWidgets.QLabel("1/1")
        self.prev_btn.clicked.connect(lambda: self._go_page(self.current_page - 1))
        self.next_btn.clicked.connect(lambda: self._go_page(self.current_page + 1))
        pagination.addStretch()
        pagination.addWidget(self.prev_btn)
        pagination.addWidget(self.page_label)
        pagination.addWidget(self.next_btn)
        pagination.addStretch()
        layout.addLayout(pagination)

        self.search_input.textChanged.connect(self._apply_filters)
        self.gender_filter.currentIndexChanged.connect(self._apply_filters)
        self.load_data()

    def load_data(self):
        try:
            rows = PatientController.get_all() or []
        except Exception as exc:
            self.all_rows = []
            self.status_label.setText(f"Lỗi tải dữ liệu: {exc}")
            self._apply_filters()
            return
        self.all_rows = [dict(row) for row in rows]
        self.status_label.setText("")
        self._apply_filters()

    def _matches(self, row):
        keyword = self.search_input.text().strip().lower()
        if keyword:
            haystack = f"BN{int(row.get('patient_id') or 0):06d} {row.get('name', '')} {row.get('phone', '')}".lower()
            if keyword not in haystack:
                return False

        gender = self.gender_filter.currentText()
        if gender != "Tất cả giới tính" and str(row.get("gender") or "") != gender:
            return False
        return True

    def _apply_filters(self):
        self.filtered_rows = [row for row in self.all_rows if self._matches(row)]
        self.current_page = 1
        self._render_page()

    def _render_page(self):
        total_pages = max(1, (len(self.filtered_rows) + self.page_size - 1) // self.page_size)
        self.current_page = max(1, min(self.current_page, total_pages))
        start = (self.current_page - 1) * self.page_size
        page_rows = self.filtered_rows[start : start + self.page_size]
        self.table.setRowCount(len(page_rows))

        for row_index, row in enumerate(page_rows):
            patient_id = row.get("patient_id")
            values = [
                f"BN{int(patient_id or 0):06d}",
                row.get("name", ""),
                row.get("gender", ""),
                row.get("dob", ""),
                row.get("phone", ""),
            ]
            for col, value in enumerate(values):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setData(QtCore.Qt.ItemDataRole.UserRole, patient_id)
                self.table.setItem(row_index, col, item)

            button = QtWidgets.QPushButton("Xem hồ sơ")
            button.clicked.connect(lambda checked=False, r=row_index: self.open_patient_profile(r))
            self.table.setCellWidget(row_index, 5, button)

        self.page_label.setText(f"{self.current_page}/{total_pages}")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)
        if not page_rows:
            self.status_label.setText("Không có bệnh nhân phù hợp.")

    def _go_page(self, page):
        self.current_page = page
        self._render_page()

    def open_patient_profile(self, row_index):
        item = self.table.item(row_index, 0)
        if not item:
            return
        self.selected_patient_id = item.data(QtCore.Qt.ItemDataRole.UserRole)
        dashboard = self._find_dashboard()
        if dashboard:
            profile = getattr(dashboard, "page_patient_record", None)
            if hasattr(profile, "set_patient"):
                profile.set_patient(self.selected_patient_id)
            dashboard.switch_page(4)

    def _find_dashboard(self):
        parent = self.parent()
        while parent and not hasattr(parent, "content_stack"):
            parent = parent.parent()
        return parent


class PrescriptionView(QtWidgets.QWidget):
    def __init__(self, doctor_id, parent=None):
        super().__init__(parent)
        self.doctor_id = doctor_id
        self.role = "doctor"
        self.all_rows = []
        self.filtered_rows = []
        self.last_message = ""

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QtWidgets.QLabel("Đơn thuốc của tôi")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0f172a;")
        layout.addWidget(title)

        filters = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Tìm theo bệnh nhân, thuốc, chẩn đoán...")
        self.status_filter = QtWidgets.QComboBox()
        self.status_filter.addItems(["Tất cả trạng thái", "draft", "issued", "dispensed", "cancelled"])
        self.message_label = QtWidgets.QLabel("")
        for widget in [self.search_input, self.status_filter]:
            widget.setMinimumHeight(38)
            filters.addWidget(widget)
        filters.addWidget(self.message_label)
        layout.addLayout(filters)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Mã đơn", "Bệnh nhân", "Ngày kê", "Chẩn đoán", "Thuốc", "SL", "Trạng thái", "Thao tác"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table, 1)

        self.search_input.textChanged.connect(self._apply_filters)
        self.status_filter.currentIndexChanged.connect(self._apply_filters)
        self.load_data()

    def load_data(self):
        try:
            self.all_rows = [dict(row) for row in (PrescriptionController.get_by_doctor(self.doctor_id) or [])]
            self.message_label.setText("")
        except Exception as exc:
            self.all_rows = []
            self.message_label.setText(f"Lỗi tải đơn thuốc: {exc}")
        self._apply_filters()

    def _matches(self, row):
        keyword = self.search_input.text().strip().lower()
        if keyword:
            haystack = (
                f"{row.get('patient_name', '')} {row.get('medicine_name', '')} "
                f"{row.get('name', '')} {row.get('diagnosis', '')}"
            ).lower()
            if keyword not in haystack:
                return False
        selected_status = self.status_filter.currentText()
        if selected_status != "Tất cả trạng thái" and str(row.get("status") or "draft") != selected_status:
            return False
        return True

    def _apply_filters(self):
        self.filtered_rows = [row for row in self.all_rows if self._matches(row)]
        self._render_table()

    def _render_table(self):
        self.table.setRowCount(len(self.filtered_rows))
        for index, row in enumerate(self.filtered_rows):
            values = [
                row.get("prescription_id", ""),
                row.get("patient_name", ""),
                row.get("prescribed_at", ""),
                row.get("diagnosis", ""),
                row.get("medicine_name") or row.get("name", ""),
                row.get("quantity", ""),
                row.get("status", "draft"),
            ]
            for col, value in enumerate(values):
                self.table.setItem(index, col, QtWidgets.QTableWidgetItem(str(value)))

            actions = QtWidgets.QWidget()
            action_layout = QtWidgets.QHBoxLayout(actions)
            action_layout.setContentsMargins(0, 0, 0, 0)
            edit_btn = QtWidgets.QPushButton("Sửa")
            cancel_btn = QtWidgets.QPushButton("Hủy")
            edit_btn.clicked.connect(lambda checked=False, r=row: self.edit_prescription(r))
            cancel_btn.clicked.connect(lambda checked=False, r=row: self.cancel_prescription(r))
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(cancel_btn)
            self.table.setCellWidget(index, 7, actions)

        if not self.filtered_rows:
            self.message_label.setText("Không có đơn thuốc phù hợp.")

    def edit_prescription(self, row):
        if not PrescriptionController.can_edit(row.get("status")):
            self._set_message("Không thể sửa đơn thuốc đã phát.")
            return {"status": False, "message": self.last_message}
        self._set_message("Đơn thuốc có thể chỉnh sửa.")
        return {"status": True, "message": self.last_message}

    def cancel_prescription(self, row):
        result = PrescriptionController.cancel(row.get("prescription_id"))
        self._set_message(result.get("message", ""))
        if result.get("status"):
            row["status"] = "cancelled"
            self._apply_filters()
        return result

    def _set_message(self, message):
        self.last_message = message
        self.message_label.setText(message)


# Modern doctor patient list used by DashboardView. It intentionally appears
# after the legacy classes above so existing imports resolve to this version.
from views.doctor_ui_utils import (
    PAGE_BG,
    age_from_dob,
    avatar,
    badge,
    button,
    card,
    icon_button,
    input_style,
    page_title,
    table_style,
)


class DoctorPatientListView(QtWidgets.QWidget):
    STATUS_META = {
        "new": ("Bệnh nhân mới", "#7A5AF8", "#F4F3FF"),
        "active": ("Đang điều trị", "#2E90FA", "#EFF8FF"),
        "follow_up": ("Tái khám", "#12B76A", "#ECFDF3"),
        "recent": ("Khám gần đây", "#F79009", "#FFF7ED"),
    }

    def __init__(self, doctor_id, parent=None):
        super().__init__(parent)
        self.doctor_id = doctor_id
        self.role = "doctor"
        self.page_size = 8
        self.current_page = 1
        self.all_rows = []
        self.filtered_rows = []
        self.selected_patient_id = None
        self.active_tab = "all"

        self.setStyleSheet(f"background: {PAGE_BG};")
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(8)
        root.addWidget(page_title("Danh sách bệnh nhân", "Trang chủ  >  Danh sách bệnh nhân"))
        root.addWidget(self._build_filter_card())

        body = QtWidgets.QHBoxLayout()
        body.setSpacing(10)
        body.addWidget(self._build_table_card(), 8)
        body.addWidget(self._build_detail_card(), 2)
        root.addLayout(body, 1)

        self.search_input.textChanged.connect(self._apply_filters)
        self.gender_filter.currentIndexChanged.connect(self._apply_filters)
        self.age_filter.currentIndexChanged.connect(self._apply_filters)
        self.status_filter.currentIndexChanged.connect(self._apply_filters)
        self.load_data()

    def _build_filter_card(self):
        wrapper = card()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        search_row = QtWidgets.QHBoxLayout()
        search_row.setSpacing(8)
        filter_row = QtWidgets.QHBoxLayout()
        filter_row.setSpacing(8)
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Tìm theo tên, SĐT, mã BN...")
        self.gender_filter = QtWidgets.QComboBox()
        self.gender_filter.addItems(["Tất cả giới tính", "Nam", "Nữ"])
        self.age_filter = QtWidgets.QComboBox()
        self.age_filter.addItems(["Tất cả độ tuổi", "Dưới 18", "18-40", "Trên 40"])
        self.status_filter = QtWidgets.QComboBox()
        self.status_filter.addItems(["Tất cả trạng thái", "Bệnh nhân mới", "Đang điều trị", "Tái khám", "Khám gần đây"])
        for widget in [self.search_input, self.gender_filter, self.age_filter, self.status_filter]:
            widget.setMinimumHeight(34)
            widget.setStyleSheet(input_style())
        search_row.addWidget(self.search_input, 1)
        for widget in [self.gender_filter, self.age_filter, self.status_filter]:
            filter_row.addWidget(widget, 1)
        add_btn = button("+ Thêm bệnh nhân")
        add_btn.clicked.connect(self.add_patient)
        export_btn = button("Xuất danh sách", "outline")
        export_btn.clicked.connect(self.export_patients)
        search_row.addWidget(export_btn)
        search_row.addWidget(add_btn)
        layout.addLayout(search_row)
        layout.addLayout(filter_row)

        self.tab_row = QtWidgets.QHBoxLayout()
        self.tab_row.setSpacing(8)
        layout.addLayout(self.tab_row)
        return wrapper

    def _build_table_card(self):
        wrapper = card()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(
            ["STT", "Mã BN", "Họ và tên", "Giới tính", "Ngày sinh", "SĐT", "Lần khám", "Trạng thái", "Thao tác"]
        )
        self.table.setStyleSheet(table_style())
        self.table.setShowGrid(False)
        self.table.setWordWrap(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self._configure_patient_table_columns()
        self.table.cellClicked.connect(lambda row, _col: self._select_patient_row(row))
        self.table.cellDoubleClicked.connect(lambda row, _col: self.open_patient_profile(row))
        layout.addWidget(self.table, 1)

        footer = QtWidgets.QHBoxLayout()
        footer.setContentsMargins(12, 8, 12, 8)
        self.status_label = QtWidgets.QLabel("")
        self.status_label.setStyleSheet("color: #667085; font-size: 13px;")
        self.prev_btn = icon_button("<")
        self.next_btn = icon_button(">")
        self.page_label = QtWidgets.QLabel("1/1")
        self.page_label.setStyleSheet("color: #344054; font-weight: 800;")
        self.prev_btn.clicked.connect(lambda: self._go_page(self.current_page - 1))
        self.next_btn.clicked.connect(lambda: self._go_page(self.current_page + 1))
        footer.addWidget(self.status_label)
        footer.addStretch()
        footer.addWidget(QtWidgets.QLabel("Hiển thị 8 bản ghi"))
        footer.addWidget(self.prev_btn)
        footer.addWidget(self.page_label)
        footer.addWidget(self.next_btn)
        layout.addLayout(footer)
        return wrapper

    def _configure_patient_table_columns(self):
        header = self.table.horizontalHeader()
        header.setMinimumSectionSize(34)
        for col in range(self.table.columnCount()):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        column_widths = {
            0: 38,
            1: 78,
            3: 50,
            4: 80,
            5: 88,
            6: 78,
            7: 100,
            8: 104,
        }
        for col, width in column_widths.items():
            self.table.setColumnWidth(col, width)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def _build_detail_card(self):
        wrapper = card()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)
        title = QtWidgets.QLabel("Thông tin bệnh nhân")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #101828;")
        layout.addWidget(title)
        self.detail_header = QtWidgets.QWidget()
        self.detail_header_layout = QtWidgets.QVBoxLayout(self.detail_header)
        self.detail_header_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.detail_header)
        self.detail_info = QtWidgets.QLabel("Chọn một bệnh nhân trong danh sách để xem chi tiết.")
        self.detail_info.setWordWrap(True)
        self.detail_info.setStyleSheet("color: #475467; font-size: 13px; line-height: 150%;")
        layout.addWidget(self.detail_info)
        for text, cb, kind in [
            ("Xem hồ sơ", lambda: self.open_patient_profile_by_id(self.selected_patient_id), "primary"),
            ("Tạo lịch hẹn", self._go_schedule, "outline"),
            ("Khám bệnh", lambda: self._switch_page(3), "outline"),
            ("Xóa bệnh nhân", self.delete_selected_patient, "danger"),
        ]:
            btn = button(text, kind)
            btn.clicked.connect(cb)
            layout.addWidget(btn)
        layout.addStretch()
        return wrapper

    def load_data(self):
        try:
            rows = PatientController.get_by_doctor(self.doctor_id) or []
        except Exception as exc:
            self.all_rows = []
            self.status_label.setText(f"Lỗi tải dữ liệu: {exc}")
            self._apply_filters()
            return
        self.all_rows = [self._decorate_patient(dict(row), idx) for idx, row in enumerate(rows)]
        self.status_label.setText("")
        self._render_tabs()
        self._apply_filters()

    def _decorate_patient(self, row, index):
        row["status_key"] = self._derive_status_key(row)
        row["patient_code"] = row.get("patient_code") or f"BN{int(row.get('patient_id') or 0):06d}"
        row["last_visit"] = self._display_datetime(
            row.get("last_visit") or row.get("last_record_at") or row.get("latest_appointment_at")
        )
        return row

    def _derive_status_key(self, row):
        if int(row.get("active_appointment_count") or 0) > 0 or int(row.get("draft_record_count") or 0) > 0:
            return "active"
        if row.get("next_visit"):
            return "follow_up"
        if int(row.get("record_count") or 0) == 0 and int(row.get("appointment_count") or 0) <= 1:
            return "new"
        last_seen = self._parse_datetime(row.get("last_visit") or row.get("last_record_at") or row.get("latest_appointment_at"))
        if last_seen and (datetime.now() - last_seen).days <= 30:
            return "recent"
        return "active"

    @staticmethod
    def _parse_datetime(value):
        if isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime(value.year, value.month, value.day)
        if isinstance(value, str):
            raw = value.strip()
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%d/%m/%Y %H:%M", "%d/%m/%Y"):
                try:
                    return datetime.strptime(raw, fmt)
                except ValueError:
                    continue
        return None

    def _display_datetime(self, value):
        parsed = self._parse_datetime(value)
        if parsed:
            return parsed.strftime("%d/%m/%Y")
        return str(value or "Chưa có")

    @staticmethod
    def _normalize_gender(value):
        text = str(value or "").strip().lower()
        if text in {"nam", "male", "m"}:
            return "Nam"
        if text in {"nữ", "nu", "female", "f"}:
            return "Nữ"
        return str(value or "")

    def _render_tabs(self):
        while self.tab_row.count():
            item = self.tab_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        tabs = [("all", f"Tất cả ({len(self.all_rows)})")]
        for key, (label, _, _) in self.STATUS_META.items():
            count = len([row for row in self.all_rows if row.get("status_key") == key])
            tabs.append((key, f"{label} ({count})"))
        for key, text in tabs:
            btn = QtWidgets.QPushButton(text)
            btn.setMinimumHeight(34)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            active = key == self.active_tab
            btn.setStyleSheet(
                "QPushButton { "
                + ("background: #ECFDF3; color: #16B364; border: none;" if active else "background: white; color: #667085; border: 1px solid #EAECF0;")
                + " border-radius: 10px; padding: 0 10px; font-weight: 800; }"
            )
            btn.clicked.connect(lambda checked=False, tab=key: self._set_tab(tab))
            self.tab_row.addWidget(btn)
        self.tab_row.addStretch()

    def _set_tab(self, tab):
        self.active_tab = tab
        self._render_tabs()
        self._apply_filters()

    def _matches(self, row):
        keyword = self.search_input.text().strip().lower()
        if keyword:
            haystack = " ".join(
                str(row.get(key) or "")
                for key in ("patient_code", "patient_id", "name", "phone", "cccd", "email")
            ).lower()
            if keyword not in haystack:
                return False
        gender = self.gender_filter.currentText()
        if gender != "Tất cả giới tính" and self._normalize_gender(row.get("gender")) != gender:
            return False
        if self.active_tab != "all" and row.get("status_key") != self.active_tab:
            return False
        status_text = self.status_filter.currentText()
        label = self.STATUS_META.get(row.get("status_key"), self.STATUS_META["new"])[0]
        if status_text != "Tất cả trạng thái" and label != status_text:
            return False
        age_text = age_from_dob(row.get("dob"))
        age = int(age_text.split()[0]) if age_text else None
        age_filter = self.age_filter.currentText()
        if age is not None:
            if age_filter == "Dưới 18" and age >= 18:
                return False
            if age_filter == "18-40" and not (18 <= age <= 40):
                return False
            if age_filter == "Trên 40" and age <= 40:
                return False
        return True

    def _apply_filters(self):
        self.filtered_rows = [row for row in self.all_rows if self._matches(row)]
        self.current_page = 1
        self._render_page()

    def _render_page(self):
        total_pages = max(1, (len(self.filtered_rows) + self.page_size - 1) // self.page_size)
        self.current_page = max(1, min(self.current_page, total_pages))
        start = (self.current_page - 1) * self.page_size
        page_rows = self.filtered_rows[start : start + self.page_size]
        self.table.setRowCount(len(page_rows))
        for row_index, row in enumerate(page_rows):
            patient_id = row.get("patient_id")
            status_label, status_color, status_bg = self.STATUS_META.get(row.get("status_key"), self.STATUS_META["new"])
            values = [
                start + row_index + 1,
                row.get("patient_code") or f"BN{int(patient_id or 0):06d}",
                "",
                self._normalize_gender(row.get("gender")),
                row.get("dob", ""),
                row.get("phone", ""),
                row.get("last_visit", ""),
                "",
            ]
            for col, value in enumerate(values):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setData(QtCore.Qt.ItemDataRole.UserRole, patient_id)
                self.table.setItem(row_index, col, item)
            self.table.setCellWidget(row_index, 2, self._patient_name_cell(row))
            self.table.setCellWidget(row_index, 7, badge(status_label, status_color, status_bg))
            self.table.setCellWidget(row_index, 8, self._patient_actions(row))
            self.table.setRowHeight(row_index, 56)
        self.page_label.setText(f"{self.current_page}/{total_pages}")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)
        self.status_label.setText("Không có bệnh nhân phù hợp." if not page_rows else f"{len(self.filtered_rows)} bệnh nhân")
        if page_rows and self.selected_patient_id is None:
            self._select_patient(page_rows[0])

    def _patient_name_cell(self, row):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)
        layout.addWidget(avatar(row.get("name"), 34))
        info = QtWidgets.QVBoxLayout()
        info.setSpacing(0)
        name = QtWidgets.QLabel(str(row.get("name", "")))
        name.setWordWrap(True)
        name.setToolTip(str(row.get("name", "")))
        name.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        name.setStyleSheet("font-weight: 800; color: #101828;")
        meta = QtWidgets.QLabel(age_from_dob(row.get("dob")) or f"BN{int(row.get('patient_id') or 0):06d}")
        meta.setToolTip(meta.text())
        meta.setStyleSheet("color: #667085; font-size: 12px;")
        info.addWidget(name)
        info.addWidget(meta)
        layout.addLayout(info)
        return wrapper

    def _patient_actions(self, row):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        for text, cb in [
            ("Xem", lambda checked=False, r=row: self.open_patient_profile_by_id(r.get("patient_id"))),
            ("Sửa", lambda checked=False, r=row: self.edit_patient(r)),
            ("...", lambda checked=False, r=row: self.show_patient_menu(r)),
        ]:
            btn = icon_button(text)
            btn.clicked.connect(cb)
            layout.addWidget(btn)
        return wrapper

    def _select_patient_row(self, row_index):
        if row_index < 0:
            return
        item = self.table.item(row_index, 0)
        if not item:
            return
        patient_id = item.data(QtCore.Qt.ItemDataRole.UserRole)
        row = next((p for p in self.filtered_rows if p.get("patient_id") == patient_id), None)
        if row:
            self._select_patient(row)

    def _select_patient(self, row):
        self.selected_patient_id = row.get("patient_id")
        while self.detail_header_layout.count():
            item = self.detail_header_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        head = QtWidgets.QHBoxLayout()
        head.addWidget(avatar(row.get("name"), 50))
        text = QtWidgets.QVBoxLayout()
        name = QtWidgets.QLabel(str(row.get("name", "")))
        name.setWordWrap(True)
        name.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        name.setStyleSheet("font-size: 18px; font-weight: 900; color: #101828;")
        code = QtWidgets.QLabel(row.get("patient_code") or f"BN{int(row.get('patient_id') or 0):06d}")
        code.setStyleSheet("color: #667085;")
        text.addWidget(name)
        text.addWidget(code)
        head.addLayout(text)
        self.detail_header_layout.addLayout(head)
        self.detail_info.setText(
            f"Giới tính: {self._normalize_gender(row.get('gender')) or 'Chưa cập nhật'}\n"
            f"Ngày sinh: {row.get('dob', 'Chưa cập nhật')} ({age_from_dob(row.get('dob')) or 'Chưa rõ tuổi'})\n"
            f"SĐT: {row.get('phone', 'Chưa cập nhật')}\n"
            f"CCCD: {row.get('cccd') or 'Chưa cập nhật'}\n"
            f"Nghề nghiệp: {row.get('occupation') or 'Chưa cập nhật'}\n"
            f"Địa chỉ: {row.get('address') or 'Chưa cập nhật'}\n"
            f"Lần khám gần nhất: {row.get('last_visit') or 'Chưa có'}\n"
            f"Số lần khám: {int(row.get('appointment_count') or 0)} lịch hẹn, {int(row.get('record_count') or 0)} hồ sơ\n"
            f"Ghi chú: {row.get('intake_notes') or 'Chưa cập nhật'}"
        )

    def _go_page(self, page):
        self.current_page = page
        self._render_page()

    def open_patient_profile(self, row_index):
        item = self.table.item(row_index, 0)
        if not item:
            return
        self.open_patient_profile_by_id(item.data(QtCore.Qt.ItemDataRole.UserRole))

    def open_patient_profile_by_id(self, patient_id):
        if not patient_id:
            return
        self.selected_patient_id = patient_id
        dashboard = self._find_dashboard()
        if dashboard:
            if hasattr(dashboard, "open_patient_record"):
                dashboard.open_patient_record(patient_id)
                return
            profile = getattr(dashboard, "page_patient_record", None)
            if hasattr(profile, "set_patient"):
                profile.set_patient(patient_id)
            dashboard.switch_page(4)

    def add_patient(self):
        dialog = PatientCreateDialog(self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            result = PatientController.create_with_status(dialog.get_data())
            if not result.get("status"):
                QtWidgets.QMessageBox.warning(self, "Không thể thêm bệnh nhân", result.get("message", "Lỗi không xác định"))
                return
            QtWidgets.QMessageBox.information(self, "Thành công", result.get("message", "Đã thêm bệnh nhân."))
            self.load_data()

    def edit_patient(self, row):
        if not row:
            return
        dialog = PatientEditDialog(row, self)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        result = PatientController.update_with_status(row.get("patient_id"), dialog.get_data())
        if not result.get("status"):
            QtWidgets.QMessageBox.warning(self, "Không thể cập nhật", result.get("message", "Lỗi không xác định"))
            return
        QtWidgets.QMessageBox.information(self, "Thành công", result.get("message", "Đã cập nhật bệnh nhân."))
        self.load_data()

    def delete_selected_patient(self):
        row = next((p for p in self.all_rows if p.get("patient_id") == self.selected_patient_id), None)
        self.delete_patient(row)

    def delete_patient(self, row):
        if not row:
            QtWidgets.QMessageBox.warning(self, "Thiếu dữ liệu", "Vui lòng chọn bệnh nhân cần xóa.")
            return
        patient_id = row.get("patient_id")
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Ngưng hoạt động bệnh nhân",
            f"Bạn có chắc muốn ngưng hoạt động bệnh nhân {row.get('name') or patient_id}?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No,
        )
        if confirm != QtWidgets.QMessageBox.StandardButton.Yes:
            return
        if not PatientController.delete(patient_id):
            QtWidgets.QMessageBox.warning(
                self,
                "Không thể cập nhật",
                "Không thể cập nhật trạng thái bệnh nhân này.",
            )
            return
        self.selected_patient_id = None
        QtWidgets.QMessageBox.information(self, "Hoàn tất", "Đã ngưng hoạt động bệnh nhân.")
        self.load_data()

    def show_patient_menu(self, row):
        menu = QtWidgets.QMenu(self)
        menu.addAction("Xem hồ sơ", lambda: self.open_patient_profile_by_id(row.get("patient_id")))
        menu.addAction("Tạo lịch hẹn", self._go_schedule)
        menu.addAction("Sửa thông tin", lambda: self.edit_patient(row))
        menu.addSeparator()
        menu.addAction("Xóa bệnh nhân", lambda: self.delete_patient(row))
        menu.exec(QtGui.QCursor.pos())

    def export_patients(self):
        if not self.filtered_rows:
            QtWidgets.QMessageBox.information(self, "Xuất danh sách", "Không có bệnh nhân để xuất.")
            return
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Xuất danh sách bệnh nhân",
            "danh_sach_benh_nhan.csv",
            "CSV Files (*.csv)",
        )
        if not path:
            return
        headers = ["Mã BN", "Họ và tên", "Giới tính", "Ngày sinh", "SĐT", "CCCD", "Lần khám gần nhất", "Trạng thái"]
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as handle:
                writer = csv.writer(handle)
                writer.writerow(headers)
                for row in self.filtered_rows:
                    status_label = self.STATUS_META.get(row.get("status_key"), self.STATUS_META["new"])[0]
                    writer.writerow(
                        [
                            row.get("patient_code"),
                            row.get("name"),
                            self._normalize_gender(row.get("gender")),
                            row.get("dob"),
                            row.get("phone"),
                            row.get("cccd"),
                            row.get("last_visit"),
                            status_label,
                        ]
                    )
        except Exception as exc:
            QtWidgets.QMessageBox.warning(self, "Không thể xuất", str(exc))
            return
        QtWidgets.QMessageBox.information(self, "Xuất danh sách", f"Đã xuất {len(self.filtered_rows)} bệnh nhân.")

    def _go_schedule(self):
        self._switch_page(1)

    def _switch_page(self, index):
        dashboard = self._find_dashboard()
        if dashboard:
            dashboard.switch_page(index)

    def _find_dashboard(self):
        parent = self.parent()
        while parent and not hasattr(parent, "content_stack"):
            parent = parent.parent()
        return parent


class PrescriptionView(QtWidgets.QWidget):
    STATUS_META = {
        "draft": ("Chờ duyệt", "#F79009", "#FFF7ED"),
        "pending": ("Chờ duyệt", "#F79009", "#FFF7ED"),
        "issued": ("Đã duyệt", "#12B76A", "#ECFDF3"),
        "approved": ("Đã duyệt", "#12B76A", "#ECFDF3"),
        "dispensed": ("Đã phát thuốc", "#2E90FA", "#EFF8FF"),
        "cancelled": ("Đã hủy", "#F04438", "#FEF3F2"),
    }

    def __init__(self, doctor_id, parent=None):
        super().__init__(parent)
        self.doctor_id = doctor_id
        self.role = "doctor"
        self.page_size = 8
        self.current_page = 1
        self.all_rows = []
        self.filtered_rows = []
        self.active_tab = "all"
        self.context_record_id = None
        self.last_message = ""
        self.setStyleSheet(f"background: {PAGE_BG};")

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(8)
        root.addWidget(page_title("Đơn thuốc của tôi", "Trang chủ  >  Đơn thuốc của tôi"))
        root.addWidget(self._build_filter_card())
        body = QtWidgets.QHBoxLayout()
        body.setSpacing(10)
        body.addWidget(self._build_table_card(), 8)
        body.addWidget(self._build_summary_sidebar(), 2)
        root.addLayout(body, 1)

        self.search_input.textChanged.connect(self._apply_filters)
        self.status_filter.currentIndexChanged.connect(self._apply_filters)
        self.type_filter.currentIndexChanged.connect(self._apply_filters)
        self.from_date.dateChanged.connect(self._apply_filters)
        self.to_date.dateChanged.connect(self._apply_filters)
        self.load_data()

    def _build_filter_card(self):
        wrapper = card()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)
        search_row = QtWidgets.QHBoxLayout()
        search_row.setSpacing(8)
        filter_row = QtWidgets.QHBoxLayout()
        filter_row.setSpacing(8)
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm theo tên bệnh nhân, mã BN, số đơn...")
        self.from_date = QtWidgets.QDateEdit(QtCore.QDate.currentDate().addMonths(-1))
        self.to_date = QtWidgets.QDateEdit(QtCore.QDate.currentDate().addMonths(1))
        for date_widget in [self.from_date, self.to_date]:
            date_widget.setCalendarPopup(True)
            date_widget.setDisplayFormat("dd/MM/yyyy")
        self.status_filter = QtWidgets.QComboBox()
        self.status_filter.addItems(["Tất cả trạng thái", "Chờ duyệt", "Đã duyệt", "Đã phát thuốc", "Đã hủy"])
        self.type_filter = QtWidgets.QComboBox()
        self.type_filter.addItems(["Tất cả loại đơn", "Đơn mới", "Đơn tái khám", "Đơn cấp phát"])
        for widget in [self.search_input, self.from_date, self.to_date, self.status_filter, self.type_filter]:
            widget.setMinimumHeight(34)
            widget.setStyleSheet(input_style())
        search_row.addWidget(self.search_input, 1)
        for widget in [self.from_date, self.to_date, self.status_filter, self.type_filter]:
            filter_row.addWidget(widget, 1)
        self.create_prescription_btn = button("+ Tạo đơn thuốc")
        self.create_prescription_btn.clicked.connect(self.create_prescription)
        search_row.addWidget(self.create_prescription_btn)
        layout.addLayout(search_row)
        layout.addLayout(filter_row)
        self.tab_row = QtWidgets.QHBoxLayout()
        self.tab_row.setSpacing(8)
        layout.addLayout(self.tab_row)
        return wrapper

    def _build_table_card(self):
        wrapper = card()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["STT", "Số đơn", "Bệnh nhân", "Ngày kê", "Chẩn đoán", "Tổng tiền", "Trạng thái", "Thao tác"])
        self.table.setStyleSheet(table_style())
        self.table.setShowGrid(False)
        self.table.setWordWrap(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self._configure_prescription_table_columns()
        layout.addWidget(self.table, 1)
        footer = QtWidgets.QHBoxLayout()
        footer.setContentsMargins(12, 8, 12, 8)
        self.message_label = QtWidgets.QLabel("")
        self.message_label.setStyleSheet("color: #667085; font-size: 13px;")
        self.prev_btn = icon_button("<")
        self.next_btn = icon_button(">")
        self.page_label = QtWidgets.QLabel("1/1")
        self.prev_btn.clicked.connect(lambda: self._go_page(self.current_page - 1))
        self.next_btn.clicked.connect(lambda: self._go_page(self.current_page + 1))
        footer.addWidget(self.message_label)
        footer.addStretch()
        footer.addWidget(QtWidgets.QLabel("Hiển thị 8 bản ghi"))
        footer.addWidget(self.prev_btn)
        footer.addWidget(self.page_label)
        footer.addWidget(self.next_btn)
        layout.addLayout(footer)
        return wrapper

    def _configure_prescription_table_columns(self):
        header = self.table.horizontalHeader()
        header.setMinimumSectionSize(34)
        for col in range(self.table.columnCount()):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        column_widths = {
            0: 38,
            1: 90,
            3: 84,
            4: 106,
            5: 76,
            6: 104,
            7: 104,
        }
        for col, width in column_widths.items():
            self.table.setColumnWidth(col, width)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def _build_summary_sidebar(self):
        wrapper = card()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)
        title = QtWidgets.QLabel("Tổng quan")
        title.setStyleSheet("font-size: 18px; font-weight: 900; color: #101828;")
        layout.addWidget(title)
        self.summary_box = QtWidgets.QVBoxLayout()
        layout.addLayout(self.summary_box)
        layout.addSpacing(4)
        quick = QtWidgets.QLabel("Thao tác nhanh")
        quick.setStyleSheet("font-size: 16px; font-weight: 800; color: #101828;")
        layout.addWidget(quick)
        quick_actions = [
            ("Tạo đơn thuốc mới", self.create_prescription),
            ("Đơn thuốc chờ duyệt", lambda: self._activate_quick_filter("draft")),
            ("Đơn thuốc hôm nay", self._show_today_prescriptions),
            ("In đơn hàng loạt", self._show_bulk_print_message),
            ("Xuất excel", self._export_prescriptions),
        ]
        for text, callback in quick_actions:
            btn = button(text, "outline")
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        layout.addStretch()
        return wrapper

    def load_data(self):
        try:
            self.all_rows = [self._decorate_row(dict(row), idx) for idx, row in enumerate(PrescriptionController.get_by_doctor(self.doctor_id) or [])]
            self.message_label.setText("")
        except Exception as exc:
            self.all_rows = []
            self.message_label.setText(f"Lỗi tải đơn thuốc: {exc}")
        self._render_tabs()
        self._apply_filters()

    def _decorate_row(self, row, index):
        row.setdefault("prescription_id", row.get("id") or index + 1)
        row.setdefault("patient_name", row.get("name") or row.get("patient") or "")
        row.setdefault("prescribed_at", row.get("created_at") or row.get("date") or "")
        row.setdefault("total_amount", row.get("total_amount") or "Chưa tính")
        row.setdefault("type", ["Đơn mới", "Đơn tái khám", "Đơn cấp phát"][index % 3])
        return row

    def _render_tabs(self):
        if not hasattr(self, "tab_row"):
            return
        while self.tab_row.count():
            item = self.tab_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        tabs = [("all", f"Tất cả ({len(self.all_rows)})")]
        for key in ["draft", "issued", "dispensed", "cancelled"]:
            label = self.STATUS_META[key][0]
            count = len([row for row in self.all_rows if self._status_key(row) == key])
            tabs.append((key, f"{label} ({count})"))
        for key, text in tabs:
            btn = QtWidgets.QPushButton(text)
            btn.setMinimumHeight(34)
            active = key == self.active_tab
            btn.setStyleSheet(
                "QPushButton { "
                + ("background: #ECFDF3; color: #16B364; border: none;" if active else "background: white; color: #667085; border: 1px solid #EAECF0;")
                + " border-radius: 10px; padding: 0 10px; font-weight: 800; }"
            )
            btn.clicked.connect(lambda checked=False, tab=key: self._set_tab(tab))
            self.tab_row.addWidget(btn)
        self.tab_row.addStretch()

    def _set_tab(self, tab):
        self.active_tab = tab
        self._render_tabs()
        self._apply_filters()

    def _status_key(self, row):
        raw = str(row.get("status") or "draft").lower()
        if raw == "pending":
            return "draft"
        if raw == "approved":
            return "issued"
        return raw if raw in self.STATUS_META else "draft"

    @staticmethod
    def _display_prescription_date(value):
        if isinstance(value, datetime):
            return value.strftime("%d/%m/%Y")
        text = str(value or "").strip()
        for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                return datetime.strptime(text, fmt).strftime("%d/%m/%Y")
            except ValueError:
                continue
        return text[:10] if len(text) > 10 else text

    def _matches(self, row):
        keyword = self.search_input.text().strip().lower()
        if keyword:
            haystack = f"{row.get('prescription_id', '')} {row.get('patient_name', '')} {row.get('medicine_name', '')} {row.get('name', '')} {row.get('diagnosis', '')}".lower()
            if keyword not in haystack:
                return False
        prescribed_at = str(row.get("prescribed_at") or "")
        prescribed_dt = None
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                prescribed_dt = datetime.strptime(prescribed_at, fmt)
                break
            except ValueError:
                continue
        if prescribed_dt is not None:
            from_date = self.from_date.date().toPyDate()
            to_date = self.to_date.date().toPyDate()
            if prescribed_dt.date() < from_date or prescribed_dt.date() > to_date:
                return False
        status_key = self._status_key(row)
        if self.active_tab != "all" and status_key != self.active_tab:
            return False
        selected_status = self.status_filter.currentText()
        status_label = self.STATUS_META[status_key][0]
        if selected_status != "Tất cả trạng thái" and status_label != selected_status:
            return False
        selected_type = self.type_filter.currentText()
        if selected_type != "Tất cả loại đơn" and row.get("type") != selected_type:
            return False
        return True

    def _apply_filters(self):
        self.filtered_rows = [row for row in self.all_rows if self._matches(row)]
        self.current_page = 1
        self._render_table()
        self._update_summary()

    def _render_table(self):
        total_pages = max(1, (len(self.filtered_rows) + self.page_size - 1) // self.page_size)
        self.current_page = max(1, min(self.current_page, total_pages))
        start = (self.current_page - 1) * self.page_size
        page_rows = self.filtered_rows[start : start + self.page_size]
        self.table.setRowCount(len(page_rows))
        for index, row in enumerate(page_rows):
            status_key = self._status_key(row)
            label, color, bg = self.STATUS_META[status_key]
            values = [
                start + index + 1,
                f"RX{int(row.get('prescription_id') or 0):06d}",
                "",
                self._display_prescription_date(row.get("prescribed_at", "")),
                row.get("diagnosis", ""),
                row.get("total_amount", "Chưa tính"),
                "",
            ]
            for col, value in enumerate(values):
                self.table.setItem(index, col, QtWidgets.QTableWidgetItem(str(value)))
            self.table.setCellWidget(index, 2, self._patient_cell(row))
            self.table.setCellWidget(index, 6, badge(label, color, bg))
            self.table.setCellWidget(index, 7, self._prescription_actions(row))
            self.table.setRowHeight(index, 56)
        self.page_label.setText(f"{self.current_page}/{total_pages}")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)
        if not self.filtered_rows:
            self.message_label.setText("Không có đơn thuốc phù hợp.")
        elif not self.last_message:
            self.message_label.setText(f"{len(self.filtered_rows)} đơn thuốc")

    def _patient_cell(self, row):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)
        layout.addWidget(avatar(row.get("patient_name"), 34))
        info = QtWidgets.QVBoxLayout()
        info.setSpacing(0)
        name = QtWidgets.QLabel(str(row.get("patient_name", "")))
        name.setWordWrap(True)
        name.setToolTip(str(row.get("patient_name", "")))
        name.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        name.setStyleSheet("font-weight: 800; color: #101828;")
        meta = QtWidgets.QLabel(str(row.get("medicine_name") or row.get("name") or ""))
        meta.setWordWrap(True)
        meta.setToolTip(meta.text())
        meta.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        meta.setStyleSheet("color: #667085; font-size: 12px;")
        info.addWidget(name)
        info.addWidget(meta)
        layout.addLayout(info)
        return wrapper

    def _prescription_actions(self, row):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        for text, cb in [
            ("Xem", lambda checked=False, r=row: self.view_prescription(r)),
            ("Sua", lambda checked=False, r=row: self.edit_prescription(r)),
            ("Huy", lambda checked=False, r=row: self.cancel_prescription(r)),
        ]:
            btn = icon_button(text)
            btn.clicked.connect(cb)
            layout.addWidget(btn)
        return wrapper

    def _update_summary(self):
        while self.summary_box.count():
            item = self.summary_box.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        rows = self.all_rows
        metrics = [
            ("Tổng số đơn", len(rows)),
            ("Chờ duyệt", len([r for r in rows if self._status_key(r) == "draft"])),
            ("Đã duyệt", len([r for r in rows if self._status_key(r) == "issued"])),
            ("Đã phát thuốc", len([r for r in rows if self._status_key(r) == "dispensed"])),
            ("Đã hủy", len([r for r in rows if self._status_key(r) == "cancelled"])),
            ("Tổng doanh thu", "Chưa tính"),
        ]
        for label_text, value in metrics:
            row = QtWidgets.QHBoxLayout()
            label_widget = QtWidgets.QLabel(label_text)
            value_widget = QtWidgets.QLabel(str(value))
            value_widget.setStyleSheet("font-weight: 900; color: #101828;")
            row.addWidget(label_widget)
            row.addStretch()
            row.addWidget(value_widget)
            holder = QtWidgets.QWidget()
            holder.setLayout(row)
            self.summary_box.addWidget(holder)

    def _go_page(self, page):
        self.current_page = page
        self._render_table()

    def edit_prescription(self, row):
        if not PrescriptionController.can_edit(row.get("status")):
            self._set_message("Không thể sửa đơn thuốc đã phát.")
            return {"status": False, "message": self.last_message}
        self._set_message("Đơn thuốc có thể chỉnh sửa.")
        return {"status": True, "message": self.last_message}

    def view_prescription(self, row):
        summary = (
            f"Bệnh nhân: {row.get('patient_name', 'Chưa cập nhật')}\n"
            f"Ngày kê: {row.get('prescribed_at', 'Chưa cập nhật')}\n"
            f"Chẩn đoán: {row.get('diagnosis', 'Chưa cập nhật')}\n"
            f"Thuốc: {row.get('medicine_name', 'Chưa cập nhật')}\n"
            f"Số lượng: {row.get('quantity', 'Chưa cập nhật')}"
        )
        QtWidgets.QMessageBox.information(self, "Chi tiết đơn thuốc", summary)
        return {"status": True, "message": "Đã mở chi tiết đơn thuốc."}

    def cancel_prescription(self, row):
        result = PrescriptionController.cancel(row.get("prescription_id"))
        self._set_message(result.get("message", ""))
        if result.get("status"):
            row["status"] = "cancelled"
            self._apply_filters()
            self._render_tabs()
        return result

    def _set_message(self, message):
        self.last_message = message
        self.message_label.setText(message)

    def create_prescription(self):
        if not self.context_record_id:
            self._set_message("Mở màn khám bệnh để tạo đơn thuốc mới từ hồ sơ khám.")
            dashboard = self._find_dashboard()
            if dashboard:
                dashboard.switch_page(3)
            return {"status": True, "message": self.last_message}

        dialog = PrescriptionDialog(self.context_record_id, self)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            self._set_message("Đã hủy tạo đơn thuốc.")
            return {"status": False, "message": self.last_message}

        data = dialog.get_data()
        created = PrescriptionController.add(data["record_id"], data["medicine_id"], data["quantity"])
        if not created:
            self._set_message("Không thể lưu đơn thuốc vào CSDL.")
            return {"status": False, "message": self.last_message}
        self._set_message(f"Đã tạo đơn thuốc cho hồ sơ #{data['record_id']}.")
        self.load_data()
        return {"status": True, "message": self.last_message}

    def set_record(self, record_id, patient_id=None):
        self.context_record_id = record_id
        self._set_message(f"Sẵn sàng kê đơn cho hồ sơ #{record_id}.")
        if patient_id:
            self.search_input.setText("")
        return {"status": True, "message": self.last_message}

    def _activate_quick_filter(self, tab):
        self.active_tab = tab
        self._render_tabs()
        self._apply_filters()
        self._set_message("Đã lọc nhanh danh sách đơn thuốc.")

    def _show_today_prescriptions(self):
        today = QtCore.QDate.currentDate()
        self.from_date.setDate(today)
        self.to_date.setDate(today)
        self._apply_filters()
        self._set_message("Đã lọc các đơn thuốc trong hôm nay.")

    def _show_bulk_print_message(self):
        self._set_message("Tính năng in hàng loạt sẽ dùng dữ liệu hiện có trong danh sách đơn thuốc.")

    def _export_prescriptions(self):
        if not self.filtered_rows:
            self._set_message("Không có đơn thuốc để xuất.")
            return {"status": False, "message": self.last_message}

        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Xuất đơn thuốc",
            "danh_sach_don_thuoc.csv",
            "CSV Files (*.csv)",
        )
        if not path:
            self._set_message("Đã hủy xuất đơn thuốc.")
            return {"status": False, "message": self.last_message}

        headers = ["Số đơn", "Bệnh nhân", "Ngày kê", "Chẩn đoán", "Thuốc", "Số lượng", "Trạng thái"]
        with open(path, "w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.writer(handle)
            writer.writerow(headers)
            for row in self.filtered_rows:
                status_key = self._status_key(row)
                writer.writerow(
                    [
                        row.get("prescription_id"),
                        row.get("patient_name"),
                        row.get("prescribed_at"),
                        row.get("diagnosis"),
                        row.get("medicine_name"),
                        row.get("quantity"),
                        self.STATUS_META[status_key][0],
                    ]
                )
        self._set_message(f"Đã xuất {len(self.filtered_rows)} đơn thuốc.")
        return {"status": True, "message": self.last_message}

    def _find_dashboard(self):
        parent = self.parent()
        while parent and not hasattr(parent, "content_stack"):
            parent = parent.parent()
        return parent
