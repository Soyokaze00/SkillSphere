from django import template

register = template.Library()

_ICONS = {
    "LOGIN": "🔓",
    "LOGOUT": "🔒",
    "CREATE_PROJECT": "🆕",
    "UPDATE_PROJECT": "✏️",
    "DELETE_PROJECT": "🗑️",
    "UPLOAD_FILE": "📤",
    "DOWNLOAD_FILE": "📥",
    "SEND_FEEDBACK": "💬",
    "LIKE_PROJECT": "❤️",
    "SHARE_PROJECT": "🔗",
    "POST_COMMENT": "💭",
    "FOLLOW_USER": "👥",
    "EDIT_PROFILE": "🙍",
    "DELETE_ACCOUNT": "⚠️",
    "MANAGE_INVITE": "✉️",
    "OTHER": "•",
}


@register.filter
def action_icon(action):
    return _ICONS.get(action, "•")