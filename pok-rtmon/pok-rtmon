#!/usr/bin/python3

# This python script serves as a realtime monitor for pok.

import os, json, numbers, time, sys
import sqlite3

os.system("")

CONFIG_LOCATION = "config.json"

with open(CONFIG_LOCATION) as file:
	conf = json.load(file)

if not "db" in conf:
	raise ValueError("Config entry db not found")
if not "db_path" in conf["db"]:
	raise ValueError("Config entry db.db_path not found")
if not "crawler" in conf:
	raise ValueError("Config entry crawler not found")
if not "critical_db_size" in conf["crawler"]:
	raise ValueError("Config entry crawler.critical_db_size not found")
if not "crawl_milestone" in conf["crawler"]:
	raise ValueError("Config entry crawler.crawl_milestone not found")

if not isinstance(conf["db"]["db_path"], str):
	raise ValueError("Config entry db.db_path must be a string")
if not isinstance(conf["crawler"]["critical_db_size"], numbers.Number):
	raise ValueError("Config entry crawler.critical_db_size must be a number")
if not (conf["crawler"]["critical_db_size"] > 0):
	raise ValueError("Config entry crawler.critical_db_size must be greater than zero")
if not (conf["crawler"]["crawl_milestone"] > 0):
	raise ValueError("Config entry crawler.crawl_milestone must be greater than zero")

conf["crawler"]["db_size_milestone"] = int(conf["crawler"]["db_size_milestone"] * 1024 * 1024) # Convert from MB to B
conf["crawler"]["critical_db_size"] = int(conf["crawler"]["critical_db_size"] * 1024 * 1024) # Convert from MB to B
conf["crawler"]["crawl_milestone"] = int(conf["crawler"]["crawl_milestone"] * 1024 * 1024) # Convert from MB to B


class DBContext:
	def __enter__(self):
		self.connection = sqlite3.connect(conf["db"]["db_path"], timeout=500)
		self.cursor = self.connection.cursor()
		return self.cursor
	def __exit__(self, exc_type, exc_value, traceback):
		self.connection.commit()
		self.connection.close()

class DBConnection:
	def totalCrawledSize(self):
		with DBContext() as cursor:
			cursor.execute("select sum(original_size) as total from Site;")
			row = cursor.fetchone()
			if row[0] == None:
				return 0
			return row[0]

dbcon = DBConnection()

def bToMb(b):
	return "{:.2f}".format(b / (1024 * 1024)) + "MB"

def main():
	print("Pok Realtime Monitor\n")
	try:
		dbFileSize = os.path.getsize(conf["db"]["db_path"])
		do = True
		while do or dbFileSize < conf["crawler"]["critical_db_size"]:
			do = False
			totalCrawled = dbcon.totalCrawledSize()
			dbFileSize = os.path.getsize(conf["db"]["db_path"])

			print("\33[0m\r\33[J", end="")

			print("\33[37m", end="")
			fraction = totalCrawled / conf["crawler"]["crawl_milestone"]
			print("Crawl milestone: ", end="")
			if fraction >= 1:
				print("\33[32m", end="")
			print(bToMb(totalCrawled) + " (" + str(int(fraction * 100)) + "%)")

			print("\33[37m", end="")
			fraction = dbFileSize / conf["crawler"]["db_size_milestone"]
			print("DB file milestone: ", end="")
			if fraction >= 1:
				print("\33[32m", end="")
			print(bToMb(dbFileSize) + " (" + str(int(fraction * 100)) + "%)")

			print("\33[37m", end="")
			print()
			fraction = dbFileSize / conf["crawler"]["critical_db_size"]
			print("DB file critical limit: ", end="")
			if fraction >= 1:
				print("\33[32m", end="")
			print(bToMb(dbFileSize) + " (" + str(int(fraction * 100)) + "%)")

			sys.stdout.flush()
			if dbFileSize < conf["crawler"]["critical_db_size"]:
				time.sleep(3)
				print("\33[4A", end="")
		print()
		print("\33[32mCritical target reached ;)")
		print("\33[0m", end="")
		while True:
			time.sleep(5)
	except KeyboardInterrupt:
		pass
	except FileNotFoundError:
		print("\33[31mERROR: Database not found")
		print("\33[0m", end="")
		try:
			while True:
				time.sleep(5)
		except KeyboardInterrupt:
			pass
	print("\33[0mExiting Pok Realtime Monitor")

main()