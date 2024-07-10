from django.core.mail import send_mail
from django.conf import settings


def send_email(subject, message, recipient_list):
    """
    Sends an email using SendGrid.

    :param subject: Subject of the email.
    :param message: Body of the email.
    :param recipient_list: List of email addresses to send the email to.
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )
