import smtplib
import os
from email.message import EmailMessage

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")

def send_otp_email(to_email: str, otp_code: str):
    msg = EmailMessage()
    msg['Subject'] = 'Your Competa Arena Email Verification Code'
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg.set_content(f'Your OTP code for Competa Arena registration is: {otp_code}\nThis code is valid for 10 minutes.')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_PASS)
        smtp.send_message(msg)

def send_password_reset_email(to_email: str, otp_code: str):
    msg = EmailMessage()
    msg['Subject'] = 'Your Competa Arena Password Reset Code'
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg.set_content(f'Your OTP code for resetting your Competa Arena password is: {otp_code}\nThis code is valid for 10 minutes.')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_PASS)
        smtp.send_message(msg)       