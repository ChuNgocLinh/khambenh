# Kế hoạch hoàn thiện đầy đủ chức năng Doctor screens

## TL;DR
> **Summary**: Hoàn thiện toàn bộ luồng Doctor đang mount trong `DashboardView` bằng dữ liệu thật, loại bỏ dữ liệu tĩnh ở các màn chính, tách rõ trách nhiệm giữa Lịch khám / Khám bệnh / Hồ sơ bệnh nhân / Đơn thuốc / Thông báo / Cài đặt, và khóa chặt state transition nghiệp vụ.
> **Deliverables**:
> - Dashboard bác sĩ lấy dữ liệu thật và điều hướng đúng
> - Lịch khám dùng implementation data-backed duy nhất
> - Danh sách bệnh nhân, Khám bệnh, Hồ sơ bệnh nhân, Đơn thuốc, Thông báo, Cài đặt hoạt động end-to-end
> - Mở rộng schema tối thiểu cho draft khám bệnh, trạng thái đơn thuốc, notification feed
> - Bộ test `pytest`/`pytest-qt` và smoke flow cho Doctor
> **Effort**: XL
> **Parallel**: YES - 3 waves
> **Critical Path**: Task 1 → Task 2 → Task 4 → Task 6 → Task 8 → Task 9 → Task 10

## Context
### Original Request
- Hoàn thiện 8 issue Doctor #24-#31 dựa trên UI hiện có, không để màn hình tĩnh.
- Không hard-code nếu đã có model/controller thật; nếu thiếu thì thêm mock/service tạm chỉ khi bắt buộc.
- Mọi button/icon/tab/dropdown/modal phải có action thật.
- Bổ sung validation, loading, empty state, error state, toast/notification, navigation liên màn, responsive desktop hiện có.
- Sau khi xong từng issue phải chỉ ra file đã sửa và chức năng đã thêm.

### Interview Summary
- Stack thực tế: Python + PyQt6 + MySQL theo MVC desktop.
- Router Doctor thực tế: `LoginView` → `MainView(role=doctor)` → `DashboardView` với `QStackedWidget` 8 trang.
- User đã chốt:
  - **Cho phép mở rộng schema/database** để thay vùng mock bằng dữ liệu thật.
  - **Đơn thuốc**: bác sĩ được xem + tạo + sửa/hủy trước khi phát thuốc.
  - **Khám bệnh**: phải hỗ trợ **lưu tạm + hoàn tất**.
  - **Kiểm thử**: chiến lược **tests-after**.

### Decision Freeze
- **Nguồn sự thật runtime**: giữ `DashboardView` làm router Doctor duy nhất; mọi màn Doctor phải được mount qua router này.
- **Lịch khám (#25)**: thay implementation `_build_schedule_page()` tĩnh bằng `DoctorScheduleView`/flow appointment data-backed; không duy trì song song 2 implementation hoạt động.
- **Khám bệnh (#27)**: tạo file runtime riêng `BTL.Nhóm6_Python/healthcare_management/views/doctor_examination_view.py` và mount file này ở page 3; tái sử dụng `MedicalRecordView`/dialog/controller/model thật làm nền nghiệp vụ; không dùng `DoctorPatientRecordView` làm màn khám bệnh chính.
- **Hồ sơ bệnh nhân (#28)**: giữ là màn riêng, chỉ tập trung xem thông tin bệnh nhân, lịch sử khám, đơn thuốc, lịch hẹn và action điều hướng; không nhập liệu khám chính tại đây.
- **Thông báo (#30)**: triển khai **notification persisted** có read/unread + mark-all-read + điều hướng target; không dùng derived feed tạm thời trên mounted path.
- **Đơn thuốc (#29)**: thêm lifecycle tối thiểu `draft` / `issued` / `dispensed` / `cancelled`; chỉ cho sửa/hủy trước `dispensed`.
- **Khám bệnh state**: dùng lifecycle tối thiểu `draft` / `finalized`; appointment phải transition hợp lệ theo quy tắc `scheduled|confirmed|checked_in -> in_progress -> completed` hoặc `cancelled`.
- **Test authority**: chuẩn hóa test entry về `BTL.Nhóm6_Python/tests/` và dùng `BTL.Nhóm6_Python/pytest.ini` làm cấu hình chuẩn; không tạo thêm đường chạy test song song mới.

### Concrete Schema Contract
- Nếu `MedicalRecords` chưa có các cột sau thì thêm đúng các cột này: `appointment_id`, `record_status`, `finalized_at`, `updated_at`.
- `record_status` chỉ nhận `draft` hoặc `finalized`.
- Nếu `Prescriptions` chưa có các cột sau thì thêm đúng các cột này: `status`, `dispensed_at`, `updated_at`.
- `Prescriptions.status` chỉ nhận `draft`, `issued`, `dispensed`, `cancelled`.
- Tạo bảng `Notifications` nếu chưa có với tối thiểu các cột: `notification_id`, `user_id`, `title`, `content`, `type`, `target_page`, `target_id`, `is_read`, `created_at`, `read_at`.
- `target_page` chỉ dùng các giá trị thuộc mounted Doctor router: `schedule`, `patient_profile`, `prescriptions`, `dashboard`, `settings`.

### Concrete File Ownership
- Page 1 runtime owner: `BTL.Nhóm6_Python/healthcare_management/views/doctor_schedule_view.py`
- Page 2 runtime owner: `BTL.Nhóm6_Python/healthcare_management/views/doctor_management_views.py` (`DoctorPatientListView`)
- Page 3 runtime owner: `BTL.Nhóm6_Python/healthcare_management/views/doctor_examination_view.py`
- Page 4 runtime owner: `BTL.Nhóm6_Python/healthcare_management/views/doctor_patient_record_view.py`
- Page 5 runtime owner: `BTL.Nhóm6_Python/healthcare_management/views/doctor_management_views.py` (`PrescriptionView`)
- Page 6 runtime owner: `BTL.Nhóm6_Python/healthcare_management/views/dashboard_view.py` + `controllers/notification_controller.py` + `models/notification_model.py`
- Page 7 runtime owner: `BTL.Nhóm6_Python/healthcare_management/views/dashboard_view.py` + `controllers/settings_controller.py`

### Metis Review (gaps addressed)
- Đã khóa single source of truth cho từng màn đang bị trùng implementation.
- Đã chặn scope creep ở Notification bằng persisted feed tối thiểu, không xây event bus tổng quát.
- Đã chặn mơ hồ giữa Khám bệnh và Hồ sơ bệnh nhân bằng tách trách nhiệm màn.
- Đã bổ sung guardrail cho state transition appointment/exam/prescription.
- Đã chuẩn hóa hướng test: tests-after nhưng mỗi slice phải thêm regression test cụ thể ngay sau khi cắm logic.

## Work Objectives
### Core Objective
Biến toàn bộ Doctor journey đang chạy trong `DashboardView` thành luồng nghiệp vụ thật, không còn phụ thuộc dữ liệu tĩnh trên mounted path, đồng thời bảo toàn UI hiện có và giữ app luôn chạy được sau mỗi vertical slice.

### Deliverables
- Router Doctor mount đúng 8 màn thật, không trỏ nhầm sang mock/dead path.
- Dashboard thống kê thật, có unread badge, upcoming appointments, CTA điều hướng đúng.
- Lịch khám data-backed với filter, detail, state update, start exam, cancel, confirm.
- Danh sách bệnh nhân data-backed với search/filter/pagination/navigation.
- Workspace khám bệnh hỗ trợ load theo appointment/patient, lưu tạm, hoàn tất, validate, chuyển sang đơn thuốc.
- Hồ sơ bệnh nhân hiển thị dữ liệu thật: demographics, lịch sử khám, đơn thuốc cũ, lịch hẹn.
- Đơn thuốc data-backed, hỗ trợ create/view/edit/cancel trước phát thuốc.
- Notification persisted feed với read/unread, mark-all-read, target navigation, dashboard badge.
- Cài đặt bác sĩ lưu thật: profile, password, notification preferences, account/workflow-related settings hiện có, logout flow rõ ràng.
- Bộ test và smoke Doctor flow theo chuẩn `pytest`/`pytest-qt`.

### Definition of Done (verifiable conditions with commands)
- `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_dashboard_routing.py -q` pass.
- `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_schedule_flow.py -q` pass.
- `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_patient_list.py -q` pass.
- `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_examination_workflow.py -q` pass.
- `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_patient_profile.py -q` pass.
- `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_prescription_workflow.py -q` pass.
- `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_notifications.py -q` pass.
- `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_settings_integration.py -q` pass.
- `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_journey_smoke.py -q` pass.
- `python -m pytest -q` pass từ repo root.

### Must Have
- Giữ `DashboardView` là router Doctor runtime.
- Chỉ dùng dữ liệu thật trên mounted Doctor path.
- Mọi state `loading/empty/error` phải hiển thị tường minh.
- Mọi action click được phải có xử lý thật hoặc bị loại bỏ khỏi mounted path.
- Mọi form có validation trước khi ghi DB.
- Navigation giữa Dashboard → Schedule → Examination → Patient Profile → Prescriptions → Notifications → Settings chạy được qua code thật.
- Mọi thay đổi schema phải tối thiểu và bám đúng 3 nhu cầu: exam draft/finalize, prescription lifecycle, notification feed.

### Must NOT Have (guardrails, AI slop patterns, scope boundaries)
- Không redesign layout/sidebar/style hiện có.
- Không triển khai tính năng cho role khác ngoài phạm vi Doctor nếu không phải dependency trực tiếp.
- Không viết song song 2 implementation hoạt động cho cùng 1 mounted màn.
- Không để mock rows/mock notifications/mock schedule tồn tại trên mounted Doctor path sau khi hoàn tất.
- Không dựng workflow engine tổng quát, event bus tổng quát, hoặc refactor MVC toàn repo.
- Không sửa rộng patient/admin modules chỉ để “đẹp code”.

## Verification Strategy
> ZERO HUMAN INTERVENTION - all verification is agent-executed.
- Test decision: **tests-after** + `pytest` + `pytest-qt`.
- QA policy: Mỗi task phải thêm hoặc cập nhật test/regression tương ứng ngay sau khi cắm logic; UI verification dùng widget tests và smoke tests headless, không dùng kiểm tra mắt thường.
- Canonical test root: `BTL.Nhóm6_Python/tests/` với `BTL.Nhóm6_Python/pytest.ini`.
- Headless test command convention: dùng `QT_QPA_PLATFORM=offscreen` cho các test widget/smoke có khởi tạo PyQt app.
- Evidence: `.sisyphus/evidence/task-{N}-{slug}.{ext}`

## Execution Strategy
### Parallel Execution Waves
> Target: 5-8 tasks per wave. <3 per wave (except final) = under-splitting.
> Extract shared dependencies as Wave-1 tasks for max parallelism.

Wave 1: T1 Router/Test Harness, T2 Schema/Domain Extensions, T3 Dashboard Real Data

Wave 2: T4 Schedule, T5 Patient List, T6 Examination Workspace, T7 Patient Profile

Wave 3: T8 Prescriptions, T9 Notifications, T10 Settings + Journey Smoke

### Dependency Matrix (full, all tasks)
- T1 blocks T3-T10
- T2 blocks T4, T6, T8, T9, T10
- T3 depends on T1 and partially on T2 (notification badge counts)
- T4 depends on T1, T2
- T5 depends on T1
- T6 depends on T1, T2, T4, T5
- T7 depends on T1, T2, T5, T6
- T8 depends on T1, T2, T6, T7
- T9 depends on T1, T2, T4, T6, T8
- T10 depends on T1-T9

### Agent Dispatch Summary (wave → task count → categories)
- Wave 1 → 3 tasks → `business-logic`, `quick`
- Wave 2 → 4 tasks → `business-logic`, `unspecified-high`
- Wave 3 → 3 tasks → `business-logic`, `unspecified-high`, `writing`

## TODOs
> Implementation + Test = ONE task. Never separate.
> EVERY task MUST have: Agent Profile + Parallelization + QA Scenarios.

- [ ] 1. Chuẩn hóa router Doctor và harness kiểm thử

  **What to do**: Chuẩn hóa `DashboardView` làm router Doctor duy nhất, xác nhận mapping 8 page index là nguồn sự thật runtime, loại bỏ nhầm lẫn giữa mounted widget và dead-path widget trong plan triển khai. Chuẩn hóa điểm chạy test về `BTL.Nhóm6_Python/tests/`, thêm fixture/test route cho login→doctor→dashboard và page switching.
  **Must NOT do**: Không đổi UI layout/sidebar. Không refactor role router ngoài phạm vi Doctor. Không sửa business logic domain ở task này.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: task cần chốt contract runtime và test harness, ảnh hưởng toàn bộ downstream.
  - Skills: `[]` - Không cần skill ngoài.
  - Omitted: `['karpathy-guidelines']` - Đã được áp dụng ở cấp planning, executor chỉ cần bám plan.

  **Parallelization**: Can Parallel: NO | Wave 1 | Blocks: [2,3,4,5,6,7,8,9,10] | Blocked By: []

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/main_view.py` - `MainView._route_role_view()` đang mount `DashboardView` cho role doctor.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/dashboard_view.py` - `switch_page(index)` và `content_stack.addWidget(...)` là mapping runtime chuẩn.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/login_view.py` - `login()` tạo `MainView` sau auth thành công.
  - Test: `BTL.Nhóm6_Python/tests/test_appointment_rbac.py` - mẫu tổ chức pytest hiện có.
  - Test config: `BTL.Nhóm6_Python/pytest.ini` - cấu hình pytest chuẩn cần giữ làm canonical path.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_dashboard_routing.py -q` pass và xác nhận page index 0-7 mount đúng widget runtime.
  - [ ] `python -m pytest -q` không bị duplicate discovery gây fail do test config mới.
  - [ ] Login doctor mở đúng `DashboardView`, không mount sai màn legacy/web.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Doctor router mounts đúng 8 page
    Tool: Bash
    Steps: Chạy `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_dashboard_routing.py -q`
    Expected: Test pass; assertions xác nhận index 0-7 của `content_stack` map đúng Dashboard/Schedule/Patient List/Examination/Patient Profile/Prescriptions/Notifications/Settings
    Evidence: .sisyphus/evidence/task-1-doctor-router.txt

  Scenario: Sai role không vào Doctor dashboard
    Tool: Bash
    Steps: Chạy test negative case trong cùng file để login bằng role không phải doctor và kiểm tra không mount `DashboardView`
    Expected: Test pass; role khác không bị route nhầm vào Doctor dashboard
    Evidence: .sisyphus/evidence/task-1-doctor-router-error.txt
  ```

  **Commit**: YES | Message: `test(doctor): lock runtime routing and doctor dashboard harness` | Files: [`BTL.Nhóm6_Python/tests/test_doctor_dashboard_routing.py`, `BTL.Nhóm6_Python/pytest.ini`, any minimal fixture helpers]

- [ ] 2. Mở rộng schema và domain tối thiểu cho exam draft, prescription lifecycle, notifications

  **What to do**: Thiết kế và áp dụng thay đổi schema tối thiểu để hỗ trợ (1) medical record draft/finalized, (2) prescription status `draft/issued/dispensed/cancelled`, (3) notification persisted feed có read/unread + target navigation. Cập nhật model/controller tương ứng và seed/test data tối thiểu.
  **Must NOT do**: Không normalize lại toàn DB. Không thêm event bus tổng quát. Không thay đổi schema ngoài đúng 3 nhu cầu đã khóa.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: task là nền tảng domain + persistence cho các màn còn mock.
  - Skills: `[]` - Không cần skill ngoài.
  - Omitted: `['supabase', 'supabase-postgres-best-practices']` - DB hiện tại là MySQL local, không dùng Supabase.

  **Parallelization**: Can Parallel: NO | Wave 1 | Blocks: [4,6,8,9,10] | Blocked By: [1]

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/models/appointment_model.py` - mẫu query/state domain mạnh nhất hiện có.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/controllers/appointment_controller.py` - guard logic status và RBAC cần noi theo.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/models/medical_record_model.py` - nơi mở rộng draft/finalized.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/models/prescription_model.py` - nơi thêm lifecycle status và guard edit/cancel.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/controllers/settings_controller.py` + `models/settings_model.py` - mẫu persisted settings/read-write controller.
  - DB seed: `BTL.Nhóm6_Python/healthcare_management/database/init_db.sql` - nơi cập nhật schema/seed chuẩn.

  **Acceptance Criteria**:
  - [ ] `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_domain_contracts.py -q` pass.
  - [ ] Schema mới khởi tạo thành công bằng seed hiện có, không làm hỏng login/app startup.
  - [ ] Controller/model mới trả về contract ổn định cho exam draft/finalize, prescription status, notification feed.

  **QA Scenarios**:
  ```
  Scenario: Domain contracts hoạt động với schema mới
    Tool: Bash
    Steps: Chạy `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_domain_contracts.py -q`
    Expected: Test pass cho create/read/update của exam draft/finalize, prescription status transitions, notifications read/unread
    Evidence: .sisyphus/evidence/task-2-domain-contracts.txt

  Scenario: Transition không hợp lệ bị chặn
    Tool: Bash
    Steps: Chạy negative cases trong cùng file với finalize exam thiếu dữ liệu, edit prescription sau dispense, mark notification target không hợp lệ
    Expected: Test pass; các transition sai trả lỗi rõ ràng, không ghi DB sai trạng thái
    Evidence: .sisyphus/evidence/task-2-domain-contracts-error.txt
  ```

  **Commit**: YES | Message: `feat(doctor): add minimal domain persistence for exam prescription notifications` | Files: [`database/init_db.sql`, relevant models/controllers/tests]

- [ ] 3. Hoàn thiện Dashboard bác sĩ bằng dữ liệu thật

  **What to do**: Thay mọi KPI/card/list/timeline/notification badge trên dashboard bằng dữ liệu thật từ appointments, patients, prescriptions, notifications. Gắn đầy đủ action click: card thống kê, lịch hẹn hôm nay, upcoming appointments, notification entry, CTA “xem tất cả”. Bổ sung loading/empty/error state theo pattern hiện có.
  **Must NOT do**: Không đổi bố cục card/chart. Không thêm chỉ số ngoài yêu cầu issue #24. Không giữ mock appointment rows trên mounted dashboard.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: task chủ yếu là ghép dữ liệu thật + navigation cross-screen.
  - Skills: `[]`
  - Omitted: `['frontend-ui-ux']` - Không redesign UI.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: [10] | Blocked By: [1,2]

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/dashboard_view.py` - `_render_dashboard_page`, `_handle_appointment_action`, notification badge/header.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/patient_view.py:771-795, 985-993, 1025-1050` - state machine loading/error/empty.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/doctor_management_views.py:1950, 2133-2139` - reminder/empty banner doctor-side.
  - API/Type: appointment/patient/prescription counts từ controllers/models hiện có.

  **Acceptance Criteria**:
  - [ ] `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_dashboard_data.py -q` pass.
  - [ ] Dashboard hiển thị tổng số bệnh nhân, lịch hôm nay, số đơn thuốc, thông báo mới, lịch sắp tới từ dữ liệu thật.
  - [ ] Click vào card/lịch/notification điều hướng đúng page index tương ứng trong router Doctor.

  **QA Scenarios**:
  ```
  Scenario: Dashboard hiển thị số liệu thật và điều hướng đúng
    Tool: Bash
    Steps: Chạy `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_dashboard_data.py -q`
    Expected: Test pass; dashboard render từ real controllers, click card chuyển đúng page và payload liên quan
    Evidence: .sisyphus/evidence/task-3-dashboard.txt

  Scenario: Dashboard empty/error state
    Tool: Bash
    Steps: Chạy negative cases trong cùng file với doctor không có lịch hôm nay và case controller raise error
    Expected: Test pass; hiển thị empty state/error state rõ ràng, không crash và không fallback sang mock rows
    Evidence: .sisyphus/evidence/task-3-dashboard-error.txt
  ```

  **Commit**: YES | Message: `feat(doctor): wire dashboard to real doctor data` | Files: [`views/dashboard_view.py`, relevant controllers/tests]

- [ ] 4. Thay màn Lịch khám bằng implementation data-backed duy nhất

  **What to do**: Đưa `DoctorScheduleView` hoặc implementation tương đương data-backed lên mounted router page 1, hợp nhất filter ngày/trạng thái/dịch vụ/phòng, panel chi tiết appointment, start exam, view patient profile, edit/cancel/confirm. Loại bỏ dependence vào `_build_schedule_page()` tĩnh trên mounted path.
  **Must NOT do**: Không duy trì cả static schedule page và real schedule page cùng là runtime option. Không kéo thêm drag-drop/resync calendar ngoài scope issue.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: task cần đồng bộ UI runtime với AppointmentController/Model thật.
  - Skills: `[]`
  - Omitted: `['frontend-ui-ux']`

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: [6,9,10] | Blocked By: [1,2]

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/doctor_schedule_view.py` - action methods `_start_selected_exam`, `_view_selected_patient`, `_edit_selected_appointment`, `_cancel_selected_appointment`.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/controllers/appointment_controller.py` - confirm/start/cancel/update status.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/models/appointment_model.py` - list/query contract + joined fields.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/dashboard_view.py` - router page 1 currently static.

  **Acceptance Criteria**:
  - [ ] `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_schedule_flow.py -q` pass.
  - [ ] Doctor chỉ thấy appointment thuộc mình theo đúng RBAC và date/filter applied.
  - [ ] Start exam từ schedule chuyển đúng sang màn khám bệnh với appointment/patient context.

  **QA Scenarios**:
  ```
  Scenario: Filter lịch khám và bắt đầu khám
    Tool: Bash
    Steps: Chạy `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_schedule_flow.py -q`
    Expected: Test pass; filter theo ngày/trạng thái hoạt động, chọn appointment -> start exam mở đúng context
    Evidence: .sisyphus/evidence/task-4-schedule.txt

  Scenario: Appointment ngoài quyền hoặc transition sai bị chặn
    Tool: Bash
    Steps: Chạy negative cases với appointment của doctor khác, cancel/start từ trạng thái không hợp lệ
    Expected: Test pass; action bị từ chối với lỗi rõ ràng, UI không cập nhật giả
    Evidence: .sisyphus/evidence/task-4-schedule-error.txt
  ```

  **Commit**: YES | Message: `feat(doctor): mount real appointment schedule flow` | Files: [`views/dashboard_view.py`, `views/doctor_schedule_view.py`, appointment controllers/tests]

- [ ] 5. Hoàn thiện Danh sách bệnh nhân bằng dữ liệu thật và điều hướng hồ sơ

  **What to do**: Nối `DoctorPatientListView` với dữ liệu thật bệnh nhân, search theo tên/SĐT/mã BN, filter tab/status, pagination, panel chi tiết bên phải, action xem chi tiết và điều hướng sang hồ sơ bệnh nhân. Nếu có sort/filter UI sẵn thì cắm logic tương ứng.
  **Must NOT do**: Không mở rộng sang admin CRUD bệnh nhân ngoài phạm vi doctor-facing flow. Không thêm export/report mới nếu UI mounted path chưa có.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: task data-backed list/panel/navigation nhưng không đòi thay đổi schema lớn.
  - Skills: `[]`
  - Omitted: `['writing']`

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: [6,7,10] | Blocked By: [1]

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/doctor_management_views.py` - `DoctorPatientListView`.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/controllers/patient_controller.py` and `models/patient_model.py` - patient data contracts.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/doctor_management_views.py:153-180, 287-304` - form validation style.

  **Acceptance Criteria**:
  - [ ] `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_patient_list.py -q` pass.
  - [ ] Search/filter/pagination hoạt động trên dữ liệu thật.
  - [ ] Click row hoặc action view mở hồ sơ bệnh nhân đúng context.

  **QA Scenarios**:
  ```
  Scenario: Tìm kiếm và mở hồ sơ bệnh nhân
    Tool: Bash
    Steps: Chạy `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_patient_list.py -q`
    Expected: Test pass; search theo tên/SĐT/mã BN lọc đúng, click bệnh nhân mở page hồ sơ đúng patient_id
    Evidence: .sisyphus/evidence/task-5-patient-list.txt

  Scenario: Không có dữ liệu hoặc query lỗi
    Tool: Bash
    Steps: Chạy negative cases với zero results và model/controller exception
    Expected: Test pass; empty state/error state rõ ràng, không hiển thị dòng placeholder giả
    Evidence: .sisyphus/evidence/task-5-patient-list-error.txt
  ```

  **Commit**: YES | Message: `feat(doctor): complete real patient list flow` | Files: [`views/doctor_management_views.py`, patient controllers/tests]

- [ ] 6. Tạo workspace Khám bệnh thật với lưu tạm và hoàn tất

  **What to do**: Tạo hoặc mount màn khám bệnh riêng cho page 3, load context từ appointment/patient, nhập lý do khám/triệu chứng/chẩn đoán/kết luận/hướng điều trị/ghi chú, validate trước lưu, hỗ trợ lưu tạm draft và finalize, thông báo kết quả, cập nhật appointment status và mở luồng tạo đơn thuốc khi phù hợp.
  **Must NOT do**: Không dùng `DoctorPatientRecordView` tĩnh làm màn khám bệnh chính. Không cho finalize nếu thiếu trường bắt buộc. Không ghi DB trực tiếp trong view nếu đã có controller/model phù hợp.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: task là heart of workflow Doctor, có state transition và persistence.
  - Skills: `[]`
  - Omitted: `['frontend-ui-ux']`

  **Parallelization**: Can Parallel: NO | Wave 2 | Blocks: [7,8,9,10] | Blocked By: [1,2,4,5]

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/doctor_management_views.py` - `MedicalRecordView`, `MedicalRecordDialog`, `PrescriptionDialog`.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/controllers/medical_record_controller.py` + `models/medical_record_model.py`.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/controllers/appointment_controller.py` - transition appointment khi bắt đầu/hoàn tất.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/doctor_management_views.py:406-420, 481-502` - validation patterns.

  **Acceptance Criteria**:
  - [ ] `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_examination_workflow.py -q` pass.
  - [ ] Có thể mở ca khám từ appointment context, lưu tạm, mở lại, hoàn tất và cập nhật status hợp lệ.
  - [ ] Finalize fail nếu thiếu dữ liệu bắt buộc; success thì phát notification/refresh data liên quan.

  **QA Scenarios**:
  ```
  Scenario: Lưu tạm rồi hoàn tất ca khám
    Tool: Bash
    Steps: Chạy `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_examination_workflow.py -q`
    Expected: Test pass; exam draft lưu được, load lại đúng dữ liệu, finalize chuyển appointment sang completed theo rule đã khóa
    Evidence: .sisyphus/evidence/task-6-examination.txt

  Scenario: Finalize thiếu chẩn đoán/kết luận bị chặn
    Tool: Bash
    Steps: Chạy negative cases với form thiếu trường bắt buộc hoặc appointment không hợp lệ
    Expected: Test pass; validation/message xuất hiện rõ ràng, DB không ghi finalized record sai
    Evidence: .sisyphus/evidence/task-6-examination-error.txt
  ```

  **Commit**: YES | Message: `feat(doctor): implement examination draft and finalize workflow` | Files: [`BTL.Nhóm6_Python/healthcare_management/views/doctor_examination_view.py`, `BTL.Nhóm6_Python/healthcare_management/controllers/medical_record_controller.py`, `BTL.Nhóm6_Python/healthcare_management/models/medical_record_model.py`, tests]

- [ ] 7. Hoàn thiện Hồ sơ bệnh nhân thành màn đọc dữ liệu thật và action điều hướng

  **What to do**: Tách page 4 thành màn hồ sơ bệnh nhân đúng nghĩa: demographics, bệnh sử, lịch sử khám, kết quả liên quan, đơn thuốc cũ, lịch hẹn. Cắm các tab/button/link, mở chi tiết lần khám, điều hướng sang khám bệnh hoặc tạo đơn thuốc khi phù hợp nhưng không nhập trực tiếp logic khám tại đây.
  **Must NOT do**: Không để page 4 tiếp tục trùng trách nhiệm với page 3. Không biến hồ sơ bệnh nhân thành chỗ edit khám chính.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: task cần gom dữ liệu read-model thật từ nhiều domain và navigation chính xác.
  - Skills: `[]`
  - Omitted: `['writing']`

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: [8,10] | Blocked By: [1,2,5,6]

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/doctor_patient_record_view.py` - UI shell/tab layout hiện có.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/models/medical_record_model.py` - lịch sử khám.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/models/prescription_model.py` - đơn thuốc theo patient/record.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/models/appointment_model.py` - lịch hẹn liên quan.

  **Acceptance Criteria**:
  - [ ] `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_patient_profile.py -q` pass.
  - [ ] Hồ sơ hiển thị dữ liệu thật cho patient, empty state đúng khi chưa có lịch sử.
  - [ ] Các tab/action mở đúng dữ liệu chi tiết hoặc điều hướng đúng page workflow.

  **QA Scenarios**:
  ```
  Scenario: Hồ sơ bệnh nhân có lịch sử thật
    Tool: Bash
    Steps: Chạy `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_patient_profile.py -q`
    Expected: Test pass; demographics/history/prescriptions/appointments hiển thị đúng patient_id và action đi đúng page liên quan
    Evidence: .sisyphus/evidence/task-7-patient-profile.txt

  Scenario: Bệnh nhân mới chưa có lịch sử
    Tool: Bash
    Steps: Chạy negative cases với patient không có medical record/prescription/appointment history
    Expected: Test pass; tab liên quan hiển thị empty state rõ ràng, không crash và không hiển thị mock data
    Evidence: .sisyphus/evidence/task-7-patient-profile-error.txt
  ```

  **Commit**: YES | Message: `feat(doctor): complete patient profile read model` | Files: [`views/doctor_patient_record_view.py`, related controllers/models/tests]

- [ ] 8. Hoàn thiện Đơn thuốc của tôi bằng dữ liệu thật và lifecycle trước phát thuốc

  **What to do**: Thay `PrescriptionView` hardcoded rows bằng dữ liệu thật từ prescription domain, hỗ trợ danh sách, xem chi tiết, tạo đơn mới từ context khám bệnh nếu UI có, sửa/hủy trước khi phát thuốc, filter/search theo bệnh nhân/ngày/trạng thái, và block edit/cancel sau `dispensed`.
  **Must NOT do**: Không suy diễn status từ appointment nếu đã có prescription status riêng. Không cho sửa/hủy sau phát thuốc. Không giữ bảng mock rows trên mounted path.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: task có domain rule rõ và phụ thuộc exam workflow + schema mới.
  - Skills: `[]`
  - Omitted: `['frontend-ui-ux']`

  **Parallelization**: Can Parallel: NO | Wave 3 | Blocks: [9,10] | Blocked By: [1,2,6,7]

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/doctor_management_views.py` - `PrescriptionView`.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/controllers/prescription_controller.py` + `models/prescription_model.py`.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/models/medicine_model.py` - inventory/medicine validation nếu đã có.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/doctor_management_views.py` action detail/print hooks.

  **Acceptance Criteria**:
  - [ ] `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_prescription_workflow.py -q` pass.
  - [ ] Danh sách đơn thuốc lấy từ DB thật, filter/search chạy được.
  - [ ] Edit/cancel chỉ được trước `dispensed`; sau đó phải bị chặn với message rõ ràng.

  **QA Scenarios**:
  ```
  Scenario: Tạo/xem/sửa đơn trước phát thuốc
    Tool: Bash
    Steps: Chạy `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_prescription_workflow.py -q`
    Expected: Test pass; prescription list lấy real data, create/edit/cancel trước dispense hoạt động đúng lifecycle
    Evidence: .sisyphus/evidence/task-8-prescriptions.txt

  Scenario: Chặn sửa/hủy sau phát thuốc hoặc dữ liệu thuốc không hợp lệ
    Tool: Bash
    Steps: Chạy negative cases với prescription đã `dispensed`, quantity invalid, medicine thiếu
    Expected: Test pass; action bị chặn với lỗi rõ ràng, DB không ghi thay đổi sai
    Evidence: .sisyphus/evidence/task-8-prescriptions-error.txt
  ```

  **Commit**: YES | Message: `feat(doctor): replace mock prescription list with real lifecycle` | Files: [`views/doctor_management_views.py`, prescription models/controllers/tests]

- [ ] 9. Xây notification feed persisted cho Doctor và nối dashboard badge

  **What to do**: Tạo `NotificationModel/Controller` tối thiểu hoặc lớp tương đương, persist thông báo với read/unread, mark-as-read, mark-all-read, delete nếu UI mounted path có, và target navigation sang lịch khám/hồ sơ bệnh nhân/đơn thuốc. Cắm unread badge vào dashboard/header.
  **Must NOT do**: Không để `_build_doctor_notification_mock_data()` tồn tại trên mounted path. Không xây realtime/WebSocket nếu không bắt buộc cho issue scope.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: task đòi persistence + UI feed + cross-screen navigation.
  - Skills: `[]`
  - Omitted: `['frontend-ui-ux']`

  **Parallelization**: Can Parallel: NO | Wave 3 | Blocks: [10] | Blocked By: [1,2,4,6,8]

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/dashboard_view.py` - notification center page + badge/header.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/doctor_patient_record_view.py:170-189` - notification badge UI style.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/controllers/settings_controller.py` - notification preferences persistence.
  - Contract target: page navigation indices trong `DashboardView`.

  **Acceptance Criteria**:
  - [ ] `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_notifications.py -q` pass.
  - [ ] Feed không còn dùng mock data trên mounted path.
  - [ ] Mark read/mark all read cập nhật persisted state và badge unread đúng.

  **QA Scenarios**:
  ```
  Scenario: Notification feed persisted và điều hướng đúng target
    Tool: Bash
    Steps: Chạy `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_notifications.py -q`
    Expected: Test pass; notification render theo persisted data, click target mở đúng page/context, unread badge cập nhật đúng
    Evidence: .sisyphus/evidence/task-9-notifications.txt

  Scenario: Feed rỗng hoặc target lỗi
    Tool: Bash
    Steps: Chạy negative cases với zero notifications, malformed target, repeated mark-read
    Expected: Test pass; empty state rõ ràng, app không crash, idempotent mark-read hoạt động đúng
    Evidence: .sisyphus/evidence/task-9-notifications-error.txt
  ```

  **Commit**: YES | Message: `feat(doctor): add persisted notification feed and badge` | Files: [`BTL.Nhóm6_Python/healthcare_management/views/dashboard_view.py`, `BTL.Nhóm6_Python/healthcare_management/controllers/notification_controller.py`, `BTL.Nhóm6_Python/healthcare_management/models/notification_model.py`, tests]

- [ ] 10. Hoàn thiện Cài đặt và smoke toàn bộ Doctor journey

  **What to do**: Rà và hoàn thiện toàn bộ mounted settings sections đang có UI: profile update, change password, notification preferences, account/account-related settings, logout flow, avatar/update messaging, save failure retention. Sau đó thêm smoke test cho full Doctor journey từ login qua 7 chặng chính, đảm bảo không còn hard-coded data trên mounted path.
  **Must NOT do**: Không thêm cài đặt mới ngoài UI hiện có. Không mở rộng logout thành auth subsystem lớn. Không để save lỗi làm mất dữ liệu form chưa lưu.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: task kết hợp persistence polish + regression + end-to-end journey verification.
  - Skills: `[]`
  - Omitted: `['writing']`

  **Parallelization**: Can Parallel: NO | Wave 3 | Blocks: [Final Verification Wave] | Blocked By: [1,2,3,4,5,6,7,8,9]

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/dashboard_view.py` - `_build_settings_page`, `_load_settings_data`, `_save_settings_personal_info`, `_open_change_password_dialog`, `_update_notification_setting`, `_handle_settings_nav_action`.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/controllers/settings_controller.py` + `models/settings_model.py`.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/controllers/auth_controller.py` + `views/login_view.py` - login/auth flow.
  - Router path: `views/main_view.py`, `views/dashboard_view.py`.

  **Acceptance Criteria**:
  - [ ] `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_settings_integration.py -q` pass.
  - [ ] `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_journey_smoke.py -q` pass.
  - [ ] `python -m pytest -q` pass toàn repo sau khi hoàn thiện 8 issue.

  **QA Scenarios**:
  ```
  Scenario: Settings persist và full doctor journey chạy xuyên màn
    Tool: Bash
    Steps: Chạy `python -m pytest BTL.Nhóm6_Python/tests/test_doctor_settings_integration.py -q && python -m pytest BTL.Nhóm6_Python/tests/test_doctor_journey_smoke.py -q`
    Expected: Test pass; profile/settings lưu đúng, notification preferences round-trip, login -> dashboard -> schedule -> exam -> patient profile -> prescriptions -> notifications -> settings chạy được không phụ thuộc mock data
    Evidence: .sisyphus/evidence/task-10-settings-journey.txt

  Scenario: Save settings thất bại hoặc navigation journey gặp dữ liệu thiếu
    Tool: Bash
    Steps: Chạy negative cases với save settings fail, password invalid, một màn không có dữ liệu domain
    Expected: Test pass; form giữ lại dữ liệu chưa lưu, error state rõ ràng, journey xử lý empty state thay vì crash
    Evidence: .sisyphus/evidence/task-10-settings-journey-error.txt
  ```

  **Commit**: YES | Message: `feat(doctor): finalize settings and doctor end-to-end journey` | Files: [`views/dashboard_view.py`, settings/auth/tests, smoke tests]

## Final Verification Wave (MANDATORY — after ALL implementation tasks)
> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.
> **Do NOT auto-proceed after verification. Wait for user's explicit approval before marking work complete.**
> **Never mark F1-F4 as checked before getting user's okay.** Rejection or user feedback -> fix -> re-run -> present again -> wait for okay.
- [ ] F1. Plan Compliance Audit — oracle
- [ ] F2. Code Quality Review — unspecified-high
- [ ] F3. Real Manual QA — unspecified-high (+ playwright if UI)
- [ ] F4. Scope Fidelity Check — deep

## Commit Strategy
- Một commit dọc cho mỗi task T1-T10; tuyệt đối để app runnable sau từng commit.
- Schema change và migration nằm trong commit đúng domain đầu tiên cần nó, không gom một cục cuối cùng.
- Sau T10 chạy full regression trước khi vào Final Verification Wave.

## Success Criteria
- Mọi Doctor screen đang mount trong `DashboardView` dùng dữ liệu thật hoặc persisted state đúng quyết định đã khóa.
- Không còn hành vi click chết trên mounted path.
- Không còn duplicate mounted flow giữa schedule/exam/profile gây mơ hồ nghiệp vụ.
- Full Doctor journey chạy qua test + smoke mà không phụ thuộc mock rows/feed.
