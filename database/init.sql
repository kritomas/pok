-- This is a crawling schema for sqlite.

PRAGMA encoding = 'UTF-8';
PRAGMA journal_mode = WAL;

begin transaction;

create table Links_To_Check
(
	id integer primary key,
	link text unique not null
) strict;

create unique index Links_To_Check_Index on Links_To_Check(link);

create table Site
(
	id integer primary key,
	link text unique not null,
	original_size int not null check(original_size >= 0),
	title text not null,
	content text not null,
	creation_date text,
	category text,
	comment_count int check(comment_count >= 0),
	photo_count int check(photo_count >= 0),
	original_html text
) strict;

create unique index Links_Site_Index on Site(link);

create table Controller -- Used to control agents
(
	id integer primary key,
	is_active integer not null default 0,
	is_ready integer not null default 0,
	base_url text not null default 'https://www.idnes.cz/'
) strict;

insert into Controller default values;
update Controller set is_ready = 1;

commit;