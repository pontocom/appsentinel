CREATE DATABASE apkscanner;
CREATE USER 'appsentinel'@'localhost' IDENTIFIED BY 'teste123';
GRANT ALL PRIVILEGES ON apkscanner.* TO 'appsentinel'@'localhost';
FLUSH PRIVILEGES;
