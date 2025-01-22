import express from "express";
import http from "http";

import { conf } from "./config.js"
import { DBConnection, dbFileSize } from "./dbprobe.js"
import { addAutomatedEntry } from "./feed.js"

const PORT = 8080;

const app = express();
const server = http.createServer(app);

app.use(express.static("./atomon/dist"));

const db = new DBConnection();

function bToMb(b)
{
	return (b / (1024 * 1024)).toFixed(2) + "MB"
}

server.listen(PORT, async () =>
{
	let thresholds = new Map();
	thresholds.set("crawl_milestone", await db.totalCrawledSize() / conf.crawler.crawl_milestone >= 1); // DONT USE []
	thresholds.set("db_size_milestone", dbFileSize() / conf.crawler.db_size_milestone >= 1);
	thresholds.set("critical_db_size", dbFileSize() / conf.crawler.critical_db_size >= 1);
	setInterval(async () =>
	{
		let thresholds_old = new Map(thresholds); // DONT USE []
		thresholds.set("crawl_milestone", await db.totalCrawledSize() / conf.crawler.crawl_milestone >= 1);
		thresholds.set("db_size_milestone", dbFileSize() / conf.crawler.db_size_milestone >= 1);
		thresholds.set("critical_db_size", dbFileSize() / conf.crawler.critical_db_size >= 1);

		if (thresholds.get("crawl_milestone") && !thresholds_old.get("crawl_milestone"))
		{
			addAutomatedEntry("Crawl milestone reached", "Pok has reached the specified milestone of " + bToMb(conf.crawler.crawl_milestone) + " articles crawled.");
		}
		if (thresholds.get("db_size_milestone") && !thresholds_old.get("db_size_milestone"))
		{
			addAutomatedEntry("Database milestone reached", "Pok's database has reached the specified milestone of " + bToMb(conf.crawler.db_size_milestone) + " total in size.");
		}
		if (thresholds.get("critical_db_size") && !thresholds_old.get("critical_db_size"))
		{
			addAutomatedEntry("Critical database size", "Pok's database has reached the specified critical size of " + bToMb(conf.crawler.critical_db_size) + " total in size, Pok terminating.");
		}
	}, 5000);

	console.log("Pok Atom Feed Monitor listening at " + PORT);
});