from .models import Notification

def create_notification(user, title, message, notification_type="system", link=None):
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        type=notification_type,
        link=link,
    )

NOTIFICATION_STYLES = {
    "project": {
        "color": "bg-purple-50 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400",
        "icon": "<svg class=\"w-5 h-5\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z\"></path></svg>",
        "border": "border-purple-500",
        "badge": "bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400"
    },
    "comment": {
        "color": "bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400",
        "icon": "<svg class=\"w-5 h-5\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z\"></path></svg>",
        "border": "border-blue-500",
        "badge": "bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400"
    },
    "feedback": {
        "color": "bg-yellow-50 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400",
        "icon": "<svg class=\"w-5 h-5\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z\"></path></svg>",
        "border": "border-yellow-500",
        "badge": "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400"
    },
    "invite": {
        "color": "bg-teal-50 dark:bg-teal-900/30 text-teal-600 dark:text-teal-400",
        "icon": "<svg class=\"w-5 h-5\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z\"></path></svg>",
        "border": "border-teal-500",
        "badge": "bg-teal-100 dark:bg-teal-900/30 text-teal-700 dark:text-teal-400"
    },
    "member": {
        "color": "bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-400",
        "icon": "<svg class=\"w-5 h-5\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z\"></path></svg>",
        "border": "border-green-500",
        "badge": "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400"
    },
    "follow": {
        "color": "bg-pink-50 dark:bg-pink-900/30 text-pink-600 dark:text-pink-400",
        "icon": "<svg class=\"w-5 h-5\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z\"></path><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M16 11a3 3 0 11-6 0 3 3 0 016 0z\"></path><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M19 15v-2m0 0v-2m0 2h-2m2 0h2\"></path></svg>",
        "border": "border-pink-500",
        "badge": "bg-pink-100 dark:bg-pink-900/30 text-pink-700 dark:text-pink-400"
    },
    "like": {
        "color": "bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400",
        "icon": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" class=\"lucide lucide-heart-icon lucide-heart\"><path d=\"M2 9.5a5.5 5.5 0 0 1 9.591-3.676.56.56 0 0 0 .818 0A5.49 5.49 0 0 1 22 9.5c0 2.29-1.5 4-3 5.5l-5.492 5.313a2 2 0 0 1-3 .019L5 15c-1.5-1.5-3-3.2-3-5.5\"/></svg>",
        "border": "border-pink-500",
        "badge": "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400"
    },
    "system": {
        "color": "bg-gray-50 dark:bg-gray-800 text-gray-600 dark:text-gray-400",
        "icon": "<svg class=\"w-5 h-5\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z\"></path><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M15 12a3 3 0 11-6 0 3 3 0 016 0z\"></path></svg>",
        "border": "border-gray-500",
        "badge": "bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-400"
    }
}

def get_notification_style(notification_type):
    return NOTIFICATION_STYLES.get(
        notification_type,
        NOTIFICATION_STYLES["system"]
    )