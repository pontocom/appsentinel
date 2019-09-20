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
  status INTEGER NOT NULL,
  details TEXT ,
  created_at DATETIME NOT NULL
);

CREATE TABLE  apkvullevel (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  md5 VARCHAR(32) NOT NULL ,
  scantool VARCHAR(32) NOT NULL ,
  results_location VARCHAR(128) NOT NULL ,
  status INTEGER NOT NULL,
  details TEXT ,
  created_at DATETIME NOT NULL
);

CREATE TABLE  apklevels (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  md5 VARCHAR(32) NOT NULL ,
  scantool VARCHAR(32) NOT NULL ,
  results_location VARCHAR(128) NOT NULL ,
  status INTEGER NOT NULL,
  details TEXT ,
  created_at DATETIME NOT NULL
);

CREATE TABLE apkrules (
  id INTEGER PRIMARY KEY NOT NULL,
  info BOOLEAN not null default 0,
  notice BOOLEAN not null default 0,
  warning BOOLEAN not null default 0,
  critical BOOLEAN not null default 0,
  vulnerability_name BOOLEAN not null default 0,
  videos BOOLEAN not null default 0,
  link BOOLEAN not null default 0,
  severity_levels BOOLEAN not null default 0,
  email_template TEXT default 'email'
);

INSERT INTO apkrules (id, info, notice, warning, critical, vulnerability_name, videos, link, severity_levels, email_template) VALUES (1, 0,0,0,0,0,0,0,0,'Email Template');