2026-05-10T00:00:00+07:00 - Chuẩn hóa schema intake theo hướng backward-compatible bằng IF COL_LENGTH + ALTER TABLE trên SQL Server để không phá dữ liệu cũ.
2026-05-10T00:00:00+07:00 - Áp dụng queue nội bộ staff 3B bằng bảng WaitingQueue với status chuẩn và unique(queue_no, queue_area) để hỗ trợ xác nhận/chuyển trạng thái hàng chờ.
2026-05-10T00:00:00+07:00 - Chống trùng intake dùng unique index cho CCCD/phone có guard kiểm tra duplicate tồn tại trước khi tạo index, tránh fail migration trên dữ liệu legacy.
[2026-05-10 10:25:20] Task 2: PatientController.find_by_cccd_or_phone now performs deterministic lookup (CCCD first; phone only when CCCD missing). PatientModel create/update now persist full intake fields (name,dob,gender,phone,cccd,address,email,occupation,intake_notes,patient_type). Added create_with_status/update_with_status returning explicit status/message while preserving boolean create/update for backward compatibility.
[2026-05-10 10:28:01] Gate fix: switched PatientController import to absolute package path (healthcare_management.models.patient_model) to satisfy LSP reportImplicitRelativeImport and preserve package module loading in verification scripts.
[2026-05-10 10:31:50] Gate pass stabilization: evidence scripts now run with dual PYTHONPATH (BTL.Nhóm6_Python;BTL.Nhóm6_Python\\healthcare_management), which resolves both healthcare_management.* and database.* imports; lookup/duplicate evidence now contains structured PASS payloads.
[2026-05-10 11:24:35] Task 3: Added staff check-in contract in appointment_controller.confirm_intake_checkin with centralized transition helpers (_can_transition, _resolve_checkin_status) and persisted service+reason note via AppointmentModel.update_intake_checkin.

- [2026-05-10 12:04:53] Task 5: Added complete intake controls for sections 1-4 with state-driven summary refresh hooks and explicit empty-source placeholders for doctor/service comboboxes.

[2026-05-10 12:16:29] Task 6: Hoàn thiện intake lookup/result branches + mode-based validation + save qua PatientController status contract. Evidence files đã tạo: task-6-save-success.txt, task-6-validation-error.png.

- [2026-05-10 12:24:38] Task 7: Added robust intake reset action to clear form inputs, shared selection state, and summary/feedback safely without touching navigation context.

- [2026-05-10 12:25:33] Final artifact pass: regenerated exact PNG evidence path for Task 7 and revalidated both reset artifacts exist.
[2026-05-10 13:17:20] Task 9: Unified intake style tokens/states with primary #1A9B6C via scoped helper styles for inputs/buttons/radios and readable info/success/error feedback badges; preserved intake business logic.
[2026-05-10 13:40:27] Task 10: Staff regression script must validate QStackedWidget via content_stack (not stack) in StaffDashboardView; corrected check produced PASS across dashboard/intake/appointment/patient/notifications/settings and full menu navigation.
[2026-05-10 13:55:30] Task 1 evidence backfill: migration script currently fails on MySQL due to SQL Server syntax in migrate.py; added explicit FAIL evidence for migration and PASS compatibility-read evidence with reproducible commands.
[2026-05-10 14:06:27] Task 1 final-wave remediation: validated init_db.sql on fresh temporary MySQL DB via multi-statement execution (33/33 success), confirmed required Patients intake columns + WaitingQueue existence, and regenerated Task 1 evidence as PASS.
[2026-05-10 14:14:59] F2 remediation: updated Users.role CHECK in init_db.sql to include 'staff'; removed LIMIT 1 from PatientModel CCCD/phone lookups to avoid engine-fragile SQL while preserving deterministic ordering via ORDER BY patient_id DESC; strengthened PatientController duplicate guard with explicit dual-key checks (CCCD + phone) using _find_duplicate_by_keys while keeping existing payload shape/API signatures.
