# Python3/bottle web server Dockerfile

FROM python:3.7-alpine
RUN pip install -U flask bottle GroupyAPI

# ADD fillbot /app

WORKDIR /app
VOLUME /app
EXPOSE 5001

# Define defaults command
CMD ["python Fillbot_rDevelopment.py"}
