# Scope Traceability Map (F2/F4 Remediation)

## Source of Truth Used
- Plan tasks: `.sisyphus/plans/staff-interface-implementation.md` (items 1..11 marked complete in plan).
- Modified files: `git status --porcelain` output at remediation time.

Modified-file set used for this mapping:
- `.gitignore`
- `BTL.Nhóm6_Python/healthcare_management/controllers/auth_controller.py`
- `BTL.Nhóm6_Python/healthcare_management/controllers/patient_controller.py`
- `BTL.Nhóm6_Python/healthcare_management/models/patient_model.py`
- `BTL.Nhóm6_Python/healthcare_management/models/user_model.py`
- `BTL.Nhóm6_Python/healthcare_management/views/admin_management_views.py`
- `BTL.Nhóm6_Python/healthcare_management/views/dashboard_view.py`
- `BTL.Nhóm6_Python/healthcare_management/views/doctor_management_views.py`
- `BTL.Nhóm6_Python/healthcare_management/views/login_view.py`
- `BTL.Nhóm6_Python/healthcare_management/views/main_view.py`
- `BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py` (untracked)

## Task-by-task Mapping (T1..T11 -> Changed Files -> Rationale)

### T1. Add canonical `staff` role in auth/domain model
- Files:
  - `models/user_model.py`
  - `controllers/auth_controller.py`
  - `views/main_view.py`
  - `views/login_view.py`
- Rationale:
  - Plan T1 references auth payload contract, role source model, login handoff, and main role dispatch. These files are the direct implementation surface for canonical role propagation (`staff`) from login through app routing.

### T2. Create Staff dashboard shell and sidebar navigation
- Files:
  - `views/staff_dashboard_view.py`
  - `views/main_view.py`
  - `views/dashboard_view.py`
- Rationale:
  - T2 requires a dedicated staff container and sidebar page switching; this is primarily new staff view code plus main-view wiring and pattern alignment with existing dashboard behavior.

### T3. Enforce staff permission guardrails and deny UX
- Files:
  - `views/doctor_management_views.py`
  - `views/admin_management_views.py`
  - `views/main_view.py`
- Rationale:
  - T3 references restricting sensitive clinical/admin actions. Guarding these action paths necessarily touches doctor/admin management view handlers and role context wiring.

### T4. Build Staff Dashboard overview widgets
- Files:
  - `views/staff_dashboard_view.py`
  - `views/dashboard_view.py`
- Rationale:
  - T4 is dashboard block/KPI composition for staff; implementation is in staff dashboard view, with existing dashboard view used as layout/pattern baseline.

### T5. Implement Patient Intake flow for front desk
- Files:
  - `views/staff_dashboard_view.py`
  - `controllers/patient_controller.py`
  - `models/patient_model.py`
- Rationale:
  - T5 requires patient lookup/create/check-in workflow. That couples staff intake UI with patient controller/model methods used for lookup and persistence.

### T6. Implement Appointment Management center for staff
- Files:
  - `views/staff_dashboard_view.py`
  - `views/admin_management_views.py`
- Rationale:
  - T6 requires appointment creation/reschedule/cancel UI and status coordination. Staff page logic and reused/parallel appointment patterns in management views are in-scope.

### T7. Implement Patient List + read-only history view for staff
- Files:
  - `views/staff_dashboard_view.py`
  - `views/doctor_management_views.py`
- Rationale:
  - T7 requires list/search and read-only history semantics. Staff UI pages implement this while doctor-side clinical-edit surfaces are relevant for explicit read-only restrictions.

### T8. Implement Billing & Invoice operations for staff
- Files:
  - `views/staff_dashboard_view.py`
  - `views/admin_management_views.py`
  - `views/dashboard_view.py`
- Rationale:
  - T8 covers invoice/payment/print operations and dashboard counters; these align with staff billing UI plus management/dashboard pattern reuse.

### T9. Implement Services/Care Packages lookup module
- Files:
  - `views/staff_dashboard_view.py`
  - `views/admin_management_views.py`
- Rationale:
  - T9 requires service lookup/filter and downstream selection context, implemented in staff modules and aligned with existing service-list presentation patterns.

### T10. Implement Notifications, Quick Reports, and Staff Settings
- Files:
  - `views/staff_dashboard_view.py`
  - `views/dashboard_view.py`
  - `views/login_view.py`
- Rationale:
  - T10 explicitly includes notifications/reports/settings and logout behavior; this maps to staff UI implementation plus existing report-card and logout-flow patterns.

### T11. End-to-end staff flow integration and regression hardening
- Files:
  - `views/main_view.py`
  - `views/staff_dashboard_view.py`
  - `main.py` (referenced by plan as startup path; no current diff shown)
- Rationale:
  - T11 is integration across role entrypoint and module flow; the modified files indicate entrypoint/flow wiring changes in views, while startup validation is referenced as verification scope.

## Explicit In-scope Justification for Reviewer-flagged Files

### `.gitignore`
- In-scope as delivery hygiene for evidence/remediation artifacts and local run byproducts generated during staff-interface implementation and verification.
- It does not alter runtime behavior; it constrains repository tracking noise for this workstream.

### `controllers/auth_controller.py`
- In-scope by T1 (canonical staff role in auth payload flow).
- Plan references auth login payload contract directly for staff role propagation.

### `models/user_model.py`
- In-scope by T1 (role source, normalization/validation surface).
- Plan references role source model as required change point for first-class `staff` role.

### `views/main_view.py`
- In-scope by T1/T2/T11 (role-based dispatch, staff dashboard mounting, integration path).
- Plan references main view dispatch and role entrypoint behavior explicitly.

## Known Blockers / Unprovable Items (Runtime + LSP)
- This remediation task is documentation-only and does not execute runtime flows.
- Therefore, claims about end-to-end UI behavior (e.g., each sidebar path rendering, payment transitions, printer handling) are **not re-proven here**; they remain dependent on previously generated evidence files and/or fresh runtime execution.
- LSP diagnostics for Markdown evidence files may be unavailable or non-authoritative in this environment; zero-runtime/lint failures cannot be inferred from this document alone.
- `main.py` is referenced by plan T11 but not present in current modified-file list, so startup-path changes are not attributable from git diff alone.

## Out-of-scope Changes Check
- For this remediation unit, no application-code changes were made.
- Evidence scope: creation of this traceability artifact only, plus append-only notepad update.
- No existing evidence files were altered or deleted.
