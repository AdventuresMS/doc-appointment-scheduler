import smtplib
from email.mime.text import MIMEText

def send_email(to_email, patient_name, date, time):
    sender_email = "easyappointmentbot@gmail.com"
    sender_password = "kprp vlbn frie mjco"  # Make sure this is your Gmail App Password

    subject = "🩺 Appointment Confirmation – Dr. Jaydeep Dutta"

    body = f"""\
Dear {patient_name},

This is to confirm that your appointment with Dr. Jaydeep Dutta has been successfully scheduled.

📅 Date: {date}
⏰ Time: {time}

Please arrive 10 minutes early and bring any previous medical records, if applicable.

If you have any questions or need to reschedule, feel free to reply to this email.

Thank you for choosing us for your healthcare needs.

Warm regards,  
Dr. Jaydeep Dutta  
Easy Appointment Scheduler  
📧 easyappointmentbot@gmail.com
"""

    try:
        msg = MIMEText(body, "plain")
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        print("=== EMAIL DEBUG INFO ===")
        print("To:", to_email)
        print("Subject:", subject)
        print("Body:", body)
        print("========================")
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent successfully to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
