FROM python:3.6.8-alpine

WORKDIR /docker-flask

COPY . .

RUN ["pip3", "install", "-r" ,"requirements.txt"]

EXPOSE 80

CMD ["python", "wrangler-server.py"]