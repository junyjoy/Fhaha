-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema fhaa
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema fhaa
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `fhaa` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `fhaa` ;

-- -----------------------------------------------------
-- Table `fhaa`.`alembic_version`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fhaa`.`alembic_version` (
  `version_num` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`version_num`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `fhaa`.`hospital`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fhaa`.`hospital` (
  `hos_name` VARCHAR(20) NOT NULL,
  `hos_tel` VARCHAR(12) NOT NULL,
  `hos_addr1` VARCHAR(80) NOT NULL,
  `hos_cid` VARCHAR(10) NOT NULL,
  `hos_pwd` VARCHAR(102) NOT NULL,
  `hos_type` VARCHAR(20) NOT NULL,
  `hos_addr2` VARCHAR(80) NULL DEFAULT NULL,
  `hos_lat` FLOAT NOT NULL,
  `hos_lnt` FLOAT NOT NULL,
  PRIMARY KEY (`hos_cid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `fhaa`.`subject`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fhaa`.`subject` (
  `ill_pid` INT NOT NULL AUTO_INCREMENT,
  `ill_name` VARCHAR(40) NOT NULL,
  `ill_sym` VARCHAR(100) NOT NULL,
  `ill_type` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`ill_pid`))
ENGINE = InnoDB
AUTO_INCREMENT = 25
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `fhaa`.`hos_sub`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fhaa`.`hos_sub` (
  `sub_id` INT NOT NULL AUTO_INCREMENT,
  `hos_cid` VARCHAR(10) NOT NULL,
  `ill_pid` INT NOT NULL,
  PRIMARY KEY (`sub_id`, `hos_cid`, `ill_pid`),
  CONSTRAINT `hos_sub_ibfk_1`
    FOREIGN KEY (`hos_cid`)
    REFERENCES `fhaa`.`hospital` (`hos_cid`),
  CONSTRAINT `hos_sub_ibfk_2`
    FOREIGN KEY (`ill_pid`)
    REFERENCES `fhaa`.`subject` (`ill_pid`))
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `fhaa`.`doctor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fhaa`.`doctor` (
  `doc_name` VARCHAR(20) NOT NULL,
  `doc_type` VARCHAR(20) NOT NULL,
  `doc_pid` VARCHAR(10) NOT NULL,
  `ill_pid` INT NOT NULL,
  `sub_id` INT NOT NULL,
  `hos_cid` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`doc_pid`, `ill_pid`, `sub_id`, `hos_cid`),
  CONSTRAINT `doctor_ibfk_1`
    FOREIGN KEY (`sub_id` , `hos_cid` , `ill_pid`)
    REFERENCES `fhaa`.`hos_sub` (`sub_id` , `hos_cid` , `ill_pid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `fhaa`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fhaa`.`user` (
  `pat_name` VARCHAR(10) NOT NULL,
  `pat_bir` DATE NOT NULL,
  `pat_ema` VARCHAR(30) NOT NULL,
  `pat_pw` VARCHAR(102) NOT NULL,
  `pat_tel` VARCHAR(11) NOT NULL,
  PRIMARY KEY (`pat_ema`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `fhaa`.`request`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fhaa`.`request` (
  `req_id` INT NOT NULL AUTO_INCREMENT,
  `pat_ema` VARCHAR(30) NOT NULL,
  `req_type` VARCHAR(20) NOT NULL,
  `req_time` VARCHAR(20) NOT NULL,
  `req_date` DATETIME NOT NULL,
  `req_loc` VARCHAR(80) NOT NULL,
  `req_req` VARCHAR(200) NOT NULL,
  `hos_cid` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`req_id`, `pat_ema`),
  CONSTRAINT `hos_cid`
    FOREIGN KEY (`hos_cid`)
    REFERENCES `fhaa`.`hospital` (`hos_cid`),
  CONSTRAINT `pad_ema`
    FOREIGN KEY (`pat_ema`)
    REFERENCES `fhaa`.`user` (`pat_ema`))
ENGINE = InnoDB
AUTO_INCREMENT = 17
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `fhaa`.`matching`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fhaa`.`matching` (
  `mat_id` INT NOT NULL AUTO_INCREMENT,
  `req_id` INT NOT NULL,
  `hos_cid` VARCHAR(10) NOT NULL,
  `pat_ema` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`mat_id`, `req_id`, `hos_cid`, `pat_ema`),
  CONSTRAINT `matching_ibfk_1`
    FOREIGN KEY (`hos_cid`)
    REFERENCES `fhaa`.`hospital` (`hos_cid`),
  CONSTRAINT `matching_ibfk_2`
    FOREIGN KEY (`req_id` , `pat_ema`)
    REFERENCES `fhaa`.`request` (`req_id` , `pat_ema`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
