import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class TrayMenu(Gtk.Menu):
	def __init__(self):
		super().__init__()
		#item1 - Settings
		self.item1 = Gtk.MenuItem()
		self.item1.set_label("Settings")
		self.append(self.item1)
		#item2 - Help
		self.item2 = Gtk.MenuItem()
		self.item2.set_label("Help")
		self.append(self.item2)
		#item3 - About
		self.item3 = Gtk.MenuItem()
		self.item3.set_label("About")
		self.append(self.item3)
		#item4 - Exit
		self.item4 = Gtk.MenuItem()
		self.item4.set_label("Exit EasyDict")
		self.append(self.item4)
		self.show_all()
		
		