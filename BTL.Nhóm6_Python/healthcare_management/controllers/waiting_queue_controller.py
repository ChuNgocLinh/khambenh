from models.waiting_queue_model import WaitingQueueModel
from config import DEFAULT_QUEUE_AREA


class WaitingQueueController:
    @staticmethod
    def check_in(patient_id, appointment_id=None, intake_note="", area=DEFAULT_QUEUE_AREA):
        if not patient_id:
            return {"status": False, "message": "Thiếu bệnh nhân để check-in."}
        row = WaitingQueueModel.check_in(
            patient_id=patient_id,
            appointment_id=appointment_id,
            intake_note=intake_note,
            area=area,
        )
        if not row:
            return {"status": False, "message": "Không thể tạo số thứ tự chờ khám."}
        return {"status": True, "message": "Đã check-in hàng chờ.", "data": row}

    @staticmethod
    def get_waiting(area=DEFAULT_QUEUE_AREA):
        return WaitingQueueModel.get_waiting(area=area)
