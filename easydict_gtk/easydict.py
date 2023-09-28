import gi
import sys
from pathlib import Path

gi.require_version("Gtk", "4.0")
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw
from sys import modules
from os import environ
# imports from my other files with classes and methods

package = Path(__file__).parent.parent
sys.path.append(str(package))

from easydict_gtk.html_generator import CreateHtml, db_search
from easydict_gtk.handlers import Handlers
from easydict_gtk.settings import cwd, cwd_images, Settings

class MainWindow(Gtk.ApplicationWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# basic window settings
		self.set_default_size(360, 640)
		self.set_title("EasyDict-GTK")
		# header bar
		self.header = Gtk.HeaderBar()
		self.set_titlebar(self.header)
		pref_icon = Gtk.Image.new_from_file(str(Path(__file__).parent / "images/ed_pref_icon.png"))
		self.open_button = Gtk.Button(label="Settings")
		self.open_button.set_child(pref_icon)
		self.header.pack_start(self.open_button)
		# widget for data visualization
		self.store = Gtk.ListStore(str, str, str, str)
		treeiter1 = self.store.append(["test", "test", "test", "test", ])
		treeiter2 = self.store.append(["test1", "test1", "test1", "test1", ])
		treeiter3 = self.store.append(["test2", "test2", "test2", "test2", ])
		treeview = Gtk.TreeView(model=self.store)
		column = Gtk.TreeViewColumn("Results:")
		cze = Gtk.CellRendererText()
		eng = Gtk.CellRendererText()
		column.pack_start(cze, True)
		column.pack_start(eng, True)
		column.add_attribute(cze, "text", 0)
		column.add_attribute(eng, "text", 1)
		select = treeview.get_selection()
		select.connect("changed", self.on_tree_selection_changed)

		treeview.append_column(column)




		# main boxes
		self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.set_child(self.main_box)
		self.button = Gtk.Button(label="Search")
		self.dropdown = Gtk.DropDown.new_from_strings(["ENG", "CZE"])
		self.button.connect('clicked', self.hello)
		self.entry = Gtk.Entry()
		self.entry.props.hexpand = True
		self.main_box.append(self.box2)
		self.main_box.append(self.box3)
		self.box2.append(self.entry)
		self.box2.append(self.button)
		self.box2.append(self.dropdown)
		self.box3.append(treeview)

	def hello(self, button):
		print(button)
		treeiter1 = self.store.append(["testik", "test", "test", "test", ])

	def on_tree_selection_changed(self, selection):
		model, treeiter = selection.get_selected()
		if treeiter is not None:
			print("You selected", model[treeiter][0])

class EasyDict(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()



def main(args=sys.argv[1:]):
	import hupper
	if '--reload' in args:
		# start_reloader will only return in a monitored subprocess
		reloader = hupper.start_reloader('easydict_gtk.easydict.main')
		# monitor an extra file
		# reloader.watch_files(['foo.ini'])
		app = EasyDict(application_id="one.jiri.easydict")
		app.run()

if __name__ == "__main__":
	print("zde")
	main()



#
#
# # I inherit from pure classes with just methods
# class EasyDict(Handlers, Settings):
# 	def __init__(self):
# 		"""
# 		Build GUI
# 		"""
# 		#My variables and classes
# 		self.cwd = cwd
# 		self.cwd_images = cwd_images
# 		self.create_html = CreateHtml()
# 		self.db_search = db_search
#
# 		# Build GUI from Glade file
# 		self.builder = Gtk.Builder()
# 		self.builder.add_from_file(str(self.cwd / "ui" / "easydict.glade"))
#
# 		# get objects and set them
# 		gui = self.builder.get_object
# 		self.window = gui("window") # main window
# 		self.header = gui("header") # HeaderBar
# 		self.header.set_decoration_layout('menu:close') # set HeaderBar decoration to show only close button
# 		self.header.props.show_close_button = True	# allow to show close button in HeaderBar
# 		self.box_dicts = gui("box_dicts") # scrolled window for dicts
# 		self.entry_search = gui("entry_search") # searched word object
# 		self.entry_search.set_activates_default(True) # set Enter to act with default widget=button_search
# 		self.button_fulltext = gui("button_fulltext") # for toggle button state
# 		self.button_search = gui("button_search") # search button
# 		self.popover_language = gui("popover_language") # popover for right button mouse click
# 		self.button_search.grab_default() # set search button for default if user hits Enter
# 		self.image_language = gui("image_language") # flag of current language
# 		self.button_easydict = gui("button_easydict") # buton for main menu in HeaderBar
# 		self.popover_main_menu = gui("popover_main_menu") # main menu popover
# 		self.dialog_about = gui("dialog_about") # about dialog
# 		self.dialog_help = gui("dialog_help") # help dialog
# 		self.dialog_settings = gui("dialog_settings") # settings dialog
# 		self.webview = WebKit2.WebView() # because of bug in Glade, it have to be declared here, not in Glade
# 		self.box_dicts.add(self.webview) # add webkit webview to scrolled window
# 		self.webview.load_html(self.create_html.default_html, "file://") # not necessary row, but maybe nice welcome image is good!
#
# 		# clipboard function
# 		self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
# 		self.clipboard.connect("owner-change", self.onClipboard)
#
# 		# settings objects
# 		self.checkbutton_scan = gui("checkbutton_scan")
# 		self.checkbutton_size = gui("checkbutton_size")
# 		self.combobox_language = gui("combobox_language")
#
# 		# connect signals from builder
# 		self.builder.connect_signals(self)
#
# 		# initiate user settings
# 		self.initiate_settings()
#
# 		# settings of windows
# 		self.window.set_icon_from_file(str(self.cwd_images / "ed_icon.png"))
# 		self.window.set_keep_above(True)
# 		self.dialog_about.set_keep_above(True)
# 		self.dialog_help.set_keep_above(True)
# 		self.dialog_settings.set_keep_above(True)
#
# 		# tray icon (I am using XAppStatusIcon, because it is last working solution for GTK)
# 		if 'gi.repository.XApp' not in modules.keys() or environ.get("DESKTOP_SESSION") == "gnome": # if import of XApp was not succesful or we are on Gnome, where the tray is not exists
# 			self.tray = None # because of onXButton handler
# 			self.window.show_all() # without show_all() the window will be hidden
# 		else:
# 			self.tray = StatusIcon()
# 			self.tray.set_icon_name(str(self.cwd_images / "ed_tray_icon.png"))
# 			self.tray.set_tooltip_text("EasyDict - The open translator")
# 			self.tray.connect("button-press-event", self.onTrayClicked)
# 			self.menu = TrayMenu() # tray icon menu from class TrayMenu in file tray_menu.py
# 			self.menu.item1.connect("activate", self.onSettingsClicked) # connect menu item Settings
# 			self.menu.item2.connect("activate", self.onHelpClicked) # connect menu item Help
# 			self.menu.item3.connect("activate", self.onAboutClicked) # connect menu item About
# 			self.menu.item4.connect("activate", self.onExitClicked) # connect menu item Exit
# 			self.tray.set_secondary_menu(self.menu)
# 			self.window.props.visible = False
#
# def main():
# 	gui = EasyDict()
# 	Gtk.main()
