# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render ,redirect , get_object_or_404
from django.core.paginator import Paginator
from notifications.utils import get_notification_style
from .models import Notification

# @login_required
# def notification_drawer(request):

#     notifications = Notification.objects.filter(
#         user=request.user
#     )

#     context = {
#         "notifications": notifications
#     }

#     return render(
#         request,
#         "notifications/notification_drawer.html",
#         context
#     )
    

@login_required
def notification_center(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    unread_count = notifications.filter(is_read=False).count()
    total_notifications = Notification.objects.filter(user=request.user).count()
   

    n_type = request.GET.get("type")
    if n_type and n_type != "all":
        notifications = notifications.filter(type=n_type)

    status = request.GET.get("status")
    if status == "unread":
        notifications = notifications.filter(is_read=False)
    elif status == "read":
        notifications = notifications.filter(is_read=True)

    current_status = request.GET.get("status", "all")
    current_type = request.GET.get("type", "all")

    for n in notifications:
        n.style = get_notification_style(n.type)

    paginator = Paginator(notifications, 10) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "notifications/notification_center.html",
        {
            "notifications": page_obj,
            "unread_count": unread_count,
            "total_notifications":total_notifications,
            "current_status": current_status,
            "current_type": current_type,
            "page_obj": page_obj,

        }
    )
    
@login_required
def mark_as_read(request, pk):
    n = request.user.notifications.get(id=pk)
    n.is_read = True
    n.save()
    return redirect("notifications:notification_center")

@login_required
def delete_notification(request, pk):
    notification = get_object_or_404(
        Notification,
        id=pk,
        user=request.user
    )

    notification.delete()

    return redirect("notifications:notification_center")


@login_required
def mark_all_as_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect("notifications:notification_center")