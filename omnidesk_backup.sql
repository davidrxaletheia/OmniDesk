-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: omnidesk
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alert`
--

DROP TABLE IF EXISTS `alert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alert` (
  `alert_id` int(11) NOT NULL AUTO_INCREMENT,
  `alert_time` datetime NOT NULL,
  `message` varchar(255) NOT NULL,
  `kind` enum('ticket','event','incident') NOT NULL DEFAULT 'incident',
  `ticket_id` int(11) DEFAULT NULL,
  `event_id` int(11) DEFAULT NULL,
  `sent` tinyint(1) NOT NULL DEFAULT 0,
  `created_by` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`alert_id`),
  KEY `fk_alert_ticket` (`ticket_id`),
  KEY `fk_alert_event` (`event_id`),
  KEY `fk_alert_creator` (`created_by`),
  KEY `idx_alert_time` (`alert_time`),
  KEY `idx_alert_sent` (`sent`,`kind`),
  CONSTRAINT `fk_alert_creator` FOREIGN KEY (`created_by`) REFERENCES `app_user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_alert_event` FOREIGN KEY (`event_id`) REFERENCES `calendar_event` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_alert_ticket` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`ticket_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `CONSTRAINT_1` CHECK (`ticket_id` is not null or `event_id` is not null)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alert`
--

LOCK TABLES `alert` WRITE;
/*!40000 ALTER TABLE `alert` DISABLE KEYS */;
INSERT INTO `alert` VALUES (1,'2025-10-25 11:00:00','Preparar equipo para visita.','ticket',1,NULL,0,12,'2025-10-25 03:00:00'),(2,'2025-10-24 17:00:00','Revisar avance del ticket.','ticket',31,NULL,0,6,'2025-10-23 17:00:00'),(3,'2025-10-25 06:00:00','Preparar equipo para visita.','ticket',1,NULL,1,2,'2025-10-24 18:00:00'),(4,'2025-10-27 19:00:00','Recordatorio: evento en 1 hora.','ticket',19,NULL,0,11,'2025-10-27 00:00:00'),(5,'2025-10-26 11:00:00','Recordatorio: evento en 1 hora.','ticket',13,NULL,1,4,'2025-10-26 02:00:00'),(6,'2025-10-23 07:00:00','Cliente solicitó actualización del caso.','incident',12,NULL,0,2,'2025-10-23 06:00:00'),(7,'2025-10-23 08:00:00','Preparar equipo para visita.','incident',8,NULL,1,4,'2025-10-22 20:00:00'),(8,'2025-10-25 15:00:00','Revisar avance del ticket.','incident',40,NULL,1,3,'2025-10-25 08:00:00'),(9,'2025-10-26 19:00:00','Preparar equipo para visita.','incident',24,20,0,4,'2025-10-26 17:00:00'),(10,'2025-10-23 18:00:00','Revisar avance del ticket.','incident',4,NULL,0,5,'2025-10-23 13:00:00'),(11,'2025-10-23 18:00:00','Preparar equipo para visita.','ticket',6,NULL,0,11,'2025-10-22 22:00:00'),(12,'2025-10-28 07:00:00','Confirmar dirección de instalación.','event',NULL,25,0,9,'2025-10-27 19:00:00'),(13,'2025-10-24 20:00:00','Preparar equipo para visita.','ticket',21,NULL,0,9,'2025-10-23 21:00:00'),(14,'2025-10-24 14:00:00','Preparar equipo para visita.','event',NULL,9,0,11,'2025-10-23 19:00:00'),(15,'2025-10-23 11:00:00','Revisar avance del ticket.','ticket',13,NULL,0,4,'2025-10-22 22:00:00'),(16,'2025-10-27 03:00:00','Preparar equipo para visita.','event',NULL,19,1,6,'2025-10-26 18:00:00'),(17,'2025-10-24 10:00:00','Revisar avance del ticket.','ticket',19,NULL,0,6,'2025-10-24 02:00:00'),(18,'2025-10-24 11:00:00','Preparar equipo para visita.','incident',40,14,0,7,'2025-10-23 23:00:00'),(19,'2025-10-25 02:00:00','Cliente solicitó actualización del caso.','event',NULL,1,1,4,'2025-10-24 17:00:00'),(20,'2025-10-23 10:00:00','Cliente solicitó actualización del caso.','ticket',19,NULL,0,9,'2025-10-22 16:00:00'),(21,'2025-10-23 10:00:00','Cliente solicitó actualización del caso.','ticket',7,NULL,1,6,'2025-10-23 08:00:00'),(22,'2025-10-24 06:00:00','Cliente solicitó actualización del caso.','ticket',22,NULL,1,12,'2025-10-23 08:00:00'),(23,'2025-10-26 06:00:00','Confirmar dirección de instalación.','ticket',35,NULL,0,1,'2025-10-25 20:00:00'),(24,'2025-10-26 01:00:00','Preparar equipo para visita.','event',NULL,27,0,11,'2025-10-26 00:00:00'),(25,'2025-10-24 16:00:00','Confirmar dirección de instalación.','ticket',26,NULL,1,12,'2025-10-23 16:00:00'),(26,'2025-10-26 21:00:00','Revisar avance del ticket.','incident',38,24,1,2,'2025-10-26 10:00:00'),(27,'2025-10-26 23:00:00','Preparar equipo para visita.','ticket',29,NULL,0,9,'2025-10-26 22:00:00'),(28,'2025-10-26 08:00:00','Confirmar dirección de instalación.','ticket',20,NULL,0,1,'2025-10-25 16:00:00'),(29,'2025-10-23 01:00:00','Cliente solicitó actualización del caso.','ticket',27,NULL,0,7,'2025-10-22 02:00:00'),(30,'2025-10-24 03:00:00','Cliente solicitó actualización del caso.','incident',10,NULL,0,6,'2025-10-23 08:00:00'),(31,'2025-10-22 17:00:00','Confirmar dirección de instalación.','incident',26,7,1,7,'2025-10-22 10:00:00'),(32,'2025-10-25 09:00:00','Cliente solicitó actualización del caso.','incident',29,NULL,1,9,'2025-10-25 03:00:00'),(33,'2025-10-27 14:00:00','Confirmar dirección de instalación.','event',NULL,1,1,2,'2025-10-27 01:00:00'),(34,'2025-10-26 06:00:00','Revisar avance del ticket.','event',NULL,22,0,8,'2025-10-26 04:00:00'),(35,'2025-10-25 20:00:00','Recordatorio: evento en 1 hora.','ticket',21,NULL,0,7,'2025-10-25 07:00:00'),(36,'2025-10-27 09:00:00','Revisar avance del ticket.','incident',27,NULL,1,4,'2025-10-27 04:00:00'),(37,'2025-10-27 03:00:00','Preparar equipo para visita.','incident',NULL,20,0,9,'2025-10-26 04:00:00'),(38,'2025-10-22 22:00:00','Cliente solicitó actualización del caso.','ticket',1,NULL,0,8,'2025-10-22 19:00:00'),(39,'2025-10-24 17:00:00','Revisar avance del ticket.','incident',22,15,0,12,'2025-10-24 14:00:00'),(40,'2025-10-25 16:00:00','Preparar equipo para visita.','event',NULL,23,0,5,'2025-10-25 03:00:00'),(41,'2025-10-24 07:00:00','Preparar equipo para visita.','ticket',12,NULL,0,12,'2025-10-23 17:00:00'),(42,'2025-10-25 00:00:00','Revisar avance del ticket.','incident',16,NULL,0,3,'2025-10-24 15:00:00'),(43,'2025-10-22 19:00:00','Cliente solicitó actualización del caso.','incident',NULL,30,0,9,'2025-10-22 15:00:00'),(44,'2025-10-26 10:00:00','Recordatorio: evento en 1 hora.','incident',21,NULL,1,9,'2025-10-26 08:00:00'),(45,'2025-10-25 12:00:00','Recordatorio: evento en 1 hora.','incident',30,11,0,7,'2025-10-25 10:00:00'),(46,'2025-10-28 04:00:00','Recordatorio: evento en 1 hora.','incident',9,22,0,2,'2025-10-28 01:00:00'),(47,'2025-10-23 15:00:00','Revisar avance del ticket.','incident',NULL,16,0,3,'2025-10-23 14:00:00'),(48,'2025-10-24 09:00:00','Revisar avance del ticket.','event',NULL,4,0,7,'2025-10-24 03:00:00'),(49,'2025-10-27 15:00:00','Recordatorio: evento en 1 hora.','incident',NULL,15,1,12,'2025-10-27 13:00:00'),(50,'2025-10-22 19:00:00','Revisar avance del ticket.','event',NULL,23,1,11,'2025-10-22 02:00:00'),(51,'2025-10-28 18:29:33','Recordatorio: visita técnica en 30min','event',NULL,31,0,1,'2025-10-28 16:59:33');
/*!40000 ALTER TABLE `alert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_user`
--

DROP TABLE IF EXISTS `app_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(150) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('admin','empleado') NOT NULL DEFAULT 'empleado',
  `active` tinyint(1) NOT NULL DEFAULT 1,
  `last_login_at` datetime DEFAULT NULL,
  `password_changed_at` datetime DEFAULT NULL,
  `failed_login_attempts` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `locked_until` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `uq_app_user_username` (`username`),
  UNIQUE KEY `uq_app_user_email` (`email`),
  KEY `idx_app_user_role_active` (`role`,`active`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_user`
--

LOCK TABLES `app_user` WRITE;
/*!40000 ALTER TABLE `app_user` DISABLE KEYS */;
INSERT INTO `app_user` VALUES (1,'Elena Gómez','elena.gómez','elena.gómez@omnidesk.mx','$2b$12$brnTP3fAbnFbmOHnKYaXRvj7uff0LYTH8xIZM1JRcoreogrNwwmq6','admin',1,'2025-10-17 10:00:00','2025-09-18 16:00:00',0,NULL,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(2,'María Castro','maría.castro1','maría.castro1@omnidesk.mx','$2b$12$Tkx9NIQ0Wobtqn62tOy4CqpIqK3yn9FfcgMXAdx9G81aSQHqNgAC7','admin',1,'2025-10-12 13:00:00','2025-09-29 20:00:00',0,NULL,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(3,'María Castro','maría.castro2','maría.castro2@omnidesk.mx','$2b$12$41sNLjVHWGaub52Ztd26fEeVVhDIq2AnHTmt9OBGhnuKoneNo41eo','empleado',1,'2025-10-16 21:00:00','2025-10-01 19:00:00',0,NULL,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(4,'María Vega','maría.vega3','maría.vega3@omnidesk.mx','$2b$12$6JDWYlgAACTP9gyv1plBArp5B1Id9Z850kEnydx9qWCA79ISjs8JH','empleado',1,'2025-10-16 02:00:00','2025-10-07 11:00:00',0,NULL,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(5,'Miguel Flores','miguel.flores4','miguel.flores4@omnidesk.mx','$2b$12$F0j7elKPoh3pKMzKG5mSoyPstUeC99enq522wjZRL9OaYsP6ihgIq','empleado',1,'2025-10-18 06:00:00','2025-09-28 06:00:00',0,NULL,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(6,'Elena Silva','elena.silva5','elena.silva5@omnidesk.mx','$2b$12$0Fp4dNZcui8kBRIg6QjcwIAcw58cwQPvI28U5okXkzl5WzPTpjRxc','empleado',1,'2025-10-20 05:00:00','2025-10-01 22:00:00',0,NULL,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(7,'Jorge Santos','jorge.santos6','jorge.santos6@omnidesk.mx','$2b$12$Y2nOyreVvFQ0ub2qJ8cKvWB9h3lcBGYQ6TmA65MPh3FPuRIlPxUkJ','empleado',1,'2025-10-20 19:00:00','2025-10-08 03:00:00',0,NULL,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(8,'Daniela Hernández','daniela.hernández7','daniela.hernández7@omnidesk.mx','$2b$12$AJOCBnD3XkfFNuYUPnmbpD0ezNmREpOaUVgAk7Gdp0CXP9K63LSFZ','empleado',1,'2025-10-18 22:00:00','2025-10-02 13:00:00',0,NULL,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(9,'Lucía Flores','lucía.flores8','lucía.flores8@omnidesk.mx','$2b$12$qpNVGMrerqtHioRRdzHzmA4KR1VxavU07zUHLnnBbuQzkChMbyIbN','empleado',1,'2025-10-24 22:00:00','2025-10-03 11:00:00',0,NULL,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(10,'Daniela Ramírez','daniela.ramírez9','daniela.ramírez9@omnidesk.mx','$2b$12$uCu2r6AZDUd7ne7cbp0MoDh6CpwL7SWktJ5J4x6mKZpRsQXXJcHPe','empleado',1,'2025-10-17 02:00:00','2025-10-07 23:00:00',0,NULL,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(11,'Lucía Gómez','lucía.gómez10','lucía.gómez10@omnidesk.mx','$2b$12$Aw3CjkGOM5WCZKtp5rBUJPuEuEvqrK2IGlozIoDSBbszpPwIv9IvC','empleado',1,'2025-10-23 04:00:00','2025-10-01 09:00:00',0,NULL,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(12,'Raúl Hernández','raúl.hernández11','raúl.hernández11@omnidesk.mx','$2b$12$tU6QlTrKVL8ZswsRhcds6NUgarDv7p1heEJQjY6fpIzKMWx4sKAJd','empleado',1,'2025-10-16 09:00:00','2025-10-01 16:00:00',0,NULL,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(13,'David Xochipa','x0chipa','davidxochipa.24@gmail.com','$2b$12$A5dNkhHK0/zItU1pXly8aug45f7Tzh26EjquOlX2qCE3CJhRs8cX6','admin',1,'2025-10-30 16:23:17','2025-10-29 16:55:05',0,NULL,'2025-10-29 16:55:05','2025-10-30 16:23:17');
/*!40000 ALTER TABLE `app_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `calendar_event`
--

DROP TABLE IF EXISTS `calendar_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `calendar_event` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(150) NOT NULL,
  `description` text DEFAULT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `ticket_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  KEY `idx_event_start` (`start_time`),
  KEY `idx_event_creator` (`created_by`),
  KEY `idx_event_ticket` (`ticket_id`),
  CONSTRAINT `fk_event_creator` FOREIGN KEY (`created_by`) REFERENCES `app_user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_event_ticket` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`ticket_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `CONSTRAINT_1` CHECK (`end_time` >= `start_time`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calendar_event`
--

LOCK TABLES `calendar_event` WRITE;
/*!40000 ALTER TABLE `calendar_event` DISABLE KEYS */;
INSERT INTO `calendar_event` VALUES (1,'Seguimiento Impresora','Revisión de sitio','2025-10-26 22:00:00','2025-10-27 00:00:00',4,28),(2,'Visita técnica Impresora','Revisión de sitio','2025-10-23 15:00:00','2025-10-23 18:00:00',6,12),(3,'Visita técnica Ventas','Sesión de capacitación','2025-10-25 05:00:00','2025-10-25 07:00:00',6,2),(4,'Capacitación Soporte','Plan de trabajo','2025-10-25 12:00:00','2025-10-25 13:00:00',11,25),(5,'Visita técnica CCTV','Plan de trabajo','2025-10-21 07:00:00','2025-10-21 10:00:00',4,36),(6,'Reunión interna Ventas','Entrega de equipo','2025-10-26 18:00:00','2025-10-26 19:00:00',12,4),(7,'Instalación CCTV','Plan de trabajo','2025-10-24 20:00:00','2025-10-24 23:00:00',5,12),(8,'Visita técnica Ventas','Plan de trabajo','2025-10-23 15:00:00','2025-10-23 18:00:00',8,NULL),(9,'Seguimiento Wi‑Fi','Sesión de capacitación','2025-10-21 23:00:00','2025-10-22 01:00:00',2,33),(10,'Seguimiento Soporte','Sesión de capacitación','2025-10-27 13:00:00','2025-10-27 14:00:00',1,17),(11,'Seguimiento Ventas','Seguimiento de casos','2025-10-23 12:00:00','2025-10-23 14:00:00',4,21),(12,'Visita técnica Ventas','Revisión de sitio','2025-10-24 14:00:00','2025-10-24 16:00:00',2,15),(13,'Instalación Impresora','Sesión de capacitación','2025-10-24 10:00:00','2025-10-24 13:00:00',11,6),(14,'Visita técnica Soporte','Seguimiento de casos','2025-10-27 18:00:00','2025-10-27 21:00:00',6,16),(15,'Instalación Wi‑Fi','Seguimiento de casos','2025-10-25 02:00:00','2025-10-25 03:00:00',6,33),(16,'Instalación Wi‑Fi','Plan de trabajo','2025-10-21 09:00:00','2025-10-21 12:00:00',8,37),(17,'Visita técnica Wi‑Fi','Revisión de sitio','2025-10-28 00:00:00','2025-10-28 02:00:00',12,4),(18,'Instalación Wi‑Fi','Seguimiento de casos','2025-10-28 03:00:00','2025-10-28 06:00:00',11,27),(19,'Visita técnica Wi‑Fi','Revisión de sitio','2025-10-28 03:00:00','2025-10-28 05:00:00',7,6),(20,'Reunión interna Soporte','Entrega de equipo','2025-10-27 22:00:00','2025-10-28 00:00:00',8,27),(21,'Reunión interna Ventas','Revisión de sitio','2025-10-22 16:00:00','2025-10-22 19:00:00',1,29),(22,'Reunión interna CCTV','Plan de trabajo','2025-10-25 09:00:00','2025-10-25 10:00:00',1,38),(23,'Visita técnica Ventas','Entrega de equipo','2025-10-25 16:00:00','2025-10-25 19:00:00',5,22),(24,'Seguimiento Soporte','Plan de trabajo','2025-10-21 07:00:00','2025-10-21 08:00:00',3,2),(25,'Visita técnica Impresora','Sesión de capacitación','2025-10-21 20:00:00','2025-10-21 23:00:00',6,19),(26,'Reunión interna Ventas','Entrega de equipo','2025-10-25 21:00:00','2025-10-25 23:00:00',10,21),(27,'Capacitación CCTV','Revisión de sitio','2025-10-26 11:00:00','2025-10-26 12:00:00',9,35),(28,'Visita técnica Soporte','Sesión de capacitación','2025-10-25 06:00:00','2025-10-25 09:00:00',4,4),(29,'Capacitación Impresora','Seguimiento de casos','2025-10-20 17:00:00','2025-10-20 20:00:00',6,37),(30,'Reunión interna CCTV','Plan de trabajo','2025-10-23 23:00:00','2025-10-24 01:00:00',3,6),(31,'Visita técnica','Optimización APs y canales','2025-10-28 18:59:33','2025-10-28 19:59:33',1,41),(32,'Test Event pytest','Event created during test','2025-11-01 09:00:00','2025-11-01 10:00:00',NULL,NULL),(33,'Test Event pytest','Event created during test','2025-11-01 09:00:00','2025-11-01 10:00:00',NULL,NULL),(34,'Test Event pytest','Event created during test','2025-11-01 09:00:00','2025-11-01 10:00:00',NULL,NULL),(35,'Test Event pytest','Event created during test','2025-11-01 09:00:00','2025-11-01 10:00:00',NULL,NULL),(36,'Test Event pytest','Event created during test','2025-11-01 09:00:00','2025-11-01 10:00:00',NULL,NULL),(37,'Test Event pytest','Event created during test','2025-11-01 09:00:00','2025-11-01 10:00:00',NULL,NULL),(38,'Test Event pytest','Event created during test','2025-11-01 09:00:00','2025-11-01 10:00:00',NULL,NULL),(39,'Test Event pytest','Event created during test','2025-11-01 09:00:00','2025-11-01 10:00:00',NULL,NULL);
/*!40000 ALTER TABLE `calendar_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalog`
--

DROP TABLE IF EXISTS `catalog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalog` (
  `catalog_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `description` text DEFAULT NULL,
  `discount_percentage` decimal(5,2) NOT NULL DEFAULT 0.00 CHECK (`discount_percentage` >= 0 and `discount_percentage` <= 100),
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `visible_to` enum('todos','premium','interno') NOT NULL DEFAULT 'todos',
  `active` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`catalog_id`),
  UNIQUE KEY `uq_catalog_name` (`name`),
  KEY `idx_catalog_active_dates` (`active`,`start_date`,`end_date`,`visible_to`),
  CONSTRAINT `chk_catalog_dates` CHECK (`end_date` is null or `start_date` is null or `start_date` <= `end_date`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalog`
--

LOCK TABLES `catalog` WRITE;
/*!40000 ALTER TABLE `catalog` DISABLE KEYS */;
INSERT INTO `catalog` VALUES (1,'Buen Fin 2025','Descuentos especiales por temporada.',15.00,'2025-11-15','2025-11-18','todos',1,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(2,'Promo Premium Q4','Beneficios exclusivos para clientes premium.',10.00,'2025-10-01','2025-12-31','premium',1,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(3,'Liquidación Oficina','Liquidación interna de mobiliario de oficina.',0.00,NULL,NULL,'interno',1,'2025-10-28 21:05:45','2025-10-28 21:05:45');
/*!40000 ALTER TABLE `catalog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalog_product`
--

DROP TABLE IF EXISTS `catalog_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalog_product` (
  `catalog_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `special_price` decimal(10,2) DEFAULT NULL CHECK (`special_price` is null or `special_price` >= 0),
  `assigned_stock` int(10) unsigned DEFAULT NULL CHECK (`assigned_stock` is null or `assigned_stock` >= 0),
  PRIMARY KEY (`catalog_id`,`product_id`),
  KEY `idx_cp_product` (`product_id`),
  CONSTRAINT `fk_cp_catalog` FOREIGN KEY (`catalog_id`) REFERENCES `catalog` (`catalog_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_cp_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalog_product`
--

LOCK TABLES `catalog_product` WRITE;
/*!40000 ALTER TABLE `catalog_product` DISABLE KEYS */;
INSERT INTO `catalog_product` VALUES (1,5,2730.60,12),(1,6,5429.38,14),(1,17,NULL,13),(1,21,NULL,15),(1,25,NULL,34),(1,26,NULL,21),(1,36,NULL,8),(1,47,6446.67,29),(1,52,NULL,21),(1,53,5770.82,52),(2,1,NULL,18),(2,18,8097.08,7),(2,27,NULL,16),(2,30,10936.30,12),(2,34,NULL,16),(2,38,NULL,31),(2,40,NULL,8),(2,45,13496.03,26),(2,48,11210.37,23),(2,59,18199.70,19),(3,7,5477.75,7),(3,8,NULL,23),(3,10,NULL,45),(3,41,19720.26,17),(3,43,4622.80,4);
/*!40000 ALTER TABLE `catalog_product` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_cp_before_ins
BEFORE INSERT ON catalog_product
FOR EACH ROW
BEGIN
  DECLARE base_price DECIMAL(10,2);
  DECLARE prod_stock INT UNSIGNED;

  SELECT price, stock INTO base_price, prod_stock
  FROM product
  WHERE product_id = NEW.product_id;

  IF NEW.assigned_stock IS NOT NULL AND NEW.assigned_stock > prod_stock THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'assigned_stock excede el stock disponible del producto';
  END IF;

  IF NEW.special_price IS NOT NULL AND NEW.special_price > base_price THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'special_price no puede ser mayor que el precio base';
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_cp_before_upd
BEFORE UPDATE ON catalog_product
FOR EACH ROW
BEGIN
  DECLARE base_price DECIMAL(10,2);
  DECLARE prod_stock INT UNSIGNED;

  SELECT price, stock INTO base_price, prod_stock
  FROM product
  WHERE product_id = NEW.product_id;

  IF NEW.assigned_stock IS NOT NULL AND NEW.assigned_stock > prod_stock THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'assigned_stock excede el stock disponible del producto';
  END IF;

  IF NEW.special_price IS NOT NULL AND NEW.special_price > base_price THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'special_price no puede ser mayor que el precio base';
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `uq_category_name` (`name`),
  KEY `fk_category_parent` (`parent_id`),
  CONSTRAINT `fk_category_parent` FOREIGN KEY (`parent_id`) REFERENCES `category` (`category_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Tecnología',NULL,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(2,'Electrónica',1,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(3,'Oficina',NULL,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(4,'Hogar',NULL,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(5,'Accesorios',1,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(6,'Redes',1,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(7,'Impresión',3,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(8,'Seguridad',2,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(9,'Mobiliario',3,'2025-10-28 21:05:45','2025-10-28 21:05:45'),(10,'Audio',2,'2025-10-28 21:05:45','2025-10-28 21:05:45');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `client` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `telegram_username` varchar(50) DEFAULT NULL,
  `telegram_user_id` bigint(20) unsigned DEFAULT NULL,
  `client_type` enum('normal','premium') NOT NULL DEFAULT 'normal',
  `status` enum('active','inactive','blocked') NOT NULL DEFAULT 'active',
  `registered_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`client_id`),
  UNIQUE KEY `uq_client_phone` (`phone`),
  UNIQUE KEY `uq_client_email` (`email`),
  UNIQUE KEY `uq_client_telegram_id` (`telegram_user_id`),
  KEY `fk_client_created_by` (`created_by`),
  KEY `fk_client_updated_by` (`updated_by`),
  KEY `idx_client_name` (`full_name`),
  KEY `idx_client_type_status` (`client_type`,`status`),
  KEY `idx_client_registered_at` (`registered_at`),
  CONSTRAINT `fk_client_created_by` FOREIGN KEY (`created_by`) REFERENCES `app_user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_client_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `app_user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
INSERT INTO `client` VALUES (1,'Servicios El Molino','221-260-4929','gcaqv@mail.com',NULL,NULL,'normal','active','2025-09-19 10:00:00','2025-10-28 21:05:45',NULL,5,12),(2,'Elena Hernández','224-906-4241','ptx63@empresa.mx',NULL,NULL,'normal','active','2025-09-12 03:00:00','2025-10-28 21:05:45',NULL,10,12),(3,'Lucía Gómez','227-805-5982','z7src@empresa.mx','0vaiy4v',5000021763,'normal','active','2025-09-12 11:00:00','2025-10-28 21:05:45',NULL,11,5),(4,'María Flores','228-767-8245','6gvwr@empresa.mx',NULL,NULL,'normal','active','2025-10-12 07:00:00','2025-10-28 21:05:45',NULL,6,11),(5,'Jorge Ramírez','227-395-7561','3tqll@corp.mx','3a5qbsw',5000522717,'normal','active','2025-09-30 19:00:00','2025-10-28 21:05:45',NULL,1,4),(6,'Tecnologías El Molino','227-815-8941','e9vif@example.com',NULL,NULL,'normal','active','2025-09-19 09:00:00','2025-10-28 21:05:45',NULL,4,2),(7,'Elena López','227-833-5781','sj49i@example.com',NULL,NULL,'premium','active','2025-09-01 08:00:00','2025-10-28 21:05:45',NULL,10,9),(8,'Carlos Santos','226-448-9318','ja04u@corp.mx','qrl1n75',5000731390,'premium','active','2025-08-29 23:00:00','2025-10-28 21:05:45',NULL,7,4),(9,'Ana Pérez','227-822-7246','nx39r@empresa.mx',NULL,NULL,'normal','active','2025-09-20 09:00:00','2025-10-28 21:05:45',NULL,6,2),(10,'Sofía Flores','220-839-3361','oxfq8@mail.com','oclyt8w',5000930556,'normal','active','2025-09-09 10:00:00','2025-10-28 21:05:45',NULL,9,1),(11,'Servicios El Molino','223-864-2480','pdw5p@mail.com','b2knftu',5000831026,'premium','active','2025-09-09 00:00:00','2025-10-28 21:05:45',NULL,3,2),(12,'Miguel Silva','223-609-3344','iwqy6@corp.mx','yfpmvxp',5000262256,'normal','active','2025-09-23 21:00:00','2025-10-28 21:05:45',NULL,5,4),(13,'Carlos Hernández','226-685-6881','u9k9x@mail.com',NULL,NULL,'normal','active','2025-09-09 13:00:00','2025-10-28 21:05:45',NULL,12,1),(14,'Lucía Santos','223-721-6772','hgj11@negocio.mx','6xlpu0d',5000309455,'normal','active','2025-10-06 08:00:00','2025-10-28 21:05:45',NULL,7,3),(15,'Sofía Pérez','228-613-5465','3j3r3@mail.com','qc1iyyo',5000886837,'normal','active','2025-08-29 00:00:00','2025-10-28 21:05:45',NULL,6,2),(16,'Alimentos El Molino','228-226-8451','n0jnw@mail.com',NULL,NULL,'premium','active','2025-09-13 02:00:00','2025-10-28 21:05:45',NULL,1,10),(17,'Miguel Hernández','221-750-8606','6kof8@mail.com','eitnn8z',5000566442,'normal','active','2025-10-08 23:00:00','2025-10-28 21:05:45',NULL,12,12),(18,'Elena Gómez','227-730-7686','7kyhq@negocio.mx','dyt9mog',5000128103,'normal','active','2025-09-06 06:00:00','2025-10-28 21:05:45',NULL,8,2),(19,'Elena Silva','229-121-1828','2ieuc@example.com',NULL,NULL,'premium','active','2025-08-30 08:00:00','2025-10-28 21:05:45',NULL,4,6),(20,'Miguel Ruiz','224-979-3370','9t2d5@negocio.mx',NULL,NULL,'normal','active','2025-09-28 12:00:00','2025-10-28 21:05:45',NULL,4,10),(21,'Tecnologías El Molino','220-229-7897','s0r2s@empresa.mx',NULL,NULL,'premium','active','2025-09-01 15:00:00','2025-10-28 21:05:45',NULL,10,1),(22,'Sofía Santos','227-758-1510','croyr@corp.mx',NULL,NULL,'premium','active','2025-10-14 08:00:00','2025-10-28 21:05:45',NULL,10,3),(23,'Daniela Mendoza','229-661-6327','nvksp@empresa.mx','x1zhqim',5000475538,'normal','active','2025-09-27 23:00:00','2025-10-28 21:05:45',NULL,12,2),(24,'Jorge Silva','224-483-3500','yrddp@mail.com','uvulemx',5000786740,'normal','active','2025-09-29 17:00:00','2025-10-28 21:05:45',NULL,12,1),(25,'Daniela Pérez','221-691-9313','hxid4@mail.com',NULL,NULL,'normal','active','2025-09-12 17:00:00','2025-10-28 21:05:45',NULL,4,7),(26,'Farmacia Don Paco','220-723-5381','bj17m@negocio.mx','uofwb0h',5000440236,'normal','active','2025-09-28 13:00:00','2025-10-28 21:05:45',NULL,3,6),(27,'Jorge Mendoza','229-186-1861','f1bcp@corp.mx',NULL,NULL,'normal','active','2025-08-30 20:00:00','2025-10-28 21:05:45',NULL,5,4),(28,'Carlos Pérez','226-213-5640','yvslh@example.com',NULL,NULL,'premium','active','2025-08-31 04:00:00','2025-10-28 21:05:45',NULL,4,3),(29,'Daniela Pérez','221-107-9149','0gnzs@mail.com',NULL,NULL,'normal','active','2025-10-16 22:00:00','2025-10-28 21:05:45',NULL,1,7),(30,'Carlos Pérez','229-539-7626','zpeal@example.com',NULL,NULL,'normal','active','2025-09-21 09:00:00','2025-10-28 21:05:45',NULL,6,2),(31,'Servicios Del Centro','229-510-9584','c50h2@empresa.mx',NULL,NULL,'premium','active','2025-08-30 01:00:00','2025-10-28 21:05:45',NULL,9,4),(32,'Jorge Vega','222-341-2684','fhv1x@negocio.mx','wquuy5x',5000654868,'normal','active','2025-10-08 22:00:00','2025-10-28 21:05:45',NULL,11,6),(33,'Carlos Flores','227-746-5961','2vmcq@empresa.mx',NULL,NULL,'normal','active','2025-10-12 17:00:00','2025-10-28 21:05:45',NULL,2,11),(34,'Miguel Castro','226-573-1672','q3xlr@negocio.mx','q349dxb',5000742005,'normal','active','2025-09-14 17:00:00','2025-10-28 21:05:45',NULL,8,9),(35,'María Pérez','225-389-7347','omv2x@empresa.mx',NULL,NULL,'normal','active','2025-10-01 13:00:00','2025-10-28 21:05:45',NULL,7,5),(36,'Farmacia Luna','225-183-3317','7lxxe@empresa.mx',NULL,NULL,'normal','active','2025-09-05 14:00:00','2025-10-28 21:05:45',NULL,6,3),(37,'Raúl Silva','228-195-7937','sal8m@corp.mx',NULL,NULL,'normal','active','2025-09-30 09:00:00','2025-10-28 21:05:45',NULL,3,2),(38,'Sofía Castro','228-138-6517','5wvfg@example.com','fpoyipk',5000784907,'normal','active','2025-10-03 03:00:00','2025-10-28 21:05:45',NULL,4,9),(39,'Lucía Hernández','225-794-8218','qkns8@negocio.mx','ejx5td4',5000892522,'premium','active','2025-09-30 22:00:00','2025-10-28 21:05:45',NULL,2,3),(40,'Sofía López','226-193-4637','357oo@mail.com',NULL,NULL,'normal','active','2025-10-17 02:00:00','2025-10-28 21:05:45',NULL,6,4),(41,'Ferretería Nova','222-240-1627','k3zez@corp.mx','6ahf7vp',5000813885,'normal','active','2025-10-15 05:00:00','2025-10-28 21:05:45',NULL,5,2),(42,'Pedro Silva','229-568-2029','d6vas@negocio.mx','kamugys',5000378130,'premium','active','2025-09-15 20:00:00','2025-10-28 21:05:45',NULL,9,9),(43,'Sofía Ruiz','226-994-8702','bnn0m@empresa.mx',NULL,NULL,'normal','active','2025-08-29 18:00:00','2025-10-28 21:05:45',NULL,11,2),(44,'Raúl Pérez','222-145-6772','t3g2q@corp.mx','3c1qkbh',5000043951,'normal','active','2025-09-22 19:00:00','2025-10-28 21:05:45',NULL,5,9),(45,'Lucía Santos','220-871-4131','k5bxj@mail.com',NULL,NULL,'normal','active','2025-09-27 07:00:00','2025-10-28 21:05:45',NULL,8,7),(46,'Logística Express','225-916-9507','jcpp9@negocio.mx',NULL,NULL,'normal','active','2025-09-06 03:00:00','2025-10-28 21:05:45',NULL,2,6),(47,'Daniela Flores','229-834-7981','fpq06@example.com','j98cwn2',5000712423,'premium','active','2025-09-09 15:00:00','2025-10-28 21:05:45',NULL,1,3),(48,'Lucía Ruiz','222-168-4866','2nnuv@corp.mx','n1utoxi',5000118969,'premium','active','2025-09-15 00:00:00','2025-10-28 21:05:45',NULL,3,8),(49,'Sofía Gómez','224-893-5264','zhwy9@negocio.mx',NULL,NULL,'normal','active','2025-09-02 22:00:00','2025-10-28 21:05:45',NULL,8,3),(50,'Carlos Silva','225-783-6692','ztkkf@negocio.mx','sehe2at',5000386841,'normal','active','2025-09-09 10:00:00','2025-10-28 21:05:45',NULL,9,3),(51,'Ferretería El Molino','226-834-8842','s13c9@empresa.mx',NULL,NULL,'normal','active','2025-08-29 19:00:00','2025-10-28 21:05:45',NULL,6,3),(52,'Elena Mendoza','222-886-3114','p6bef@negocio.mx',NULL,NULL,'normal','active','2025-09-15 03:00:00','2025-10-28 21:05:45',NULL,4,6),(53,'Carlos Santos','223-750-5496','ektsg@example.com',NULL,NULL,'normal','active','2025-09-26 18:00:00','2025-10-28 21:05:45',NULL,12,10),(54,'Ana Ruiz','221-146-5336','x1oxr@example.com',NULL,NULL,'normal','active','2025-09-05 00:00:00','2025-10-28 21:05:45',NULL,8,4),(55,'Daniela Flores','221-805-1981','foqmf@mail.com','49enulq',5000280474,'normal','active','2025-10-15 03:00:00','2025-10-28 21:05:45',NULL,3,2),(56,'Textiles Sigma','226-354-3616','37zgf@example.com',NULL,NULL,'normal','active','2025-10-13 00:00:00','2025-10-28 21:05:45',NULL,8,1),(57,'Sofía Flores','223-320-6781','bkv4y@mail.com',NULL,NULL,'normal','active','2025-10-01 13:00:00','2025-10-28 21:05:45',NULL,7,3),(58,'Jorge Ramírez','225-146-7563','bunkn@corp.mx','k9ye9o2',5000355566,'normal','active','2025-10-05 17:00:00','2025-10-28 21:05:45',NULL,6,3),(59,'Sofía Ramírez','228-141-1742','bz2sf@example.com',NULL,NULL,'normal','active','2025-09-22 17:00:00','2025-10-28 21:05:45',NULL,6,3),(60,'Raúl Santos','229-444-9311','3tzk3@mail.com',NULL,NULL,'premium','active','2025-09-28 13:00:00','2025-10-28 21:05:45',NULL,7,10),(61,'Alimentos Sigma','227-371-4728','zvgww@corp.mx',NULL,NULL,'normal','active','2025-09-04 09:00:00','2025-10-28 21:05:45',NULL,1,10),(62,'Luis Ruiz','227-421-7861','fyo17@empresa.mx','su9rn8q',5000559034,'normal','active','2025-08-29 13:00:00','2025-10-28 21:05:45',NULL,6,11),(63,'Elena Silva','224-724-8932','giui9@mail.com','zyrru7z',5000301779,'premium','active','2025-09-24 00:00:00','2025-10-28 21:05:45',NULL,11,9),(64,'Jorge López','224-143-5712','8c7x0@negocio.mx',NULL,NULL,'normal','active','2025-10-01 08:00:00','2025-10-28 21:05:45',NULL,9,12),(65,'Carlos Mendoza','229-345-4972','b6iid@mail.com','d1at7o7',5000921078,'normal','active','2025-08-31 03:00:00','2025-10-28 21:05:45',NULL,11,4),(66,'Constructora El Molino','220-887-2465','xi04b@negocio.mx',NULL,NULL,'normal','active','2025-08-28 21:00:00','2025-10-28 21:05:45',NULL,1,7),(67,'María Vega','224-997-1613','aud9k@example.com',NULL,NULL,'normal','active','2025-09-19 04:00:00','2025-10-28 21:05:45',NULL,3,9),(68,'Luis Gómez','225-266-8518','xzamk@negocio.mx',NULL,NULL,'normal','active','2025-09-16 02:00:00','2025-10-28 21:05:45',NULL,7,7),(69,'Carlos Ramírez','221-289-3303','r7anq@mail.com','k0axyce',5000321719,'premium','active','2025-09-03 03:00:00','2025-10-28 21:05:45',NULL,11,9),(70,'Raúl Gómez','224-476-4618','hef0v@corp.mx','61231yv',5000825628,'premium','active','2025-09-03 01:00:00','2025-10-28 21:05:45',NULL,8,9),(71,'Ferretería Sigma','221-163-9972','6htf4@corp.mx',NULL,NULL,'premium','active','2025-10-12 20:00:00','2025-10-28 21:05:45',NULL,10,8),(72,'Lucía Ruiz','227-235-9409','ouuyl@empresa.mx',NULL,NULL,'normal','active','2025-09-11 10:00:00','2025-10-28 21:05:45',NULL,12,4),(73,'Ana Ramírez','225-817-2044','tc69q@mail.com',NULL,NULL,'normal','active','2025-09-06 23:00:00','2025-10-28 21:05:45',NULL,11,12),(74,'Jorge Ramírez','227-990-7184','nyxtx@mail.com',NULL,NULL,'normal','active','2025-10-09 13:00:00','2025-10-28 21:05:45',NULL,7,9),(75,'Luis Ruiz','220-405-8585','ytt3i@mail.com',NULL,NULL,'premium','active','2025-10-15 15:00:00','2025-10-28 21:05:45',NULL,12,2),(76,'Textiles Sigma','220-346-4376','cvqy5@negocio.mx','oih5csk',5000855423,'normal','active','2025-09-11 17:00:00','2025-10-28 21:05:45',NULL,10,6),(77,'Elena Pérez','223-409-3347','9soju@example.com','6wpr97y',5000823985,'normal','active','2025-09-22 08:00:00','2025-10-28 21:05:45',NULL,12,7),(78,'Daniela Ramírez','222-872-9813','r4kz3@empresa.mx',NULL,NULL,'normal','active','2025-10-10 00:00:00','2025-10-28 21:05:45',NULL,9,9),(79,'Luis Santos','223-438-2295','74d0g@mail.com',NULL,NULL,'normal','active','2025-10-05 18:00:00','2025-10-28 21:05:45',NULL,1,2),(80,'Raúl Silva','228-322-8854','h6k6h@negocio.mx','e9rivh6',5000578907,'normal','active','2025-09-18 19:00:00','2025-10-28 21:05:45',NULL,5,7),(81,'Constructora El Molino','224-468-9401','5q201@mail.com','nouhfj7',5000607285,'normal','active','2025-10-06 02:00:00','2025-10-28 21:05:45',NULL,5,3),(82,'Luis Ramírez','229-953-5026','rxyj3@corp.mx',NULL,NULL,'normal','active','2025-10-09 13:00:00','2025-10-28 21:05:45',NULL,6,3),(83,'Sofía Flores','222-655-1962','s4c3b@empresa.mx',NULL,NULL,'normal','active','2025-09-03 08:00:00','2025-10-28 21:05:45',NULL,4,2),(84,'Ana Hernández','228-566-7114','cw76x@empresa.mx',NULL,NULL,'normal','active','2025-09-14 13:00:00','2025-10-28 21:05:45',NULL,1,1),(85,'Daniela Castro','224-117-9228','3y36d@empresa.mx',NULL,NULL,'premium','active','2025-10-02 01:00:00','2025-10-28 21:05:45',NULL,10,9),(86,'Café Del Centro','221-482-7652','qizk3@empresa.mx','41dntca',5000179718,'premium','active','2025-08-29 02:00:00','2025-10-28 21:05:45',NULL,7,11),(87,'Miguel Gómez','228-143-4764','h55rb@empresa.mx','ktxg4ah',5000151205,'normal','active','2025-10-14 03:00:00','2025-10-28 21:05:45',NULL,12,7),(88,'María Mendoza','223-680-7375','ytn02@empresa.mx',NULL,NULL,'normal','active','2025-09-21 05:00:00','2025-10-28 21:05:45',NULL,1,2),(89,'Carlos Pérez','229-887-7499','8lw2q@negocio.mx',NULL,NULL,'normal','active','2025-09-04 18:00:00','2025-10-28 21:05:45',NULL,7,3),(90,'Elena Ramírez','221-890-5839','2zcfz@negocio.mx','ldalmje',5000196504,'normal','active','2025-09-15 23:00:00','2025-10-28 21:05:45',NULL,9,9),(91,'Ferretería Del Valle','221-462-2524','v25ao@empresa.mx','u9isygj',5000281454,'normal','active','2025-09-21 04:00:00','2025-10-28 21:05:45',NULL,2,3),(92,'Pedro Santos','227-901-2260','n7zrw@corp.mx',NULL,NULL,'normal','active','2025-09-09 00:00:00','2025-10-28 21:05:45',NULL,7,6),(93,'Jorge Flores','225-540-3230','kvzrg@corp.mx','kzruin3',5000412032,'normal','active','2025-09-10 19:00:00','2025-10-28 21:05:45',NULL,10,4),(94,'María Silva','228-127-8563','7h23c@corp.mx','fkjfpnq',5000626989,'normal','active','2025-09-15 14:00:00','2025-10-28 21:05:45',NULL,7,9),(95,'Pedro Castro','220-909-6890','z3v6d@negocio.mx','mxb9yo1',5000834918,'normal','active','2025-10-02 05:00:00','2025-10-28 21:05:45',NULL,1,2),(96,'Agro Don Paco','228-694-4621','qo1vs@mail.com','rk7d30m',5000359741,'normal','active','2025-09-18 01:00:00','2025-10-28 21:05:45',NULL,4,9),(97,'Lucía Gómez','227-839-8412','lk3e4@empresa.mx','f9igfu8',5000243128,'normal','active','2025-10-06 16:00:00','2025-10-28 21:05:45',NULL,11,3),(98,'Elena Ramírez','226-129-4232','qpahk@empresa.mx',NULL,NULL,'normal','active','2025-09-25 02:00:00','2025-10-28 21:05:45',NULL,9,3),(99,'Luis Flores','221-368-9019','sxvwv@mail.com',NULL,NULL,'normal','active','2025-09-03 03:00:00','2025-10-28 21:05:45',NULL,3,11),(100,'Miguel Mendoza','221-788-3194','lienf@corp.mx',NULL,NULL,'premium','active','2025-10-06 21:00:00','2025-10-28 21:05:45',NULL,7,7),(101,'Agro Luna','228-270-9022','kg4w5@empresa.mx',NULL,NULL,'premium','active','2025-09-15 16:00:00','2025-10-28 21:05:45',NULL,7,9),(102,'Lucía Ramírez','227-525-8272','rcb1k@mail.com',NULL,NULL,'normal','active','2025-08-31 21:00:00','2025-10-28 21:05:45',NULL,8,10),(103,'Sofía Castro','221-686-2871','jt9t1@corp.mx',NULL,NULL,'normal','active','2025-09-07 05:00:00','2025-10-28 21:05:45',NULL,2,12),(104,'Daniela Ruiz','227-369-6711','5d5e3@negocio.mx','vmzwffh',5000217005,'normal','active','2025-09-14 04:00:00','2025-10-28 21:05:45',NULL,10,6),(105,'Miguel Castro','222-431-5794','kj49y@empresa.mx',NULL,NULL,'normal','active','2025-09-30 16:00:00','2025-10-28 21:05:45',NULL,7,1),(106,'Tecnologías Luna','223-249-6277','31yru@mail.com','nc21o0z',5000919943,'normal','active','2025-09-11 12:00:00','2025-10-28 21:05:45',NULL,8,6),(107,'Raúl Gómez','227-750-6869','42o83@corp.mx',NULL,NULL,'normal','active','2025-09-12 08:00:00','2025-10-28 21:05:45',NULL,6,9),(108,'Miguel Flores','225-798-1793','bw4a7@negocio.mx',NULL,NULL,'premium','active','2025-09-04 08:00:00','2025-10-28 21:05:45',NULL,7,4),(109,'Elena Santos','222-995-5489','dmcxx@empresa.mx',NULL,NULL,'normal','active','2025-09-20 16:00:00','2025-10-28 21:05:45',NULL,12,4),(110,'Carlos Vega','221-101-4496','reiya@mail.com','9pecn0d',5000328582,'normal','active','2025-09-24 08:00:00','2025-10-28 21:05:45',NULL,5,3),(111,'Tecnologías La Tuerca','228-676-1138','vfmh0@corp.mx','ph6fe0m',5000450256,'normal','active','2025-09-30 16:00:00','2025-10-28 21:05:45',NULL,3,4),(112,'Carlos Hernández','228-715-5668','2y4xk@example.com','gox22in',5000252802,'normal','active','2025-09-15 12:00:00','2025-10-28 21:05:45',NULL,10,2),(113,'Jorge Pérez','222-496-7895','ny181@empresa.mx',NULL,NULL,'premium','active','2025-10-15 00:00:00','2025-10-28 21:05:45',NULL,4,1),(114,'Sofía Santos','228-885-7806','poxtf@empresa.mx',NULL,NULL,'normal','active','2025-09-14 02:00:00','2025-10-28 21:05:45',NULL,4,3),(115,'Pedro Mendoza','221-417-8167','04cdp@corp.mx','bxxgaea',5000520536,'normal','active','2025-08-28 13:00:00','2025-10-28 21:05:45',NULL,9,9),(116,'Café Luna','225-229-5403','0e6mp@example.com',NULL,NULL,'normal','active','2025-10-13 21:00:00','2025-10-28 21:05:45',NULL,10,11),(117,'Lucía Castro','225-156-9185','4gf16@empresa.mx',NULL,NULL,'normal','active','2025-10-03 11:00:00','2025-10-28 21:05:45',NULL,1,1),(118,'Lucía Pérez','226-253-3932','74t60@corp.mx',NULL,NULL,'premium','active','2025-10-01 10:00:00','2025-10-28 21:05:45',NULL,12,6),(119,'Miguel Pérez','221-614-1862','g298c@corp.mx','1ldqnk2',5000775511,'normal','active','2025-09-10 21:00:00','2025-10-28 21:05:45',NULL,8,6),(120,'Luis Vega','228-878-5016','f7atw@empresa.mx','ax40dti',5000515939,'normal','active','2025-10-01 10:00:00','2025-10-28 21:05:45',NULL,3,12),(121,'María',NULL,'maria@example.com',NULL,NULL,'normal','active','2025-10-31 14:32:36','2025-10-31 20:32:36',NULL,NULL,NULL),(126,'María López',NULL,'maria+1@example.com',NULL,NULL,'normal','active','2025-10-31 14:38:27','2025-10-31 20:38:27',NULL,NULL,NULL);
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conversation`
--

DROP TABLE IF EXISTS `conversation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conversation` (
  `conversation_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) DEFAULT NULL,
  `channel` enum('web','telegram','whatsapp','sms','email','other') NOT NULL DEFAULT 'web',
  `external_chat_id` varchar(128) DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT 1,
  `handled_by_bot` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `last_message_at` datetime DEFAULT NULL,
  PRIMARY KEY (`conversation_id`),
  UNIQUE KEY `uq_conv_channel_ext` (`channel`,`external_chat_id`),
  KEY `idx_conversation_client` (`client_id`),
  KEY `idx_conversation_lastmsg` (`last_message_at`),
  CONSTRAINT `fk_conv_client` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conversation`
--

LOCK TABLES `conversation` WRITE;
/*!40000 ALTER TABLE `conversation` DISABLE KEYS */;
INSERT INTO `conversation` VALUES (1,110,'telegram','tg-500000000',1,0,'2025-10-22 16:00:00','2025-10-28 21:05:45','2025-10-14 09:15:00'),(2,53,'other',NULL,1,0,'2025-10-14 15:00:00','2025-10-28 21:05:45','2025-10-24 13:48:00'),(3,2,'email','thr-6xvaj2k8xp',1,1,'2025-10-23 06:00:00','2025-10-28 21:05:45','2025-10-23 13:37:00'),(4,60,'whatsapp','5215579878835',0,1,'2025-10-26 12:00:00','2025-10-28 21:05:45','2025-10-24 02:20:00'),(5,66,'whatsapp','5215585357498',1,0,'2025-10-22 15:00:00','2025-10-28 21:05:45','2025-10-26 20:04:00'),(6,14,'email','thr-c9x5jz6kf1',0,0,'2025-10-14 17:00:00','2025-10-28 21:05:45','2025-10-25 15:25:00'),(7,52,'whatsapp','5215528781020',0,0,'2025-10-23 04:00:00','2025-10-28 21:05:45','2025-10-21 15:02:00'),(8,117,'email','thr-o0u93mzywr',0,1,'2025-10-23 07:00:00','2025-10-28 21:05:45','2025-10-15 07:04:00'),(9,108,'other',NULL,1,1,'2025-10-24 13:00:00','2025-10-28 21:05:45','2025-10-27 09:35:00'),(10,34,'other',NULL,0,1,'2025-10-17 02:00:00','2025-10-28 21:05:45','2025-10-24 15:49:00'),(11,84,'web',NULL,1,1,'2025-10-14 03:00:00','2025-10-28 21:05:45','2025-10-28 04:21:00'),(12,54,'whatsapp','5215559886371',1,1,'2025-10-14 09:00:00','2025-10-28 21:05:45','2025-10-23 17:38:00'),(13,61,'web',NULL,0,1,'2025-10-18 10:00:00','2025-10-28 21:05:45','2025-10-16 06:26:00'),(14,61,'telegram','tg-500000013',1,0,'2025-10-20 20:00:00','2025-10-28 21:05:45','2025-10-18 16:46:00'),(15,39,'email','thr-b4ehou6qlz',0,1,'2025-10-17 07:00:00','2025-10-28 21:05:45','2025-10-21 08:27:00'),(16,41,'web',NULL,1,1,'2025-10-15 07:00:00','2025-10-28 21:05:45','2025-10-22 23:32:00'),(17,74,'telegram','tg-500000016',1,0,'2025-10-26 08:00:00','2025-10-28 21:05:45','2025-10-25 13:46:00'),(18,79,'email','thr-wo8nbhnal3',1,0,'2025-10-16 13:00:00','2025-10-28 21:05:45','2025-10-21 20:12:00'),(19,32,'telegram','tg-500000018',1,1,'2025-10-25 09:00:00','2025-10-28 21:05:45','2025-10-14 07:07:00'),(20,50,'other',NULL,1,1,'2025-10-14 11:00:00','2025-10-28 21:05:45','2025-10-14 11:34:00'),(21,39,'whatsapp','5215571193393',0,1,'2025-10-21 23:00:00','2025-10-28 21:05:45','2025-10-24 08:02:00'),(22,114,'telegram','tg-500000021',1,0,'2025-10-22 06:00:00','2025-10-28 21:05:45','2025-10-13 16:13:00'),(23,22,'email','thr-ai9hasez2n',1,0,'2025-10-18 11:00:00','2025-10-28 21:05:45','2025-10-18 04:59:00'),(24,77,'web',NULL,1,0,'2025-10-27 11:00:00','2025-10-28 21:05:45','2025-10-26 03:42:00'),(25,89,'web',NULL,1,1,'2025-10-19 04:00:00','2025-10-28 21:05:45','2025-10-20 04:10:00'),(26,61,'telegram','tg-500000025',1,0,'2025-10-27 03:00:00','2025-10-28 21:05:45','2025-10-15 14:28:00'),(27,54,'web',NULL,1,1,'2025-10-17 14:00:00','2025-10-28 21:05:45','2025-10-14 01:41:00'),(28,18,'email','thr-3dzeedhhjs',1,0,'2025-10-23 07:00:00','2025-10-28 21:05:45','2025-10-14 13:30:00'),(29,6,'other',NULL,1,1,'2025-10-20 02:00:00','2025-10-28 21:05:45','2025-10-18 13:07:00'),(30,31,'web',NULL,1,1,'2025-10-25 18:00:00','2025-10-28 21:05:45','2025-10-16 22:05:00'),(31,86,'email','thr-fds0dji9kq',1,1,'2025-10-27 03:00:00','2025-10-28 21:05:45','2025-10-19 09:54:00'),(32,47,'whatsapp','5215567176108',0,1,'2025-10-15 11:00:00','2025-10-28 21:05:45','2025-10-16 10:22:00'),(33,2,'telegram','tg-500000032',1,1,'2025-10-21 22:00:00','2025-10-28 21:05:45','2025-10-13 20:51:00'),(34,80,'whatsapp','5215522475714',1,1,'2025-10-26 00:00:00','2025-10-28 21:05:45','2025-10-28 07:40:00'),(35,52,'email','thr-jn42x2ezc7',1,1,'2025-10-17 21:00:00','2025-10-28 21:05:45','2025-10-22 00:30:00'),(36,103,'other',NULL,1,1,'2025-10-21 01:00:00','2025-10-28 21:05:45','2025-10-26 18:06:00'),(37,79,'web',NULL,0,0,'2025-10-16 08:00:00','2025-10-28 21:05:45','2025-10-27 12:54:00'),(38,62,'email','thr-eobjlzy1uu',0,0,'2025-10-21 20:00:00','2025-10-28 21:05:45','2025-10-18 07:09:00'),(39,67,'other',NULL,1,0,'2025-10-23 21:00:00','2025-10-28 21:05:45','2025-10-25 20:33:00'),(40,45,'email','thr-f36wa7sqrf',0,1,'2025-10-22 04:00:00','2025-10-28 21:05:45','2025-10-14 21:46:00'),(41,7,'other',NULL,1,0,'2025-10-21 05:00:00','2025-10-28 21:05:45','2025-10-16 18:28:00'),(42,11,'email','thr-pudrl90aob',1,0,'2025-10-14 17:00:00','2025-10-28 21:05:45','2025-10-16 02:43:00'),(43,80,'whatsapp','5215578227936',1,0,'2025-10-20 02:00:00','2025-10-28 21:05:45','2025-10-17 02:30:00'),(44,47,'web',NULL,0,0,'2025-10-21 19:00:00','2025-10-28 21:05:45','2025-10-25 07:28:00'),(45,99,'other',NULL,1,0,'2025-10-21 14:00:00','2025-10-28 21:05:45','2025-10-27 16:28:00'),(46,58,'web',NULL,1,0,'2025-10-27 02:00:00','2025-10-28 21:05:45','2025-10-15 12:21:00'),(47,46,'whatsapp','5215583509785',1,0,'2025-10-27 07:00:00','2025-10-28 21:05:45','2025-10-15 01:55:00'),(48,64,'telegram','tg-500000047',0,0,'2025-10-21 09:00:00','2025-10-28 21:05:45','2025-10-20 13:55:00'),(49,33,'other',NULL,1,1,'2025-10-14 00:00:00','2025-10-28 21:05:45','2025-10-15 15:24:00'),(50,28,'email','thr-3gm1bwye6q',1,1,'2025-10-20 12:00:00','2025-10-28 21:05:45','2025-10-24 00:38:00'),(51,68,'web',NULL,1,1,'2025-10-17 21:00:00','2025-10-28 21:05:45','2025-10-21 06:48:00'),(52,119,'other',NULL,0,0,'2025-10-15 18:00:00','2025-10-28 21:05:45','2025-10-15 04:32:00'),(53,23,'telegram','tg-500000052',1,0,'2025-10-18 02:00:00','2025-10-28 21:05:45','2025-10-23 02:45:00'),(54,65,'email','thr-pvyiomk2ev',0,1,'2025-10-13 14:00:00','2025-10-28 21:05:45','2025-10-16 21:42:00'),(55,71,'whatsapp','5215584300459',1,1,'2025-10-17 14:00:00','2025-10-28 21:05:45','2025-10-13 22:52:00'),(56,38,'whatsapp','5215527806897',0,0,'2025-10-24 20:00:00','2025-10-28 21:05:45','2025-10-24 14:49:00'),(57,70,'whatsapp','5215525489430',0,1,'2025-10-17 18:00:00','2025-10-28 21:05:45','2025-10-25 21:58:00'),(58,86,'email','thr-y6t5padnbc',1,0,'2025-10-22 15:00:00','2025-10-28 21:05:45','2025-10-18 09:28:00'),(59,33,'telegram','tg-500000058',0,0,'2025-10-23 06:00:00','2025-10-28 21:05:45','2025-10-25 18:18:00'),(60,97,'other',NULL,1,0,'2025-10-25 17:00:00','2025-10-28 21:05:45','2025-10-26 00:50:00'),(61,112,'other',NULL,0,0,'2025-10-19 00:00:00','2025-10-28 21:05:45','2025-10-15 08:37:00'),(62,31,'other',NULL,0,0,'2025-10-22 14:00:00','2025-10-28 21:05:45','2025-10-20 00:39:00'),(63,86,'web',NULL,0,1,'2025-10-14 15:00:00','2025-10-28 21:05:45','2025-10-26 23:32:00'),(64,41,'other',NULL,1,0,'2025-10-23 17:00:00','2025-10-28 21:05:45','2025-10-15 17:23:00'),(65,112,'email','thr-36zx1tv18k',1,0,'2025-10-25 07:00:00','2025-10-28 21:05:45','2025-10-26 11:21:00'),(66,95,'other',NULL,1,1,'2025-10-22 19:00:00','2025-10-28 21:05:45','2025-10-19 11:06:00'),(67,34,'telegram','tg-500000066',1,0,'2025-10-27 02:00:00','2025-10-28 21:05:45','2025-10-25 02:18:00'),(68,60,'telegram','tg-500000067',1,0,'2025-10-18 11:00:00','2025-10-28 21:05:45','2025-10-16 18:16:00'),(69,100,'other',NULL,0,1,'2025-10-14 18:00:00','2025-10-28 21:05:45','2025-10-19 00:09:00'),(70,71,'whatsapp','5215519781894',0,1,'2025-10-24 07:00:00','2025-10-28 21:05:45','2025-10-23 20:26:00'),(71,67,'web',NULL,0,1,'2025-10-18 19:00:00','2025-10-28 21:05:45','2025-10-16 18:08:00'),(72,52,'web',NULL,1,0,'2025-10-17 02:00:00','2025-10-28 21:05:45','2025-10-16 05:52:00'),(73,43,'whatsapp','5215549402883',1,0,'2025-10-18 21:00:00','2025-10-28 21:05:45','2025-10-23 22:15:00'),(74,72,'web',NULL,1,1,'2025-10-23 16:00:00','2025-10-28 21:05:45','2025-10-27 17:30:00'),(75,79,'other',NULL,1,1,'2025-10-22 00:00:00','2025-10-28 21:05:45','2025-10-24 12:12:00'),(76,118,'web',NULL,1,1,'2025-10-23 12:00:00','2025-10-28 21:05:45','2025-10-18 00:59:00'),(77,117,'other',NULL,0,1,'2025-10-14 20:00:00','2025-10-28 21:05:45','2025-10-24 22:14:00'),(78,58,'email','thr-b6gs8g8tac',1,0,'2025-10-13 15:00:00','2025-10-28 21:05:45','2025-10-21 23:21:00'),(79,55,'web',NULL,1,0,'2025-10-15 23:00:00','2025-10-28 21:05:45','2025-10-20 04:55:00'),(80,83,'web',NULL,0,1,'2025-10-19 14:00:00','2025-10-28 21:05:45','2025-10-20 02:49:00'),(81,40,'web',NULL,1,1,'2025-10-28 16:59:33','2025-10-28 22:59:33','2025-10-28 16:59:33');
/*!40000 ALTER TABLE `conversation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_order`
--

DROP TABLE IF EXISTS `customer_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_order` (
  `order_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `status` enum('borrador','confirmado','preparando','enviado','entregado','cancelado','devuelto') NOT NULL DEFAULT 'borrador',
  `payment_status` enum('pendiente','pagado','reembolsado','fallido') NOT NULL DEFAULT 'pendiente',
  `subtotal` decimal(12,2) NOT NULL DEFAULT 0.00 CHECK (`subtotal` >= 0),
  `discount_total` decimal(12,2) NOT NULL DEFAULT 0.00 CHECK (`discount_total` >= 0),
  `tax_total` decimal(12,2) NOT NULL DEFAULT 0.00 CHECK (`tax_total` >= 0),
  `shipping_total` decimal(12,2) NOT NULL DEFAULT 0.00 CHECK (`shipping_total` >= 0),
  `grand_total` decimal(12,2) GENERATED ALWAYS AS (round(`subtotal` - `discount_total` + `tax_total` + `shipping_total`,2)) STORED,
  `notes` text DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  KEY `fk_order_created_by` (`created_by`),
  KEY `fk_order_updated_by` (`updated_by`),
  KEY `idx_order_client_created` (`client_id`,`created_at`),
  KEY `idx_order_status_payment` (`status`,`payment_status`),
  KEY `idx_order_updated_at` (`updated_at`),
  CONSTRAINT `fk_order_client` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_order_created_by` FOREIGN KEY (`created_by`) REFERENCES `app_user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_order_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `app_user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_order`
--

LOCK TABLES `customer_order` WRITE;
/*!40000 ALTER TABLE `customer_order` DISABLE KEYS */;
INSERT INTO `customer_order` VALUES (1,64,'2025-10-20 17:00:00','2025-10-28 21:05:45','enviado','pendiente',52768.40,719.36,8327.85,0.00,60376.89,'Pedido por WhatsApp',10,NULL),(2,45,'2025-10-21 01:00:00','2025-10-28 21:05:45','enviado','pagado',25512.63,913.47,3935.86,0.00,28535.02,'Compra en tienda',6,NULL),(3,35,'2025-10-15 21:00:00','2025-10-28 21:05:45','entregado','pendiente',16485.26,1648.53,2373.88,0.00,17210.61,'Pedido por feria comercial',1,NULL),(4,44,'2025-10-18 15:00:00','2025-10-28 21:05:45','preparando','pagado',20273.60,1013.68,3081.59,0.00,22341.51,'Pedido por WhatsApp',8,NULL),(5,7,'2025-10-18 00:00:00','2025-10-28 21:05:45','enviado','pendiente',8400.21,0.00,1344.03,0.00,9744.24,'Pedido vía web',5,NULL),(6,27,'2025-10-25 16:00:00','2025-10-28 21:05:45','confirmado','pendiente',27260.46,827.00,4229.36,0.00,30662.82,'Pedido por WhatsApp',6,NULL),(7,74,'2025-10-23 15:00:00','2025-10-28 21:05:45','entregado','pagado',142061.10,3739.73,22131.43,0.00,160452.80,'Pedido corporativo',8,NULL),(8,53,'2025-10-25 16:00:00','2025-10-28 21:05:45','confirmado','pendiente',71066.16,3148.22,10866.87,0.00,78784.81,'Pedido vía web',6,NULL),(9,72,'2025-10-20 16:00:00','2025-10-28 21:05:45','entregado','pagado',27078.23,0.00,4332.52,0.00,31410.75,'Compra en tienda',7,NULL),(10,8,'2025-10-21 17:00:00','2025-10-28 21:05:45','enviado','pendiente',34068.22,0.00,5450.92,0.00,39519.14,'Pedido por WhatsApp',2,NULL),(11,15,'2025-10-15 20:00:00','2025-10-28 21:05:45','confirmado','pagado',22029.79,1978.06,3208.28,0.00,23260.01,'Compra en tienda',10,NULL),(12,53,'2025-10-18 11:00:00','2025-10-28 21:05:45','enviado','pagado',99987.18,2655.04,15573.14,0.00,112905.28,'Pedido corporativo',5,NULL),(13,108,'2025-10-17 11:00:00','2025-10-28 21:05:45','enviado','pendiente',101739.27,0.00,16278.28,0.00,118017.55,'Pedido vía web',12,NULL),(14,118,'2025-10-17 02:00:00','2025-10-28 21:05:45','preparando','pagado',12131.06,606.55,1843.92,0.00,13368.43,'Pedido corporativo',8,NULL),(15,106,'2025-10-16 04:00:00','2025-10-28 21:05:45','preparando','pendiente',49978.52,4997.85,7196.91,0.00,52177.58,'Pedido por feria comercial',3,NULL),(16,1,'2025-10-23 16:00:00','2025-10-28 21:05:45','entregado','pagado',78247.43,2280.09,12154.78,0.00,88122.12,'Pedido por WhatsApp',7,NULL),(17,11,'2025-10-22 07:00:00','2025-10-28 21:05:45','entregado','pagado',62061.32,1224.66,9733.86,0.00,70570.52,'Pedido corporativo',7,NULL),(18,77,'2025-10-25 10:00:00','2025-10-28 21:05:45','enviado','pendiente',38880.00,2367.95,5841.93,0.00,42353.98,'Pedido por WhatsApp',5,NULL),(19,17,'2025-10-23 17:00:00','2025-10-28 21:05:45','entregado','pendiente',45208.25,0.00,7233.32,0.00,52441.57,'Pedido vía web',7,NULL),(20,18,'2025-10-16 00:00:00','2025-10-28 21:05:45','confirmado','pendiente',36135.79,570.36,5690.47,0.00,41255.90,'Pedido vía web',6,NULL),(21,33,'2025-10-18 00:00:00','2025-10-28 21:05:45','confirmado','pagado',127328.83,2555.12,19963.79,0.00,144737.50,'Pedido por WhatsApp',9,NULL),(22,17,'2025-10-22 13:00:00','2025-10-28 21:05:45','enviado','pagado',124360.15,115.48,19879.14,0.00,144123.81,'Pedido por WhatsApp',8,NULL),(23,5,'2025-10-23 07:00:00','2025-10-28 21:05:45','preparando','pagado',106470.61,6660.01,15969.70,0.00,115780.30,'Pedido corporativo',8,NULL),(24,75,'2025-10-18 18:00:00','2025-10-28 21:05:45','confirmado','pagado',67814.04,0.00,10850.25,0.00,78664.29,'Pedido vía web',1,NULL),(25,59,'2025-10-16 21:00:00','2025-10-28 21:05:45','confirmado','pendiente',68925.96,2274.97,10664.15,0.00,77315.14,'Pedido corporativo',12,NULL),(26,71,'2025-10-21 10:00:00','2025-10-28 21:05:45','confirmado','pagado',17033.42,270.54,2682.05,0.00,19444.93,'Pedido corporativo',10,NULL),(27,86,'2025-10-21 20:00:00','2025-10-28 21:05:45','entregado','pagado',49374.26,4292.96,7213.02,0.00,52294.32,'Pedido vía web',2,NULL),(28,60,'2025-10-23 16:00:00','2025-10-28 21:05:45','enviado','pagado',125801.04,2041.60,19801.51,0.00,143560.95,'Pedido vía web',11,NULL),(29,73,'2025-10-19 10:00:00','2025-10-28 21:05:45','enviado','pendiente',35532.84,1776.64,5400.99,0.00,39157.19,'Compra en tienda',1,NULL),(30,75,'2025-10-19 12:00:00','2025-10-28 21:05:45','enviado','pendiente',133465.54,6416.27,20327.88,0.00,147377.15,'Compra en tienda',2,NULL),(31,56,'2025-10-27 12:00:00','2025-10-28 21:05:45','entregado','pagado',17609.92,880.50,2676.71,0.00,19406.13,'Pedido corporativo',9,NULL),(32,80,'2025-10-21 14:00:00','2025-10-28 21:05:45','preparando','pagado',49884.02,0.00,7981.45,0.00,57865.47,'Pedido corporativo',10,NULL),(33,39,'2025-10-24 21:00:00','2025-10-28 21:05:45','enviado','pagado',15200.57,0.00,2432.09,0.00,17632.66,'Pedido corporativo',8,NULL),(34,7,'2025-10-27 09:00:00','2025-10-28 21:05:45','preparando','pagado',149104.45,12789.01,21810.48,0.00,158125.92,'Pedido corporativo',6,NULL),(35,55,'2025-10-21 19:00:00','2025-10-28 21:05:45','confirmado','pendiente',107892.56,3275.59,16738.72,0.00,121355.69,'Compra en tienda',10,NULL),(36,61,'2025-10-20 05:00:00','2025-10-28 21:05:45','enviado','pagado',122586.09,3040.20,19127.34,0.00,138673.23,'Pedido por feria comercial',6,NULL),(37,103,'2025-10-18 06:00:00','2025-10-28 21:05:45','preparando','pagado',15166.48,0.00,2426.64,0.00,17593.12,'Pedido por WhatsApp',3,NULL),(38,64,'2025-10-24 06:00:00','2025-10-28 21:05:45','preparando','pendiente',7193.58,0.00,1150.97,0.00,8344.55,'Pedido por feria comercial',5,NULL),(39,44,'2025-10-25 17:00:00','2025-10-28 21:05:45','enviado','pagado',8158.96,407.95,1240.16,0.00,8991.17,'Pedido vía web',7,NULL),(40,110,'2025-10-18 17:00:00','2025-10-28 21:05:45','preparando','pendiente',49863.10,2493.16,7579.19,0.00,54949.13,'Compra en tienda',12,NULL),(41,40,'0000-00-00 00:00:00','2025-10-28 22:59:33','confirmado','pagado',10639.21,0.00,1702.27,0.00,12341.48,'Pedido creado desde main.py',NULL,NULL),(42,126,'2025-10-31 14:38:47','2025-10-31 20:38:47','borrador','pendiente',0.00,0.00,0.00,0.00,0.00,NULL,NULL,NULL);
/*!40000 ALTER TABLE `customer_order` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_order_require_invoice
BEFORE UPDATE ON customer_order
FOR EACH ROW
BEGIN
  IF NEW.status IN ('confirmado','preparando','enviado','entregado','devuelto') THEN
    IF (SELECT COUNT(*) FROM invoice WHERE order_id = NEW.order_id) = 0 THEN
      SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El pedido requiere al menos una factura para cambiar a ese estado.';
    END IF;
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `invoice`
--

DROP TABLE IF EXISTS `invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `invoice` (
  `invoice_id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL,
  `invoice_number` varchar(40) NOT NULL,
  `series` varchar(10) DEFAULT NULL,
  `issued_at` datetime NOT NULL DEFAULT current_timestamp(),
  `due_at` datetime DEFAULT NULL,
  `currency_code` char(3) NOT NULL DEFAULT 'MXN',
  `status` enum('emitida','pagada','parcial','cancelada') NOT NULL DEFAULT 'emitida',
  `notes` text DEFAULT NULL,
  PRIMARY KEY (`invoice_id`),
  UNIQUE KEY `uq_invoice_order_number` (`order_id`,`invoice_number`),
  KEY `idx_invoice_issued_at` (`issued_at`),
  KEY `idx_invoice_number` (`invoice_number`),
  CONSTRAINT `fk_invoice_order` FOREIGN KEY (`order_id`) REFERENCES `customer_order` (`order_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice`
--

LOCK TABLES `invoice` WRITE;
/*!40000 ALTER TABLE `invoice` DISABLE KEYS */;
INSERT INTO `invoice` VALUES (1,1,'INV-2025-0001','C','2025-10-22 00:00:00',NULL,'MXN','emitida','Crédito a 15 días'),(2,2,'INV-2025-0002A','A','2025-10-22 07:00:00',NULL,'MXN','emitida','Anticipo del 50%'),(3,2,'INV-2025-0002B','A','2025-10-19 15:00:00',NULL,'MXN','pagada','Crédito a 15 días'),(4,3,'INV-2025-0003','C','2025-10-25 21:00:00',NULL,'MXN','emitida','Pago en efectivo'),(5,4,'INV-2025-0004','A','2025-10-19 06:00:00',NULL,'MXN','pagada','Anticipo del 50%'),(6,5,'INV-2025-0005','B','2025-10-25 18:00:00',NULL,'MXN','pagada','Crédito a 15 días'),(7,6,'INV-2025-0006','C','2025-10-19 07:00:00',NULL,'MXN','emitida','Pago en efectivo'),(8,7,'INV-2025-0007','A','2025-10-24 08:00:00',NULL,'MXN','pagada','Crédito a 15 días'),(9,8,'INV-2025-0008','A','2025-10-24 03:00:00',NULL,'MXN','pagada','Crédito a 15 días'),(10,9,'INV-2025-0009','A','2025-10-26 13:00:00',NULL,'MXN','pagada','Pago vía SPEI'),(11,10,'INV-2025-0010','A','2025-10-20 13:00:00',NULL,'MXN','emitida','Pago en efectivo'),(12,11,'INV-2025-0011A','C','2025-10-23 23:00:00',NULL,'MXN','emitida','Pago en efectivo'),(13,11,'INV-2025-0011B','A','2025-10-25 06:00:00',NULL,'MXN','pagada','Crédito a 15 días'),(14,12,'INV-2025-0012','C','2025-10-22 03:00:00',NULL,'MXN','emitida','Pago vía SPEI'),(15,13,'INV-2025-0013A','B','2025-10-27 00:00:00',NULL,'MXN','pagada','Anticipo del 50%'),(16,13,'INV-2025-0013B','A','2025-10-24 03:00:00',NULL,'MXN','emitida','Pago en efectivo'),(17,14,'INV-2025-0014','B','2025-10-21 14:00:00',NULL,'MXN','pagada','Pago vía SPEI'),(18,15,'INV-2025-0015A','C','2025-10-21 22:00:00',NULL,'MXN','emitida','Pago vía SPEI'),(19,15,'INV-2025-0015B','C','2025-10-24 16:00:00',NULL,'MXN','pagada','Pago en efectivo'),(20,16,'INV-2025-0016A','B','2025-10-19 21:00:00',NULL,'MXN','emitida','Anticipo del 50%'),(21,16,'INV-2025-0016B','A','2025-10-18 02:00:00',NULL,'MXN','pagada','Pago en efectivo'),(22,17,'INV-2025-0017','C','2025-10-25 11:00:00',NULL,'MXN','pagada','Crédito a 15 días'),(23,18,'INV-2025-0018A','B','2025-10-26 05:00:00',NULL,'MXN','emitida','Pago en efectivo'),(24,18,'INV-2025-0018B','B','2025-10-22 13:00:00',NULL,'MXN','pagada','Crédito a 15 días'),(25,19,'INV-2025-0019A','A','2025-10-17 22:00:00',NULL,'MXN','emitida','Anticipo del 50%'),(26,19,'INV-2025-0019B','C','2025-10-20 10:00:00',NULL,'MXN','emitida','Crédito a 15 días'),(27,20,'INV-2025-0020','B','2025-10-17 15:00:00',NULL,'MXN','emitida','Pago vía SPEI'),(28,21,'INV-2025-0021A','B','2025-10-25 10:00:00',NULL,'MXN','pagada','Crédito a 15 días'),(29,21,'INV-2025-0021B','A','2025-10-23 09:00:00',NULL,'MXN','pagada','Pago vía SPEI'),(30,22,'INV-2025-0022A','A','2025-10-18 15:00:00',NULL,'MXN','pagada','Pago vía SPEI'),(31,22,'INV-2025-0022B','A','2025-10-25 11:00:00',NULL,'MXN','emitida','Pago en efectivo'),(32,23,'INV-2025-0023A','A','2025-10-26 01:00:00',NULL,'MXN','emitida','Pago en efectivo'),(33,23,'INV-2025-0023B','B','2025-10-25 07:00:00',NULL,'MXN','pagada','Pago en efectivo'),(34,24,'INV-2025-0024','A','2025-10-22 08:00:00',NULL,'MXN','emitida','Pago vía SPEI'),(35,25,'INV-2025-0025A','C','2025-10-18 08:00:00',NULL,'MXN','emitida','Pago vía SPEI'),(36,25,'INV-2025-0025B','C','2025-10-23 02:00:00',NULL,'MXN','emitida','Pago vía SPEI'),(37,26,'INV-2025-0026A','B','2025-10-25 09:00:00',NULL,'MXN','pagada','Crédito a 15 días'),(38,26,'INV-2025-0026B','B','2025-10-22 15:00:00',NULL,'MXN','emitida','Anticipo del 50%'),(39,27,'INV-2025-0027','C','2025-10-21 10:00:00',NULL,'MXN','emitida','Anticipo del 50%'),(40,28,'INV-2025-0028','B','2025-10-23 20:00:00',NULL,'MXN','pagada','Anticipo del 50%'),(41,29,'INV-2025-0029','C','2025-10-18 04:00:00',NULL,'MXN','pagada','Anticipo del 50%'),(42,30,'INV-2025-0030A','B','2025-10-18 04:00:00',NULL,'MXN','pagada','Pago en efectivo'),(43,30,'INV-2025-0030B','A','2025-10-25 10:00:00',NULL,'MXN','pagada','Pago vía SPEI'),(44,31,'INV-2025-0031','B','2025-10-17 13:00:00',NULL,'MXN','pagada','Anticipo del 50%'),(45,32,'INV-2025-0032','A','2025-10-23 23:00:00',NULL,'MXN','emitida','Pago vía SPEI'),(46,33,'INV-2025-0033A','B','2025-10-19 21:00:00',NULL,'MXN','emitida','Crédito a 15 días'),(47,33,'INV-2025-0033B','C','2025-10-24 06:00:00',NULL,'MXN','pagada','Crédito a 15 días'),(48,34,'INV-2025-0034','C','2025-10-20 05:00:00',NULL,'MXN','emitida','Pago vía SPEI'),(49,35,'INV-2025-0035','B','2025-10-27 07:00:00',NULL,'MXN','pagada','Pago en efectivo'),(50,36,'INV-2025-0036','B','2025-10-20 23:00:00',NULL,'MXN','pagada','Crédito a 15 días'),(51,37,'INV-2025-0037','A','2025-10-17 21:00:00',NULL,'MXN','emitida','Crédito a 15 días'),(52,38,'INV-2025-0038','A','2025-10-24 20:00:00',NULL,'MXN','emitida','Pago vía SPEI'),(53,39,'INV-2025-0039','B','2025-10-22 11:00:00',NULL,'MXN','pagada','Pago en efectivo'),(54,40,'INV-2025-0040A','A','2025-10-25 17:00:00',NULL,'MXN','emitida','Pago vía SPEI'),(55,40,'INV-2025-0040B','C','2025-10-26 07:00:00',NULL,'MXN','emitida','Pago en efectivo'),(56,41,'INV-MAIN-0041','A','0000-00-00 00:00:00',NULL,'MXN','emitida','Factura generada desde main.py');
/*!40000 ALTER TABLE `invoice` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_invoice_before_delete
BEFORE DELETE ON invoice
FOR EACH ROW
BEGIN
  DECLARE v_status VARCHAR(20);
  DECLARE v_count  INT;

  SELECT status INTO v_status
  FROM customer_order
  WHERE order_id = OLD.order_id
  FOR UPDATE;

  SELECT COUNT(*) INTO v_count
  FROM invoice
  WHERE order_id = OLD.order_id;

  IF v_count = 1 AND v_status NOT IN ('borrador','cancelado') THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'No puedes eliminar la última factura de un pedido activo.';
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `message` (
  `message_id` int(11) NOT NULL AUTO_INCREMENT,
  `conversation_id` int(11) NOT NULL,
  `sender` enum('client','user','bot') NOT NULL,
  `content` mediumtext NOT NULL,
  `external_message_id` varchar(128) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`message_id`),
  UNIQUE KEY `uq_msg_conv_ext` (`conversation_id`,`external_message_id`),
  KEY `idx_message_created_at` (`created_at`),
  CONSTRAINT `fk_msg_conversation` FOREIGN KEY (`conversation_id`) REFERENCES `conversation` (`conversation_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=403 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES (1,43,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-27 10:49:00'),(2,33,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-jnwpaytx','2025-10-26 17:08:00'),(3,80,'client','¿Aceptan pago con transferencia?',NULL,'2025-10-19 10:16:00'),(4,10,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-27 02:10:00'),(5,39,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-27 02:12:00'),(6,57,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-14 14:59:00'),(7,61,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-25 07:13:00'),(8,51,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-23 15:51:00'),(9,39,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-13 12:19:00'),(10,48,'client','¿Cuál es el tiempo de garantía?','te-m-avt8k06m','2025-10-14 18:51:00'),(11,53,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-h4gg2447','2025-10-14 19:51:00'),(12,71,'user','Sí, te envío CLABE por DM.',NULL,'2025-10-20 09:42:00'),(13,9,'user','Con gusto, ¿qué producto requiere?',NULL,'2025-10-24 12:23:00'),(14,63,'user','Sí, en CDMX y Puebla mismo día.',NULL,'2025-10-25 14:19:00'),(15,31,'client','¿Manejan entregas el mismo día?','em-m-rlxyfu38','2025-10-19 09:03:00'),(16,22,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-25 04:15:00'),(17,56,'user','Sí, en CDMX y Puebla mismo día.',NULL,'2025-10-25 14:14:00'),(18,43,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-21 00:11:00'),(19,40,'user','Garantía de 12 meses con fabricante.','em-m-44ftj5cc','2025-10-27 06:19:00'),(20,3,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','em-m-ov6tt9q1','2025-10-18 11:08:00'),(21,47,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-13 17:14:00'),(22,38,'client','Necesito factura, por favor.','em-m-sx43wfsq','2025-10-19 19:55:00'),(23,23,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-18 14:05:00'),(24,62,'user','Con gusto, ¿qué producto requiere?',NULL,'2025-10-24 20:46:00'),(25,9,'user','Sí, en CDMX y Puebla mismo día.',NULL,'2025-10-25 10:18:00'),(26,27,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-14 00:36:00'),(27,61,'user','Con gusto, ¿qué producto requiere?',NULL,'2025-10-27 15:40:00'),(28,14,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-0uunnv6c','2025-10-19 15:07:00'),(29,33,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-19 23:38:00'),(30,45,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-13 17:00:00'),(31,65,'client','Necesito factura, por favor.','em-m-kffv3xol','2025-10-26 04:56:00'),(32,15,'user','Sí, te envío CLABE por DM.','em-m-xoieves6','2025-10-20 20:47:00'),(33,19,'client','Tengo problemas con mi impresora.',NULL,'2025-10-24 06:27:00'),(34,77,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-18 11:04:00'),(35,37,'client','Tengo problemas con mi impresora.',NULL,'2025-10-20 16:30:00'),(36,62,'client','Tengo problemas con mi impresora.',NULL,'2025-10-14 22:22:00'),(37,19,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-j0mqvind','2025-10-15 06:21:00'),(38,26,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-fdrwb2se','2025-10-14 19:17:00'),(39,62,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-25 16:26:00'),(40,1,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-5zp7r1m2','2025-10-17 22:27:00'),(41,74,'client','Necesito factura, por favor.',NULL,'2025-10-26 03:30:00'),(42,30,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-18 18:34:00'),(43,33,'client','Hola, ¿me puedes apoyar con una cotización?','te-m-ssnh2odp','2025-10-16 12:10:00'),(44,75,'user','Sí, en CDMX y Puebla mismo día.',NULL,'2025-10-14 18:33:00'),(45,73,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-23 14:35:00'),(46,27,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-15 18:30:00'),(47,23,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-19 20:44:00'),(48,74,'user','Sí, te envío CLABE por DM.',NULL,'2025-10-21 12:52:00'),(49,16,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-24 21:10:00'),(50,21,'client','Tengo problemas con mi impresora.',NULL,'2025-10-19 23:10:00'),(51,44,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-18 13:17:00'),(52,7,'client','Necesito factura, por favor.',NULL,'2025-10-18 11:09:00'),(53,12,'client','Necesito factura, por favor.',NULL,'2025-10-13 16:33:00'),(54,12,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-25 00:55:00'),(55,78,'client','¿Aceptan pago con transferencia?','em-m-k8c1gra4','2025-10-21 23:21:00'),(56,67,'user','Te apoyo de inmediato, ¿qué modelo tienes?','te-m-igbiaf92','2025-10-27 16:28:00'),(57,46,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-21 23:23:00'),(58,26,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-dk36m8jv','2025-10-27 12:15:00'),(59,25,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-19 11:44:00'),(60,23,'user','Garantía de 12 meses con fabricante.','em-m-mesjt2jp','2025-10-26 18:56:00'),(61,49,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-21 04:12:00'),(62,44,'user','Sí, te envío CLABE por DM.',NULL,'2025-10-20 17:05:00'),(63,4,'user','Con gusto, ¿qué producto requiere?',NULL,'2025-10-24 09:36:00'),(64,29,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-17 04:09:00'),(65,41,'user','Sí, en CDMX y Puebla mismo día.',NULL,'2025-10-19 19:00:00'),(66,34,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-26 23:17:00'),(67,44,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-14 06:30:00'),(68,41,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-13 17:43:00'),(69,24,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-18 05:29:00'),(70,26,'client','¿Aceptan pago con transferencia?','te-m-44m2ec8r','2025-10-25 03:47:00'),(71,1,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-r965r96k','2025-10-27 20:37:00'),(72,29,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-26 10:27:00'),(73,55,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-27 19:38:00'),(74,51,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-16 06:31:00'),(75,16,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-19 21:40:00'),(76,2,'client','¿Aceptan pago con transferencia?',NULL,'2025-10-24 23:23:00'),(77,13,'user','Sí, en CDMX y Puebla mismo día.',NULL,'2025-10-19 03:49:00'),(78,71,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-23 20:21:00'),(79,44,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-20 22:47:00'),(80,54,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-16 00:37:00'),(81,36,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-19 07:24:00'),(82,30,'client','¿Aceptan pago con transferencia?',NULL,'2025-10-24 04:25:00'),(83,56,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-25 12:51:00'),(84,61,'client','Tengo problemas con mi impresora.',NULL,'2025-10-21 20:52:00'),(85,67,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-j4bdfhj4','2025-10-17 01:10:00'),(86,13,'user','Sí, te envío CLABE por DM.',NULL,'2025-10-23 03:37:00'),(87,47,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-20 03:38:00'),(88,3,'user','Con gusto, ¿qué producto requiere?','em-m-uxg2myr0','2025-10-22 14:22:00'),(89,11,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-23 21:20:00'),(90,19,'client','¿Aceptan pago con transferencia?','te-m-u4cfilkj','2025-10-16 01:34:00'),(91,51,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-16 00:13:00'),(92,76,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-20 22:50:00'),(93,24,'client','Tengo problemas con mi impresora.',NULL,'2025-10-17 04:18:00'),(94,33,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-od7rb1s9','2025-10-16 12:55:00'),(95,14,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-26 09:19:00'),(96,50,'user','Te apoyo de inmediato, ¿qué modelo tienes?','em-m-esgbm65q','2025-10-24 12:42:00'),(97,70,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-21 07:16:00'),(98,70,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-18 21:20:00'),(99,73,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-17 15:26:00'),(100,40,'user','Para factura, compárteme tus datos fiscales.','em-m-lofas1ek','2025-10-20 04:09:00'),(101,69,'client','¿Aceptan pago con transferencia?',NULL,'2025-10-13 20:12:00'),(102,62,'user','Con gusto, ¿qué producto requiere?',NULL,'2025-10-15 22:09:00'),(103,38,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','em-m-ouof0onj','2025-10-25 11:25:00'),(104,55,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-24 19:12:00'),(105,79,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-18 03:42:00'),(106,69,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-25 09:49:00'),(107,18,'user','Con gusto, ¿qué producto requiere?','em-m-zrlf8a9k','2025-10-17 21:21:00'),(108,17,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-frml29q2','2025-10-20 13:00:00'),(109,43,'client','Tengo problemas con mi impresora.',NULL,'2025-10-28 03:11:00'),(110,51,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-21 06:48:00'),(111,33,'user','Con gusto, ¿qué producto requiere?','te-m-9i9h0dxh','2025-10-26 13:45:00'),(112,50,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','em-m-b7sjwh55','2025-10-24 01:50:00'),(113,28,'client','Tengo problemas con mi impresora.','em-m-2voi8uyy','2025-10-17 22:40:00'),(114,20,'user','Con gusto, ¿qué producto requiere?',NULL,'2025-10-25 06:29:00'),(115,12,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-19 01:01:00'),(116,8,'client','¿Manejan entregas el mismo día?','em-m-drluxm60','2025-10-18 07:16:00'),(117,3,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','em-m-6rpkzggm','2025-10-22 00:14:00'),(118,60,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-13 18:50:00'),(119,9,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-25 21:42:00'),(120,34,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-22 22:00:00'),(121,65,'user','Sí, te envío CLABE por DM.',NULL,'2025-10-26 11:21:00'),(122,80,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-17 09:18:00'),(123,69,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-19 14:29:00'),(124,71,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-24 01:34:00'),(125,42,'client','Hola, ¿me puedes apoyar con una cotización?','em-m-7gbdgbxn','2025-10-19 14:56:00'),(126,63,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-18 13:23:00'),(127,33,'client','¿Manejan entregas el mismo día?','te-m-7hr6c2cu','2025-10-24 16:15:00'),(128,54,'user','Sí, te envío CLABE por DM.','em-m-04chsdin','2025-10-27 16:43:00'),(129,25,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-18 04:24:00'),(130,23,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-16 18:34:00'),(131,74,'user','Sí, te envío CLABE por DM.',NULL,'2025-10-20 13:18:00'),(132,55,'client','Tengo problemas con mi impresora.',NULL,'2025-10-16 06:25:00'),(133,52,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-22 14:50:00'),(134,69,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-21 00:03:00'),(135,41,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-23 00:34:00'),(136,56,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-22 16:45:00'),(137,73,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-24 23:11:00'),(138,71,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-24 00:32:00'),(139,58,'user','Con gusto, ¿qué producto requiere?','em-m-s9kkh4a3','2025-10-17 10:42:00'),(140,36,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-19 18:24:00'),(141,74,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-27 21:38:00'),(142,20,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-22 17:45:00'),(143,30,'user','Sí, en CDMX y Puebla mismo día.',NULL,'2025-10-26 17:35:00'),(144,73,'client','¿Aceptan pago con transferencia?',NULL,'2025-10-26 12:40:00'),(145,62,'client','Necesito factura, por favor.',NULL,'2025-10-14 13:16:00'),(146,74,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-18 02:58:00'),(147,74,'user','Con gusto, ¿qué producto requiere?',NULL,'2025-10-16 10:02:00'),(148,43,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-22 08:05:00'),(149,30,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-17 16:01:00'),(150,2,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-15 15:36:00'),(151,7,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-28 01:26:00'),(152,73,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-19 13:46:00'),(153,20,'client','¿Aceptan pago con transferencia?',NULL,'2025-10-16 23:32:00'),(154,77,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-20 09:46:00'),(155,56,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-26 07:39:00'),(156,11,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-17 10:25:00'),(157,52,'user','Con gusto, ¿qué producto requiere?',NULL,'2025-10-21 19:33:00'),(158,17,'client','Necesito factura, por favor.','te-m-uu9sijpy','2025-10-20 05:29:00'),(159,74,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-17 22:33:00'),(160,47,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-23 00:22:00'),(161,4,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-22 16:08:00'),(162,57,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-25 21:58:00'),(163,30,'client','¿Aceptan pago con transferencia?',NULL,'2025-10-23 07:12:00'),(164,11,'client','¿Aceptan pago con transferencia?',NULL,'2025-10-28 04:21:00'),(165,19,'user','Con gusto, ¿qué producto requiere?','te-m-qahthsjr','2025-10-22 13:09:00'),(166,19,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-6sjchzjq','2025-10-16 14:59:00'),(167,2,'client','Necesito factura, por favor.',NULL,'2025-10-18 03:18:00'),(168,47,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-23 15:36:00'),(169,30,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-17 08:03:00'),(170,41,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-20 09:49:00'),(171,26,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-20 18:01:00'),(172,6,'client','¿Cuál es el tiempo de garantía?','em-m-fmmwi9s3','2025-10-24 01:29:00'),(173,33,'user','Con gusto, ¿qué producto requiere?','te-m-6xdn8wwi','2025-10-20 03:46:00'),(174,31,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-25 22:41:00'),(175,43,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-26 05:19:00'),(176,18,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','em-m-ey66p61x','2025-10-19 14:09:00'),(177,73,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-26 18:26:00'),(178,16,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-15 07:14:00'),(179,4,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-22 02:32:00'),(180,36,'client','Tengo problemas con mi impresora.',NULL,'2025-10-27 07:49:00'),(181,4,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-19 03:22:00'),(182,73,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-24 16:46:00'),(183,30,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-28 00:55:00'),(184,62,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-14 16:30:00'),(185,48,'client','Necesito factura, por favor.','te-m-io878iyh','2025-10-20 20:52:00'),(186,27,'client','Tengo problemas con mi impresora.',NULL,'2025-10-13 21:05:00'),(187,79,'user','Sí, te envío CLABE por DM.',NULL,'2025-10-22 21:04:00'),(188,32,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-16 10:22:00'),(189,49,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-22 23:21:00'),(190,74,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-19 19:19:00'),(191,5,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-26 21:31:00'),(192,6,'client','¿Cuál es el tiempo de garantía?','em-m-n18gp51k','2025-10-19 23:13:00'),(193,22,'user','Sí, en CDMX y Puebla mismo día.','te-m-f3q0e27z','2025-10-19 10:16:00'),(194,18,'user','Para factura, compárteme tus datos fiscales.','em-m-vzhqjy62','2025-10-22 21:59:00'),(195,16,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-16 21:20:00'),(196,47,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-16 23:14:00'),(197,66,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-25 23:25:00'),(198,49,'client','Tengo problemas con mi impresora.',NULL,'2025-10-14 01:24:00'),(199,20,'client','Tengo problemas con mi impresora.',NULL,'2025-10-25 13:57:00'),(200,54,'user','Sí, en CDMX y Puebla mismo día.','em-m-eehwjq4t','2025-10-16 21:42:00'),(201,1,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-xqpva5kw','2025-10-13 20:45:00'),(202,27,'client','Tengo problemas con mi impresora.',NULL,'2025-10-26 10:19:00'),(203,45,'client','Tengo problemas con mi impresora.',NULL,'2025-10-15 10:18:00'),(204,74,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-24 01:02:00'),(205,12,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-22 06:50:00'),(206,37,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-17 13:16:00'),(207,77,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-15 18:49:00'),(208,59,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-1l6314cq','2025-10-19 00:01:00'),(209,16,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-15 03:39:00'),(210,68,'user','Garantía de 12 meses con fabricante.','te-m-d0w9ry79','2025-10-24 13:47:00'),(211,37,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-15 01:44:00'),(212,68,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-uswrgvz9','2025-10-19 00:01:00'),(213,1,'client','Hola, ¿me puedes apoyar con una cotización?','te-m-429omuwa','2025-10-20 15:10:00'),(214,26,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-kt1elou8','2025-10-24 03:10:00'),(215,23,'client','¿Manejan entregas el mismo día?','em-m-62xrw6tm','2025-10-15 01:01:00'),(216,53,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-ytaul62c','2025-10-27 19:41:00'),(217,20,'user','Con gusto, ¿qué producto requiere?',NULL,'2025-10-22 23:20:00'),(218,69,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-18 23:49:00'),(219,77,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-17 01:15:00'),(220,5,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-26 20:04:00'),(221,31,'user','Para factura, compárteme tus datos fiscales.','em-m-gnbhds26','2025-10-15 02:47:00'),(222,20,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-13 20:14:00'),(223,68,'user','Sí, en CDMX y Puebla mismo día.',NULL,'2025-10-26 08:08:00'),(224,67,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-n5elb45l','2025-10-26 05:14:00'),(225,6,'client','¿Cuál es el tiempo de garantía?','em-m-ul6lgjlp','2025-10-15 14:13:00'),(226,16,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-26 03:53:00'),(227,2,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-19 19:54:00'),(228,27,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-22 18:40:00'),(229,35,'client','¿Aceptan pago con transferencia?','em-m-cwmpeqyd','2025-10-16 02:24:00'),(230,7,'client','Necesito factura, por favor.',NULL,'2025-10-22 06:15:00'),(231,77,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-17 13:16:00'),(232,58,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-23 02:39:00'),(233,69,'client','Necesito factura, por favor.',NULL,'2025-10-19 07:55:00'),(234,60,'client','Necesito factura, por favor.',NULL,'2025-10-23 14:19:00'),(235,60,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-25 07:05:00'),(236,79,'user','Sí, en CDMX y Puebla mismo día.',NULL,'2025-10-22 06:16:00'),(237,43,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-21 11:56:00'),(238,61,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-20 21:06:00'),(239,22,'user','Sí, en CDMX y Puebla mismo día.','te-m-ozduckqv','2025-10-18 17:52:00'),(240,31,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-24 18:50:00'),(241,50,'client','¿Manejan entregas el mismo día?','em-m-9umygy0z','2025-10-24 13:23:00'),(242,63,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-18 21:40:00'),(243,72,'client','Necesito factura, por favor.',NULL,'2025-10-26 02:35:00'),(244,9,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-26 14:08:00'),(245,77,'user','Sí, en CDMX y Puebla mismo día.',NULL,'2025-10-20 15:18:00'),(246,8,'client','Tengo problemas con mi impresora.','em-m-131xqkwq','2025-10-15 07:04:00'),(247,27,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-14 01:41:00'),(248,73,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-23 22:15:00'),(249,45,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-27 16:28:00'),(250,52,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-28 00:03:00'),(251,71,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-16 18:08:00'),(252,46,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-15 11:45:00'),(253,56,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-18 23:20:00'),(254,41,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-21 23:36:00'),(255,56,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-24 14:49:00'),(256,61,'client','Tengo problemas con mi impresora.',NULL,'2025-10-19 23:07:00'),(257,47,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-23 14:52:00'),(258,18,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-18 11:51:00'),(259,63,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-22 07:55:00'),(260,18,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','em-m-2vpgstqm','2025-10-15 22:05:00'),(261,24,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-27 17:29:00'),(262,31,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-20 03:34:00'),(263,74,'user','Con gusto, ¿qué producto requiere?',NULL,'2025-10-27 17:30:00'),(264,48,'client','¿Cuál es el tiempo de garantía?','te-m-0992qc6d','2025-10-20 13:55:00'),(265,61,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-16 14:18:00'),(266,10,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-17 18:09:00'),(267,75,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-28 01:26:00'),(268,2,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-19 20:24:00'),(269,43,'user','Sí, en CDMX y Puebla mismo día.',NULL,'2025-10-16 02:42:00'),(270,22,'client','¿Aceptan pago con transferencia?','te-m-2jwuuxk0','2025-10-13 16:13:00'),(271,4,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-27 07:28:00'),(272,10,'user','Sí, en CDMX y Puebla mismo día.',NULL,'2025-10-25 16:43:00'),(273,36,'user','Con gusto, ¿qué producto requiere?',NULL,'2025-10-17 08:22:00'),(274,23,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','em-m-3jzr25md','2025-10-17 07:18:00'),(275,19,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-91ipwh0m','2025-10-14 07:07:00'),(276,34,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-25 21:35:00'),(277,61,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-16 18:46:00'),(278,49,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-16 23:30:00'),(279,34,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-14 23:00:00'),(280,37,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-18 01:27:00'),(281,6,'client','¿Cuál es el tiempo de garantía?','em-m-74mjdxo1','2025-10-18 00:06:00'),(282,31,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','em-m-mygty3ad','2025-10-17 17:11:00'),(283,14,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-21 00:46:00'),(284,33,'client','Hola, ¿me puedes apoyar con una cotización?','te-m-v6hve8dv','2025-10-27 16:55:00'),(285,49,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-15 15:24:00'),(286,24,'client','¿Aceptan pago con transferencia?',NULL,'2025-10-26 03:42:00'),(287,60,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-14 09:20:00'),(288,59,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-16 14:11:00'),(289,33,'client','Hola, ¿me puedes apoyar con una cotización?','te-m-9j3gc9ho','2025-10-24 10:36:00'),(290,63,'client','Tengo problemas con mi impresora.',NULL,'2025-10-19 22:47:00'),(291,79,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-26 21:15:00'),(292,34,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-27 09:24:00'),(293,33,'user','Con gusto, ¿qué producto requiere?','te-m-abofloaz','2025-10-13 20:51:00'),(294,63,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-21 12:11:00'),(295,9,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-25 11:36:00'),(296,62,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-20 00:39:00'),(297,39,'user','Con gusto, ¿qué producto requiere?',NULL,'2025-10-17 15:55:00'),(298,47,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-15 01:55:00'),(299,59,'user','Sí, te envío CLABE por DM.','te-m-ngz6wmdw','2025-10-25 06:25:00'),(300,25,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-25 11:14:00'),(301,76,'client','Necesito factura, por favor.',NULL,'2025-10-22 09:10:00'),(302,70,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-23 20:26:00'),(303,58,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-23 10:39:00'),(304,6,'user','Con gusto, ¿qué producto requiere?','em-m-75t0ic0r','2025-10-24 15:18:00'),(305,3,'user','Garantía de 12 meses con fabricante.','em-m-aw63dw4c','2025-10-28 04:16:00'),(306,14,'client','Necesito factura, por favor.','te-m-hm40oeyt','2025-10-18 16:46:00'),(307,42,'client','Hola, ¿me puedes apoyar con una cotización?','em-m-j1gnfiue','2025-10-19 06:39:00'),(308,79,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-27 20:55:00'),(309,1,'client','Tengo problemas con mi impresora.','te-m-5o31yhxs','2025-10-14 09:15:00'),(310,53,'client','Tengo problemas con mi impresora.','te-m-zwd3kpug','2025-10-18 13:58:00'),(311,68,'client','¿Cuál es el tiempo de garantía?','te-m-1xjg2y8r','2025-10-22 18:28:00'),(312,23,'client','¿Aceptan pago con transferencia?','em-m-kpm21b07','2025-10-14 10:57:00'),(313,23,'client','Hola, ¿me puedes apoyar con una cotización?','em-m-iqup06id','2025-10-20 19:53:00'),(314,30,'client','Tengo problemas con mi impresora.',NULL,'2025-10-16 22:05:00'),(315,26,'user','Te apoyo de inmediato, ¿qué modelo tienes?','te-m-6f7qnezw','2025-10-26 20:23:00'),(316,35,'client','¿Manejan entregas el mismo día?','em-m-kdqp1hkf','2025-10-26 10:16:00'),(317,79,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-20 04:55:00'),(318,53,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-qap5ipi7','2025-10-21 05:23:00'),(319,20,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-14 11:34:00'),(320,6,'client','Necesito factura, por favor.','em-m-o3zdrc1y','2025-10-16 19:58:00'),(321,53,'client','Tengo problemas con mi impresora.','te-m-drkz40aq','2025-10-23 02:45:00'),(322,18,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-22 06:10:00'),(323,60,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-18 11:05:00'),(324,10,'user','Sí, te envío CLABE por DM.',NULL,'2025-10-22 19:58:00'),(325,38,'user','Sí, en CDMX y Puebla mismo día.','em-m-hywm7s6n','2025-10-16 16:26:00'),(326,7,'client','Necesito factura, por favor.',NULL,'2025-10-22 21:21:00'),(327,6,'user','Sí, en CDMX y Puebla mismo día.',NULL,'2025-10-25 15:25:00'),(328,72,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-16 05:52:00'),(329,43,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-26 15:30:00'),(330,75,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-24 12:12:00'),(331,29,'user','Sí, en CDMX y Puebla mismo día.',NULL,'2025-10-14 03:28:00'),(332,55,'user','Con gusto, ¿qué producto requiere?',NULL,'2025-10-27 00:38:00'),(333,58,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-20 08:30:00'),(334,69,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-19 00:09:00'),(335,9,'client','Necesito factura, por favor.',NULL,'2025-10-27 09:35:00'),(336,23,'user','Con gusto, ¿qué producto requiere?','em-m-ffh8aoy7','2025-10-27 06:43:00'),(337,61,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-20 12:19:00'),(338,3,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-27 11:05:00'),(339,67,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-xlvz4qke','2025-10-22 22:23:00'),(340,40,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-24 20:37:00'),(341,7,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-23 21:50:00'),(342,80,'client','¿Aceptan pago con transferencia?',NULL,'2025-10-20 02:49:00'),(343,23,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','em-m-iblejgub','2025-10-16 14:10:00'),(344,41,'user','Te apoyo de inmediato, ¿qué modelo tienes?',NULL,'2025-10-22 21:26:00'),(345,21,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-24 08:02:00'),(346,4,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-16 07:31:00'),(347,41,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-16 18:28:00'),(348,43,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-17 02:30:00'),(349,38,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','em-m-6py06ftl','2025-10-18 07:09:00'),(350,52,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-15 04:32:00'),(351,46,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-27 16:19:00'),(352,25,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-20 04:10:00'),(353,36,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-26 18:06:00'),(354,58,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','em-m-rvscyozp','2025-10-18 09:28:00'),(355,50,'user','Con gusto, ¿qué producto requiere?','em-m-quh50opf','2025-10-24 00:38:00'),(356,55,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-13 22:52:00'),(357,76,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-27 07:47:00'),(358,39,'user','Garantía de 12 meses con fabricante.',NULL,'2025-10-23 09:01:00'),(359,76,'user','Con gusto, ¿qué producto requiere?',NULL,'2025-10-27 22:20:00'),(360,35,'user','Te apoyo de inmediato, ¿qué modelo tienes?','em-m-6h3kr3kv','2025-10-19 21:15:00'),(361,64,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-16 21:46:00'),(362,4,'client','Tengo problemas con mi impresora.',NULL,'2025-10-24 02:20:00'),(363,61,'client','¿Aceptan pago con transferencia?',NULL,'2025-10-18 02:34:00'),(364,23,'user','Sí, te envío CLABE por DM.','em-m-j9c0uu5w','2025-10-18 04:59:00'),(365,61,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-15 08:37:00'),(366,66,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-19 11:06:00'),(367,34,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-28 07:40:00'),(368,60,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-26 00:50:00'),(369,7,'user','Sí, en CDMX y Puebla mismo día.',NULL,'2025-10-21 15:02:00'),(370,46,'client','¿Manejan entregas el mismo día?',NULL,'2025-10-23 19:20:00'),(371,10,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-24 15:49:00'),(372,13,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-16 06:26:00'),(373,42,'user','Sí, te envío CLABE por DM.','em-m-ydu3asnr','2025-10-16 02:43:00'),(374,44,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-25 07:28:00'),(375,29,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-18 13:07:00'),(376,68,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-16 18:16:00'),(377,15,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-14 09:53:00'),(378,3,'user','Sí, en CDMX y Puebla mismo día.','em-m-p9s8gk0e','2025-10-23 13:37:00'),(379,17,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-h9p1earp','2025-10-25 13:46:00'),(380,26,'client','Hola, ¿me puedes apoyar con una cotización?','te-m-q6bkadev','2025-10-15 14:28:00'),(381,76,'client','Tengo problemas con mi impresora.',NULL,'2025-10-18 00:59:00'),(382,12,'client','¿Aceptan pago con transferencia?',NULL,'2025-10-23 17:38:00'),(383,46,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-15 12:21:00'),(384,31,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-19 09:54:00'),(385,2,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-24 13:48:00'),(386,37,'client','¿Cuál es el tiempo de garantía?',NULL,'2025-10-27 12:54:00'),(387,28,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','em-m-vp8gmnhi','2025-10-14 13:30:00'),(388,15,'user','Con gusto, ¿qué producto requiere?','em-m-1zublekv','2025-10-21 08:27:00'),(389,40,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','em-m-k4gc4ryg','2025-10-14 21:46:00'),(390,63,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-26 23:32:00'),(391,67,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','te-m-ovd79c9m','2025-10-18 09:53:00'),(392,77,'user','Con gusto, ¿qué producto requiere?',NULL,'2025-10-24 22:14:00'),(393,64,'user','Sí, te envío CLABE por DM.',NULL,'2025-10-15 17:23:00'),(394,35,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?','em-m-89sfqeri','2025-10-22 00:30:00'),(395,18,'client','Hola, ¿me puedes apoyar con una cotización?','em-m-y8nyfwdc','2025-10-17 10:07:00'),(396,67,'user','Para factura, compárteme tus datos fiscales.','te-m-st3ta195','2025-10-25 02:18:00'),(397,16,'user','Para factura, compárteme tus datos fiscales.',NULL,'2025-10-22 23:32:00'),(398,59,'client','Hola, ¿me puedes apoyar con una cotización?',NULL,'2025-10-25 18:18:00'),(399,39,'bot','Soy el bot de OmniDesk, ¿en qué te ayudo?',NULL,'2025-10-25 20:33:00'),(400,18,'user','Sí, te envío CLABE por DM.','em-m-yxyur4so','2025-10-21 20:12:00'),(401,81,'client','Hola, ¿tienen stock del router?',NULL,'2025-10-28 16:59:33'),(402,81,'user','Sí, hay disponibilidad.',NULL,'2025-10-28 16:59:33');
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_msg_ai
AFTER INSERT ON message
FOR EACH ROW
BEGIN
  UPDATE conversation
     SET last_message_at = NEW.created_at
   WHERE conversation_id = NEW.conversation_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `order_item`
--

DROP TABLE IF EXISTS `order_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_item` (
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(10) unsigned NOT NULL CHECK (`quantity` > 0),
  `product_name` varchar(150) NOT NULL,
  `sku` varchar(64) DEFAULT NULL,
  `unit_price` decimal(10,2) NOT NULL CHECK (`unit_price` >= 0),
  `discount_pct` decimal(5,2) DEFAULT NULL CHECK (`discount_pct` >= 0 and `discount_pct` <= 100),
  `discount_amount` decimal(10,2) DEFAULT NULL CHECK (`discount_amount` >= 0),
  `tax_rate` decimal(5,2) NOT NULL DEFAULT 0.00 CHECK (`tax_rate` >= 0 and `tax_rate` <= 100),
  `line_subtotal` decimal(12,2) GENERATED ALWAYS AS (round(`quantity` * `unit_price`,2)) STORED,
  `line_discount` decimal(12,2) GENERATED ALWAYS AS (round(coalesce(`discount_amount`,`quantity` * `unit_price` * coalesce(`discount_pct`,0) / 100),2)) STORED,
  `line_tax_base` decimal(12,2) GENERATED ALWAYS AS (round(`line_subtotal` - `line_discount`,2)) STORED,
  `line_tax` decimal(12,2) GENERATED ALWAYS AS (round(`line_tax_base` * `tax_rate` / 100,2)) STORED,
  `line_total` decimal(12,2) GENERATED ALWAYS AS (`line_tax_base` + `line_tax`) STORED,
  PRIMARY KEY (`order_id`,`product_id`),
  KEY `idx_oi_product` (`product_id`),
  KEY `idx_oi_totals` (`order_id`,`line_total`),
  CONSTRAINT `fk_oi_order` FOREIGN KEY (`order_id`) REFERENCES `customer_order` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_oi_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_item`
--

LOCK TABLES `order_item` WRITE;
/*!40000 ALTER TABLE `order_item` DISABLE KEYS */;
INSERT INTO `order_item` VALUES (1,2,2,'Router Wi‑Fi','RTR-694D',3596.79,10.00,NULL,16.00,7193.58,719.36,6474.22,1035.88,7510.10),(1,4,1,'Laptop 14\" Pro','LTP-920M',20846.93,0.00,NULL,16.00,20846.93,0.00,20846.93,3335.51,24182.44),(1,21,3,'Audífonos Inalámbricos','AUD-452S',8242.63,0.00,NULL,16.00,24727.89,0.00,24727.89,3956.46,28684.35),(2,16,2,'Impresora Láser Plus','IMP-491V',4567.34,10.00,NULL,16.00,9134.68,913.47,8221.21,1315.39,9536.60),(2,42,1,'Router Wi‑Fi','RTR-948P',16377.95,0.00,NULL,16.00,16377.95,0.00,16377.95,2620.47,18998.42),(3,21,2,'Audífonos Inalámbricos','AUD-452S',8242.63,10.00,NULL,16.00,16485.26,1648.53,14836.73,2373.88,17210.61),(4,20,1,'Switch Gigabit 16p Plus','SWC-913A',19612.32,5.00,NULL,16.00,19612.32,980.62,18631.70,2981.07,21612.77),(4,40,2,'Teclado Mecánico RGB','KB-905D',330.64,5.00,NULL,16.00,661.28,33.06,628.22,100.52,728.74),(5,46,3,'Monitor 27\" IPS Pro','MON-544F',2800.07,0.00,NULL,16.00,8400.21,0.00,8400.21,1344.03,9744.24),(6,28,2,'Router Wi‑Fi','RTR-157H',5703.58,0.00,NULL,16.00,11407.16,0.00,11407.16,1825.15,13232.31),(6,35,2,'Teclado Mecánico RGB','KB-230F',343.41,10.00,NULL,16.00,686.82,68.68,618.14,98.90,717.04),(6,43,2,'Audífonos Inalámbricos Pro','AUD-175Z',7583.24,5.00,NULL,16.00,15166.48,758.32,14408.16,2305.31,16713.47),(7,35,3,'Teclado Mecánico RGB','KB-230F',343.41,0.00,NULL,16.00,1030.23,0.00,1030.23,164.84,1195.07),(7,41,3,'Proyector LED 1080p Plus','PRJ-270N',22078.74,0.00,NULL,16.00,66236.22,0.00,66236.22,10597.80,76834.02),(7,60,3,'Router Wi‑Fi Pro','RTR-799N',24931.55,5.00,NULL,16.00,74794.65,3739.73,71054.92,11368.79,82423.71),(8,18,1,'Teclado Mecánico RGB','KB-610N',12131.06,0.00,NULL,16.00,12131.06,0.00,12131.06,1940.97,14072.03),(8,19,1,'Cámara Seguridad 4K','CCTV-529G',22149.92,5.00,NULL,16.00,22149.92,1107.50,21042.42,3366.79,24409.21),(8,42,1,'Router Wi‑Fi','RTR-948P',16377.95,0.00,NULL,16.00,16377.95,0.00,16377.95,2620.47,18998.42),(8,53,3,'Laptop 14\" Pro Pro','LTP-291O',6802.41,10.00,NULL,16.00,20407.23,2040.72,18366.51,2938.64,21305.15),(9,11,1,'Switch Gigabit 16p Plus','SWC-355D',2816.11,0.00,NULL,16.00,2816.11,0.00,2816.11,450.58,3266.69),(9,18,2,'Teclado Mecánico RGB','KB-610N',12131.06,0.00,NULL,16.00,24262.12,0.00,24262.12,3881.94,28144.06),(10,58,2,'Monitor 27\" IPS','MON-629Z',17034.11,0.00,NULL,16.00,34068.22,0.00,34068.22,5450.92,39519.14),(11,6,2,'Router Wi‑Fi Plus','RTR-268O',8055.62,10.00,NULL,16.00,16111.24,1611.12,14500.12,2320.02,16820.14),(11,32,1,'Router Wi‑Fi Plus','RTR-444J',3669.36,10.00,NULL,16.00,3669.36,366.94,3302.42,528.39,3830.81),(11,57,1,'Monitor 27\" IPS Plus','MON-341P',2249.19,0.00,NULL,16.00,2249.19,0.00,2249.19,359.87,2609.06),(12,8,2,'Teclado Mecánico RGB','KB-946W',15200.57,0.00,NULL,16.00,30401.14,0.00,30401.14,4864.18,35265.32),(12,21,2,'Audífonos Inalámbricos','AUD-452S',8242.63,0.00,NULL,16.00,16485.26,0.00,16485.26,2637.64,19122.90),(12,45,3,'Laptop 14\" Pro Plus','LTP-708T',17700.26,5.00,NULL,16.00,53100.78,2655.04,50445.74,8071.32,58517.06),(13,20,3,'Switch Gigabit 16p Plus','SWC-913A',19612.32,0.00,NULL,16.00,58836.96,0.00,58836.96,9413.91,68250.87),(13,25,3,'Laptop 14\" Pro Pro','LTP-959F',6141.81,0.00,NULL,16.00,18425.43,0.00,18425.43,2948.07,21373.50),(13,36,3,'Monitor 27\" IPS','MON-133F',8158.96,0.00,NULL,16.00,24476.88,0.00,24476.88,3916.30,28393.18),(14,18,1,'Teclado Mecánico RGB','KB-610N',12131.06,5.00,NULL,16.00,12131.06,606.55,11524.51,1843.92,13368.43),(15,23,2,'Switch Gigabit 16p','SWC-466Y',24989.26,10.00,NULL,16.00,49978.52,4997.85,44980.67,7196.91,52177.58),(16,6,3,'Router Wi‑Fi Plus','RTR-268O',8055.62,0.00,NULL,16.00,24166.86,0.00,24166.86,3866.70,28033.56),(16,8,3,'Teclado Mecánico RGB','KB-946W',15200.57,5.00,NULL,16.00,45601.71,2280.09,43321.62,6931.46,50253.08),(16,37,1,'Monitor 27\" IPS Pro','MON-206P',8478.86,0.00,NULL,16.00,8478.86,0.00,8478.86,1356.62,9835.48),(17,15,1,'Audífonos Inalámbricos','AUD-151F',10997.96,5.00,NULL,16.00,10997.96,549.90,10448.06,1671.69,12119.75),(17,37,3,'Monitor 27\" IPS Pro','MON-206P',8478.86,0.00,NULL,16.00,25436.58,0.00,25436.58,4069.85,29506.43),(17,54,1,'Teclado Mecánico RGB Pro','KB-677B',18879.21,0.00,NULL,16.00,18879.21,0.00,18879.21,3020.67,21899.88),(17,57,3,'Monitor 27\" IPS Plus','MON-341P',2249.19,10.00,NULL,16.00,6747.57,674.76,6072.81,971.65,7044.46),(18,8,2,'Teclado Mecánico RGB','KB-946W',15200.57,5.00,NULL,16.00,30401.14,1520.06,28881.08,4620.97,33502.05),(18,37,1,'Monitor 27\" IPS Pro','MON-206P',8478.86,10.00,NULL,16.00,8478.86,847.89,7630.97,1220.96,8851.93),(19,13,1,'Router Wi‑Fi Plus','RTR-696S',22959.49,0.00,NULL,16.00,22959.49,0.00,22959.49,3673.52,26633.01),(19,44,2,'Router Wi‑Fi Plus','RTR-450F',4273.34,0.00,NULL,16.00,8546.68,0.00,8546.68,1367.47,9914.15),(19,47,2,'Switch Gigabit 16p','SWC-839X',6851.04,0.00,NULL,16.00,13702.08,0.00,13702.08,2192.33,15894.41),(20,28,1,'Router Wi‑Fi','RTR-157H',5703.58,10.00,NULL,16.00,5703.58,570.36,5133.22,821.32,5954.54),(20,39,2,'Laptop 14\" Pro Plus','LTP-557A',5478.20,0.00,NULL,16.00,10956.40,0.00,10956.40,1753.02,12709.42),(20,46,2,'Monitor 27\" IPS Pro','MON-544F',2800.07,0.00,NULL,16.00,5600.14,0.00,5600.14,896.02,6496.16),(20,48,1,'Router Wi‑Fi','RTR-150M',13875.67,0.00,NULL,16.00,13875.67,0.00,13875.67,2220.11,16095.78),(21,9,2,'Cámara Seguridad 4K Pro','CCTV-193W',24218.48,0.00,NULL,16.00,48436.96,0.00,48436.96,7749.91,56186.87),(21,24,3,'Silla Ergonómica','SLL-372R',1679.94,0.00,NULL,16.00,5039.82,0.00,5039.82,806.37,5846.19),(21,43,3,'Audífonos Inalámbricos Pro','AUD-175Z',7583.24,0.00,NULL,16.00,22749.72,0.00,22749.72,3639.96,26389.68),(21,58,3,'Monitor 27\" IPS','MON-629Z',17034.11,5.00,NULL,16.00,51102.33,2555.12,48547.21,7767.55,56314.76),(22,17,2,'Teclado Mecánico RGB Pro','KB-386O',1154.84,5.00,NULL,16.00,2309.68,115.48,2194.20,351.07,2545.27),(22,19,3,'Cámara Seguridad 4K','CCTV-529G',22149.92,0.00,NULL,16.00,66449.76,0.00,66449.76,10631.96,77081.72),(22,57,2,'Monitor 27\" IPS Plus','MON-341P',2249.19,0.00,NULL,16.00,4498.38,0.00,4498.38,719.74,5218.12),(22,58,3,'Monitor 27\" IPS','MON-629Z',17034.11,0.00,NULL,16.00,51102.33,0.00,51102.33,8176.37,59278.70),(23,8,1,'Teclado Mecánico RGB','KB-946W',15200.57,5.00,NULL,16.00,15200.57,760.03,14440.54,2310.49,16751.03),(23,32,2,'Router Wi‑Fi Plus','RTR-444J',3669.36,0.00,NULL,16.00,7338.72,0.00,7338.72,1174.20,8512.92),(23,58,2,'Monitor 27\" IPS','MON-629Z',17034.11,10.00,NULL,16.00,34068.22,3406.82,30661.40,4905.82,35567.22),(23,60,2,'Router Wi‑Fi Pro','RTR-799N',24931.55,5.00,NULL,16.00,49863.10,2493.16,47369.94,7579.19,54949.13),(24,5,2,'Teclado Mecánico RGB Pro','KB-339C',3660.96,0.00,NULL,16.00,7321.92,0.00,7321.92,1171.51,8493.43),(24,16,2,'Impresora Láser Plus','IMP-491V',4567.34,0.00,NULL,16.00,9134.68,0.00,9134.68,1461.55,10596.23),(24,50,2,'Audífonos Inalámbricos Pro','AUD-304D',5410.74,0.00,NULL,16.00,10821.48,0.00,10821.48,1731.44,12552.92),(24,59,2,'Audífonos Inalámbricos Pro','AUD-277F',20267.98,0.00,NULL,16.00,40535.96,0.00,40535.96,6485.75,47021.71),(25,1,2,'Impresora Láser Plus','IMP-337Q',17609.92,0.00,NULL,16.00,35219.84,0.00,35219.84,5635.17,40855.01),(25,39,2,'Laptop 14\" Pro Plus','LTP-557A',5478.20,0.00,NULL,16.00,10956.40,0.00,10956.40,1753.02,12709.42),(25,43,3,'Audífonos Inalámbricos Pro','AUD-175Z',7583.24,10.00,NULL,16.00,22749.72,2274.97,20474.75,3275.96,23750.71),(26,12,2,'Impresora Láser Pro','IMP-950Y',3527.67,0.00,NULL,16.00,7055.34,0.00,7055.34,1128.85,8184.19),(26,16,1,'Impresora Láser Plus','IMP-491V',4567.34,0.00,NULL,16.00,4567.34,0.00,4567.34,730.77,5298.11),(26,50,1,'Audífonos Inalámbricos Pro','AUD-304D',5410.74,5.00,NULL,16.00,5410.74,270.54,5140.20,822.43,5962.63),(27,25,1,'Laptop 14\" Pro Pro','LTP-959F',6141.81,5.00,NULL,16.00,6141.81,307.09,5834.72,933.56,6768.28),(27,29,2,'Laptop 14\" Pro Pro','LTP-728G',8715.75,10.00,NULL,16.00,17431.50,1743.15,15688.35,2510.14,18198.49),(27,31,2,'Switch Gigabit 16p Pro','SWC-981L',9526.69,10.00,NULL,16.00,19053.38,1905.34,17148.04,2743.69,19891.73),(27,57,3,'Monitor 27\" IPS Plus','MON-341P',2249.19,5.00,NULL,16.00,6747.57,337.38,6410.19,1025.63,7435.82),(28,6,1,'Router Wi‑Fi Plus','RTR-268O',8055.62,0.00,NULL,16.00,8055.62,0.00,8055.62,1288.90,9344.52),(28,34,2,'Laptop 14\" Pro','LTP-328V',20416.02,5.00,NULL,16.00,40832.04,2041.60,38790.44,6206.47,44996.91),(28,41,2,'Proyector LED 1080p Plus','PRJ-270N',22078.74,0.00,NULL,16.00,44157.48,0.00,44157.48,7065.20,51222.68),(28,42,2,'Router Wi‑Fi','RTR-948P',16377.95,0.00,NULL,16.00,32755.90,0.00,32755.90,5240.94,37996.84),(29,33,2,'Audífonos Inalámbricos Pro','AUD-764K',17766.42,5.00,NULL,16.00,35532.84,1776.64,33756.20,5400.99,39157.19),(30,12,1,'Impresora Láser Pro','IMP-950Y',3527.67,0.00,NULL,16.00,3527.67,0.00,3527.67,564.43,4092.10),(30,26,3,'Laptop 14\" Pro','LTP-705A',17602.85,5.00,NULL,16.00,52808.55,2640.43,50168.12,8026.90,58195.02),(30,51,2,'Audífonos Inalámbricos Plus','AUD-964D',19685.45,0.00,NULL,16.00,39370.90,0.00,39370.90,6299.34,45670.24),(30,54,2,'Teclado Mecánico RGB Pro','KB-677B',18879.21,10.00,NULL,16.00,37758.42,3775.84,33982.58,5437.21,39419.79),(31,1,1,'Impresora Láser Plus','IMP-337Q',17609.92,5.00,NULL,16.00,17609.92,880.50,16729.42,2676.71,19406.13),(32,1,1,'Impresora Láser Plus','IMP-337Q',17609.92,0.00,NULL,16.00,17609.92,0.00,17609.92,2817.59,20427.51),(32,6,1,'Router Wi‑Fi Plus','RTR-268O',8055.62,0.00,NULL,16.00,8055.62,0.00,8055.62,1288.90,9344.52),(32,9,1,'Cámara Seguridad 4K Pro','CCTV-193W',24218.48,0.00,NULL,16.00,24218.48,0.00,24218.48,3874.96,28093.44),(33,8,1,'Teclado Mecánico RGB','KB-946W',15200.57,0.00,NULL,16.00,15200.57,0.00,15200.57,2432.09,17632.66),(34,32,2,'Router Wi‑Fi Plus','RTR-444J',3669.36,0.00,NULL,16.00,7338.72,0.00,7338.72,1174.20,8512.92),(34,38,2,'Laptop 14\" Pro Pro','LTP-271U',20594.05,10.00,NULL,16.00,41188.10,4118.81,37069.29,5931.09,43000.38),(34,48,2,'Router Wi‑Fi','RTR-150M',13875.67,5.00,NULL,16.00,27751.34,1387.57,26363.77,4218.20,30581.97),(34,55,3,'Laptop 14\" Pro Plus','LTP-927R',24275.43,10.00,NULL,16.00,72826.29,7282.63,65543.66,10486.99,76030.65),(35,27,3,'Monitor 27\" IPS Plus','MON-292Z',13689.48,0.00,NULL,16.00,41068.44,0.00,41068.44,6570.95,47639.39),(35,42,2,'Router Wi‑Fi','RTR-948P',16377.95,10.00,NULL,16.00,32755.90,3275.59,29480.31,4716.85,34197.16),(35,58,2,'Monitor 27\" IPS','MON-629Z',17034.11,0.00,NULL,16.00,34068.22,0.00,34068.22,5450.92,39519.14),(36,38,3,'Laptop 14\" Pro Pro','LTP-271U',20594.05,0.00,NULL,16.00,61782.15,0.00,61782.15,9885.14,71667.29),(36,59,3,'Audífonos Inalámbricos Pro','AUD-277F',20267.98,5.00,NULL,16.00,60803.94,3040.20,57763.74,9242.20,67005.94),(37,43,2,'Audífonos Inalámbricos Pro','AUD-175Z',7583.24,0.00,NULL,16.00,15166.48,0.00,15166.48,2426.64,17593.12),(38,2,2,'Router Wi‑Fi','RTR-694D',3596.79,0.00,NULL,16.00,7193.58,0.00,7193.58,1150.97,8344.55),(39,36,1,'Monitor 27\" IPS','MON-133F',8158.96,5.00,NULL,16.00,8158.96,407.95,7751.01,1240.16,8991.17),(40,60,2,'Router Wi‑Fi Pro','RTR-799N',24931.55,5.00,NULL,16.00,49863.10,2493.16,47369.94,7579.19,54949.13),(41,56,1,'Impresora Láser','IMP-960M',10639.21,NULL,NULL,16.00,10639.21,0.00,10639.21,1702.27,12341.48);
/*!40000 ALTER TABLE `order_item` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_oi_ai AFTER INSERT ON order_item
FOR EACH ROW BEGIN
  CALL sp_recalc_order_totals(NEW.order_id);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_oi_au AFTER UPDATE ON order_item
FOR EACH ROW BEGIN
  CALL sp_recalc_order_totals(NEW.order_id);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_oi_ad AFTER DELETE ON order_item
FOR EACH ROW BEGIN
  CALL sp_recalc_order_totals(OLD.order_id);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `sku` varchar(64) DEFAULT NULL,
  `name` varchar(150) NOT NULL,
  `description` text DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL CHECK (`price` >= 0),
  `stock` int(10) unsigned NOT NULL DEFAULT 0 CHECK (`stock` >= 0),
  `status` enum('draft','active','archived') NOT NULL DEFAULT 'active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `uq_product_sku` (`sku`),
  KEY `fk_product_category` (`category_id`),
  KEY `idx_product_name` (`name`),
  FULLTEXT KEY `ftx_product_nd` (`name`,`description`),
  CONSTRAINT `fk_product_category` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'IMP-337Q','Impresora Láser Plus','Impresora láser monocroma con Wi-Fi.',NULL,7,17609.92,105,'active','2025-10-12 19:00:00','2025-10-28 21:05:45'),(2,'RTR-694D','Router Wi‑Fi','Router Wi‑Fi de doble banda.',NULL,6,3596.79,110,'active','2025-10-25 00:00:00','2025-10-28 21:05:45'),(3,'MON-163N','Monitor 27\" IPS','Monitor 27\" IPS 75Hz.',NULL,1,24115.19,70,'active','2025-10-18 10:00:00','2025-10-28 21:05:45'),(4,'LTP-920M','Laptop 14\" Pro','Ultrabook 14\" 16GB/512GB.',NULL,1,20846.93,93,'active','2025-10-17 04:00:00','2025-10-28 21:05:45'),(5,'KB-339C','Teclado Mecánico RGB Pro','Teclado mecánico con switches rojos.',NULL,5,3660.96,159,'active','2025-10-24 14:00:00','2025-10-28 21:05:45'),(6,'RTR-268O','Router Wi‑Fi Plus','Router Wi‑Fi de doble banda.',NULL,6,8055.62,40,'active','2025-10-10 07:00:00','2025-10-28 21:05:45'),(7,'SLL-562J','Silla Ergonómica Plus','Silla con soporte lumbar ajustable.',NULL,9,6844.70,40,'active','2025-10-25 13:00:00','2025-10-28 21:05:45'),(8,'KB-946W','Teclado Mecánico RGB','Teclado mecánico con switches rojos.',NULL,5,15200.57,65,'active','2025-10-01 08:00:00','2025-10-28 21:05:45'),(9,'CCTV-193W','Cámara Seguridad 4K Pro','Cámara seguridad 4K para interiores/exteriores.',NULL,8,24218.48,111,'active','2025-10-11 17:00:00','2025-10-28 21:05:45'),(10,'KB-366F','Teclado Mecánico RGB Pro','Teclado mecánico con switches rojos.',NULL,5,23815.79,125,'active','2025-10-09 19:00:00','2025-10-28 21:05:45'),(11,'SWC-355D','Switch Gigabit 16p Plus','Switch 16 puertos 10/100/1000.',NULL,6,2816.11,45,'active','2025-10-24 18:00:00','2025-10-28 21:05:45'),(12,'IMP-950Y','Impresora Láser Pro','Impresora láser monocroma con Wi-Fi.',NULL,7,3527.67,112,'active','2025-10-15 21:00:00','2025-10-28 21:05:45'),(13,'RTR-696S','Router Wi‑Fi Plus','Router Wi‑Fi de doble banda.',NULL,6,22959.49,29,'active','2025-10-27 16:00:00','2025-10-28 21:05:45'),(14,'SLL-761O','Silla Ergonómica Pro','Silla con soporte lumbar ajustable.',NULL,9,2570.87,94,'active','2025-10-24 17:00:00','2025-10-28 21:05:45'),(15,'AUD-151F','Audífonos Inalámbricos','Bluetooth con cancelación activa.',NULL,10,10997.96,195,'active','2025-10-15 03:00:00','2025-10-28 21:05:45'),(16,'IMP-491V','Impresora Láser Plus','Impresora láser monocroma con Wi-Fi.',NULL,7,4567.34,64,'active','2025-09-28 13:00:00','2025-10-28 21:05:45'),(17,'KB-386O','Teclado Mecánico RGB Pro','Teclado mecánico con switches rojos.',NULL,5,1154.84,168,'active','2025-10-08 11:00:00','2025-10-28 21:05:45'),(18,'KB-610N','Teclado Mecánico RGB','Teclado mecánico con switches rojos.',NULL,5,12131.06,32,'active','2025-10-19 06:00:00','2025-10-28 21:05:45'),(19,'CCTV-529G','Cámara Seguridad 4K','Cámara seguridad 4K para interiores/exteriores.',NULL,8,22149.92,144,'active','2025-10-19 22:00:00','2025-10-28 21:05:45'),(20,'SWC-913A','Switch Gigabit 16p Plus','Switch 16 puertos 10/100/1000.',NULL,6,19612.32,101,'active','2025-10-12 01:00:00','2025-10-28 21:05:45'),(21,'AUD-452S','Audífonos Inalámbricos','Bluetooth con cancelación activa.',NULL,10,8242.63,79,'active','2025-10-22 18:00:00','2025-10-28 21:05:45'),(22,'LTP-711H','Laptop 14\" Pro Pro','Ultrabook 14\" 16GB/512GB.',NULL,1,22424.39,81,'active','2025-10-26 03:00:00','2025-10-28 21:05:45'),(23,'SWC-466Y','Switch Gigabit 16p','Switch 16 puertos 10/100/1000.',NULL,6,24989.26,50,'active','2025-10-24 11:00:00','2025-10-28 21:05:45'),(24,'SLL-372R','Silla Ergonómica','Silla con soporte lumbar ajustable.',NULL,9,1679.94,66,'active','2025-10-09 06:00:00','2025-10-28 21:05:45'),(25,'LTP-959F','Laptop 14\" Pro Pro','Ultrabook 14\" 16GB/512GB.',NULL,1,6141.81,91,'active','2025-10-01 19:00:00','2025-10-28 21:05:45'),(26,'LTP-705A','Laptop 14\" Pro','Ultrabook 14\" 16GB/512GB.',NULL,1,17602.85,155,'active','2025-10-09 14:00:00','2025-10-28 21:05:45'),(27,'MON-292Z','Monitor 27\" IPS Plus','Monitor 27\" IPS 75Hz.',NULL,1,13689.48,54,'active','2025-10-12 17:00:00','2025-10-28 21:05:45'),(28,'RTR-157H','Router Wi‑Fi','Router Wi‑Fi de doble banda.',NULL,6,5703.58,144,'active','2025-10-12 18:00:00','2025-10-28 21:05:45'),(29,'LTP-728G','Laptop 14\" Pro Pro','Ultrabook 14\" 16GB/512GB.',NULL,1,8715.75,55,'active','2025-09-28 08:00:00','2025-10-28 21:05:45'),(30,'IMP-122E','Impresora Láser','Impresora láser monocroma con Wi-Fi.',NULL,7,17705.00,46,'active','2025-10-03 15:00:00','2025-10-28 21:05:45'),(31,'SWC-981L','Switch Gigabit 16p Pro','Switch 16 puertos 10/100/1000.',NULL,6,9526.69,179,'active','2025-10-15 00:00:00','2025-10-28 21:05:45'),(32,'RTR-444J','Router Wi‑Fi Plus','Router Wi‑Fi de doble banda.',NULL,6,3669.36,50,'active','2025-10-04 05:00:00','2025-10-28 21:05:45'),(33,'AUD-764K','Audífonos Inalámbricos Pro','Bluetooth con cancelación activa.',NULL,10,17766.42,153,'active','2025-10-04 23:00:00','2025-10-28 21:05:45'),(34,'LTP-328V','Laptop 14\" Pro','Ultrabook 14\" 16GB/512GB.',NULL,1,20416.02,106,'active','2025-10-17 19:00:00','2025-10-28 21:05:45'),(35,'KB-230F','Teclado Mecánico RGB','Teclado mecánico con switches rojos.',NULL,5,343.41,189,'active','2025-10-09 06:00:00','2025-10-28 21:05:45'),(36,'MON-133F','Monitor 27\" IPS','Monitor 27\" IPS 75Hz.',NULL,1,8158.96,166,'active','2025-10-19 22:00:00','2025-10-28 21:05:45'),(37,'MON-206P','Monitor 27\" IPS Pro','Monitor 27\" IPS 75Hz.',NULL,1,8478.86,29,'active','2025-10-20 07:00:00','2025-10-28 21:05:45'),(38,'LTP-271U','Laptop 14\" Pro Pro','Ultrabook 14\" 16GB/512GB.',NULL,1,20594.05,181,'active','2025-10-06 19:00:00','2025-10-28 21:05:45'),(39,'LTP-557A','Laptop 14\" Pro Plus','Ultrabook 14\" 16GB/512GB.',NULL,1,5478.20,187,'active','2025-10-25 07:00:00','2025-10-28 21:05:45'),(40,'KB-905D','Teclado Mecánico RGB','Teclado mecánico con switches rojos.',NULL,5,330.64,108,'active','2025-10-12 19:00:00','2025-10-28 21:05:45'),(41,'PRJ-270N','Proyector LED 1080p Plus','Proyector 1080p para oficina y hogar.',NULL,2,22078.74,99,'active','2025-10-10 06:00:00','2025-10-28 21:05:45'),(42,'RTR-948P','Router Wi‑Fi','Router Wi‑Fi de doble banda.',NULL,6,16377.95,185,'active','2025-10-20 13:00:00','2025-10-28 21:05:45'),(43,'AUD-175Z','Audífonos Inalámbricos Pro','Bluetooth con cancelación activa.',NULL,10,7583.24,91,'active','2025-10-19 15:00:00','2025-10-28 21:05:45'),(44,'RTR-450F','Router Wi‑Fi Plus','Router Wi‑Fi de doble banda.',NULL,6,4273.34,29,'active','2025-10-10 16:00:00','2025-10-28 21:05:45'),(45,'LTP-708T','Laptop 14\" Pro Plus','Ultrabook 14\" 16GB/512GB.',NULL,1,17700.26,120,'active','2025-10-07 13:00:00','2025-10-28 21:05:45'),(46,'MON-544F','Monitor 27\" IPS Pro','Monitor 27\" IPS 75Hz.',NULL,1,2800.07,62,'active','2025-10-21 05:00:00','2025-10-28 21:05:45'),(47,'SWC-839X','Switch Gigabit 16p','Switch 16 puertos 10/100/1000.',NULL,6,6851.04,82,'active','2025-10-18 11:00:00','2025-10-28 21:05:45'),(48,'RTR-150M','Router Wi‑Fi','Router Wi‑Fi de doble banda.',NULL,6,13875.67,135,'active','2025-10-23 17:00:00','2025-10-28 21:05:45'),(49,'LTP-103N','Laptop 14\" Pro Pro','Ultrabook 14\" 16GB/512GB.',NULL,1,7574.37,179,'active','2025-10-06 23:00:00','2025-10-28 21:05:45'),(50,'AUD-304D','Audífonos Inalámbricos Pro','Bluetooth con cancelación activa.',NULL,10,5410.74,173,'active','2025-10-18 16:00:00','2025-10-28 21:05:45'),(51,'AUD-964D','Audífonos Inalámbricos Plus','Bluetooth con cancelación activa.',NULL,10,19685.45,130,'active','2025-10-11 21:00:00','2025-10-28 21:05:45'),(52,'KB-193U','Teclado Mecánico RGB','Teclado mecánico con switches rojos.',NULL,5,9870.92,104,'active','2025-09-29 06:00:00','2025-10-28 21:05:45'),(53,'LTP-291O','Laptop 14\" Pro Pro','Ultrabook 14\" 16GB/512GB.',NULL,1,6802.41,129,'active','2025-10-19 11:00:00','2025-10-28 21:05:45'),(54,'KB-677B','Teclado Mecánico RGB Pro','Teclado mecánico con switches rojos.',NULL,5,18879.21,180,'active','2025-10-24 16:00:00','2025-10-28 21:05:45'),(55,'LTP-927R','Laptop 14\" Pro Plus','Ultrabook 14\" 16GB/512GB.',NULL,1,24275.43,160,'active','2025-10-20 01:00:00','2025-10-28 21:05:45'),(56,'IMP-960M','Impresora Láser','Impresora láser monocroma con Wi-Fi.',NULL,7,10639.21,147,'active','2025-10-06 03:00:00','2025-10-28 21:05:45'),(57,'MON-341P','Monitor 27\" IPS Plus','Monitor 27\" IPS 75Hz.',NULL,1,2249.19,192,'active','2025-10-26 02:00:00','2025-10-28 21:05:45'),(58,'MON-629Z','Monitor 27\" IPS','Monitor 27\" IPS 75Hz.',NULL,1,17034.11,168,'active','2025-10-23 15:00:00','2025-10-28 21:05:45'),(59,'AUD-277F','Audífonos Inalámbricos Pro','Bluetooth con cancelación activa.',NULL,10,20267.98,42,'active','2025-10-26 05:00:00','2025-10-28 21:05:45'),(60,'RTR-799N','Router Wi‑Fi Pro','Router Wi‑Fi de doble banda.',NULL,6,24931.55,170,'active','2025-10-22 23:00:00','2025-10-28 21:05:45');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ticket` (
  `ticket_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `subject` varchar(150) NOT NULL,
  `description` text DEFAULT NULL,
  `priority` enum('alta','media','baja') NOT NULL DEFAULT 'media',
  `status` enum('abierto','en_progreso','cerrado') NOT NULL DEFAULT 'abierto',
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `due_at` datetime DEFAULT NULL,
  `resolved_at` datetime DEFAULT NULL,
  `assigned_to` int(11) DEFAULT NULL,
  PRIMARY KEY (`ticket_id`),
  KEY `fk_ticket_assigned` (`assigned_to`),
  KEY `idx_ticket_client` (`client_id`),
  KEY `idx_ticket_status` (`status`,`priority`),
  KEY `idx_ticket_created_at` (`created_at`),
  KEY `idx_ticket_due_at` (`due_at`),
  CONSTRAINT `fk_ticket_assigned` FOREIGN KEY (`assigned_to`) REFERENCES `app_user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_ticket_client` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`) ON UPDATE CASCADE,
  CONSTRAINT `CONSTRAINT_1` CHECK (`due_at` is null or `due_at` >= `created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
INSERT INTO `ticket` VALUES (1,4,'Consulta garantía','Cámara 3 presenta imagen borrosa por la noche.','media','cerrado','2025-10-20 20:00:00','2025-10-21 20:00:00',NULL,12),(2,8,'Problema con facturación','Consulta sobre periodo de garantía extendida.','baja','cerrado','2025-10-22 09:00:00','2025-10-23 09:00:00',NULL,11),(3,16,'Error al iniciar sesión','Consulta sobre periodo de garantía extendida.','baja','cerrado','2025-10-26 22:00:00','2025-10-29 22:00:00',NULL,4),(4,104,'Falla cámara seguridad','Error CFDI al timbrar, requiere reintento.','media','en_progreso','2025-10-16 14:00:00','2025-10-21 14:00:00',NULL,11),(5,18,'Entrega no recibida','Cámara 3 presenta imagen borrosa por la noche.','alta','cerrado','2025-10-18 18:00:00','2025-10-20 18:00:00','2025-10-28 15:05:45',6),(6,59,'Impresora atora papel','Cotización para 10 unidades con entrega en 48h.','baja','cerrado','2025-10-21 10:00:00','2025-10-22 10:00:00','2025-10-28 15:05:45',1),(7,55,'Solicitud de cotización','Usuario olvida contraseña con frecuencia.','alta','en_progreso','2025-10-26 01:00:00','2025-11-01 01:00:00',NULL,9),(8,52,'Entrega no recibida','Consulta sobre periodo de garantía extendida.','baja','cerrado','2025-10-16 23:00:00','2025-10-20 23:00:00','2025-10-28 15:05:45',12),(9,120,'Error al iniciar sesión','Paquetería marcó entregado pero cliente no lo tiene.','alta','abierto','2025-10-19 08:00:00','2025-10-23 08:00:00',NULL,12),(10,59,'Solicitud de cotización','Atascos frecuentes al imprimir documentos largos.','baja','abierto','2025-10-19 21:00:00','2025-10-20 21:00:00',NULL,12),(11,21,'Problema con facturación','Atascos frecuentes al imprimir documentos largos.','baja','en_progreso','2025-10-26 09:00:00','2025-10-29 09:00:00',NULL,10),(12,38,'Intermitencia en Wi‑Fi','Cotización para 10 unidades con entrega en 48h.','alta','cerrado','2025-10-23 01:00:00','2025-10-26 01:00:00','2025-10-28 15:05:45',5),(13,63,'Intermitencia en Wi‑Fi','Cotización para 10 unidades con entrega en 48h.','alta','cerrado','2025-10-21 11:00:00','2025-10-24 11:00:00',NULL,5),(14,28,'Solicitud de cotización','Usuario olvida contraseña con frecuencia.','alta','abierto','2025-10-19 01:00:00','2025-10-20 01:00:00',NULL,1),(15,54,'Error al iniciar sesión','Consulta sobre periodo de garantía extendida.','baja','en_progreso','2025-10-22 00:00:00','2025-10-26 00:00:00',NULL,12),(16,107,'Solicitud de cotización','Cotización para 10 unidades con entrega en 48h.','baja','cerrado','2025-10-19 22:00:00','2025-10-25 22:00:00',NULL,8),(17,20,'Problema con facturación','Atascos frecuentes al imprimir documentos largos.','baja','cerrado','2025-10-17 23:00:00','2025-10-21 23:00:00',NULL,4),(18,116,'Entrega no recibida','Error CFDI al timbrar, requiere reintento.','baja','abierto','2025-10-16 22:00:00','2025-10-22 22:00:00',NULL,5),(19,83,'Impresora atora papel','Cotización para 10 unidades con entrega en 48h.','baja','abierto','2025-10-17 16:00:00','2025-10-24 16:00:00',NULL,12),(20,40,'Impresora atora papel','Atascos frecuentes al imprimir documentos largos.','alta','cerrado','2025-10-18 18:00:00','2025-10-25 18:00:00',NULL,1),(21,73,'Falla cámara seguridad','Usuario olvida contraseña con frecuencia.','baja','abierto','2025-10-25 15:00:00','2025-10-30 15:00:00',NULL,3),(22,3,'Consulta garantía','Cámara 3 presenta imagen borrosa por la noche.','alta','cerrado','2025-10-17 22:00:00','2025-10-18 22:00:00',NULL,9),(23,78,'Problema con facturación','Paquetería marcó entregado pero cliente no lo tiene.','baja','cerrado','2025-10-20 12:00:00','2025-10-23 12:00:00','2025-10-28 15:05:45',7),(24,24,'Entrega no recibida','Reporte de cortes de conexión en horas pico.','baja','en_progreso','2025-10-21 04:00:00','2025-10-22 04:00:00',NULL,2),(25,13,'Solicitud de cotización','Consulta sobre periodo de garantía extendida.','alta','cerrado','2025-10-23 10:00:00','2025-10-25 10:00:00','2025-10-28 15:05:45',5),(26,53,'Solicitud de cotización','Reporte de cortes de conexión en horas pico.','baja','en_progreso','2025-10-25 12:00:00','2025-10-31 12:00:00',NULL,1),(27,39,'Entrega no recibida','Atascos frecuentes al imprimir documentos largos.','media','cerrado','2025-10-21 02:00:00','2025-10-24 02:00:00','2025-10-28 15:05:45',7),(28,106,'Impresora atora papel','Reporte de cortes de conexión en horas pico.','alta','abierto','2025-10-17 18:00:00','2025-10-19 18:00:00',NULL,8),(29,66,'Entrega no recibida','Atascos frecuentes al imprimir documentos largos.','media','cerrado','2025-10-21 22:00:00','2025-10-26 22:00:00','2025-10-28 15:05:45',7),(30,9,'Error al iniciar sesión','Reporte de cortes de conexión en horas pico.','media','cerrado','2025-10-24 12:00:00','2025-10-27 12:00:00',NULL,9),(31,76,'Impresora atora papel','Cámara 3 presenta imagen borrosa por la noche.','baja','cerrado','2025-10-25 03:00:00','2025-10-30 03:00:00',NULL,7),(32,58,'Impresora atora papel','Cámara 3 presenta imagen borrosa por la noche.','alta','en_progreso','2025-10-19 07:00:00','2025-10-26 07:00:00',NULL,4),(33,69,'Entrega no recibida','Usuario olvida contraseña con frecuencia.','alta','abierto','2025-10-19 17:00:00','2025-10-22 17:00:00',NULL,11),(34,22,'Intermitencia en Wi‑Fi','Reporte de cortes de conexión en horas pico.','media','en_progreso','2025-10-18 04:00:00','2025-10-25 04:00:00',NULL,11),(35,49,'Problema con facturación','Cámara 3 presenta imagen borrosa por la noche.','baja','cerrado','2025-10-23 11:00:00','2025-10-25 11:00:00',NULL,12),(36,69,'Impresora atora papel','Consulta sobre periodo de garantía extendida.','alta','en_progreso','2025-10-16 09:00:00','2025-10-23 09:00:00',NULL,3),(37,93,'Consulta garantía','Paquetería marcó entregado pero cliente no lo tiene.','alta','cerrado','2025-10-19 02:00:00','2025-10-25 02:00:00',NULL,6),(38,82,'Consulta garantía','Usuario olvida contraseña con frecuencia.','media','abierto','2025-10-17 02:00:00','2025-10-20 02:00:00',NULL,4),(39,59,'Problema con facturación','Reporte de cortes de conexión en horas pico.','baja','abierto','2025-10-17 12:00:00','2025-10-22 12:00:00',NULL,8),(40,1,'Intermitencia en Wi‑Fi','Cotización para 10 unidades con entrega en 48h.','media','cerrado','2025-10-15 14:00:00','2025-10-19 14:00:00',NULL,7),(41,40,'Intermitencia Wi-Fi','Cortes frecuentes en horas pico','alta','cerrado','0000-00-00 00:00:00','0000-00-00 00:00:00','2025-10-28 16:59:33',2),(45,1,'Test ticket from pytest','Created during automated test','media','abierto','2025-10-30 15:37:06',NULL,NULL,NULL),(46,1,'Test ticket from pytest','Created during automated test','media','abierto','2025-10-30 15:37:25',NULL,NULL,NULL),(47,1,'Test ticket from pytest','Created during automated test','media','abierto','2025-10-30 15:38:33',NULL,NULL,NULL),(48,1,'Test ticket from pytest','Created during automated test','media','abierto','2025-10-30 15:38:57',NULL,NULL,NULL),(49,1,'Test ticket from pytest','Created during automated test','media','abierto','2025-10-30 15:41:03',NULL,NULL,NULL),(50,1,'Test ticket from pytest','Created during automated test','media','abierto','2025-10-30 15:47:43',NULL,NULL,NULL),(51,1,'Test ticket from pytest','Created during automated test','media','abierto','2025-10-30 15:47:59',NULL,NULL,NULL),(52,1,'Test ticket from pytest','Created during automated test','media','abierto','2025-10-31 14:09:55',NULL,NULL,NULL),(53,1,'Test ticket from pytest','Created during automated test','media','abierto','2025-10-31 14:55:32',NULL,NULL,NULL),(54,1,'Test ticket from pytest','Created during automated test','media','abierto','2025-10-31 15:01:41',NULL,NULL,NULL);
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_ticket_set_resolved
BEFORE UPDATE ON ticket
FOR EACH ROW
BEGIN
  IF NEW.status = 'cerrado' AND OLD.status <> 'cerrado' AND NEW.resolved_at IS NULL THEN
    SET NEW.resolved_at = CURRENT_TIMESTAMP;
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Temporary table structure for view `v_catalog_effective_price`
--

DROP TABLE IF EXISTS `v_catalog_effective_price`;
/*!50001 DROP VIEW IF EXISTS `v_catalog_effective_price`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `v_catalog_effective_price` AS SELECT
 1 AS `catalog_id`,
  1 AS `product_id`,
  1 AS `product_name`,
  1 AS `catalog_name`,
  1 AS `base_price`,
  1 AS `discount_percentage`,
  1 AS `special_price`,
  1 AS `effective_price` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `v_order_totals`
--

DROP TABLE IF EXISTS `v_order_totals`;
/*!50001 DROP VIEW IF EXISTS `v_order_totals`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `v_order_totals` AS SELECT
 1 AS `order_id`,
  1 AS `v_subtotal`,
  1 AS `v_discount_total`,
  1 AS `v_tax_total`,
  1 AS `v_items_total` */;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `v_catalog_effective_price`
--

/*!50001 DROP VIEW IF EXISTS `v_catalog_effective_price`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_catalog_effective_price` AS select `cp`.`catalog_id` AS `catalog_id`,`cp`.`product_id` AS `product_id`,`p`.`name` AS `product_name`,`c`.`name` AS `catalog_name`,`p`.`price` AS `base_price`,`c`.`discount_percentage` AS `discount_percentage`,`cp`.`special_price` AS `special_price`,case when `cp`.`special_price` is not null then `cp`.`special_price` when `c`.`discount_percentage` > 0 then round(`p`.`price` * (1 - `c`.`discount_percentage` / 100),2) else `p`.`price` end AS `effective_price` from ((`catalog_product` `cp` join `product` `p` on(`p`.`product_id` = `cp`.`product_id`)) join `catalog` `c` on(`c`.`catalog_id` = `cp`.`catalog_id`)) where `c`.`active` = 1 and (`c`.`start_date` is null or `c`.`start_date` <= curdate()) and (`c`.`end_date` is null or `c`.`end_date` >= curdate()) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_order_totals`
--

/*!50001 DROP VIEW IF EXISTS `v_order_totals`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_order_totals` AS select `oi`.`order_id` AS `order_id`,round(sum(`oi`.`line_subtotal`),2) AS `v_subtotal`,round(sum(`oi`.`line_discount`),2) AS `v_discount_total`,round(sum(`oi`.`line_tax`),2) AS `v_tax_total`,round(sum(`oi`.`line_total`),2) AS `v_items_total` from `order_item` `oi` group by `oi`.`order_id` */;
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

-- Dump completed on 2025-10-31 15:19:25
