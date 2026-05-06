import tkinter as tk
from controllers.medicine_controller import MedicineController

class MedicineView:

    def __init__(self, root):
        tk.Label(root, text="Medicine Management", font=("Arial", 14)).pack()

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack()

        tk.Button(root, text="Load", command=self.load).pack()

    def load(self):
        self.listbox.delete(0, tk.END)
        data = MedicineController.get_all()

        for m in data:
            self.listbox.insert(tk.END, f"{m['medicine_id']} - {m['name']}")