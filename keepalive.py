import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Retrieve and clean environment variables
username = os.getenv('USERNAME').strip()
password = os.getenv('PASSWORD').strip()
keepalive_server_ids = os.getenv('KEEPALIVE_SERVER_IDS').split(',')  # Server IDs for keepalive
log_directory_path = os.getenv('LOG_DIRECTORY_PATH')
allow_reassignment = os.getenv('ALLOW_REASSIGNMENT', 'true').strip().lower() == 'true'

# Create log directory if it doesn't exist
os.makedirs(log_directory_path, exist_ok=True)

# Setup logging configuration
logging.basicConfig(filename=os.path.join(log_directory_path, 'keepalive.log'),
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def test_authentication():
    """Test API authentication."""
    url = "https://dathost.net/api/0.1/account"
    response = requests.get(url, auth=(username, password))
    if response.status_code == 200:
        logging.info("Authentication successful.")
    else:
        logging.error(f"Authentication failed: {response.status_code}, {response.text}")
        exit(1)

def start_server(server_id):
    """Send a start command to the Dathost server."""
    url = f"https://dathost.net/api/0.1/game-servers/{server_id}/start"

    # Configure payload and headers based on reassignment option
    if allow_reassignment:
        payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"allow_host_reassignment\"\r\n\r\ntrue\r\n-----011000010111000001101001--"
        headers = {
            "content-type": "multipart/form-data; boundary=---011000010111000001101001"
        }
        response = requests.post(url, data=payload, headers=headers, auth=(username, password))
    else:
        response = requests.post(url, auth=(username, password))

    # Log response
    if response.status_code == 200:
        logging.info(f"Successfully started server: {server_id}")
    else:
        logging.error(f"Failed to start server {server_id}: {response.text}")

def main():
    test_authentication()
    for server_id in keepalive_server_ids:
        start_server(server_id)

if __name__ == "__main__":
    main()
