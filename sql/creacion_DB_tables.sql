-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema diary
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema diary
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `diary` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------
-- Schema 
-- -----------------------------------------------------
USE `diary` ;

-- -----------------------------------------------------
-- Table `diary`.`etiquetas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diary`.`etiquetas` (
  `id_etiqueta` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  PRIMARY KEY (`id_etiqueta`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `diary`.`propietarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diary`.`propietarios` (
  `id_propietario` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `direccion` VARCHAR(45) NULL,
  `mail` VARCHAR(45) NULL,
  `telefono` VARCHAR(45) NULL,
  `latitud` VARCHAR(45) NULL,
  `longitud` VARCHAR(45) NULL,
  `pass` VARCHAR(45) NULL,
  PRIMARY KEY (`id_propietario`),
  UNIQUE INDEX `mail_UNIQUE` (`mail` ASC) VISIBLE,
  UNIQUE INDEX `telefono_UNIQUE` (`telefono` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `diary`.`paises`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diary`.`paises` (
  `id_pais` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `acron` VARCHAR(45) NULL,
  PRIMARY KEY (`id_pais`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC) VISIBLE,
  UNIQUE INDEX `acron_UNIQUE` (`acron` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `diary`.`ciudades`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diary`.`ciudades` (
  `id_ciudad` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  PRIMARY KEY (`id_ciudad`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `diary`.`municipios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diary`.`municipios` (
  `id_municipio` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  PRIMARY KEY (`id_municipio`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `diary`.`cp`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diary`.`cp` (
  `id_cp` INT NOT NULL AUTO_INCREMENT,
  `codigo` INT NULL,
  PRIMARY KEY (`id_cp`),
  UNIQUE INDEX `codigo_UNIQUE` (`codigo` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `diary`.`restaurantes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diary`.`restaurantes` (
  `id_rest` INT NOT NULL AUTO_INCREMENT,
  `clave` VARCHAR(45) NULL COMMENT 'Mira a ver si encuentras algo que identifique de manera única este sitio, a las malas puedes usar latitud y longitud que deberían de ser únicas.',
  `nombre` VARCHAR(100) NULL,
  `direccion` VARCHAR(150) NULL,
  `latitud` VARCHAR(45) NULL,
  `longitud` VARCHAR(45) NULL,
  `telefono` INT NULL COMMENT 'Mira a ver si puedes alimentar esta parte',
  `web` VARCHAR(45) NULL COMMENT 'Mira a ver si puedes alimentar esta parte',
  `id_etiqueta` INT NULL,
  `id_propietario` INT NULL,
  `id_pais` INT NULL,
  `id_ciudad` INT NULL,
  `id_municipio` INT NULL,
  `id_cp` INT NULL,
  PRIMARY KEY (`id_rest`),
  INDEX `fk_restaurantes_etiquetas1_idx` (`id_etiqueta` ASC) VISIBLE,
  INDEX `fk_restaurantes_propietarios1_idx` (`id_propietario` ASC) VISIBLE,
  INDEX `fk_restaurantes_paises1_idx` (`id_pais` ASC) VISIBLE,
  INDEX `fk_restaurantes_ciudades1_idx` (`id_ciudad` ASC) VISIBLE,
  INDEX `fk_restaurantes_municipios1_idx` (`id_municipio` ASC) VISIBLE,
  UNIQUE INDEX `telefono_UNIQUE` (`telefono` ASC) VISIBLE,
  UNIQUE INDEX `web_UNIQUE` (`web` ASC) VISIBLE,
  UNIQUE INDEX `direccion_UNIQUE` (`direccion` ASC) VISIBLE,
  UNIQUE INDEX `clave_UNIQUE` (`clave` ASC) VISIBLE,
  INDEX `fk_restaurantes_cp1_idx` (`id_cp` ASC) VISIBLE,
  CONSTRAINT `fk_restaurantes_etiquetas1`
    FOREIGN KEY (`id_etiqueta`)
    REFERENCES `diary`.`etiquetas` (`id_etiqueta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_restaurantes_propietarios1`
    FOREIGN KEY (`id_propietario`)
    REFERENCES `diary`.`propietarios` (`id_propietario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_restaurantes_paises1`
    FOREIGN KEY (`id_pais`)
    REFERENCES `diary`.`paises` (`id_pais`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_restaurantes_ciudades1`
    FOREIGN KEY (`id_ciudad`)
    REFERENCES `diary`.`ciudades` (`id_ciudad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_restaurantes_municipios1`
    FOREIGN KEY (`id_municipio`)
    REFERENCES `diary`.`municipios` (`id_municipio`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_restaurantes_cp1`
    FOREIGN KEY (`id_cp`)
    REFERENCES `diary`.`cp` (`id_cp`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `diary`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diary`.`usuarios` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(20) NULL,
  `apellidos` VARCHAR(35) NULL,
  `mail` VARCHAR(33) NULL,
  `telefono` VARCHAR(45) NULL,
  `direccion` VARCHAR(45) NULL,
  `latitud` VARCHAR(45) NULL,
  `longitud` VARCHAR(45) NULL,
  `pass` VARCHAR(45) NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE INDEX `telefono_UNIQUE` (`telefono` ASC) VISIBLE,
  UNIQUE INDEX `mail_UNIQUE` (`mail` ASC) VISIBLE)
ENGINE = InnoDB
COMMENT = '            ';


-- -----------------------------------------------------
-- Table `diary`.`visitado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diary`.`visitado` (
  `id_visitado` INT NOT NULL AUTO_INCREMENT,
  `valoracion` INT NULL,
  `comentario` VARCHAR(300) NULL,
  `fecha` DATETIME NULL,
  `id_usuario` INT NOT NULL,
  `id_rest` INT NOT NULL,
  PRIMARY KEY (`id_visitado`),
  INDEX `fk_visitado_usuario1_idx` (`id_usuario` ASC) VISIBLE,
  INDEX `fk_visitado_restaurantes1_idx` (`id_rest` ASC) VISIBLE,
  CONSTRAINT `fk_visitado_usuario1`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `diary`.`usuarios` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_visitado_restaurantes1`
    FOREIGN KEY (`id_rest`)
    REFERENCES `diary`.`restaurantes` (`id_rest`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `diary`.`itinerario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diary`.`itinerario` (
  `id_iti` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `visitado` TINYINT NULL,
  `id_usuario` INT NOT NULL,
  `id_rest` INT NOT NULL,
  PRIMARY KEY (`id_iti`),
  INDEX `fk_itinerario_usuario1_idx` (`id_usuario` ASC) VISIBLE,
  INDEX `fk_itinerario_restaurantes1_idx` (`id_rest` ASC) VISIBLE,
  CONSTRAINT `fk_itinerario_usuario1`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `diary`.`usuarios` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_itinerario_restaurantes1`
    FOREIGN KEY (`id_rest`)
    REFERENCES `diary`.`restaurantes` (`id_rest`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `diary`.`platos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diary`.`platos` (
  `id_plato` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `puntuacion` VARCHAR(45) NULL,
  `comentario` VARCHAR(300) NULL,
  `id_usuario` INT NOT NULL,
  `id_rest` INT NOT NULL,
  PRIMARY KEY (`id_plato`),
  INDEX `fk_plato_usuario1_idx` (`id_usuario` ASC) VISIBLE,
  INDEX `fk_plato_restaurantes1_idx` (`id_rest` ASC) VISIBLE,
  CONSTRAINT `fk_plato_usuario1`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `diary`.`usuarios` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_plato_restaurantes1`
    FOREIGN KEY (`id_rest`)
    REFERENCES `diary`.`restaurantes` (`id_rest`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
