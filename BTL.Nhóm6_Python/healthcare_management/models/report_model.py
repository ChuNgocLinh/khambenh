from datetime import date, datetime, timedelta

from database.db import fetch_all


class ReportModel:
    @staticmethod
    def _rows(query, params=()):
        rows = fetch_all(query, params) or []
        return [row for row in rows if isinstance(row, dict)]

    @staticmethod
    def _as_float(value, default=0.0):
        try:
            return float(value or 0)
        except (TypeError, ValueError):
            return float(default)

    @staticmethod
    def _as_int(value, default=0):
        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return int(default)

    @staticmethod
    def _as_text(value, default=""):
        if value is None:
            return default
        return str(value)

    @staticmethod
    def _parse_date(value):
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        text = ReportModel._as_text(value).strip()
        if not text:
            return None
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y", "%d/%m/%Y %H:%M"):
            try:
                return datetime.strptime(text[:19], fmt).date()
            except ValueError:
                continue
        return None

    @staticmethod
    def _format_short_date(value):
        parsed = ReportModel._parse_date(value)
        if not parsed:
            return ReportModel._as_text(value)
        return parsed.strftime("%d/%m")

    @staticmethod
    def _normalize_doctor_name(doctor_name):
        name = ReportModel._as_text(doctor_name).strip()
        if name.lower().startswith("bs."):
            name = name[3:].strip()
        return name

    @staticmethod
    def _resolve_period_days(range_days):
        try:
            days = int(range_days or 0)
        except (TypeError, ValueError):
            days = 0
        return max(days, 0)

    @staticmethod
    def _resolve_bounds(range_days):
        days = ReportModel._resolve_period_days(range_days)
        if days <= 0:
            return None, None
        today = date.today()
        start = today - timedelta(days=max(days - 1, 0))
        end = today + timedelta(days=1)
        return start, end

    @staticmethod
    def get_active_doctors():
        return ReportModel._rows(
            """
            SELECT doctor_id, name
            FROM Doctors
            WHERE COALESCE(is_active, 1) = 1
            ORDER BY name ASC
            """
        )

    @staticmethod
    def get_service_groups():
        return ReportModel._rows(
            """
            SELECT DISTINCT category
            FROM Services
            WHERE COALESCE(is_active, 1) = 1
              AND category IS NOT NULL
              AND TRIM(category) <> ''
            ORDER BY category ASC
            """
        )

    @staticmethod
    def _payment_scope_rows(start_date, end_date, group_name, doctor_name):
        query = """
            SELECT
                p.payment_id,
                p.patient_id,
                p.appointment_id,
                p.total_amount,
                p.method,
                p.status,
                p.payment_date,
                pa.name AS patient_name,
                d.name AS doctor_name,
                COALESCE(service_pick.service_name, CONCAT('Lịch hẹn #', p.appointment_id)) AS service_name,
                service_pick.category AS service_group
            FROM Payments p
            LEFT JOIN Patients pa ON pa.patient_id = p.patient_id
            LEFT JOIN Appointments a ON a.appointment_id = p.appointment_id
            LEFT JOIN Doctors d ON d.doctor_id = a.doctor_id
            LEFT JOIN (
                SELECT i1.payment_id, s1.service_name, s1.category
                FROM Invoices i1
                JOIN Services s1 ON s1.service_id = i1.service_id
                WHERE i1.invoice_id = (
                    SELECT MIN(i2.invoice_id)
                    FROM Invoices i2
                    WHERE i2.payment_id = i1.payment_id
                )
            ) service_pick ON service_pick.payment_id = p.payment_id
            WHERE 1=1
        """
        params = []

        if start_date and end_date:
            query += " AND p.payment_date >= ? AND p.payment_date < ?"
            params.extend([start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")])

        if group_name and group_name != "Tất cả":
            query += " AND EXISTS (SELECT 1 FROM Invoices ig JOIN Services sg ON sg.service_id = ig.service_id WHERE ig.payment_id = p.payment_id AND COALESCE(sg.category, '') = ?)"
            params.append(group_name)

        if doctor_name and doctor_name != "Tất cả":
            query += " AND COALESCE(d.name, '') = ?"
            params.append(doctor_name)

        query += " ORDER BY p.payment_date DESC, p.payment_id DESC"
        return ReportModel._rows(query, tuple(params))

    @staticmethod
    def _service_aggregate_rows(start_date, end_date, group_name, doctor_name):
        query = """
            SELECT
                s.service_name,
                SUM(CASE WHEN p.status = 'paid' THEN COALESCE(i.total_price, i.quantity * i.unit_price, 0) ELSE 0 END) AS revenue,
                SUM(CASE WHEN p.status = 'paid' THEN COALESCE(i.quantity, 0) ELSE 0 END) AS usage_count
            FROM Payments p
            JOIN Invoices i ON i.payment_id = p.payment_id
            JOIN Services s ON s.service_id = i.service_id
            LEFT JOIN Appointments a ON a.appointment_id = p.appointment_id
            LEFT JOIN Doctors d ON d.doctor_id = a.doctor_id
            WHERE 1=1
        """
        params = []

        if start_date and end_date:
            query += " AND p.payment_date >= ? AND p.payment_date < ?"
            params.extend([start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")])

        if group_name and group_name != "Tất cả":
            query += " AND COALESCE(s.category, '') = ?"
            params.append(group_name)

        if doctor_name and doctor_name != "Tất cả":
            query += " AND COALESCE(d.name, '') = ?"
            params.append(doctor_name)

        query += " GROUP BY s.service_name ORDER BY revenue DESC"
        return ReportModel._rows(query, tuple(params))

    @staticmethod
    def _scoped_patient_ids(start_date, end_date, group_name, doctor_name):
        query = """
            SELECT DISTINCT p.patient_id
            FROM Payments p
            LEFT JOIN Appointments a ON a.appointment_id = p.appointment_id
            LEFT JOIN Doctors d ON d.doctor_id = a.doctor_id
            WHERE 1=1
        """
        params = []

        if start_date and end_date:
            query += " AND p.payment_date >= ? AND p.payment_date < ?"
            params.extend([start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")])

        if group_name and group_name != "Tất cả":
            query += " AND EXISTS (SELECT 1 FROM Invoices ig JOIN Services sg ON sg.service_id = ig.service_id WHERE ig.payment_id = p.payment_id AND COALESCE(sg.category, '') = ?)"
            params.append(group_name)

        if doctor_name and doctor_name != "Tất cả":
            query += " AND COALESCE(d.name, '') = ?"
            params.append(doctor_name)

        rows = ReportModel._rows(query, tuple(params))
        ids = {ReportModel._as_int(row.get("patient_id")) for row in rows}
        ids.discard(0)
        return ids

    @staticmethod
    def get_report_payload(range_days=30, group_name="Tất cả", doctor_name="Tất cả"):
        normalized_group = ReportModel._as_text(group_name, "Tất cả").strip()
        normalized_doctor = ReportModel._normalize_doctor_name(doctor_name)
        start_date, end_date = ReportModel._resolve_bounds(range_days)

        payment_rows = ReportModel._payment_scope_rows(
            start_date=start_date,
            end_date=end_date,
            group_name=normalized_group,
            doctor_name=normalized_doctor,
        )
        service_rows = ReportModel._service_aggregate_rows(
            start_date=start_date,
            end_date=end_date,
            group_name=normalized_group,
            doctor_name=normalized_doctor,
        )

        paid_rows = [row for row in payment_rows if ReportModel._as_text(row.get("status")).lower() == "paid"]
        total_revenue = sum(ReportModel._as_float(row.get("total_amount")) for row in paid_rows)
        total_paid_amount = total_revenue
        total_gross_amount = sum(ReportModel._as_float(row.get("total_amount")) for row in payment_rows)

        daily_map = {}
        method_map = {}
        status_map = {}
        for row in payment_rows:
            status = ReportModel._as_text(row.get("status"), "unpaid").strip().lower()
            bucket = status if status in {"paid", "unpaid", "failed"} else "other"
            status_map[bucket] = status_map.get(bucket, 0) + 1

        for row in paid_rows:
            date_key = ReportModel._parse_date(row.get("payment_date"))
            if not date_key:
                continue
            date_label = date_key.strftime("%Y-%m-%d")
            amount = ReportModel._as_float(row.get("total_amount"))
            method = ReportModel._as_text(row.get("method"), "Tiền mặt").strip() or "Tiền mặt"

            daily_map[date_label] = daily_map.get(date_label, 0.0) + amount
            method_map[method] = method_map.get(method, 0.0) + amount

        daily_revenue = []
        for key in sorted(daily_map.keys()):
            amount = daily_map.get(key, 0.0)
            daily_revenue.append(
                {
                    "key": key,
                    "label": ReportModel._format_short_date(key),
                    "amount": amount,
                    "amount_million": amount / 1_000_000,
                }
            )

        payment_methods = []
        for method, amount in sorted(method_map.items(), key=lambda item: item[1], reverse=True):
            percent = (amount / total_revenue * 100) if total_revenue > 0 else 0
            payment_methods.append(
                {
                    "method": method,
                    "amount": amount,
                    "percent": round(percent, 1),
                }
            )

        top_services = []
        for idx, row in enumerate(service_rows[:5], 1):
            top_services.append(
                {
                    "rank": idx,
                    "name": ReportModel._as_text(row.get("service_name"), "Chưa xác định"),
                    "revenue": ReportModel._as_float(row.get("revenue")),
                    "count": ReportModel._as_int(row.get("usage_count")),
                }
            )

        scoped_patient_ids = ReportModel._scoped_patient_ids(
            start_date=start_date,
            end_date=end_date,
            group_name=normalized_group,
            doctor_name=normalized_doctor,
        )
        patients = []
        if scoped_patient_ids:
            placeholders = ", ".join(["?"] * len(scoped_patient_ids))
            patients = ReportModel._rows(
                f"SELECT patient_id, gender, created_at FROM Patients WHERE COALESCE(is_active, 1) = 1 AND patient_id IN ({placeholders})",
                tuple(scoped_patient_ids),
            )

        male_count = sum(1 for row in patients if ReportModel._as_text(row.get("gender")).strip() == "Nam")
        female_count = sum(1 for row in patients if ReportModel._as_text(row.get("gender")).strip() == "Nữ")

        if start_date and end_date:
            new_count = 0
            for row in patients:
                created = ReportModel._parse_date(row.get("created_at"))
                if created and start_date <= created < end_date:
                    new_count += 1
        else:
            new_count = len(patients)

        patient_total = len(patients)
        returning_count = max(patient_total - new_count, 0)

        active_services = ReportModel._rows("SELECT service_id FROM Services WHERE COALESCE(is_active, 1) = 1")
        total_services = len(active_services)

        return {
            "filters": {
                "range_days": ReportModel._resolve_period_days(range_days),
                "group": normalized_group or "Tất cả",
                "doctor": normalized_doctor or "Tất cả",
            },
            "summary": {
                "total_revenue": total_revenue,
                "total_paid": total_paid_amount,
                "total_gross": total_gross_amount,
                "total_patients": patient_total,
                "total_services": total_services,
                "total_transactions": len(payment_rows),
            },
            "daily_revenue": daily_revenue,
            "payment_methods": payment_methods,
            "top_services": top_services,
            "patient_stats": {
                "total": patient_total,
                "new": new_count,
                "returning": returning_count,
                "male": male_count,
                "female": female_count,
            },
            "payment_status": {
                "paid": status_map.get("paid", 0),
                "unpaid": status_map.get("unpaid", 0),
                "failed": status_map.get("failed", 0),
                "other": status_map.get("other", 0),
            },
            "recent_transactions": payment_rows[:10],
        }
