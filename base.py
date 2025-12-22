import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class TorrentBackend(ABC):
    @abstractmethod
    def get_port(self) -> int:
        pass

    @abstractmethod
    def set_port(self, port: int) -> None:
        pass

    def sync_port(self, target_port: int):
        current_port = self.get_port()
        if current_port != target_port:
            logger.info(f"Updating {self.__class__.__name__} port from {current_port} to {target_port}")
            self.set_port(target_port)
        else:
            logger.info(f"{self.__class__.__name__} port is already up to date ({target_port})")
