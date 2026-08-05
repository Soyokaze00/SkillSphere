from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_verification_email(email, code):
    send_mail(
        subject="Your verification code",
        message=f"Your code is: {code}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
