from .models import Notification

def notifications(request):

    if request.user.is_authenticated:
        qs = request.user.notifications.all()

        return {
            "notifications": Notification.objects.filter(
                user=request.user
            ).order_by("-created_at")[:10],
            "unread_count": qs.filter(is_read=False).count(),

        }

    return {
        "notifications": [],
        "unread_count": 0,

    }
    
    
    
    
    
