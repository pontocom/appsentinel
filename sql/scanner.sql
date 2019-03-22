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

CREATE TABLE apk2scan(
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  md5 VARCHAR(32) NOT NULL ,
  created_at DATETIME NOT NULL
);