# Use an official Python runtime as a parent image
FROM python:3.7.4-slim-stretch

RUN apt-get update
RUN apt-get install -y git

# Set the working directory to /home/runner
WORKDIR /home/app

# Upgrade pip to last version
RUN pip install --upgrade pip

# Copy requirements into the container at /app
COPY API.requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install -r API.requirements.txt