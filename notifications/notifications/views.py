from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from notifications.utils import get_notification_style

from .models import Notification, NotificationSeen


@login_required
def notification_center(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")

    unread_count = notifications.filter(is_read=False).count()
    read_count = notifications.filter(is_read=True).count()

    total_notifications = notifications.count()

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

    unread_notifications = request.user.notifications.filter(is_read=False)

    return render(
        request,
        "notifications/notification_center.html",
        {
            "notifications": page_obj,
            "unread_count": unread_count,
            "total_notifications": total_notifications,
            "current_status": current_status,
            "current_type": current_type,
            "page_obj": page_obj,
            "page_title": "Notification",
            "read_count": read_count,
            "unread_notifications": unread_notifications,
        },
    )


@login_required
@require_POST
def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, id=pk, user=request.user)

    if not notification.is_read:
        notification.is_read = True
        notification.save()

        messages.success(request, "Notification marked as read successfully.")
    else:
        messages.info(request, "This notification has already been read.")

    return redirect("notifications:notification_center")


@login_required
@require_POST
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, id=pk, user=request.user)

    notification.delete()

    messages.success(request, "Notification deleted successfully.")

    return redirect("notifications:notification_center")


@login_required
@require_POST
def mark_all_as_read(request):
    updated_count = request.user.notifications.filter(is_read=False).update(is_read=True)

    if updated_count:
        messages.success(request, f"{updated_count} notifications marked as read.")
    else:
        messages.info(request, "There are no unread notifications.")

    return redirect("notifications:notification_center")


@login_required
@require_POST
def delete_all_notifications(request):
    deleted_count, _ = request.user.notifications.all().delete()

    if deleted_count:
        messages.success(request, f"{deleted_count} notifications deleted.")
    else:
        messages.info(request, "You have no notifications to delete.")

    return redirect("notifications:notification_center")


@login_required
@require_POST
def mark_notifications_seen(request):
    seen, _ = NotificationSeen.objects.get_or_create(user=request.user)
    seen.last_seen_at = timezone.now()
    seen.save(update_fields=["last_seen_at"])
    return JsonResponse({"status": "ok"})
