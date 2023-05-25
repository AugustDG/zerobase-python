from typing import List
from attr import dataclass


@dataclass
class ZeroBaseSubConfig:
    """
    This represents the configuration for a ZeroBase subscriber socket.
    """

    addr: str
    topics: List[str]