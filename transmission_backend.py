from configparser import ConfigParser
from transmission_rpc import Client as TransmissionClient
from base import TorrentBackend

class TransmissionBackend(TorrentBackend):
    def __init__(self, config: ConfigParser):
        self.client = TransmissionClient(
            username=config["TRANSMISSION"]["USER"],
            password=config["TRANSMISSION"]["PASSWORD"],
            host=config["TRANSMISSION"]["HOST"],
            port=config["TRANSMISSION"].getint("PORT"),
        )

    def get_port(self) -> int:
        return self.client.get_session().peer_port

    def set_port(self, port: int) -> None:
        self.client.set_session(peer_port=port)
