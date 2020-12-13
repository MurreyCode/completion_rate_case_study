# Use dvcorg runtime as a parent image
FROM dvcorg/cml-py3:latest

RUN apt-get update
RUN apt-get install git -y

# Set the working directory to /home/runner
WORKDIR /home/runner

# Upgrade pip to last version
RUN pip install --upgrade pip

# Copy requirements into the container at /app
COPY pipeline.requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install -r pipeline.requirements.txt

# Copy all the code in the container
COPY . ./
