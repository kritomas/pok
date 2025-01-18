import sqlite3, os

DB_PATH = "pok.db"
DB_INIT_PATH = "database/init.sql"

class DBConnection:
	def __init__(self):
		self.connection = sqlite3.connect(DB_PATH)
		self.conn_cursor = self.connection.cursor()
		try:
			self.conn_cursor.execute("select is_ready from Controller")
			res = self.conn_cursor.fetchone()
			if res == None:
				raise Exception("DB not properly initialized")
			if res[0] != 1:
				raise Exception("DB not properly initialized")
		except:
			self._reset()
			with open(DB_INIT_PATH) as file:
				sql = file.read()
				self.conn_cursor.executescript(sql)
	def _reset(self):
		"""
		Resets the database. THIS WILL WIPE ALL DATA.
		"""
		self.connection.close()
		os.remove(DB_PATH)
		self.connection = sqlite3.connect(DB_PATH)
		self.conn_cursor = self.connection.cursor()
