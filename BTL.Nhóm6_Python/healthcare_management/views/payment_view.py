import tkinter as tk
from controllers.payment_controller import PaymentController

class PaymentView:

    def __init__(self, root):
        tk.Label(root, text="Payments", font=("Arial", 14)).pack()

        self.listbox = tk.Listbox(root, width=60)
        self.listbox.pack()

        tk.Button(root, text="Load", command=self.load).pack()

    def load(self):
        self.listbox.delete(0, tk.END)
        data = PaymentController.get_all()

        for p in data:
            self.listbox.insert(tk.END, f"{p['payment_id']} - {p['total_amount']} - {p['status']}")