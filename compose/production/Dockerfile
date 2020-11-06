FROM python:3.8.2-slim

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
	git \
	python3-dev \
	python3-setuptools \
	python3-pip \
#	nginx \
#	supervisor \
	nano \
	sendmail \
#	postgis* \
	binutils \
	libproj-dev \
	gdal-bin \
	sqlite3 && \
	pip3 install -U pip setuptools && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements /requirements
RUN pip install -r /requirements/production.txt

COPY ./compose/production/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/production/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

#COPY ./compose/local/wait-for /bin/wait-for
#RUN sed -i 's/\r$//g' /bin/wait-for
#RUN chmod +x /bin/wait-for
COPY ./Backend /app

WORKDIR /app
EXPOSE 8082

ENTRYPOINT ["/entrypoint"]
