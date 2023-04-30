FROM python:3.9-alpine

WORKDIR /app

COPY ./ ./

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && pip install -r requirements.txt
