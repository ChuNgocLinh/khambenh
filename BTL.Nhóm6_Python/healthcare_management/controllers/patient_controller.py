from models.patient_model import PatientModel


class PatientController:

    # 🔹 LẤY DANH SÁCH BỆNH NHÂN
    @staticmethod
    def get_all():
        return PatientModel.get_all()

    @staticmethod
    def find_by_cccd_or_phone(cccd=None, phone=None):
        normalized_phone = str(phone or "").strip()
        normalized_cccd = str(cccd or "").strip()

        # Current DB schema has no CCCD column; retain CCCD input for intake UX
        # and fall back to phone-based lookup when available.
        lookup_phone = normalized_phone or normalized_cccd
        if not lookup_phone:
            return None

        return PatientModel.get_by_phone(lookup_phone)


    # 🔹 TẠO BỆNH NHÂN (DÙNG CHO FORM WEB)
    @staticmethod
    def create(form):
        return PatientModel.create(
            form.get("name"),
            form.get("dob"),
            form.get("gender"),
            form.get("phone"),
            form.get("address")
        )


    # 🔹 CẬP NHẬT
    @staticmethod
    def update(patient_id, form):
        return PatientModel.update(
            patient_id,
            form.get("name"),
            form.get("dob"),
            form.get("gender"),
            form.get("phone"),
            form.get("address")
        )


    # 🔹 XÓA
    @staticmethod
    def delete(patient_id):
        return PatientModel.delete(patient_id)
