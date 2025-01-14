########################################################################################
# Dockerfile for Real-time Cryptocurrency Application
#
# Author: Augusto Bastos
# Date: 2024-10-05
#
# Description:
# This Dockerfile sets up a Python 3.11 environment for running the real-time 
# cryptocurrency application. It installs all necessary system dependencies, including 
# PostgreSQL client and netcat for testing purposes, and sets up the Python environment 
# with all required packages specified in the requirements.txt file. The default command 
# starts the producer script, but this can be overridden in the Docker Compose file.
#
# Instructions:
# - Build the Docker image with the following command:
#   docker build -t crypto-app .
#
# - Use in combination with a Docker Compose setup to ensure all services are connected 
#   properly (Postgres, Redpanda).
#
########################################################################################

# Use the official Python 3.11 image
FROM python:3.11-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Install netcat for testing purposes
RUN apt-get update && apt-get install -y netcat-traditional

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the container
COPY . .

# Expose port 5432 (if needed for PostgreSQL)
EXPOSE 5432

# Default command (can be overridden in docker-compose)
CMD ["python", "producer.py"]
