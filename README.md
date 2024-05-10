# Dathost Maintenance Scripts

## Overview
This repository contains Python scripts designed to manage and maintain Dathost game servers. These scripts automate the cleanup of old logs, temporary files, and ensure the server performs optimally without manual intervention. The focus is on cleaning up files from the CS2 plugin MatchZy, console logs, and logs from CounterStrikeSharp.

## Scripts Included
- `cleanup.py`: This script automates the deletion of old logs and temporary files specific to MatchZy and other elements of the game server.
- `keepalive.py`: Ensures that the servers specified are kept active by periodically sending a start command to prevent auto shutdown by the hosting provider.
- `keepalive_no_reassignment.py`: Same as keepalive.py, but without the allow_host_reassignment boolean

## Setup Instructions
1. Clone this repository to your local machine or server where you intend to run these scripts:
   ```
   git clone git@github.com:enghausen/LinuxGSM-maintenance-scripts.git
   ```
2. Navigate into the repository directory:
   ```
   cd LinuxGSM-maintenance-scripts
   ```
3. Set up a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate
   ```
4. Install required packages:
   ```
   pip install -r requirements.txt
   ```
5. Copy the example environment file and configure your settings:
   ```
   cp .env.example .env
   vi .env
   ```

## Logging
Logs generated by the cleanup script are configured to be stored in a specified log directory, with all entries consolidated into `output.log`. These logs assist in diagnosing issues and auditing server operations. The `keepalive.py` script logs its operations into `keepalive.log` within the same directory.

## Crontab Setup
To automate the execution of the scripts, add entries to your crontab. Use `crontab -e` to edit your cron jobs and ensure the virtual environment is activated before running the scripts:

```bash
# Daily cleanup at 06:00
0 6 * * * /home/enghausen/python/Dathost-maintenance-scripts/venv/bin/python /home/enghausen/python/Dathost-maintenance-scripts/cleanup.py >> /home/enghausen/python/Dathost-maintenance-scripts/logs/cleanup.log 2>&1

# Weekly server keepalive at 01:00 on Sundays
0 1 * * 0 /home/enghausen/python/Dathost-maintenance-scripts/venv/bin/python /home/enghausen/python/Dathost-maintenance-scripts/keepalive.py >> /home/enghausen/python/Dathost-maintenance-scripts/logs/keepalive.log 2>&1
```

## Customizing the Scripts
You can customize the scripts by editing the `.env` file or directly modifying the Python scripts. Ensure that the paths specified for logs and other directories match your server's directory structure.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
