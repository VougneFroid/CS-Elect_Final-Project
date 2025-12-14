-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: shiperd
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `pilot`
--

DROP TABLE IF EXISTS `pilot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pilot` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `flight_years` int NOT NULL,
  `rank` varchar(45) NOT NULL,
  `mission_success` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pilot`
--

LOCK TABLES `pilot` WRITE;
/*!40000 ALTER TABLE `pilot` DISABLE KEYS */;
INSERT INTO `pilot` VALUES (1,'Vougne Froid Alis',30,'Admiral',234),(2,'Jophil Gulane',24,'Top Seargent',146),(3,'Ivan Rossvelt Venturillo',34,'Top Admiral',398),(4,'Dianara Kristy Garciano',19,'Seargent',98),(5,'Juan Miguel',28,'Overseer',237),(6,'Kenneth Castillo',28,'Gunman',198);
/*!40000 ALTER TABLE `pilot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ship`
--

DROP TABLE IF EXISTS `ship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ship` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `capacity` int NOT NULL,
  `speed` int NOT NULL,
  `shield` int NOT NULL,
  `ship_class_id` int NOT NULL,
  `pilot_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_ship_ship_class1_idx` (`ship_class_id`),
  KEY `fk_ship_pilot1_idx` (`pilot_id`),
  CONSTRAINT `fk_ship_pilot1` FOREIGN KEY (`pilot_id`) REFERENCES `pilot` (`id`),
  CONSTRAINT `fk_ship_ship_class1` FOREIGN KEY (`ship_class_id`) REFERENCES `ship_class` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ship`
--

LOCK TABLES `ship` WRITE;
/*!40000 ALTER TABLE `ship` DISABLE KEYS */;
INSERT INTO `ship` VALUES (1,'Heihachi',100,500,100,1,1),(2,'Lars',500,250,150,2,2),(3,'Kazuya',50,750,120,3,3),(4,'Annie',250,400,150,4,4),(5,'Camille',100,300,300,5,5),(6,'Gnar',100,300,300,5,6),(7,'Krushna',250,400,150,4,1),(8,'Poseidon',50,750,120,3,2),(9,'Zues',500,250,150,2,3),(10,'Hades',100,500,100,1,4),(11,'Penetrator',100,500,100,1,5),(12,'The luxury',500,250,150,2,6),(13,'Star Killer',50,250,150,3,1),(14,'Pietro',250,205,150,4,2),(15,'Sabre',500,540,200,5,3),(16,'Elephant',100,400,100,5,4),(17,'UnosAnos',50,250,50,4,5),(18,'FlyBird',132,540,50,3,6),(19,'Decimator',430,431,100,2,1),(20,'The Civ',700,500,500,4,1);
/*!40000 ALTER TABLE `ship` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ship_class`
--

DROP TABLE IF EXISTS `ship_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ship_class` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ship_class`
--

LOCK TABLES `ship_class` WRITE;
/*!40000 ALTER TABLE `ship_class` DISABLE KEYS */;
INSERT INTO `ship_class` VALUES (1,'corvette','for personal travels'),(2,'hauler','enhanced inventory for more capacity'),(3,'fighter','enhanced weaponry'),(4,'cruise','enhance quality of life and luxury'),(5,'tank','enhanced shield');
/*!40000 ALTER TABLE `ship_class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ship_weapons`
--

DROP TABLE IF EXISTS `ship_weapons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ship_weapons` (
  `ship_id` int NOT NULL,
  `ship_class_id` int NOT NULL,
  `weapon_class_id` int NOT NULL,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`ship_id`,`ship_class_id`,`weapon_class_id`),
  KEY `fk_ship_has_weapon_class_weapon_class1_idx` (`weapon_class_id`),
  KEY `fk_ship_has_weapon_class_ship1_idx` (`ship_id`,`ship_class_id`),
  CONSTRAINT `fk_ship_has_weapon_class_ship1` FOREIGN KEY (`ship_id`) REFERENCES `ship` (`id`),
  CONSTRAINT `fk_ship_has_weapon_class_weapon_class1` FOREIGN KEY (`weapon_class_id`) REFERENCES `weapon_class` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ship_weapons`
--

LOCK TABLES `ship_weapons` WRITE;
/*!40000 ALTER TABLE `ship_weapons` DISABLE KEYS */;
INSERT INTO `ship_weapons` VALUES (1,1,1,'Galil'),(2,2,2,'Ark Blast'),(3,3,3,'Dark Upper'),(4,4,4,'Electric Wind God Fist'),(5,5,5,'Shockwave'),(6,6,1,'Hell Sweep'),(7,7,2,'Orbital'),(8,8,3,'Crushing Wing Interference'),(9,9,4,'Shield Crusher'),(10,10,5,'Life Seeker'),(11,11,1,'AK-47000'),(12,12,2,'MP90M'),(13,13,3,'LightEnder'),(14,14,4,'SoulCrusher'),(15,15,5,'LinieageEnder'),(16,16,1,'CantTouchMe'),(17,17,2,'Incenerator'),(18,18,3,'ShiningWizard'),(19,19,4,'Explosion'),(20,20,5,'WingCrusher');
/*!40000 ALTER TABLE `ship_weapons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weapon_class`
--

DROP TABLE IF EXISTS `weapon_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weapon_class` (
  `id` int NOT NULL AUTO_INCREMENT,
  `class` varchar(45) NOT NULL,
  `damage` int NOT NULL,
  `reload_speed` int NOT NULL,
  `spread` int NOT NULL,
  `range` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weapon_class`
--

LOCK TABLES `weapon_class` WRITE;
/*!40000 ALTER TABLE `weapon_class` DISABLE KEYS */;
INSERT INTO `weapon_class` VALUES (1,'gatling',150,5,20,1000),(2,'missile',200,2,0,5000),(3,'laser',80,7,0,1500),(4,'shrapnel',250,10,100,500),(5,'melee',300,0,0,200);
/*!40000 ALTER TABLE `weapon_class` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-12 14:35:06
