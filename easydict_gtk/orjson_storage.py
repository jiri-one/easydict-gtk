import orjson
from tinydb import Storage

class ORJSONStorage(Storage):
	"""This is Storage only for EasyDict, I don't testet it for other purposes."""
	def __init__(self, filename):
		self.filename = filename
		print(filename)

	def read(self):
		try:
			with open(self.filename, "rb") as handle:
				try:
					data = orjson.loads(handle.read())
					return data
				except orjson.JSONDecodeError:
					return None
		except FileNotFoundError:
			with open(self.filename, 'a'):
				pass

	def write(self, data):
		try:
			with open(self.filename, "wb") as handle:
				handle.write(orjson.dumps(data))
		except orjson.JSONEncodeError:
			return None		

	def close(self):
		pass
