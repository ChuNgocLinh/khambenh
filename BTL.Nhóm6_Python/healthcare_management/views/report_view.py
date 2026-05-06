import tkinter as tk
from controllers.report_controller import ReportController

class ReportView:

    def __init__(self, root):
        tk.Label(root, text="Reports", font=("Arial", 14)).pack()

        tk.Button(root, text="Load Report", command=self.load).pack()

        self.result = tk.Label(root, text="")
        self.result.pack()

    def load(self):
        revenue = ReportController.revenue()
        count = ReportController.appointments_count()

        self.result.config(
            text=f"Revenue: {revenue[0]['total_revenue']}\nAppointments: {count[0]['total_appointments']}"
        )