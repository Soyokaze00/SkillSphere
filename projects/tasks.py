from celery import shared_task
from .models import ProjectFile
from django.core.mail import send_mail
from django.conf import settings
import os

@shared_task
def process_uploaded_file(file_id):
    try:
        project_file = ProjectFile.objects.get(id=file_id)
    except ProjectFile.DoesNotExist:
        return f"ProjectFile {file_id} does not exist."

    file = project_file.file

    print(f"Processing file: {file.name}")

    file_size = file.size
    file_name = file.name

    print(f"File name: {file_name}")
    print(f"File size: {file_size} bytes")

    text_extensions = {
        ".txt",
        ".py",
        ".js",
        ".html",
        ".css",
        ".json",
        ".xml",
        ".csv",
        ".md",
        ".sql",
        ".java",
        ".cpp",
        ".c",
        ".cs",
    }

    extension = os.path.splitext(file_name)[1].lower()

    if extension in text_extensions:
        try:
            file.open("rb")
            content = file.read()
            file.close()
            text = content.decode("utf-8", errors="ignore")

            print(f"Text content extracted: {len(text)} characters")

            line_count = len(text.splitlines())
            word_count = len(text.split())

            print(f"Lines: {line_count}")
            print(f"Words: {word_count}")

        except Exception as exc:
            print(f"Could not read text file: {exc}")

    else:
        print(f"Skipping text extraction for {extension} file.")

    print(f"Finished processing: {file_name}")

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