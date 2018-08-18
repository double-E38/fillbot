#
# Python3/bottle web server Dockerfile
#
# based off of https://github.com/Pablosan/bottle-py3
#

# Pull base image
FROM ubuntu:18.04

# Add Python 3.6 repository, update and upgrade.
RUN DEBIAN_FRONTEND=noninteractive apt-get -y update && apt-get -y upgrade \
&& apt-get install -y software-properties-common python-software-properties wget \
&& apt-get -y install python3-minimal python3-pip \

# Install Python packages
RUN python3 -m pip install -U bottle GroupyAPI

# Cleanup for a smaller image
RUN apt-get clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/*

# Add python scripts
ADD fillbot /app

# Define working directory
WORKDIR /app

# Expose volumes
VOLUME /app

# Expose ports
EXPOSE 5001

# Define defaults command
ENTRYPOINT /usr/bin/python3 /app/Fillbot_rDevelopment.py
