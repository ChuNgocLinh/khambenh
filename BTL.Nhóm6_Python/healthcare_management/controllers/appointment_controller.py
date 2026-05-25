from models.appointment_model import AppointmentModel
from models.doctor_model import DoctorModel
from models.service_model import ServiceModel
from models.waiting_queue_model import WaitingQueueModel
from datetime import datetime, timedelta
from config import DEFAULT_SLOTS, DEFAULT_QUEUE_AREA


class AppointmentController:
    VALID_STATUSES = {"pending", "confirmed", "in_progress", "done", "cancelled"}
    START_EXAM_STATUSES = {"pending", "confirmed", "in_progress"}
    ROLES = {"admin", "staff", "doctor", "patient"}
    APPOINTMENT_ACTIONS = [
        "list_all",
        "list_own",
        "view_detail",
        "create",
        "update_time",
        "update_doctor",
        "confirm",
        "start_consultation",
        "complete",
        "cancel",
        "print",
    ]
    APPOINTMENT_RBAC = {
        "list_all": {
            "allow": {"admin", "staff"},
            "deny": {"doctor", "patient"},
        },
        "list_own": {
            "allow": {"doctor", "patient"},
            "deny": {"admin", "staff"},
        },
        "view_detail": {
            "allow": {"admin", "staff", "doctor", "patient"},
            "deny": set(),
        },
        "create": {
            "allow": {"admin", "staff", "doctor", "patient"},
            "deny": set(),
        },
        "update_time": {
            "allow": {"admin", "staff", "doctor", "patient"},
            "deny": set(),
        },
        "update_doctor": {
            "allow": {"admin", "staff"},
            "deny": {"doctor", "patient"},
        },
        "confirm": {
            "allow": {"admin", "staff"},
            "deny": {"doctor", "patient"},
        },
        "start_consultation": {
            "allow": {"admin", "staff", "doctor"},
            "deny": {"patient"},
        },
        "complete": {
            "allow": {"admin", "staff", "doctor"},
            "deny": {"patient"},
        },
        "cancel": {
            "allow": {"admin", "staff", "doctor", "patient"},
            "deny": set(),
        },
        "print": {
            "allow": {"admin", "staff", "doctor", "patient"},
            "deny": set(),
        },
    }

    @staticmethod
    def _validate_rbac_matrix():
        action_set = set(AppointmentController.APPOINTMENT_ACTIONS)
        matrix_actions = set(AppointmentController.APPOINTMENT_RBAC.keys())

        if action_set != matrix_actions:
            missing = sorted(action_set - matrix_actions)
            extra = sorted(matrix_actions - action_set)
            return False, f"RBAC action mismatch - missing: {missing}, extra: {extra}"

        for action in AppointmentController.APPOINTMENT_ACTIONS:
            rule = AppointmentController.APPOINTMENT_RBAC.get(action, {})
            allow = set(rule.get("allow", set()))
            deny = set(rule.get("deny", set()))

            if allow & deny:
                return False, f"RBAC invalid: overlap allow/deny for action '{action}'"

            covered = allow | deny
            if covered != AppointmentController.ROLES:
                missing_roles = sorted(AppointmentController.ROLES - covered)
                extra_roles = sorted(covered - AppointmentController.ROLES)
                return (
                    False,
                    f"RBAC invalid for '{action}' - missing roles: {missing_roles}, extra roles: {extra_roles}",
                )

        return True, "RBAC matrix is valid and complete."

    @staticmethod
    def _is_patient_owner(user_patient_id, appointment_patient_id):
        return str(user_patient_id) == str(appointment_patient_id)

    @staticmethod
    def _is_doctor_owner(user_doctor_id, appointment_doctor_id):
        return str(user_doctor_id) == str(appointment_doctor_id)

    @staticmethod
    def debug_validate_rbac_matrix():
        is_valid, detail = AppointmentController._validate_rbac_matrix()
        if not is_valid:
            return {"status": False, "message": f"RBAC validation failed: {detail}"}
        return {"status": True, "message": detail}

    @staticmethod
    def _deny(message="Bạn không có quyền thực hiện thao tác này."):
        return {"status": False, "message": message}

    @staticmethod
    def _get_context_value(user_context, key):
        if user_context is None:
            return None
        if isinstance(user_context, dict):
            return user_context.get(key)
        return getattr(user_context, key, None)

    @staticmethod
    def authorize(role, action, user_context=None, appointment=None):
        normalized_role = str(role or "").strip().lower()
        rule = AppointmentController.APPOINTMENT_RBAC.get(action)

        if normalized_role not in AppointmentController.ROLES or not rule:
            return False, "Vai trò hoặc hành động không hợp lệ."

        if normalized_role in set(rule.get("deny", set())):
            return False, "Bạn không có quyền thực hiện thao tác này."

        if normalized_role not in set(rule.get("allow", set())):
            return False, "Bạn không có quyền thực hiện thao tác này."

        if appointment and normalized_role in {"doctor", "patient"}:
            appointment_patient_id = appointment.get("patient_id")
            appointment_doctor_id = appointment.get("doctor_id")

            if normalized_role == "patient":
                user_patient_id = AppointmentController._get_context_value(user_context, "patient_id")
                if not user_patient_id:
                    return False, "Thiếu thông tin bệnh nhân để xác thực quyền truy cập."
                if not AppointmentController._is_patient_owner(user_patient_id, appointment_patient_id):
                    return False, "Bạn chỉ có thể thao tác trên lịch hẹn của chính mình."

            if normalized_role == "doctor":
                user_doctor_id = AppointmentController._get_context_value(user_context, "doctor_id")
                if not user_doctor_id:
                    return False, "Thiếu thông tin bác sĩ để xác thực quyền truy cập."
                if not AppointmentController._is_doctor_owner(user_doctor_id, appointment_doctor_id):
                    return False, "Bạn chỉ có thể thao tác trên lịch hẹn của chính mình."

        return True, ""

    @staticmethod
    def _can_transition(current_status, target_status):
        current = str(current_status or "")
        target = str(target_status or "")

        if target not in AppointmentController.VALID_STATUSES:
            return False

        if current in {"done", "cancelled"} and target != current:
            return False

        return True

    @staticmethod
    def can_start_exam(current_status):
        return str(current_status or "") in AppointmentController.START_EXAM_STATUSES

    @staticmethod
    def _resolve_checkin_status(current_status):
        current = str(current_status or "")
        if current == "pending":
            return "confirmed"
        if current == "confirmed":
            return "in_progress"
        return None

    @staticmethod
    def _service_exists(service_name):
        return AppointmentController._resolve_service(service_name) is not None

    @staticmethod
    def _resolve_service(service_value):
        normalized = str(service_value or "").strip()
        if not normalized:
            return None

        services = ServiceModel.get_visible_active() or []
        for service in services:
            if str(service.get("service_id")) == normalized:
                return service
            if str(service.get("service_name", "")).strip().lower() == normalized.lower():
                return service
        return None

    @staticmethod
    def _doctor_is_bookable(doctor_id):
        doctor = DoctorModel.get_by_id(doctor_id)
        if not doctor:
            return False
        if str(doctor.get("is_active", 1)).lower() in {"0", "false", "none"}:
            return False
        work_status = str(doctor.get("work_status") or "").strip().lower()
        if work_status and any(token in work_status for token in ("nghỉ", "nghi", "off", "inactive")):
            return False
        return True

    @staticmethod
    def _default_slot_times():
        return DEFAULT_SLOTS

    @staticmethod
    def get_available_slots(doctor_id, date_str, service_id=None):
        if not doctor_id or not date_str:
            return {"status": False, "message": "Thiếu bác sĩ hoặc ngày khám.", "slots": []}

        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return {"status": False, "message": "Ngày khám không đúng định dạng.", "slots": []}

        if not AppointmentController._doctor_is_bookable(doctor_id):
            return {"status": False, "message": "Bác sĩ không khả dụng.", "slots": []}

        booked_rows = AppointmentModel.get_booked_slots(doctor_id, selected_date.strftime("%Y-%m-%d")) or []
        booked_times = set()
        for row in booked_rows:
            raw_value = row.get("appointment_date")
            if hasattr(raw_value, "strftime"):
                booked_times.add(raw_value.strftime("%H:%M"))
            else:
                try:
                    booked_times.add(datetime.fromisoformat(str(raw_value).replace("Z", "")).strftime("%H:%M"))
                except ValueError:
                    value = str(raw_value or "")
                    if len(value) >= 16:
                        booked_times.add(value[11:16])

        now = datetime.now()
        slots = []
        for time_value in AppointmentController._default_slot_times():
            slot_dt = datetime.combine(selected_date, datetime.strptime(time_value, "%H:%M").time())
            disabled = time_value in booked_times or slot_dt < now
            slots.append({"time": time_value, "available": not disabled})
        return {"status": True, "slots": slots}

    # 🔹 LẤY TẤT CẢ LỊCH HẸN
    @staticmethod
    def get_all():
        return AppointmentModel.get_all()

    @staticmethod
    def get_all_for_role(role, user_context):
        normalized_role = str(role or "").strip().lower()

        if normalized_role in {"admin", "staff"}:
            return AppointmentController.get_all()

        if normalized_role == "doctor":
            doctor_id = AppointmentController._get_context_value(user_context, "doctor_id")
            if not doctor_id:
                return AppointmentController._deny("Thiếu thông tin bác sĩ để xem danh sách lịch hẹn.")
            return AppointmentController.get_by_doctor(doctor_id)

        if normalized_role == "patient":
            patient_id = AppointmentController._get_context_value(user_context, "patient_id")
            if not patient_id:
                return AppointmentController._deny("Thiếu thông tin bệnh nhân để xem danh sách lịch hẹn.")
            return AppointmentController.get_by_patient(patient_id)

        return AppointmentController._deny()
        
    @staticmethod
    def get_by_patient(patient_id):
        return AppointmentModel.get_by_patient(patient_id)
        
    @staticmethod
    def get_by_doctor(doctor_id):
        return AppointmentModel.get_by_doctor(doctor_id)

    @staticmethod
    def get_upcoming_by_patient(patient_id):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return AppointmentModel.get_upcoming_by_patient(patient_id, current_datetime)


    # 🔹 TẠO LỊCH HẸN (TỪ FORM WEB/APP)
    @staticmethod
    def create(patient_id, doctor_id, date, role=None, user_context=None, service_id=None):
        if role is not None:
            allowed, message = AppointmentController.authorize(role, "create", user_context=user_context)
            if not allowed:
                return AppointmentController._deny(message)

            normalized_role = str(role or "").strip().lower()
            if normalized_role == "patient":
                context_patient_id = AppointmentController._get_context_value(user_context, "patient_id")
                if not context_patient_id:
                    return AppointmentController._deny("Thiếu thông tin bệnh nhân để tạo lịch hẹn.")
                if not AppointmentController._is_patient_owner(context_patient_id, patient_id):
                    return AppointmentController._deny("Bạn chỉ có thể tạo lịch hẹn cho chính mình.")

        return AppointmentModel.create(patient_id, doctor_id, date, "pending", "", service_id)

    @staticmethod
    def book_with_validation(patient_id, doctor_id, service_name, date_str, time_str, role=None, user_context=None):
        required_fields = [patient_id, doctor_id, service_name, date_str, time_str]
        if not all(required_fields):
            return {
                "status": False,
                "message": "Vui lòng chọn đầy đủ dịch vụ, ngày, giờ và bác sĩ.",
            }

        if service_name.strip().lower() == "chưa có dịch vụ":
            return {
                "status": False,
                "message": "Hiện chưa có dịch vụ khả dụng để đặt lịch.",
            }

        if role is not None:
            allowed, message = AppointmentController.authorize(role, "create", user_context=user_context)
            if not allowed:
                return AppointmentController._deny(message)
            if str(role or "").strip().lower() == "patient":
                context_patient_id = AppointmentController._get_context_value(user_context, "patient_id")
                if not context_patient_id or not AppointmentController._is_patient_owner(context_patient_id, patient_id):
                    return AppointmentController._deny("Bạn chỉ có thể tạo lịch hẹn cho chính mình.")

        service = AppointmentController._resolve_service(service_name)
        if not service:
            return {
                "status": False,
                "message": "Dịch vụ không khả dụng hoặc đã ngừng hiển thị.",
            }

        if not AppointmentController._doctor_is_bookable(doctor_id):
            return {
                "status": False,
                "message": "Bác sĩ không khả dụng để đặt lịch.",
            }

        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return {
                "status": False,
                "message": "Ngày khám không đúng định dạng.",
            }

        try:
            selected_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            return {
                "status": False,
                "message": "Giờ khám không hợp lệ.",
            }

        if selected_date < datetime.now().date():
            return {
                "status": False,
                "message": "Không thể đặt lịch cho ngày trong quá khứ.",
            }

        if selected_time.strftime("%H:%M") not in AppointmentController._default_slot_times():
            return {
                "status": False,
                "message": "Khung giờ ngoài giờ làm việc hoặc không đúng bước 30 phút.",
            }

        appointment_datetime = datetime.combine(selected_date, selected_time)
        appointment_dt_str = appointment_datetime.strftime("%Y-%m-%d %H:%M:%S")

        if appointment_datetime < datetime.now():
            return {
                "status": False,
                "message": "Không thể đặt lịch cho khung giờ đã qua.",
            }

        # Use exact datetime matching to prevent double-booking at the same slot.
        doctor_conflict, patient_conflict = AppointmentModel.has_conflict(
            doctor_id,
            patient_id,
            appointment_dt_str,
        )

        if doctor_conflict:
            return {
                "status": False,
                "message": "Bác sĩ đã có lịch ở khung giờ này. Vui lòng chọn thời gian khác.",
            }

        if patient_conflict:
            return {
                "status": False,
                "message": "Bạn đã có lịch ở khung giờ này. Vui lòng chọn thời gian khác.",
            }

        service_label = service.get("service_name") or service_name
        note = f"Dịch vụ: {service_label}"
        is_created = AppointmentModel.create(
            patient_id,
            doctor_id,
            appointment_dt_str,
            "pending",
            note,
            service.get("service_id"),
        )

        if not is_created:
            return {
                "status": False,
                "message": "Không thể lưu lịch hẹn. Vui lòng thử lại.",
            }

        return {
            "status": True,
            "message": "Đặt lịch khám thành công.",
        }


    # 🔹 CẬP NHẬT TRẠNG THÁI
    @staticmethod
    def update_status(appointment_id, status, role=None, user_context=None):
        if status not in AppointmentController.VALID_STATUSES:
            return False

        existing = AppointmentModel.get_by_id(appointment_id)
        if not existing:
            return False

        if role is not None:
            action = "cancel" if status == "cancelled" else "update_time"
            allowed, message = AppointmentController.authorize(
                role,
                action,
                user_context=user_context,
                appointment=existing,
            )
            if not allowed:
                return AppointmentController._deny(message)

        current_status = str(existing.get("status", ""))
        if not AppointmentController._can_transition(current_status, status):
            return False

        return AppointmentModel.update_status(appointment_id, status)

    @staticmethod
    def get_management_rows_by_doctor(doctor_id):
        return AppointmentModel.get_management_rows_by_doctor(doctor_id)

    @staticmethod
    def get_by_id(appointment_id):
        return AppointmentModel.get_by_id(appointment_id)

    @staticmethod
    def update_full(appointment_id, patient_id, doctor_id, date_str, time_str, status, service_name, note, role=None, user_context=None):
        required_fields = [appointment_id, patient_id, doctor_id, date_str, time_str]
        if not all(required_fields):
            return {
                "status": False,
                "message": "Thiếu dữ liệu để cập nhật lịch hẹn.",
            }

        if status not in AppointmentController.VALID_STATUSES:
            return {
                "status": False,
                "message": "Trạng thái lịch hẹn không hợp lệ.",
            }

        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            selected_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            return {
                "status": False,
                "message": "Ngày hoặc giờ không hợp lệ.",
            }

        if selected_time.strftime("%H:%M") not in AppointmentController._default_slot_times():
            return {
                "status": False,
                "message": "Khung giờ ngoài giờ làm việc hoặc không đúng bước 30 phút.",
            }

        appointment_datetime = datetime.combine(selected_date, selected_time)
        appointment_dt_str = appointment_datetime.strftime("%Y-%m-%d %H:%M:%S")

        existing = AppointmentModel.get_by_id(appointment_id)
        if not existing:
            return {
                "status": False,
                "message": "Không tìm thấy lịch hẹn cần cập nhật.",
            }

        if role is not None:
            action = "cancel" if status == "cancelled" else "update_time"
            allowed, message = AppointmentController.authorize(
                role,
                action,
                user_context=user_context,
                appointment=existing,
            )
            if not allowed:
                return AppointmentController._deny(message)

        existing_status = str(existing.get("status", ""))
        if not AppointmentController._can_transition(existing_status, status):
            return {
                "status": False,
                "message": "Không thể thay đổi trạng thái của lịch hẹn đã kết thúc hoặc đã hủy.",
            }

        doctor_conflict, patient_conflict = AppointmentModel.has_conflict(
            doctor_id,
            patient_id,
            appointment_dt_str,
            appointment_id,
        )

        if doctor_conflict:
            return {
                "status": False,
                "message": "Bác sĩ đã có lịch ở khung giờ này.",
            }

        if patient_conflict:
            return {
                "status": False,
                "message": "Bệnh nhân đã có lịch ở khung giờ này.",
            }

        if appointment_datetime < datetime.now() and status in {"pending", "confirmed", "in_progress"}:
            return {
                "status": False,
                "message": "Không thể đặt trạng thái hoạt động cho lịch hẹn trong quá khứ.",
            }

        normalized_service = (service_name or "").strip()
        normalized_note = (note or "").strip()
        service_id = existing.get("service_id")

        if normalized_service:
            service = AppointmentController._resolve_service(normalized_service)
            if not service:
                return {
                    "status": False,
                    "message": "Dịch vụ không khả dụng hoặc đã ngừng hiển thị.",
                }
            service_id = service.get("service_id")
            normalized_service = service.get("service_name") or normalized_service
            combined_note = f"Dịch vụ: {normalized_service}"
            if normalized_note:
                combined_note += f" | {normalized_note}"
        else:
            combined_note = normalized_note

        is_updated = AppointmentModel.update_full(
            appointment_id,
            patient_id,
            doctor_id,
            appointment_dt_str,
            status,
            combined_note,
            service_id,
        )

        if not is_updated:
            return {
                "status": False,
                "message": "Không thể cập nhật lịch hẹn.",
            }

        return {
            "status": True,
            "message": "Cập nhật lịch hẹn thành công.",
        }

    @staticmethod
    def cancel(appointment_id, role=None, user_context=None):
        existing = AppointmentModel.get_by_id(appointment_id)
        if not existing:
            return {"status": False, "message": "Không tìm thấy lịch hẹn."}

        if role is not None:
            allowed, message = AppointmentController.authorize(
                role,
                "cancel",
                user_context=user_context,
                appointment=existing,
            )
            if not allowed:
                return AppointmentController._deny(message)

        current_status = str(existing.get("status", ""))
        if not AppointmentController._can_transition(current_status, "cancelled"):
            return {
                "status": False,
                "message": "Không thể hủy lịch hẹn đã kết thúc hoặc đã hủy.",
            }

        is_updated = AppointmentModel.update_status(appointment_id, "cancelled")
        if not is_updated:
            return {"status": False, "message": "Không thể hủy lịch hẹn."}

        return {"status": True, "message": "Hủy lịch hẹn thành công."}

    @staticmethod
    def update_appointment(appointment_id, date, time, doctor_id, status, role=None, user_context=None):
        existing = AppointmentModel.get_by_id(appointment_id)
        if not existing:
            return {"status": False, "message": "Khong tim thay lich hen."}

        if role is not None:
            action = "cancel" if status == "cancelled" else "update_time"
            allowed, message = AppointmentController.authorize(
                role,
                action,
                user_context=user_context,
                appointment=existing,
            )
            if not allowed:
                return AppointmentController._deny(message)

        try:
            appointment_datetime = datetime.combine(
                datetime.strptime(date, "%Y-%m-%d").date(),
                datetime.strptime(time, "%H:%M").time(),
            )
        except ValueError:
            return {"status": False, "message": "Ngay hoac gio khong hop le."}

        if status not in AppointmentController.VALID_STATUSES:
            return {"status": False, "message": "Trang thai lich hen khong hop le."}

        if not AppointmentController._can_transition(existing.get("status"), status):
            return {"status": False, "message": "Khong the chuyen trang thai lich hen."}

        updated = AppointmentModel.update_appointment(
            appointment_id,
            appointment_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            doctor_id,
            status,
        )
        return {"status": bool(updated), "message": "Cap nhat lich hen thanh cong."}

    @staticmethod
    def create_with_details(patient_id, doctor_id, date_str, time_str, status, service_name, note, role=None, user_context=None):
        required_fields = [patient_id, doctor_id, date_str, time_str]
        if not all(required_fields):
            return {
                "status": False,
                "message": "Thiếu dữ liệu để tạo lịch hẹn.",
            }

        if role is not None:
            allowed, message = AppointmentController.authorize(
                role,
                "create",
                user_context=user_context,
                appointment={"doctor_id": doctor_id, "patient_id": patient_id},
            )
            if not allowed:
                return AppointmentController._deny(message)

        if status not in AppointmentController.VALID_STATUSES:
            return {
                "status": False,
                "message": "Trạng thái lịch hẹn không hợp lệ.",
            }

        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            selected_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            return {
                "status": False,
                "message": "Ngày hoặc giờ không hợp lệ.",
            }

        if selected_time.strftime("%H:%M") not in AppointmentController._default_slot_times():
            return {
                "status": False,
                "message": "Khung giờ ngoài giờ làm việc hoặc không đúng bước 30 phút.",
            }

        appointment_datetime = datetime.combine(selected_date, selected_time)
        appointment_dt_str = appointment_datetime.strftime("%Y-%m-%d %H:%M:%S")

        if appointment_datetime < datetime.now() and status in {"pending", "confirmed", "in_progress"}:
            return {
                "status": False,
                "message": "Không thể tạo lịch hẹn hoạt động trong quá khứ.",
            }

        doctor_conflict, patient_conflict = AppointmentModel.has_conflict(
            doctor_id,
            patient_id,
            appointment_dt_str,
        )
        if doctor_conflict:
            return {
                "status": False,
                "message": "Bác sĩ đã có lịch ở khung giờ này.",
            }
        if patient_conflict:
            return {
                "status": False,
                "message": "Bệnh nhân đã có lịch ở khung giờ này.",
            }

        normalized_service = (service_name or "").strip() or "Khám tổng quát"
        normalized_note = (note or "").strip()
        service = AppointmentController._resolve_service(normalized_service)
        if not service:
            return {
                "status": False,
                "message": "Dịch vụ không khả dụng hoặc đã ngừng hiển thị.",
            }
        normalized_service = service.get("service_name") or normalized_service
        combined_note = f"Dịch vụ: {normalized_service}"
        if normalized_note:
            combined_note += f" | {normalized_note}"

        is_created = AppointmentModel.create(
            patient_id,
            doctor_id,
            appointment_dt_str,
            status,
            combined_note,
            service.get("service_id"),
        )
        if not is_created:
            return {
                "status": False,
                "message": "Không thể tạo lịch hẹn.",
            }

        return {
            "status": True,
            "message": "Đã thêm lịch hẹn mới.",
        }

    @staticmethod
    def confirm_intake_checkin(appointment_id, patient_id, doctor_id, service_name, intake_date_str, intake_time_str, reason_note):
        required_fields = [appointment_id, patient_id, doctor_id, service_name, intake_date_str, intake_time_str]
        if not all(required_fields):
            return {
                "status": False,
                "message": "Thiếu dữ liệu check-in: cần bệnh nhân, dịch vụ, bác sĩ, ngày và giờ tiếp nhận.",
            }

        doctor = DoctorModel.get_by_id(doctor_id)
        if not doctor:
            return {
                "status": False,
                "message": "Bác sĩ không tồn tại.",
            }

        if not AppointmentController._service_exists(service_name):
            return {
                "status": False,
                "message": "Dịch vụ không tồn tại.",
            }

        try:
            intake_date = datetime.strptime(intake_date_str, "%Y-%m-%d").date()
            intake_time = datetime.strptime(intake_time_str, "%H:%M").time()
        except ValueError:
            return {
                "status": False,
                "message": "Ngày hoặc giờ tiếp nhận không hợp lệ.",
            }

        intake_datetime = datetime.combine(intake_date, intake_time)
        intake_dt_str = intake_datetime.strftime("%Y-%m-%d %H:%M:%S")

        existing = AppointmentModel.get_by_id(appointment_id)
        if not existing or int(existing.get("patient_id", 0)) != int(patient_id):
            return {
                "status": False,
                "message": "Không tìm thấy lịch hẹn phù hợp với bệnh nhân.",
            }

        next_status = AppointmentController._resolve_checkin_status(existing.get("status"))
        if not next_status:
            return {
                "status": False,
                "message": "Trạng thái hiện tại không hợp lệ để check-in (chỉ hỗ trợ pending -> confirmed hoặc confirmed -> in_progress).",
            }

        if not AppointmentController._can_transition(existing.get("status"), next_status):
            return {
                "status": False,
                "message": "Không thể chuyển trạng thái check-in theo quy tắc hiện tại.",
            }

        doctor_conflict, patient_conflict = AppointmentModel.has_conflict(
            doctor_id,
            patient_id,
            intake_dt_str,
            appointment_id,
        )
        if doctor_conflict:
            return {
                "status": False,
                "message": "Bác sĩ đã có lịch ở khung giờ tiếp nhận này.",
            }
        if patient_conflict:
            return {
                "status": False,
                "message": "Bệnh nhân đã có lịch ở khung giờ tiếp nhận này.",
            }

        normalized_service = (service_name or "").strip()
        normalized_reason = (reason_note or "").strip()
        combined_note = f"Dịch vụ: {normalized_service}"
        if normalized_reason:
            combined_note += f" | Lý do tiếp nhận: {normalized_reason}"

        is_updated = AppointmentModel.update_intake_checkin(
            appointment_id,
            patient_id,
            doctor_id,
            intake_dt_str,
            next_status,
            combined_note,
        )
        if not is_updated:
            return {
                "status": False,
                "message": "Không thể xác nhận check-in. Vui lòng thử lại.",
            }

        queue_row = WaitingQueueModel.check_in(
            patient_id=patient_id,
            appointment_id=appointment_id,
            intake_note=combined_note,
            area=DEFAULT_QUEUE_AREA,
        )

        return {
            "status": True,
            "message": "Xác nhận tiếp nhận thành công.",
            "appointment_id": appointment_id,
            "next_status": next_status,
            "intake_time": intake_dt_str,
            "note": combined_note,
            "queue": queue_row,
        }
