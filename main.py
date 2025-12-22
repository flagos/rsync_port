import logging
import sys
from configparser import ConfigParser
from pathlib import Path

from mapper import PortMapper
from transmission_backend import TransmissionBackend
from qbittorrent_backend import QbittorrentBackend

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    dir_path = Path(__file__).absolute().parent
    config_filepath = dir_path / "config.ini"

    if not config_filepath.exists():
        logger.error(f"No file found at {config_filepath}")
        sys.exit(1)

    config = ConfigParser()
    config.read(config_filepath)

    try:
        # 1. Map Port
        mapper = PortMapper(
            gateway_ip=config["NATPMP"]["GATEWAY"],
            lifetime=config["NATPMP"].getint("LIFETIME"),
        )
        public_port = mapper.map_port()

        # 2. Initialize Backend
        backend_name = config.get("GENERAL", "TORRENT_BACKEND", fallback="TRANSMISSION").upper()
        if backend_name == "TRANSMISSION":
            backend = TransmissionBackend(config)
        elif backend_name == "QBITTORRENT":
            backend = QbittorrentBackend(config)
        else:
            logger.error(f"Unknown backend: {backend_name}")
            sys.exit(1)

        # 3. Sync Port
        backend.sync_port(public_port)

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()