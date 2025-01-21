import sqlite3 from "sqlite3";

import { conf } from "./config.js";

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
		return (await this.fetchFirst("select sum(original_size) as total from Site;")).total;
	}
}