# Python3/bottle web server Dockerfile

FROM python:3.7-alpine
RUN python3 -m pip install -U flask bottle GroupyAPI

# ADD fillbot /app

WORKDIR /app
VOLUME /app
EXPOSE 5001

# Define defaults command
ENTRYPOINT ["python3"]
CMD ["Fillbot_rDevelopment.py"}
