import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .config import settings
from pydantic import EmailStr
import codecs

with open('templates/email/resetpassword.html', 'r') as file:
    change_password_template = file.read()

with open('templates/email/confirm-email.html', 'r') as file:
    confirm_email_template = file.read()

async def send_noreply_email(message : MIMEMultipart):
    message['From'] = settings.SMTP_NO_REPLY_EMAIL

    await aiosmtplib.send(message=message, hostname=settings.SMTP_HOSTNAME, port=settings.SMTP_PORT, start_tls=True, username=settings.SMTP_USERNAME, password=settings.SMTP_PASSWORD)

async def send_confirmation_email(email : EmailStr, token : str):
    message = MIMEMultipart('alternative')
    message['To'] = email
    message['Subject'] = 'Email confirmation - AuthServer'
    message.add_header('Content-Type', 'text/html')
    html_message = MIMEText(confirm_email_template.replace("{token}",token), 'html')
    message.attach(html_message)
    await send_noreply_email(message)

async def send_change_password_email(email : EmailStr, token : str):
    message = MIMEMultipart('alternative')
    message['To'] = email
    message['Subject'] = 'Change password - AuthServer'
    message.add_header('Content-Type', 'text/html')
    html_message = MIMEText(change_password_template.replace("{token}",token), 'html')
    message.attach(html_message)
    await send_noreply_email(message)