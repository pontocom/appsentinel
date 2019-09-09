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

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD ["python3", "server.py"]