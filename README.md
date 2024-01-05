This script is to provide a simple way to get a port on natpmp provider like a VPN and forward it to transmission.

## setup

This assumes python and virtualenv are installed.

### install dependencies
```bash

virtualenv env
source env/bin/activate

pip install -r requirements.txt
```
### systemd installation

Update the systemd files to fit the paths and user to execute the script.

Copy the systemd files into `/etc/systemd/system/`

### configuration
Copy the provided example config file
```bash
cp config.ini-example config.ini
```
and edit it.
