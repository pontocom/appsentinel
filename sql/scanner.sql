CREATE TABLE apk (
  md5 VARCHAR(32) PRIMARY KEY NOT NULL ,
  applicationName TEXT NOT NULL ,
  applicationPackage TEXT NOT NULL ,
  applicationVersion TEXT,
  applicationPath TEXT,
  apkFile TEXT ,
  status BOOL NOT NULL ,
  created_at DATETIME NOT NULL,
  updated_at DATETIME
);

CREATE TABLE apk2scan (
  id INT PRIMARY KEY AUTO_INCREMENT,
  md5 VARCHAR(32) NOT NULL,
  created_at DATETIME  NOT NULL
);

CREATE TABLE apkscantools (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(32) NOT NULL
);

CREATE TABLE apkresults (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  md5 VARCHAR(32) NOT NULL ,
  scantool VARCHAR(32) NOT NULL ,
  results_location VARCHAR(128) NOT NULL ,
  created_at DATETIME NOT NULL
);

-- -----------------------------------------------------
-- Table `apkscanner`.`apk_has_scan_tools`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `apkscanner`.`apk_has_scan_tools` (
  `apk_md5` VARCHAR(32) NOT NULL,
  `scan_tools_idscan_tools` INT NOT NULL,
  PRIMARY KEY (`apk_md5`, `scan_tools_idscan_tools`),
  INDEX `fk_apk_has_scan_tools_scan_tools1_idx` (`scan_tools_idscan_tools` ASC) VISIBLE,
  INDEX `fk_apk_has_scan_tools_apk_idx` (`apk_md5` ASC) VISIBLE,
  CONSTRAINT `fk_apk_has_scan_tools_apk`
    FOREIGN KEY (`apk_md5`)
    REFERENCES `apkscanner`.`apk` (`md5`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_apk_has_scan_tools_scan_tools1`
    FOREIGN KEY (`scan_tools_idscan_tools`)
    REFERENCES `apkscanner`.`scan_tools` (`idscan_tools`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `apkscanner`.`apk_results`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `apkscanner`.`apk_results` (
  `idapk_results` INT NOT NULL AUTO_INCREMENT,
  `scan_tools_idscan_tools` INT NOT NULL,
  `apk_md5` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`idapk_results`, `scan_tools_idscan_tools`, `apk_md5`),
  INDEX `fk_apk_results_scan_tools1_idx` (`scan_tools_idscan_tools` ASC) VISIBLE,
  INDEX `fk_apk_results_apk1_idx` (`apk_md5` ASC) VISIBLE,
  CONSTRAINT `fk_apk_results_scan_tools1`
    FOREIGN KEY (`scan_tools_idscan_tools`)
    REFERENCES `apkscanner`.`scan_tools` (`idscan_tools`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_apk_results_apk1`
    FOREIGN KEY (`apk_md5`)
    REFERENCES `apkscanner`.`apk` (`md5`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


