FROM alpine:3.13

ARG APP_DIR=/app

RUN apk update --no-cache \
    && apk add --no-cache --virtual .build-deps build-base libpq linux-headers \
    musl-dev postgresql-dev python3 python3-dev py3-pip py3-setuptools

ADD requirements.txt /
RUN pip install --upgrade pip --no-cache-dir \
    && pip install -r  requirements.txt --no-cache-dir

WORKDIR /app

ADD . .

CMD ["echo", "'Holi'"]