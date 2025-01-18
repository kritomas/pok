-- This is a crawling schema for sqlite.

begin transaction;

create table Links_To_Check
(
	id integer primary key,
	link text not null
) strict;

create table Site
(
	id integer primary key,
	link text not null,
	--title text not null,
	--category text not null,
	--comment_count int not null check(comment_count > 0),
	--photo_count int not null check(photo_count > 0),
	--contents text not null,
	--creation_date text not null,
	original_html text
) strict;

create table Controller -- Used to control agents
(
	id integer primary key,
	is_active integer not null default 0,
	is_ready integer not null default 0
) strict;

insert into Controller default values;
update Controller set is_ready = 1;

commit;