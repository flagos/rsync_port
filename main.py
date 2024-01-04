import logging
from configparser import ConfigParser
from pathlib import Path

import natpmp
from transmission_rpc import Client

dir_path = Path(__file__).absolute().parent
config_filepath = dir_path / "config.ini"

config = None
if config_filepath.exists():
    config = ConfigParser()
    config.read(config_filepath)
else:
    raise ValueError(f"No file found at {str(config_filepath)}")


response = natpmp.map_port(
    protocol=natpmp.NATPMP_PROTOCOL_TCP,
    public_port=1,
    private_port=0,
    lifetime=config["NATPMP"].getint("LIFETIME"),
    gateway_ip=config["NATPMP"]["GATEWAY"],
)

if not response.is_successful():
    raise Exception(str(response))


client = Client(
    username=config["TRANSMISSION"]["USER"],
    password=config["TRANSMISSION"]["PASSWORD"],
    host=config["TRANSMISSION"]["HOST"],
    port=config["TRANSMISSION"].getint("PORT"),
)

session = client.get_session()


if response.public_port != session.peer_port:
    logging.debug("Need to update transmission port")
    client.set_session(peer_port=response.public_port)

else:
    logging.debug("No need to update transmission port")
