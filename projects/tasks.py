from celery import shared_task
from .models import ProjectFile

@shared_task
def process_uploaded_file(file_id):
    file_obj = ProjectFile.objects.get(id=file_id)
    print(f"Processing file: {file_obj.file.name}")
    return True
