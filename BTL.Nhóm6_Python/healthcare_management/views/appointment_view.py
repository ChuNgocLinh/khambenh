import tkinter as tk
from controllers.appointment_controller import AppointmentController

class AppointmentView:

    def __init__(self, root):
        self.root = root

        tk.Label(root, text="Appointments", font=("Arial", 14)).pack()

        self.listbox = tk.Listbox(root, width=60)
        self.listbox.pack()

        tk.Button(root, text="Load", command=self.load).pack()

    def load(self):
        self.listbox.delete(0, tk.END)
        data = AppointmentController.get_all()

        for a in data:
            self.listbox.insert(tk.END,
                f"{a['appointment_id']} - {a['patient_name']} - {a['doctor_name']}")