from configparser import ConfigParser
from qbittorrent import Client as QbittorrentClient
from base import TorrentBackend

class QbittorrentBackend(TorrentBackend):
    def __init__(self, config: ConfigParser):
        url = f"http://{config['QBITTORRENT']['HOST']}:{config['QBITTORRENT']['PORT']}/"
        self.client = QbittorrentClient(url=url)
        self.client.login(
            username=config["QBITTORRENT"]["USER"],
            password=config["QBITTORRENT"]["PASSWORD"],
        )

    def get_port(self) -> int:
        return self.client.preferences().get("listen_port")

    def set_port(self, port: int) -> None:
        self.client.set_preferences(listen_port=port)
