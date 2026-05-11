
## 2026-05-11 - Task 1 blockers

- Pytest baseline command trong plan (`python -m pytest -q`) bị block do môi trường không có alias `python`.
  - Repro: chạy tại `BTL.Nhóm6_Python/healthcare_management`
  - Output: `/bin/bash: dòng 1: python: không tìm thấy lệnh`

- Pytest fallback (`python3 -m pytest -q`) tiếp tục bị block do thiếu package `pytest` trong runtime hiện tại.
  - Output: `/usr/bin/python3: No module named pytest`

- App-launch smoke (`python3 main.py` hoặc `python3 BTL.Nhóm6_Python/healthcare_management/main.py`) bị block trước login do import path mismatch.
  - Failing module: `controllers/patient_controller.py`
  - Error: `ModuleNotFoundError: No module named 'healthcare_management'`

- Đây là blocker môi trường/package import, chưa phải blocker DB schema; task baseline đã ghi nhận đầy đủ trong evidence để các task sau quyết định hướng xử lý.

## 2026-05-11 - Task 4 diagnostics note

- `lsp_diagnostics` cho `staff_dashboard_view.py` sau task issue #20 vẫn còn error mức môi trường/baseline: thiếu `PyQt6` trong môi trường phân tích và repo dùng import kiểu `from controllers...` nên basedpyright báo `reportImplicitRelativeImport`.
- Sau khi vá các lỗi logic thật vừa lộ ra trong cùng file, verify đáng tin cậy cho task này vẫn là `python3 -m py_compile BTL.Nhóm6_Python/healthcare_management/views/staff_dashboard_view.py` (đã pass).
- Review note (staff suite): `update_staff_personal_info()` updates `Patients` and `UserSettings` via separate committed `execute()` calls, so a failed rollback leaves partial writes and inconsistent staff profile state.
- Review note (staff reports): report KPIs mix global `ReportController.get_core_totals()` with period-filtered appointment/payment rows, so filtered views can silently present all-time patient/revenue totals beside filtered counts.
- Review note (notifications): `_focus_staff_notification_source()` only scans the first 8 appointments and current filtered billing rows, so 'Đi tới nguồn dữ liệu' can report success without actually focusing the referenced record.
- Review note (settings UX): the 'Tự động xác nhận lịch hẹn sau khi tạo' checkbox persists `notify_new_appointment`, which is a notification flag, not auto-confirm behavior; the label promises a behavior the code never implements.

- 2026-05-11: Re-check QA readiness found `python3 -m py_compile views/staff_dashboard_view.py` passes, but runtime entry remains blocked by import-path/package mismatch (`main.py` -> `healthcare_management` / `views` resolution depends on launch context).
- Existing evidence shows prior bounded startup smoke and offscreen page-switch probe passed, but this host cannot currently reproduce an executable end-to-end or startup path without import fixes and lacks pytest in the active interpreter.

## 2026-05-11 - Final QA evidence recheck

- Current evidence set still contains clear traces for `MAIN_RUNTIME_OK` and `SERVICE_SCOPE_SAFE_OK`, and code inspection confirms `main.py` bootstrap plus `staff_dashboard_view.py` guards/switch routing still match those claims.
- No current repo evidence/notepad entry exposes the required token `STAFF_SUITE_MANUAL_QA_OK`; under the final review gate, this leaves the deeper multi-page manual QA proof incomplete even if the shipping threshold now accepts truthful placeholders.

## 2026-05-11 - Final manual QA recheck after task-13 artifact

- Recheck after adding :  and  are now explicit in current evidence, and existing offscreen/switch-page proofs still support navigation stability.
- Shipping threshold override allows truthful placeholders for non-critical advanced features, so the remaining gate is proof completeness rather than UI polish.
- Final review still cannot approve because no standalone current evidence artifact was found carrying ; the token only appears in notepad text, while several older page-specific artifacts still declare .

## 2026-05-11 - Final manual QA recheck after task-13 artifact

- Recheck after adding `task-13-staff-suite-manual-qa.txt`: `MAIN_RUNTIME_OK` and `STAFF_SUITE_MANUAL_QA_OK` are now explicit in current evidence, and existing offscreen/switch-page proofs still support navigation stability.
- Shipping threshold override allows truthful placeholders for non-critical advanced features, so the remaining gate is proof completeness rather than UI polish.
- Final review still cannot approve because no standalone current evidence artifact was found carrying `SERVICE_SCOPE_SAFE_OK`; the token only appears in notepad text, while several older page-specific artifacts still declare `PARTIAL/UNVERIFIED RUNTIME`.
