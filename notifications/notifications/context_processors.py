from notifications.models import NotificationSeen


def notifications(request):
    if not request.user.is_authenticated:
        return {
            "notifications": [],
            "unread_notifications": [],
            "unread_count": 0,
            "badge_count": 0,
        }

    qs = request.user.notifications.all()
    unread_count = qs.filter(is_read=False).count()

    seen, _ = NotificationSeen.objects.get_or_create(user=request.user)

    if seen.last_seen_at:
        badge_count = qs.filter(created_at__gt=seen.last_seen_at).count()
    else:
        badge_count = unread_count

    return {
        "notifications": qs.order_by("-created_at")[:10],
        "unread_notifications": qs.filter(is_read=False).order_by("-created_at")[:10],
        "unread_count": unread_count,
        "badge_count": badge_count,
    }
