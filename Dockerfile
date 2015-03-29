FROM python:2.7
WORKDIR /code
ADD . /code

RUN apt-get update \
 && apt-get install -y redis-server sudo \
 && rm -rf /var/lib/apt/lists/* # 20150323

RUN pip install -r requirements.txt

RUN sed 's/^daemonize yes/daemonize no/' -i /etc/redis/redis.conf \
 && sed 's/^bind 127.0.0.1/bind 0.0.0.0/' -i /etc/redis/redis.conf \
 && sed 's/^# unixsocket /unixsocket /' -i /etc/redis/redis.conf \
 && sed 's/^# unixsocketperm 755/unixsocketperm 777/' -i /etc/redis/redis.conf \
 && sed '/^logfile/d' -i /etc/redis/redis.conf

RUN chmod 755 start


EXPOSE 6379
EXPOSE 5000

VOLUME ["/var/lib/redis"]
VOLUME ["/run/redis"]
CMD ["./start"]

