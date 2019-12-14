# base image
FROM python:3.6.8-alpine
MAINTAINER Prakash Oraon <prakash.o@gmail.com>

# set working directory
WORKDIR /usr/src/app

# add requirements
COPY ./requirements.txt /usr/src/app/requirements.txt

# Install system dependencies
#
#	Pillow (Python Imaging Library) dependencies
#		libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev
# 		liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk
#
#   sudo apt-get install build-essential python-dev libjpeg-dev zlib1g-dev libfreetype6-dev
#  Link: https://pkgs.alpinelinux.org/packages 

#RUN apk add --no-cache build-base jpeg-dev zlib zlib-dev
RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib

# Add the dependencies to the container and install the python dependencies
RUN pip install -r requirements.txt
RUN pip install Pillow

# add app
COPY . /usr/src/app
