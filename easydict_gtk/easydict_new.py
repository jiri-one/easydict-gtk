"""
EasyDict-GTK - Python Gtk4 based Application
"""
import sys
import os
from typing import List
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, GLib, GObject, Gio, Adw
from widgets import MyListViewStrings, SearchBar


class MyWindow(Adw.ApplicationWindow):
    def __init__(self, title, width, height, **kwargs):
        super(MyWindow, self).__init__(**kwargs)
        self.load_css("ui/search_box.css")
        self.set_default_size(width, height)
        self.set_title(title)
        box = Gtk.Box()
        box.props.orientation = Gtk.Orientation.VERTICAL
        header = Gtk.HeaderBar()
        # Add Options button (Menu content need to be added)
        option_btn = Gtk.MenuButton()
        option_btn.set_icon_name("preferences-other-symbolic")
        self.search_options = option_btn
        header.pack_start(option_btn)
        search = SearchBar(self)
        stack = Adw.ViewStack()
        box.append(header)
        box.append(search)
        content = self.setup_content()
        stack.add(content)
        box.append(stack)
        self.set_content(box)

    def setup_content(self):
        # Simple Listview with strings
        self.listview_str = MyListViewStrings(self)
        lw_frame = Gtk.Frame()
        lw_frame.set_valign(Gtk.Align.FILL)
        lw_frame.set_vexpand(True)
        # lw_frame.set_margin_start(20)
        # lw_frame.set_margin_end(20)
        # lw_frame.set_margin_top(10)
        # lw_frame.set_margin_bottom(10)
        sw = Gtk.ScrolledWindow()
        # Create Gtk.Listview
        lw = self.listview_str
        sw.set_child(lw)
        lw_frame.set_child(sw)
        return lw_frame

    def load_css(self, css_fn):
        """create a provider for custom styling"""
        css_full_path = (Path(__file__).parent / css_fn).resolve()
        print(css_full_path, os.path.exists(css_full_path))
        if css_fn and os.path.exists(css_fn):
            css_provider = Gtk.CssProvider()
            try:
                css_provider.load_from_path(css_full_path)
            except GLib.Error as e:
                print(f"Error loading CSS : {e} ")
                return None
            print(f"loading custom styling : {css_fn}")
            self.css_provider = css_provider


class Application(Adw.Application):
    """Main Aplication class"""

    def __init__(self):
        super().__init__(
            application_id="one.jiri.easydict-gtk",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MyWindow("EasyDict-GTK", 600, 1200, application=self)
        win.present()


def main(args=sys.argv[1:]):
    """Run the main application"""
    if "--reload" in args:
        import hupper

        package = Path(__file__).parent.parent
        sys.path.append(str(package))
        # start_reloader will only return in a monitored subprocess
        reloader = hupper.start_reloader("easydict_gtk.easydict_new.main")
        # monitor an extra file
        # reloader.watch_files(['foo.ini'])
        app = Application()
        return app.run()


if __name__ == "__main__":
    main()
