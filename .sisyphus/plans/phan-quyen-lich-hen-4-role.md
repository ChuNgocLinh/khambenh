# Kế hoạch hoàn thiện màn Quản lý lịch hẹn (Staff) + phân quyền 4 role

## TL;DR
> **Summary**: Hoàn thiện đầy đủ màn "Quản lý lịch hẹn" cho Staff theo UI spec CarePlus, đồng thời chuẩn hóa phân quyền 4 role (admin/staff/doctor/patient) cho nghiệp vụ lịch hẹn với DB role canonical.
> **Deliverables**:
> - Màn staff appointment đúng cấu trúc 3 vùng + table + detail panel + legend + pagination.
> - Ma trận quyền 4 role và enforcement tại controller/model + gating UI.
> - Migration DB bổ sung role `staff`, xử lý legacy mapping, và bộ test/CI tối thiểu cho RBAC lịch hẹn.
> **Effort**: Large
> **Parallel**: YES - 4 waves
> **Critical Path**: T1 RBAC matrix + T2 DB migration → T4/T5 controller-model enforcement → T7/T8 UI staff appointment → T10 tests

## Context

### Original Request
- Hoàn thiện đầy đủ màn "Quản lý lịch hẹn" PyQt6 cho Staff theo spec chi tiết (layout, dữ liệu mẫu, badge màu, action menu, right panel).
- Phân biệt rõ quyền cho 4 role: admin, staff, bác sĩ, bệnh nhân.
- Được phép sửa DB.

### Interview Summary
- User xác nhận muốn làm **đầy đủ màn Staff Appointment Management**, không chỉ RBAC backend.
- User chấp nhận phương án "làm đầy đủ" gồm UI + quyền + DB + kiểm thử.

### Metis Review (gaps addressed)
- Chốt nguồn sự thật role ở DB (không duy trì 2 nguồn lâu dài).
- Enforce quyền tại backend trước, UI chỉ là lớp hiển thị.
- Có migration theo pha + kiểm tra drift quyền trước/sau.
- Giới hạn scope trong module lịch hẹn để tránh scope creep.

## Work Objectives

### Core Objective
Triển khai đầy đủ màn "Quản lý lịch hẹn" cho Staff theo spec và đảm bảo mọi thao tác lịch hẹn tuân thủ RBAC 4 role thống nhất từ DB → model/controller → UI.

### Deliverables
1. UI staff appointment khớp spec chức năng/chủ đề.
2. RBAC matrix chuẩn hóa cho action lịch hẹn.
3. DB migration thêm `staff` + migration dữ liệu legacy.
4. Auth role resolution thống nhất (loại bỏ dần heuristic).
5. Test/QA tự động cho luồng quyền và luồng nghiệp vụ chính.

### Definition of Done (verifiable)
- `python -m healthcare_management.main` hiển thị màn staff appointment đủ: tabs, search, filters, table 6 cột, right panel, legend, pagination.
- Tài khoản mỗi role chỉ thấy/được thao tác đúng quyền đã định.
- DB `Users.role` chấp nhận `staff`; dữ liệu legacy chuyển đổi không lỗi.
- Test RBAC + appointment flow pass trong local/CI.

### Must Have
- Role canonical: `admin|staff|doctor|patient`.
- RBAC action-level cho lịch hẹn: view/list/detail/create/update/cancel/confirm/check-in/start/complete/print.
- Dữ liệu trạng thái chuẩn: `pending|confirmed|in_progress|done|cancelled`.

### Must NOT Have
- Không dùng username heuristic lâu dài để cấp quyền staff.
- Không chỉ chặn bằng UI mà bỏ backend.
- Không mở rộng sang module ngoài lịch hẹn (billing/report sâu) trừ chỗ phụ thuộc trực tiếp.

## Verification Strategy
> ZERO HUMAN INTERVENTION - all verification is agent-executed.

- Test decision: tests-after, framework `pytest` (bootstrap nếu chưa có).
- QA policy: Mỗi task có ít nhất 1 happy + 1 failure scenario.
- Evidence: `.sisyphus/evidence/task-{N}-{slug}.{ext}`.

## Execution Strategy

### Parallel Execution Waves
Wave 1 (foundation): T1, T2, T3
Wave 2 (backend enforcement): T4, T5, T6
Wave 3 (UI staff appointment): T7, T8, T9
Wave 4 (quality gate): T10, T11, T12

### Dependency Matrix
- T1 blocks T4,T6,T8,T10
- T2 blocks T3,T4,T10
- T3 blocks T6
- T4 blocks T7,T8,T10
- T5 blocks T8,T10
- T6 blocks T8,T9
- T7 blocks T9,T11
- T8 blocks T10,T11
- T10 blocks T12

### Agent Dispatch Summary
- Wave 1: 3 tasks (quick/unspecified-high)
- Wave 2: 3 tasks (unspecified-high)
- Wave 3: 3 tasks (visual-engineering + unspecified-high)
- Wave 4: 3 tasks (unspecified-high + deep)

## TODOs

- [x] 1. Định nghĩa ma trận quyền RBAC cho lịch hẹn

  **What to do**:
  - Tạo bảng action x role cho: list_all, list_own, view_detail, create, update_time, update_doctor, confirm, start_consultation, complete, cancel, print.
  - Chốt quy tắc ownership:
    - patient: chỉ appointment của chính mình.
    - doctor: chỉ appointment gán cho doctor_id của mình.
    - staff/admin: toàn bộ appointment.

  **Must NOT do**:
  - Không để action nào mơ hồ ("có thể").

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: Quyết định nghiệp vụ xuyên lớp.
  - Skills: `[]`
  - Omitted: `[]`

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: T4,T6,T8,T10 | Blocked By: none

  **References**:
  - `healthcare_management/views/main_view.py`
  - `healthcare_management/controllers/appointment_controller.py`
  - `healthcare_management/models/appointment_model.py`

  **Acceptance Criteria**:
  - [ ] Có tài liệu RBAC matrix lưu trong repo (module docs nội bộ hoặc comment hằng số quyền).
  - [ ] Tất cả action lịch hẹn có trạng thái Allow/Deny cho 4 role.

  **QA Scenarios**:
  ```
  Scenario: RBAC matrix đủ action
    Tool: Bash
    Steps: Chạy script kiểm tra presence action keys trong RBAC map
    Expected: Không thiếu action; exit code 0
    Evidence: .sisyphus/evidence/task-1-rbac-matrix.txt

  Scenario: Action chưa khai báo
    Tool: Bash
    Steps: Inject test action giả và chạy validator
    Expected: Validator báo lỗi rõ ràng
    Evidence: .sisyphus/evidence/task-1-rbac-matrix-error.txt
  ```

  **Commit**: YES | Message: `feat(rbac): define appointment permissions for 4 roles` | Files: `controllers/*`, `views/*`, `docs/internal*`

- [x] 2. Chuẩn hóa DB role và migration legacy staff

  **What to do**:
  - Cập nhật schema `Users.role` cho phép `staff` trong `database/init_db.sql`.
  - Thêm migration trong `database/migrate.py` để:
    - Nới CHECK constraint/enum role.
    - Backfill user legacy staff (theo tiêu chí hiện hành) sang role `staff`.
    - Ghi log số lượng record đổi role.

  **Must NOT do**:
  - Không overwrite role của doctor/admin/patient hợp lệ.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: thay đổi schema + dữ liệu nhạy cảm.
  - Skills: `[]`
  - Omitted: `[]`

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: T3,T4,T10 | Blocked By: none

  **References**:
  - `healthcare_management/database/init_db.sql`
  - `healthcare_management/database/migrate.py`
  - `healthcare_management/models/user_model.py` (legacy normalize_role)

  **Acceptance Criteria**:
  - [ ] DB mới cho phép role `staff`.
  - [ ] Migration chạy idempotent 2 lần không lỗi.
  - [ ] Có thống kê trước/sau số lượng theo role.

  **QA Scenarios**:
  ```
  Scenario: Migration thành công
    Tool: Bash
    Steps: Chạy migrate script trên DB test
    Expected: Schema cập nhật + log migrated count
    Evidence: .sisyphus/evidence/task-2-migration.txt

  Scenario: Re-run migration
    Tool: Bash
    Steps: Chạy migrate lần 2
    Expected: Không lỗi duplicate/constraint
    Evidence: .sisyphus/evidence/task-2-migration-rerun.txt
  ```

  **Commit**: YES | Message: `feat(db): add explicit staff role and migration` | Files: `database/init_db.sql`, `database/migrate.py`

- [x] 3. Chuẩn hóa login role resolution

  **What to do**:
  - Điều chỉnh `models/user_model.py` và `controllers/auth_controller.py` để ưu tiên role canonical từ DB.
  - Giữ fallback normalize có cờ tương thích tạm (`LEGACY_STAFF_ROLE_FALLBACK`) và logging.
  - Định nghĩa điều kiện gỡ fallback sau khi migration pass.

  **Must NOT do**:
  - Không xóa fallback ngay nếu chưa có migration-safe gate.

  **Recommended Agent Profile**:
  - Category: `quick` - Reason: phạm vi file hẹp, logic cụ thể.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: T6 | Blocked By: T2

  **References**:
  - `healthcare_management/models/user_model.py`
  - `healthcare_management/controllers/auth_controller.py`

  **Acceptance Criteria**:
  - [ ] Login trả role `staff` đúng với record DB.
  - [ ] Có log khi fallback được dùng.

  **QA Scenarios**:
  ```
  Scenario: User staff canonical login
    Tool: Bash
    Steps: Seed user role=staff, gọi login()
    Expected: Response.role = staff
    Evidence: .sisyphus/evidence/task-3-login-role.txt

  Scenario: Legacy fallback disabled
    Tool: Bash
    Steps: Tắt flag fallback, login user legacy
    Expected: Không auto-map sai role
    Evidence: .sisyphus/evidence/task-3-login-role-error.txt
  ```

  **Commit**: YES | Message: `refactor(auth): canonicalize role resolution with guarded fallback` | Files: `models/user_model.py`, `controllers/auth_controller.py`

- [x] 4. Enforce quyền trong AppointmentController

  **What to do**:
  - Bọc tất cả API nghiệp vụ lịch hẹn trong `controllers/appointment_controller.py` bằng `authorize(role, action, user_context, appointment)`.
  - Trả kết quả deny nhất quán (`status=False`, message rõ ràng).
  - Bổ sung API role-scoped list (`get_all_for_role`).

  **Must NOT do**:
  - Không để route nào bypass authorize.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: điểm chặn bảo mật chính.

  **Parallelization**: Can Parallel: NO | Wave 2 | Blocks: T7,T8,T10 | Blocked By: T1,T2

  **References**:
  - `healthcare_management/controllers/appointment_controller.py`
  - `healthcare_management/models/appointment_model.py`

  **Acceptance Criteria**:
  - [ ] Mọi action lịch hẹn kiểm tra quyền trước khi mutate/read nhạy cảm.
  - [ ] Lỗi deny đồng nhất format.

  **QA Scenarios**:
  ```
  Scenario: Staff update appointment
    Tool: Bash
    Steps: Gọi API update với role=staff
    Expected: Thành công khi dữ liệu hợp lệ
    Evidence: .sisyphus/evidence/task-4-controller-auth.txt

  Scenario: Patient cố update appointment người khác
    Tool: Bash
    Steps: Gọi update với patient_id không ownership
    Expected: Bị từ chối với message quyền
    Evidence: .sisyphus/evidence/task-4-controller-auth-error.txt
  ```

  **Commit**: YES | Message: `feat(appointment): add controller-level authorization gates` | Files: `controllers/appointment_controller.py`

- [x] 5. Bổ sung query role-scoped ở AppointmentModel

  **What to do**:
  - Thêm các query rõ ràng: `get_for_staff_admin`, `get_for_doctor`, `get_for_patient`, `get_detail_with_joins`.
  - Bảo toàn status mapping + filter today/tomorrow/by-date + search/filter doctor/service/status.

  **Must NOT do**:
  - Không trả data ngoài scope role.

  **Recommended Agent Profile**:
  - Category: `unspecified-high`

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: T8,T10 | Blocked By: T1

  **References**:
  - `healthcare_management/models/appointment_model.py`
  - `healthcare_management/database/init_db.sql` (Appointments, Doctors, Patients)

  **Acceptance Criteria**:
  - [ ] Role query trả đúng tập dữ liệu theo ownership.
  - [ ] Filter/search tương thích yêu cầu màn staff.

  **QA Scenarios**:
  ```
  Scenario: Staff lọc theo bác sĩ + trạng thái
    Tool: Bash
    Steps: Query với doctor_id/status
    Expected: Chỉ trả bản ghi khớp filter
    Evidence: .sisyphus/evidence/task-5-model-filters.txt

  Scenario: Doctor truy cập appointment bác sĩ khác
    Tool: Bash
    Steps: Query role doctor với doctor_id mismatch
    Expected: Không trả dữ liệu ngoài quyền
    Evidence: .sisyphus/evidence/task-5-model-filters-error.txt
  ```

  **Commit**: YES | Message: `feat(appointment-model): role-scoped queries and filters` | Files: `models/appointment_model.py`

- [x] 6. Gating role điều hướng vào đúng dashboard/view

  **What to do**:
  - Chuẩn hóa entry trong `views/main_view.py` cho 4 role.
  - Đảm bảo role không hợp lệ vào màn fallback an toàn.
  - Đồng bộ nhãn role hiển thị.

  **Must NOT do**:
  - Không hardcode role mơ hồ trong nhiều nơi.

  **Recommended Agent Profile**:
  - Category: `quick`

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: T8,T9 | Blocked By: T1,T3

  **References**:
  - `healthcare_management/views/main_view.py`
  - `healthcare_management/views/login_view.py`

  **Acceptance Criteria**:
  - [ ] Đăng nhập mỗi role mở đúng dashboard tương ứng.

  **QA Scenarios**:
  ```
  Scenario: Login role staff vào StaffDashboardView
    Tool: interactive_bash
    Steps: Seed user staff, login UI
    Expected: Render sidebar staff + module lịch hẹn
    Evidence: .sisyphus/evidence/task-6-role-routing.png

  Scenario: Role rác
    Tool: interactive_bash
    Steps: Seed role invalid, login
    Expected: Màn fallback an toàn, không crash
    Evidence: .sisyphus/evidence/task-6-role-routing-error.png
  ```

  **Commit**: YES | Message: `fix(auth-ui): enforce role-based dashboard routing` | Files: `views/main_view.py`, `views/login_view.py`

- [x] 7. Hoàn thiện UI shell màn Staff Appointment theo spec

  **What to do**:
  - Cập nhật `views/staff_dashboard_view.py` (hoặc tách subview) để có 3 vùng: sidebar ~200px, main ~65%, detail ~35%.
  - Top tabs: Hôm nay, Ngày mai, Theo ngày.
  - Toolbar: search + nút "+ Tạo lịch hẹn"; filter row 4 controls.

  **Must NOT do**:
  - Không phá style chung các module staff khác.

  **Recommended Agent Profile**:
  - Category: `visual-engineering` - Reason: layout fidelity + UX detail.

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: T9,T11 | Blocked By: T4

  **References**:
  - `healthcare_management/views/staff_dashboard_view.py`
  - UI spec from user prompt.

  **Acceptance Criteria**:
  - [ ] Có đủ 3 vùng layout và control rows đúng thứ tự.
  - [ ] Màu primary và active tab đúng `#1A9B6C`.

  **QA Scenarios**:
  ```
  Scenario: Render đầy đủ shell
    Tool: Playwright
    Steps: Mở màn staff appointment, chụp screenshot viewport 1440x900
    Expected: Đủ sidebar/main/detail và top tabs
    Evidence: .sisyphus/evidence/task-7-ui-shell.png

  Scenario: Resize cửa sổ
    Tool: Playwright
    Steps: Resize 1280x800 và 1600x900
    Expected: Layout không chồng lấp, panel phải vẫn hiển thị hợp lý
    Evidence: .sisyphus/evidence/task-7-ui-shell-resize.png
  ```

  **Commit**: YES | Message: `feat(staff-ui): build appointment management shell layout` | Files: `views/staff_dashboard_view.py`

- [x] 8. Bảng lịch hẹn + trạng thái + action theo quyền

  **What to do**:
  - Implement table 6 cột đúng dữ liệu mẫu + badge màu trạng thái.
  - Cột thao tác có 👁️ và ⋮; menu action tùy role:
    - admin/staff: view/edit/reschedule/reassign/cancel/print
    - doctor: view/start/complete (không đổi bác sĩ)
    - patient: view/cancel (nếu chưa in_progress/done)

  **Must NOT do**:
  - Không hiển thị action mà backend deny.

  **Recommended Agent Profile**:
  - Category: `visual-engineering`

  **Parallelization**: Can Parallel: NO | Wave 3 | Blocks: T10,T11 | Blocked By: T1,T4,T5,T6

  **References**:
  - `healthcare_management/views/staff_dashboard_view.py`
  - `healthcare_management/controllers/appointment_controller.py`
  - `healthcare_management/models/appointment_model.py`

  **Acceptance Criteria**:
  - [ ] 8 dòng mẫu hiển thị đúng format giờ/tên/sđt/dịch vụ/bác sĩ/status.
  - [ ] Badge màu đúng mã màu spec.
  - [ ] Action menu khác nhau theo role và thực thi đúng quyền.

  **QA Scenarios**:
  ```
  Scenario: Staff thấy đầy đủ action
    Tool: Playwright
    Steps: Login staff, mở menu row 1
    Expected: Có edit/cancel/print và thao tác thành công
    Evidence: .sisyphus/evidence/task-8-table-actions-staff.png

  Scenario: Patient không thấy action cấm
    Tool: Playwright
    Steps: Login patient, mở menu row
    Expected: Không có reassign/complete; gọi API trực tiếp bị deny
    Evidence: .sisyphus/evidence/task-8-table-actions-patient-error.txt
  ```

  **Commit**: YES | Message: `feat(appointments-ui): role-aware table actions and status badges` | Files: `views/staff_dashboard_view.py`, `controllers/appointment_controller.py`

- [x] 9. Right panel chi tiết + timeline + 3 nút thao tác

  **What to do**:
  - Render chi tiết lịch hẹn: patient card, info grid, timeline, nút sửa/hủy/in.
  - Đồng bộ trạng thái enable/disable nút theo role + trạng thái lịch.

  **Must NOT do**:
  - Không cho thực thi nút khi backend không cho phép.

  **Recommended Agent Profile**:
  - Category: `visual-engineering`

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: T11 | Blocked By: T6,T7

  **References**:
  - `healthcare_management/views/staff_dashboard_view.py`
  - `healthcare_management/controllers/appointment_controller.py`

  **Acceptance Criteria**:
  - [ ] Right panel khớp spec text chính.
  - [ ] Timeline hiển thị dot + timestamp + mô tả.

  **QA Scenarios**:
  ```
  Scenario: Click row cập nhật panel
    Tool: Playwright
    Steps: Chọn từng row trong table
    Expected: Detail panel đổi đúng dữ liệu row
    Evidence: .sisyphus/evidence/task-9-detail-panel.png

  Scenario: Nút disabled theo quyền
    Tool: Playwright
    Steps: Login doctor/patient thử nút sửa/hủy/in
    Expected: Nút cấm bị disable hoặc blocked với message
    Evidence: .sisyphus/evidence/task-9-detail-panel-error.png
  ```

  **Commit**: YES | Message: `feat(appointments-ui): implement detail panel and timeline` | Files: `views/staff_dashboard_view.py`

- [x] 10. Bootstrap test infra + RBAC tests

  **What to do**:
  - Thiết lập `pytest` tối thiểu.
  - Viết test cho appointment authorization matrix + ownership checks + status transition rules.
  - Thêm workflow CI chạy test.

  **Must NOT do**:
  - Không để test phụ thuộc dữ liệu production.

  **Recommended Agent Profile**:
  - Category: `unspecified-high`

  **Parallelization**: Can Parallel: YES | Wave 4 | Blocks: T12 | Blocked By: T1,T2,T4,T5,T8

  **References**:
  - `healthcare_management/controllers/appointment_controller.py`
  - `healthcare_management/models/appointment_model.py`
  - `healthcare_management/database/*`

  **Acceptance Criteria**:
  - [ ] Có test chạy bằng một lệnh chuẩn.
  - [ ] Có test deny/allow cho 4 role.

  **QA Scenarios**:
  ```
  Scenario: Test suite pass
    Tool: Bash
    Steps: Chạy pytest
    Expected: 100% test RBAC/appointment pass
    Evidence: .sisyphus/evidence/task-10-tests.txt

  Scenario: Introduce forbidden action
    Tool: Bash
    Steps: Bật case patient complete appointment
    Expected: Test fail đúng case
    Evidence: .sisyphus/evidence/task-10-tests-error.txt
  ```

  **Commit**: YES | Message: `test(rbac): add appointment permission and ownership coverage` | Files: `tests/*`, `.github/workflows/*`

- [ ] 11. QA UI regression cho màn Staff Appointment

  **What to do**:
  - Chạy QA checklist theo spec: tabs, search, filter, table, pagination, legend, detail panel.
  - Thu screenshot bằng role staff/doctor/patient.

  **Must NOT do**:
  - Không kết luận pass khi thiếu evidence file.

  **Recommended Agent Profile**:
  - Category: `unspecified-high`

  **Parallelization**: Can Parallel: YES | Wave 4 | Blocks: T12 | Blocked By: T7,T8,T9

  **References**:
  - `healthcare_management/views/staff_dashboard_view.py`
  - UI spec user-provided.

  **Acceptance Criteria**:
  - [ ] Bộ ảnh evidence đủ tất cả vùng UI chính.
  - [ ] Không có mismatch lớn so với spec (màu, cấu trúc, thành phần).

  **QA Scenarios**:
  ```
  Scenario: Visual pass staff role
    Tool: Playwright
    Steps: Capture full-page screenshots với dữ liệu mẫu
    Expected: Đúng 3 vùng + table 8 rows + right panel
    Evidence: .sisyphus/evidence/task-11-visual-staff.png

  Scenario: Role doctor/patient truy cập màn staff-only
    Tool: Playwright
    Steps: Login doctor/patient vào route/menu staff
    Expected: Không truy cập trái quyền hoặc chỉ thấy bản thu gọn đúng policy
    Evidence: .sisyphus/evidence/task-11-visual-role-error.png
  ```

  **Commit**: NO | Message: `n/a` | Files: `n/a`

- [ ] 12. Tắt fallback legacy và cleanup

  **What to do**:
  - Sau khi migration + tests pass, tắt `LEGACY_STAFF_ROLE_FALLBACK` mặc định.
  - Xóa/giảm logic normalize dựa username nếu đã an toàn.
  - Cập nhật release note nội bộ về breaking/behavior change.

  **Must NOT do**:
  - Không tắt fallback trước khi test pass toàn bộ.

  **Recommended Agent Profile**:
  - Category: `quick`

  **Parallelization**: Can Parallel: NO | Wave 4 | Blocks: none | Blocked By: T10

  **References**:
  - `healthcare_management/models/user_model.py`
  - `healthcare_management/controllers/auth_controller.py`

  **Acceptance Criteria**:
  - [ ] Không còn cấp staff bằng heuristic ở runtime mặc định.
  - [ ] Login 4 role vẫn hoạt động đúng.

  **QA Scenarios**:
  ```
  Scenario: Post-cleanup login matrix
    Tool: Bash
    Steps: Chạy test login cho 4 role
    Expected: Tất cả pass, không fallback warning bất thường
    Evidence: .sisyphus/evidence/task-12-cleanup.txt

  Scenario: Legacy username không còn auto-elevate
    Tool: Bash
    Steps: Seed patient username staff123 nhưng role=patient
    Expected: Không bị map thành staff
    Evidence: .sisyphus/evidence/task-12-cleanup-error.txt
  ```

  **Commit**: YES | Message: `chore(auth): remove legacy staff role heuristic` | Files: `models/user_model.py`, `controllers/auth_controller.py`

## Final Verification Wave (MANDATORY — after ALL implementation tasks)
- [ ] F1. Plan Compliance Audit — oracle
- [ ] F2. Code Quality Review — unspecified-high
- [ ] F3. Real Manual QA — unspecified-high (+ playwright if UI)
- [ ] F4. Scope Fidelity Check — deep

## Commit Strategy
- Commit theo từng task lớn (RBAC, DB, auth, controller/model, UI, tests).
- Không gộp migration + UI vào cùng commit.

## Success Criteria
- Màn Staff Appointment đạt spec chức năng/chính tả/màu/chức năng cốt lõi.
- Phân quyền 4 role nhất quán từ DB tới UI.
- Không còn privilege drift do legacy mapping.
- Có bằng chứng QA + test pass để sẵn sàng merge.
