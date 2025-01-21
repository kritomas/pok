import json, numbers

CONFIG_LOCATION = "config.json"

with open(CONFIG_LOCATION) as file:
	conf = json.load(file)

if not "db" in conf:
	raise ValueError("Config entry db not found")
if not "db_path" in conf["db"]:
	raise ValueError("Config entry db.db_path not found")
if not "schema_path" in conf["db"]:
	raise ValueError("Config entry db.schema_path not found")
if not "save_html" in conf["crawler"]:
	raise ValueError("Config entry crawler.save_html not found")
if not "crawler" in conf:
	raise ValueError("Config entry crawler not found")
if not "save_html" in conf["crawler"]:
	raise ValueError("Config entry crawler.save_html not found")
if not "processes" in conf["crawler"]:
	raise ValueError("Config entry crawler.processes not found")
if not "critical_db_size" in conf["crawler"]:
	raise ValueError("Config entry crawler.critical_db_size not found")

if not isinstance(conf["db"]["db_path"], str):
	raise ValueError("Config entry db.db_path must be a string")
if not isinstance(conf["db"]["schema_path"], str):
	raise ValueError("Config entry db.schema_path must be a string")
if not isinstance(conf["crawler"]["save_html"], bool):
	raise ValueError("Config entry crawler.save_html must be an boolean")
if not isinstance(conf["crawler"]["processes"], int):
	raise ValueError("Config entry crawler.processes must be an integer")
if not (conf["crawler"]["processes"] > 0):
	raise ValueError("Config entry crawler.processes must be greater than zero")
if not isinstance(conf["crawler"]["critical_db_size"], numbers.Number):
	raise ValueError("Config entry crawler.critical_db_size must be a number")
if not (conf["crawler"]["critical_db_size"] > 0):
	raise ValueError("Config entry crawler.critical_db_size must be greater than zero")

conf["crawler"]["critical_db_size"] = int(conf["crawler"]["critical_db_size"] * 1024 * 1024) # Convert from MB to B
print("Critical size in bytes: " + str(conf["crawler"]["critical_db_size"]))