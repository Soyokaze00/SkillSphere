from django import template
from notifications.utils import get_notification_style
from django.utils import timezone

register = template.Library()

@register.filter
def notification_style(notification_type):
    return get_notification_style(notification_type)


@register.filter
def timesince_precise(value):
    if not value:
        return ""
    now = timezone.now()
    diff = now - value
    seconds = int(diff.total_seconds())

    if seconds < 60:
        unit = "second" if seconds == 1 else "seconds"
        return f"{seconds} {unit}"
    elif seconds < 3600:
        minutes = seconds // 60
        unit = "minute" if minutes == 1 else "minutes"
        return f"{minutes} {unit}"
    elif seconds < 86400:
        hours = seconds // 3600
        unit = "hour" if hours == 1 else "hours"
        return f"{hours} {unit}"
    else:
        days = seconds // 86400
        unit = "day" if days == 1 else "days"
        return f"{days} {unit}"