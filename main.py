import logging
import sys
from configparser import ConfigParser
from pathlib import Path

import natpmp
from transmission_rpc import Client as TransmissionClient
from qbittorrent import Client as QbittorrentClient


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

logger.info(f"Successfully mapped port {response.public_port}")

backend = config.get("GENERAL", "TORRENT_BACKEND", fallback="TRANSMISSION").upper()

if backend == "TRANSMISSION":
    logger.info("Using Transmission backend")
    client = TransmissionClient(
        username=config["TRANSMISSION"]["USER"],
        password=config["TRANSMISSION"]["PASSWORD"],
        host=config["TRANSMISSION"]["HOST"],
        port=config["TRANSMISSION"].getint("PORT"),
    )

    session = client.get_session()

    if response.public_port != session.peer_port:
        logger.info(f"Updating Transmission port from {session.peer_port} to {response.public_port}")
        client.set_session(peer_port=response.public_port)
    else:
        logger.info("Transmission port is already up to date")

elif backend == "QBITTORRENT":
    logger.info("Using qBittorrent backend")
    client = QbittorrentClient(
        url=f"http://{config['QBITTORRENT']['HOST']}:{config['QBITTORRENT']['PORT']}/"
    )
    client.login(
        username=config["QBITTORRENT"]["USER"],
        password=config["QBITTORRENT"]["PASSWORD"],
    )

    preferences = client.preferences()
    current_port = preferences.get("listen_port")

    if response.public_port != current_port:
        logger.info(f"Updating qBittorrent port from {current_port} to {response.public_port}")
        client.set_preferences(listen_port=response.public_port)
    else:
        logger.info("qBittorrent port is already up to date")

else:
    logger.error(f"Unknown backend: {backend}")
    sys.exit(1)
