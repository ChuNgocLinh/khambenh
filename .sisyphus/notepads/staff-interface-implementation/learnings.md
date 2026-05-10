## 2026-05-09T15:10:00Z Task: init
Initialized notepad. Key baseline: PyQt6 desktop app, no automated test infrastructure detected.

## 2026-05-09T15:35:00Z Task: canonical-staff-role
- Added `UserModel.normalize_role()` to enforce lowercase role values and map legacy `patient`+`staff*` usernames to canonical `staff` without changing DB schema.
- Kept auth payload contract stable (`status`, `user`, `role`) while ensuring `user.role` and top-level `role` are synchronized after normalization.
- Main role routing now has explicit `staff` branch (separate from patient fallback) and a safe unknown-role UI path to avoid crashes.

## 2026-05-09T16:05:00Z Task: staff-dashboard-shell
- Added dedicated `StaffDashboardView` (`views/staff_dashboard_view.py`) using existing admin/dashboard PyQt shell conventions: left sidebar + `QStackedWidget` page containers.
- Sidebar order is fixed to 9 required items and each button is connected to `switch_page(idx)` with guarded index checks to prevent invalid stack access.
- `MainView` now mounts staff-specific shell for role `staff` and reuses existing `MainView.logout` by connecting `staff_dashboard.btn_logout.clicked`.

## 2026-05-09T16:40:00Z Task: staff-permission-guardrails
- Added centralized role guards in BaseDoctorView and BaseManagementView so permission checks execute at handler entry points, not only via UI visibility.
- Staff-deny UX is explicit and consistent via QtWidgets.QMessageBox.warning with clear denial reason for clinical record edits and admin management mutations.
- Propagated canonical role context through MainView.user_data['role'] and dashboard-instantiated management pages to preserve doctor/admin behavior while enabling staff restrictions.

## 2026-05-09T17:05:00Z Task: staff-dashboard-overview-widgets
- Replaced the dashboard landing page (stack index 0) with modular widget builders (`_build_dashboard_page`, `_build_section_card`, `_build_kpi_card`, `_build_quick_action_button`) while keeping sidebar/stack switch architecture untouched.
- Implemented all requested staff blocks: KPI cards, appointment table, quick actions, waiting intake list, notifications, lightweight service statistics, and daily checklist with graceful empty-state labels for list/table contexts.
- Wired quick actions directly to existing `switch_page(idx)` flow for intake (1), appointments (2), patients (3), and billing (4), preserving existing role shell behavior and logout/sidebar logic.

## 2026-05-09T17:40:00Z Task: staff-intake-flow
- Implemented a real intake workflow at staff stack index 1 (Tra c?u -> T?o/C?p nh?t -> Check-in) directly in iews/staff_dashboard_view.py with localized handlers and explicit user feedback labels.
- Added minimal patient lookup helpers (PatientModel.get_by_phone, PatientController.find_by_cccd_or_phone) to keep lookup logic reusable while avoiding broad refactors.
- Check-in now uses existing appointment state transition contract via AppointmentController.update_status(..., 'in_progress'), and only targets pending/confirmed appointments tied to the selected patient.
- CCCD input is preserved in UI, but current schema has no Patients.cccd; lookup therefore falls back to S�T (or CCCD-as-phone input) with explicit explanatory feedback to staff.

## 2026-05-09T18:20:00Z Task: staff-appointment-management-center
- Replaced staff stack index 2 placeholder with a dedicated appointment management page in `views/staff_dashboard_view.py`, preserving existing sidebar/stack routing and non-clinical role boundaries.
- Wired create/reschedule/cancel flows to existing `AppointmentController` contracts (`create_with_details`, `update_full`, `update_status`) so conflict/status validations stay centralized and consistent.
- Reused `DoctorController.get_all()` and `ServiceController.get_all()` to populate dropdowns, and added row-selection form binding + explicit feedback messaging so front-desk staff can coordinate appointments without touching clinical outcomes.

## 2026-05-09T19:10:00Z Task: staff-patient-list-readonly-history
- Replaced the stack index 3 placeholder with a dedicated patient lookup module in iews/staff_dashboard_view.py wired into content_stack.addWidget(self._build_staff_patient_list_page()).
- Implemented front-desk split layout: searchable patient table (ID/T�n/S�T) on the left and read-only profile + appointment timeline on the right with explicit empty-state messaging.
- Enforced read-only behavior at widget level (QLineEdit.setReadOnly(True), QTextEdit.setReadOnly(True), history table NoEditTriggers/NoSelection) and avoided any create/update/delete path in this module.

## 2026-05-09T19:30:00Z Task: staff-patient-list-readonly-history-fix-date-field
- Fixed Task 7 history date mapping in iews/staff_dashboard_view.py to prefer canonical ppointment_date and fallback to legacy date for compatibility (history_date = appt.get('appointment_date') or appt.get('date')).
- Confirmed appointment payload conventions across modules: tables and model/controller flows primarily use ppointment_date; fallback is only for compatibility reads.

## 2026-05-09T20:05:00Z Task: staff-billing-invoice-operations
- Implemented a dedicated billing module at staff stack index 4 in `views/staff_dashboard_view.py` (replacing placeholder) while preserving existing sidebar/stack routing.
- Reused existing `PaymentController` operations (`get_all`, `create`, `update_status`) and admin payment status contract (`unpaid`/`paid`) to avoid introducing new billing architecture.
- Added front-desk guardrails in UI handlers: input validation, appointment-to-patient ownership check before invoice create, duplicate invoice prevention by appointment, duplicate confirm prevention for already-paid invoices, and paid-only receipt print with fallback preview message.

## 2026-05-09T23:32:23Z Task: staff-service-lookup-module
- Replaced staff stack index 5 placeholder with a dedicated service lookup page in iews/staff_dashboard_view.py, wired into content_stack for menu item 'D?ch v? & G�i kh�m'.
- Implemented read-only catalog lookup from ServiceController.get_all() with name search + type filter and list fields: service name, category/type, price, summary.
- Added explicit select-service action with visible selected-state feedback; selection now pre-fills local appointment service combo and billing amount suggestion when amount is empty.

## 2026-05-09T21:30:00Z Task: staff-notifications-reports-settings
- Replaced staff placeholders at stack indices 6/7/8 with dedicated pages: Notifications, B�o c�o nhanh, and C�i �?t c� nh�n in iews/staff_dashboard_view.py.
- Notifications feed now aggregates operational events from appointments/payments (new/cancelled/in_progress/unpaid), includes timestamps/status, and has explicit empty-state + mark-handled feedback labels.
- Settings page keeps personal-only scope: in-session profile fields update, password change via SettingsController.change_password validation flow, and logout compatibility through self.btn_logout.click hook reuse.
## 2026-05-09T21:30:00Z Task: staff-flow-integration-hardening
- Added shared workflow context in `views/staff_dashboard_view.py` (`shared_selected_patient_id`, `shared_selected_appointment_id`, `shared_selected_service_name`) to keep intake -> appointment -> billing handoff predictable.
- Centralized context re-apply helpers (`_apply_shared_context_to_appointment_form`, `_apply_shared_context_to_billing_form`) and invoked them on page switches so staff forms are prefilled consistently without changing role routing.
- Hardened interruption UX by wrapping intake/appointment/billing controller write calls with retry-oriented feedback messages when backend operations are temporarily interrupted.
- Added targeted refresh hooks in `switch_page` for appointment/patient/billing/service/notification/report pages to reduce stale cross-module state after actions.
- 2026-05-10: Hardened legacy role normalization in healthcare_management/models/user_model.py from broad startswith('staff') to strict regex ^staff\d+$ when stored role is patient, reducing false-positive staff inference while preserving intended legacy staffN mapping.
## 2026-05-10 Scope-remediation note
- Added `.sisyphus/evidence/scope-traceability-map.md` to map plan tasks T1..T11 to the current git modified-file set with explicit in-scope rationale for reviewer-flagged files and clear runtime/LSP non-provability boundaries.

## 2026-05-09T17:57:45Z Task: explicit-python312-runtime-verification
- Explicit Python312 runtime is now executable via absolute path and can run syntax checks (`py_compile`) on target modules.
- Bounded startup/import smoke checks fail at runtime on missing PyQt6 dependency, so F3 can be evidenced as partially executed rather than no-runtime blocked.

## 2026-05-09T18:11:45Z Task: runtime-smoke-progression
- Verified VC++ 2015+ x64 runtime is installed/upgraded (Installed=1, Version=v14.50.35719.00).
- Confirmed Python runtime deps for smoke path: PyQt6-Qt6==6.5.2 and pyodbc==5.3.0 present under Python312.
- Startup smoke improved: python main.py produced no immediate traceback and remained alive for full 20s timeout (consistent with active GUI/event loop startup).
## 2026-05-09T22:40:00Z F3 offscreen runtime probe
- Running `main.py` with explicit Python312 now stays alive until timeout (no immediate traceback), indicating Qt event loop can start under current dependency set.
- Additional headless probe using `QT_QPA_PLATFORM=offscreen` also keeps process alive during timeout window; this strengthens runtime smoke confidence.
- F3 still requires interactive click-through evidence and cannot be marked APPROVE from smoke-only checks.
## 2026-05-09T23:00:00Z Offscreen interactive probe (runtime)
- With explicit Python312 runtime and offscreen Qt platform, staff shell can be instantiated and navigated across all sidebar indices when controller data providers are monkeypatched for non-DB runtime.
- Observed runtime outcomes: `HAS_STAFF_DASHBOARD=True`, `SWITCH_OK` for 0..8, final `OFFSCREEN_FLOW_RESULT=PASS`.
- This provides stronger runtime evidence than startup smoke alone, while still distinct from full human-visual manual QA.
