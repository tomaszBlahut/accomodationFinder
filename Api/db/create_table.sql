create schema pite;

create table pite.shop (
	id SERIAL PRIMARY KEY,
	name VARCHAR(20),
	city VARCHAR(40),
	latitude REAL,
	longitude REAL
); 