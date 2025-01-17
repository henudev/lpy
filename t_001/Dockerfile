# Description: Dockerfile for the python application
FROM python:3.9-slim

# Set the working directory

RUN mkdir -p /application
WORKDIR /application
COPY . .
RUN pip install flask
EXPOSE 5000
CMD ["python", "test.py"]