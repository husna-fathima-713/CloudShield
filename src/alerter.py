import smtplib
from email.mime.text import MIMEText


def send_alert(message):
    sender = "yourgmail@gmail.com"
    password = "your16charapppassword"
    receiver = "yourgmail@gmail.com"

    msg = MIMEText(message)
    msg["Subject"] = "CloudShield Security Alert"
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            print("Email alert sent successfully.")

    except Exception as e:
        print("Email alert failed:", e)