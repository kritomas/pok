import json, numbers

CONFIG_LOCATION = "./pok.json" # "/usr/local/etc/pok.json" TODO

with open(CONFIG_LOCATION) as file:
	conf = json.load(file)

if not "db" in conf:
	raise ValueError("Config entry db not found")
if not "user" in conf["db"]:
	raise ValueError("Config entry db.user not found")
if not "password" in conf["db"]:
	raise ValueError("Config entry db.password not found")
if not "host" in conf["db"]:
	raise ValueError("Config entry db.host not found")
if not "database" in conf["db"]:
	raise ValueError("Config entry db.database not found")

if not "crawler" in conf:
	raise ValueError("Config entry crawler not found")
if not "save_html" in conf["crawler"]:
	raise ValueError("Config entry crawler.save_html not found")
if not "agents" in conf["crawler"]:
	raise ValueError("Config entry crawler.agents not found")
if not "critical_db_size" in conf["crawler"]:
	raise ValueError("Config entry crawler.critical_db_size not found")

if not isinstance(conf["db"]["user"], str):
	raise ValueError("Config entry db.user must be a string")
if not isinstance(conf["db"]["password"], str):
	raise ValueError("Config entry db.password must be a string")
if not isinstance(conf["db"]["host"], str):
	raise ValueError("Config entry db.host must be a string")
if not isinstance(conf["db"]["database"], str):
	raise ValueError("Config entry db.database must be a string")

if not isinstance(conf["crawler"]["save_html"], bool):
	raise ValueError("Config entry crawler.save_html must be an boolean")
if not isinstance(conf["crawler"]["agents"], int):
	raise ValueError("Config entry crawler.agents must be an integer")
if not (conf["crawler"]["agents"] > 0):
	raise ValueError("Config entry crawler.agents must be greater than zero")
if not isinstance(conf["crawler"]["critical_db_size"], numbers.Number):
	raise ValueError("Config entry crawler.critical_db_size must be a number")
if not (conf["crawler"]["critical_db_size"] > 0):
	raise ValueError("Config entry crawler.critical_db_size must be greater than zero")

conf["crawler"]["critical_db_size"] = int(conf["crawler"]["critical_db_size"] * 1024 * 1024) # Convert from MB to B
print("Critical size in bytes: " + str(conf["crawler"]["critical_db_size"]))