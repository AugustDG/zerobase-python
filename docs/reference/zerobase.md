# API Reference

## Root Module

### ZeroBase

Base class for the ZeroBase library. This class is intended to be used directly and should be the starting point to interact with the library.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| pub_config | _[configs.ZeroBasePubConfig](configs/zerobasepubconfig.md)_ | Configuration object for the publisher socket |
| sub_configs | _[configs.ZeroBaseSubConfig](configs/zerobasesubconfig.md)_ | Configuration objects (if multiple subscriptions) for the subscriber socket |
| main | _Function_ | Main function to run (will be called in a `while (true)`) |
| message_received_cb | _Function_ | Callback function to call when a message is received |
| logger | _Function_ | Logger function to use for logging |

#### Example

```python
from zerobase import ZeroBase, ZeroBasePubConfig, ZeroBaseSubConfig

pub_config = ZeroBasePubConfig(addr="tcp://*:5555")
sub_config = ZeroBaseSubConfig(addr="tcp://localhost:5555", topics=["topic1", "topic2"])
main = lambda: print("Hello World!")
on_message_received = lambda topic, message: print(f"Received message on topic {topic}: {message}")

zb = ZeroBase(pub_config=pub_config, sub_configs=[sub_config], main=main, message_received_cb=on_message_received, logger=print)
```

### ZeroBase.run()

This function is the main entry point for the ZeroBase class (and it should be for the program as well)! It will assume that this is the main thread and run the flow in the appropriate order.

However, if a `main` function has not been provided, it won't do anything and assume that the user will manually call start() and stop() outside of this class (therefore, not calling `run()`).

#### Parameters

None

#### Returns

None

#### Example

```python
[...] # after running above example

zb.run() # call is blocking, will run until the program is stopped
```

### ZeroBase.start()

Starts this ZeroBase instance's necessary threads. Must be called before sending or receiving messages.

#### Parameters

None

#### Returns

None

#### Example

```python
[...] # after running class example, instead of calling run()

zb.start()

[...] # main loop

zb.stop()
```

### ZeroBase.stop()

Stops and cleans up this instance. Must be called before the program exits (automatically called if the system kills this process).

#### Parameters

None

#### Returns

None

#### Example

```python
[...] # after running class example, instead of calling run()

zb.start()

[...] # main loop

zb.stop()
```

### ZeroBase.send()

Sends a message to the specified topic, through the publisher socket.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| message | _Any_ | Message to send |
| topic | _String_ | Topic on which to send the message to |

#### Returns

None

#### Example

```python
[...] # after running class example

zb.send("Hello World!", "topic1")

# or

zb.send("Hello World!", "topic3")

# or

zb.send("Hello World!", "topic/porkchop")
```