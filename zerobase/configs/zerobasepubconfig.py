from attr import dataclass

@dataclass
class ZeroBasePubConfig:
    """
    This represents the configuration for a ZeroBase publisher socket.
    """

    addr: str