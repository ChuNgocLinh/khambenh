"""Report aggregation controller for admin dashboard."""
# pyright: reportImplicitRelativeImport=false

try:
    from ..models.report_model import ReportModel
except Exception:  # pragma: no cover - fallback for direct script imports.
    from models.report_model import ReportModel

from controllers.scoping_helper import enforce_admin_or_staff


class ReportController:
    @staticmethod
    def get_core_totals(user_context=None):
        if user_context is not None:
            enforce_admin_or_staff(user_context)
        payload = ReportModel.get_report_payload(range_days=0)
        summary = payload.get("summary", {})
        if not isinstance(summary, dict):
            summary = {}

        total_patients = summary.get("total_patients", 0)
        total_revenue = summary.get("total_revenue", 0)
        total_transactions = summary.get("total_transactions", 0)

        return {
            "total_patients": int(total_patients or 0),
            "total_appointments": int(total_transactions or 0),
            "total_revenue": float(total_revenue or 0),
        }

    @staticmethod
    def get_filter_options(user_context=None):
        if user_context is not None:
            enforce_admin_or_staff(user_context)
        doctors = ReportModel.get_active_doctors()
        groups = ReportModel.get_service_groups()
        return {
            "doctors": doctors,
            "groups": groups,
            "ranges": [
                {"label": "7 ngày qua", "value": 7},
                {"label": "30 ngày qua", "value": 30},
                {"label": "90 ngày qua", "value": 90},
                {"label": "Tất cả", "value": 0},
            ],
            "report_types": [
                "Tổng quan",
                "Doanh thu",
                "Thanh toán",
                "Bệnh nhân",
                "Dịch vụ",
                "Bác sĩ",
                "Thuốc",
            ],
        }

    @staticmethod
    def get_report_stats(range_days=30, group_name="Tất cả", doctor_name="Tất cả", user_context=None):
        if user_context is not None:
            enforce_admin_or_staff(user_context)
        return ReportModel.get_report_payload(
            range_days=range_days,
            group_name=group_name,
            doctor_name=doctor_name,
        )
