import gi

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, WebKit2, Gdk
from html_generator import CreateHtml


from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image

from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from orjson_storage import ORJSONStorage
import difflib
import re

db = TinyDB("eng-cze.json", storage=CachingMiddleware(ORJSONStorage))
eng_cze = db.table("eng_cze")
MyQuery = Query()


def db_search(language, text, fulltext):
    if fulltext == False:
        text = rf"\b{text}\b"
    results = eng_cze.search(MyQuery[language].search(text, flags=re.IGNORECASE))
    results_with_matchratio = []
    for result in results:
        ratio = difflib.SequenceMatcher(None, result[language], text).ratio()
        results_with_matchratio.append([result, ratio])
    return sorted(results_with_matchratio, key=lambda x: x[1], reverse=True)


class EasyDict(object):
    def __init__(self):
        """
        Build GUI
        """
        # My variables and classes
        self.language = "eng"
        self.create_html = CreateHtml()

        # Build GUI from Glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file(
            "easydict.glade"
        )  # this file have to be in same directory like easydict.py file

        # get objects
        gui = self.builder.get_object
        self.window = gui("window")  # main window
        self.box_dicts = gui("box_dicts")  # scrolled window for dicts
        self.entry_search = gui("entry_search")  # searched word object
        self.entry_search.set_activates_default(
            True
        )  # set Enter to act with default widget=button_search
        self.button_fulltext = gui("button_fulltext")  # for toggle button state
        self.button_search = gui("button_search")  # search button
        self.popover_language = gui(
            "popover_language"
        )  # popover for right button mouse click
        self.button_search.grab_default()  # set search button for default if user hits Enter
        self.image_language = gui("image_language")  # flag of current language
        self.button_easydict = gui(
            "button_easydict"
        )  # TADY POKRAČOVAT A PŘIDAT BUBLINKOVÉ MENU
        self.popover_main_menu = gui("popover_main_menu")
        self.webview = (
            WebKit2.WebView()
        )  # because of bug in Glade, it have to be declared here, not in Glade
        self.box_dicts.add(self.webview)  # add webkit webview to scrolled window
        self.webview.load_html(
            self.create_html.default_html, "file:///"
        )  # not necessary row, but maybe nice welcome image is good!

        # connect signals
        self.builder.connect_signals(self)

        # final settings and show (hidden) windows
        # self.window.props.visible = True
        self.window.set_icon_from_file("ed_icon.png")
        self.window.set_keep_above(False)
        self.window.show_all()

        # start pystray for trayicon
        self.trayIcon()

    def onXButton(self, *args):
        self.window.hide()
        return True

    def onSearchClicked(self, button):
        # create query for pymongo
        if (
            self.entry_search.props.text_length > 0
        ):  # user is not able to send empty query
            # if self.button_fulltext.get_active() == True:
            # self.myquery =  { "eng": { "$regex": f"\^*{self.entry_search.get_text()}\$*" } }
            # if self.button_fulltext.get_active() == False:
            # self.myquery = { "$text": { "$search": f"{self.entry_search.get_text()}" } }
            # self.mydoc = mycol.find(self.myquery)
            # self.html = CreateHtml(self.mydoc).html_string
            # self.webview.load_html(self.html)

            self.results = db_search(
                self.language,
                self.entry_search.get_text(),
                self.button_fulltext.get_active(),
            )
            self.html = self.create_html.finish_html(self.results)
            self.webview.load_html(self.html)

    def onLangClicked(self, button):
        if button.props.text == "ENG":
            self.image_language.props.file = "flag_eng.svg"
            self.language = "eng"
        if button.props.text == "CZE":
            self.image_language.props.file = "flag_cze.svg"
            self.language = "cze"

    def onSearchRightClick(self, button, event):
        # detects if the right mouse button is pressed https://lazka.github.io/pgi-docs/Gdk-3.0/classes/Event.html#Gdk.Event.get_button
        if event.type == Gdk.EventType.BUTTON_PRESS and event.get_button() == (True, 3):
            self.popover_language.show_all()
            self.popover_language.popup()

    def onEasyDictClicked(self, button):
        self.popover_main_menu.show_all()
        self.popover_main_menu.popup()

    def onExitClicked(self, button):
        Gtk.main_quit()

    def trayIcon(self):
        self.tray_img = Image.open("ed_tray_icon.png")
        self.my_menu = menu(
            item(text="Show EasyDict", action=self.alternate, default=True),
            item(text="Exit EasyDict", action=Gtk.main_quit),
        )
        self.icon = icon("EasyBright", self.tray_img, menu=self.my_menu)
        self.icon.run()

    def alternate(self):
        if self.window.props.visible:
            self.window.hide()
        else:
            self.window.show()


if __name__ == "__main__":
    gui = EasyDict()
    Gtk.main()
