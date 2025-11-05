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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alert`
--

LOCK TABLES `alert` WRITE;
/*!40000 ALTER TABLE `alert` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_user`
--

LOCK TABLES `app_user` WRITE;
/*!40000 ALTER TABLE `app_user` DISABLE KEYS */;
INSERT INTO `app_user` VALUES (1,'Administrador General','admin','admin@omnidesk.com','$2b$12$cr7UMDpdfvvWHlg9eNl8QeLdUCSWqASZ7aFxQQXf3NmbTFUHcNfdq','admin',1,NULL,NULL,0,NULL,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(2,'Empleado de Ventas','employee','empleado@omnidesk.com','$2b$12$RjLvXCUhFvbvlKsC14POpukZ8ldz6Yc42ZKiaE9O8FM2SEYVLYQ5K','empleado',1,NULL,NULL,0,NULL,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(3,'Dev Seed x0chipa','x0chipa','dev+x0chipa@example.test','$2b$12$UkrAK241xqMT917QbQyVnuVR3oI1lq7vWSVKY0sAhjOeqYf7ys7PK','admin',1,NULL,NULL,0,NULL,'2025-11-05 21:08:20','2025-11-05 21:08:20');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calendar_event`
--

LOCK TABLES `calendar_event` WRITE;
/*!40000 ALTER TABLE `calendar_event` DISABLE KEYS */;
INSERT INTO `calendar_event` VALUES (1,'Test Event pytest','Event created during test','2025-11-01 09:00:00','2025-11-01 10:00:00',NULL,NULL);
/*!40000 ALTER TABLE `calendar_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cart` (
  `cart_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) DEFAULT NULL,
  `status` enum('active','checked_out','abandoned') NOT NULL DEFAULT 'active',
  `metadata` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`metadata`)),
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`cart_id`),
  KEY `idx_cart_client` (`client_id`),
  KEY `idx_cart_status` (`status`),
  KEY `idx_cart_updated_at` (`updated_at`),
  CONSTRAINT `fk_cart_client` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart_item`
--

DROP TABLE IF EXISTS `cart_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cart_item` (
  `cart_item_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `cart_id` bigint(20) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(10) unsigned NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `catalog_special_price` decimal(10,2) DEFAULT NULL,
  `applied_catalog_discount_pct` decimal(5,4) DEFAULT NULL,
  `final_price` decimal(10,2) NOT NULL,
  `sku` varchar(64) DEFAULT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `tax_rate` decimal(5,2) DEFAULT NULL,
  `added_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`cart_item_id`),
  KEY `idx_ci_cart` (`cart_id`),
  KEY `idx_ci_product` (`product_id`),
  CONSTRAINT `fk_ci_cart` FOREIGN KEY (`cart_id`) REFERENCES `cart` (`cart_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_item`
--

LOCK TABLES `cart_item` WRITE;
/*!40000 ALTER TABLE `cart_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `cart_item` ENABLE KEYS */;
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
  `start_date` date DEFAULT curdate(),
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
INSERT INTO `catalog` VALUES (1,'Black Friday','Descuentos especiales de temporada',25.00,'2025-11-05','2025-12-05','todos',1,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(2,'Clientes Premium','Ofertas exclusivas para clientes premium',15.00,'2025-11-05','2025-12-05','premium',1,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(3,'Verano Tech','Descuentos en electrónica y gadgets',10.00,'2025-11-05','2025-12-05','todos',1,'2025-11-05 21:08:18','2025-11-05 21:08:18');
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
INSERT INTO `catalog_product` VALUES (1,1,NULL,9),(1,3,NULL,15),(1,5,NULL,1),(1,8,NULL,19),(1,9,NULL,3),(1,13,NULL,19),(1,14,NULL,25),(1,15,NULL,6),(2,1,NULL,4),(2,2,NULL,4),(2,3,NULL,1),(2,5,NULL,10),(2,9,NULL,3),(2,10,NULL,5),(2,12,NULL,26),(2,15,NULL,11),(2,18,NULL,1),(3,8,NULL,31),(3,9,NULL,5),(3,12,NULL,13),(3,15,NULL,4),(3,16,NULL,2),(3,17,NULL,9);
/*!40000 ALTER TABLE `catalog_product` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
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
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
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
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Electrónica',NULL,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(2,'Computadoras',1,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(3,'Smartphones',1,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(4,'Accesorios',1,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(5,'Redes',1,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(6,'Audio y Video',1,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(7,'Hogar y Oficina',NULL,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(8,'Muebles',7,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(9,'Electrodomésticos',7,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(10,'Papelería',7,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(11,'Decoración',7,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(12,'Moda',NULL,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(13,'Ropa',12,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(14,'Zapatos',12,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(15,'Accesorios de Moda',12,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(16,'Deportes',NULL,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(17,'Fitness',16,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(18,'Ciclismo',16,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(19,'Natación',16,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(20,'Senderismo',16,'2025-11-05 21:08:18','2025-11-05 21:08:18'),(21,'test-cat-1762376902',NULL,'2025-11-05 21:08:22','2025-11-05 21:08:22');
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
INSERT INTO `client` VALUES (1,'María López','+5215512345678','maria@example.com',NULL,NULL,'normal','active','2025-11-05 15:08:18','2025-11-05 21:08:18',NULL,NULL,NULL),(2,'Carlos Hernández','+5215511111111','carlos@example.com',NULL,NULL,'normal','active','2025-11-05 15:08:18','2025-11-05 21:08:18',NULL,NULL,NULL),(3,'Ana Pérez','+5215522222222','ana@example.com',NULL,NULL,'normal','active','2025-11-05 15:08:18','2025-11-05 21:08:18',NULL,NULL,NULL),(4,'Luis González','+5215533333333','luis@example.com',NULL,NULL,'normal','active','2025-11-05 15:08:18','2025-11-05 21:08:18',NULL,NULL,NULL),(5,'Fernanda Castillo','+5215544444444','fer@example.com',NULL,NULL,'normal','active','2025-11-05 15:08:18','2025-11-05 21:08:18',NULL,NULL,NULL),(6,'Ana Cliente','+521f03b4071','ana.client+8f3c7535@example.com',NULL,NULL,'normal','active','2025-11-05 15:08:22','2025-11-05 21:08:22',NULL,NULL,NULL),(7,'Premium Test','99db4b432','prem+9db4b432@test.com',NULL,NULL,'premium','active','2025-11-05 15:08:22','2025-11-05 21:08:22',NULL,NULL,NULL);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conversation`
--

LOCK TABLES `conversation` WRITE;
/*!40000 ALTER TABLE `conversation` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_order`
--

LOCK TABLES `customer_order` WRITE;
/*!40000 ALTER TABLE `customer_order` DISABLE KEYS */;
INSERT INTO `customer_order` VALUES (1,6,'2025-11-05 15:08:22','2025-11-05 21:08:22','borrador','pendiente',14500.00,0.00,0.00,0.00,14500.00,'Order from test',NULL,NULL),(2,7,'2025-11-05 15:08:22','2025-11-05 21:08:22','borrador','pendiente',14500.00,725.00,0.00,0.00,13775.00,'Premium order',NULL,NULL),(3,1,'2025-11-05 15:16:08','2025-11-05 21:16:08','borrador','pendiente',29000.00,0.00,0.00,0.00,29000.00,NULL,NULL,NULL),(4,1,'2025-11-05 15:20:32','2025-11-05 21:20:32','borrador','pendiente',75600.00,0.00,0.00,0.00,75600.00,NULL,NULL,NULL),(5,1,'2025-11-05 15:23:35','2025-11-05 21:23:36','borrador','pendiente',75600.00,0.00,0.00,0.00,75600.00,NULL,NULL,NULL),(6,1,'2025-11-05 15:30:46','2025-11-05 21:30:46','borrador','pendiente',75600.00,0.00,0.00,0.00,75600.00,NULL,NULL,NULL),(7,1,'2025-11-05 15:39:45','2025-11-05 21:39:45','borrador','pendiente',75600.00,0.00,0.00,0.00,75600.00,NULL,NULL,NULL),(8,1,'2025-11-05 15:42:03','2025-11-05 21:42:03','borrador','pendiente',75600.00,0.00,0.00,0.00,75600.00,NULL,NULL,NULL),(9,1,'2025-11-05 15:45:57','2025-11-05 21:45:57','borrador','pendiente',75600.00,0.00,0.00,0.00,75600.00,NULL,NULL,NULL);
/*!40000 ALTER TABLE `customer_order` ENABLE KEYS */;
UNLOCK TABLES;

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
  `billing_name` varchar(150) DEFAULT NULL,
  `rfc` varchar(13) DEFAULT NULL,
  `regimen_fiscal` varchar(120) DEFAULT NULL,
  `fiscal_postal_code` varchar(10) DEFAULT NULL,
  `billing_address` text DEFAULT NULL,
  `uso_cfdi` varchar(10) DEFAULT NULL,
  `forma_pago` varchar(50) DEFAULT NULL,
  `metodo_pago` varchar(50) DEFAULT NULL,
  `series` varchar(10) DEFAULT NULL,
  `issued_at` datetime NOT NULL DEFAULT current_timestamp(),
  `due_at` datetime DEFAULT NULL,
  `currency_code` char(3) NOT NULL DEFAULT 'MXN',
  `exchange_rate` decimal(18,6) DEFAULT NULL,
  `status` enum('emitida','pagada','parcial','cancelada') NOT NULL DEFAULT 'emitida',
  `notes` text DEFAULT NULL,
  PRIMARY KEY (`invoice_id`),
  UNIQUE KEY `uq_invoice_order_number` (`order_id`,`invoice_number`),
  KEY `idx_invoice_issued_at` (`issued_at`),
  KEY `idx_invoice_number` (`invoice_number`),
  CONSTRAINT `fk_invoice_order` FOREIGN KEY (`order_id`) REFERENCES `customer_order` (`order_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice`
--

LOCK TABLES `invoice` WRITE;
/*!40000 ALTER TABLE `invoice` DISABLE KEYS */;
/*!40000 ALTER TABLE `invoice` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
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
INSERT INTO `order_item` VALUES (1,1,1,'Laptop HP Pavilion 15','EL-1001',14500.00,NULL,NULL,0.00,14500.00,0.00,14500.00,0.00,14500.00),(2,1,1,'Laptop HP Pavilion 15','EL-1001',14500.00,0.05,725.00,0.00,14500.00,725.00,13775.00,0.00,13775.00),(3,1,2,'Laptop HP Pavilion 15','EL-1001',14500.00,NULL,NULL,0.00,29000.00,0.00,29000.00,0.00,29000.00),(4,1,3,'Laptop HP Pavilion 15','EL-1001',14500.00,NULL,NULL,0.00,43500.00,0.00,43500.00,0.00,43500.00),(4,2,1,'Apple iPhone 14 128GB','EL-1002',18500.00,NULL,NULL,0.00,18500.00,0.00,18500.00,0.00,18500.00),(4,3,2,'Audífonos Sony WH-1000XM5','EL-1003',6800.00,NULL,NULL,0.00,13600.00,0.00,13600.00,0.00,13600.00),(5,1,3,'Laptop HP Pavilion 15','EL-1001',14500.00,NULL,NULL,0.00,43500.00,0.00,43500.00,0.00,43500.00),(5,2,1,'Apple iPhone 14 128GB','EL-1002',18500.00,NULL,NULL,0.00,18500.00,0.00,18500.00,0.00,18500.00),(5,3,2,'Audífonos Sony WH-1000XM5','EL-1003',6800.00,NULL,NULL,0.00,13600.00,0.00,13600.00,0.00,13600.00),(6,1,3,'Laptop HP Pavilion 15','EL-1001',14500.00,NULL,NULL,0.00,43500.00,0.00,43500.00,0.00,43500.00),(6,2,1,'Apple iPhone 14 128GB','EL-1002',18500.00,NULL,NULL,0.00,18500.00,0.00,18500.00,0.00,18500.00),(6,3,2,'Audífonos Sony WH-1000XM5','EL-1003',6800.00,NULL,NULL,0.00,13600.00,0.00,13600.00,0.00,13600.00),(7,1,3,'Laptop HP Pavilion 15','EL-1001',14500.00,NULL,NULL,0.00,43500.00,0.00,43500.00,0.00,43500.00),(7,2,1,'Apple iPhone 14 128GB','EL-1002',18500.00,NULL,NULL,0.00,18500.00,0.00,18500.00,0.00,18500.00),(7,3,2,'Audífonos Sony WH-1000XM5','EL-1003',6800.00,NULL,NULL,0.00,13600.00,0.00,13600.00,0.00,13600.00),(8,1,3,'Laptop HP Pavilion 15','EL-1001',14500.00,NULL,NULL,0.00,43500.00,0.00,43500.00,0.00,43500.00),(8,2,1,'Apple iPhone 14 128GB','EL-1002',18500.00,NULL,NULL,0.00,18500.00,0.00,18500.00,0.00,18500.00),(8,3,2,'Audífonos Sony WH-1000XM5','EL-1003',6800.00,NULL,NULL,0.00,13600.00,0.00,13600.00,0.00,13600.00),(9,1,3,'Laptop HP Pavilion 15','EL-1001',14500.00,NULL,NULL,0.00,43500.00,0.00,43500.00,0.00,43500.00),(9,2,1,'Apple iPhone 14 128GB','EL-1002',18500.00,NULL,NULL,0.00,18500.00,0.00,18500.00,0.00,18500.00),(9,3,2,'Audífonos Sony WH-1000XM5','EL-1003',6800.00,NULL,NULL,0.00,13600.00,0.00,13600.00,0.00,13600.00);
/*!40000 ALTER TABLE `order_item` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
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
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
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
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
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
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'EL-1001','Laptop HP Pavilion 15','Intel i5, 8GB RAM, 512GB SSD',NULL,2,14500.00,25,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(2,'EL-1002','Apple iPhone 14 128GB','Pantalla OLED de 6.1 pulgadas, cámara dual',NULL,3,18500.00,15,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(3,'EL-1003','Audífonos Sony WH-1000XM5','Cancelación activa de ruido',NULL,6,6800.00,30,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(4,'EL-1004','Teclado Mecánico Logitech G Pro','Switches GX Blue, RGB',NULL,4,2200.00,40,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(5,'EL-1005','Router TP-Link Archer AX50','Wi-Fi 6, Dual Band, 3 Gbps',NULL,5,2100.00,20,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(6,'EL-1006','Monitor Dell Ultrasharp 27\"','Resolución QHD, panel IPS',NULL,2,7200.00,18,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(7,'EL-1007','Disco Duro Externo Seagate 2TB','USB 3.0, portátil',NULL,4,1500.00,60,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(8,'EL-1008','Cable HDMI 2.1 2m','Soporta 8K UHD y HDR',NULL,4,180.00,200,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(9,'HO-2001','Silla Ergonómica de Oficina','Respaldo de malla, soporte lumbar',NULL,8,3200.00,12,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(10,'HO-2002','Escritorio de Madera 120cm','Color nogal con estructura metálica',NULL,8,2800.00,10,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(11,'HO-2003','Refrigerador LG Smart Inverter','Capacidad 420L, eficiencia A+',NULL,9,9800.00,8,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(12,'HO-2004','Lámpara de Escritorio LED','Luz blanca cálida, regulable',NULL,11,450.00,100,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(13,'HO-2005','Paquete de hojas tamaño carta','500 hojas blancas',NULL,10,95.00,400,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(14,'MO-3001','Playera Nike Dri-FIT','Tela transpirable, color negro',NULL,13,550.00,80,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(15,'MO-3002','Tenis Adidas Ultraboost 23','Amortiguación premium',NULL,14,2800.00,40,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(16,'MO-3003','Reloj Casio Vintage Dorado','Resistente al agua, estilo clásico',NULL,15,900.00,30,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(17,'DE-4001','Mancuernas Ajustables 24kg','Set ajustable con selector rápido',NULL,17,3500.00,25,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(18,'DE-4002','Bicicleta de Montaña Trek Marlin 7','Cuadro de aluminio, frenos de disco',NULL,18,15800.00,6,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(19,'DE-4003','Gafas de Natación Speedo Aquapulse','Antivaho y protección UV',NULL,19,480.00,50,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(20,'DE-4004','Mochila de Senderismo 50L','Impermeable con soporte lumbar',NULL,20,1200.00,35,'active','2025-11-05 21:08:18','2025-11-05 21:08:18'),(21,'RB-e2e888de','RB Product 3',NULL,NULL,NULL,30.00,2,'active','2025-11-05 21:08:23','2025-11-05 21:08:23');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
INSERT INTO `ticket` VALUES (1,1,'Test ticket from pytest','Created during automated test','media','abierto','2025-11-05 15:08:23',NULL,NULL,NULL);
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
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
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
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
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
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

-- Dump completed on 2025-11-05 15:46:30
