FROM python:3.7.3-slim
WORKDIR /app

COPY . /app

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD ["python3", "server.py"]