# Kế hoạch triển khai màn hình Tiếp nhận bệnh nhân (Staff)

## TL;DR
> **Summary**: Nâng cấp màn hình "Tiếp nhận bệnh nhân" trong `StaffDashboardView` theo đúng UI spec, đồng bộ với luồng lưu DB hiện tại (MVC + `database/db.py`) và cập nhật hàng chờ khám nội bộ staff (3B).
> **Deliverables**:
> - UI/UX đầy đủ 4 khu vực + sidebar/topbar đúng đặc tả
> - Luồng tìm kiếm, toggle mode, validate/lưu, reset, xác nhận tiếp nhận
> - Mở rộng schema + seed dữ liệu phục vụ CCCD/email/nghề nghiệp/ghi chú + queue chờ khám
> - Bằng chứng QA agent-executed cho từng task
> **Effort**: Large
> **Parallel**: YES - 4 waves
> **Critical Path**: T1 (schema) → T2/T3 (model/controller) → T4/T5/T6 (UI + behaviors) → T8 (confirm+queue) → Verification Wave

## Context
### Original Request
- Thiết kế và code màn hình "Tiếp nhận bệnh nhân" (nhân viên) bằng PyQt6 với bố cục/sidebar/topbar/main 2 cột và style chi tiết (màu, spacing, typography, badge, button).
- Bắt buộc có các hành vi: tra cứu, mode bệnh nhân mới/vãng lai, lưu có validate, xóa form, xác nhận tiếp nhận có dialog + cập nhật trạng thái + thông báo.

### Interview Summary
- Lưu dữ liệu: **theo kiểu DB hiện tại trong codebase**.
- DB đã có nhưng chưa connect hoàn chỉnh cho nhu cầu mới: cần bổ sung migration/seed theo convention hiện tại.
- "Bệnh nhân vãng lai": **giữ đầy đủ field**.
- Xác nhận tiếp nhận chọn **3B**: đồng bộ sang danh sách chờ khám nội bộ staff.
- Scope khóa: **màn của nhân viên**.

### Metis Review (gaps addressed)
- Bổ sung guardrail chống duplicate BN theo CCCD/phone.
- Chốt mapping field UI → DB column rõ ràng.
- Chốt state machine confirm intake → waiting queue.
- Chốt acceptance criteria dạng binary, không phụ thuộc người kiểm thử.

## Work Objectives
### Core Objective
Triển khai đầy đủ màn hình tiếp nhận bệnh nhân cho nhân viên trong `StaffDashboardView`, đúng thiết kế yêu cầu và tương thích tuyệt đối với kiến trúc MVC + DB hiện tại của dự án.

### Deliverables
- Trang intake mới (hoặc refactor intake hiện hữu) với sidebar active state, topbar, 2 cột và card section 1→4.
- DB schema/migration/seed phục vụ dữ liệu intake (CCCD, email, nghề nghiệp, ghi chú, queue chờ khám nếu thiếu).
- Model/controller methods phục vụ lookup, create/update patient, confirm intake + queue sync.
- Luồng UI events hoàn chỉnh: search, toggle mode, save/reset, confirm dialog + success feedback.

### Definition of Done (verifiable conditions with commands)
- Chạy app mở được trang staff intake không lỗi runtime.
- Lookup theo phone/CCCD trả đúng nhánh: có hồ sơ / không có hồ sơ.
- Save bệnh nhân hợp lệ ghi DB thành công; dữ liệu truy vấn lại được.
- Confirm intake tạo/cập nhật trạng thái chờ khám và hiển thị thông báo thành công.
- Manual QA script toàn bộ scenarios chạy pass và có evidence file.

### Must Have
- Bám pattern hiện có tại `views/staff_dashboard_view.py` (menu, content stack, section card, inline QSS).
- Dùng controller/model pattern hiện có (`controllers/*`, `models/*`, `database/db.py`).
- Không tạo luồng routing mới ngoài staff dashboard hiện tại.
- Triển khai validation có message rõ ràng cho field bắt buộc và dữ liệu sai định dạng.

### Must NOT Have (guardrails, AI slop patterns, scope boundaries)
- Không đổi kiến trúc app tổng thể (không thêm framework UI mới).
- Không thêm persistence style mới tách khỏi `database/db.py`.
- Không mở rộng nghiệp vụ sang role khác (doctor/admin/patient).
- Không hardcode logic mơ hồ; mọi status transition phải explicit.

## Verification Strategy
> ZERO HUMAN INTERVENTION - all verification is agent-executed.
- Test decision: **none (automated test infra absent)** + manual agent-executed scenarios.
- QA policy: Mỗi task implementation đều kèm 2 scenario (happy + failure/edge).
- Evidence: `.sisyphus/evidence/task-{N}-{slug}.{ext}`

## Execution Strategy
### Parallel Execution Waves
> Target: 5-8 tasks per wave. Shared dependencies được bóc tách vào Wave 1.

Wave 1: nền dữ liệu + contracts (T1-T3)
Wave 2: layout/screen composition (T4-T5)
Wave 3: event behaviors + persistence wiring (T6-T8)
Wave 4: polish + regression + doc checklist (T9-T10)

### Dependency Matrix (full, all tasks)
- T1 blocks: T2, T3, T6, T7, T8
- T2 blocks: T6, T7
- T3 blocks: T6, T8
- T4 blocks: T5, T6
- T5 blocks: T6, T8
- T6 blocks: T8, T9
- T7 blocks: T9
- T8 blocks: T9, T10
- T9 blocks: Final Verification Wave
- T10 blocks: Final Verification Wave

### Agent Dispatch Summary (wave → task count → categories)
- Wave 1 → 3 tasks → unspecified-high, quick
- Wave 2 → 2 tasks → visual-engineering
- Wave 3 → 3 tasks → unspecified-high
- Wave 4 → 2 tasks → unspecified-low, writing

## TODOs
> Implementation + Test = ONE task. Never separate.
> EVERY task MUST have: Agent Profile + Parallelization + QA Scenarios.

- [x] 1. Chuẩn hóa schema intake + hàng chờ khám theo DB style hiện tại

  **What to do**: Cập nhật migration/schema theo convention hiện có để hỗ trợ đầy đủ field intake staff: CCCD/CMND, email, nghề nghiệp, ghi chú, loại bệnh nhân (mới/vãng lai), metadata tiếp nhận và trạng thái hàng chờ. Nếu cột/bảng đã tồn tại thì chỉ bổ sung thiếu; tránh phá dữ liệu cũ.
  **Must NOT do**: Không thay đổi driver/persistence abstraction; không drop table hiện hữu; không đổi kiểu query placeholder hiện tại.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: cần xử lý schema evolution an toàn và tương thích dữ liệu cũ.
  - Skills: `[]` - không có skill đặc thù bắt buộc.
  - Omitted: [`/refactor`] - không cần tái cấu trúc toàn hệ thống.

  **Parallelization**: Can Parallel: NO | Wave 1 | Blocks: [2,3,6,7,8] | Blocked By: []

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/database/migrate.py` - pattern create table IF OBJECT_ID.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/database/db.py` - execute/fetch pattern và commit/rollback.
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/models/patient_model.py` - cột Patients hiện có.
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/models/appointment_model.py` - trạng thái lịch hẹn và note.
  - External: `README.md` - môi trường DB MySQL qua docker compose.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Script migration chạy không lỗi trên DB mới.
  - [ ] Schema sau migration chứa đầy đủ cột phục vụ intake đã mapping.
  - [ ] Không làm hỏng các bảng hiện tại (Users/Patients/Doctors/Appointments).

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Migration happy path
    Tool: Bash
    Steps: Chạy migrate/init theo entrypoint hiện có; query thông tin schema các bảng liên quan.
    Expected: Cột/bảng mới xuất hiện đúng tên/kiểu; command exit code thành công.
    Evidence: .sisyphus/evidence/task-1-schema-migration.txt

  Scenario: Backward compatibility
    Tool: Bash
    Steps: Thực thi một query đọc dữ liệu bảng cũ (Patients/Appointments) sau migration.
    Expected: Query thành công, không lỗi thiếu cột/khóa.
    Evidence: .sisyphus/evidence/task-1-schema-compatibility.txt
  ```

  **Commit**: YES | Message: `feat(db): extend intake schema for staff reception` | Files: [`database/migrate.py`, `database/init_db.sql`]

- [x] 2. Bổ sung PatientModel/Controller cho lookup ưu tiên CCCD → phone và lưu đủ field

  **What to do**: Mở rộng model/controller bệnh nhân để hỗ trợ tìm theo CCCD + phone deterministic, create/update đầy đủ field màn intake (name,dob,gender,phone,cccd,address,email,occupation,note,patient_type). Chuẩn hóa rule duplicate rõ ràng.
  **Must NOT do**: Không để fallback mơ hồ gây tạo duplicate âm thầm; không bypass controller gọi SQL trực tiếp từ view.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: logic nghiệp vụ và data integrity.
  - Skills: `[]`
  - Omitted: [`/frontend-ui-ux`] - không tập trung UI.

  **Parallelization**: Can Parallel: PARTIAL | Wave 1 | Blocks: [6,7] | Blocked By: [1]

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `controllers/patient_controller.py` - facade methods hiện hữu và ghi chú thiếu CCCD.
  - API/Type: `models/patient_model.py` - static methods get/create/update/delete hiện tại.
  - Pattern: `database/db.py` - `fetch_one`, `execute` và placeholder `?`.
  - Pattern: `controllers/appointment_controller.py` - kiểu trả về `{status,message}` cho validation.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Có method lookup theo CCCD/phone trả kết quả deterministic (ưu tiên CCCD).
  - [ ] Create/update từ controller lưu đủ trường intake vào DB.
  - [ ] Case duplicate phát hiện được và trả thông báo lỗi/nhắc hợp lệ.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Lookup by CCCD then phone
    Tool: Bash
    Steps: Seed 2 bệnh nhân; gọi layer controller/model qua script nhỏ để lookup CCCD và phone.
    Expected: Kết quả đúng patient tương ứng, không lẫn record.
    Evidence: .sisyphus/evidence/task-2-lookup-priority.txt

  Scenario: Duplicate constraint/handling
    Tool: Bash
    Steps: Tạo record trùng CCCD hoặc phone theo rule; chạy create/update.
    Expected: Hệ thống từ chối hoặc trả trạng thái lỗi đúng thông điệp đã định nghĩa.
    Evidence: .sisyphus/evidence/task-2-duplicate-handling.txt
  ```

  **Commit**: YES | Message: `feat(patient): support cccd-first lookup and full intake fields` | Files: [`models/patient_model.py`, `controllers/patient_controller.py`]

- [x] 3. Bổ sung contracts cho intake queue/appointment check-in phía staff

  **What to do**: Mở rộng model/controller lịch hẹn để hỗ trợ action check-in từ màn staff: nhận patient + service + doctor + thời gian tiếp nhận, cập nhật trạng thái sang hàng chờ (`confirmed`/`in_progress` theo rule đã chốt) và lưu note/lý do khám.
  **Must NOT do**: Không hardcode trạng thái trong view; không tạo logic trùng lặp ở nhiều nơi.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: state transition + consistency.
  - Skills: `[]`
  - Omitted: [`/ai-slop-remover`] - chưa phải pha cleanup.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: [6,8] | Blocked By: [1]

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `controllers/appointment_controller.py` - validation + status set.
  - API/Type: `models/appointment_model.py` - create/get_by_patient/has_conflict/update_status.
  - Pattern: `views/staff_dashboard_view.py` - biến shared_selected_* và intake_selected_*.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Có API controller rõ ràng cho confirm intake/check-in từ màn staff.
  - [ ] Status transition nhất quán, query lại thấy appointment vào nhóm chờ khám.
  - [ ] Lưu được lý do khám/note theo input màn intake.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Confirm intake success
    Tool: Bash
    Steps: Tạo dữ liệu patient/doctor/service/appointment, gọi API confirm intake.
    Expected: Trạng thái appointment đổi đúng và dữ liệu note/lý do được lưu.
    Evidence: .sisyphus/evidence/task-3-checkin-success.txt

  Scenario: Invalid transition or missing doctor/service
    Tool: Bash
    Steps: Gọi confirm với thiếu doctor hoặc trạng thái không hợp lệ.
    Expected: Trả lỗi có message rõ ràng, không commit dữ liệu sai.
    Evidence: .sisyphus/evidence/task-3-checkin-failure.txt
  ```

  **Commit**: YES | Message: `feat(appointment): add staff check-in transition contract` | Files: [`models/appointment_model.py`, `controllers/appointment_controller.py`]

- [x] 4. Refactor layout màn intake trong StaffDashboardView đúng spec 2 cột + topbar

  **What to do**: Thiết kế lại `_build_patient_intake_page` theo đặc tả: sidebar active state, topbar (title+breadcrumb+notification/avatar), main content 2 cột tỉ lệ ~55/43, section 1→4 card styling đúng màu/radius/spacing.
  **Must NOT do**: Không phá navigation stack hiện tại; không tạo top-level window mới.

  **Recommended Agent Profile**:
  - Category: `visual-engineering` - Reason: yêu cầu pixel-approx UI chi tiết.
  - Skills: `[]`
  - Omitted: [`/git-master`] - không phải tác vụ git.

  **Parallelization**: Can Parallel: NO | Wave 2 | Blocks: [5,6] | Blocked By: [4 foundation from existing code only]

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `views/staff_dashboard_view.py` - sidebar/menu item active state hiện tại.
  - Pattern: `views/staff_dashboard_view.py` - `_build_section_card` style card reuse.
  - Pattern: `views/dashboard_view.py` - status card/table spacing conventions.
  - External: User UI spec in conversation (primary `#1A9B6C`, borders, badges).

  **Acceptance Criteria** (agent-executable only):
  - [ ] Trang intake render đầy đủ 4 section và topbar đúng cấu trúc.
  - [ ] Sidebar item "Tiếp nhận bệnh nhân" hiển thị trạng thái ACTIVE đúng style.
  - [ ] Không có lỗi layout overflow khi resize cửa sổ tiêu chuẩn desktop.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Visual structure check
    Tool: Playwright
    Steps: Mở app, đăng nhập staff, chuyển đến menu Tiếp nhận bệnh nhân, chụp ảnh toàn trang.
    Expected: Có sidebar + topbar + 2 cột + section 1-4 theo bố cục đã định.
    Evidence: .sisyphus/evidence/task-4-layout.png

  Scenario: Resize edge case
    Tool: Playwright
    Steps: Resize cửa sổ xuống mức nhỏ hơn chuẩn, quan sát card/input/button.
    Expected: Không chồng lấp text/controls nghiêm trọng; vẫn thao tác được.
    Evidence: .sisyphus/evidence/task-4-resize-edge.png
  ```

  **Commit**: YES | Message: `feat(staff-intake): rebuild intake layout per design spec` | Files: [`views/staff_dashboard_view.py`]

- [x] 5. Dựng đầy đủ control fields + state containers cho section 1/2/3/4

  **What to do**: Thêm/chuẩn hóa tất cả widget theo spec: search input+button+result card+divider OR; form full fields + required markers + radio mode; tiếp nhận date/time/service/doctor/reason; summary card + info badge + confirm CTA.
  **Must NOT do**: Không cột cứng dữ liệu tĩnh ở summary ngoài sample default; không bỏ required marker với field bắt buộc.

  **Recommended Agent Profile**:
  - Category: `visual-engineering` - Reason: cấu trúc form/phân cấp UI chi tiết.
  - Skills: `[]`
  - Omitted: [`/playwright`] - chỉ dùng ở QA step, không dùng để implement.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: [6,8] | Blocked By: [4]

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `views/staff_dashboard_view.py` - các biến `self.intake_*` đang dùng.
  - Pattern: `views/doctor_management_views.py` - form label/helptext style nhất quán.
  - API/Type: `controllers/doctor_controller.py`, `controllers/service_controller.py` - data source combobox.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Tất cả control theo spec đều tồn tại và focus/tab được.
  - [ ] Combobox dịch vụ/bác sĩ load được dữ liệu từ controller (hoặc fallback có thông báo).
  - [ ] Summary card cập nhật khi state thay đổi.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Controls availability
    Tool: Playwright
    Steps: Điều hướng màn intake; kiểm tra tồn tại từng control theo nhãn.
    Expected: 100% field/button/label xuất hiện đúng section.
    Evidence: .sisyphus/evidence/task-5-controls-check.txt

  Scenario: Empty source fallback
    Tool: Playwright
    Steps: Trường hợp danh sách dịch vụ/bác sĩ rỗng, mở combobox.
    Expected: Hiển thị placeholder/fallback message an toàn, không crash.
    Evidence: .sisyphus/evidence/task-5-empty-source.txt
  ```

  **Commit**: YES | Message: `feat(staff-intake): add full intake controls and state bindings` | Files: [`views/staff_dashboard_view.py`]

- [x] 6. Hoàn thiện hành vi tra cứu + toggle mode + validate/lưu bệnh nhân

  **What to do**: Cập nhật `_handle_intake_lookup`, radio mode handlers và save handler để: (a) search show result card, (b) toggle new/walk-in vẫn giữ full fields nhưng điều chỉnh rules, (c) validate bắt buộc + định dạng, (d) create/update DB đúng model/controller.
  **Must NOT do**: Không validate lỏng lẻo; không ghi trực tiếp DB trong view; không để message lỗi mơ hồ.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: UI-event + business validation.
  - Skills: `[]`
  - Omitted: [`/frontend-ui-ux`] - trọng tâm logic hơn mỹ thuật.

  **Parallelization**: Can Parallel: NO | Wave 3 | Blocks: [8,9] | Blocked By: [1,2,4,5]

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `views/staff_dashboard_view.py` - `_handle_intake_lookup` và feedback label hiện tại.
  - Pattern: `controllers/patient_controller.py` - find/create/update pattern.
  - API/Type: `models/patient_model.py` - cột lưu và query.
  - Pattern: `controllers/appointment_controller.py` - thông điệp validation dạng dict.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Nhấn "Tìm kiếm" hiển thị result card đúng nhánh có/không có hồ sơ.
  - [ ] Radio mode đổi được behavior rule mà không mất field rendering đầy đủ.
  - [ ] "Lưu thông tin" validate đúng, lưu DB thành công, phản hồi thành công/lỗi rõ ràng.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Search + save success
    Tool: Playwright
    Steps: Nhập CCCD/phone mẫu, search; nếu không có thì nhập form hợp lệ và lưu.
    Expected: Có feedback success và query lại thấy bản ghi trong DB.
    Evidence: .sisyphus/evidence/task-6-save-success.txt

  Scenario: Validation failure
    Tool: Playwright
    Steps: Bỏ trống field bắt buộc hoặc nhập phone/email sai định dạng, nhấn lưu.
    Expected: Không lưu DB; hiển thị lỗi đúng vị trí/thông điệp.
    Evidence: .sisyphus/evidence/task-6-validation-error.png
  ```

  **Commit**: YES | Message: `feat(staff-intake): implement lookup, mode toggle, validation and save flow` | Files: [`views/staff_dashboard_view.py`, `controllers/patient_controller.py`, `models/patient_model.py`]

- [x] 7. Triển khai hành vi "Xóa thông tin" reset toàn bộ form + state liên quan

  **What to do**: Thêm handler reset để đưa toàn bộ form/state/summaries về mặc định ban đầu: inputs trống, date/time default, selected patient/appointment clear, feedback reset an toàn.
  **Must NOT do**: Không giữ state rác (`shared_selected_*`) sau reset; không reset nhầm navigation context.

  **Recommended Agent Profile**:
  - Category: `quick` - Reason: thay đổi scoped, rõ ràng.
  - Skills: `[]`
  - Omitted: [`/refactor`] - không cần mở rộng.

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: [9] | Blocked By: [1,2,5]

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `views/staff_dashboard_view.py` - trạng thái intake tại `__init__` và các `self.intake_*` widgets.
  - Pattern: `views/staff_dashboard_view.py` - feedback update method `_set_intake_feedback`.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Nút xóa reset 100% field + summary + state selection.
  - [ ] Sau reset, thao tác nhập/lưu mới hoạt động bình thường.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Full reset
    Tool: Playwright
    Steps: Điền form + chọn data + search, nhấn "Xóa thông tin".
    Expected: Tất cả field/state quay về mặc định ban đầu.
    Evidence: .sisyphus/evidence/task-7-reset-before-after.png

  Scenario: Reset then save
    Tool: Playwright
    Steps: Reset xong nhập lại dữ liệu hợp lệ và lưu.
    Expected: Save thành công, chứng minh reset không phá flow.
    Evidence: .sisyphus/evidence/task-7-reset-save.txt
  ```

  **Commit**: YES | Message: `feat(staff-intake): add complete intake form reset flow` | Files: [`views/staff_dashboard_view.py`]

- [x] 8. Triển khai "Xác nhận tiếp nhận" + dialog + đồng bộ danh sách chờ (3B)

  **What to do**: Implement confirm button full-width theo spec, mở dialog xác nhận, gọi controller check-in, cập nhật trạng thái appointment sang chờ khám, refresh khu vực waiting list của staff dashboard và show success notice.
  **Must NOT do**: Không xác nhận khi thiếu thông tin bắt buộc (doctor/service/patient); không cập nhật nửa vời (UI đổi nhưng DB không đổi).

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: transactional behavior giữa UI + DB + waiting list sync.
  - Skills: `[]`
  - Omitted: [`/playwright`] - chỉ cho QA.

  **Parallelization**: Can Parallel: NO | Wave 3 | Blocks: [9,10] | Blocked By: [1,3,5,6]

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `views/staff_dashboard_view.py` - waiting list card và intake summaries.
  - Pattern: `controllers/appointment_controller.py` - status constants + validation response shape.
  - API/Type: `models/appointment_model.py` - update status và truy vấn theo doctor/patient.
  - Pattern: `views/patient_view.py` - dialog interaction patterns.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Nhấn confirm mở dialog xác nhận; chọn đồng ý thực hiện cập nhật thành công.
  - [ ] Sau confirm thành công, hàng chờ khám staff hiển thị BN vừa tiếp nhận.
  - [ ] Toast/feedback thành công hiển thị đúng nội dung nghiệp vụ.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Confirm intake happy path
    Tool: Playwright
    Steps: Chọn bệnh nhân + dịch vụ + bác sĩ + giờ, nhấn xác nhận và đồng ý dialog.
    Expected: Trạng thái đổi sang chờ khám, waiting list cập nhật, hiện thông báo thành công.
    Evidence: .sisyphus/evidence/task-8-confirm-success.png

  Scenario: Confirm blocked on missing required
    Tool: Playwright
    Steps: Bỏ trống bác sĩ hoặc dịch vụ rồi nhấn xác nhận.
    Expected: Không mở/không complete confirm flow; hiển thị lỗi rõ ràng.
    Evidence: .sisyphus/evidence/task-8-confirm-missing-required.png
  ```

  **Commit**: YES | Message: `feat(staff-intake): confirm check-in and sync waiting queue` | Files: [`views/staff_dashboard_view.py`, `controllers/appointment_controller.py`, `models/appointment_model.py`]

- [x] 9. Đồng bộ style tokens + accessibility/state feedback cho màn intake

  **What to do**: Chuẩn hóa QSS theo palette đã chốt (`#1A9B6C`, border/text/badge colors), trạng thái hover/active/disabled cơ bản, contrast đủ đọc, thông báo lỗi/thành công nhất quán trong trang.
  **Must NOT do**: Không ép thay đổi global stylesheet toàn app ngoài phạm vi cần thiết.

  **Recommended Agent Profile**:
  - Category: `visual-engineering` - Reason: tinh chỉnh UI/UX cuối.
  - Skills: `[]`
  - Omitted: [`/remove-ai-slops`] - chưa cần.

  **Parallelization**: Can Parallel: YES | Wave 4 | Blocks: [Final Verification] | Blocked By: [6,7,8]

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `main.py` - baseline QSS app.
  - Pattern: `views/staff_dashboard_view.py` - inline style hiện hữu.
  - External: color/spacing table từ user spec.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Các thành phần chính hiển thị đúng palette và hierarchy text.
  - [ ] Badge/status/info box đúng semantic màu.
  - [ ] Không phát sinh text khó đọc trên nền card.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Color/token consistency
    Tool: Playwright
    Steps: Chụp screenshot từng section và đối chiếu palette đã định.
    Expected: Màu chủ đạo, badge, border khớp spec trong sai số chấp nhận được.
    Evidence: .sisyphus/evidence/task-9-style-consistency.png

  Scenario: Error/success visibility
    Tool: Playwright
    Steps: Trigger 1 lỗi validate + 1 success save/confirm.
    Expected: Feedback dễ đọc, phân biệt rõ lỗi vs thành công.
    Evidence: .sisyphus/evidence/task-9-feedback-states.png
  ```

  **Commit**: YES | Message: `style(staff-intake): align intake styling and feedback states` | Files: [`views/staff_dashboard_view.py`, `main.py`]

- [x] 10. Regression checklist cho luồng staff liên quan sau intake integration

  **What to do**: Chạy lại các luồng staff bị ảnh hưởng: dashboard mở trang, quản lý lịch hẹn, danh sách bệnh nhân, thông báo cơ bản để đảm bảo intake refactor không phá tương thích.
  **Must NOT do**: Không mở rộng regression sang toàn bộ app roles ngoài staff trừ khi phát hiện lỗi chéo rõ ràng.

  **Recommended Agent Profile**:
  - Category: `unspecified-low` - Reason: kiểm tra hồi quy tập trung.
  - Skills: `[]`
  - Omitted: [`/review-work`] - đây là regression trước final verification wave.

  **Parallelization**: Can Parallel: YES | Wave 4 | Blocks: [Final Verification] | Blocked By: [8]

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `views/staff_dashboard_view.py` - menu/page indices và refresh methods.
  - Pattern: `views/main_view.py` - role switch vào staff dashboard.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Các menu staff mở bình thường, không crash sau thay đổi intake.
  - [ ] Dữ liệu intake mới không làm hỏng hiển thị danh sách/appointment hiện có.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Staff navigation regression
    Tool: Playwright
    Steps: Đi qua toàn bộ menu staff, thao tác tối thiểu mỗi trang.
    Expected: Không exception UI; navigation và render ổn định.
    Evidence: .sisyphus/evidence/task-10-staff-regression.txt

  Scenario: Data compatibility regression
    Tool: Bash
    Steps: Query một số record mới tạo từ intake và record cũ ở patients/appointments.
    Expected: Cả dữ liệu mới và cũ truy xuất bình thường, không sai schema mapping.
    Evidence: .sisyphus/evidence/task-10-data-compatibility.txt
  ```

  **Commit**: YES | Message: `chore(staff-intake): run staff regression and capture evidence` | Files: [`.sisyphus/evidence/*`]

## Final Verification Wave (MANDATORY — after ALL implementation tasks)
> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.
> **Do NOT auto-proceed after verification. Wait for user's explicit approval before marking work complete.**
> **Never mark F1-F4 as checked before getting user's okay.** Rejection or user feedback -> fix -> re-run -> present again -> wait for okay.
- [x] F1. Plan Compliance Audit — oracle
- [x] F2. Code Quality Review — unspecified-high
- [x] F3. Real Manual QA — unspecified-high (+ playwright if UI)
- [x] F4. Scope Fidelity Check — deep

## Commit Strategy
- Commit 1: `feat(db): extend patient and intake schema for staff reception flow`
- Commit 2: `feat(staff-intake): redesign reception UI and intake interactions`
- Commit 3: `feat(staff-intake): confirm check-in and waiting queue synchronization`
- Commit 4: `chore(qa): add evidence artifacts and regression checklist`

## Success Criteria
- Màn hình "Tiếp nhận bệnh nhân" đạt đúng design spec đã cung cấp (layout, màu, spacing, typography, states).
- Dữ liệu lưu/truy xuất bám đúng kiểu DB hiện tại trong codebase.
- Luồng xác nhận tiếp nhận cập nhật đúng trạng thái chờ khám và đồng bộ danh sách chờ staff.
- Có bộ evidence đầy đủ chứng minh pass toàn bộ QA scenarios.
