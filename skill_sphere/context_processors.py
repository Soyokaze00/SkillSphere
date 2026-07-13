from .menus import SIDEBAR_MENU

def sidebar_menu(request):
    return {
        "sidebar_items": SIDEBAR_MENU
    }