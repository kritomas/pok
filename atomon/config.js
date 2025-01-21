import { readFileSync } from 'fs';

const CONFIG_LOCATION = "config.json"

export const conf = JSON.parse(readFileSync(CONFIG_LOCATION))
if (conf.db == undefined)
{
	throw new Error("Config entry db not found");
}
if (conf.db.db_path == undefined)
{
	throw new Error("Config entry db.db_path not found");
}
if (conf.crawler.critical_db_size == undefined)
{
	throw new Error("Config entry crawler.critical_db_size not found");
}
if (conf.crawler.db_size_milestone == undefined)
{
	throw new Error("Config entry crawler.db_size_milestone not found");
}
if (conf.crawler.crawl_milestone == undefined)
{
	throw new Error("Config entry crawler.crawl_milestone not found");
}

if (typeof(conf.db.db_path) !== "string")
{
	throw new Error("Config entry db.db_path must be a string");
}
if (typeof(conf.crawler.critical_db_size) !== "number")
{
	throw new Error("Config entry crawler.critical_db_size must be a number");
}
if (typeof(conf.crawler.db_size_milestone) !== "number")
{
	throw new Error("Config entry crawler.db_size_milestone must be a number");
}
if (typeof(conf.crawler.crawl_milestone) !== "number")
{
	throw new Error("Config entry crawler.crawl_milestone must be a number");
}

if (conf.crawler.critical_db_size <= 0)
{
	throw new Error("Config entry crawler.critical_db_size must be positive");
}
if (conf.crawler.db_size_milestone <= 0)
{
	throw new Error("Config entry crawler.db_size_milestone must be positive");
}
if (conf.crawler.crawl_milestone <= 0)
{
	throw new Error("Config entry crawler.crawl_milestone must be positive");
}

conf.crawler.crawl_milestone = Math.round(conf.crawler.critical_db_size * 1024 * 1024)