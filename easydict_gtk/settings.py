# imports of TinyDB
from tinydb import TinyDB, Query, where
from tinydb.middlewares import CachingMiddleware
# import my ORJSON extension for TinyDB
from easydict_gtk.orjson_storage import ORJSONStorage
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
query = Query()

class Settings:
	def initiate_settings(self):
		try:
			# get setting of clippboard scan from db and set it
			pref_clipboard_scan = prefdb.search(query["settings"] == "clipboard_scan")[0]["value"]
			self.checkbutton_scan.props.active = pref_clipboard_scan
			# get setting of window size remembering from db and set it
			pref_win_size_remember = prefdb.search(query["settings"] == "win_size_remember")[0]["value"]
			self.checkbutton_size.props.active = pref_win_size_remember
			# get the window size from db and set it
			window_width, window_height = prefdb.search(query["settings"] == "window_size")[0]["value"]
			self.window.set_default_size(window_width, window_height)			
			# get setting of search language from db and set it
			pref_search_language = prefdb.search(query["settings"] == "search_language")[0]["value"]
			self.image_language.props.file = str(self.cwd_images / f"flag_{pref_search_language}.svg")
			self.language = pref_search_language
			self.combobox_language.set_active_id(pref_search_language)
		except IndexError:
			self.create_default_settings()
		# set the version from poetry pyproject.toml file
		self.dialog_about.props.version = self.extract_version_from_toml()

	def write_setting(self, name, value):
		prefdb.update({'value': value}, where("settings") == name)
	
	def create_default_settings(self):
		# set default settings
		prefdb.upsert({'settings': 'search_language', 'value': "eng"}, query["settings"] == "search_language")
		prefdb.upsert({'settings': 'clipboard_scan', 'value': True}, query["settings"] == "clipboard_scan")
		prefdb.upsert({'settings': 'window_size', 'value': [360,640]}, query["settings"] == "window_size")
		prefdb.upsert({'settings': 'win_size_remember', 'value': True}, query["settings"] == "win_size_remember")
		# after default values are set, call initiate_settings again
		self.initiate_settings()
	
	def extract_version_from_toml(self):
		"""Extract version from pyproject.toml file (poetry settings file)"""
		toml_path = cwd.parent / 'pyproject.toml'
		result = None
		if toml_path.is_file():
			with open(str(toml_path), "r") as f:
				while result == None:
					string=f.readline()
					if 'version = ' in string:
						result = string.split('"')[1]
		return result
	



