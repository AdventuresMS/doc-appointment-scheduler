# ========================
# 🔹 Step 1: Imports
# ========================
import tkinter as tk
from tkinter import messagebox
from utils.file_utils import save_appointment, read_appointments, is_slot_available
from utils.validation import validate_date, validate_time

# ========================
# 🔹 Step 2: Main Window
# ========================
root = tk.Tk()
root.title("Doctor's Appointment Scheduler")
root.geometry("400x500")

# ========================
# 🔹 Step 3: Input Fields
# ========================
tk.Label(root, text="Patient Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Age").pack()
entry_age = tk.Entry(root)
entry_age.pack()

tk.Label(root, text="Contact Number").pack()
entry_contact = tk.Entry(root)
entry_contact.pack()

tk.Label(root, text="Date (YYYY-MM-DD)").pack()
entry_date = tk.Entry(root)
entry_date.pack()

tk.Label(root, text="Time (HH:MM in 24hr)").pack()
entry_time = tk.Entry(root)
entry_time.pack()

tk.Label(root, text="Email (optional)").pack()
entry_email = tk.Entry(root)
entry_email.pack()

# ========================
# 🔹 Step 4: Booking Logic
# ========================
def book_appointment_gui():
    name = entry_name.get()
    age = entry_age.get()
    contact = entry_contact.get()
    date = entry_date.get()
    time = entry_time.get()
    email = entry_email.get()

    if not (validate_date(date) and validate_time(time)):
        messagebox.showerror("Error", "❌ Invalid date or time format.")
        return

    if not is_slot_available(date, time):
        messagebox.showwarning("Unavailable", f"⚠️ The slot on {date} at {time} is already booked.")
        return

    save_appointment(name, age, contact, date, time)
    messagebox.showinfo("Success", "✅ Appointment booked successfully!")

# ========================
# 🔹 Step 5: View Logic
# ========================
def view_appointments_gui():
    appointments = read_appointments()
    if not appointments:
        messagebox.showinfo("Appointments", "No appointments found.")
        return

    view_window = tk.Toplevel(root)
    view_window.title("📅 All Appointments")

    for appt in appointments:
        tk.Label(view_window, text=" | ".join(appt)).pack()

# ========================
# 🔹 Step 6: Buttons
# ========================
tk.Button(root, text="📌 Book Appointment", command=book_appointment_gui).pack(pady=10)
tk.Button(root, text="📂 View Appointments", command=view_appointments_gui).pack(pady=5)

# ========================
# 🔹 Step 7: Run App
# ========================
root.mainloop()
