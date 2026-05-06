import tkinter as tk
from controllers.prescription_controller import PrescriptionController

class PrescriptionView:

    def __init__(self, root):
        tk.Label(root, text="Prescriptions", font=("Arial", 14)).pack()

        self.listbox = tk.Listbox(root, width=60)
        self.listbox.pack()

        tk.Button(root, text="Load", command=self.load).pack()

    def load(self):
        self.listbox.delete(0, tk.END)

        data = PrescriptionController.get_by_record(1)

        for p in data:
            self.listbox.insert(tk.END, f"{p['medicine_id']} - {p['name']} x{p['quantity']}")