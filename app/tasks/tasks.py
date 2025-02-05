from pydantic import EmailStr
import smtplib

from app.config import settings
from app.tasks.celery import celery
from app.tasks.email_templates import create_booking_confirmation_template


@celery.task()
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr
):
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(msg_content)