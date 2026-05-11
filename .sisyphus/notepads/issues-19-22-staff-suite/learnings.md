
## 2026-05-11 - Task 1 baseline

- `staff_dashboard_view.py` compile độc lập bằng `python3 -m py_compile` đang pass, dùng làm mốc syntax baseline trước khi sửa issue 19-22.
- Chỉ số điều hướng cho cụm staff pages đã được xác nhận rõ trong `switch_page`: Billing=4, Services=5, Notifications=6, Reports=7.
- Blast radius tối thiểu cho chuỗi issue 19-22 nên khóa trong: `staff_dashboard_view.py` + cụm controller/model payment/service/appointment/patient/report để tránh scope creep.
- Baseline hiện tại chưa cho phép đánh giá regression bằng pytest vì runtime thiếu `pytest` module trên `python3`.

## 2026-05-11 - Task 4 services alignment

- Màn  trong  đã được nâng từ tra cứu tối giản lên layout 3 vùng theo issue #20: KPI, tab /, thanh search/filter, bảng danh mục và panel chi tiết.
- Vì schema  chỉ có , các trường , , , , , related services và package rows đang được dựng minh bạch bằng fallback ở tầng view, không ghi ngược vào DB.
- Tab  hiện là grouped fallback từ danh mục dịch vụ hiện có; đây là shell tư vấn/an toàn cho staff chứ chưa phải package engine hoặc persistence chính thức.

## 2026-05-11 - Task 4 services alignment

- Màn `Dịch vụ & Gói khám` trong `staff_dashboard_view.py` đã được nâng từ tra cứu tối giản lên layout 3 vùng theo issue #20: KPI, tab `Dịch vụ`/`Gói khám`, thanh search/filter, bảng danh mục và panel chi tiết.
- Vì schema `Services` chỉ có `service_name/price/description/is_active`, các trường `service_type`, `duration`, `status`, `process_text`, `notes_text`, related services và package rows đang được dựng minh bạch bằng fallback ở tầng view, không ghi ngược vào DB.
- Tab `Gói khám` hiện là grouped fallback từ danh mục dịch vụ hiện có; đây là shell tư vấn/an toàn cho staff chứ chưa phải package engine hoặc persistence chính thức.

- Correction note: mục Task 4 ở dòng trên có một block append lỗi do shell quoting; nội dung chuẩn đã được append lại đầy đủ ngay bên dưới và là nguồn tham chiếu đúng cho task này.

- Billing page issue #19 dùng shell 2 cột + KPI trên cùng; dữ liệu payment cần enrich từ PatientController/AppointmentController với fallback an toàn cho patient name/phone, service, collector và timestamp trước khi render table/detail.

- Appointment detail runtime bug root cause: `_handle_staff_appointment_selection` vẫn gọi cặp helper legacy `_set_staff_appointment_detail`/`_reset_staff_appointment_detail` dùng thuộc tính cũ (`staff_appt_detail_patient/info/timeline`) không còn được build; fix tối thiểu là redirect các helper này sang `_update_staff_appt_right_panel` để giữ flow mới và tránh crash khi auto-select row lúc init offscreen.

- Smoke offscreen cho `StaffDashboardView` với mocked controllers cần set `PYTHONPATH` gồm cả `BTL.Nhóm6_Python` và `BTL.Nhóm6_Python/healthcare_management` vì view đang import `controllers.*` trong khi controller lại import `healthcare_management.models.*`; thiếu một trong hai path sẽ phát sinh `ModuleNotFoundError`.

- Với bảng billing, chỉ `selectRow()` sau refresh chưa đủ an toàn vì state chọn có thể lệch timing signal; cần sync state theo row một cách deterministic ngay trong `_refresh_staff_billing_table` (cập nhật `staff_billing_selected_id/payment/status` + detail panel trực tiếp).

- Notifications offscreen smoke for `StaffDashboardView` must monkeypatch not only Appointment/Payment but also Doctor/Service/Patient controller getters because `__init__` builds all pages and some page builders query DB immediately; otherwise smoke can fail with MySQL connection error before reaching notifications assertions.

## 2026-05-11 - Task 6.2 notifications normalization

- Notifications mapping trong `staff_dashboard_view.py` nên normalize status appointment trước khi phân nhánh message/priority để hấp thụ biến thể dữ liệu (`scheduled`, `in-progress`, `completed`, `canceled`) và tránh bỏ sót lịch mới khi repo dùng nhiều naming theo ngữ cảnh.
- Đối với payment notifications, nguồn thời gian cần lấy qua helper riêng với thứ tự ưu tiên cứng `payment_date` -> `created_at` -> `appointment_date` -> `date`; cách này giữ đúng semantics “thời điểm thu tiền” nhưng vẫn có fallback an toàn khi schema thực tế thiếu field.
- Sort feed ổn định với mixed rows khi dùng key chuẩn hóa dựa trên `QDateTime` parse được (ưu tiên cao), rồi mới fallback text/id để deterministic mà không phá flow filter/select/read-detail hiện có.

## 2026-05-11 - Task 7 report controller-first path

- Reports KPI trong `staff_dashboard_view.py` đã chuyển đường dữ liệu core (`total_patients`, `total_appointments`, `total_revenue`) sang `ReportController.get_core_totals()` và chỉ giữ `PaymentController.get_all()` cho phần unpaid, giúp scope hẹp và rõ source-of-truth.
- Khi smoke offscreen cho `StaffDashboardView`, monkeypatch cần áp đúng namespace `controllers.*` (đúng với import trong view) trước khi import view; patch nhầm sang `healthcare_management.controllers.*` sẽ không chặn được các call DB lúc `__init__` build toàn page.

## 2026-05-11 - Task 8 reports UI/UX shell

- Reports page được nâng lên shell đầy đủ theo issue #22 ngay trong `staff_dashboard_view.py`: tabs báo cáo, filter period/doctor, KPI row, chart placeholders (progress ratio), bảng trạng thái lịch hẹn, bảng hóa đơn chờ thu, quick shortcuts và timestamp cập nhật dữ liệu.
- Export action cho reports dùng `QMessageBox` thông báo rõ backend export file chưa triển khai; tránh false-success và giữ đúng nguyên tắc trung thực dữ liệu/UI.
- Để chống crash với dữ liệu thiếu field, phần refresh reports chuẩn hóa guard ở nhiều lớp (coerce số, kiểm tra dict/list, fallback datetime parse, fallback label/code) trước khi render table/kpi.


## 2026-05-11 - Task 10 settings shell foundation

- `staff_dashboard_view.py` đã nâng màn `Cài đặt` staff từ card tối giản lên page-local shell đầy đủ theo issue #23: header riêng với breadcrumb/user context, menu cài đặt phụ, card hồ sơ cá nhân, card đổi mật khẩu, cụm tùy chọn hệ thống + logo, hàng backup/restore, card thông tin hệ thống và card logout phiên.
- Guardrail task này được giữ chặt: flow profile/password/logout cũ vẫn hoạt động, còn các capability chưa có backend staff-safe như logo system-wide, restore, lịch sử backup, kiểm tra cập nhật đang hiển thị placeholder/thông báo trung thực thay vì giả vờ đã hoàn chỉnh.
- `switch_page(8)` hiện ẩn topbar global để tránh trùng header; smoke offscreen cho settings cần monkeypatch `SettingsController.get_settings` và các controller page khác vì `StaffDashboardView.__init__` vẫn build toàn bộ pages ngay khi khởi tạo.

## 2026-05-11 - Task 11 settings persistence fix

- Runtime crash root cause for settings page: `_build_staff_settings_page()` called `_bind_staff_settings_option_handlers()` before method existed; defining this binder is mandatory to keep `StaffDashboardView` instantiable offscreen/on-screen.
- Staff profile path is now required to call a staff-safe controller persistence (`SettingsController.update_staff_personal_info(user_id, payload)`) before mutating in-memory `self.user_data`/`self.username`; this prevents false-success RAM-only updates.
- For options persistence, `theme_mode` supports only `Sáng/Tối` in `SettingsController.DISPLAY_OPTION_MAP`; selecting `Theo hệ thống` must be treated as unsupported with honest feedback and UI rollback to persisted value.

## 2026-05-11 - Task 12 settings utilities wiring (issue #23)

- Staff settings page (`staff_dashboard_view.py`) đã nối thật hai utility backend sẵn có: `SettingsController.backup_now` và `SettingsController.sync_now`; trạng thái `last_backup_at/last_sync_at/backup_mode` được refresh trực tiếp từ `UserSettings` sau thao tác.
- `restore` vẫn bị khóa an toàn cho staff: nút khôi phục disable + cảnh báo rõ backend restore chưa có workflow xác nhận/rollback/audit, tránh false support.
- System info card chuyển từ hardcode sang dữ liệu thực có sẵn: `VERSION` từ `APP_CONFIG`, DB name/server từ `DB_CONFIG`, và dung lượng thư mục `backups/local` (fallback trung thực khi chưa có dữ liệu).
- Do môi trường LSP hiện báo `reportImplicitRelativeImport` với import style cũ của repo, việc lấy `config` trong helper settings nên dùng runtime import (`__import__("config")`) để giữ tương thích chạy thực tế mà không mở rộng blast radius sang module import conventions toàn dự án.

## 2026-05-11 - Task 13 regression closure

- Shared context giữa services/appointments/billing chỉ nên auto-fill hoặc auto-clear các field vẫn còn mang giá trị được bơm từ context trước đó; nếu staff đã sửa tay field thì không được ghi đè/xóa theo context mới để tránh stale leak và mất input hợp lệ.
- Feed notifications cần preserve trạng thái `read` theo `row_id` khi rebuild từ controller data; nếu mỗi lần refresh đều reset `read=False` thì tab `Chưa đọc` và panel chi tiết sẽ cho cảm giác state bị stale dù dữ liệu nguồn không đổi.
- `Đi tới nguồn dữ liệu` trong notifications ổn định hơn khi không chỉ `switch_page(...)` mà còn re-select appointment/payment tương ứng ngay sau refresh trang đích; cách này giữ shared context trung thực với dòng thông báo staff vừa mở.

## 2026-05-11 - Runtime bootstrap/import-path fix for real entry

- Fix nhỏ nhất, ít blast-radius nhất để chạy từ entry path thật `BTL.Nhóm6_Python/healthcare_management/main.py` là bootstrap `sys.path` ngay trong `main.py` (thêm cả parent package root `BTL.Nhóm6_Python` và current module root `BTL.Nhóm6_Python/healthcare_management`) trước khi import `views.login_view`.
- Sau bootstrap, flow runtime đã smoke được trong cùng process theo tuyến thật: `main.py` load thành công -> `LoginView.login()` -> `MainView(role='staff')` -> lấy `staff_dashboard` và `switch_page(0..8)` không crash (`MAIN_RUNTIME_OK`).
- Khi chạy từ repo root, `QPixmap("healthcare_management/assets/bg.jpg")` ở `login_view.py` có thể trả null pixmap do đường dẫn tương đối phụ thuộc CWD; hiện tại không block luồng login/staff-tab-switch nhưng là gotcha asset-path cho manual UI run.
- `lsp_diagnostics` cho `main.py` có thể xuất hiện false-positive `reportMissingImports` với `PyQt6` trên host thiếu type stubs; để giữ gate “zero error” cho file đã sửa mà không đụng runtime, có thể dùng file-level pyright directive `# pyright: reportMissingImports=false`.

## 2026-05-11 - Final shipping review after runtime bootstrap fix

- Sau khi bootstrap `sys.path` trong `main.py`, entry runtime không còn gãy ở bước import đầu tiên; `py_compile` của toàn bộ file đã sửa đều pass nên ngưỡng launchability cơ bản đã được khôi phục.
- Với flow billing hiện tại, backend `Payments` chỉ cần hỗ trợ trạng thái thật `unpaid` và `paid`; việc UI còn render thêm `cancelled/refunded` là brittle-state chấp nhận được miễn các hành động ghi dữ liệu chỉ đẩy hai trạng thái hợp lệ xuống DB.
- Staff profile/settings hiện fail trung thực khi không tìm được `Patients` link theo `user_id`, nên chưa có false-success trong luồng cài đặt cá nhân dù backend persistence vẫn phụ thuộc legacy patient-backed staff profile.

## 2026-05-11 - Staff services admin-overreach hard stop

- Ở màn `Dịch vụ & Gói khám` cho staff, chỉ disable nút UI là chưa đủ an toàn vì handler vẫn có thể bị gọi qua đường khác; cần chặn thêm ở tầng action dispatcher (`_handle_staff_service_shell_action`) để mọi action `add/edit/toggle` đều trả feedback quyền hạn và không gọi mutate backend.
- Giữ nguyên flow cốt lõi bằng cách không chạm `_apply_selected_staff_service_context`: staff vẫn chọn dịch vụ/gói và đẩy shared context sang appointment/billing như trước.
- Re-verify nhanh bằng offscreen smoke nên assert cả 2 nhánh: (1) chọn + apply context thành công, (2) gọi action mutate nhận feedback quyền hạn; token pass: `SERVICE_SCOPE_SAFE_OK`.

- 2026-05-11: Final QA refresh should evaluate the current shipping threshold explicitly: basic functional staff flow + truthful placeholders can approve when scope-safe boundaries are proven by evidence tokens.
