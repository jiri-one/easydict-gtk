"""
EasyDict-GTK - Python Gtk4 based Application
"""
import sys
import os
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, GLib, GObject, Gio, Adw
from widgets import MyListViewStrings, SearchBar, FrontPage

# internal imports
from settings import images

class MyWindow(Adw.ApplicationWindow):
    def __init__(self, title, width, height, loop, **kwargs):
        super(MyWindow, self).__init__(**kwargs)
        self.load_css("ui/search_box.css")
        self.set_default_size(width, height)
        self.set_title(title)
        self.main_box = Gtk.Box()
        self.main_box.props.orientation = Gtk.Orientation.VERTICAL
        title_label = Gtk.Label.new()
        title_label.set_justify(Gtk.Justification.CENTER)
        title_label.set_markup('EasyDict-GTK\n<small>Completely open translator</small>')
        header = Gtk.HeaderBar()
        header.set_title_widget(title_label)
        # Add Options button (Menu content need to be added)
        opt_image = Gtk.Image.new_from_file(images["ed_pref_icon.png"])
        opt_image.set_size_request(60, 60)
        option_btn = Gtk.MenuButton()
        option_btn.set_child(opt_image)
        option_btn.set_child_visible(True)
        self.search_options = option_btn
        header.pack_start(option_btn)
        search = SearchBar(loop, self)
        self.front_page = FrontPage()
        self.stack = Adw.ViewStack()
        self.main_box.append(header)
        self.main_box.append(search)
        self.main_box.append(self.front_page)
        content = self.setup_content()
        self.stack.add(content)
        # box.append(self.stack)
        self.set_content(self.main_box)

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

    def __init__(self, loop):
        super().__init__(
            application_id="one.jiri.easydict-gtk",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )
        self._loop = loop

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MyWindow("EasyDict-GTK", 600, 1200, loop=self._loop, application=self)
        win.present()


def run_event_loop(q):
    """Run asyncio event loop in ThreadPoolExecutor in another Thread"""
    loop = asyncio.new_event_loop()
    q.put(loop)
    loop.run_forever()


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

        q = Queue()
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(run_event_loop, q)
            loop = q.get()
            app = Application(loop)
            app.run()


if __name__ == "__main__":
    main()
