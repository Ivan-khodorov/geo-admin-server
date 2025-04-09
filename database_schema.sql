
CREATE TABLE users (
	id INTEGER NOT NULL, 
	telegram_id VARCHAR(64) NOT NULL, 
	name VARCHAR(128) NOT NULL, 
	role VARCHAR(16) NOT NULL, 
	city VARCHAR(128), 
	PRIMARY KEY (id), 
	UNIQUE (telegram_id)
)

;


CREATE TABLE city_zones (
	id INTEGER NOT NULL, 
	city_name VARCHAR(128) NOT NULL, 
	polygon_coords JSON NOT NULL, 
	created_by INTEGER NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(created_by) REFERENCES users (id)
)

;


CREATE TABLE reports (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	date DATETIME NOT NULL, 
	completed_points INTEGER NOT NULL, 
	total_points INTEGER NOT NULL, 
	notes TEXT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)

;


CREATE TABLE routes (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	date DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)

;


CREATE TABLE houses (
	id INTEGER NOT NULL, 
	city_zone_id INTEGER NOT NULL, 
	address VARCHAR(256) NOT NULL, 
	lat FLOAT NOT NULL, 
	lon FLOAT NOT NULL, 
	is_visited BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(city_zone_id) REFERENCES city_zones (id)
)

;


CREATE TABLE points (
	id INTEGER NOT NULL, 
	route_id INTEGER NOT NULL, 
	address VARCHAR(255) NOT NULL, 
	lat FLOAT NOT NULL, 
	lon FLOAT NOT NULL, 
	flyer_count INTEGER NOT NULL, 
	is_completed BOOLEAN NOT NULL, 
	completed_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(route_id) REFERENCES routes (id)
)

;


CREATE TABLE failed_attempts (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	point_id INTEGER, 
	attempt_lat FLOAT NOT NULL, 
	attempt_lon FLOAT NOT NULL, 
	distance_meters FLOAT, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(point_id) REFERENCES points (id)
)

;


CREATE TABLE point_photos (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	point_id INTEGER NOT NULL, 
	filepath VARCHAR(255) NOT NULL, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(point_id) REFERENCES points (id)
)

;


CREATE TABLE sub_points (
	id INTEGER NOT NULL, 
	point_id INTEGER NOT NULL, 
	entrance_number INTEGER NOT NULL, 
	is_completed BOOLEAN NOT NULL, 
	completed_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(point_id) REFERENCES points (id)
)

;


CREATE TABLE sub_point_photos (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	sub_point_id INTEGER NOT NULL, 
	filepath VARCHAR(255) NOT NULL, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(sub_point_id) REFERENCES sub_points (id)
)

;

