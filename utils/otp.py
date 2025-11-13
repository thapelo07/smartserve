import random
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_otp_email(receiver_email: str, otp_code: str):
    """Send OTP via Gmail SMTP"""
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"  # use an app password, not your Gmail password

    subject = "SmartServe OTP Verification"
    body = f"Your verification code is {otp_code}. It will expire in 5 minutes."

    msg = MIMEText(body)
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"✅ OTP sent to {receiver_email}")
    except Exception as e:
        print("❌ Error sending OTP:", e)
