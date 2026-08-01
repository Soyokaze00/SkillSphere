from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.filter
def highlight(text, query):
    if not text or not query:
        return text

    pattern = re.compile(re.escape(query), re.IGNORECASE)

    highlighted = pattern.sub(
        lambda m: f"<mark>{m.group(0)}</mark>",
        text,
    )

    return mark_safe(highlighted)