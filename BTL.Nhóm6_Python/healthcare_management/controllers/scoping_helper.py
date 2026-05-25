def get_context_value(user_context, key):
    if user_context is None:
        return None
    if isinstance(user_context, dict):
        return user_context.get(key)
    return getattr(user_context, key, None)


def enforce_patient_scope(patient_id, user_context):
    """
    Nếu user_context chỉ có quyền patient, bắt buộc patient_id phải khớp với patient_id trong context.
    Nếu user_context có quyền admin/staff/doctor, cho phép qua.
    """
    if not user_context:
        raise PermissionError("Yêu cầu thông tin xác thực (user_context).")

    role = get_context_value(user_context, "role")
    if role == "patient":
        context_patient_id = get_context_value(user_context, "patient_id")
        if not context_patient_id or int(context_patient_id) != int(patient_id):
            raise PermissionError("Bạn không có quyền truy cập thông tin của bệnh nhân này.")
    elif role in {"admin", "staff", "doctor"}:
        pass
    else:
        raise PermissionError("Vai trò không hợp lệ.")


def enforce_doctor_scope(doctor_id, user_context):
    """
    Nếu user_context chỉ có quyền doctor, bắt buộc doctor_id phải khớp với doctor_id trong context.
    Nếu user_context có quyền admin/staff, cho phép qua.
    """
    if not user_context:
        raise PermissionError("Yêu cầu thông tin xác thực (user_context).")

    role = get_context_value(user_context, "role")
    if role == "doctor":
        context_doctor_id = get_context_value(user_context, "doctor_id")
        if not context_doctor_id or int(context_doctor_id) != int(doctor_id):
            raise PermissionError("Bạn không có quyền thao tác cho bác sĩ này.")
    elif role in {"admin", "staff"}:
        pass
    else:
        raise PermissionError("Vai trò không hợp lệ.")
