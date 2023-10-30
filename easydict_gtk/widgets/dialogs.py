from pathlib import Path
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GLib, Gdk, GdkPixbuf, GObject, Adw

# internal imports
from settings import ed_setup
from .drop_down import LanguageDropdown


class SettingsDialog(Gtk.Dialog):
    def __init__(self, win):
        self.win = win
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
        # Title of the settings column
        label = Gtk.Label.new("EasyDict settings:")

        # label.set_justify(Gtk.Justification.CENTER)
        self.box.append(label)
        # setting for remember window size
        checkbutton = Gtk.CheckButton.new_with_label("Remember the window size?")
        checkbutton.set_active(ed_setup.win_size_remember)
        checkbutton.props.halign = Gtk.Align.CENTER
        checkbutton.connect(
            "toggled",
            lambda obj: ed_setup.write_settings("win_size_remember", obj.props.active),
        )
        self.box.append(checkbutton)
        # setting for clipboard scan
        checkbutton = Gtk.CheckButton.new_with_label("Clippboard snan?")
        checkbutton.set_active(ed_setup.clipboard_scan)
        checkbutton.props.halign = Gtk.Align.CENTER
        checkbutton.connect(
            "toggled",
            lambda obj: ed_setup.write_settings("clipboard_scan", obj.props.active),
        )
        self.box.append(checkbutton)
        # setting for default language
        label = Gtk.Label.new("Default language for search:")
        dropdown = LanguageDropdown()
        box = Gtk.Box()
        box.set_orientation(Gtk.Orientation.HORIZONTAL)
        box.append(label)
        box.append(dropdown)
        self.box.append(box)

    def __call__(self):
        self.set_visible(True)
