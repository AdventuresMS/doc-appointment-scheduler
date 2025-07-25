import csv
import os
from utils.file_utils import save_appointment, read_appointments, is_slot_available
from email_sender import send_email
from datetime import datetime
from utils.validation import validate_date, validate_time

APPT_FILE = "data/appointments.csv"

def book_appointment():
    name = input("Enter patient name: ")
    age = input("Enter age: ")
    contact = input("Enter contact number: ")
    date = input("Enter appointment date (YYYY-MM-DD): ")
    time = input("Enter time (HH:MM in 24hr format): ")
    email = input("Enter email for confirmation (optional): ")

    if not (validate_date(date) and validate_time(time)):
        print("❌ Invalid date or time format.")
        return

    if not is_slot_available(date, time):
        print("⚠️ That slot is already booked.")
        return

    save_appointment(name, age, contact, date, time)
    print("✅ Appointment booked successfully!")

    if email.strip():
        subject = "Appointment Confirmation"
        body = f"Dear {name},\n\nYour appointment is booked for {date} at {time}.\n\nThank you!"
        send_email(email, subject, body)

    os.makedirs("data", exist_ok=True)

    # email = input("Enter email (optional): ")
    send_email(email, "Appointment Confirmation", f"Dear {name}, your appointment is booked for {date} at {time}.")

def view_appointments():
    if not os.path.exists(APPT_FILE):
        print("No appointments yet.")
        return
    with open(APPT_FILE, 'r') as file:
        reader = csv.reader(file)
        print("\n📅 Appointments:\n")
        for row in reader:
            print(" | ".join(row))
        print()

def search_appointments():
    if not os.path.exists(APPT_FILE):
        print("No appointments found.")
        return

    keyword = input("🔎 Enter name or date (YYYY-MM-DD) to search: ").strip().lower()

    found = False
    with open(APPT_FILE, 'r') as file:
        reader = csv.reader(file)
        print("\n🔍 Search Results:\n")
        for row in reader:
            if any(keyword in field.lower() for field in row):
                print(" | ".join(row))
                found = True

    if not found:
        print("❌ No matching appointments found.")


def menu():
    print("\n=== Doctor's Appointment Scheduler ===")
    print("1. Book Appointment")
    print("2. View Appointments")
    print("3. Search Appointments")  # New Option
    print("4. Exit")

while True:
    menu()
    choice = input("Enter choice: ")
    if choice == '1':
        book_appointment()
    elif choice == '2':
        view_appointments()
    elif choice == '3':
        search_appointments()
    elif choice == '4':
        print("👋 Exiting program.")
        break
    else:
        print("❌ Invalid input.")

