import os
import requests
import logging
import urllib.parse
from datetime import datetime, timedelta
import fnmatch
import re

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Retrieve environment variables
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
server_ids = os.getenv('SERVER_IDS').split(',')  # Multiple server IDs
log_directory_path = os.getenv('LOG_DIRECTORY_PATH')
log_retention_days = int(os.getenv('LOG_RETENTION_DAYS', 7))

# Create log directory if it doesn't exist
os.makedirs(log_directory_path, exist_ok=True)

# Setup logging configuration
logging.basicConfig(filename=os.path.join(log_directory_path, 'output.log'),
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def list_files_in_folder(server_id, folder_path=''):
    """List files in a specified folder on Dathost for a given server ID."""
    url = f"https://dathost.net/api/0.1/game-servers/{server_id}/files"
    params = {"hide_default_files": "true", "path": folder_path}
    response = requests.get(url, params=params, auth=(username, password))
    return response.json() if response.text.strip() else []

def delete_content(server_id, path):
    """Delete a specified file or folder on Dathost for a given server ID."""
    encoded_path = urllib.parse.quote(path)
    url = f"https://dathost.net/api/0.1/game-servers/{server_id}/files/{encoded_path}"
    response = requests.delete(url, auth=(username, password))
    if response.status_code == 200:
        logging.info(f"Successfully deleted: {path} - Response: {response.text}")
    else:
        logging.error(f"Failed to delete {path}: {response.text} with status code {response.status_code}")

def parse_date_from_filename(filename, date_pattern, date_format):
    """Extract the date from filenames using a regex pattern."""
    match = re.search(date_pattern, filename)
    if match:
        try:
            return datetime.strptime(match.group(), date_format)
        except ValueError:
            logging.error(f"Failed to parse date from filename {filename}")
    return None

def should_delete_file(file_date):
    """Determine if a file should be deleted based on its age."""
    if file_date:
        cutoff_date = datetime.now() - timedelta(days=log_retention_days)
        return file_date < cutoff_date
    return False

def cleanup_for_server(server_id):
    logging.info(f"Starting cleanup process for server ID: {server_id}")
    # Delete files matching specific patterns at the root directory
    root_files = list_files_in_folder(server_id)
    pattern = 'matchzy_*_*_round*.txt'
    for file in root_files:
        if fnmatch.fnmatch(file['path'], pattern):
            logging.info(f"Preparing to delete: {file['path']}")
            delete_content(server_id, file['path'])

    # Handle predefined folders
    folders = ["MatchZy", "MatchZyDataBackup", "MatchZy_Stats"]
    for folder in folders:
        files = list_files_in_folder(server_id, folder)
        for file in files:
            delete_content(server_id, f"{folder}/{file['path']}")

    # Specific date patterns for each log folder
    log_folders = {
        '/addons/counterstrikesharp/logs': (r'\d{8}', '%Y%m%d'),
        '/logs': (r'\d{4}_\d{2}_\d{2}', '%Y_%m_%d')
    }

    for log_folder, (pattern, date_format) in log_folders.items():
        files = list_files_in_folder(server_id, log_folder)
        for file in files:
            file_date = parse_date_from_filename(file['path'], pattern, date_format)
            if should_delete_file(file_date):
                logging.info(f"Deleting {log_folder}/{file['path']} as it is older than {log_retention_days} days.")
                delete_content(server_id, f"{log_folder}/{file['path']}")

    logging.info(f"Cleanup process completed for server ID: {server_id}")

def main():
    for server_id in server_ids:
        cleanup_for_server(server_id)

if __name__ == "__main__":
    main()
