## 2026-05-11 - Shipping threshold override

- User explicitly prioritized `basic functional flow` over full polish/spec completeness.
- For this pass, placeholder/truthful UI is acceptable for advanced utilities that do not block core flows:
  - avatar/logo upload persistence
  - restore workflow
  - backup history popup
  - update-check online
  - export file backend
  - real chart engine
- Remaining fixes should only target blockers to opening pages, running primary actions, and avoiding false-success behavior.

## 2026-05-11 - Scope fidelity recheck after runtime bootstrap fix

- Runtime bootstrap in `main.py` stays within launchability support and does not expand domain scope.
- Billing, notifications, reports, and settings pages remain inside the staff page cluster with truthful placeholder messaging for unsupported utilities.
- Reject signal: the staff services page now performs real `ServiceController.create/update/set_active` mutations against `Services`, which exceeds the allowed staff-page shell/lookup scope and drifts toward admin/catalog management.
- No new schema migration was introduced in this pass, but the service CRUD overreach alone breaks the final scope guardrail.

- 2026-05-11: Refreshed `task-13-service-scope-safe.txt` to link `SERVICE_SCOPE_SAFE_OK` with `STAFF_SUITE_MANUAL_QA_OK` and offscreen switch-page proofs, treating non-mutating service placeholders as acceptable under the updated shipping threshold.
2026-05-11 - Final QA readiness recheck
- Under the updated shipping threshold, APPROVE is supported by `MAIN_RUNTIME_OK`, `STAFF_SUITE_MANUAL_QA_OK`, `SERVICE_SCOPE_SAFE_OK`, plus earlier offscreen `switch_page(0..8)` stability proofs.
- Remaining limitation is still truthful: evidence is headless/offscreen rather than human-observed GUI, but the current gate only requires basic functional flow first.
