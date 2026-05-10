# Staff Interface Implementation (PyQt6)

## TL;DR
> **Summary**: Add a dedicated `staff` role and a new Staff dashboard/navigation flow in the existing PyQt6 clinic system, covering intake, appointment coordination, patient lookup, billing operations, notifications, quick reports, and personal settings with strict non-clinical boundaries.
> **Deliverables**:
> - Staff role routing + access control behavior
> - Staff dashboard view + left menu + top KPI cards
> - Functional staff modules (intake, appointments, patients, billing, services, notifications, reports, settings)
> - Tests-after verification artifacts and evidence bundle
> **Effort**: Large
> **Parallel**: YES - 3 waves
> **Critical Path**: 1 → 2 → 4 → 8 → F1-F4

## Context
### Original Request
Create a new detailed Staff interface matching provided menu and dashboard blocks: Dashboard, Patient Intake, Appointment Management, Patient List, Billing & Invoices, Services, Notifications, Reports, Settings; include workflow realism and operational constraints.

### Interview Summary
- User confirmed output should be a full implementation work plan.
- User chose to add a dedicated new `staff` role.
- User chose tests-after minimal strategy (repo has no automated test baseline today).
- Staff must support front-desk operations and must not edit specialist clinical records.

### Metis Review (gaps addressed)
- Added guardrails to prevent privilege bleed when reusing admin/doctor components.
- Added explicit permission-failure UX requirement (predictable deny/redirect behavior).
- Added module-level scope boundaries to avoid staff panel becoming full admin clone.
- Added edge-case acceptance criteria for state transitions (queue, billing status, appointment status).
- Marked unresolved business-policy items as explicit `[DECISION NEEDED]` placeholders.

## Work Objectives
### Core Objective
Implement a production-usable Staff UI in current PyQt6 architecture with clear role isolation and complete front-desk operational flow.

### Deliverables
1. Role model + auth/routing support for `staff`.
2. Staff dashboard shell with sidebar and page switching.
3. Staff pages for intake, appointments, patients, billing, services, notifications, reports, settings.
4. Guardrails enforcing non-clinical permissions.
5. Tests-after verification pack under `.sisyphus/evidence/`.

### Definition of Done (verifiable conditions with commands)
- `python "BTL.Nhóm6_Python/healthcare_management/main.py"` launches without runtime error.
- Login as staff routes to Staff dashboard (not patient/doctor/admin view).
- All staff sidebar items are reachable and render without crash.
- Disallowed clinical-edit action path for staff returns deny UX (dialog/message + no mutation).
- Core workflows execute end-to-end: intake → waiting queue handoff, appointment update, invoice create/confirm/print path.

### Must Have
- Dedicated `staff` role path (not aliasing doctor/admin).
- Sidebar exactly aligned to requested sections.
- Dashboard includes requested widgets/sections and actionable quick actions.
- Read-only clinical boundaries for staff.
- Logging or visible feedback for key transitions (check-in, status change, payment confirm).

### Must NOT Have (guardrails, AI slop patterns, scope boundaries)
- No staff write access to clinical diagnosis/treatment record content.
- No broad admin capability inheritance (user/system administration excluded).
- No introduction of large new external frameworks for v1.
- No silent permission failures; always explicit outcome.

## Verification Strategy
> ZERO HUMAN INTERVENTION - all verification is agent-executed.
- Test decision: tests-after + existing Python runtime checks (no formal framework baseline).
- QA policy: Every task includes happy-path and failure/edge scenario execution.
- Evidence: `.sisyphus/evidence/task-{N}-{slug}.{ext}`

## Execution Strategy
### Parallel Execution Waves
> Target: 5-8 tasks per wave.

Wave 1: Role/control foundation and staff shell
- Tasks: 1, 2, 3

Wave 2: Operational modules (parallel by domain)
- Tasks: 4, 5, 6, 7, 9

Wave 3: Remaining modules + hardening + integrated verification
- Tasks: 8, 10, 11

### Dependency Matrix (full, all tasks)
- 1 blocks 2,3,4,5,6,7,8,9,10
- 2 blocks 4,5,6,7,8,9,10
- 3 blocks 4,5,6,7,8,9,10
- 4 blocks 11
- 5 blocks 11
- 6 blocks 11
- 7 blocks 11
- 8 blocks 11
- 9 blocks 11
- 10 blocks 11
- 11 blocks F1-F4

### Agent Dispatch Summary (wave → task count → categories)
- Wave 1 → 3 tasks → `unspecified-high`, `visual-engineering`
- Wave 2 → 5 tasks → `visual-engineering`, `unspecified-high`
- Wave 3 → 3 tasks → `visual-engineering`, `unspecified-high`
- Final Verification → 4 tasks → `oracle`, `unspecified-high`, `deep`

## TODOs
> Implementation + Test = ONE task. Never separate.
> EVERY task includes Agent Profile + Parallelization + QA Scenarios.

- [x] 1. Add canonical `staff` role in auth/domain model

  **What to do**: Extend role constants/validation and auth payload flow so `staff` is first-class from login to main view initialization.
  **Must NOT do**: Must not remap staff to doctor/admin behind the scenes.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: cross-file role contract update.
  - Skills: `[]` - existing code pattern sufficient.
  - Omitted: `[]` - no external docs needed.

  **Parallelization**: Can Parallel: NO | Wave 1 | Blocks: 2,3,4,5,6,7,8,9,10 | Blocked By: none

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/login_view.py` - auth result handoff.
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/controllers/auth_controller.py` - login payload contract.
  - API/Type: `BTL.Nhóm6_Python/healthcare_management/models/user_model.py` - role source.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/main_view.py` - role-based branch dispatch.

  **Acceptance Criteria**:
  - [ ] Staff credentials resolve role=`staff` through auth flow without exception.
  - [ ] Existing roles (`admin`,`doctor`,`patient`) still authenticate and route correctly.

  **QA Scenarios**:
  ```
  Scenario: Happy path - staff login role propagation
    Tool: Bash
    Steps: Run app; authenticate with staff test user; observe main window target view class.
    Expected: Staff role reaches main view and does not fallback to patient path.
    Evidence: .sisyphus/evidence/task-1-staff-role.txt

  Scenario: Failure/edge case - unknown role
    Tool: Bash
    Steps: Authenticate with malformed role fixture or patched test user role.
    Expected: Explicit deny/fallback handling without crash.
    Evidence: .sisyphus/evidence/task-1-staff-role-error.txt
  ```

  **Commit**: YES | Message: `feat(auth): add canonical staff role routing contract` | Files: auth/model/main view role mapping files

- [x] 2. Create Staff dashboard shell and sidebar navigation

  **What to do**: Implement staff dashboard container (new view or extension) with sidebar menu items: Dashboard, Intake, Appointments, Patients, Billing, Services, Notifications, Reports, Settings.
  **Must NOT do**: Do not duplicate entire admin dashboard code if reusable components already exist.

  **Recommended Agent Profile**:
  - Category: `visual-engineering` - Reason: UI layout and navigation assembly.
  - Skills: `[]` - in-repo UI conventions available.
  - Omitted: `[]`.

  **Parallelization**: Can Parallel: NO | Wave 1 | Blocks: 4,5,6,7,8,9,10 | Blocked By: 1

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/dashboard_view.py` - menu/page switch pattern.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/main_view.py` - container wiring.

  **Acceptance Criteria**:
  - [ ] Staff sidebar renders all requested sections in correct order.
  - [ ] Clicking each menu item switches to corresponding page container.

  **QA Scenarios**:
  ```
  Scenario: Happy path - full menu traversal
    Tool: Bash
    Steps: Login as staff; click each sidebar item sequentially.
    Expected: Corresponding panel loads with no exception or blank crash.
    Evidence: .sisyphus/evidence/task-2-staff-sidebar.txt

  Scenario: Failure/edge case - invalid page key
    Tool: Bash
    Steps: Trigger navigation with unknown key (dev hook/test action).
    Expected: Graceful fallback to dashboard + warning log/dialog.
    Evidence: .sisyphus/evidence/task-2-staff-sidebar-error.txt
  ```

  **Commit**: YES | Message: `feat(staff-ui): add staff dashboard shell and sidebar` | Files: staff dashboard/main view wiring

- [x] 3. Enforce staff permission guardrails and deny UX

  **What to do**: Add centralized permission checks for staff actions to block clinical-record edits and any out-of-scope admin operations; define consistent deny message/redirect behavior.
  **Must NOT do**: Do not rely only on hidden buttons; backend/controller action paths must also guard.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: authorization consistency across UI and actions.
  - Skills: `[]`.
  - Omitted: `[]`.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: 11 | Blocked By: 1

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/doctor_management_views.py` - sensitive clinical actions to restrict.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/admin_management_views.py` - admin-only capabilities to keep excluded.

  **Acceptance Criteria**:
  - [ ] Staff cannot edit diagnosis/treatment/prescription fields from any reachable path.
  - [ ] Forbidden action shows explicit deny UX and leaves persisted data unchanged.

  **QA Scenarios**:
  ```
  Scenario: Happy path - allowed staff action
    Tool: Bash
    Steps: Staff performs check-in or invoice confirm action.
    Expected: Action succeeds and state updates normally.
    Evidence: .sisyphus/evidence/task-3-permissions.txt

  Scenario: Failure/edge case - forbidden clinical edit
    Tool: Bash
    Steps: Staff opens any route/dialog exposing clinical edit and attempts save.
    Expected: Save blocked, explicit "Access denied" feedback, no DB mutation.
    Evidence: .sisyphus/evidence/task-3-permissions-error.txt
  ```

  **Commit**: YES | Message: `feat(staff-auth): enforce non-clinical permission boundaries` | Files: permission checks + guarded actions

- [x] 4. Build Staff Dashboard overview widgets

  **What to do**: Implement top KPI cards and dashboard blocks: today patients, today appointments, unpaid invoices, paid invoices, today appointments table, waiting intake list, quick actions, notifications, service distribution, today checklist.
  **Must NOT do**: No deep analytics/admin-level reporting in this task.

  **Recommended Agent Profile**:
  - Category: `visual-engineering` - Reason: dashboard composition and data binding.
  - Skills: `[]`.
  - Omitted: `[]`.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: 11 | Blocked By: 2

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/dashboard_view.py` - KPI card and table layout style.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/admin_management_views.py` - list/table widget patterns.

  **Acceptance Criteria**:
  - [ ] Dashboard renders all requested sections with populated placeholders or live values.
  - [ ] Appointment table contains columns: time, patient, service, doctor, status, action.

  **QA Scenarios**:
  ```
  Scenario: Happy path - dashboard completeness
    Tool: Bash
    Steps: Login staff; inspect all dashboard blocks and click each quick action button.
    Expected: Each action opens corresponding module without crash.
    Evidence: .sisyphus/evidence/task-4-dashboard.txt

  Scenario: Failure/edge case - empty day data
    Tool: Bash
    Steps: Use test dataset with zero appointments/patients for day.
    Expected: Empty-state messages shown; UI remains usable.
    Evidence: .sisyphus/evidence/task-4-dashboard-error.txt
  ```

  **Commit**: YES | Message: `feat(staff-ui): add staff dashboard widgets and quick actions` | Files: staff dashboard views

- [x] 5. Implement Patient Intake flow for front desk

  **What to do**: Build intake page/form for CCCD/SĐT lookup, existing-patient retrieval, new profile creation, check-in confirmation, and transfer to doctor waiting queue.
  **Must NOT do**: Do not include clinical diagnosis entry fields.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: mixed UI + workflow/state transitions.
  - Skills: `[]`.
  - Omitted: `[]`.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: 11 | Blocked By: 2

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/admin_management_views.py` - patient CRUD dialog patterns.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/doctor_management_views.py` - waiting/appointment linkage patterns.

  **Acceptance Criteria**:
  - [ ] Lookup by CCCD/SĐT returns existing patient or explicit "not found" state.
  - [ ] New patient creation validates required fields and persists.
  - [ ] Check-in moves patient to waiting queue tied to selected appointment/doctor.

  **QA Scenarios**:
  ```
  Scenario: Happy path - returning patient check-in
    Tool: Bash
    Steps: Search by existing CCCD; confirm patient; perform check-in.
    Expected: Patient status becomes checked-in/waiting and appears in waiting list.
    Evidence: .sisyphus/evidence/task-5-intake.txt

  Scenario: Failure/edge case - missing identity inputs
    Tool: Bash
    Steps: Submit intake form with empty CCCD/SĐT.
    Expected: Validation error shown; no record created/updated.
    Evidence: .sisyphus/evidence/task-5-intake-error.txt
  ```

  **Commit**: YES | Message: `feat(staff-intake): implement lookup, create, and check-in workflow` | Files: staff intake view + related handlers

- [x] 6. Implement Appointment Management center for staff

  **What to do**: Add staff appointment page with create, reschedule, cancel, select doctor, select service, and status updates for front-desk coordination.
  **Must NOT do**: Do not allow editing completed clinical outcomes.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: business rules + scheduling states.
  - Skills: `[]`.
  - Omitted: `[]`.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: 11 | Blocked By: 2

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/admin_management_views.py` - appointment management patterns.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/doctor_management_views.py` - doctor linkage/status conventions.

  **Acceptance Criteria**:
  - [ ] Staff can create appointment with required patient-doctor-service-time fields.
  - [ ] Reschedule/cancel actions update status and visible schedule list immediately.
  - [ ] `[DECISION NEEDED: Policy for modifying in-progress/completed appointments]` is implemented per chosen rule.

  **QA Scenarios**:
  ```
  Scenario: Happy path - create and reschedule appointment
    Tool: Bash
    Steps: Create new appointment; then reschedule to another time.
    Expected: Both operations persist; table reflects latest status/time.
    Evidence: .sisyphus/evidence/task-6-appointments.txt

  Scenario: Failure/edge case - conflicting slot
    Tool: Bash
    Steps: Attempt booking same doctor/time slot already occupied.
    Expected: Conflict error displayed; appointment not saved.
    Evidence: .sisyphus/evidence/task-6-appointments-error.txt
  ```

  **Commit**: YES | Message: `feat(staff-schedule): add appointment coordination module` | Files: staff appointment page + handlers

- [x] 7. Implement Patient List + read-only history view for staff

  **What to do**: Provide searchable patient list and read-only detail pane with basic profile, appointment history, and visit timeline appropriate for front-desk use.
  **Must NOT do**: Do not enable mutation of diagnosis/treatment notes.

  **Recommended Agent Profile**:
  - Category: `visual-engineering` - Reason: list/detail UX and filtering.
  - Skills: `[]`.
  - Omitted: `[]`.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: 11 | Blocked By: 2,3

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/patient_view.py` - patient info display patterns.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/admin_management_views.py` - patient search/list components.

  **Acceptance Criteria**:
  - [ ] Search by name/phone/ID returns matching patients.
  - [ ] Staff can view appointment history and non-clinical timeline.
  - [ ] `[DECISION NEEDED: clinical-note visibility level for staff]` enforced exactly.

  **QA Scenarios**:
  ```
  Scenario: Happy path - patient lookup and history view
    Tool: Bash
    Steps: Search existing patient; open detail/history.
    Expected: Correct identity + appointment timeline visible in read-only mode.
    Evidence: .sisyphus/evidence/task-7-patient-list.txt

  Scenario: Failure/edge case - unauthorized edit attempt
    Tool: Bash
    Steps: Attempt editing any clinical note field from patient detail context.
    Expected: Edit controls absent/disabled; save action blocked with explicit message.
    Evidence: .sisyphus/evidence/task-7-patient-list-error.txt
  ```

  **Commit**: YES | Message: `feat(staff-patients): add searchable patient list and read-only history` | Files: staff patient list/detail views

- [x] 8. Implement Billing & Invoice operations for staff

  **What to do**: Build staff billing page to create invoice, confirm payment, print receipt, and review payment history for front-desk completion after consultation.
  **Must NOT do**: No refund/void/adjust historical finance flows unless explicitly approved.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: transactional state management and safeguards.
  - Skills: `[]`.
  - Omitted: `[]`.

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: 11 | Blocked By: 2,3

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/admin_management_views.py` - payment/invoice UI and controller interactions.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/dashboard_view.py` - summary count integration pattern.

  **Acceptance Criteria**:
  - [ ] Staff can create invoice linked to patient visit.
  - [ ] Staff can confirm payment and status transitions to paid.
  - [ ] Print action executes and handles printer-unavailable case gracefully.
  - [ ] `[DECISION NEEDED: whether staff may void/refund invoices]` enforced.

  **QA Scenarios**:
  ```
  Scenario: Happy path - post-visit payment completion
    Tool: Bash
    Steps: Open billing module; create invoice; confirm payment; trigger print.
    Expected: Invoice status paid; payment appears in history; print workflow returns success state.
    Evidence: .sisyphus/evidence/task-8-billing.txt

  Scenario: Failure/edge case - duplicate payment confirm
    Tool: Bash
    Steps: Attempt confirming payment on already-paid invoice.
    Expected: Blocked with informative message; no duplicate transaction.
    Evidence: .sisyphus/evidence/task-8-billing-error.txt
  ```

  **Commit**: YES | Message: `feat(staff-billing): implement invoice and payment handling` | Files: staff billing views + handlers

- [x] 9. Implement Services/Care Packages lookup module

  **What to do**: Provide searchable service catalog for staff consulting and appointment support (service name, category, price, short description).
  **Must NOT do**: Do not include admin-level service CRUD unless explicitly approved.

  **Recommended Agent Profile**:
  - Category: `visual-engineering` - Reason: lookup UX and filtering.
  - Skills: `[]`.
  - Omitted: `[]`.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: 11 | Blocked By: 2

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/admin_management_views.py` - service list presentation pattern.

  **Acceptance Criteria**:
  - [ ] Staff can find services by name/type and view pricing quickly.
  - [ ] Staff can link selected service into appointment/invoice context.

  **QA Scenarios**:
  ```
  Scenario: Happy path - service consult and attach
    Tool: Bash
    Steps: Search service; select one; attach to new appointment/invoice flow.
    Expected: Selected service metadata propagates correctly (name/price).
    Evidence: .sisyphus/evidence/task-9-services.txt

  Scenario: Failure/edge case - missing service selection
    Tool: Bash
    Steps: Attempt appointment/invoice save without required service where applicable.
    Expected: Validation message shown; save blocked.
    Evidence: .sisyphus/evidence/task-9-services-error.txt
  ```

  **Commit**: YES | Message: `feat(staff-services): add service catalog lookup for front desk` | Files: staff service lookup page

- [x] 10. Implement Notifications, Quick Reports, and Staff Settings

  **What to do**: Add three staff modules: notifications feed (new/cancelled appointments, waiting patients, unpaid invoices), quick reports (today counts/revenue/appointments), and staff settings (profile/password/logout).
  **Must NOT do**: No clinic-wide system configuration controls.

  **Recommended Agent Profile**:
  - Category: `visual-engineering` - Reason: multi-panel UI composition.
  - Skills: `[]`.
  - Omitted: `[]`.

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: 11 | Blocked By: 2

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/dashboard_view.py` - summary/report card style.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/login_view.py` - logout flow pattern.

  **Acceptance Criteria**:
  - [ ] Notifications show key operational events with timestamp and status.
  - [ ] Reports page shows today KPIs expected by staff (patients, appointments, revenue/unpaid).
  - [ ] Settings supports password/profile update and logout return to login screen.

  **QA Scenarios**:
  ```
  Scenario: Happy path - notifications and settings workflow
    Tool: Bash
    Steps: Open notifications; verify event list; update password/profile; logout.
    Expected: Updates succeed; logout returns to login view.
    Evidence: .sisyphus/evidence/task-10-notify-report-settings.txt

  Scenario: Failure/edge case - invalid password change
    Tool: Bash
    Steps: Submit weak/mismatched password in settings.
    Expected: Validation error shown; password unchanged.
    Evidence: .sisyphus/evidence/task-10-notify-report-settings-error.txt
  ```

  **Commit**: YES | Message: `feat(staff-ops): add notifications reports and staff settings` | Files: staff notifications/reports/settings views

- [x] 11. End-to-end staff flow integration and regression hardening

  **What to do**: Validate integrated workflow across modules: intake → waiting → appointment updates → billing completion; ensure no regressions for admin/doctor/patient routing.
  **Must NOT do**: Do not mark complete without evidence artifacts for all listed scenarios.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: system integration verification.
  - Skills: `[]`.
  - Omitted: `[]`.

  **Parallelization**: Can Parallel: NO | Wave 3 | Blocks: F1-F4 | Blocked By: 3,4,5,6,7,8,9,10

  **References**:
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/views/main_view.py` - role-based entrypoint.
  - Pattern: `BTL.Nhóm6_Python/healthcare_management/main.py` - application startup path.

  **Acceptance Criteria**:
  - [ ] Full staff workflow executes without uncaught exception.
  - [ ] Legacy roles still route to original dashboards and key pages.
  - [ ] Evidence bundle exists for all task scenarios.

  **QA Scenarios**:
  ```
  Scenario: Happy path - full daily staff flow
    Tool: Bash
    Steps: Login staff; intake patient; confirm queue; update appointment; complete payment; print receipt.
    Expected: Every state transition visible and persisted end-to-end.
    Evidence: .sisyphus/evidence/task-11-e2e-flow.txt

  Scenario: Failure/edge case - module interruption recovery
    Tool: Bash
    Steps: Simulate failure mid-flow (e.g., billing confirm failure); return to dashboard and retry.
    Expected: Partial state is consistent, retry succeeds or fails cleanly with no corruption.
    Evidence: .sisyphus/evidence/task-11-e2e-flow-error.txt
  ```

  **Commit**: YES | Message: `fix(staff): harden integrated staff workflow and regressions` | Files: cross-module fixes and route protections

## Final Verification Wave (MANDATORY — after ALL implementation tasks)
> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.
> **Do NOT auto-proceed after verification. Wait for user's explicit approval before marking work complete.**
> **Never mark F1-F4 as checked before getting user's okay.** Rejection or user feedback -> fix -> re-run -> present again -> wait for okay.
- [x] F1. Plan Compliance Audit — oracle
- [x] F2. Code Quality Review — unspecified-high
- [x] F3. Real Manual QA — unspecified-high (+ playwright if UI)
- [x] F4. Scope Fidelity Check — deep

## Commit Strategy
- Commit per module cluster (foundation, operations, verification hardening) to keep revertable boundaries.
- Conventional format: `feat(staff): ...`, `refactor(auth): ...`, `fix(staff): ...`.

## Success Criteria
- Staff can complete daily front-desk flow in one role-specific workspace without accessing clinical-edit capabilities.
- No regressions in admin/doctor/patient login routing.
- Operational UI states are explicit, auditable, and consistent.
