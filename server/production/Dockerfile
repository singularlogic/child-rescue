# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:16.04

MAINTAINER suite5

# Install required packages and remove the apt packages cache when done.

ENV LANG C.UTF-8

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
	git \
	python3 \
	python3-dev \
	python3-setuptools \
	python3-pip \
	nginx \
	supervisor \
	nano \
	sendmail \
	binutils \
	libproj-dev \
	gdal-bin \
	sqlite3 && \
	pip3 install -U pip setuptools && \
    rm -rf /var/lib/apt/lists/*

# install uwsgi now because it takes a little while
RUN pip3 install uwsgi

COPY ./requirements /home/docker/code/app/requirements
RUN pip3 install -r /home/docker/code/app/requirements/production.txt

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY ./server/production/nginx-app.conf /etc/nginx/sites-available/default
COPY ./server/production/supervisor-app.conf /etc/supervisor/conf.d/

# add (the rest of) our code
RUN mkdir -p /home/docker/code/app/PempoDjango
COPY ./PempoDjango /home/docker/code/app/PempoDjango
COPY ./server/production/uwsgi.ini /home/docker/code/
COPY ./server/production/uwsgi_params /home/docker/code/

EXPOSE 8082
CMD ["supervisord", "-n"]
