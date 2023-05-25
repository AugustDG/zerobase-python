import zmq

from attr import dataclass

from ..configs import ZeroBaseSubConfig

@dataclass
class ZeroBaseSubSocket:
    """
    This represents a ZeroBase subscriber socket.
    """

    socket: zmq.Socket
    config: ZeroBaseSubConfig
    registered: bool = False