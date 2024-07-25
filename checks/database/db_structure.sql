CREATE TABLE users (
	id INTEGER NOT NULL, 
	email VARCHAR, 
	hashed_password VARCHAR, 
	is_active BOOLEAN, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE TABLE countries (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
CREATE TABLE categories (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	meta_name VARCHAR, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	UNIQUE (meta_name)
);
CREATE TABLE productions (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	quantity INTEGER, 
	year INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES categories (id)
);
CREATE TABLE sales (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	quantity INTEGER, 
	year INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES categories (id)
);
CREATE TABLE imports (
	id INTEGER NOT NULL, 
	quantity INTEGER, 
	value FLOAT, 
	year INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	country_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES categories (id), 
	FOREIGN KEY(country_id) REFERENCES countries (id)
);
CREATE TABLE exports (
	id INTEGER NOT NULL, 
	quantity INTEGER, 
	value FLOAT, 
	year INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	country_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES categories (id), 
	FOREIGN KEY(country_id) REFERENCES countries (id)
);
CREATE TABLE processing (
	id INTEGER NOT NULL, 
	cultivation VARCHAR NOT NULL, 
	year INTEGER NOT NULL, 
	quantity INTEGER, 
	grape_class_id INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(grape_class_id) REFERENCES categories (id), 
	FOREIGN KEY(category_id) REFERENCES categories (id)
);
