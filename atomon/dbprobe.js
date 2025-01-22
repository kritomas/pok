import { statSync, existsSync } from "fs";
import sqlite3 from "sqlite3";

import { conf } from "./config.js";

if (!existsSync(conf.db.db_path))
{
	throw Error("Database not found");
}

export function DBConnection()
{
	this.fetchFirst = async (sql, params) => {
		const db = new sqlite3.Database(conf.db.db_path);
		try
		{
			return new Promise((resolve, reject) => {
				db.get(sql, params, (err, row) => {
					if (err) reject(err);
					resolve(row);
				});
			});
		}
		finally
		{
			db.close();
		}
	};

	this.totalCrawledSize = async () =>
	{
		let result = (await this.fetchFirst("select sum(original_size) as total from Site;")).total
		if (result === null)
		{
			return 0
		}
		return result;
	}
}

export function dbFileSize()
{
	return statSync(conf.db.db_path).size;
}