CREATE TABLE melody
(
id int NOT NULL AUTO_INCREMENT,
track_id varchar(255) unique,
artist varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
song varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
filename varchar(2048) CHARACTER SET utf8 COLLATE utf8_general_ci, 
PRIMARY KEY (id)
); 

CREATE INDEX artist_index
ON melody(artist);

CREATE INDEX song_index
ON melody(song);


CREATE TABLE played_melody
(
id int NOT NULL AUTO_INCREMENT,
track_id varchar(255),
radio varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
date_played date,
time_played time,
PRIMARY KEY (id)
);

CREATE INDEX radio_index
ON played_melody(radio);

CREATE INDEX time_played_index
ON played_melody(time_played);

CREATE INDEX date_played_index
ON played_melody(date_played);

CREATE INDEX track_id_index
ON played_melody(track_id);


CREATE TABLE artist
(
id int NOT NULL AUTO_INCREMENT,
name varchar(2048) CHARACTER SET utf8 COLLATE utf8_general_ci,
gender char(1),
birthdate date,
active boolean,
phonenumber varchar(20),
PRIMARY KEY (id)
);

create TABLE fingerprint
(
id int NOT NULL AUTO_INCREMENT,
fp varchar(32000),
radio varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
date_played date,
time_played time,
time_identified datetime,
status char(1),
PRIMARY KEY (id)
);

CREATE INDEX fp_radio_index
ON fingerprint(radio);

CREATE INDEX fp_time_played_index
ON fingerprint(time_played);

CREATE INDEX fp_date_played_index
ON fingerprint(date_played);

CREATE TABLE artist_melody
(
id int NOT NULL AUTO_INCREMENT,
artist_id int REFERENCES artist(id),
melody_id int REFERENCES melody(id),
PRIMARY KEY (id)
);

