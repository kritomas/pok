import sqlite3, os, multiprocessing

DB_PATH = "pok.db"
DB_INIT_PATH = "database/init.sql"

_dblock = multiprocessing.Lock()

class DBContext:
	def __enter__(self):
		_dblock.acquire() # TODO Maybe only acquire for writes
		self.connection = sqlite3.connect(DB_PATH, timeout=500)
		self.cursor = self.connection.cursor()
		return self.cursor
	def __exit__(self, exc_type, exc_value, traceback):
		self.connection.commit()
		self.connection.close()
		_dblock.release()

class DBController:
	def __init__(self):
		try:
			with DBContext() as cursor:
				cursor.execute("select is_ready from Controller;")
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
	def __init__(self):
		with DBContext() as cursor:
			cursor.execute("select is_ready from Controller;")
			res = cursor.fetchone()
			if res == None:
				raise Exception("DB not properly initialized")
			if res[0] != 1:
				raise Exception("DB not properly initialized")

	def nextURL(self):
		with DBContext() as cursor:
			cursor.execute("begin transaction;")
			cursor.execute("select id, link from Links_To_Check order by id asc limit 1;")
			row = cursor.fetchone()
			if row != None:
				cursor.execute("delete from Links_To_Check where id=?;", (row[0],))
			cursor.execute("commit;")
			if row == None:
				return None
			return row[1]