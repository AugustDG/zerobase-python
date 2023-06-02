# API Reference

## Sockets

### ZeroBasePubSocket

This represents a ZeroBase publisher socket. This object shouldn't be created directly, but instead internally through the `ZeroBase` class.

#### Parameters

| Parameter | Type                                                           | Description                                |
| --------- | -------------------------------------------------------------- | ------------------------------------------ |
| socket    | _zmq.Socket_                                                   | The ZeroMQ socket to use for this instance |
| config    | _[configs.ZeroBasePubConfig](../configs/zerobasepubconfig.md)_ | Configuration for this socket              |

#### Example

```python
from zerobase import ZeroBasePubSocket, ZeroBasePubConfig

config = ZeroBasePubConfig(addr="tcp://*:5555")
socket = zmq.Context().socket(zmq.PUB)

zbps = ZeroBasePubSocket(socket=socket, config=config)
```
