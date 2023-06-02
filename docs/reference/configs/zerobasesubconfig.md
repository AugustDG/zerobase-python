# API Reference

## Configs

### ZeroBaseSubConfig

This represents the configuration for a ZeroBase subscriber socket.

#### Parameters

| Parameter | Type              | Description                                                  |
| --------- | ----------------- | ------------------------------------------------------------ |
| addr      | _String_          | Address to connect to, formatted under ZeroMQ specifications |
| topics    | _List of Strings_ | Topics to subscribe to                                       |

#### Example

```python
from zerobase import ZeroBaseSubConfig

config = ZeroBaseSubConfig(addr="tcp://10.34.0.2:5555", topics=["topic1", "topic2"])

# or

config = ZeroBaseSubConfig(addr="ipc:///temp/pub2", topics=["topic/porkchop", "topic3"])
```
