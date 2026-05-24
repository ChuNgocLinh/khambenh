from models.patient_model import PatientModel


class PatientController:

    # 🔹 LẤY DANH SÁCH BỆNH NHÂN
    @staticmethod
    def get_all():
        return PatientModel.get_all()

    @staticmethod
    def get_all_patients():
        # Backward-compatible alias for legacy web handlers.
        return PatientController.get_all()

    @staticmethod
    def get_by_doctor(doctor_id):
        return PatientModel.get_by_doctor(doctor_id)

    @staticmethod
    def get_by_id(patient_id):
        return PatientModel.get_by_id(patient_id)

    @staticmethod
    def _normalize_form(form):
        data = form or {}
        intake_notes = data.get("intake_notes")
        if intake_notes is None:
            intake_notes = data.get("note")

        return {
            "name": data.get("name"),
            "dob": data.get("dob"),
            "gender": data.get("gender"),
            "phone": (str(data.get("phone") or "").strip() or None),
            "cccd": (str(data.get("cccd") or "").strip() or None),
            "address": data.get("address"),
            "email": data.get("email"),
            "occupation": data.get("occupation"),
            "intake_notes": intake_notes,
            "patient_type": data.get("patient_type") or "general",
        }

    @staticmethod
    def _create_status(status, message, data=None):
        payload = {"status": bool(status), "message": message}
        if data is not None:
            payload["data"] = data
        return payload

    @staticmethod
    def find_by_cccd_or_phone(cccd=None, phone=None):
        normalized_cccd = str(cccd or "").strip()
        normalized_phone = str(phone or "").strip()

        # Deterministic lookup: CCCD first (when provided), otherwise phone.
        if normalized_cccd:
            return PatientModel.get_by_cccd(normalized_cccd)
        if normalized_phone:
            return PatientModel.get_by_phone(normalized_phone)
        return None

    @staticmethod
    def find_by_identifier(identifier):
        value = str(identifier or "").strip()
        if not value:
            return None

        upper_value = value.upper()
        if upper_value.startswith("BN"):
            numeric_part = upper_value[2:].lstrip("0") or "0"
            if numeric_part.isdigit():
                return PatientModel.get_by_id(int(numeric_part))

        if value.isdigit():
            patient = PatientModel.get_by_id(int(value))
            if patient:
                return patient

        patient = PatientModel.get_by_cccd(value)
        if patient:
            return patient
        return PatientModel.get_by_phone(value)

    @staticmethod
    def _find_duplicate_by_keys(cccd=None, phone=None):
        normalized_cccd = str(cccd or "").strip()
        normalized_phone = str(phone or "").strip()

        duplicate_cccd = PatientModel.get_by_cccd(normalized_cccd) if normalized_cccd else None
        duplicate_phone = PatientModel.get_by_phone(normalized_phone) if normalized_phone else None

        if duplicate_cccd:
            return duplicate_cccd, "CCCD"
        if duplicate_phone:
            return duplicate_phone, "SĐT"
        return None, None

    @staticmethod
    def create_with_status(form):
        payload = PatientController._normalize_form(form)

        duplicate, duplicate_by = PatientController._find_duplicate_by_keys(
            cccd=payload.get("cccd"),
            phone=payload.get("phone"),
        )
        if duplicate:
            return PatientController._create_status(
                False,
                f"Bệnh nhân đã tồn tại theo {duplicate_by}.",
                {"patient_id": duplicate.get("patient_id")},
            )

        ok = PatientModel.create(
            payload.get("name"),
            payload.get("dob"),
            payload.get("gender"),
            payload.get("phone"),
            payload.get("cccd"),
            payload.get("address"),
            payload.get("email"),
            payload.get("occupation"),
            payload.get("intake_notes"),
            payload.get("patient_type"),
        )
        if not ok:
            return PatientController._create_status(False, "Tạo hồ sơ bệnh nhân thất bại.")

        return PatientController._create_status(True, "Tạo hồ sơ bệnh nhân thành công.")

    @staticmethod
    def update_with_status(patient_id, form):
        payload = PatientController._normalize_form(form)

        duplicate, duplicate_by = PatientController._find_duplicate_by_keys(
            cccd=payload.get("cccd"),
            phone=payload.get("phone"),
        )
        if duplicate and duplicate.get("patient_id") != patient_id:
            return PatientController._create_status(
                False,
                f"Thông tin trùng với bệnh nhân khác theo {duplicate_by}.",
                {"patient_id": duplicate.get("patient_id")},
            )

        ok = PatientModel.update(
            patient_id,
            payload.get("name"),
            payload.get("dob"),
            payload.get("gender"),
            payload.get("phone"),
            payload.get("cccd"),
            payload.get("address"),
            payload.get("email"),
            payload.get("occupation"),
            payload.get("intake_notes"),
            payload.get("patient_type"),
        )
        if not ok:
            return PatientController._create_status(False, "Cập nhật hồ sơ bệnh nhân thất bại.")

        return PatientController._create_status(True, "Cập nhật hồ sơ bệnh nhân thành công.")

    # 🔹 TẠO BỆNH NHÂN (DÙNG CHO FORM WEB)
    @staticmethod
    def create(form):
        # Backward-compatible return for existing callers expecting boolean.
        return PatientController.create_with_status(form).get("status", False)

    # 🔹 CẬP NHẬT
    @staticmethod
    def update(patient_id, form):
        # Backward-compatible return for existing callers expecting boolean.
        return PatientController.update_with_status(patient_id, form).get("status", False)

    # 🔹 XÓA
    @staticmethod
    def delete(patient_id):
        return PatientModel.delete(patient_id)
