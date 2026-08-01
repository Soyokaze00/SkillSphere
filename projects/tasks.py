from celery import shared_task
from .models import ProjectFile
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def process_uploaded_file(file_id):
    project_file = ProjectFile.objects.get(id=file_id)
    print(f"Processing file: {project_file.file.name}")
    return True


@shared_task
def send_project_invite_email(recipient_email, subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient_email],
        fail_silently=False,
    )