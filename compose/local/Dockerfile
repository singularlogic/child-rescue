#FROM python:3.7-alpine
FROM ubuntu:16.04

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1

# install ca-certificates so that HTTPS works consistently
# the other runtime dependencies for Python are installed later
RUN apk add --no-cache ca-certificates

RUN set -ex \
   	&& apk add --no-cache --virtual .fetch-deps \
		gnupg \
		openssl \
		tar \
		xz \
	\
	&& apk add --no-cache --virtual .build-deps  \
		bzip2-dev \
		coreutils \
		dpkg-dev dpkg \
		gcc \
		gdbm-dev \
		libc-dev \
		linux-headers \
		make \
		ncurses-dev \
		openssl \
		openssl-dev \
		pax-utils \
		readline-dev \
		sqlite-dev \
		tcl-dev \
		tk \
		tk-dev \
		zlib-dev \
#		cython \
# add build deps before removing fetch deps in case there's overlap
	&& apk del .fetch-deps \
	&& apk del .build-deps

ENV PACKAGES="\
    alpine-sdk \
    libffi-dev \
    jpeg-dev \
    python-dev \
    zlib-dev \
    musl-dev \
    libffi \
    postgresql-dev \
"

RUN \
	apk add --virtual .build-deps --no-cache --upgrade $PACKAGES \
   	&& echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
   	&& echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
   	&& echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories  \
        \
        && apk add \
            gdal-dev \
            geos-dev  \
        \
        && apk add --virtual .build-deps postgresql-libs \
        \
	&& pip install --upgrade pip \
        \
	&& apk --purge del .build-deps

RUN apk add --no-cache build-base python-dev py-pip jpeg-dev zlib-dev postgresql-dev libstdc++ tzdata && \
    apk add --no-cache --virtual .build-deps g++ gcc && \
    pip3 install cython && \
    pip3 install numpy && \
    pip3 install pandas && \
    pip3 install sklearn && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip3 install psycopg2-binary==2.8.4 && \
    apk del .build-deps


COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/local/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
