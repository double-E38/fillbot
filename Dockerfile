# 
# Python3/bottle web server Dockerfile 
# 
# based off of https://github.com/Pablosan/bottle-py3 
# 

# Pull base image 
FROM ubuntu:16.04

# Make sure we're up to date! 
RUN apt-get update && apt-get -y upgrade

# Install Python3 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip

# Install Python packages 
RUN pip install -U bottle==0.12.13 GroupyAPI==0.8.1

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
