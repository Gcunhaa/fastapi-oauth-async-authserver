import aiosmtplib
from email.message import EmailMessage
from .config import settings
from pydantic import EmailStr

async def send_noreply_email(message : EmailMessage):
    message['From'] = settings.SMTP_NO_REPLY_EMAIL

    await aiosmtplib.send(message=message, hostname=settings.SMTP_HOSTNAME, port=settings.SMTP_PORT, start_tls=True, username=settings.SMTP_USERNAME, password=settings.SMTP_PASSWORD)

async def send_confirmation_email(email : EmailStr, token : str):
    message = EmailMessage()
    message['To'] = email
    message['Subject'] = 'Email confirmation - AuthServer'
    message.set_content(f'Click here to verify your email and complete registration: https://localhost/confirmemail/{token}')
    await send_noreply_email(message)

async def send_change_password_email(email : EmailStr, token : str):
    message = EmailMessage()
    message['To'] = email
    message['Subject'] = 'Change password - AuthServer'
    message.set_content(f'Click here to your change password: https://localhost/changepassword/{token}')
    await send_noreply_email(message)