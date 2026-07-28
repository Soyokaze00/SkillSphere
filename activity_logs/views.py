from collections import defaultdict
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.shortcuts import render
from django.utils import timezone

from .models import ActivityLog

CATEGORY_MAP = {
    ActivityLog.Action.LOGIN: "login",
    ActivityLog.Action.LOGOUT: "login",
    ActivityLog.Action.CREATE_PROJECT: "project",
    ActivityLog.Action.UPDATE_PROJECT: "project",
    ActivityLog.Action.DELETE_PROJECT: "project",
    ActivityLog.Action.UPLOAD_FILE: "file",
    ActivityLog.Action.DOWNLOAD_FILE: "file",
    ActivityLog.Action.LIKE_PROJECT: "social",
    ActivityLog.Action.SHARE_PROJECT: "social",
    ActivityLog.Action.POST_COMMENT: "social",
    ActivityLog.Action.FOLLOW_USER: "social",
    ActivityLog.Action.EDIT_PROFILE: "account",
    ActivityLog.Action.DELETE_ACCOUNT: "account",
    ActivityLog.Action.MANAGE_INVITE: "project",
    ActivityLog.Action.SEND_FEEDBACK: "account",
    ActivityLog.Action.OTHER: "other",
}


@login_required
def activity_list(request):
    logs_queryset = (
        ActivityLog.objects
        .filter(user=request.user)
        .order_by("-created_at")[:200]
    )

    logs_data = []
    counts = defaultdict(int)

    for log in logs_queryset:
        category = CATEGORY_MAP.get(log.action, "other")
        counts[category] += 1
        logs_data.append({
            "id": log.id,
            "type": category,
            "action_label": log.get_action_display(),
            "desc": log.description or log.get_action_display(),
            "ip": log.ip_address or "—",
            "time": naturaltime(log.created_at),
            "date": timezone.localtime(log.created_at).strftime("%b %d, %Y %H:%M"),
        })


    today = timezone.localdate()
    week_start = today - timedelta(days=6)
    week_end = today
    week_range = f"{week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')}"

    weekly_qs = ActivityLog.objects.filter(
        user=request.user,
        created_at__date__gte=week_start,
    )

    day_order = [(week_start + timedelta(days=i)) for i in range(7)]
    weekly = {d.strftime("%a"): defaultdict(int) for d in day_order}

    for log in weekly_qs:
        day_key = timezone.localtime(log.created_at).strftime("%a")
        if day_key in weekly:
            category = CATEGORY_MAP.get(log.action, "other")
            weekly[day_key][category] += 1

    weekly_list = [
        {
            "day": day,
            "login": data.get("login", 0),
            "project": data.get("project", 0),
            "file": data.get("file", 0),
            "social": data.get("social", 0),
            "account": data.get("account", 0),
        }
        for day, data in weekly.items()
    ]

    activity_data = {
        "logs": logs_data,
        "weekly": weekly_list,
        "week_range": week_range,
        "summary": {
            "login": counts.get("login", 0),
            "project": counts.get("project", 0),
            "file": counts.get("file", 0),
            "social": counts.get("social", 0),
            "account": counts.get("account", 0),
        },
    }

    return render(request, "activity_logs/activity_list.html", {
        "activity_data": activity_data,
    })