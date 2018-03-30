# 
# Python3/bottle web server Dockerfile 
# 
# based off of https://github.com/Pablosan/bottle-py3 
# 

# Pull base image 
FROM ubuntu:16.04.4

# Make sure we're up to date! 
RUN apt-get update && apt-get -y upgrade 

# Install Python3 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip 

# Install Python packages 
RUN pip3 install -U bottle==0.12.13 GroupyAPI==0.9.2

# Cleanup for a smaller image 
RUN apt-get clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/*

# Expose volumes
VOLUME /config
VOLUME /opt
VOLUME /var

# Add python scripts
ADD fillbot /app/Fillbot

# Expose ports
EXPOSE 5001

# Define defaults command
ENTRYPOINT /usr/bin/python3 /opt/Fillbot/Fillbot_rDevelopment.py
