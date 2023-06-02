# API Reference

## Configs

### ZeroBasePubConfig

This represents the configuration for a ZeroBase publisher socket.

#### Parameters

| Parameter | Type     | Description                                               |
| --------- | -------- | --------------------------------------------------------- |
| addr      | _String_ | Address to bind to, formatted under ZeroMQ specifications |

#### Example

```python
from zerobase import ZeroBasePubConfig

config = ZeroBasePubConfig(addr="tcp://*:5555")

# or

config = ZeroBasePubConfig(addr="ipc:///temp/pub2") # IPC currently only works on Linux, more info: https://github.com/zeromq/netmq/issues/331
```
