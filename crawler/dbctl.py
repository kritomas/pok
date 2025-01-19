import sqlite3, os

DB_PATH = "pok.db"
DB_INIT_PATH = "database/init.sql"

class DBContext:
	def __enter__(self):
		self.connection = sqlite3.connect(DB_PATH)
		self.connection.execute("PRAGMA journal_mode=WAL;")
		self.cursor = self.connection.cursor()
		return self.cursor
	def __exit__(self, exc_type, exc_value, traceback):
		self.connection.commit()
		self.connection.close()

class DBController:
	"""
	Make sure to only ever instantiate this in a subprocess, transactions may otherwise not work concurrently.
	"""
	def __init__(self):
		try:
			with DBContext() as cursor:
				cursor.execute("select is_ready from Controller")
				res = cursor.fetchone()
				if res == None:
					raise Exception("DB not properly initialized")
				if res[0] != 1:
					raise Exception("DB not properly initialized")
		except:
			self._reset()
	def _reset(self):
		"""
		Resets the database. THIS WILL WIPE ALL DATA.
		"""
		os.remove(DB_PATH)
		with open(DB_INIT_PATH) as file:
			sql = file.read()
			with DBContext() as cursor:
				cursor.executescript(sql)

class DBConnection:
	"""
	Make sure to only ever instantiate this in a subprocess, transactions may otherwise not work concurrently.
	"""
	def __init__(self):
		with DBContext() as cursor:
			cursor.execute("select is_ready from Controller")
			res = cursor.fetchone()
			if res == None:
				raise Exception("DB not properly initialized")
			if res[0] != 1:
				raise Exception("DB not properly initialized")

	def nextURL(self):
		with DBContext() as cursor:
			pass