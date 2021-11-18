import gi

gi.require_version("Gtk", "3.0")
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, WebKit2, Gdk
from sys import modules
try:
	gi.require_version("XApp", "1.0")
	from gi.repository.XApp import StatusIcon
	from easydict_gtk.tray_menu import TrayMenu # import of TrayMenu makes sense only if XApps are presented
except (ValueError, ModuleNotFoundError):
	print("XApps not found, tray icon is not available.")
from os import environ
# imports from my other files with classes and methods
from easydict_gtk.html_generator import CreateHtml, db_search
from easydict_gtk.handlers import Handlers
from easydict_gtk.settings import cwd, cwd_images, Settings

# I inherit from pure classes with just methods
class EasyDict(Handlers, Settings):
	def __init__(self):
		"""
		Build GUI
		"""
		#My variables and classes
		self.cwd = cwd
		self.cwd_images = cwd_images
		self.create_html = CreateHtml()
		self.db_search = db_search
		
		# Build GUI from Glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file(str(self.cwd / "ui" / "easydict.glade"))
		
		# get objects and set them
		gui = self.builder.get_object
		self.window = gui("window") # main window
		self.header = gui("header") # HeaderBar
		self.header.set_decoration_layout('menu:close') # set HeaderBar decoration to show only close button
		self.header.props.show_close_button = True	# allow to show close button in HeaderBar	
		self.box_dicts = gui("box_dicts") # scrolled window for dicts
		self.entry_search = gui("entry_search") # searched word object
		self.entry_search.set_activates_default(True) # set Enter to act with default widget=button_search
		self.button_fulltext = gui("button_fulltext") # for toggle button state
		self.button_search = gui("button_search") # search button
		self.popover_language = gui("popover_language") # popover for right button mouse click
		self.button_search.grab_default() # set search button for default if user hits Enter
		self.image_language = gui("image_language") # flag of current language
		self.button_easydict = gui("button_easydict") # buton for main menu in HeaderBar
		self.popover_main_menu = gui("popover_main_menu") # main menu popover
		self.dialog_about = gui("dialog_about") # about dialog
		self.dialog_help = gui("dialog_help") # help dialog
		self.dialog_settings = gui("dialog_settings") # settings dialog
		self.webview = WebKit2.WebView() # because of bug in Glade, it have to be declared here, not in Glade
		self.box_dicts.add(self.webview) # add webkit webview to scrolled window
		self.webview.load_html(self.create_html.default_html, "file://") # not necessary row, but maybe nice welcome image is good!
		
		# clipboard function
		self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
		self.clipboard.connect("owner-change", self.onClipboard)
		
		# settings objects
		self.checkbutton_scan = gui("checkbutton_scan")
		self.checkbutton_size = gui("checkbutton_size")
		self.combobox_language = gui("combobox_language")
		
		# connect signals from builder
		self.builder.connect_signals(self)		
		
		# initiate user settings
		self.initiate_settings()
		
		# settings of windows
		self.window.set_icon_from_file(str(self.cwd_images / "ed_icon.png"))
		self.window.set_keep_above(True)
		self.dialog_about.set_keep_above(True)
		self.dialog_help.set_keep_above(True)
		self.dialog_settings.set_keep_above(True)
		
		# tray icon (I am using XAppStatusIcon, because it is last working solution for GTK)
		if 'gi.repository.XApp' not in modules.keys() or environ.get("DESKTOP_SESSION") == "gnome": # if import of XApp was not succesful or we are on Gnome, where the tray is not exists 
			self.tray = None # because of onXButton handler
			self.window.show_all() # without show_all() the window will be hidden	
		else:
			self.tray = StatusIcon()
			self.tray.set_icon_name(str(self.cwd_images / "ed_tray_icon.png"))
			self.tray.set_tooltip_text("EasyDict - The open translator")
			self.tray.connect("button-press-event", self.onTrayClicked)
			self.menu = TrayMenu() # tray icon menu from class TrayMenu in file tray_menu.py
			self.menu.item1.connect("activate", self.onSettingsClicked) # connect menu item Settings
			self.menu.item2.connect("activate", self.onHelpClicked) # connect menu item Help
			self.menu.item3.connect("activate", self.onAboutClicked) # connect menu item About
			self.menu.item4.connect("activate", self.onExitClicked) # connect menu item Exit
			self.tray.set_secondary_menu(self.menu)
			self.window.props.visible = False			
		
def main():
	gui = EasyDict()
	Gtk.main()






