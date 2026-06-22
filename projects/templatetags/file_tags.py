from django import template

register = template.Library()

FILE_COLORS = {
    "pdf": "bg-red-50 text-red-600",
    "doc": "bg-blue-50 text-blue-600",
    "docx": "bg-blue-50 text-blue-600",
    "xls": "bg-green-50 text-green-600",
    "xlsx": "bg-green-50 text-green-600",
    "zip": "bg-yellow-50 text-yellow-600",
    "rar": "bg-yellow-50 text-yellow-600",
    "png": "bg-purple-50 text-purple-600",
    "jpg": "bg-purple-50 text-purple-600",
    "jpeg": "bg-purple-50 text-purple-600",
    "gif": "bg-pink-50 text-pink-600",
}

@register.filter
def file_color(file_name):
    ext = file_name.split(".")[-1].lower()
    return FILE_COLORS.get(ext, "bg-gray-50 text-gray-600")