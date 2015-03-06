CREATE TABLE unchecked_melody
(
id int NOT NULL AUTO_INCREMENT,
fingerprint varchar(2048),
radio varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
time_played datetime,
PRIMARY KEY (id)
);

CREATE INDEX radio_index_unchecked
ON unchecked_melody(radio);

CREATE INDEX time_played_index_unchecked
ON unchecked_melody(time_played);




