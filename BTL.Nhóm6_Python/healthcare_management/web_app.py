from flask import Flask, render_template, request, redirect

# import controller của bạn
from healthcare_management.controllers.patient_controller import PatientController
from healthcare_management.controllers.auth_controller import AuthController

app = Flask(__name__)

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = AuthController.login(username, password)
        if user:
            return redirect("/dashboard")

    return render_template("login.html")

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# PATIENT
@app.route("/patients")
def patients():
    data = PatientController.get_all()
    return render_template("patients.html", patients=data)

app.run(debug=True)
