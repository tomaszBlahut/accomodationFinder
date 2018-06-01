create schema pite;

create table pite.shop (
	id SERIAL PRIMARY KEY,
	name VARCHAR(20),
	city VARCHAR(40),
	latitude REAL,
	longitude REAL
);

create table pite.finding_results (
  id VARCHAR PRIMARY KEY,
  request_params VARCHAR(512),
  status INTEGER,
  result VARCHAR,
  created_date TIMESTAMP,
  updated_date TIMESTAMP
);