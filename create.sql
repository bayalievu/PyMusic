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
time_played datetime,
PRIMARY KEY (id)
);

CREATE INDEX radio_index
ON played_melody(radio);

CREATE INDEX time_played_index
ON played_melody(time_played);

CREATE INDEX track_id_index
ON played_melody(track_id);


CREATE TABLE artist
(
id int NOT NULL AUTO_INCREMENT,
name varchar(2048) CHARACTER SET utf8 COLLATE utf8_general_ci,
PRIMARY KEY (id)
);

