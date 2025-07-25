import csv
import os

APPT_FILE = "data/appointments.csv"

def save_appointment(name, age, contact, date, time):
    os.makedirs("data", exist_ok=True)
    with open(APPT_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, age, contact, date, time])

def read_appointments():
    if not os.path.exists(APPT_FILE):
        return []
    with open(APPT_FILE, 'r') as file:
        reader = csv.reader(file)
        return list(reader)

def is_slot_available(date, time):
    appointments = read_appointments()
    for appt in appointments:
        if appt[3] == date and appt[4] == time:
            return False
    return True
