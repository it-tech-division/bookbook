create database hyundai_book;

use hyundai_book;

create table book_info (
	book_no INT(11) unsigned NOT NULL AUTO_INCREMENT,
	title VARCHAR(100),
	isbn VARCHAR(30),
	author VARCHAR(50),
	description VARCHAR(500),
	image VARCHAR(100),
	link VARCHAR(100),
	register VARCHAR(50),
	register_email VARCHAR(50),
	register_date DATE,
	created_date DATE,
	avalability VARCHAR(10),
	primary key(book_no)
	);

create table book_log (
	no INT(11) unsigned NOT NULL,
	borrower VARCHAR(50),
	borrower_email varchar(50),
	borrow_date DATE NOT NULL,
	return_date DATE,
	message varchar(500)
	);
	
alter table book_info convert to character set utf8;
alter table book_log convert to character set utf8;




	
