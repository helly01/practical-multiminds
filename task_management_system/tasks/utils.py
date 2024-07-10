from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user):
    print("innnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
    subject = "Welcome to Task Manager"
    message = f"Hi {user.username},\n\nThank you for registering at Task Manager!"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def send_password_reset_email(user, reset_link):
    subject = "Password Reset Request"
    message = f"Hi {user.username},\n\nClick the link below to reset your password:\n{reset_link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def send_task_update_email(user, task):
    subject = f"Task Updated: {task.title}"
    message = f'Hi {user.username},\n\nThe task "{task.title}" has been updated.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
