from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import json
import os
from datetime import datetime
from email_sender import send_email
from utils.file_utils import save_appointment, is_slot_available
from utils.validation import validate_date, validate_time
import csv
app = Flask(__name__)
APPOINTMENT_FILE = 'appointments.csv'

def load_appointments():
    if not os.path.exists(APPOINTMENT_FILE):
        with open(APPOINTMENT_FILE, 'w', newline='') as file:
            fieldnames = ['id', 'name', 'email', 'doctor', 'date', 'time']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
        return []
    with open(APPOINTMENT_FILE, newline='') as file:
        return list(csv.DictReader(file))


def save_appointments(appointments):
    with open(APPOINTMENT_FILE, 'w', newline='') as file:
        fieldnames = ['id', 'name', 'email', 'doctor', 'date', 'time']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(appointments)

@app.route("/manage")
def manage_appointments():
    appointments = load_appointments()
    return render_template("reschedule.html", appointments=appointments)

@app.route("/reschedule", methods=["POST"])
def reschedule():
    appt_id = request.form["id"]
    new_date = request.form["date"]
    new_time = request.form["time"]

    appointments = load_appointments()
    for appt in appointments:
        if appt["id"] == appt_id:
            appt["date"] = new_date
            appt["time"] = new_time
            break
    save_appointments(appointments)
    return redirect("/manage")

@app.route("/cancel", methods=["POST"])
def cancel():
    appt_id = request.form["id"]
    appointments = load_appointments()
    appointments = [appt for appt in appointments if appt["id"] != appt_id]
    save_appointments(appointments)
    return redirect("/manage")



# === Diagnosis Config ===
DATA_FILE = 'disease_data.csv'
df = pd.read_csv(DATA_FILE)

HISTORY_FILE = 'history.json'
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'w') as f:
        json.dump([], f)

# === Diagnosis Function ===
def diagnose(symptoms_input):
    symptoms = [s.strip().lower() for s in symptoms_input.split(',')]
    for index, row in df.iterrows():
        row_symptoms = [str(row['symptom1']).lower(), str(row['symptom2']).lower(), str(row['symptom3']).lower()]
        match_count = sum([s in row_symptoms for s in symptoms])
        if match_count >= 2:
            return f"{row['disease']} - {row.get('diagnosis_info', 'No additional info available.')}"
    return "No matching disease found. Please check your symptoms."

# === Save Diagnosis History ===
def save_history(symptoms, result):
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symptoms": symptoms,
        "result": result
    }
    history.append(entry)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

# === Routes ===

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/slider")
def slider():
    return render_template("slider.html")

@app.route("/project", methods=["GET", "POST"])
def project():
    result = None
    if request.method == "POST":
        symptoms = request.form['symptoms']
        result = diagnose(symptoms)
        save_history(symptoms, result)
    
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    return render_template("project.html", result=result, history=history)

@app.route("/history")
def view_history():
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    return render_template("history.html", history=history)

@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        contact = request.form.get("contact")
        date = request.form.get("date")
        time = request.form.get("time")
        email = request.form.get("email")

        if not (validate_date(date) and validate_time(time)):
            return render_template("book.html", error="Invalid date or time format.")

        if not is_slot_available(date, time):
            return render_template("book.html", error="Slot already booked.")

        save_appointment(name, age, contact, date, time)

        if email:
            send_email(email, name, date, time)

        return redirect(url_for("success", name=name, date=date, time=time))

    return render_template("book.html")

@app.route("/success")
def success():
    name = request.args.get("name")
    date = request.args.get("date")
    time = request.args.get("time")
    return render_template("success.html", name=name, date=date, time=time)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
