from PyQt6 import QtCore, QtGui, QtWidgets
from views.admin_management_views import AdminListPage, FormDialog, _status_colors, _as_text, _format_money

class ServiceManagementPage(AdminListPage):
    page_title = "Quản lý dịch vụ"
    breadcrumb = "Dashboard / Quản lý dịch vụ"
    headers = ["☐", "STT", "Mã dịch vụ", "Tên dịch vụ", "Danh mục", "Giá dịch vụ", "Thời gian (phút)", "Trạng thái", "Thao tác"]
    column_widths = [0.35, 0.45, 1.25, 2.0, 1.5, 1.25, 1.0, 1.25, 0.95]
    search_placeholder = "Tìm kiếm dịch vụ (Tên, mã, mô tả...)"
    
    def __init__(self, user_data=None, parent=None):
        self.selected_service_ids = set()
        self.total_services = 0
        self.active_services = 0
        self.paused_services = 0
        self.discontinued_services = 0
        super().__init__(user_data, parent)

    def _add_filters(self, layout):
        self.category_filter = self._combo([
            ("Danh mục: Tất cả", "all"),
            ("Khám bệnh", "Khám bệnh"),
            ("Xét nghiệm", "Xét nghiệm"),
            ("Chẩn đoán hình ảnh", "Chẩn đoán hình ảnh"),
            ("Thăm dò chức năng", "Thăm dò chức năng"),
            ("Điều trị", "Điều trị"),
            ("Vật lý trị liệu", "Vật lý trị liệu"),
            ("Tiêm chủng", "Tiêm chủng"),
            ("Cấp cứu", "Cấp cứu"),
            ("Dịch vụ khác", "Dịch vụ khác")
        ])
        self.status_filter = self._combo([
            ("Trạng thái: Tất cả", "all"),
            ("Đang hoạt động", "1"),
            ("Tạm ngưng", "0")
        ])
        self.visibility_filter = self._combo([
            ("Hiển thị: Tất cả", "all"),
            ("Đang hiển thị", "1"),
            ("Đang ẩn", "0")
        ])
        
        layout.addWidget(self.category_filter)
        layout.addWidget(self.status_filter)
        layout.addWidget(self.visibility_filter)

    def _add_toolbar_buttons(self, layout):
        add_btn = self._button("+ Thêm dịch vụ", primary=True)
        add_btn.setFixedWidth(132)
        add_btn.clicked.connect(self.add_service)
        layout.addWidget(add_btn)
        
        export_btn = self._button("Xuất Excel")
        export_btn.setFixedWidth(106)
        export_btn.clicked.connect(self.export_excel)
        layout.addWidget(export_btn)

    def stat_cards(self):
        return [
            self._stat_card("🏥", "Tổng dịch vụ", self.total_services, "Tất cả dịch vụ", "#2563eb"),
            self._stat_card("✅", "Đang hoạt động", self.active_services, "Đang cung cấp", "#16A34A"),
            self._stat_card("⏸", "Tạm ngưng", self.paused_services, "Tạm không đặt lịch", "#F97316"),
            self._stat_card("❌", "Ngừng cung cấp", self.discontinued_services, "Không còn cung cấp", "#7E22CE"),
        ]

    def load_rows(self):
        try:
            from controllers.service_controller import ServiceController
            data = ServiceController.get_all()
            if not data:
                return []
            
            self.total_services = len(data)
            self.active_services = sum(1 for row in data if row.get("is_active"))
            self.paused_services = sum(1 for row in data if not row.get("is_active") and row.get("is_visible"))
            self.discontinued_services = sum(1 for row in data if not row.get("is_active") and not row.get("is_visible"))
            
            return data
        except Exception as e:
            print(f"Error loading services: {e}")
            return []

    def accept_row(self, row):
        cat_f = self.category_filter.currentData()
        if cat_f != "all" and str(row.get("category", "")) != cat_f:
            return False
            
        status_f = self.status_filter.currentData()
        if status_f != "all":
            is_active = str(1 if row.get("is_active") else 0)
            if is_active != status_f:
                return False
                
        vis_f = self.visibility_filter.currentData()
        if vis_f != "all":
            is_visible = str(1 if row.get("is_visible") else 0)
            if is_visible != vis_f:
                return False

        query = self.search_input.text().lower().strip()
        if query:
            match = False
            for field in ["service_code", "service_name", "description", "category"]:
                if query in str(row.get(field, "")).lower():
                    match = True
                    break
            if not match:
                return False
                
        return True

    def _get_status_badge(self, row):
        is_active = row.get("is_active")
        is_visible = row.get("is_visible")
        
        if is_active:
            return self._badge("Đang hoạt động", "success")
        elif not is_active and is_visible:
            return self._badge("Tạm ngưng", "warning")
        else:
            return self._badge("Ngừng cung cấp", "danger")

    def render_row(self, row_index, row_data):
        service_id = row_data.get("service_id")
        
        cb = QtWidgets.QCheckBox()
        cb.setStyleSheet("margin-left: 8px;")
        cb.setChecked(service_id in self.selected_service_ids)
        cb.stateChanged.connect(lambda state, sid=service_id: self._toggle_selection(sid, state))
        self.table.setCellWidget(row_index, 0, cb)
        
        self._set_item(row_index, 1, str(row_index + 1 + (self.current_page - 1) * self.page_size))
        self._set_item(row_index, 2, row_data.get("service_code", ""))
        self._set_item(row_index, 3, row_data.get("service_name", ""))
        self._set_item(row_index, 4, row_data.get("category", ""))
        self._set_item(row_index, 5, _format_money(row_data.get("price", 0)))
        self._set_item(row_index, 6, str(row_data.get("duration", 0)))
        
        self.table.setCellWidget(row_index, 7, self._get_status_badge(row_data))
        
        view_btn = self._icon_button("Xem", "info")
        edit_btn = self._icon_button("Sửa", "info")
        del_btn = self._icon_button("Xóa", "danger")
        
        view_btn.clicked.connect(lambda _, d=row_data: self.view_service(d))
        edit_btn.clicked.connect(lambda _, d=row_data: self.edit_service(d))
        del_btn.clicked.connect(lambda _, sid=service_id, name=row_data.get("service_name"): self.delete_service(sid, name))
        
        self.table.setCellWidget(row_index, 8, self._action_cell([view_btn, edit_btn, del_btn]))

    def _toggle_selection(self, service_id, state):
        if state == QtCore.Qt.CheckState.Checked.value:
            self.selected_service_ids.add(service_id)
        else:
            self.selected_service_ids.discard(service_id)

    def _get_form_fields(self):
        return [
            {"key": "code", "label": "Mã dịch vụ *", "type": "text"},
            {"key": "name", "label": "Tên dịch vụ *", "type": "text"},
            {
                "key": "category", "label": "Danh mục *", "type": "combo",
                "options": [
                    ("Khám bệnh", "Khám bệnh"),
                    ("Xét nghiệm", "Xét nghiệm"),
                    ("Chẩn đoán hình ảnh", "Chẩn đoán hình ảnh"),
                    ("Thăm dò chức năng", "Thăm dò chức năng"),
                    ("Điều trị", "Điều trị"),
                    ("Vật lý trị liệu", "Vật lý trị liệu"),
                    ("Tiêm chủng", "Tiêm chủng"),
                    ("Cấp cứu", "Cấp cứu"),
                    ("Dịch vụ khác", "Dịch vụ khác")
                ]
            },
            {"key": "price", "label": "Giá dịch vụ (VNĐ) *", "type": "money", "min": 0},
            {"key": "duration", "label": "Thời gian (phút) *", "type": "spin", "min": 1},
            {"key": "description", "label": "Mô tả", "type": "text"},
            {
                "key": "is_active", "label": "Trạng thái", "type": "combo",
                "options": [("Đang hoạt động", 1), ("Tạm ngưng", 0)],
                "default": 1
            },
            {
                "key": "is_visible", "label": "Hiển thị", "type": "combo",
                "options": [("Có", 1), ("Không", 0)],
                "default": 1
            }
        ]

    def add_service(self):
        dialog = FormDialog("Thêm dịch vụ mới", self._get_form_fields(), parent=self)
        if dialog.exec():
            data = dialog.values()
            if not data.get("code") or not data.get("name") or not data.get("category"):
                self._show_info("Lỗi", "Vui lòng nhập đầy đủ mã, tên và danh mục dịch vụ.")
                return
                
            try:
                from controllers.service_controller import ServiceController
                ServiceController.create(data)
                self.refresh()
                self._show_info("Thành công", "Đã thêm dịch vụ thành công.")
            except Exception as e:
                self._show_info("Lỗi", f"Không thể thêm dịch vụ: {e}")

    def edit_service(self, row_data):
        data = {
            "code": row_data.get("service_code", ""),
            "name": row_data.get("service_name", ""),
            "category": row_data.get("category", ""),
            "price": row_data.get("price", 0),
            "duration": row_data.get("duration", 30),
            "description": row_data.get("description", ""),
            "is_active": 1 if row_data.get("is_active") else 0,
            "is_visible": 1 if row_data.get("is_visible") else 0
        }
        
        dialog = FormDialog("Chỉnh sửa dịch vụ", self._get_form_fields(), data=data, parent=self)
        if dialog.exec():
            new_data = dialog.values()
            if not new_data.get("name") or not new_data.get("category"):
                self._show_info("Lỗi", "Vui lòng nhập đầy đủ tên và danh mục dịch vụ.")
                return
                
            try:
                from controllers.service_controller import ServiceController
                ServiceController.update(row_data.get("service_id"), new_data)
                self.refresh()
                self._show_info("Thành công", "Đã cập nhật dịch vụ thành công.")
            except Exception as e:
                self._show_info("Lỗi", f"Không thể cập nhật dịch vụ: {e}")

    def view_service(self, row_data):
        details = (
            f"Mã dịch vụ: {row_data.get('service_code')}\n"
            f"Tên: {row_data.get('service_name')}\n"
            f"Danh mục: {row_data.get('category')}\n"
            f"Giá: {_format_money(row_data.get('price'))}\n"
            f"Thời gian: {row_data.get('duration')} phút\n"
            f"Trạng thái: {'Đang hoạt động' if row_data.get('is_active') else 'Tạm ngưng/Ngừng cung cấp'}\n"
            f"Hiển thị: {'Có' if row_data.get('is_visible') else 'Không'}\n"
            f"Mô tả: {row_data.get('description')}\n"
        )
        self._show_info("Chi tiết dịch vụ", details)

    def delete_service(self, service_id, name):
        if self._confirm("Xóa dịch vụ", f"Bạn có chắc chắn muốn xóa dịch vụ '{name}' không?\nHành động này có thể ảnh hưởng đến lịch sử nếu đã được sử dụng (sẽ chuyển sang trạng thái ngừng cung cấp thay vì xóa cứng)."):
            try:
                from controllers.service_controller import ServiceController
                ServiceController.delete(service_id)
                self.refresh()
                self._show_info("Thành công", "Đã xử lý xóa/ngừng cung cấp dịch vụ thành công.")
            except Exception as e:
                self._show_info("Lỗi", f"Không thể xóa dịch vụ: {e}")

    def export_row(self, row):
        return [
            row.get("service_code") or row.get("service_id"),
            row.get("service_name"),
            row.get("category"),
            _format_money(row.get("price", 0)),
            row.get("duration"),
            "Đang hoạt động" if row.get("is_active") else "Tạm ngưng/Ngừng cung cấp",
            "Đang hiển thị" if row.get("is_visible") else "Đang ẩn"
        ]
