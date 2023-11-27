from easytray import get_dbus_backend, EasyTrayMenu, install_icon_to_xdg_data_home
from settings import images
from pathlib import Path

DBUS_PATH = "/SNIMenu"


def get_tray(app, win):
    icon_image = images["easydict-tray-icon.png"]
    icon_path = install_icon_to_xdg_data_home(Path(icon_image), 285)
    dbus_tray_backend = get_dbus_backend("dasbus")
    tray = dbus_tray_backend(
        category="ApplicationStatus",
        id=app.get_application_id(),
        title="First open source translator.",
        status="Active",
        icon="easydict-tray-icon",
        object_path=DBUS_PATH,
        icon_theme_path=icon_path,
    )
    tray.create_tray_icon()
    return tray


def menu_buttons_catcher(action, target):
    button_label = action.property_get("label")
    print(f"The button {button_label} was pressed.")


def get_menu(app, win):
    menu = EasyTrayMenu(
        menu_items={
            "Settings": lambda *args: win.activate_action("win.settings"),
            "Help": lambda *args: win.activate_action("win.help"),
            "About": lambda *args: win.activate_action("win.about"),
            "Quit": lambda *args: win.activate_action("win.quit"),
        },
        dbus_path=DBUS_PATH,
    )
    menu.create_dbus_menu()
    return menu
