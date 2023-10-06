"""
EasyDict-GTK - Python Gtk4 based Application
"""
import sys
from typing import List
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, GObject, Gio, Adw
from widgets import MyListViewStrings


class MyWindow(Adw.ApplicationWindow):
    def __init__(self, title, width, height, **kwargs):
        super(MyWindow, self).__init__(**kwargs)
        self.set_default_size(width, height)
        box = Gtk.Box()
        box.props.orientation = Gtk.Orientation.VERTICAL
        header = Gtk.HeaderBar()
        stack = Adw.ViewStack()
        box.append(header)
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
        lw_frame.set_margin_start(20)
        lw_frame.set_margin_end(20)
        # lw_frame.set_margin_top(10)
        lw_frame.set_margin_bottom(10)
        sw = Gtk.ScrolledWindow()
        # Create Gtk.Listview
        lw = self.listview_str
        sw.set_child(lw)
        lw_frame.set_child(sw)
        return lw_frame

class Application(Adw.Application):
    """Main Aplication class"""

    def __init__(self):
        super().__init__(
            application_id="dk.rasmil.Example", flags=Gio.ApplicationFlags.FLAGS_NONE
        )

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MyWindow("My Gtk4 Application", 800, 800, application=self)
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
