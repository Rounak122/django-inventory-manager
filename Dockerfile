FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev \
    && apk add postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /src
COPY ./src /src
WORKDIR /src
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D docker_ron
RUN chown -R docker_ron:docker_ron /vol
RUN chmod -R 755 /vol/web
USER docker_ron

CMD ["entrypoint.sh"]