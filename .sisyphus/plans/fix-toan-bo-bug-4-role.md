# Fix toàn bộ bug 4 role (admin / doctor / staff / patient)

## TL;DR
> **Summary**: Sửa toàn bộ lỗi bảo mật, logic nghiệp vụ, schema drift, direct DB access trong view, hardcoded dữ liệu, và lỗi nhất quán dữ liệu đã phát hiện trên 4 role. Trọng tâm là vá lỗ hổng truy cập sai dữ liệu trước, sau đó tái lập ranh giới MVC đúng, gom migration về một đường chính thống, và khóa regression bằng test + docker DB verification.
> **Deliverables**:
> - Vá toàn bộ bug CRITICAL/HIGH/MEDIUM đã review
> - Loại bỏ direct DB access khỏi các view nằm trong phạm vi bug
> - Bỏ runtime schema mutation trong flow UI/model runtime, chuyển sang migration có kiểm soát
> - Bỏ password/default/hardcode nguy hiểm và siết RBAC/self-service scoping
> - Bổ sung test hồi quy cho security, role isolation, transaction/data consistency
> **Effort**: XL
> **Parallel**: YES - 2 waves
> **Critical Path**: 1 → 2 → 3 → 7/8/9/10/11 → 12 → F1/F2/F3/F4

## Context
### Original Request
- Lên plan fix toàn bộ bug trên, thật chi tiết, theo kiểu cầm tay chỉ việc.

### Interview Summary
- User muốn fix toàn bộ nhóm lỗi đã được review thủ công trên 4 role.
- Scope bao gồm: bug logic, dữ liệu hardcoded, direct DB access trong view, IDOR, runtime schema mutation, lỗi backup/restore consistency, broad `except Exception`, slot thời gian hardcoded, password mặc định/reset cứng.
- Không yêu cầu thêm feature mới ngoài phạm vi fix bug.

### Metis Review (gaps addressed)
- Guardrail bắt buộc: không còn DB access trực tiếp trong `views/*` thuộc phạm vi fix; không còn `except Exception` nuốt lỗi không log; không còn runtime `ALTER/CREATE TABLE` trong luồng UI/runtime; không dùng SQL string interpolation cho dữ liệu người dùng hoặc dynamic operator không whitelist; mọi bulk operation/backup-restore phải có transaction boundary rõ.
- Chặn scope creep: không rewrite toàn bộ app; chỉ refactor các module liên quan bug và các pattern tương đồng trực tiếp; không thêm security feature lớn ngoài phạm vi fix (2FA/IAM/encryption-at-rest full-stack).
- Acceptance criteria phải đo được: không còn IDOR, không còn password hardcoded, không còn DB import/call trực tiếp trong các view mục tiêu, không còn silent broad-except trong luồng mục tiêu, backup/restore pass consistency checks.

## Work Objectives
### Core Objective
Biến codebase từ trạng thái “vá cục bộ, logic phân tán trong view, có drift schema và security bug” thành trạng thái “role-safe, data-safe, MVC boundary rõ, migration một nguồn sự thật, regression có thể kiểm chứng tự động”.

### Deliverables
- Bộ sửa lỗi cho admin role: password reset flow, RBAC seed/bulk safety, bỏ DB logic khỏi view, bỏ password/render mặc định nguy hiểm.
- Bộ sửa lỗi cho patient role: vá IDOR, siết self-service scoping, đồng bộ slot booking, bỏ DB query trực tiếp trong patient view.
- Bộ sửa lỗi cho doctor role: bỏ DB query trực tiếp trong medical record view, đẩy logic sang controller/model, siết workflow record/prescription.
- Bộ sửa lỗi cho staff role: loại silent exception trong dashboard/queue/payment luồng mục tiêu, bóc business logic ra khỏi view, siết queue/payment consistency.
- Bộ sửa lỗi cross-cutting: migration/schema bootstrap, payment/report access scoping, backup/restore validation + transaction/rollback, centralized error handling/logging, regression test suite.

### Definition of Done (verifiable conditions with commands)
- `docker compose up -d` chạy thành công và MySQL sẵn sàng trên cổng cấu hình.
- `python3 BTL.Nhóm6_Python/healthcare_management/database/migrate.py` chạy không lỗi, không phát sinh drift mới.
- Không còn import `execute/fetch_all/fetch_one` trực tiếp trong các file view mục tiêu:
  - `python3 - <<'PY'
from pathlib import Path
targets = [
    Path('BTL.Nhóm6_Python/healthcare_management/views/admin_management_views.py'),
    Path('BTL.Nhóm6_Python/healthcare_management/views/doctor_management_views.py'),
    Path('BTL.Nhóm6_Python/healthcare_management/views/patient_view.py'),
    Path('BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py'),
]
bad = []
for p in targets:
    txt = p.read_text(encoding='utf-8')
    if 'from database.db import' in txt or ' execute(' in txt or 'fetch_all(' in txt or 'fetch_one(' in txt:
        bad.append(str(p))
print('\n'.join(bad))
raise SystemExit(1 if bad else 0)
PY`
- Test security/regression pass:
  - `pytest BTL.Nhóm6_Python/tests/test_appointment_rbac.py`
  - `pytest BTL.Nhóm6_Python/tests/test_doctor_domain_contracts.py`
  - `pytest BTL.Nhóm6_Python/tests/test_doctor_examination_workflow.py`
  - `pytest BTL.Nhóm6_Python/tests/test_doctor_schedule_flow.py`
  - `pytest BTL.Nhóm6_Python/tests -q`
- Không còn password mặc định hardcoded trong UI/admin reset flow:
  - `rg -n '123456|12345678|bsminh' BTL.Nhóm6_Python/healthcare_management`
  - Chỉ được còn ở fixture/test seed có giải thích rõ; không được còn trong UI/runtime flow.

### Must Have
- Vá triệt để `patient_view.py` luồng xem hồ sơ khám để không thể truy cập chéo bệnh nhân.
- Gỡ password reset cứng `123456` và input password mặc định trên dashboard/settings.
- Loại direct DB calls khỏi view admin/doctor/patient/staff trong phạm vi bug đã tìm thấy.
- Chuẩn hóa slot/giờ làm việc khỏi hardcode phân tán.
- Chuyển runtime schema mutation ở view/model thành migration/bootstrap có kiểm soát.
- Thêm regression tests cho security, role isolation, bulk safety, backup/restore.

### Must NOT Have (guardrails, AI slop patterns, scope boundaries)
- Không thêm feature business mới ngoài phạm vi sửa bug.
- Không giữ lại `except Exception` im lặng trong các luồng mục tiêu; nếu bắt rộng phải log rõ và trả lỗi có ngữ nghĩa.
- Không để view import/call DB trực tiếp trong các module mục tiêu.
- Không thêm migration chạy ngầm mỗi lần mở UI.
- Không sửa kiểu “đắp if” ở view nếu bug thực chất cần dời logic xuống controller/model.
- Không thay đổi contract dữ liệu role/appointment/payment mà không thêm test tương ứng.

## Verification Strategy
> ZERO HUMAN INTERVENTION - all verification is agent-executed.
- Test decision: **tests-after** trên hạ tầng pytest hiện có; nếu thiếu coverage thì tạo test mới trước khi đóng task.
- QA policy: Mỗi task đều có scenario happy path + failure/edge case, lưu evidence vào `.sisyphus/evidence/`.
- Evidence: `.sisyphus/evidence/task-{N}-{slug}.{ext}`

## Execution Strategy
### Parallel Execution Waves
> Target: 5-8 tasks per wave. Các dependency chung được bóc thành Wave 1 để tối đa hóa song song ở Wave 2.

Wave 1: 1, 2, 3, 4, 5, 6  
Wave 2: 7, 8, 9, 10, 11, 12

### Dependency Matrix (full, all tasks)
| Task | Depends On | Notes |
|---|---|---|
| 1 | - | Baseline, bootstrap DB, chụp evidence trước sửa |
| 2 | 1 | Khóa hướng migration/schema trước khi refactor module |
| 3 | 1,2 | Tạo boundary helper/scoping để các module cùng dùng |
| 4 | 1 | Tách slot/business-hour config để patient/staff/doctor dùng chung |
| 5 | 1 | Tạo mẫu xử lý lỗi/logging để thay broad-except ở module sau |
| 6 | 1,3,4,5 | Dựng harness test security/regression để các task sau bám vào |
| 7 | 2,3,4,5,6 | Patient IDOR + self-service scoping |
| 8 | 2,3,5,6 | Admin password/RBAC/bulk safety |
| 9 | 2,3,5,6 | Doctor record/prescription data-access refactor |
| 10 | 2,3,4,5,6 | Staff dashboard/payment/queue refactor |
| 11 | 2,3,5,6 | Payment/report/backup/restore hardening |
| 12 | 7,8,9,10,11 | Sweep direct DB access còn sót + full regression |

### Agent Dispatch Summary
| Wave | Task Count | Categories |
|---|---:|---|
| Wave 1 | 6 | business-logic, deep, unspecified-high |
| Wave 2 | 6 | business-logic, deep, unspecified-high |
| Final Verification | 4 | oracle, unspecified-high, deep |

## TODOs
> Implementation + Test = ONE task. Never separate.
> EVERY task MUST have: Agent Profile + Parallelization + QA Scenarios.

- [x] 1. Thiết lập baseline xác minh hiện trạng và khóa môi trường DB

  **What to do**:
  - Xác minh `.env` hiện tại có `DB_TYPE=mysql`, `DB_PORT=3307`, `DB_NAME=HealthcareDB`, `DB_USER=root`, `DB_PASSWORD=your_password` hoặc giá trị thực tế tương thích với `docker-compose.yml`.
  - Chạy `docker compose up -d` ở thư mục gốc repo.
  - Chờ container `healthcare_mysql` healthy/ready bằng cách kiểm tra log và khả năng kết nối.
  - Chạy `python3 BTL.Nhóm6_Python/healthcare_management/database/migrate.py` để chụp trạng thái migrate hiện tại.
  - Chạy nhanh test smoke đang có để lấy baseline trước sửa:
    - `pytest BTL.Nhóm6_Python/tests/test_appointment_rbac.py -q`
    - `pytest BTL.Nhóm6_Python/tests/test_doctor_dashboard_routing.py -q`
  - Lưu toàn bộ output vào evidence làm mốc so sánh sau sửa.

  **Must NOT do**:
  - Không sửa code ứng dụng ở task này.
  - Không bỏ qua migrate vì “đã seed sẵn”.
  - Không chuyển sang task refactor khi chưa chụp đủ baseline evidence.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: cần phối hợp DB/docker/test baseline đúng thứ tự.
  - Skills: `[]` - không cần skill chuyên biệt.
  - Omitted: `react-doctor` - không liên quan stack React.

  **Parallelization**: Can Parallel: NO | Wave 1 | Blocks: 2,3,4,5,6 | Blocked By: none

  **References**:
  - Pattern: `docker-compose.yml:1-12` - cấu hình MySQL 8.0, port 3307.
  - Pattern: `README.md:1-40` - hướng dẫn khởi động DB và app.
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/config.py:9-18,75-84` - config DB đang default `sqlserver`, cần xác minh env override.
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/database/migrate.py:76-132` - migrate legacy role.
  - Test: `BTL.Nhóm6_Python/tests/test_appointment_rbac.py` - baseline RBAC.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `docker compose up -d` thành công.
  - [ ] `python3 BTL.Nhóm6_Python/healthcare_management/database/migrate.py` exit code 0.
  - [ ] Có evidence log baseline trước sửa.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Khởi tạo MySQL baseline thành công
    Tool: Bash
    Steps: Chạy `docker compose up -d`; sau đó chạy `python3 BTL.Nhóm6_Python/healthcare_management/database/migrate.py`
    Expected: Container `healthcare_mysql` chạy; migrate in role distribution và exit 0
    Evidence: .sisyphus/evidence/task-1-baseline-db.txt

  Scenario: Baseline test smoke trước sửa
    Tool: Bash
    Steps: Chạy 2 lệnh pytest baseline đã chỉ định
    Expected: Có kết quả pass/fail rõ ràng, được lưu làm mốc đối chiếu
    Evidence: .sisyphus/evidence/task-1-baseline-tests.txt
  ```

  **Commit**: NO | Message: `n/a` | Files: none

- [x] 2. Gom toàn bộ schema drift về migration/bootstrap chuẩn, loại runtime schema mutation khỏi flow UI/runtime mục tiêu

  **What to do**:
  - Liệt kê toàn bộ nơi đang tự `ALTER TABLE` / `CREATE TABLE` trong runtime:
    - `views/admin_management_views.py:_ensure_admin_runtime_schema()`
    - `models/patient_model.py:_ensure_schema()`
    - `models/user_model.py:_ensure_auth_schema()`
    - các model tương tự như `backup_model.py` nếu có bootstrap runtime.
  - Quyết định chuẩn duy nhất: schema thay đổi phải đi qua `database/init_db.sql` và/hoặc file migration có kiểm soát; runtime chỉ được **assert/preflight** chứ không mutate schema.
  - Di chuyển các cột/bảng đang được thêm runtime vào nơi migration chính thống.
  - Thay các `_ensure_*schema()` bằng một trong hai dạng:
    1. no-op nếu schema đã được quản lý bởi migration, hoặc
    2. hàm preflight đọc metadata rồi raise/lỗi hướng dẫn chạy migration nếu schema thiếu.
  - Đảm bảo admin view không còn chạy `ALTER TABLE` khi mở UI.

  **Must NOT do**:
  - Không để lại `ALTER TABLE` trong view/admin runtime path.
  - Không thêm migration tạm kiểu “nếu thiếu thì app tự sửa giúp”.
  - Không phá tương thích MySQL hiện tại của `init_db.sql`.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: task này là nền tảng kiến trúc và ảnh hưởng nhiều module.
  - Skills: `[]`.
  - Omitted: `supabase` - không liên quan.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: 7,8,9,10,11,12 | Blocked By: 1

  **References**:
  - Pattern: `views/admin_management_views.py:47-78` - runtime alter columns.
  - Pattern: `models/patient_model.py:8-33` - `_ensure_schema()` đang mutate schema trực tiếp.
  - Pattern: `models/user_model.py:42-128` - `_ensure_auth_schema()`.
  - Pattern: `database/init_db.sql:4-1190` - nguồn schema hiện tại.
  - API/Type: `database/migrate.py:27-73` - ví dụ migrate có điều kiện.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `rg -n 'ALTER TABLE|CREATE TABLE IF NOT EXISTS|COL_LENGTH' BTL.Nhóm6_Python/healthcare_management/views BTL.Nhóm6_Python/healthcare_management/models` không còn runtime schema mutation trong các module mục tiêu, ngoại trừ file migration/bootstrap được phép.
  - [ ] App vẫn khởi động được sau khi chạy migration trên DB trống docker.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: DB trống + migration chính thống tạo đủ schema
    Tool: Bash
    Steps: Reset volume DB nếu cần; chạy `docker compose up -d`; chạy migrate; khởi động app/test module đọc schema
    Expected: Không module runtime nào cố tự ALTER TABLE trong lúc mở UI/khởi tạo controller
    Evidence: .sisyphus/evidence/task-2-schema-bootstrap.txt

  Scenario: Chặn drift schema bằng preflight có ngữ nghĩa
    Tool: Bash
    Steps: Tạm mô phỏng thiếu cột/bảng trên DB test phụ; gọi flow liên quan
    Expected: Hệ thống báo lỗi rõ yêu cầu chạy migration thay vì âm thầm tự sửa schema
    Evidence: .sisyphus/evidence/task-2-schema-preflight.txt
  ```

  **Commit**: YES | Message: `refactor(schema): remove runtime mutations from ui flows` | Files: `BTL.Nhóm6_Python/healthcare_management/database/*`, `views/admin_management_views.py`, `models/patient_model.py`, `models/user_model.py`, related bootstrap files

- [x] 3. Dựng lớp kiểm soát truy cập và data-scoping dùng chung cho 4 role

  **What to do**:
  - Tạo/chuẩn hóa helper role scoping trong controller/model để tránh mỗi view tự cầm `patient_id`, `doctor_id`, `user_id` rồi query DB.
  - Với patient flows: mọi thao tác nhận `patient_id` phải so khớp với `user_context.patient_id` trước khi đọc/ghi dữ liệu.
  - Với doctor flows: mọi thao tác nhận `doctor_id` phải so khớp `user_context.doctor_id` nếu là self-scope.
  - Với staff/admin flows: giữ quyền tổng nhưng vẫn phải đi qua controller rõ ràng, không bypass ở view.
  - Nếu chưa có helper chung, tạo ở controller hoặc module authz/scoping nhỏ gọn để các controller appointment/patient/medical record/payment dùng lại.

  **Must NOT do**:
  - Không sao chép logic ownership check lặp ở nhiều view.
  - Không để controller public method nào trả dữ liệu cross-user mà thiếu context check nếu method đó dùng cho self-service.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: đây là lớp nghiệp vụ xuyên nhiều role.
  - Skills: `[]`.
  - Omitted: `understand` - không cần overhead knowledge graph.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: 7,8,9,10,11 | Blocked By: 1,2

  **References**:
  - Pattern: `controllers/appointment_controller.py:121-160` - `_get_context_value()` + `authorize()` ownership hiện có.
  - Pattern: `controllers/patient_controller.py:21-23,132-162` - controller hiện chưa buộc context ownership.
  - Pattern: `models/patient_model.py:101-103` - `get_by_id(patient_id)` raw by id.
  - Pattern: `views/patient_view.py:1396-1402` - bug IDOR tiêu biểu.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Có một đường chuẩn để self-service flows lấy dữ liệu theo context thay vì id raw từ view.
  - [ ] Test âm cho patient truy cập patient khác thất bại với message/quyền phù hợp.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Patient chỉ xem được dữ liệu của chính mình
    Tool: Bash
    Steps: Chạy test mới mô phỏng user_context của Patient A yêu cầu record/profile Patient B
    Expected: Trả lỗi quyền hoặc tập rỗng theo contract đã định, không lộ dữ liệu B
    Evidence: .sisyphus/evidence/task-3-patient-scope.txt

  Scenario: Doctor không thao tác được lịch của doctor khác qua controller chung
    Tool: Bash
    Steps: Gọi controller với user_context doctor A và appointment doctor B
    Expected: Authorization fail rõ ràng
    Evidence: .sisyphus/evidence/task-3-doctor-scope.txt
  ```

  **Commit**: YES | Message: `fix(authz): centralize role ownership scoping` | Files: `controllers/*.py`, `models/*.py` liên quan scoping

- [x] 4. Chuẩn hóa slot lịch hẹn và giờ làm việc, bỏ hardcode phân tán giữa controller và patient view

  **What to do**:
  - Đưa khung giờ làm việc và bước slot thành nguồn cấu hình chung (ví dụ config constants hoặc settings module nhẹ) thay vì hardcode ở nhiều nơi.
  - Sửa `AppointmentController._default_slot_times()` để lấy từ nguồn chung.
  - Sửa `views/patient_view.py` không còn render 4 slot sáng cứng; thay bằng dữ liệu slot từ controller hoặc helper dùng chung.
  - Đảm bảo luồng patient booking, doctor schedule, staff intake cùng dùng một logic slot.
  - Giữ nguyên phạm vi hiện tại: chưa cần hỗ trợ multi-duration thông minh toàn hệ thống; nhưng phải loại bất nhất 4-slot-vs-full-day.

  **Must NOT do**:
  - Không để patient view tiếp tục hardcode `['08:00', '09:00', '10:00', '11:00']`.
  - Không đổi business rule giờ làm việc theo cảm tính; chỉ externalize rule hiện có hoặc rule đã được code dùng chung.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: liên quan contract appointment across views/controllers.
  - Skills: `[]`.
  - Omitted: `frontend-ui-ux` - đây là logic, không phải polish giao diện.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: 7,10,12 | Blocked By: 1

  **References**:
  - Pattern: `controllers/appointment_controller.py:219-227` - slot mặc định 08:00-17:00 mỗi 30 phút.
  - Pattern: `controllers/appointment_controller.py:381-385,497-501,698-702` - validation slot hợp lệ.
  - Pattern: `views/patient_view.py:1535-1544` - hardcoded 4 slot sáng.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Patient booking UI và controller validation sử dụng cùng một tập slot.
  - [ ] Không còn hardcoded danh sách 4 slot trong patient view.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Slot hiển thị thống nhất với slot backend
    Tool: Bash
    Steps: Chạy test/unit kiểm tra helper slot + render source trong patient view/controller
    Expected: Tập slot giống nhau, không có mismatch 4-slot-vs-full-day
    Evidence: .sisyphus/evidence/task-4-slot-unification.txt

  Scenario: Slot ngoài giờ bị từ chối
    Tool: Bash
    Steps: Gọi booking/update với giờ không nằm trong cấu hình slot
    Expected: Trả message lỗi hợp lệ, không tạo appointment
    Evidence: .sisyphus/evidence/task-4-slot-reject.txt
  ```

  **Commit**: YES | Message: `fix(appointments): unify booking slot configuration` | Files: `controllers/appointment_controller.py`, `views/patient_view.py`, shared config/helper files

- [x] 5. Chuẩn hóa error handling và logging ở các luồng mục tiêu, thay thế broad silent-except

  **What to do**:
  - Quét toàn bộ `except Exception` trong các module mục tiêu: `views/staff_dashboard_view.py`, `views/admin_management_views.py`, `views/dashboard_view.py`, `views/doctor_schedule_view.py`, `controllers/settings_controller.py`, `models/payment_model.py`, `models/backup_model.py`.
  - Phân loại từng khối:
    1. có thể thay bằng exception cụ thể,
    2. phải log + fallback có kiểm soát,
    3. phải propagate lỗi thay vì nuốt.
  - Thêm logging nhất quán ở mức controller/model cho lỗi DB/JSON/backup/restore.
  - Với dashboard summary không quan trọng, cho phép fallback an toàn **nhưng phải log**; với payment/check-in/restore/bulk update thì phải báo lỗi rõ, không được im lặng.

  **Must NOT do**:
  - Không giữ lại `except Exception: pass` hoặc `except Exception: return []/False` ở các luồng cập nhật dữ liệu quan trọng.
  - Không thêm logging rải rác thiếu ngữ cảnh; phải có message đủ biết file/operation.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: cần phán đoán từng broad-except theo mức độ critical.
  - Skills: `[]`.
  - Omitted: `karpathy-guidelines` - không cần nếu implementer đã bám plan chi tiết.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: 8,9,10,11,12 | Blocked By: 1

  **References**:
  - Pattern: `views/staff_dashboard_view.py:467-500` - fallback dashboard hiện nuốt lỗi.
  - Pattern: `views/admin_management_views.py:29-44` - `_safe_fetch_all()` / `_safe_execute()` silent fallback.
  - Pattern: `views/dashboard_view.py:3025-3031` - settings load broad except.
  - Pattern: `controllers/settings_controller.py:565-568` - JSON parse restore failure.
  - Pattern: `models/payment_model.py:16-21` - broad except quanh schema ensure.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Không còn broad silent-except trong các luồng ghi dữ liệu quan trọng đã scope.
  - [ ] Dashboard fallback không crash UI nhưng có log evidence khi dependency fail.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Lỗi dependency dashboard được log thay vì nuốt im lặng
    Tool: Bash
    Steps: Mock controller trả exception trong staff/admin dashboard summary
    Expected: UI/data fallback an toàn và log chứa operation lỗi
    Evidence: .sisyphus/evidence/task-5-dashboard-logging.txt

  Scenario: Lỗi restore/payment quan trọng không bị nuốt
    Tool: Bash
    Steps: Mock lỗi DB/JSON trong restore hoặc payment flow
    Expected: Trả message lỗi rõ ràng, có log, không success giả
    Evidence: .sisyphus/evidence/task-5-critical-errors.txt
  ```

  **Commit**: YES | Message: `refactor(errors): replace silent broad exceptions in critical flows` | Files: affected views/controllers/models

- [x] 6. Dựng regression harness cho security, role isolation, direct-db ban, và consistency rules

  **What to do**:
  - Kiểm kê test hiện có trong `BTL.Nhóm6_Python/tests/` và map test nào sẽ bảo vệ task nào.
  - Thêm test mới tối thiểu cho:
    - patient IDOR / ownership denial,
    - admin reset password flow mới,
    - no direct DB access in target views (text-based guard test được phép),
    - backup/restore ownership & malformed payload,
    - bulk account protection cho “last active admin”,
    - slot unification.
  - Nếu chưa có harness cho monkeypatch DB/model calls, chuẩn hóa fixture trong `conftest.py`.
  - Mọi task từ 7-11 phải cập nhật/đi qua test tương ứng trước khi coi là done.

  **Must NOT do**:
  - Không tạo test “snapshot UI vô nghĩa” không khóa đúng bug.
  - Không phụ thuộc thao tác tay để xác nhận security fix.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: test phải bám đúng contract nghiệp vụ/security.
  - Skills: `[]`.
  - Omitted: `playwright` - app là PyQt desktop, ưu tiên pytest/monkeypatch/Qt test utils.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: 7,8,9,10,11,12 | Blocked By: 1,3,4,5

  **References**:
  - Test: `BTL.Nhóm6_Python/tests/conftest.py` - fixture entry point.
  - Test: `BTL.Nhóm6_Python/tests/test_appointment_rbac.py` - RBAC pattern.
  - Test: `BTL.Nhóm6_Python/tests/test_doctor_*` - doctor workflow patterns.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Có test mới bảo vệ từng bug critical/high chính.
  - [ ] Có ít nhất một guard test text-based cấm direct DB imports/calls trong target views.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Regression harness chạy được độc lập trước khi refactor module sâu
    Tool: Bash
    Steps: Chạy nhóm test mới thêm ngay sau khi tạo harness/fixtures
    Expected: Test fail đúng ở code cũ hoặc pass với mock scaffold theo chủ đích, tạo baseline rõ ràng
    Evidence: .sisyphus/evidence/task-6-regression-harness.txt

  Scenario: Guard test phát hiện direct DB access nếu tái phạm
    Tool: Bash
    Steps: Chạy test/command guard quét target views
    Expected: Fail nếu còn import/call DB trực tiếp, pass khi sạch
    Evidence: .sisyphus/evidence/task-6-direct-db-guard.txt
  ```

  **Commit**: YES | Message: `test(security): add regression coverage for role isolation and consistency` | Files: `BTL.Nhóm6_Python/tests/*`

- [x] 7. Vá patient role triệt để: IDOR, self-service ownership, direct DB access, booking flow bất nhất

  **What to do**:
  - Refactor `views/patient_view.py` để không gọi `fetch_all` trực tiếp cho medical records.
  - Tạo controller method chuyên biệt kiểu `get_medical_history_for_current_patient(user_context)` hoặc tương đương; tuyệt đối không để view tự truyền `patient_id` raw vào query DB.
  - Sửa `ProfilePage.load_data()/save_data()` để mọi update/read profile đi qua controller có ownership guard, không chỉ dựa vào `self.patient_id` từ UI.
  - Sửa `HomePage` booking flow để dùng dữ liệu slot/doctor từ source chuẩn, và bảo đảm patient chỉ book cho chính mình.
  - Chuẩn hóa các placeholder liên quan self-service: nếu chức năng chưa hỗ trợ thì không được lộ dữ liệu/route mơ hồ.

  **Must NOT do**:
  - Không giữ `from database.db import fetch_all` trong `views/patient_view.py`.
  - Không chỉ “ẩn UI” mà bỏ qua authorization ở controller/model.
  - Không sửa bằng cách hardcode patient_id từ username string.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: đây là security fix lõi có ownership invariant rõ.
  - Skills: `[]`.
  - Omitted: `frontend-ui-ux` - không cần redesign giao diện.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: 12 | Blocked By: 2,3,4,5,6

  **References**:
  - Pattern: `views/patient_view.py:1-4` - import DB trực tiếp.
  - Pattern: `views/patient_view.py:1396-1402` - query medical record theo `self.patient_id`.
  - Pattern: `views/patient_view.py:1458-1488` - profile read/write hiện gắn với `self.patient_id`.
  - Pattern: `controllers/appointment_controller.py:270-288,306-320,323-345,596-623` - ownership rules hiện có để tận dụng/mở rộng.
  - Pattern: `models/patient_model.py:101-103,143-177` - raw by-id model methods.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Không còn direct DB access trong `views/patient_view.py`.
  - [ ] Patient A không thể đọc/sửa profile, lịch sử khám, lịch hẹn của Patient B bằng bất kỳ đường controller/view nào trong phạm vi fix.
  - [ ] Booking UI dùng slot thống nhất với backend.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Patient xem lịch sử khám của chính mình
    Tool: Bash
    Steps: Chạy test với user_context hợp lệ của patient, gọi controller/view adapter lấy medical history
    Expected: Chỉ trả records của patient hiện tại
    Evidence: .sisyphus/evidence/task-7-patient-history-own.txt

  Scenario: Patient truy cập chéo bệnh nhân bị chặn
    Tool: Bash
    Steps: Dùng user_context Patient A, truyền patient_id của B vào các method đọc/sửa liên quan
    Expected: Authorization fail hoặc no data; tuyệt đối không lộ dữ liệu B
    Evidence: .sisyphus/evidence/task-7-patient-history-cross-deny.txt
  ```

  **Commit**: YES | Message: `fix(patient): enforce self-service scoping and remove direct db access` | Files: `views/patient_view.py`, `controllers/patient_controller.py`, related models/tests

- [x] 8. Vá admin role triệt để: password reset, default credentials, RBAC seed safety, bulk account consistency, direct DB access

  **What to do**:
  - Thay flow reset password cứng `123456` bằng một trong hai cách và **chỉ dùng một cách thống nhất** trong codebase:
    1. random one-time password + bắt buộc đổi mật khẩu ở lần đăng nhập kế tiếp, hoặc
    2. reset token/out-of-band flow nội bộ nếu app đã có nền tảng phù hợp.
  - Với codebase hiện tại chưa có token/email hoàn chỉnh, chọn **one-time password + force_change flag** là hướng mặc định trong plan này.
  - Bổ sung cột/trạng thái bắt buộc đổi mật khẩu nếu chưa có; migration phải đi qua task 2.
  - Gỡ `QLineEdit("12345678")` và mọi credential mặc định hiển thị sẵn trong `dashboard_view.py` / admin settings UI.
  - Refactor admin account/role management theo hướng controller/model đảm nhận mutate DB; view chỉ gọi orchestration methods.
  - Siết bulk disable/delete/assign role bằng transaction + fresh DB recheck để không khóa/xóa admin hoạt động cuối cùng vì dữ liệu stale.
  - Tách seed RBAC defaults ra khỏi vòng đời render UI nếu đang chạy mỗi lần mở màn hình.

  **Must NOT do**:
  - Không còn reset password về giá trị public/dễ đoán.
  - Không render username/password mẫu trong UI settings runtime.
  - Không để RBAC seed chạy ẩn mỗi lần mở view nếu việc đó có thể mutate DB lặp lại.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: đụng security + RBAC + schema + bulk consistency cùng lúc.
  - Skills: `[]`.
  - Omitted: `git-master` - chưa cần thao tác git trong lúc implement.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: 12 | Blocked By: 2,3,5,6

  **References**:
  - Pattern: `views/admin_management_views.py:1778-1797` - tạo user/doctor/patient trực tiếp từ view.
  - Pattern: `views/admin_management_views.py:1820-1834` - update user/profile trực tiếp từ view.
  - Pattern: `views/admin_management_views.py:1843-1847,1865-1868,1894-1903,1919-1923` - bulk safety/last admin issues.
  - Pattern: `views/admin_management_views.py:1880-1883` - reset password cứng.
  - Pattern: `views/dashboard_view.py:2598-2605` - render username/password mặc định.
  - Pattern: `views/admin_management_views.py:3859-4021` - seed RBAC defaults + username hardcode.
  - API/Type: `models/user_model.py:197-256,287-311` - auth/password contract.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Không còn password mặc định cứng trong admin reset flow và dashboard/settings UI.
  - [ ] Có cơ chế force-change-password sau reset được test.
  - [ ] Bulk disable/delete không thể vô hiệu hóa admin hoạt động cuối cùng trong tình huống dữ liệu concurrent/stale đã mô phỏng.
  - [ ] RBAC seed không mutate DB lặp theo vòng đời render UI.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Admin reset password tạo mật khẩu dùng một lần và buộc đổi ở lần đăng nhập tiếp theo
    Tool: Bash
    Steps: Gọi flow reset password; sau đó mô phỏng login bằng mật khẩu tạm
    Expected: Login được hoặc theo contract mới, nhưng hệ thống buộc đổi mật khẩu trước khi dùng đầy đủ chức năng
    Evidence: .sisyphus/evidence/task-8-reset-password.txt

  Scenario: Không thể khóa/xóa admin hoạt động cuối cùng
    Tool: Bash
    Steps: Seed trạng thái chỉ còn 1 admin active; gọi bulk disable/delete
    Expected: Thao tác bị từ chối bởi kiểm tra fresh state trong transaction
    Evidence: .sisyphus/evidence/task-8-last-admin-protection.txt
  ```

  **Commit**: YES | Message: `fix(admin): harden credential reset and bulk account safety` | Files: `views/admin_management_views.py`, `views/dashboard_view.py`, `controllers/*`, `models/user_model.py`, tests/migrations



- [x] 9. Vá doctor role triệt để: bỏ direct DB access, siết medical record/prescription workflow, validation lâm sàng

  **What to do**:
  - Refactor `MedicalRecordView.load_data()` trong `views/doctor_management_views.py` để không import/call `fetch_all` trực tiếp.
  - Tạo controller/model method tương đương `get_records_by_doctor(doctor_id, search=...)` hoặc adapter tương tự.
  - Đảm bảo luồng `create medical record -> update appointment status -> prescription` có contract nhất quán:
    - nếu lưu bệnh án fail thì không đổi trạng thái lịch,
    - nếu đổi trạng thái lịch fail sau khi lưu bệnh án thì phải báo lỗi rõ và có khả năng reconcile.
  - Xem lại prescription flow để tránh ghi đơn thuốc khi `medicine_id` rỗng, số lượng âm/0, hoặc stock không đủ.
  - Thêm validation dữ liệu cho form khám lâm sàng (numeric fields như mạch, nhiệt độ, huyết áp, nhịp thở, cân nặng, chiều cao).

  **Must NOT do**:
  - Không giữ import `from database.db import fetch_all` trong doctor view.
  - Không để luồng record/prescription tạo dữ liệu nửa vời mà không có thông báo/reconcile path.
  - Không validate chỉ ở UI nếu controller/model vẫn nhận dữ liệu bẩn.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: workflow doctor là nghiệp vụ lõi, cần giữ tính nhất quán dữ liệu y khoa.
  - Skills: `[]`.
  - Omitted: `ai-slop-remover` - refactor phải theo nghiệp vụ, không chỉ cleanup style.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: 12 | Blocked By: 2,3,5,6

  **References**:
  - Pattern: `views/doctor_management_views.py:519-540` - query trực tiếp record by doctor.
  - Pattern: `views/doctor_management_views.py:542-572` - create medical record rồi đổi trạng thái lịch.
  - Pattern: `views/doctor_management_views.py:574-579` - prescription entry point.
  - Pattern: `views/doctor_examination_view.py:87-100` - field lâm sàng đang thiếu validation numeric rõ.
  - Test: `BTL.Nhóm6_Python/tests/test_doctor_examination_workflow.py`
  - Test: `BTL.Nhóm6_Python/tests/test_doctor_prescription_workflow.py`

  **Acceptance Criteria** (agent-executable only):
  - [ ] Không còn direct DB access trong doctor management view mục tiêu.
  - [ ] Luồng lưu bệnh án và đổi trạng thái lịch có hành vi thất bại rõ ràng, không success giả.
  - [ ] Prescription không thể tạo với dữ liệu thiếu hoặc stock không hợp lệ.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Doctor xem danh sách bệnh án qua controller/model boundary
    Tool: Bash
    Steps: Chạy test load_data với monkeypatch controller/model thay vì DB trực tiếp
    Expected: View render từ controller response, không cần DB import trực tiếp
    Evidence: .sisyphus/evidence/task-9-doctor-record-list.txt

  Scenario: Tạo bệnh án fail thì không cập nhật trạng thái lịch thành done
    Tool: Bash
    Steps: Mock MedicalRecordController.create trả fail và gọi flow add_new
    Expected: Appointment status không đổi; có message lỗi đúng
    Evidence: .sisyphus/evidence/task-9-record-create-fail.txt
  ```

  **Commit**: YES | Message: `fix(doctor): refactor record workflows and remove direct db access` | Files: `views/doctor_management_views.py`, `views/doctor_examination_view.py`, doctor-related controllers/models/tests

- [ ] 10. Vá staff role triệt để: dashboard silent failures, queue/payment consistency, direct business logic leakage

  **What to do**:
  - Rà các broad-except trong `views/staff_dashboard_view.py`, đặc biệt các luồng snapshot/dashboard, check-in, payment, waiting queue, reports, settings.
  - Với snapshot/dashboard summary: thay silent fallback bằng fallback + logging.
  - Với payment/check-in/queue thao tác thật: nếu controller lỗi thì phải show lỗi chuẩn, không tự nuốt thành danh sách rỗng/success giả.
  - Bóc dần các logic tổng hợp dữ liệu dashboard lớn ra helper/controller để view chỉ render.
  - Chuẩn hóa queue area `3B`: đưa thành config/constant dùng chung; nếu hệ thống hiện chỉ có 1 khu thì ghi rõ là default configurable, không hardcode tản mát.
  - Siết payment data exposure: nếu method `PaymentController.get_enriched_all()` đang dùng cả cho UI staff/admin, thêm lớp scoping/caller-specific method để không vô tình dùng sai nơi.

  **Must NOT do**:
  - Không giữ pattern `except Exception: appointments = []` cho luồng vận hành quan trọng mà không log.
  - Không để queue/payment logic tiếp tục phân tán nặng trong view nếu đã có controller phù hợp.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: file staff lớn nhất, nhiều workflow chồng nhau.
  - Skills: `[]`.
  - Omitted: `frontend-ui-ux` - trọng tâm là luồng nghiệp vụ, không phải thẩm mỹ.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: 12 | Blocked By: 2,3,4,5,6

  **References**:
  - Pattern: `views/staff_dashboard_view.py:463-539` - snapshot dashboard với nhiều silent except.
  - Pattern: `views/staff_dashboard_view.py` - các dòng broad except đã grep ra: 469, 493, 499, 3057, 3077, 3137, ...
  - Pattern: `controllers/waiting_queue_controller.py:5-21` - queue API mỏng, area default `3B`.
  - Pattern: `controllers/payment_controller.py:5-19` - payment controller đang expose all payments thẳng.
  - Pattern: `models/payment_model.py:15-73` - enriched payment query dùng rộng.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Các luồng staff mục tiêu không còn silent failure không log.
  - [ ] Queue area không còn hardcode phân tán; dùng chung một constant/config source.
  - [ ] Payment/queue/check-in flow có xử lý lỗi rõ và test được.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Staff dashboard fallback an toàn nhưng có log khi service phụ lỗi
    Tool: Bash
    Steps: Mock AppointmentController/PaymentController/WaitingQueueController ném exception trong snapshot builder
    Expected: Dashboard không crash, fallback hiển thị an toàn, log có đủ context
    Evidence: .sisyphus/evidence/task-10-staff-dashboard-fallback.txt

  Scenario: Queue/check-in lỗi không bị nuốt thành success giả
    Tool: Bash
    Steps: Mock WaitingQueueModel.check_in trả fail trong check-in flow
    Expected: Trả message lỗi chuẩn, không tạo queue/data ảo
    Evidence: .sisyphus/evidence/task-10-queue-failure.txt
  ```

  **Commit**: YES | Message: `fix(staff): harden dashboard queue and payment error handling` | Files: `views/staff_dashboard_view.py`, payment/queue controllers/models/tests

- [x] 11. Vá cross-cutting data-integrity: backup/restore, payment/report access, dynamic SQL patterns, service delete safety

  **What to do**:
  - `models/backup_model.py`: giữ whitelist field như hiện có nhưng thay `execute(f"UPDATE ... SET {set_clause}")` bằng builder an toàn chỉ ghép từ danh sách cột whitelist đã map sẵn; không ghép trực tiếp key raw dù đã filter.
  - `controllers/settings_controller.restore_from_backup()`: siết validation payload JSON, bảo đảm restore settings/profile thực hiện trong transaction hoặc rollback-safe block; nếu backup-before-restore fail thì quyết định rõ có dừng restore hay không. Trong plan này: **dừng restore nếu pre-backup được yêu cầu nhưng thất bại**.
  - `models/service_model.delete()`: không `DELETE` cứng service nếu đã được dùng trong `Invoices`; chuyển sang soft-disable hoặc chặn xóa có message rõ.
  - `models/payment_model.get_enriched_all()`: bỏ broad-except khởi tạo schema; cân nhắc tách method theo role nếu cần để giảm misuse.
  - Review `report_controller`/report access để bảo đảm không lộ dữ liệu không đúng role nếu đang tái sử dụng payment/report query tổng.

  **Must NOT do**:
  - Không để backup/restore cập nhật nửa chừng khi một phần profile/settings fail.
  - Không giữ `DELETE FROM Services` cho service đã có invoice lịch sử.
  - Không ghép SQL động từ keys không map tường minh.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: đụng data integrity, restore semantics, SQL safety.
  - Skills: `[]`.
  - Omitted: `supabase-postgres-best-practices` - DB là MySQL/SQLServer compatibility, không phải Postgres.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: 12 | Blocked By: 2,3,5,6

  **References**:
  - Pattern: `models/backup_model.py:240-262,370-379` - dynamic set_clause update.
  - Pattern: `controllers/settings_controller.py:547-619` - restore flow.
  - Pattern: `models/service_model.py:41-53` - delete cứng và `check_used()`.
  - Pattern: `models/payment_model.py:15-73` - broad-except + enriched query.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Backup settings/job update builder không dùng SQL động từ field keys raw chưa map.
  - [ ] Restore flow fail-safe: pre-backup fail => restore dừng; malformed JSON => fail rõ; cross-user backup => bị chặn.
  - [ ] Service đã có invoice không bị xóa cứng.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Restore backup chéo user bị chặn và malformed JSON fail rõ
    Tool: Bash
    Steps: Tạo payload backup giả với user_id khác; tạo file JSON hỏng; gọi restore flow
    Expected: Cả hai trường hợp đều fail rõ ràng, không mutate profile/settings
    Evidence: .sisyphus/evidence/task-11-restore-guards.txt

  Scenario: Service đã có invoice không bị delete cứng
    Tool: Bash
    Steps: Seed service đã được invoice tham chiếu; gọi delete service
    Expected: Hệ thống chặn xóa hoặc chuyển soft-disable theo contract mới; lịch sử invoice còn nguyên
    Evidence: .sisyphus/evidence/task-11-service-delete-safety.txt
  ```

  **Commit**: YES | Message: `fix(data): harden backup restore payment and service integrity` | Files: `models/backup_model.py`, `controllers/settings_controller.py`, `models/service_model.py`, `models/payment_model.py`, related report/payment code/tests

- [x] 12. Quét dọn cuối cùng: loại direct DB access còn sót, sweep hardcoded nguy hiểm, full regression và desktop startup verification

  **What to do**:
  - Chạy sweep cuối cùng cho toàn bộ target files để tìm:
    - `from database.db import`
    - `execute(` / `fetch_all(` / `fetch_one(` trong view target
    - `123456`, `12345678`, `bsminh`, `staff1`, `quan.do`, `dung.bui` trong runtime path
    - `except Exception:` còn sót trong luồng target.
  - Với hardcoded seed trong `init_db.sql` được phép giữ lại nếu là dữ liệu seed có chủ đích; nhưng runtime/UI logic không được còn phụ thuộc username seed đặc biệt.
  - Chạy full pytest suite.
  - Chạy startup verification cho app desktop ở mức không tương tác tay: import main modules / smoke open flows nếu test harness hỗ trợ.
  - Gom changelog kỹ thuật ngắn để executor/reviewer hiểu mỗi bug đã được bảo vệ bởi test nào.

  **Must NOT do**:
  - Không đóng task nếu guard grep vẫn ra direct DB access trong target views.
  - Không bỏ qua startup smoke của desktop app sau loạt refactor lớn.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: đây là sweep tổng hợp cần kỷ luật và coverage rộng.
  - Skills: `[]`.
  - Omitted: `review-work` - review cuối đã có Final Verification Wave riêng.

  **Parallelization**: Can Parallel: NO | Wave 2 | Blocks: F1,F2,F3,F4 | Blocked By: 7,8,9,10,11

  **References**:
  - Pattern: `views/admin_management_views.py`, `views/doctor_management_views.py`, `views/patient_view.py`, `views/staff_dashboard_view.py` - bốn target views chính.
  - Test: toàn bộ `BTL.Nhóm6_Python/tests/`.

  **Acceptance Criteria** (agent-executable only):
  - [ ] Guard grep/direct-DB test pass sạch.
  - [ ] `pytest BTL.Nhóm6_Python/tests -q` pass.
  - [ ] Desktop module smoke/import pass, không crash do refactor.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Full regression suite xanh toàn bộ
    Tool: Bash
    Steps: Chạy `pytest BTL.Nhóm6_Python/tests -q`
    Expected: Tất cả test pass; nếu có skip thì phải có lý do hợp lệ đã biết trước
    Evidence: .sisyphus/evidence/task-12-full-pytest.txt

  Scenario: Sweep cuối phát hiện 0 direct DB access trong target views
    Tool: Bash
    Steps: Chạy guard grep/test text-based trên 4 target views
    Expected: Không còn import/call DB trực tiếp và không còn credential hardcoded runtime
    Evidence: .sisyphus/evidence/task-12-guard-sweep.txt
  ```

  **Commit**: YES | Message: `test(regression): finalize role safety and cleanup sweep` | Files: guards/tests/minor cleanup across target modules

## Final Verification Wave (MANDATORY — after ALL implementation tasks)
> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.
> **Do NOT auto-proceed after verification. Wait for user's explicit approval before marking work complete.**
> **Never mark F1-F4 as checked before getting user's okay.** Rejection or user feedback -> fix -> re-run -> present again -> wait for okay.
- [ ] F1. Plan Compliance Audit — oracle
- [ ] F2. Code Quality Review — unspecified-high
- [ ] F3. Real Manual QA — unspecified-high (+ desktop flow automation via pytest/Qt test utilities where applicable)
- [ ] F4. Scope Fidelity Check — deep

## Commit Strategy
- Không commit sau từng thay đổi lẻ tẻ trong cùng một file lớn nếu còn đang phá build/test.
- Commit theo cụm logic sau khi từng nhóm task pass test:
  1. `fix(security): lock down role scoping and credential defaults`
  2. `refactor(mvc): remove direct db access from role views`
  3. `fix(data): harden transactions backup restore and payment flows`
  4. `test(regression): add role isolation and consistency coverage`

## Success Criteria
- Không còn đường truy cập dữ liệu chéo role/chéo patient trong các flow đã review.
- Không còn password reset/default hardcoded trong runtime/UI.
- Không còn runtime schema mutation trong admin view/patient model/runtime flow mục tiêu.
- Không còn direct DB call trong 4 view mục tiêu.
- Silent broad-except trong các luồng mục tiêu được thay bằng error handling có log và hành vi thất bại rõ ràng.
- Regression suite và docker/migration verification đều pass, có evidence đầy đủ.
