import random
from django.core.mail import send_mail


def generate_code():
    return str(random.randint(100000, 999999))


def send_verification_email(email, code):
    send_mail(
        subject="Your verification code",
        message=f"Your code is: {code}",
        from_email="your_email@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )