import pgdb, os
import config

class DBController:
	def __init__(self):
		self.conn = pgdb.connect(user=config.conf["db"]["user"], password=config.conf["db"]["password"], host=config.conf["db"]["host"], database=config.conf["db"]["database"])

		with self.conn.cursor() as cursor:
			cursor.execute("select is_ready from Controller;")
			res = cursor.fetchone()
			if res == None:
				raise Exception("DB not properly initialized")
			if res[0] != 1:
				raise Exception("DB not properly initialized")

	def active(self):
		with self.conn.cursor() as cursor:
			cursor.execute("select is_active from Controller;")
			row = cursor.fetchone()
			return row[0] != 0
	def activate(self):
		with self.conn.cursor() as cursor:
			cursor.execute("update Controller set is_active=true;")
			self.conn.commit()
	def deactivate(self):
		with self.conn.cursor() as cursor:
			cursor.execute("update Controller set is_active=false;")
			self.conn.commit()
	def size(self):
		with self.conn.cursor() as cursor:
			cursor.execute("select pg_database_size('pok');")
			row = cursor.fetchone()
			return row[0]

class DBConnection:
	def __init__(self):
		self.conn = pgdb.connect(user=config.conf["db"]["user"], password=config.conf["db"]["password"], host=config.conf["db"]["host"], database=config.conf["db"]["database"])

		with self.conn.cursor() as cursor:
			cursor.execute("select is_ready from Controller;")
			res = cursor.fetchone()
			if res == None:
				raise Exception("DB not properly initialized")
			if res[0] != 1:
				raise Exception("DB not properly initialized")

	def active(self):
		with self.conn.cursor() as cursor:
			cursor.execute("select is_active from Controller;")
			row = cursor.fetchone()
			return row[0] != 0

	def nextLink(self):
		with self.conn.cursor() as cursor:
			cursor.execute("start transaction;")
			cursor.execute("select id, link from Links_To_Check order by id asc limit 1;")
			row = cursor.fetchone()
			if row != None:
				cursor.execute("delete from Links_To_Check where id=%s;", (row[0],))
			cursor.execute("commit;")
			if row == None:
				return None
			return row[1]

	def alreadyCrawled(self, link):
		with self.conn.cursor() as cursor:
			cursor.execute("select link from Site where link=%s;", (link,))
			row = cursor.fetchone()
			return row != None
	def toBeCrawled(self, link):
		with self.conn.cursor() as cursor:
			cursor.execute("select link from Links_To_Check where link=%s;", (link,))
			row = cursor.fetchone()
			return row != None
	def baseUrl(self):
		with self.conn.cursor() as cursor:
			cursor.execute("select base_url from Controller;")
			row = cursor.fetchone()
			return row[0]

	def addLink(self, link):
		with self.conn.cursor() as cursor:
			cursor.execute("start transaction;")
			cursor.execute("select link from Links_To_Check where link=%s;", (link,))
			row = cursor.fetchone()
			if row == None:
				cursor.execute("insert into Links_To_Check (link) values (%s);", (link,))
			cursor.execute("commit;")
	def addLinks(self, links):
		with self.conn.cursor() as cursor:
			cursor.execute("start transaction;")
			for link in links:
				cursor.execute("select link from Links_To_Check where link=%s;", (link,))
				row = cursor.fetchone()
				if row == None:
					cursor.execute("insert into Links_To_Check (link) values (%s);", (link,))
			cursor.execute("commit;")
	def addCrawl(self, link, html, object):
		with self.conn.cursor() as cursor:
			cursor.execute("start transaction;")
			cursor.execute("select link from Site where link=%s;", (link,))
			row = cursor.fetchone()
			if row == None:
				cursor.execute("insert into Site (link, original_html, original_size, title, content, creation_date, category, comment_count, photo_count) values (%s, %s, %s, %s, %s, %s, %s, %s, %s);", (link, (html if config.conf["crawler"]["save_html"] else None), len(html), object["title"], object["content"], object["date"], object["category"], object["comment_count"], object["photo_count"]))
			cursor.execute("commit;")
	def addCrawlHtmlOnly(self, link, html):
		with self.conn.cursor() as cursor:
			cursor.execute("start transaction;")
			cursor.execute("select link from Site where link=%s;", (link,))
			row = cursor.fetchone()
			if row == None:
				cursor.execute("insert into Site (link, original_html, original_size) values (%s, %s, %s);", (link, html, len(html)))
			cursor.execute("commit;")