FROM python:3.7.3-slim
WORKDIR /app

COPY . /app

# This is just for testing... no clue if it works or not... needs testing!!!
# ---- START OF TEST
# Install mysql/mariadb database server
RUN apt install mariadb

# Install the database on the mysql/mariadb server
RUN mysql -u root -p < sql/scanner.sql
# ---- END OF TEST
# https://stackoverflow.com/questions/47252273/unable-to-build-a-mariadb-base-in-a-dockerfile
# https://github.com/dockerfile/mariadb
# https://linoxide.com/containers/setup-use-mariadb-docker-container/
# https://stackoverflow.com/questions/29420870/install-mysql-in-dockerfile (this seems to be what we want!!!)

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD ["python3", "server.py"]