from models.invoice_model import InvoiceModel

class InvoiceController:

    @staticmethod
    def get_by_payment(payment_id):
        return InvoiceModel.get_by_payment(payment_id)

    @staticmethod
    def add_item(payment_id, service_id, quantity, price):
        return InvoiceModel.add_item(
            payment_id,
            service_id,
            quantity,
            price
        )