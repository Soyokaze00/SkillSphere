def notifications(request):

    if request.user.is_authenticated:

        qs = request.user.notifications.all()

        return {
            "notifications": qs.order_by("-created_at")[:10],

            "unread_notifications": qs.filter(
                is_read=False
            ).order_by("-created_at")[:10],

            "unread_count": qs.filter(
                is_read=False
            ).count(),
        }

    return {
        "notifications": [],
        "unread_notifications": [],
        "unread_count": 0,
    }    
    
    
    
    
