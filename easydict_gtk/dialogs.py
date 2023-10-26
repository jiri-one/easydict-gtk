from pathlib import Path
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GLib, Gdk, GdkPixbuf, GObject, Adw

class SettingsDialog(Gtk.Dialog):
    def __init__(self, win):
        super().__init__()
        self.set_transient_for(win)
        self.set_size_request(800, 800)
        self.set_title("Settings dialog")
        self.box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 10)
        self.add_content_to_settings_box()
        sw = Gtk.ScrolledWindow()
        sw.set_child(self.box)
        frame = Gtk.Frame()
        frame.set_child(sw)
        self.set_child(frame)

    def add_content_to_settings_box(self):
        label = Gtk.Label.new()
        label.set_text("the settings itself will come later")
        self.box.append(label)

    def __call__(self):
        self.set_visible(True)
