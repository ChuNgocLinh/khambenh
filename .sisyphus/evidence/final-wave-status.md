# Final Wave Status (Explicit Runtime Verification)

## Current Verdicts
- F1 Plan Compliance Audit: APPROVE
- F2 Code Quality Review: APPROVE
- F3 Real Manual QA: PARTIAL (runtime smoke progressed; no immediate traceback, but full GUI flow still manual/unexecuted)
- F4 Scope Fidelity Check: APPROVE

## Runtime Verification Evidence (UTC 2026-05-09T18:11:45Z)
- VC++ 2015+ x64 runtime installed/upgraded:
  - Command: `Get-ItemProperty HKLM:\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64`
  - Result: `Installed=1`, `Version=v14.50.35719.00`.
- PyQt6-Qt6 pinned as required:
  - Command: `C:\Users\manhc\AppData\Local\Programs\Python\Python312\python.exe -m pip show PyQt6-Qt6`
  - Result: `Version: 6.5.2`.
- pyodbc present:
  - Command: `C:\Users\manhc\AppData\Local\Programs\Python\Python312\python.exe -m pip show pyodbc`
  - Result: `Version: 5.3.0`.
- Startup smoke in explicit Python312 runtime:
  - Command: `C:\Users\manhc\AppData\Local\Programs\Python\Python312\python.exe main.py` (20s timeout)
  - Workdir: `BTL.Nhóm6_Python\healthcare_management`
  - Result: no immediate traceback; process remained alive until timeout (GUI/event-loop likely running).

## F3 Remaining Manual Work
- Rerun startup smoke, then perform manual staff flow click-through (login -> intake -> appointments -> patient list -> billing -> services -> notifications/report/settings -> logout).
- Capture GUI-observed behavior/errors after successful startup.

## Additional Automated Offscreen Probe
- Command: instantiate `MainView('staff', user)` under `QT_QPA_PLATFORM=offscreen` and iterate `staff_dashboard.switch_page(i)`.
- Result: PASS after monkeypatching controller data providers for runtime probe; `HAS_STAFF_DASHBOARD True`, `SWITCH_OK 0..8`, `OFFSCREEN_FLOW_RESULT PASS`.
- Note: DB/ODBC dependency remains environment-sensitive for non-mocked runs.

## Closure Condition
- Full manual GUI flow verification is required to promote F3 from PARTIAL to APPROVE.
