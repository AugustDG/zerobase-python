# API Reference

## Root Module

### ZeroBase

Base class for the ZeroBase library. This class is intended to be used directly and should be the starting point to interact with the library.

#### Parameters

| Parameter        | Type                            | Description                                                                                   |
| ---------------- | ------------------------------- | --------------------------------------------------------------------------------------------- |
| main             | _Function() -> bool_            | Main function to run (will be called in a `while (true)`, default is None)                    |
| terminated       | _Function() -> None_            | Callback function to call when the program is terminated (gracefully or not; default is None) |
| message_received | _Function(String, Any) -> None_ | Callback function to call when a message is received (default is None)                        |
| logger           | _Function(Any) -> None_         | Logger function to use for logging (default is `print`)                                       |

#### Example

```python
from zerobase import ZeroBase, ZeroBasePubConfig, ZeroBaseSubConfig

pub_config = ZeroBasePubConfig(addr="tcp://*:5555")
sub_config = ZeroBaseSubConfig(addr="tcp://localhost:5555", topics=["topic1", "topic2"])
main = lambda: print("Hello World!")
on_terminated = lambda: print("Bye World...")
on_message_received = lambda topic, message: print(f"Received message on topic {topic}: {message}")

zb = ZeroBase(main=main, terminated=on_terminated, message_received=on_message_received, logger=print)
```

### ZeroBase.init()

Initializes the ZeroBase instance. Must be called before anything else!

#### Parameters

| Parameter   | Type                                                        | Description                                                                 |
| ----------- | ----------------------------------------------------------- | --------------------------------------------------------------------------- |
| pub_configs | _[configs.ZeroBasePubConfig](configs/zerobasepubconfig.md)_ | Configuration objects (if multiple addresses) for the publisher socket      |
| sub_configs | _[configs.ZeroBaseSubConfig](configs/zerobasesubconfig.md)_ | Configuration objects (if multiple subscriptions) for the subscriber socket |

#### Returns

None

#### Example

```python
[...] # after running above example

zb.init(pub_configs=[pub_config], sub_configs=[sub_config])
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

### ZeroBase.uninit()

Stops and cleans up this instance. Must be called before the program exits (automatically called if the system kills this process).

#### Parameters

None

#### Returns

None

#### Example

```python
[...] # after running class example, instead of calling run()

zb.init()

[...] # main loop

zb.uninit()
```

### ZeroBase.send()

Sends a message to the specified topic, through all the publisher sockets.

#### Parameters

| Parameter | Type     | Description                           |
| --------- | -------- | ------------------------------------- |
| topic     | _String_ | Topic on which to send the message to |
| message   | _Any_    | Message to send                       |

#### Returns

None

#### Example

```python
[...] # after running above example

zb.send("topic1", "Hello World!")

# or

zb.send("topic3", "Hello World!")

# or

zb.send("topic/porkchop", "Hello World!")
```
