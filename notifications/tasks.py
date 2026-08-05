# from celery import shared_task

# from .models import Notification


# @shared_task
# def create_notification_task(
#     user_id,
#     title,
#     message,
#     notification_type="system",
#     link=None,
# ):
#     Notification.objects.create(
#         user_id=user_id,
#         title=title,
#         message=message,
#         type=notification_type,
#         link=link,
#     )