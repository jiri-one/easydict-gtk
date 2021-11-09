# imports of TinyDB
from tinydb import TinyDB, Query, where
from tinydb.middlewares import CachingMiddleware
# import my ORJSON extension for TinyDB
from .orjson_storage import ORJSONStorage
# import to set current working directory
from pathlib import Path

# set current working directory
cwd = Path(__file__).parent
cwd_images = cwd / "images"
cfg_dir = Path.home() / ".config" / "easydict" # set user config directory
cfg_dir.mkdir(exist_ok=True) # create the config directory if not exists

# main db with eng-cze dict (name just db, but table is eng_cze and EasyDict works with that table)
db = TinyDB(cwd / "data" / "eng-cze.json", storage=CachingMiddleware(ORJSONStorage))
eng_cze = db.table('eng_cze')

# second db to store and restore program settings (name prefdb, with just _default table)
prefdb = TinyDB(cfg_dir / "settings.json", storage=ORJSONStorage)

class Settings:
	def initiate_settings(self):
		try:
			# get setting of clippboard scan from db and set it
			pref_clipboard_scan = prefdb.search(where("settings") == "clipboard_scan")[0]["value"]
			self.checkbutton_scan.props.active = pref_clipboard_scan
			# get setting of search language from db and set it
			pref_search_language = prefdb.search(where("settings") == "search_language")[0]["value"]
			self.image_language.props.file = str(self.cwd_images / f"flag_{pref_search_language}.svg")
			self.language = pref_search_language
			self.combobox_language.set_active_id(pref_search_language)
		except IndexError:
			self.create_default_settings()		

	def write_setting(self, name, value):
		prefdb.update({'value': value}, where("settings") == name)
	
	def create_default_settings(self):
		# default language settings and turn the clipboard scanning on
		prefdb.insert({'settings': 'search_language', 'value': "eng"})
		prefdb.insert({'settings': 'clipboard_scan', 'value': True})
		# after default values are set, call initiate_settings again
		self.initiate_settings()


