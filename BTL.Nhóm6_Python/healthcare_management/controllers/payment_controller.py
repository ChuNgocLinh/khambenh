from models.payment_model import PaymentModel

class PaymentController:

    @staticmethod
    def get_all():
        return PaymentModel.get_all()

    @staticmethod
    def create(patient_id, appointment_id, total_amount):
        return PaymentModel.create(patient_id, appointment_id, total_amount)

    @staticmethod
    def update_status(payment_id, status):
        return PaymentModel.update_status(payment_id, status)