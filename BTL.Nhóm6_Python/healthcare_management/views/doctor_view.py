import tkinter as tk
from controllers.doctor_controller import DoctorController

class DoctorView:

    def __init__(self, root):
        tk.Label(root, text="Doctor Management", font=("Arial", 14)).pack()

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack()

        tk.Button(root, text="Load Data", command=self.load).pack()

    def load(self):
        self.listbox.delete(0, tk.END)
        data = DoctorController.get_all()

        for d in data:
            self.listbox.insert(tk.END, f"{d['doctor_id']} - {d['name']}")