import sqlite3, os, multiprocessing
import config

_dblock = multiprocessing.Lock()

class DBContext:
	def __enter__(self):
		_dblock.acquire() # TODO Maybe only acquire for writes
		self.connection = sqlite3.connect(config.conf["db"]["db_path"], timeout=500)
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
		os.remove(config.conf["db"]["db_path"])
		with open(config.conf["db"]["schema_path"]) as file:
			sql = file.read()
			with DBContext() as cursor:
				cursor.executescript(sql)
	def active(self):
		with DBContext() as cursor:
			cursor.execute("select is_active from Controller;")
			row = cursor.fetchone()
			return row[0] != 0
	def activate(self):
		with DBContext() as cursor:
			cursor.execute("update Controller set is_active=1;")
	def deactivate(self):
		with DBContext() as cursor:
			cursor.execute("update Controller set is_active=0;")

class DBConnection:
	def __init__(self):
		with DBContext() as cursor:
			cursor.execute("select is_ready from Controller;")
			res = cursor.fetchone()
			if res == None:
				raise Exception("DB not properly initialized")
			if res[0] != 1:
				raise Exception("DB not properly initialized")

	def active(self):
		with DBContext() as cursor:
			cursor.execute("select is_active from Controller;")
			row = cursor.fetchone()
			return row[0] != 0

	def nextLink(self):
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

	def alreadyCrawled(self, link):
		with DBContext() as cursor:
			cursor.execute("select link from Site where link=?;", (link,))
			row = cursor.fetchone()
			return row != None
	def toBeCrawled(self, link):
		with DBContext() as cursor:
			cursor.execute("select link from Links_To_Check where link=?;", (link,))
			row = cursor.fetchone()
			return row != None
	def baseUrl(self):
		with DBContext() as cursor:
			cursor.execute("select base_url from Controller;")
			row = cursor.fetchone()
			return row[0]

	def addLink(self, link):
		with DBContext() as cursor:
			cursor.execute("begin transaction;")
			cursor.execute("select link from Links_To_Check where link=?;", (link,))
			row = cursor.fetchone()
			if row == None:
				cursor.execute("insert into Links_To_Check (link) values (?);", (link,))
			cursor.execute("commit;")
	def addLinks(self, links):
		with DBContext() as cursor:
			cursor.execute("begin transaction;")
			for link in links:
				cursor.execute("select link from Links_To_Check where link=?;", (link,))
				row = cursor.fetchone()
				if row == None:
					cursor.execute("insert into Links_To_Check (link) values (?);", (link,))
			cursor.execute("commit;")
	def addCrawl(self, link, html, object):
		with DBContext() as cursor:
			cursor.execute("begin transaction;")
			cursor.execute("select link from Site where link=?;", (link,))
			row = cursor.fetchone()
			if row == None:
				cursor.execute("insert into Site (link, original_html, original_size, title, content, creation_date, category, comment_count, photo_count) values (?, ?, ?, ?, ?, ?, ?, ?, ?);", (link, (html if config.conf["crawler"]["save_html"] else None), len(html), object["title"], object["content"], object["date"], object["category"], object["comment_count"], object["photo_count"]))
			cursor.execute("commit;")
	def addCrawlHtmlOnly(self, link, html):
		with DBContext() as cursor:
			cursor.execute("begin transaction;")
			cursor.execute("select link from Site where link=?;", (link,))
			row = cursor.fetchone()
			if row == None:
				cursor.execute("insert into Site (link, original_html, original_size) values (?, ?, ?);", (link, html, len(html)))
			cursor.execute("commit;")