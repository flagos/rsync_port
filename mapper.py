import logging
import natpmp

logger = logging.getLogger(__name__)

class PortMapper:
    def __init__(self, gateway_ip: str, lifetime: int):
        self.gateway_ip = gateway_ip
        self.lifetime = lifetime

    def map_port(self, internal_port: int = 0) -> int:
        response = natpmp.map_port(
            protocol=natpmp.NATPMP_PROTOCOL_TCP,
            public_port=1,
            private_port=internal_port,
            lifetime=self.lifetime,
            gateway_ip=self.gateway_ip,
        )
        if not response.is_successful():
            raise Exception(f"NAT-PMP failed: {response}")
        logger.info(f"Successfully mapped port {response.public_port}")
        return response.public_port
