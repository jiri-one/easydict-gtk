from pathlib import Path
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GLib, Gdk, GdkPixbuf, GObject, Adw

# internal imports
from settings import images

class FrontPage(Gtk.Box):
    """Front page of EasyDict-GTK in one Box"""

    def __init__(self):
        super().__init__()
        self.set_orientation(Gtk.Orientation.VERTICAL)
        welcome = self.welcome_label()
        self.append(welcome)
        logo = self.logo_image()
        self.append(logo)
        slogan = self.slogan_label()
        self.append(slogan)

    def welcome_label(self):
        label = Gtk.Label.new()
        # markup = GLib.markup_escape_text()
        label.set_justify(Gtk.Justification.CENTER)
        label.set_wrap(True)
        label.set_markup(
            '\n<b><span size="x-large">Welcome to EasyDict</span></b>\n\nJust start typing to see results!\n'
        )
        return label

    def logo_image(self):
        logo_pixbuf = GdkPixbuf.Pixbuf.new_from_file(images["ed_icon.png"])
        print(images.get("ed_icon.png", None))
        image = Gtk.Image.new_from_pixbuf(logo_pixbuf)
        image.set_size_request(500, 500)
        image.set_halign(Gtk.Align.CENTER)
        return image

    def slogan_label(self):
        label = Gtk.Label.new()
        # markup = GLib.markup_escape_text()
        label.set_justify(Gtk.Justification.CENTER)
        label.set_wrap(True)
        label.set_markup(
            "\n<big>The first translator which is completely open with dictionary data too.</big>"
        )
        return label

