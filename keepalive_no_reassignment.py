import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve environment variables
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
server_ids = os.getenv('SERVER_IDS').split(',')  # Multiple server IDs
log_directory_path = os.getenv('LOG_DIRECTORY_PATH')

# Setup logging configuration
log_file_path = os.path.join(log_directory_path, 'keepalive.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start_server(server_id):
    """Send a start command to the Dathost server."""
    url = f"https://dathost.net/api/0.1/game-servers/{server_id}/start"
    headers = {
        "Authorization": f"Basic {username}:{password}"
    }
    # Log the attempt before making the request
    logging.info(f"Attempting to start server ID: {server_id}")
    response = requests.post(url, auth=(username, password))
    if response.status_code == 200:
        logging.info(f"Successfully started server: {server_id}")
    else:
        logging.error(f"Failed to start server {server_id}: {response.text}")

def main():
    for server_id in server_ids:
        start_server(server_id)

if __name__ == "__main__":
    main()
