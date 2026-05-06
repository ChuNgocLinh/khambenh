import tkinter as tk
from controllers.invoice_controller import InvoiceController

class InvoiceView:

    def __init__(self, root):
        tk.Label(root, text="Invoices", font=("Arial", 14)).pack()

        self.listbox = tk.Listbox(root, width=60)
        self.listbox.pack()

        tk.Button(root, text="Load", command=self.load).pack()

    def load(self):
        self.listbox.delete(0, tk.END)
        data = InvoiceController.get_by_payment(1)

        for i in data:
            self.listbox.insert(tk.END, f"{i['service_name']} x{i['quantity']} = {i['total_price']}")