-- This is a crawling schema for sqlite.

PRAGMA encoding = 'UTF-8';
PRAGMA journal_mode = WAL;

begin transaction;

create table Links_To_Check
(
	id integer primary key,
	link text unique not null
) strict;

create table Site
(
	id integer primary key,
	link text unique not null,
	original_size int not null check(original_size >= 0),
	title text not null,
	--category text,
	content text not null,
	creation_date text,
	comment_count int check(comment_count >= 0),
	photo_count int check(photo_count >= 0),
	original_html text
) strict;

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