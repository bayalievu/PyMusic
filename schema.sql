-- MySQL dump 10.13  Distrib 5.5.41, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: pymusic
-- ------------------------------------------------------
-- Server version	5.5.41-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `approved_songs`
--

DROP TABLE IF EXISTS `approved_songs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `approved_songs` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `singer_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `song_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `akyn` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `composer` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `arranger` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `producer` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `year` int(5) NOT NULL,
  `genre` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `filename` varchar(2048) COLLATE utf8_unicode_ci NOT NULL,
  `uploaded_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `approve_flag` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `artist`
--

DROP TABLE IF EXISTS `artist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `artist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(2048) CHARACTER SET utf8 DEFAULT NULL,
  `gender` char(1) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `phonenumber` varchar(20) DEFAULT NULL,
  `is_singer` tinyint(1) DEFAULT '1',
  `is_compositor` tinyint(1) DEFAULT '0',
  `is_editor` tinyint(1) DEFAULT '0',
  `is_arranger` tinyint(1) DEFAULT '0',
  `is_producer` tinyint(1) DEFAULT '0',
  `photo_url` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `artist_name` (`name`(255))
) ENGINE=InnoDB AUTO_INCREMENT=852 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `artist_melody`
--

DROP TABLE IF EXISTS `artist_melody`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `artist_melody` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `artist_id` int(11) DEFAULT NULL,
  `melody_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6133 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fingerprint`
--

DROP TABLE IF EXISTS `fingerprint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fingerprint` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fp` varchar(32000) DEFAULT NULL,
  `radio` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `date_played` date DEFAULT NULL,
  `time_played` time DEFAULT NULL,
  `time_identified` datetime DEFAULT NULL,
  `status` char(1) DEFAULT NULL,
  `radio_id` int(11) DEFAULT NULL,
  `track_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fp_radio_index` (`radio`),
  KEY `fp_time_played_index` (`time_played`),
  KEY `fp_date_played_index` (`date_played`),
  KEY `fp_radio_id_index` (`radio_id`),
  KEY `fp_track_id_index` (`track_id`)
) ENGINE=InnoDB AUTO_INCREMENT=496026 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `genre`
--

DROP TABLE IF EXISTS `genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `genre` (
  `id` int(6) NOT NULL DEFAULT '12',
  `name` varchar(250) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `logcompare`
--

DROP TABLE IF EXISTS `logcompare`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logcompare` (
  `log_id` int(50) NOT NULL AUTO_INCREMENT,
  `date_view` varchar(255) NOT NULL,
  `time_view` varchar(255) NOT NULL,
  `userid` int(11) DEFAULT NULL,
  `singer1` int(11) DEFAULT NULL,
  `singer2` int(11) DEFAULT NULL,
  `username` varchar(25) DEFAULT NULL,
  `singername1` varchar(25) DEFAULT NULL,
  `singername2` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=630 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs` (
  `log_id` int(50) NOT NULL AUTO_INCREMENT,
  `remote_addr` varchar(255) NOT NULL,
  `request_uri` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `date_view` varchar(255) NOT NULL,
  `time_view` varchar(255) NOT NULL,
  `userid` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1627 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `melody`
--

DROP TABLE IF EXISTS `melody`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `melody` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `track_id` varchar(255) DEFAULT NULL,
  `artist` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `song` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `filename` varchar(2048) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `track_id` (`track_id`),
  KEY `artist_index` (`artist`),
  KEY `song_index` (`song`)
) ENGINE=InnoDB AUTO_INCREMENT=5736 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `played_melody`
--

DROP TABLE IF EXISTS `played_melody`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `played_melody` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `track_id` varchar(255) DEFAULT NULL,
  `radio` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `date_played` date DEFAULT NULL,
  `time_played` time DEFAULT NULL,
  `radio_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `radio_index` (`radio`),
  KEY `time_played_index` (`time_played`),
  KEY `date_played_index` (`date_played`),
  KEY `track_id_index` (`track_id`),
  KEY `radio_id` (`radio_id`)
) ENGINE=InnoDB AUTO_INCREMENT=40618 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `radio`
--

DROP TABLE IF EXISTS `radio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `logo` varchar(225) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `uploaded_artist_melody`
--

DROP TABLE IF EXISTS `uploaded_artist_melody`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `uploaded_artist_melody` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `artist_id` int(10) NOT NULL,
  `melody_id` int(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `artist_id` (`artist_id`),
  KEY `melody_id` (`melody_id`),
  CONSTRAINT `uploaded_artist_melody_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `artist` (`id`),
  CONSTRAINT `uploaded_artist_melody_ibfk_2` FOREIGN KEY (`melody_id`) REFERENCES `melody` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=312 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `uploaded_song`
--

DROP TABLE IF EXISTS `uploaded_song`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `uploaded_song` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `singer_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `song_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `akyn` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `composer` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `arranger` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `producer` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `year` int(5) DEFAULT NULL,
  `genre` int(7) DEFAULT NULL,
  `filename` varchar(2048) COLLATE utf8_unicode_ci NOT NULL,
  `uploaded_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `approved_flag` tinyint(1) DEFAULT '0',
  `melody_added_flag` tinyint(1) DEFAULT '0',
  `melody_declined_flag` tinyint(1) DEFAULT '0',
  `melody_declined_error` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `track_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `genre` (`genre`),
  CONSTRAINT `uploaded_song_ibfk_1` FOREIGN KEY (`genre`) REFERENCES `genre` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=425 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_tie`
--

DROP TABLE IF EXISTS `user_tie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_tie` (
  `user_id` int(11) DEFAULT NULL,
  `singer_id` int(11) DEFAULT NULL,
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  `is_always` tinyint(1) DEFAULT '0',
  `radio` int(25) NOT NULL,
  KEY `user_id` (`user_id`),
  KEY `singer_id` (`singer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `user_type` int(5) NOT NULL,
  `status` int(5) NOT NULL,
  `full_name` varchar(225) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `p` varchar(10) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=168 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-05-13 17:31:32
