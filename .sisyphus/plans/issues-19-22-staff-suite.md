# Kế hoạch triển khai issues 19-23 cho cụm màn STAFF

## TL;DR
> **Summary**: Căn chỉnh 5 màn STAFF hiện có trong `StaffDashboardView` để khớp đặc tả GitHub issues #19–#23, ưu tiên đúng thứ tự nghiệp vụ `Thanh toán & Hóa đơn → Dịch vụ & Gói khám → Thông báo → Báo cáo → Cài đặt`, đồng thời giữ nguyên điều hướng staff hiện tại và tránh mở rộng sang refactor kiến trúc hoặc thay đổi schema DB nếu chưa thật sự bị chặn.
> **Deliverables**:
> - Màn `Thanh toán & Hóa đơn` khớp issue #19 trên nền `Payments`
> - Màn `Dịch vụ & Gói khám` khớp issue #20 với fallback không đổi schema
> - Màn `Thông báo` khớp issue #21 với chuẩn hóa field/status/date
> - Màn `Báo cáo` khớp issue #22 với logic gom số liệu được cô lập tốt hơn
> - Màn `Cài đặt` khớp issue #23 với giới hạn quyền staff rõ ràng và persistence path thực tế
> - Chuỗi verify/commit tách theo từng màn, một nhánh nhiều commit
> **Effort**: XL
> **Parallel**: YES - 3 waves chính + 1 wave tích hợp
> **Critical Path**: T1 Baseline → T2/T3 Billing → T4/T5 Services → T6 Notifications → T7/T8 Reports → T10/T11/T12 Settings → T13 Cross-page regression → Final Verification

## Context
### Original Request
- Làm cho 5 issue 19, 20, 21, 22, 23 của repo `ChuNgocLinh/khambenh`.
- Các file `issue/issue_19.md` đến `issue/issue_22.md` trong repo rỗng; `issue/issue_23.md` có đặc tả chi tiết. Nguồn sự thật cho cả cụm là GitHub issues + file `issue_23.md`.
- Người dùng đã chốt:
  - Thứ tự ưu tiên: `19 → 20 → 21 → 22 → 23`
  - Nhóm deliverable: `một nhánh, nhiều commit`

### Interview Summary
- Cả 5 issue đều là màn STAFF nằm trong `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py`.
- Đây là cụm màn liên tiếp trong sidebar staff, nên mọi thay đổi phải bảo toàn `switch_page` và signal wiring hiện có.
- Hệ thống test hiện tại dựa trên pytest nhưng coverage UI rất hẹp; verify thực tế phải dùng kết hợp compile/smoke/manual UI check.
- Mặc định không mở rộng sang đổi schema DB, trừ khi thực sự bị chặn bởi đặc tả không thể đạt được bằng controller/view adaptation.
- Issue #23 hiện có mismatch quan trọng: STAFF settings page mới chỉ có profile/password/logout rất tối giản; `SettingsController.update_personal_info(...)` đang gắn với `doctor_id`, không phù hợp trực tiếp cho staff.
- User override 2026-05-11: ưu tiên **luồng cơ bản chạy ổn** hơn là hoàn tất mọi chi tiết UI/utility nâng cao. Những phần như upload avatar/logo thật, restore thật, lịch sử backup riêng, export file thật, update-check online, chart engine thật được phép giữ ở trạng thái placeholder trung thực nếu không cản luồng chính.

### Metis Review (gaps addressed)
- Đã áp dụng mặc định an toàn cho các câu hỏi còn mở:
  - Issue #19 mặc định triển khai trên nền `Payments`, không tự mở rộng thành hệ thống invoice line-items mới nếu chưa bị chặn.
  - Issue #20 mặc định xử lý `gói khám / loại dịch vụ` ở tầng UI/controller trước, không thêm cột schema ngay.
  - Issue #21 mặc định chuẩn hóa field/status/date ở mapping layer, không thay DB.
  - Issue #22 mặc định ưu tiên chuyển logic tổng hợp sang `ReportController` ở mức tối thiểu cần thiết.
  - Issue #23 mặc định ưu tiên tái dùng `SettingsController`/`SettingsModel` cho display/notification/backup metadata, nhưng không reuse mù `update_personal_info(doctor_id, ...)` cho staff.
- Guardrails quan trọng đã được đưa vào plan:
  - Không đổi schema DB mặc định
  - Tách feature delivery khỏi technical debt cleanup tổng quát
  - Giữ blast radius chủ yếu trong `staff_dashboard_view.py` + controller/model đích danh
  - Mỗi commit phải để app ở trạng thái runnable

## Work Objectives
### Core Objective
Hoàn thiện 5 màn STAFF tương ứng issues #19–#23 sao cho khớp đặc tả UI/UX và luồng nghiệp vụ được mô tả trên GitHub, trong khi vẫn bám sát data model hiện có của dự án và tránh refactor lan rộng ngoài phạm vi.

### Deliverables
- Billing page staff khớp issue #19
- Service/package page staff khớp issue #20
- Notifications page staff khớp issue #21
- Reports page staff khớp issue #22
- Settings page staff khớp issue #23
- Regression-safe integration cho shared staff navigation/context
- Chuỗi commit riêng theo từng issue trong cùng một nhánh

### Definition of Done (verifiable conditions with commands)
- `python3 -m py_compile BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py` chạy thành công.
- Tất cả controller/model file có sửa đều compile được bằng `python3 -m py_compile <file>`.
- Từ thư mục `BTL.Nhóm6_Python/healthcare_management`, `python -m pytest -q` không fail thêm so với baseline.
- Mở app desktop theo `python3 BTL.Nhóm6_Python/healthcare_management/main.py` và đăng nhập role staff, truy cập được 5 màn mà không ném runtime exception.
- Sau mỗi commit issue, trạng thái working tree sạch trước khi sang issue tiếp theo.

### Must Have
- Giữ nguyên sidebar/staff dashboard structure hiện tại.
- Giữ thứ tự commit: 19 rồi 20 rồi 21 rồi 22.
- Issue #23 phải giữ đúng giới hạn quyền staff: được sửa thông tin cá nhân của chính mình, đổi mật khẩu của chính mình, đổi tùy chọn hiển thị cá nhân; không được đụng cấu hình lõi/phân quyền admin/DB nhạy cảm.
- Chuẩn hóa mismatch `payment`/`invoice` ở UI mà không đổi schema mặc định.
- Có fallback rõ ràng khi dữ liệu thiếu field mong muốn (đặc biệt service type, notification date/status, report datasets).
- Có fallback/truthful behavior rõ ràng cho Settings khi feature chưa có backend đầy đủ (logo system-wide, restore, update check, email persistence nếu thiếu backing field).
- Có verify cho cả happy path và empty/edge path trên từng màn.
- Tiêu chí shipping của pass này là **basic functional flow**: page mở được, thao tác chính chạy được, placeholder không được báo success giả.

### Must NOT Have (guardrails, AI slop patterns, scope boundaries)
- Không tự ý thay đổi schema DB (`init_db.sql`, migration, thêm cột/table) trừ khi task bị block hoàn toàn và đã ghi rõ lý do trong execution log.
- Không refactor tổng thể `StaffDashboardView` vượt ra ngoài helper thực sự cần cho 4 issue.
- Không mở rộng sang các màn doctor/admin/patient không thuộc issues #19–#23.
- Không thêm cơ chế accounting/notification/reporting mới ở cấp hệ thống nếu controller/view mapping hiện có vẫn đủ phục vụ đặc tả.
- Không dùng `DoctorModel`/`doctor_id` làm đường persistence mặc định cho issue #23 staff profile nếu không có chứng cứ staff thật sự là doctor-context.
- Không gộp mọi thay đổi thành một commit duy nhất.
- Không theo đuổi polish/feature nâng cao nếu chúng không cần thiết để giữ luồng chính chạy ổn ở pass hiện tại.

## Verification Strategy
> ZERO HUMAN INTERVENTION - all verification is agent-executed.
- Test decision: **tests-after** + pytest hiện có + compile smoke + app launch smoke
- QA policy: Mỗi task đều phải có scenario happy path và edge/failure path
- Evidence: `.sisyphus/evidence/task-{N}-{slug}.{ext}`

## Execution Strategy
### Parallel Execution Waves
> Target: 5-8 tasks per wave. <3 per wave (except final) = under-splitting.
> Extract shared dependencies as Wave-1 tasks for max parallelism.

Wave 1: Baseline + Issue 19 foundation + Issue 20 foundation  
Wave 2: Issue 19 completion + Issue 20 completion + Issue 21 + Issue 22 data path  
Wave 3: Issue 22 UI completion + Issue 23 foundation  
Wave 4: Issue 23 completion + cross-page regression/polish  
Wave F: Final verification wave

### Dependency Matrix (full, all tasks)
- T1 → blocks T2, T4, T6, T7, T10
- T2 → blocks T3
- T4 → blocks T5
- T7 → blocks T8
- T10 → blocks T11, T12
- T3, T5, T6, T8, T11, T12 → block T13
- T13 → blocks Final Verification

### Agent Dispatch Summary (wave → task count → categories)
- Wave 1 → 3 tasks → `quick`, `business-logic`, `unspecified-high`
- Wave 2 → 4 tasks → `business-logic`, `quick`, `unspecified-high`
- Wave 3 → 2 tasks → `business-logic`, `visual-engineering`
- Wave 4 → 2 tasks → `business-logic`, `unspecified-high`
- Final → 4 review tasks → `oracle`, `unspecified-high`, `deep`

## TODOs
> Implementation + Test = ONE task. Never separate.
> EVERY task MUST have: Agent Profile + Parallelization + QA Scenarios.

- [x] 1. Thiết lập baseline verify và chốt blast radius của cụm staff pages

  **What to do**:
  - Ghi baseline hiện tại của `staff_dashboard_view.py` và các controller/model sẽ bị chạm cho issues 19–23.
  - Chạy baseline compile/smoke/test để biết sẵn lỗi có trước.
  - Tạo checklist regression cho 4 page indices trong `switch_page`.
  - Xác nhận không có thay đổi schema DB trong scope ban đầu.

  **Must NOT do**:
  - Không sửa feature behavior ở task này.
  - Không bắt đầu cleanup kiến trúc lớn.

  **Recommended Agent Profile**:
  - Category: `quick` - Reason: baseline check, compile/test capture nhanh
  - Skills: `[]` - không cần skill phụ
  - Omitted: `karpathy-guidelines` - chưa cần ở task baseline ngắn

  **Parallelization**: Can Parallel: NO | Wave 1 | Blocks: T2, T4, T6, T7 | Blocked By: []

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:343` - bắt đầu page Notifications
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:395` - bắt đầu page Reports
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:787` - bắt đầu page Services
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3151` - bắt đầu page Billing
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3858` - `switch_page` và refresh theo index
  - Test: `BTL.Nhóm6_Python/pytest.ini:1` - testpaths hiện có
  - Test: `.github/workflows/tests.yml:15` - CI đang chạy `python -m pytest -q`
  - External: `https://github.com/ChuNgocLinh/khambenh/issues/19` - đặc tả issue 19
  - External: `https://github.com/ChuNgocLinh/khambenh/issues/20` - đặc tả issue 20
  - External: `https://github.com/ChuNgocLinh/khambenh/issues/21` - đặc tả issue 21
  - External: `https://github.com/ChuNgocLinh/khambenh/issues/22` - đặc tả issue 22

  **Acceptance Criteria**:
  - [ ] Có baseline note cho compile/test/app launch trong execution log.
  - [ ] Có danh sách file được phép sửa cho cụm 19–23.
  - [ ] Xác nhận scope hiện tại không bao gồm DB schema migration.

  **QA Scenarios**:
  ```
  Scenario: Baseline compile và pytest path
    Tool: Bash
    Steps: Chạy py_compile cho `staff_dashboard_view.py`; chạy `python -m pytest -q` từ `BTL.Nhóm6_Python/healthcare_management`
    Expected: Compile pass; pytest trả về baseline result để so sánh về sau
    Evidence: .sisyphus/evidence/task-1-baseline.txt

  Scenario: Baseline app route staff
    Tool: Bash
    Steps: Launch app theo entrypoint, đăng nhập staff trên môi trường verify, ghi nhận có vào được dashboard staff hay không
    Expected: Vào được `StaffDashboardView` hoặc ghi rõ blocker DB/env nếu có
    Evidence: .sisyphus/evidence/task-1-staff-launch.txt
  ```

  **Commit**: YES | Message: `chore(staff): capture baseline for issues 19-23` | Files: [`tests/*` nếu cần, `.sisyphus/evidence/*`]

- [x] 2. Căn chỉnh shell UI và danh sách chính cho màn Thanh toán & Hóa đơn (Issue 19)

  **What to do**:
  - Cập nhật `staff billing page` để có đúng cấu trúc: KPI trên cùng, tab trạng thái hóa đơn, search, filter thời gian, bảng danh sách hóa đơn, panel chi tiết hóa đơn.
  - Giữ data source chính trên nền `PaymentController`/`PaymentModel`.
  - Đảm bảo bảng có các cột theo đặc tả: mã hóa đơn, bệnh nhân, ngày tạo, tổng tiền, trạng thái, thao tác.
  - Tạo empty state rõ ràng cho trường hợp không có payment nào.

  **Must NOT do**:
  - Không tạo schema invoice line-item mới trong task này.
  - Không thay đổi semantics database ngoài mapping UI.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: vừa sửa UI vừa căn data mapping billing
  - Skills: `[]`
  - Omitted: `supabase` - không liên quan

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: T3 | Blocked By: T1

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3151` - `_build_staff_billing_page`
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3255` - `_refresh_staff_billing_table`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/payment_controller.py:1` - `get_all/create/update_status`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/models/payment_model.py` - schema thực tế của payment rows
  - Test: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3858` - refresh theo `switch_page`
  - External: `https://github.com/ChuNgocLinh/khambenh/issues/19` - source of truth cho UI/UX billing

  **Acceptance Criteria**:
  - [ ] Page billing hiển thị đủ KPI, tabs, search/filter, table, detail panel theo spec issue #19.
  - [ ] Không crash khi payment rows thiếu field phụ như ngày tạo hoặc tên bệnh nhân.
  - [ ] Trạng thái billing được render nhất quán với `unpaid/paid/cancelled/refunded` hoặc mapping tương đương hiện có.

  **QA Scenarios**:
  ```
  Scenario: Mở màn billing và xem danh sách hóa đơn
    Tool: Bash
    Steps: Launch app, đăng nhập staff, chuyển sang page billing, quan sát table/detail panel
    Expected: Table hiển thị danh sách hoặc empty state, không có runtime exception
    Evidence: .sisyphus/evidence/task-2-billing-ui.txt

  Scenario: Dữ liệu billing rỗng hoặc thiếu field
    Tool: Bash
    Steps: Dùng môi trường test/mock hiện có để khiến danh sách billing rỗng hoặc field date/name thiếu; refresh page
    Expected: UI render fallback text thay vì crash hoặc ô trống lỗi format
    Evidence: .sisyphus/evidence/task-2-billing-empty.txt
  ```

  **Commit**: YES | Message: `feat(staff): align billing page with issue 19` | Files: [`views/staff_dashboard_view.py`, `controllers/payment_controller.py`, `models/payment_model.py` nếu cần]

- [x] 3. Hoàn thiện hành vi thanh toán, xác nhận giao dịch và in hóa đơn cho Issue 19

  **What to do**:
  - Hoàn thiện luồng chọn phương thức thanh toán, nhập số tiền nhận, tính tiền thừa, xác nhận thanh toán.
  - Chuẩn hóa mapping “invoice” trong UI sang record `Payments` hiện có nếu chưa có invoice entity thực thụ.
  - Cho phép in hóa đơn/biên nhận theo data đã xác nhận thanh toán, ít nhất ở dạng preview nhất quán.
  - Chặn double-submit và chặn tạo thanh toán trùng cho cùng appointment khi có thể ở controller/view layer.

  **Must NOT do**:
  - Không thiết kế lại toàn bộ accounting model.
  - Không gắn PDF engine mới nếu spec không bắt buộc.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: task trọng tâm về state transition và validation
  - Skills: `[]`
  - Omitted: `karpathy-guidelines` - không bắt buộc nếu task runner đã bám plan chặt

  **Parallelization**: Can Parallel: NO | Wave 2 | Blocks: T9 | Blocked By: T2

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3304` - `_handle_staff_create_invoice`
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3367` - `_handle_staff_confirm_payment`
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3395` - `_handle_staff_print_receipt`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/payment_controller.py:10` - `create`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/payment_controller.py:14` - `update_status`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/appointment_controller.py` - kiểm tra appointment thuộc patient và status hợp lệ
  - External: `https://github.com/ChuNgocLinh/khambenh/issues/19`

  **Acceptance Criteria**:
  - [ ] Xác nhận thanh toán cập nhật trạng thái đúng và refresh lại table/detail ngay sau thao tác.
  - [ ] Tính tiền thừa đúng với tiền nhận và tổng phải thu.
  - [ ] Nút in hóa đơn chỉ khả dụng sau khi giao dịch ở trạng thái đã thanh toán hoặc equivalent state theo plan.

  **QA Scenarios**:
  ```
  Scenario: Thanh toán thành công một hóa đơn chờ thanh toán
    Tool: Bash
    Steps: Chọn một row unpaid, chọn phương thức, nhập số tiền nhận hợp lệ, bấm xác nhận
    Expected: Status đổi sang paid, doanh thu và feedback cập nhật, in hóa đơn khả dụng
    Evidence: .sisyphus/evidence/task-3-payment-success.txt

  Scenario: Double-submit hoặc số tiền nhận không hợp lệ
    Tool: Bash
    Steps: Bấm xác nhận 2 lần nhanh hoặc nhập tiền nhận nhỏ hơn tổng thanh toán
    Expected: Không tạo giao dịch trùng; UI chặn hoặc báo lỗi rõ ràng
    Evidence: .sisyphus/evidence/task-3-payment-error.txt
  ```

  **Commit**: YES | Message: `feat(staff): complete payment actions for issue 19` | Files: [`views/staff_dashboard_view.py`, `controllers/payment_controller.py`, `controllers/appointment_controller.py` nếu cần]

- [x] 4. Căn chỉnh màn Dịch vụ & Gói khám theo đặc tả hiển thị của Issue 20

  **What to do**:
  - Cập nhật page dịch vụ để có đúng KPI, tab `Dịch vụ`/`Gói khám`, search, filter, thêm dịch vụ, bảng danh sách, panel chi tiết.
  - Chuẩn hóa fallback khi schema `Services` chưa có `service_type/category`.
  - Render được mô tả dịch vụ, quy trình thực hiện, lưu ý và các dịch vụ thường được chọn kèm theo chiến lược fallback an toàn.

  **Must NOT do**:
  - Không thêm cột mới vào bảng `Services` trong task này.
  - Không biến task này thành redesign taxonomy dịch vụ.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: UI + fallback data mapping
  - Skills: `[]`
  - Omitted: `supabase-postgres-best-practices` - không liên quan

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: T5 | Blocked By: T1

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:787` - `_build_staff_service_lookup_page`
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:898` - `_refresh_staff_service_lookup`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/service_controller.py:1` - CRUD service hiện có
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/models/service_model.py` - schema chỉ có name/price/description
  - External: `https://github.com/ChuNgocLinh/khambenh/issues/20`

  **Acceptance Criteria**:
  - [ ] Page hiển thị đủ structure theo issue #20 ngay cả khi model chưa có `category/service_type`.
  - [ ] Tab/giao diện không crash với dữ liệu service tối giản.
  - [ ] Detail panel luôn hiện tên, giá, mô tả; các field thiếu phải fallback rõ ràng.

  **QA Scenarios**:
  ```
  Scenario: Mở màn dịch vụ và lọc dữ liệu cơ bản
    Tool: Bash
    Steps: Launch app, vào page dịch vụ, search theo tên, đổi filter trạng thái/loại nếu có
    Expected: Danh sách cập nhật đúng hoặc hiển thị empty state rõ, không crash vì thiếu category/service_type
    Evidence: .sisyphus/evidence/task-4-service-ui.txt

  Scenario: Service row thiếu metadata package/type
    Tool: Bash
    Steps: Dùng row service chỉ có name/price/description và refresh panel chi tiết
    Expected: UI dùng fallback text hợp lệ thay vì trace lỗi hoặc trống hỏng bố cục
    Evidence: .sisyphus/evidence/task-4-service-fallback.txt
  ```

  **Commit**: YES | Message: `feat(staff): align services page with issue 20` | Files: [`views/staff_dashboard_view.py`, `controllers/service_controller.py` nếu cần]

- [x] 5. Hoàn thiện thao tác dịch vụ và tích hợp ngữ cảnh đặt lịch/billing cho Issue 20

  **What to do**:
  - Hoàn thiện nút `Thêm dịch vụ`, `Xem`, `Sửa`, `Ngưng áp dụng`/menu tương ứng nếu đã có scaffolding.
  - Chuẩn hóa việc chọn dịch vụ để đẩy sang shared context cho lịch hẹn/billing.
  - Nếu `Gói khám` chưa có entity thật, dùng grouping/presentation layer và ghi rõ giới hạn trong UI thay vì fake persistence.

  **Must NOT do**:
  - Không tạo package engine hoặc combo pricing engine mới.
  - Không để thao tác “ngưng áp dụng” phá dữ liệu liên quan appointment cũ.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: phụ thuộc nhiều vào current controller semantics
  - Skills: `[]`
  - Omitted: `karpathy-guidelines` - optional, không bắt buộc

  **Parallelization**: Can Parallel: NO | Wave 2 | Blocks: T9 | Blocked By: T4

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:945` - `_handle_staff_service_selection`
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:964` - `_apply_selected_staff_service_context`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/service_controller.py:10` - `create`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/service_controller.py:18` - `update`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/service_controller.py:26` - `delete`
  - External: `https://github.com/ChuNgocLinh/khambenh/issues/20`

  **Acceptance Criteria**:
  - [ ] Chọn dịch vụ cập nhật shared context đúng cho luồng tiếp theo.
  - [ ] Thao tác add/edit không làm hỏng danh sách hiện có và feedback rõ ràng.
  - [ ] Nếu chưa có package persistence, UI thể hiện trung thực đây là grouping/view-level behavior.

  **QA Scenarios**:
  ```
  Scenario: Chọn một dịch vụ và áp ngữ cảnh sang luồng kế tiếp
    Tool: Bash
    Steps: Chọn service row, bấm chọn, chuyển sang màn liên quan (lịch hẹn hoặc billing)
    Expected: Shared context phản ánh đúng service đã chọn
    Evidence: .sisyphus/evidence/task-5-service-context.txt

  Scenario: Thao tác sửa/ngưng áp dụng trên service đang có dữ liệu thiếu
    Tool: Bash
    Steps: Chạy edit hoặc disable trên service có metadata tối giản
    Expected: Không crash; feedback rõ; danh sách refresh đúng
    Evidence: .sisyphus/evidence/task-5-service-action.txt
  ```

  **Commit**: YES | Message: `feat(staff): complete service actions for issue 20` | Files: [`views/staff_dashboard_view.py`, `controllers/service_controller.py`, `models/service_model.py` nếu cần]

- [x] 6. Chuẩn hóa màn Thông báo theo Issue 21 và sửa mismatch field/status/date

  **What to do**:
  - Cập nhật page thông báo để có KPI, tabs (`Tất cả`, `Chưa đọc`, `Lịch hẹn`, `Thanh toán`, `Hệ thống`), search/filter, nút `Đánh dấu đã đọc`, danh sách thông báo và panel chi tiết.
  - Chuẩn hóa rule mapping từ `AppointmentController` và `PaymentController` sang notification rows.
  - Sửa mismatch giữa status issue spec với status thực tế (`pending/confirmed/in_progress/done/cancelled`) và giữa `created_at` vs `payment_date`.
  - Hỗ trợ hiển thị related notifications hoặc fallback group nếu không có persisted thread thực.

  **Must NOT do**:
  - Không thiết kế notification architecture mới ở cấp hệ thống.
  - Không thêm queue/read-state persistence mới nếu không có sẵn chỗ dựa.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: normalization logic là trọng tâm
  - Skills: `[]`
  - Omitted: `supabase` - không liên quan

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: T9 | Blocked By: T1

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:343` - `_build_staff_notifications_page`
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3531` - `_refresh_staff_notifications`
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3586` - `_mark_notification_as_handled`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/appointment_controller.py` - source notification lịch hẹn
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/payment_controller.py:6` - source notification thanh toán
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/models/payment_model.py` - kiểm tra field thời gian thực tế (`payment_date`)
  - External: `https://github.com/ChuNgocLinh/khambenh/issues/21`

  **Acceptance Criteria**:
  - [ ] Page thông báo không bỏ sót “lịch mới” do mismatch status string.
  - [ ] Payment notifications hiển thị đúng thời gian từ field có thật trong model/schema.
  - [ ] Mark-as-read behavior không crash ngay cả khi read-state chỉ là UI-level state.

  **QA Scenarios**:
  ```
  Scenario: Render danh sách thông báo với dữ liệu mixed appointment/payment
    Tool: Bash
    Steps: Mở page thông báo, refresh data, kiểm tra row appointment và payment cùng xuất hiện
    Expected: Thời gian và loại thông báo hiển thị đúng, không có row rỗng lỗi format
    Evidence: .sisyphus/evidence/task-6-notifications.txt

  Scenario: Notification row có status hoặc date thiếu/không parse được
    Tool: Bash
    Steps: Cấp dữ liệu có status lạ hoặc payment thiếu time field chuẩn rồi refresh page
    Expected: UI fallback an toàn, không crash, feedback rõ
    Evidence: .sisyphus/evidence/task-6-notifications-edge.txt
  ```

  **Commit**: YES | Message: `feat(staff): align notifications page with issue 21` | Files: [`views/staff_dashboard_view.py`, `controllers/payment_controller.py`, `models/payment_model.py` nếu cần]

- [x] 7. Chuyển luồng tổng hợp dữ liệu báo cáo về hướng controller-first cho Issue 22

  **What to do**:
  - Đánh giá và áp dụng `ReportController` cho các số liệu báo cáo cơ bản: tổng bệnh nhân, tổng lịch hẹn, doanh thu cơ bản.
  - Giữ adaptation tối thiểu: chỉ đưa vào controller phần tổng hợp thực sự cần cho màn staff reports.
  - Định nghĩa rõ contract dữ liệu mà reports page sẽ consume.

  **Must NOT do**:
  - Không refactor toàn bộ analytics/reporting subsystem.
  - Không mở rộng export PDF/Excel nếu chưa cần cho issue completion bước đầu.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: ranh giới MVC và logic tổng hợp là phần chính
  - Skills: `[]`
  - Omitted: `supabase-postgres-best-practices` - không liên quan

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: T8 | Blocked By: T1

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3601` - `_refresh_staff_reports`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/report_controller.py:1` - `revenue`, `appointments_count`, `patients_count`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/patient_controller.py:8` - `get_all`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/appointment_controller.py` - source counts/status breakdown
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/payment_controller.py:6` - source revenue/payment totals
  - External: `https://github.com/ChuNgocLinh/khambenh/issues/22`

  **Acceptance Criteria**:
  - [ ] Phần tổng hợp cốt lõi cho reports có đường dữ liệu rõ ràng, ưu tiên qua controller.
  - [ ] Page reports không tự ôm thêm business logic khó test ngoài phần presentation cần thiết.
  - [ ] Empty dataset không làm crash reports page.

  **QA Scenarios**:
  ```
  Scenario: Reports load với dataset bình thường
    Tool: Bash
    Steps: Mở page reports sau khi dữ liệu có bệnh nhân/lịch hẹn/payment
    Expected: KPI và summary khớp controller outputs, không lỗi runtime
    Evidence: .sisyphus/evidence/task-7-report-data.txt

  Scenario: Reports load với dataset rỗng hoặc date range hẹp
    Tool: Bash
    Steps: Kiểm tra trường hợp controller trả rỗng hoặc filter ra 0 bản ghi
    Expected: UI hiển thị 0/fallback thay vì traceback hoặc chia 0
    Evidence: .sisyphus/evidence/task-7-report-empty.txt
  ```

  **Commit**: YES | Message: `refactor(staff): route report totals through controller` | Files: [`views/staff_dashboard_view.py`, `controllers/report_controller.py`]

- [x] 8. Hoàn thiện UI/UX màn Báo cáo theo Issue 22

  **What to do**:
  - Cập nhật reports page cho đủ tabs báo cáo, bộ lọc thời gian/bác sĩ, KPI cards, chart placeholders/tables, quick shortcuts, dòng cập nhật dữ liệu và note cuối màn.
  - Nếu chưa có chart engine riêng, dùng visualization nhẹ/phù hợp với pattern staff hiện tại hoặc placeholder có số liệu rõ ràng.
  - Hỗ trợ export action theo mức tối thiểu chấp nhận được trong scope hiện tại; nếu chưa có file export thật thì phải ghi rõ trạng thái và không đánh lừa người dùng.

  **Must NOT do**:
  - Không tích hợp library chart/export nặng chỉ để đẹp UI nếu chưa cần.
  - Không biến task này thành báo cáo tài chính sâu toàn hệ thống.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: gắn UI với report contract vừa chuẩn hóa
  - Skills: `[]`
  - Omitted: `frontend-ui-ux` - không có giá trị trực tiếp trong PyQt desktop text-driven task này

  **Parallelization**: Can Parallel: NO | Wave 3 | Blocks: T9 | Blocked By: T7

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:395` - `_build_staff_reports_page`
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3601` - refresh logic reports hiện tại
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:12` - `StaffServiceDonutChart` có thể tái dùng cho tỷ lệ dịch vụ
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/report_controller.py:6` - revenue
  - External: `https://github.com/ChuNgocLinh/khambenh/issues/22`

  **Acceptance Criteria**:
  - [ ] Reports page phản ánh đủ các nhóm nội dung chính của issue #22.
  - [ ] Có fallback rõ ràng cho chart/export khi dữ liệu hoặc engine hạn chế.
  - [ ] Có dòng “Dữ liệu cập nhật đến ...” hoặc equivalent status message theo spec.

  **QA Scenarios**:
  ```
  Scenario: Mở báo cáo tổng quan và xem KPI/summary/charts
    Tool: Bash
    Steps: Chuyển sang reports page, đổi filter thời gian/bác sĩ, quan sát KPI và khối summary
    Expected: Số liệu refresh ổn định, không có widget rỗng lỗi hoặc crash khi đổi filter
    Evidence: .sisyphus/evidence/task-8-report-ui.txt

  Scenario: Trigger export/shortcut khi chức năng chỉ hỗ trợ mức tối thiểu
    Tool: Bash
    Steps: Bấm export hoặc quick shortcut report
    Expected: Hành vi trung thực (thực thi được hoặc thông báo rõ là placeholder/in-progress), không đánh lừa người dùng
    Evidence: .sisyphus/evidence/task-8-report-export.txt
  ```

  **Commit**: YES | Message: `feat(staff): align reports page with issue 22` | Files: [`views/staff_dashboard_view.py`, `controllers/report_controller.py` nếu cần]

- [x] 10. Dựng foundation cho màn Cài đặt STAFF theo issue #23

  **What to do**:
  - Mở rộng `staff settings page` từ phiên bản tối giản hiện tại thành bố cục gần đặc tả: header, breadcrumb/topbar context, menu cài đặt phụ, card thông tin cá nhân, card đổi mật khẩu, card tùy chọn hệ thống, card logo, hàng backup/restore, card thông tin hệ thống.
  - Giữ đúng sidebar staff hiện hữu; phần “menu cài đặt phụ” chỉ là cấu trúc page-local, không đổi menu chính.
  - Với các mục chưa có backend đầy đủ, phải dựng shell trung thực và gắn trạng thái placeholder rõ ràng.

  **Must NOT do**:
  - Không giả vờ đã có full restore/update-check/logo-persistence nếu backend chưa có.
  - Không xé rời staff settings thành module kiến trúc mới ngoài nhu cầu issue.

  **Recommended Agent Profile**:
  - Category: `visual-engineering` - Reason: task nặng về layout/hierarchy/card composition PyQt6
  - Skills: `karpathy-guidelines`, `frontend-ui-ux` - giữ UI rõ ràng nhưng vẫn sửa tối thiểu
  - Omitted: `supabase` - không liên quan

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: T11, T12 | Blocked By: T1

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:440` - `_build_staff_settings_page` hiện tại
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:178` - settings page add vào `content_stack`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/settings_controller.py:9` - controller settings trung tâm
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/models/settings_model.py:6` - `UserSettings`
  - External: `issue/issue_23.md:1` - đặc tả settings staff

  **Acceptance Criteria**:
  - [ ] Màn Settings staff có đủ shell/layout chính theo issue #23.
  - [ ] Các section chưa có backend đầy đủ vẫn hiển thị placeholder trung thực, không misleading.
  - [ ] Không phá current logout/password/profile flow đang có.

  **QA Scenarios**:
  ```
  Scenario: Mở màn settings staff và quan sát đầy đủ các card/section
    Tool: Bash
    Steps: Launch app, login staff, chuyển sang page settings
    Expected: Có đầy đủ khu vực cá nhân, mật khẩu, tùy chọn hệ thống, logo, backup/restore, system info hoặc placeholder tương đương; không runtime exception
    Evidence: .sisyphus/evidence/task-10-settings-shell.txt

  Scenario: Empty/fallback shell cho feature chưa implement đủ backend
    Tool: Bash
    Steps: Mở settings trong môi trường hiện tại và kiểm tra các section logo/restore/update check khi chưa có backend đầy đủ
    Expected: UI hiển thị trạng thái trung thực, không có nút gây hiểu nhầm là đã hoạt động đầy đủ
    Evidence: .sisyphus/evidence/task-10-settings-fallback.txt
  ```

  **Commit**: YES | Message: `feat(staff): align settings layout with issue 23` | Files: [`views/staff_dashboard_view.py`]

- [x] 11. Hoàn thiện persistence path đúng cho thông tin cá nhân, mật khẩu và tùy chọn cá nhân của STAFF

  **What to do**:
  - Thay thế hoặc bọc lại logic `_handle_staff_profile_update` để không còn chỉ update `self.user_data` trong RAM.
  - Không dùng thẳng `SettingsController.update_personal_info(doctor_id, ...)` nếu staff không có `doctor_id`; phải thiết kế luồng persistence đúng với staff context hiện có (`Users` / `Patients` / `UserSettings` tùy dữ liệu thực tế).
  - Nối UI cho các tùy chọn cá nhân khả dụng với `SettingsController.update_notification`, `update_display_option`, `update_language` khi phù hợp.
  - Giữ `change_password` trên đường thực thi hiện có qua `SettingsController.change_password` / `UserModel.change_password`.

  **Must NOT do**:
  - Không ép staff đi qua `DoctorModel` nếu không có quan hệ dữ liệu hợp lệ.
  - Không thêm schema mới nếu còn có thể dựa trên `UserSettings` + bảng hiện hữu.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: đây là task ranh giới dữ liệu/quyền và persistence
  - Skills: `karpathy-guidelines` - để tránh overengineering khi vá mismatch staff-vs-doctor
  - Omitted: `frontend-ui-ux` - không phải trọng tâm task này

  **Parallelization**: Can Parallel: YES | Wave 4 | Blocks: T13 | Blocked By: T10

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:4817` - `_handle_staff_profile_update`
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:4845` - `_handle_staff_password_change`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/settings_controller.py:32` - `update_personal_info(doctor_id, user_id, payload)` mismatch hiện tại
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/settings_controller.py:118` - `update_notification`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/settings_controller.py:127` - `update_display_option`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/settings_controller.py:137` - `update_language`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/settings_controller.py:252` - `change_password`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/models/user_model.py:138` - `change_password`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/models/settings_model.py:113` - `update_fields`
  - External: `issue/issue_23.md:1065` - workflow cá nhân/mật khẩu/tùy chọn

  **Acceptance Criteria**:
  - [ ] Lưu profile staff không còn chỉ là session-only nếu dữ liệu backing field cho phép.
  - [ ] Đổi mật khẩu staff pass đủ matrix validate theo issue #23.
  - [ ] Tùy chọn cá nhân được lưu theo đường persistence đúng và không đụng quyền nhạy cảm.

  **QA Scenarios**:
  ```
  Scenario: Lưu thông tin cá nhân staff với dữ liệu hợp lệ và không hợp lệ
    Tool: Bash
    Steps: Sửa họ tên/email/sđt, bấm lưu; thử cả case thiếu tên/email sai format/phone sai format
    Expected: Case hợp lệ được lưu theo path đúng; case sai báo lỗi rõ; không chỉ đổi local state giả nếu backend có thể lưu
    Evidence: .sisyphus/evidence/task-11-profile-persistence.txt

  Scenario: Đổi mật khẩu staff và login lại
    Tool: Bash
    Steps: Nhập current/new/confirm theo nhiều case; với case thành công, logout/login lại bằng mật khẩu mới
    Expected: Validate đúng; case thành công cập nhật thật qua Users table path hiện có
    Evidence: .sisyphus/evidence/task-11-password-flow.txt
  ```

  **Commit**: YES | Message: `feat(staff): persist settings and password flows for issue 23` | Files: [`views/staff_dashboard_view.py`, `controllers/settings_controller.py`, `models/settings_model.py`, `models/user_model.py`, file dữ liệu staff liên quan nếu cần]

- [x] 12. Hoàn thiện logo, backup/restore, system info và quyền hiển thị cho issue #23

  **What to do**:
  - Nối phần backup/sync đang có trong `SettingsController` vào UI staff ở mức quyền cho phép.
  - Quyết định rõ behavior cho restore: nếu chưa có backend restore thật, hiển thị action bị khóa hoặc cảnh báo “chưa hỗ trợ” thay vì giả lập thành công.
  - Hiển thị system info tối thiểu dựa trên `config` / env có thật.
  - Với logo phòng khám: nếu chưa có persistence/policy cho system-wide logo, dùng preview + hành vi trung thực (ví dụ local/session placeholder hoặc disabled action có giải thích).
  - Bảo đảm các mục không thuộc quyền staff (phân quyền, database lõi, cấu hình nhạy cảm) chỉ xem/disable/cảnh báo đúng như spec.

  **Must NOT do**:
  - Không làm restore phá dữ liệu thật khi chưa có quy trình an toàn.
  - Không tạo fake update-check online nếu không có nguồn kiểm tra thực.
  - Không cho staff chỉnh phân quyền/admin/system core.

  **Recommended Agent Profile**:
  - Category: `business-logic` - Reason: task pha trộn UI action + quyền + file-system integration
  - Skills: `karpathy-guidelines`, `frontend-ui-ux` - để giữ hành vi trung thực, UI rõ ràng
  - Omitted: `supabase` - không liên quan

  **Parallelization**: Can Parallel: YES | Wave 4 | Blocks: T13 | Blocked By: T10

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:440` - base settings page hiện tại
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/settings_controller.py:146` - `backup_now`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/settings_controller.py:218` - `sync_now`
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/models/settings_model.py:7` - defaults/backup timestamps
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/config.py` - version/db config cho system info
  - External: `issue/issue_23.md:758` - logo card
  - External: `issue/issue_23.md:845` - backup/restore cards
  - External: `issue/issue_23.md:1000` - system info card
  - External: `issue/issue_23.md:1389` - quyền staff

  **Acceptance Criteria**:
  - [ ] Backup/sync UI hoạt động đúng hoặc báo blocker trung thực.
  - [ ] Restore/update-check không được trình bày như feature hoàn chỉnh nếu backend chưa có.
  - [ ] System info hiển thị dữ liệu thật sẵn có; các mục staff không được phép chỉnh thì disable/cảnh báo đúng.

  **QA Scenarios**:
  ```
  Scenario: Backup/sync và thông tin hệ thống trên settings staff
    Tool: Bash
    Steps: Mở settings, kích hoạt backup/sync nếu khả dụng, kiểm tra card system info và feedback
    Expected: Backup/sync thành công hoặc blocker rõ; system info hiển thị trung thực từ config/runtime
    Evidence: .sisyphus/evidence/task-12-backup-system-info.txt

  Scenario: Restore/logo/update-check với backend chưa đủ
    Tool: Bash
    Steps: Tương tác các nút restore/logo/update-check trong môi trường hiện tại
    Expected: UI disable hoặc cảnh báo rõ; không có “success giả”
    Evidence: .sisyphus/evidence/task-12-guardrails.txt
  ```

  **Commit**: YES | Message: `feat(staff): complete guarded settings utilities for issue 23` | Files: [`views/staff_dashboard_view.py`, `controllers/settings_controller.py`, `config.py` nếu cần nhẹ, helper persistence/file dialog nếu thật sự cần]

- [x] 13. Regression integration cho shared context, navigation và technical debt tối thiểu của cụm 19–23

  **What to do**:
  - Kiểm tra và chỉnh lại shared context giữa billing/service/notifications/reports/settings nếu có stale state.
  - Dọn technical debt tối thiểu phát sinh trực tiếp từ 5 issue: helper dùng chung thật sự cần thiết, naming mismatch gây lỗi, dead branches trong 5 màn đích.
  - Không mở rộng cleanup sang toàn bộ dashboard staff.

  **Must NOT do**:
  - Không “tiện tay” refactor các màn staff khác ngoài 5 issue.
  - Không đổi public controller APIs nếu không cần cho 5 màn này.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: task tích hợp, cần phán đoán cẩn thận nhưng phải giữ scope hẹp
  - Skills: `karpathy-guidelines` - giúp giữ thay đổi gọn và chống overengineering
  - Omitted: `supabase` - không liên quan

  **Parallelization**: Can Parallel: NO | Wave 4 | Blocks: Final Verification | Blocked By: T3, T5, T6, T8, T11, T12

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3858` - `switch_page`
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:964` - shared service context
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3151` - billing page integration point
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3531` - notifications refresh integration point
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:3601` - reports refresh integration point
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py:440` - settings page integration point

  **Acceptance Criteria**:
  - [ ] Chuyển trang qua 5 màn đích không làm mất state sai cách hoặc gây stale data rõ rệt.
  - [ ] Không còn mismatch field/status/date/profile-path đã biết trong 5 màn này.
  - [ ] Technical debt cleanup giới hạn trong phạm vi hỗ trợ 5 issue.

  **QA Scenarios**:
  ```
  Scenario: Đi qua liên tiếp 5 màn staff 19→20→21→22→23 rồi quay lại
    Tool: Bash
    Steps: Launch app, login staff, chuyển page liên tiếp theo thứ tự và quay vòng lại
    Expected: Không runtime exception, không stale selection nghiêm trọng, data refresh đúng theo page
    Evidence: .sisyphus/evidence/task-9-staff-regression.txt

  Scenario: Shared context sau khi chọn service rồi sang billing/notifications/reports
    Tool: Bash
    Steps: Chọn service, sang billing, rồi notifications/reports
    Expected: Context liên quan được giữ đúng nơi cần, không leak sang chỗ không liên quan
    Evidence: .sisyphus/evidence/task-9-context.txt
  ```

  **Commit**: YES | Message: `fix(staff): stabilize shared flows across issues 19-23` | Files: [`views/staff_dashboard_view.py`, controller/model liên quan nếu thật sự cần]

## Final Verification Wave (MANDATORY — after ALL implementation tasks)
> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.
> **Do NOT auto-proceed after verification. Wait for user's explicit approval before marking work complete.**
> **Never mark F1-F4 as checked before getting user's okay.** Rejection or user feedback -> fix -> re-run -> present again -> wait for okay.
- [x] F1. Plan Compliance Audit — oracle
- [x] F2. Code Quality Review — unspecified-high
- [x] F3. Real Manual QA — unspecified-high (+ playwright if UI)
- [x] F4. Scope Fidelity Check — deep

## Commit Strategy
- Commit A: `chore(staff): capture baseline for issues 19-23`
- Commit B: `feat(staff): align billing page with issue 19`
- Commit C: `feat(staff): complete payment actions for issue 19`
- Commit D: `feat(staff): align services page with issue 20`
- Commit E: `feat(staff): complete service actions for issue 20`
- Commit F: `feat(staff): align notifications page with issue 21`
- Commit G: `refactor(staff): route report totals through controller`
- Commit H: `feat(staff): align reports page with issue 22`
- Commit I: `feat(staff): align settings layout with issue 23`
- Commit J: `feat(staff): persist settings and password flows for issue 23`
- Commit K: `feat(staff): complete guarded settings utilities for issue 23`
- Commit L: `fix(staff): stabilize shared flows across issues 19-23`

## Success Criteria
- 5 màn STAFF của issues 19–23 khớp đặc tả ở mức UI/flow/feedback quan trọng.
- Không có DB schema change mặc định; mọi schema change nếu buộc phải có phải được ghi nhận như blocker/resolution riêng.
- Không có regression rõ rệt khi chuyển trang trong cụm staff.
- Mỗi màn có commit riêng hoặc cặp commit riêng dễ review.
- Toàn bộ verify bắt buộc (compile + pytest baseline + app smoke) được ghi evidence rõ ràng.
- Với chỉ đạo mới của user, các capability nâng cao chưa có backend thật được phép giữ ở trạng thái placeholder trung thực miễn là không cản basic flow và không báo thành công giả.
