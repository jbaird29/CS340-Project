-- MySQL dump 10.13  Distrib 8.0.23, for macos10.15 (x86_64)
--
-- Host: localhost    Database: cs340_project
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customer_contacts`
--

DROP TABLE IF EXISTS `customer_contacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_contacts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` varchar(12) NOT NULL,
  `house_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_email` (`email`),
  KEY `house_id` (`house_id`),
  CONSTRAINT `customer_contacts_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `houses` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_contacts`
--

LOCK TABLES `customer_contacts` WRITE;
/*!40000 ALTER TABLE `customer_contacts` DISABLE KEYS */;
INSERT INTO `customer_contacts` VALUES (1,'Lawrence','Lima','lawrence@email.com','123-456-7890',1),(2,'Mandy','Mike','mandy@email.com','234-567-8901',2),(3,'Norman','November','norman@email.com','345-678-9012',3),(4,'Ollie','Oscar','ollie@email.com','456-789-0123',4),(5,'Paul','Papa','paul@email.com','567-890-1234',5),(6,'Pauline','Papa','pauline@email.com','678-901-2345',5);
/*!40000 ALTER TABLE `customer_contacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `houses`
--

DROP TABLE IF EXISTS `houses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `houses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `street_address` varchar(100) NOT NULL,
  `street_address_2` varchar(100) DEFAULT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(2) NOT NULL,
  `zip_code` varchar(5) NOT NULL,
  `yard_size_acres` decimal(8,2) NOT NULL,
  `sales_manager_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sales_manager_id` (`sales_manager_id`),
  CONSTRAINT `houses_ibfk_1` FOREIGN KEY (`sales_manager_id`) REFERENCES `sales_managers` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `houses`
--

LOCK TABLES `houses` WRITE;
/*!40000 ALTER TABLE `houses` DISABLE KEYS */;
INSERT INTO `houses` VALUES (1,'1 Alpha Road',NULL,'Lennyville','NY','98765',1.10,1),(2,'2 Beta Street',NULL,'Lennyville','NY','98765',1.20,1),(3,'3 Charlie Ave','Unit 10','Lennyville','NY','98765',1.30,2),(4,'4 Delta Court',NULL,'Lennyville','NY','98765',1.40,2),(5,'5 Echo Lane',NULL,'Lennyville','NY','98765',1.50,3);
/*!40000 ALTER TABLE `houses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_workers`
--

DROP TABLE IF EXISTS `job_workers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_workers` (
  `job_id` int NOT NULL,
  `worker_id` int NOT NULL,
  PRIMARY KEY (`job_id`,`worker_id`),
  KEY `job_id` (`job_id`),
  KEY `worker_id` (`worker_id`),
  CONSTRAINT `job_workers_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `job_workers_ibfk_2` FOREIGN KEY (`worker_id`) REFERENCES `workers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_workers`
--

LOCK TABLES `job_workers` WRITE;
/*!40000 ALTER TABLE `job_workers` DISABLE KEYS */;
INSERT INTO `job_workers` VALUES (1,1),(1,2),(2,1),(2,2),(3,3),(4,3),(5,3),(6,1),(6,4),(7,1),(7,4);
/*!40000 ALTER TABLE `job_workers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `house_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `house_id` (`house_id`),
  CONSTRAINT `jobs_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `houses` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (1,'2020-04-01',55.00,1),(2,'2020-04-02',60.00,2),(3,'2020-04-03',65.00,3),(4,'2020-04-04',70.00,4),(5,'2020-04-05',75.00,5),(6,'2020-04-11',70.00,4),(7,'2020-04-12',75.00,5);
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lawnmowers`
--

DROP TABLE IF EXISTS `lawnmowers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lawnmowers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `brand` varchar(100) NOT NULL,
  `make_year` int NOT NULL,
  `model_name` varchar(100) NOT NULL,
  `is_functional` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lawnmowers`
--

LOCK TABLES `lawnmowers` WRITE;
/*!40000 ALTER TABLE `lawnmowers` DISABLE KEYS */;
INSERT INTO `lawnmowers` VALUES (1,'Alpha Motors',2020,'Slicer1000',1),(2,'Bravo Motors',2019,'Mower2000',1),(3,'Charlie Motors',2018,'Roarer3000',1),(4,'Delta Motors',2017,'Cutter4000',1),(5,'Echo Motors',2016,'Chopper5000',1),(6,'Foxtrot Motors',2015,'Snipper6000',0),(7,'Golf Motors',2015,'Vroomer7000',1),(8,'Hotel Motors',2015,'Soarer8000',1);
/*!40000 ALTER TABLE `lawnmowers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_managers`
--

DROP TABLE IF EXISTS `sales_managers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_managers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `region` varchar(100) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` varchar(12) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_managers`
--

LOCK TABLES `sales_managers` WRITE;
/*!40000 ALTER TABLE `sales_managers` DISABLE KEYS */;
INSERT INTO `sales_managers` VALUES (1,'North','Zach','Zulu','zach@lennys.com','111-111-1111'),(2,'South','Yara','Yankee','yara@lennys.com','222-222-2222'),(3,'East','Xavier','Xray','xavier@lennys.com','333-333-3333');
/*!40000 ALTER TABLE `sales_managers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workers`
--

DROP TABLE IF EXISTS `workers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` varchar(12) NOT NULL,
  `lawnmower_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_email` (`email`),
  KEY `lawnmower_id` (`lawnmower_id`),
  CONSTRAINT `workers_ibfk_1` FOREIGN KEY (`lawnmower_id`) REFERENCES `lawnmowers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workers`
--

LOCK TABLES `workers` WRITE;
/*!40000 ALTER TABLE `workers` DISABLE KEYS */;
INSERT INTO `workers` VALUES (1,'Adam','Alpha','adam@lennys.com','999-999-9999',1),(2,'Brenda','Bravo','brenda@lennys.com','888-888-8888',2),(3,'Connor','Charlie','connor@lennys.com','777-777-7777',3),(4,'Denise','Delta','denise@lennys.com','666-666-6666',4);
/*!40000 ALTER TABLE `workers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-24 17:48:55
