# imports of TinyDB
from tinydb import TinyDB, Query, where
from tinydb.middlewares import CachingMiddleware
# import my ORJSON extension for TinyDB
from orjson_storage import ORJSONStorage
# import to set current working directory
from os import getcwd

# set current working directory
cwd = getcwd() + "/"
cwd_images = cwd + "images/"

# main db with eng-cze dict (name just db, but table is eng_cze and EasyDict works with that table)
db = TinyDB(f'{cwd}eng-cze.json', storage=CachingMiddleware(ORJSONStorage))
eng_cze = db.table('eng_cze')

# second db to restore program settings (name prefdb, with just _default table)
prefdb = TinyDB(f'{cwd}settings.json', storage=ORJSONStorage)

class Settings:
	def initiate_settings(self):
		# get setting of clippboard scan from db and set it
		pref_clipboard_scan = prefdb.search(where("settings") == "clipboard_scan")[0]["value"]
		self.checkbutton_scan.props.active = pref_clipboard_scan
		# get setting of search language from db and set it
		pref_search_language = prefdb.search(where("settings") == "search_language")[0]["value"]
		self.image_language.props.file = self.cwd_images + f"flag_{pref_search_language}.svg"
		self.language = pref_search_language
		self.combobox_language.set_active_id(pref_search_language)

	def write_setting(self, name, value):
		prefdb.update({'value': value}, where("settings") == name)

