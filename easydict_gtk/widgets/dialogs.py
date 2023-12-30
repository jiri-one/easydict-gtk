from pathlib import Path
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GLib, Gdk, GdkPixbuf, GObject, Adw

# internal imports
from settings import ed_setup, LANGUAGES_DATA as lng_data
from .drop_down import LanguageDropdown


class SettingsDialog(Gtk.Dialog):
    def __init__(self, win):
        self.win = win
        super().__init__()
        self.set_transient_for(win)
        self.set_size_request(800, 800)
        self.set_title("Settings dialog")
        self.grid = Gtk.Grid.new()
        self.add_content_to_settings_box()
        sw = Gtk.ScrolledWindow()
        sw.set_child(self.grid)
        frame = Gtk.Frame()
        frame.set_child(sw)
        self.set_child(frame)

    def add_content_to_settings_box(self):
        # Title of the settings
        label = Gtk.Label.new()
        label.set_markup("\n<b>EasyDict settings:</b>\n")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.grid.attach(label, 0, 0, 2, 1)  # child, column, row, width, height
        # two boxes like two columns

        # setting for remember window size
        label = Gtk.Label.new("Remember the window size?")
        self.grid.attach(label, 0, 1, 1, 1)

        checkbutton = Gtk.CheckButton.new()
        checkbutton.set_active(ed_setup.win_size_remember)
        checkbutton.props.halign = Gtk.Align.CENTER
        checkbutton.connect(
            "toggled",
            lambda obj: ed_setup.write_settings("win_size_remember", obj.props.active),
        )
        self.grid.attach(checkbutton, 1, 1, 1, 1)
        # setting for clipboard scan
        label = Gtk.Label.new("Clippboard snan?")
        self.grid.attach(label, 0, 2, 1, 1)
        checkbutton = Gtk.CheckButton.new()
        checkbutton.set_active(ed_setup.clipboard_scan)
        checkbutton.props.halign = Gtk.Align.CENTER
        checkbutton.connect(
            "toggled",
            lambda obj: ed_setup.write_settings("clipboard_scan", obj.props.active),
        )
        self.grid.attach(checkbutton, 1, 2, 1, 1)
        # setting for default language
        label = Gtk.Label.new("Default language for search:")
        label.set_hexpand(True)
        self.grid.attach(label, 0, 3, 1, 1)
        dropdown = LanguageDropdown()
        dropdown.set_hexpand(False)
        dropdown.connect("notify::selected-item", self.on_change)
        self.grid.attach(dropdown, 1, 3, 1, 1)

    def on_change(self, widget, param_spec):
        selected_item = widget.get_selected_item()
        # sync setting with actual search language
        self.win.search.dropdown.set_selected(selected_item.id)
        # write settings to configuration file
        ed_setup.search_language = selected_item.language

    def __call__(self):
        self.set_visible(True)
