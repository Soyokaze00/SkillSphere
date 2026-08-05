import re

from django import template
from django.utils.html import format_html, format_html_join

register = template.Library()


@register.filter
def highlight(text, query):
    if not text or not query:
        return text

    text = str(text)
    pattern = re.compile(re.escape(str(query)), re.IGNORECASE)

    parts = []
    last_end = 0

    for match in pattern.finditer(text):
        parts.append((text[last_end : match.start()],))
        parts.append((format_html("<mark>{}</mark>", match.group(0)),))
        last_end = match.end()

    parts.append((text[last_end:],))

    return format_html_join("", "{}", parts)
