import express from "express";
import http from "http";

import { conf } from "./config.js"
import { DBConnection } from "./dbprobe.js"
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
	setInterval(async () =>
	{
		let thresholds_old = new Map(thresholds); // DONT USE []
		thresholds.set("crawl_milestone", await db.totalCrawledSize() / conf.crawler.crawl_milestone >= 1);

		if (thresholds.get("crawl_milestone") && !thresholds_old.get("crawl_milestone"))
		{
			addAutomatedEntry("Crawl milestone reached", "Pok has reached the specified milestone of " + bToMb(conf.crawler.crawl_milestone) + " articles crawled");
		}
	}, 5000);

	console.log("Pok Atom Feed Monitor listening at " + PORT);
});