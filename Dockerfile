FROM python:3.7.3-slim

# Adding server directory to make absolute filepaths consistent across services
WORKDIR /server

# Copy our code from the current folder to /server inside the container
COPY . /server

# Install system dependencies
RUN apt-get update && \
apt-get upgrade -y && \
apt-get install -y python-pip git aapt

# Install python dependencies
ADD requirements.txt /server/requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

CMD ["python3", "server.py"]

# This is just for testing... no clue if it works or not... needs testing!!!
# ---- START OF TEST
# Install mysql/mariadb database server
# RUN apt install mariadb

# Install the database on the mysql/mariadb server
# RUN mysql -u root -p < sql/scanner.sql
# ---- END OF TEST
# https://stackoverflow.com/questions/47252273/unable-to-build-a-mariadb-base-in-a-dockerfile
# https://github.com/dockerfile/mariadb
# https://linoxide.com/containers/setup-use-mariadb-docker-container/
# https://stackoverflow.com/questions/29420870/install-mysql-in-dockerfile (this seems to be what we want!!!)