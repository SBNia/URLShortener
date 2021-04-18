# Alpine
FROM python:3.7-alpine

RUN apk add --update gcc bash libc-dev fortify-headers linux-headers && rm -rf /var/cache/apk/*

RUN mkdir -p /home/app
COPY ./run /home/app
COPY requirements.txt /home/app
RUN mkdir -p /home/app/URLShortener
ADD URLShortener /home/app/URLShortener

WORKDIR /home/app
RUN pip install -r requirements.txt

EXPOSE 5000

RUN chmod +x /home/app/run

ENTRYPOINT ["/home/app/run"]