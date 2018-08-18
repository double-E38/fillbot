# Python3/bottle web server Dockerfile

FROM python:3.7-alpine
RUN pip install -U bottle GroupyAPI

WORKDIR /app
VOLUME /app
EXPOSE 5001

# Define default command
CMD ["python", "-u", "Fillbot_rDevelopment.py"]
