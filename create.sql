CREATE TABLE melody
(
id int NOT NULL AUTO_INCREMENT,
track_id varchar(255) unique,
artist varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
song varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
PRIMARY KEY (id)
); 

CREATE INDEX artist_index
ON melody(artist);

CREATE INDEX song_index
ON melody(song);

