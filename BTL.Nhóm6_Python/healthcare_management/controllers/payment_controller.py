from models.payment_model import PaymentModel

class PaymentController:

    @staticmethod
    def get_all():
        return PaymentModel.get_all()

    @staticmethod
    def get_enriched_all(status=None, date_from=None, date_to=None, user_context=None):
        patient_id = None
        if user_context is not None:
            role = user_context.get("role")
            if role == "patient":
                patient_id = user_context.get("patient_id")
        return PaymentModel.get_enriched_all(status=status, date_from=date_from, date_to=date_to, patient_id=patient_id)

    @staticmethod
    def create(patient_id, appointment_id, total_amount):
        return PaymentModel.create(patient_id, appointment_id, total_amount)

    @staticmethod
    def update_status(payment_id, status):
        return PaymentModel.update_status(payment_id, status)
