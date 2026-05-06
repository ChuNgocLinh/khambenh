import tkinter as tk
from controllers.medical_record_controller import MedicalRecordController

class MedicalRecordView:

    def __init__(self, root):
        tk.Label(root, text="Medical Records", font=("Arial", 14)).pack()

        self.listbox = tk.Listbox(root, width=60)
        self.listbox.pack()

        tk.Button(root, text="Load", command=self.load).pack()

    def load(self):
        self.listbox.delete(0, tk.END)

        # demo load theo patient_id = 1
        data = MedicalRecordController.get_by_patient(1)

        for m in data:
            self.listbox.insert(tk.END, f"{m['record_id']} - {m['diagnosis']}")