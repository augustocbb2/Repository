# Real-Time Cryptocurrency Data Ingestion with Redpanda and PostgreSQL

## Overview

This project is designed to ingest real-time cryptocurrency data (e.g., Bitcoin, Ethereum, Zcash) from the CoinGecko API and store it in a PostgreSQL database. The system utilizes **Redpanda** as a Kafka-compatible event streaming platform to handle the data flow between a Python producer and consumer. The application also runs tests automatically and, if successful, proceeds with the execution of the main application logic.

## Features

- **Real-time data ingestion**: Fetches OHLCV data (Open, High, Low, Close, Volume) for cryptocurrencies using the CoinGecko API.
- **Redpanda Integration**: Used as a Kafka-compatible event streaming platform.
- **PostgreSQL Storage**: Stores cryptocurrency data for future analysis and reporting.
- **Automated Testing**: Uses `pytest` to run unit tests on Docker build before launching the application.
- **Dockerized**: Fully containerized using Docker and Docker Compose for easy deployment.

## Prerequisites

Before setting up the project, ensure that you have the following installed on your system:

```bash
# Install Docker
docker --version

# Install Docker Compose
docker-compose --version

You might also want to install PostgreSQL locally if required for development purposes.

## Environmental Variables

Create a `.env` file in the root directory and provide the following values:

```bash
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name
POSTGRES_HOST=postgres
KAFKA_BROKER=redpanda:9092

> **Note:** Replace `your_postgres_user`, `your_postgres_password`, and `your_database_name` with your actual PostgreSQL credentials.

## Project Structure

```bash
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── producer.py
├── consumer.py
├── init.py
├── test_docker_compose.py
└── README.md

## Key Files

- **Dockerfile**: Defines the Docker image, including dependencies and the default application command.
- **docker-compose.yml**: Defines the services (PostgreSQL, Redpanda, App) and networks.
- **producer.py**: Producer service that fetches cryptocurrency data from CoinGecko and sends it to Redpanda.
- **consumer.py**: Consumer service that reads data from Redpanda and stores it in PostgreSQL.
- **init.py**: Initializes any necessary setup tasks for the application.
- **test_docker_compose.py**: Pytest file that runs automated tests to ensure the application is functioning correctly.
- **requirements.txt**: Python dependencies required for the project.

## Setup Instructions

### Step 1: Build and Run the Application

Run the following commands to set up and run the application:

```bash
# Build and run the Docker Compose setup
docker-compose up --build

This command will:

1. **Build the Docker image**.
2. **Run tests** using `pytest`.
3. If the tests pass, the application will start, and the **producer** will begin fetching data from the CoinGecko API, while the **consumer** stores the data in PostgreSQL.

### Step 2: Verify the Setup

To ensure everything is running correctly, you can check the status of the running containers:

```bash
docker ps

You should see three containers running:

- **app**: The Python application (producer/consumer).
- **postgres**: The PostgreSQL database.
- **redpanda**: The Redpanda broker.

### Step 3: Access the PostgreSQL Database

You can connect to the PostgreSQL database to view the stored cryptocurrency data:

```bash
docker exec -it <postgres_container_name> psql -U <POSTGRES_USER> -d <POSTGRES_DB>

### Step 4: Testing

The application runs tests automatically before starting the main logic. You can also run tests manually:

```bash
docker-compose run app pytest test_docker_compose.py

### Step 5: Stopping the Application

To stop the application and remove containers:

```bash
docker-compose down

### Step 5: Data Export
The application allows you to export data from the PostgreSQL database to local files, ensuring no data is lost when containers are stopped or removed.

Manual Data Export:
You can manually export cryptocurrency data using the export_data.py script. To do this, simply run the following command:

bash
docker-compose run export_data
This will export two files:

Daily OHLCV Data (CSV): This contains daily aggregated data (Open, High, Low, Close, Volume) for each cryptocurrency ticker.
Minute-Level Price Data (Parquet): This file contains minute-level price data for each cryptocurrency in Parquet format.
The files will be saved to the data_export directory in your project folder.

Automated Data Export on Shutdown:
The Docker setup is configured to automatically export the data to CSV and Parquet files when the application is stopped using the docker-compose down command. This ensures no data is lost during shutdown.


### Troubleshooting

- **Container Name Mismatch**: Ensure the container names in your tests match the names defined in the `docker-compose.yml` file.
- **Database Connection Issues**: Check if PostgreSQL is up and running, and verify that the environment variables are correctly set.
- **Redpanda Issues**: Ensure Redpanda is accessible on the correct port (9092).