from datetime import datetime, timedelta

from PyQt6 import QtCore

from views.dashboard_view import DashboardView


def test_dashboard_data_uses_controller_rows(monkeypatch):
    now = datetime.now()
    appointment_date = (now + timedelta(days=1)).strftime("%Y-%m-%d 09:00:00")
    monkeypatch.setattr(
        "controllers.appointment_controller.AppointmentController.get_by_doctor",
        lambda doctor_id: [
            {
                "appointment_id": 1,
                "patient_id": 2,
                "appointment_date": appointment_date,
                "status": "done",
                "patient_name": "Nguyen Van A",
            },
            {
                "appointment_id": 2,
                "patient_id": 3,
                "appointment_date": appointment_date,
                "status": "confirmed",
                "patient_name": "Tran Thi B",
            },
        ],
    )
    monkeypatch.setattr(
        "database.db.fetch_all",
        lambda query, params=(): [
            {
                "record_id": 9,
                "created_at": appointment_date,
                "diagnosis": "Flu",
                "treatment": "Rest",
                "patient_id": 2,
                "patient_name": "Nguyen Van A",
                "appointment_status": "done",
                "appointment_date": appointment_date,
                "prescription_id": 10,
                "quantity": 1,
                "medicine_name": "Paracetamol",
                "medicine_description": "Pain relief",
                "visit_type": "Khám tổng quát",
            }
        ],
    )

    view = DashboardView.__new__(DashboardView)
    view.dashboard_filter_state = {
        "from_date": QtCore.QDate.currentDate().addDays(-1),
        "to_date": QtCore.QDate.currentDate().addDays(1),
    }

    data = DashboardView._build_doctor_dashboard_data(view, 1)

    assert data["kpis"]["total_appointments"] == 2
    assert data["kpis"]["prescriptions"] == 1
    assert data["status_counts"]["done"] == 1
    assert data["status_counts"]["confirmed"] == 1
    assert data["upcoming_appointments"]


def test_dashboard_data_empty_state(monkeypatch):
    monkeypatch.setattr("controllers.appointment_controller.AppointmentController.get_by_doctor", lambda doctor_id: [])
    monkeypatch.setattr("database.db.fetch_all", lambda query, params=(): [])

    view = DashboardView.__new__(DashboardView)
    view.dashboard_filter_state = {
        "from_date": QtCore.QDate.currentDate().addDays(-1),
        "to_date": QtCore.QDate.currentDate().addDays(1),
    }

    data = DashboardView._build_doctor_dashboard_data(view, 1)

    assert data["kpis"]["total_appointments"] == 0
    assert data["upcoming_appointments"] == []
    assert data["notifications"]
