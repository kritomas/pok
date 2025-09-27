# Pok

A webcrawler for www.idnes.cz.

# Installation

This project is made up of three parts: the crawler itself, and two monitors.

## Pok Crawler

1.	Install dependencies: `python3`

2.	Install python modules: `requests`, `lxml`, `pygresql`

	**Note:** The modules have to be installed globally. If you want to use a venv, you'll have to modify the running script (`pok-crawler/start-crawler.sh`).

3.	Ensure that `pok-crawler/start-crawler.sh` is executable.

4.	Copy all of `pok-crawler` into `/var/pok`.

5.	Copy `pok-crawler.service` into `/etc/systemd/system`.

## Pok Atom Feed Monitor

Broken on the PostgreSQL version.

## Pok Realtime Monitor

1.	Install dependencies: `python3`

2.	Install python modules: `pygresql`

	**Note:** The modules have to be installed globally. If you want to use a venv, you'll have to modify the shebang in `pok-rtmon/pok-rtmon`.

3.	Ensure that `pok-rtmon/pok-rtmon` is executable.

4.	Copy `pok-rtmon/pok-rtmon` into `/usr/local/sbin`.

5.	Change ownership: `chown root:root /usr/local/sbin/pok-rtmon`.

6.	Change permissions: `chmod u=rwx,g=rx,o=rx /usr/local/sbin/pok-rtmon`.

7.	Create a new user with the shell set to `/usr/local/sbin/pok-rtmon`.

## Database

Create a PostgreSQL database and invoke `database/init.sql`.

# Configuration

Create `/usr/local/etc/pok.json` with the following format:

```json
{
	"db": {
		"user": "[DB user]",
		"password": "[DB password]",
		"host": "[DB server address (optionally with port)]",
		"database": "[DB name]"
	},
	"crawler": {
		"save_html": "[Whether to store the original HTML (true) or not (false)]",
		"agents": "[Amount of agents]",
		"critical_db_size": "[The size of the DB file in MB, at which the crawler will stop]",
		"db_size_milestone": "[The size of the DB file in MB, at which the monitors make an annoucement]",
		"crawl_milestone": "[The amount of HTML in MB to crawl, at which the monitors make an announcement]"
	}
}
```

# Usage

## Pok Crawler

Start crawler systemd service: `systemctl start pok-crawler`.

This will create the database and begin crawling.

Make sure you start this before the monitors.

## Pok Atom Feed Monitor

Broken on the PostgreSQL version.

## Pok Realtime Monitor

Login to the user you created for this monitor.

Ideally, allow SSH login as well.