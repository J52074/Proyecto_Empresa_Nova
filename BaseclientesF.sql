-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: cliente
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `ID_Cliente` char(12) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Primer_apellido` varchar(100) NOT NULL,
  `Segundo_apellido` varchar(100) NOT NULL,
  `Correo_electronico` varchar(100) NOT NULL,
  `Telefono` char(8) NOT NULL,
  `FK_Factura` int DEFAULT NULL,
  `FK_Pais` char(2) NOT NULL,
  `FK_Direccion` char(5) NOT NULL,
  PRIMARY KEY (`ID_Cliente`),
  KEY `idx_fk_factura` (`FK_Factura`),
  KEY `idx_fk_pais` (`FK_Pais`),
  KEY `idx_fk_direccion` (`FK_Direccion`),
  CONSTRAINT `fk_cliente_direccion` FOREIGN KEY (`FK_Direccion`) REFERENCES `direccion` (`ID_Direccion`),
  CONSTRAINT `fk_cliente_factura` FOREIGN KEY (`FK_Factura`) REFERENCES `facturas` (`ID_Factura`),
  CONSTRAINT `fk_cliente_pais` FOREIGN KEY (`FK_Pais`) REFERENCES `pais` (`ID_Pais`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES ('201110221','Alonso','Chaves','Brenes','esteban@example.com','87654321',NULL,'CR','30101'),('301110221','Jeniffer','Arias','Brenes','esteban@example.com','88888888',2270,'CR','30101'),('701110221','Mario','Chaves','Alcaceres','alcaceres@example.com','87654320',NULL,'CR','30101');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `direccion`
--

DROP TABLE IF EXISTS `direccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `direccion` (
  `ID_Direccion` char(5) NOT NULL,
  `Provincia` char(1) DEFAULT NULL,
  `Canton` char(2) DEFAULT NULL,
  `Distrito` char(2) DEFAULT NULL,
  PRIMARY KEY (`ID_Direccion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direccion`
--

LOCK TABLES `direccion` WRITE;
/*!40000 ALTER TABLE `direccion` DISABLE KEYS */;
INSERT INTO `direccion` VALUES ('10101','1','01','01'),('10201','1','02','01'),('20101','2','01','01'),('30101','3','01','01'),('30102','3','01','02'),('40101','4','01','01'),('60101','6','01','01');
/*!40000 ALTER TABLE `direccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facturas`
--

DROP TABLE IF EXISTS `facturas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facturas` (
  `ID_Factura` int NOT NULL AUTO_INCREMENT,
  `Fecha` datetime DEFAULT NULL,
  `Total_compra` decimal(7,2) DEFAULT NULL,
  `Detalle_Productos` text,
  PRIMARY KEY (`ID_Factura`)
) ENGINE=InnoDB AUTO_INCREMENT=8209 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facturas`
--

LOCK TABLES `facturas` WRITE;
/*!40000 ALTER TABLE `facturas` DISABLE KEYS */;
INSERT INTO `facturas` VALUES (105,NULL,NULL,'[{\"codigo\": \"P01\", \"nombre\": \"Teclado Mecánico\", \"cantidad\": 1}, {\"codigo\": \"P05\", \"nombre\": \"Mouse Inalámbrico\", \"cantidad\": 2}]'),(2270,NULL,NULL,'[{\"codigo\": \"P01\", \"nombre\": \"Teclado Mecánico RGB\", \"cantidad\": 1}, {\"codigo\": \"P05\", \"nombre\": \"Mouse Inalámbrico Pro\", \"cantidad\": 3}]'),(8208,NULL,NULL,'[{\"codigo\": \"P01\", \"nombre\": \"Teclado Mecánico RGB\", \"cantidad\": 1}, {\"codigo\": \"P05\", \"nombre\": \"Mouse Inalámbrico Pro\", \"cantidad\": 3}]');
/*!40000 ALTER TABLE `facturas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pais`
--

DROP TABLE IF EXISTS `pais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pais` (
  `ID_Pais` char(2) NOT NULL,
  `Detalle` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID_Pais`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pais`
--

LOCK TABLES `pais` WRITE;
/*!40000 ALTER TABLE `pais` DISABLE KEYS */;
INSERT INTO `pais` VALUES ('CO','Colombia'),('CR','Costa Rica'),('ES','España'),('MX','México'),('PA','Panamá');
/*!40000 ALTER TABLE `pais` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'cliente'
--
/*!50003 DROP PROCEDURE IF EXISTS `Mantenimiento_Cliente` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `Mantenimiento_Cliente`(
    IN p_id_cliente CHAR(12),
    IN p_nombre VARCHAR(100),
    IN p_primer_apellido VARCHAR(100),
    IN p_segundo_apellido VARCHAR(100),
    IN p_correo_electronico VARCHAR(100),
    IN p_telefono CHAR(8),
    IN p_fk_factura INT,
    IN p_fk_pais CHAR(2),
    IN p_fk_direccion CHAR(5),
    IN p_opcion INT
)
BEGIN
    -- Agregar un cliente
    IF p_opcion = 1 THEN
        INSERT INTO Cliente (ID_Cliente, Nombre, Primer_apellido, Segundo_apellido, Correo_electronico, Telefono, FK_Pais, FK_Direccion)
        VALUES (p_id_cliente, p_nombre, p_primer_apellido, p_segundo_apellido, p_correo_electronico, p_telefono, p_fk_pais, p_fk_direccion);

    -- Borrar un cliente
    ELSEIF p_opcion = 2 THEN
        DELETE FROM Cliente
        WHERE ID_Cliente = p_id_cliente;

    -- Modificar un cliente
    ELSEIF p_opcion = 3 THEN
        UPDATE Cliente
        SET Nombre = COALESCE(p_nombre, Nombre),
            Primer_apellido = COALESCE(p_primer_apellido, Primer_apellido),
            Segundo_apellido = COALESCE(p_segundo_apellido, Segundo_apellido),
            Correo_electronico = COALESCE(p_correo_electronico, Correo_electronico),
            Telefono = COALESCE(p_telefono, Telefono),
            FK_Pais = COALESCE(p_fk_pais, FK_Pais),
            FK_Direccion = COALESCE(p_fk_direccion, FK_Direccion)
        WHERE ID_Cliente = p_id_cliente;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `Mantenimiento_Cliente_Con_Factura` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `Mantenimiento_Cliente_Con_Factura`(
    IN p_id_cliente CHAR(12),
    IN p_id_factura INT,
    IN p_detalle_productos TEXT,
    IN p_accion INT -- 1: Agregar con datos V2, etc.
)
BEGIN
    -- 1. Registrar o actualizar la factura y sus productos en la tabla Facturas
    INSERT INTO Facturas (ID_Factura, Detalle_Productos)
    VALUES (p_id_factura, p_detalle_productos)
    ON DUPLICATE KEY UPDATE Detalle_Productos = p_detalle_productos;

    -- 2. Actualizar o insertar el cliente asociando la factura (FK_Factura)
    -- Ajusta los campos según tu tabla Cliente real
    IF p_accion = 1 THEN
        -- Ejemplo de actualización del cliente existente para asignarle la factura del V2
        UPDATE Cliente 
        SET FK_Factura = p_id_factura 
        WHERE ID_Cliente = p_id_cliente;
    END IF;
    
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `Registrar_Operacion_Almacen4` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `Registrar_Operacion_Almacen4`(
    IN p_id_cliente CHAR(12),
    IN p_estado VARCHAR(50),
    IN p_detalle TEXT
)
BEGIN
    INSERT INTO Registro_Almacen4 (ID_Cliente, Estado_Simulador, Detalle_Respuesta)
    VALUES (p_id_cliente, p_estado, p_detalle);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-02 17:32:53
