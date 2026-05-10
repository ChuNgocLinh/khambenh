## 2026-05-10T07:40:00Z Task: init
Khởi tạo notepad cho plan phan-quyen-lich-hen-4-role.

## 2026-05-10T08:02:00Z Task: T1
Đã xác nhận artifact RBAC được thêm trong appointment_controller.py gồm ROLES, APPOINTMENT_ACTIONS, APPOINTMENT_RBAC.
Có helper ownership cho patient/doctor và validator matrix debug_validate_rbac_matrix().
T1 đủ nền tảng cho enforcement ở T4/T5; chưa đụng DB/UI theo đúng scope.
- Added canonical appointment RBAC artifact in `AppointmentController` with explicit `allow/deny` sets per action for roles admin/staff/doctor/patient.
- Standardized action list for downstream tasks: list_all, list_own, view_detail, create, update_time, update_doctor, confirm, start_consultation, complete, cancel, print.
- Ownership rules are explicit helpers: patient can match only own patient_id, doctor can match only own doctor_id; staff/admin remain global by matrix.
- Added `_validate_rbac_matrix()` to prevent privilege drift by asserting full action coverage and full 4-role coverage per action.
- Added `debug_validate_rbac_matrix()` returning `{"status": bool, "message": str}` so later tasks can reuse current deny/response conventions.
- Validation run succeeded with debug output: RBAC matrix is valid and complete.

## 2026-05-10T08:18:00Z Task: T2
Đã chuẩn hóa schema Users.role với canonical set có `staff` trong init_db.sql (đồng bộ comment).
Đã có migration idempotent ở database/migrate.py: chỉ backfill user role=patient và username match `^staff\d+$` sang staff.
Migration in đầy đủ phân bố role trước/sau + migrated_to_staff count.
Đã verify chạy 2 lần liên tiếp: run2 không gây tác động ngoài mong đợi (idempotent).

## 2026-05-10T10:51:55Z Task: T2
- init_db.sql đã canonical CHECK role gồm admin/doctor/patient/staff; thêm comment để đồng bộ với migration.
- database/migrate.py thêm migration idempotent: chỉ migrate Users.role=patient có username khớp ^staff\d+$ sang staff.
- Migration in thống kê role trước/sau và migrated_to_staff để audit privilege drift.
- Verify chạy 2 lần bằng python -m database.migrate: lần 1 migrated=1, lần 2 migrated=0, phân phối role ổn định.

## 2026-05-10T11:00:00Z Task: T3
- UserModel đã chuyển sang DB-first role resolution với `resolve_login_role`.
- Có cờ `LEGACY_STAFF_ROLE_FALLBACK` để bật/tắt tương thích legacy; mặc định đang bật.
- Khi fallback kích hoạt có warning log rõ ràng để theo dõi và chuẩn bị gỡ ở T12.
- AuthController giữ nguyên contract payload login (`status`, `user`, `role`, `message`).

## 2026-05-10T11:32:00Z Task: T4
- Đã thêm gate trung tâm `authorize(role, action, user_context, appointment)` và helper `_deny(...)`.
- Đã thêm `get_all_for_role` để role-scoped listing: admin/staff toàn bộ, doctor/patient theo ownership context.
- Các flow mutate chính (`create`, `update_status`, `update_full`, `cancel`) đã bọc kiểm tra quyền trước business logic.
- Signature được giữ backward-compatible bằng optional params `role=None, user_context=None`.

## 2026-05-10T11:50:00Z Task: T5
- AppointmentModel đã có bộ query role-scoped: `get_for_staff_admin`, `get_for_doctor`, `get_for_patient`.
- Đã thêm `get_detail_with_joins(appointment_id)` phục vụ panel chi tiết với dữ liệu joined.
- Filter hỗ trợ today/tomorrow/by-date + search (name/phone/service) + doctor/service/status và ORDER BY deterministic.
- Sanity import pass, lsp error = 0, không còn TODO/FIXME trong file mới chỉnh.

## 2026-05-10T12:04:00Z Task: T6
- Đã chuẩn hóa routing role ở `main_view.py` bằng `CANONICAL_ROLES`, `normalize_role`, và `_route_role_view()`.
- Role không hợp lệ được ép về `unknown` và đi vào fallback UI an toàn (`init_unknown_role_ui`) thay vì rẽ nhánh mơ hồ.
- LoginView contract giữ nguyên, không cần đổi file login_view.py trong task này.
- Compile file pass; các lsp errors còn lại chủ yếu là tồn đọng import-style/type toàn file, không phát sinh blocker runtime mới từ phần routing vừa thêm.

## 2026-05-10T12:18:00Z Task: T7
- `_build_appointment_management_page` đã được dựng lại theo shell 3 vùng: sidebar trái, main giữa, detail panel phải.
- Đã có tabs top, toolbar search + nút tạo lịch, filter row 4 controls và table/detail containers cho các task T8/T9.
- Giữ tương thích wiring chính (selection/create hooks) và compile pass.

## 2026-05-10T12:42:00Z Task: T8
- Bảng lịch hẹn đã chuyển về 6 cột UI chuẩn: Giờ hẹn, Bệnh nhân, Dịch vụ, Bác sĩ, Trạng thái, Thao tác.
- Đã thêm status badge mapping đúng màu cho pending/confirmed/in_progress/done/cancelled.
- Cột thao tác có widget 👁️ + ⋮ và menu options ẩn/hiện theo role hiện tại.
- Action menu đã nối với flow an toàn: view/edit/reschedule/reassign/cancel/print/start/complete theo permission role.

## 2026-05-10T11:20:00Z Task: T3
- Chu?n h�a login role resolution theo DB-first: th�m `resolve_login_role(role, username)` trong `models/user_model.py`, �u ti�n role canonical t? DB (`admin|staff|doctor|patient`) v� gi? nguy�n role canonical ��ng s?n.
- Th�m c? b?o v? `UserModel.LEGACY_STAFF_ROLE_FALLBACK = True` �? b?t/t?t backward-compat mapping legacy `patient + ^staff\d+$ -> staff`.
- Khi fallback legacy ��?c �p d?ng, ghi `logging.warning` r? r�ng v?i username v� role chuy?n �?i �? audit/gi?m d?n heuristic.
- `UserModel.login` v� `AuthController.login` �?u d�ng `resolve_login_role`; payload login kh�ng �?i format (`status`, `user`, `role`, `message`).
- Verify: LSP errors = 0 cho 2 file s?a; m� ph?ng runtime cho fallback ON/OFF cho k?t qu? ��ng (`on staff`, `off patient`) v� warning log xu?t hi?n khi fallback ch?y.

## 2026-05-10T11:55:00Z Task: T4
- Added centralized auth gate in AppointmentController: _deny, _get_context_value, uthorize (RBAC + ownership checks for doctor/patient on record-level actions).
- Added role-scoped listing API get_all_for_role(role, user_context) with admin/staff full list, doctor/patient own-list, and deny response for invalid/missing context.
- Wrapped mutating flows with optional auth params (backward-compatible): create(..., role=None, user_context=None), update_status(..., role=None, user_context=None), update_full(..., role=None, user_context=None), and new cancel(appointment_id, role=None, user_context=None) using centralized authorize before mutation.

## 2026-05-10T12:30:00Z Task: T7
- Rebuilt `StaffDashboardView._build_appointment_management_page` into a 3-zone shell for appointment management: left sidebar (fixed ~200px), center main panel, right detail panel with 65/35 stretch split.
- Implemented top tab row with 3 labels exactly per spec: `L?ch h?n h�m nay`, `L?ch h?n ng�y mai`, `?? L?ch h?n theo ng�y`; active state styled with `#1A9B6C` and underline.
- Added toolbar row with search input + green primary `+ T?o l?ch h?n` action, while preserving existing create/reschedule/cancel/reset signal wiring compatibility.
- Added filter row with 4 controls ready for T8/T9 behavior wiring: doctor, service, status, date.
- Kept non-appointment staff pages untouched; retained appointment table and selection slot as shell-ready containers for next tasks.
- Verify: `python -m py_compile` and `python -m compileall` pass for the modified file; LSP error set remains pre-existing project baseline (no new T7-specific diagnostics).

## 2026-05-10T12:25:00Z Task: T8
- B?ng l?ch h?n staff chuy?n sang 6 c?t UI: Gi? h?n | B?nh nh�n | D?ch v? | B�c s? | Tr?ng th�i | Thao t�c, v?n gi? mapping ID n?i b? qua staff_appointment_rows.
- Badge tr?ng th�i d�ng map m�u c? �?nh theo spec (confirmed/pending/in_progress/done/cancelled) b?ng cell widget QLabel �? �?m b?o m�u n?n/ch? hi?n th? ��ng.
- C?t Thao t�c d�ng widget ??? + ?; menu options ��?c ?n theo role ngay tr�n UI thay v? �? click r?i fail (admin/staff, doctor, patient).
- Data refresh d�ng AppointmentController.get_all_for_role(role, user_context) �? t�i s? d?ng RBAC hi?n c� m� kh�ng s?a controller/model/db.

- Role runtime cho b?ng l?ch h?n chu?n h�a: l?y user_data.role, fallback staff khi r?ng/kh�ng thu?c t?p admin|staff|doctor|patient.
- Menu action theo role render theo allowlist t?i UI �? ?n l?a ch?n kh�ng ��?c ph�p ngay t? �?u.
- Compile sanity b?ng python -m py_compile pass sau khi c?p nh?t fallback role.

## 2026-05-10T14:20:00Z Task: T9
- Right detail panel in `staff_dashboard_view.py` is now fully wired to table selection through `_handle_staff_appointment_selection` + `_update_staff_appt_right_panel`.
- Panel renders patient card, detail info grid, timeline entries (dot + timestamp + description), and 3 action buttons (edit/cancel/print) per spec intent.
- Action buttons are gated by role/status permissions via existing `_get_allowed_appointment_actions(appt)` to avoid exposing forbidden operations.
- Added safe empty-state reset path when no row is selected or selection is invalid.
- Verification executed: `python -m py_compile "BTL.Nhóm6_Python\healthcare_management\views\staff_dashboard_view.py"` passed.

## 2026-05-10T14:48:20Z Task: T10
- Fixed healthcare_management test bootstrap path in tests/conftest.py by adding package-parent to sys.path so absolute package imports resolve under pytest.
- Repaired RBAC ownership regression test to align with current controller API: uses AppointmentController.update_full and monkeypatches AppointmentModel.update_full (not nonexistent update_appointment).
- Removed stale ServiceModel monkeypatch that targeted nonexistent method and was unnecessary for ownership-deny short-circuit intent.
- Verification: python -m pytest -q in BTL.Nh�m6_Python/healthcare_management => 6 passed.

