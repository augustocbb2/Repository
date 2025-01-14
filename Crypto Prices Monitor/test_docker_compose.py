import docker
import pytest
import time

client = docker.from_env()

# Test if the Redpanda service starts correctly
def test_redpanda_service():
    try:
        container = client.containers.get("realtime_crypto-redpanda-1")  # Adjust the name based on your setup
        container.start()
        time.sleep(5)  # Wait a few seconds for the service to initialize
        assert container.status == 'running'
        print("Redpanda service is running.")
    except docker.errors.NotFound:
        pytest.fail("Redpanda service not found.")

# Test if the PostgreSQL service starts correctly
def test_postgres_service():
    try:
        container = client.containers.get("realtime_crypto-postgres-1")  # Adjust the name based on your setup
        container.start()
        time.sleep(5)  # Wait for PostgreSQL to start
        assert container.status == 'running'
        print("PostgreSQL service is running.")
    except docker.errors.NotFound:
        pytest.fail("PostgreSQL service not found.")

# Test if the application starts correctly
def test_app_service():
    try:
        container = client.containers.get("realtime_crypto-app-1")  # Adjust the name based on your setup
        container.start()
        time.sleep(5)  # Wait for the app to start
        assert container.status == 'running'
        print("Application service is running.")
    except docker.errors.NotFound:
        pytest.fail("Application service not found.")





def main():
    test_redpanda_service()
    print("Redpanda service is running.")
    test_postgres_service()
    print("PostgreSQL service is running.")
    test_app_service()
    print("Application service is running.")


if __name__ == "__main__":
    main()