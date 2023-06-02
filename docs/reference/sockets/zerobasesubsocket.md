# API Reference

## Sockets

### ZeroBaseSubSocket

This represents a ZeroBase subscriber socket. This object shouldn't be created directly, but instead internally through the `ZeroBase` class.

#### Parameters

| Parameter | Type                                                           | Description                                |
| --------- | -------------------------------------------------------------- | ------------------------------------------ |
| socket    | _zmq.Socket_                                                   | The ZeroMQ socket to use for this instance |
| config    | _[configs.ZeroBaseSubConfig](../configs/zerobasesubconfig.md)_ | Configuration for this socket              |

#### Example

```python
from zerobase import ZeroBaseSubSocket, ZeroBaseSubConfig

config = ZeroBaseSubConfig(addr="tcp://*:5555", topics=["topic1", "topic2"])
socket = zmq.Context().socket(zmq.SUB)

zbss = ZeroBaseSubSocket(socket=socket, config=config)
```
