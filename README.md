# Appsentinel - APK security scanner

Mobile platforms and mobile applications are more and more used by millions of users worldwide. More and more developers and developing mobile applications and placing those on app stores for the users to install on their devices.

## Set Up

Intall Docker https://docs.docker.com/get-docker/

Once you have docker, clone the repository and inside the project run:
```bash
docker-compose build
```
After build, start the containers
```bash
docker-compose up -d
```
Then you need to go inside the database container to create the tables
```bash
docker exec -ti mariadb_server_1 bash

mysql -uappsentinel -p < data/application/scanner.sql
```