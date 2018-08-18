#
# Python3/bottle web server Dockerfile
#

# Pull base image
FROM python:3.7-alpine

# Install Python packages
RUN python3 -m pip install -U flask bottle GroupyAPI

# Add python scripts
ADD fillbot /app

# Define working directory
WORKDIR /app

# Expose volumes
VOLUME /app

# Expose ports
EXPOSE 5001

# Define defaults command
ENTRYPOINT ["python"]

# Command
CMD ["Fillbot_rDevelopment.py"}
