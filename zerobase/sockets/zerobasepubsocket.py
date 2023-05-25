import zmq

from attr import dataclass

from ..configs import ZeroBasePubConfig

@dataclass
class ZeroBasePubSocket:
    """
    This represents a ZeroBase publisher socket.
    """

    socket: zmq.Socket
    config: ZeroBasePubConfig