-- MySQL dump 10.13  Distrib 8.0.26, for Linux (x86_64)
--
-- Host: localhost    Database: sac_elec
-- ------------------------------------------------------
-- Server version	8.0.26-0ubuntu0.20.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CANDIDATES`
--

DROP TABLE IF EXISTS `CANDIDATES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CANDIDATES` (
  `NAME` varchar(100) NOT NULL,
  `DEPT` varchar(100) NOT NULL,
  `POSITION` varchar(100) NOT NULL,
  `PROG` varchar(50) NOT NULL,
  `ROLLNO` varchar(10) NOT NULL,
  `VOTES` int DEFAULT '0',
  PRIMARY KEY (`ROLLNO`),
  UNIQUE KEY `NAME` (`NAME`,`DEPT`,`POSITION`,`PROG`),
  CONSTRAINT `CANDIDATES_ibfk_1` FOREIGN KEY (`ROLLNO`) REFERENCES `USER` (`ROLLNO`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CANDIDATES`
--

LOCK TABLES `CANDIDATES` WRITE;
/*!40000 ALTER TABLE `CANDIDATES` DISABLE KEYS */;
/*!40000 ALTER TABLE `CANDIDATES` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `GENSEC`
--

DROP TABLE IF EXISTS `GENSEC`;
/*!50001 DROP VIEW IF EXISTS `GENSEC`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `GENSEC` AS SELECT 
/* 1 AS `NAME`,
/* 1 AS `DEPT`,
/* 1 AS `POSITION`,
/* 1 AS `PROG`,
/* 1 AS `ROLLNO`, 
/* 1 AS `VOTES`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `SESSION`
--

DROP TABLE IF EXISTS `SESSION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SESSION` (
  `ROLLNO` varchar(10) NOT NULL,
  `TOKEN` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ROLLNO`),
  CONSTRAINT `SESSION_ibfk_1` FOREIGN KEY (`ROLLNO`) REFERENCES `USER` (`ROLLNO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SESSION`
--

LOCK TABLES `SESSION` WRITE;
/*!40000 ALTER TABLE `SESSION` DISABLE KEYS */;
/*!40000 ALTER TABLE `SESSION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `SPORTSEC`
--

DROP TABLE IF EXISTS `SPORTSEC`;
/*!50001 DROP VIEW IF EXISTS `SPORTSEC`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `SPORTSEC` AS SELECT 
/* 1 AS `NAME`,
/* 1 AS `DEPT`,
/* 1 AS `POSITION`,
/* 1 AS `PROG`,
/* 1 AS `ROLLNO`,
/* 1 AS `VOTES`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `USER`
--

DROP TABLE IF EXISTS `USER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `USER` (
  `ROLLNO` varchar(10) NOT NULL,
  `EMAIL` varchar(255) NOT NULL,
  `PWD` varchar(256) NOT NULL,
  `VOTED` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`ROLLNO`),
  UNIQUE KEY `EMAIL` (`EMAIL`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USER`
--

LOCK TABLES `USER` WRITE;
/*!40000 ALTER TABLE `USER` DISABLE KEYS */;
INSERT INTO `USER` VALUES ('admin','admin@nitc.ac.in','7fcf4ba391c48784edde599889d6e3f1e47a27db36ecc050cc92f259bfac38afad2c68a1ae804d77075e8fb722503f3eca2b2c1006ee6f6c7b7628cb45fffd1d',0);
/*!40000 ALTER TABLE `USER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `GENSEC`
--

/*!50001 DROP VIEW IF EXISTS `GENSEC`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`debian-sys-maint`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `GENSEC` AS select `CANDIDATES`.`NAME` AS `NAME`,`CANDIDATES`.`DEPT` AS `DEPT`,`CANDIDATES`.`POSITION` AS `POSITION`,`CANDIDATES`.`PROG` AS `PROG`,`CANDIDATES`.`ROLLNO` AS `ROLLNO`,`CANDIDATES`.`VOTES` AS `VOTES` from `CANDIDATES` where (`CANDIDATES`.`POSITION` = 'General Secretary') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `SPORTSEC`
--

/*!50001 DROP VIEW IF EXISTS `SPORTSEC`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`debian-sys-maint`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `SPORTSEC` AS select `CANDIDATES`.`NAME` AS `NAME`,`CANDIDATES`.`DEPT` AS `DEPT`,`CANDIDATES`.`POSITION` AS `POSITION`,`CANDIDATES`.`PROG` AS `PROG`,`CANDIDATES`.`ROLLNO` AS `ROLLNO`,`CANDIDATES`.`VOTES` AS `VOTES` from `CANDIDATES` where (`CANDIDATES`.`POSITION` = 'Sports Secretary') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-09-26 10:27:36
