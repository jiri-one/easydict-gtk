import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class Handlers:
	def onXButton(self, *args):
		"""This is used to hide main window, when the close button (X) is pressed"""
		if self.tray != None:
			self.window.hide()
		else:
			self.window.iconify() # minize it on gnome or there, where aro not XApps
		return True
	
	def onSearchClicked(self, button):
		if self.entry_search.props.text_length > 0: # user is not able to send empty query
			self.results = self.db_search(self.language, self.entry_search.get_text(), self.button_fulltext.get_active())
			self.html = self.create_html(self.results, self.language)
			self.webview.load_html(self.html)
	
	def onLangClicked(self, button):
		if button.props.text == "English":
			self.language = 'eng'
		if button.props.text == "Czech":
			self.language = 'cze'
		self.image_language.props.file = str(self.cwd_images / f"flag_{self.language}.svg")
	
	def onSearchRightClick(self, button, event):
		# detects if the right mouse button is pressed https://lazka.github.io/pgi-docs/Gdk-3.0/classes/Event.html#Gdk.Event.get_button
		if event.type ==  Gdk.EventType.BUTTON_PRESS and event.get_button() == (True, 3):
			self.popover_language.show_all()
			self.popover_language.popup()
	
	def onEasyDictClicked(self, button):
		self.popover_main_menu.show_all()
		self.popover_main_menu.popup()
	
	def onExitClicked(self, *args):
		Gtk.main_quit()
	
	def onTrayClicked(self, status_icon, x, y, button, time, panel_position):
		if button == 1:
			if self.window.props.visible:
				self.window.hide()
			else:
				self.window.show_all()
				self.window.show()
				if self.checkbutton_scan.get_active(): # this condition is state of check button for clipboard scan, it can be from prefdb, but this is maybe better
					if len(self.clipboard.wait_for_text().split()) == 1:
						self.entry_search.set_text(self.clipboard.wait_for_text())
	
	def onClipboard(self, clippboard, event):
		if self.window.props.visible: # first condition is check, if the window is shown
			if self.checkbutton_scan.get_active(): # second condition is state of check button for clipboard scan, it can be from prefdb, but this is maybe better
				if self.clipboard.wait_for_text() != None: # if clipboard was something else, result is None, else is text, which is converted to UTF-8
					if len(self.clipboard.wait_for_text().split()) == 1: # this condition is check, if in clipboard is just one word
						# three consecutive conditions look little bit ugly, but it make sense and it is better then logical and
						self.entry_search.set_text(self.clipboard.wait_for_text()) # text from clipboard added to search entry
						self.onSearchClicked(None) # run search method which will show results in webview
	
	def onNonEmptyText(self, *args):
		if self.entry_search.get_text():
			self.entry_search.set_icon_from_stock(Gtk.EntryIconPosition.PRIMARY, "gtk-delete")
		else:
			self.entry_search.set_icon_from_stock(Gtk.EntryIconPosition.PRIMARY, None)
	
	def onTrashPress(self, *args):
		self.entry_search.set_text("")
		
	def onWindowSizeChange(self, widget, event):
		if self.checkbutton_size.get_active():
			window_width, window_height = self.window.get_size()
			self.write_setting("window_size", [window_width, window_height])
	
	# handlers for dialogs
	def onAboutClicked(self, *args):
		self.dialog_about.run()
		self.dialog_about.hide()
		
	def onHelpClicked(self, *args):
		self.dialog_help.run()
		self.dialog_help.hide()
	
	def onSettingsClicked(self, *args):
		self.dialog_settings.run()
		self.dialog_settings.hide()	
	
	# settings handlers
	def onCheckbuttonScanToggled(self, check_button):
		self.write_setting("clipboard_scan", check_button.get_active())
		
	def onCheckbuttonSizeToggled(self, check_button):
		self.write_setting("win_size_remember", check_button.get_active())	
	
	def onComboboxLanguageChanged(self, combo):
		self.write_setting("search_language", combo.get_active_id())
		# those next two lines means, that settings of language has immediate effect on the current search (it may not be necessary or desirable)
		self.image_language.props.file = str(self.cwd_images / f"flag_{combo.get_active_id()}.svg")
		self.language = combo.get_active_id()
	
	
