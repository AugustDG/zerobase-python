# zerobase-python

## Welcome

Hey! Welcome to ZeroBase, a pub-sub communications framework based on [ZeroMQ](https://zeromq.org/) for multiprocessing systems!

This is a Python package that provides a base class for building ZeroMQ & pub-sub -based programs for NanoStride. It handles all of the necessary setup and teardown for ZeroMQ, and provides a simple interface for sending and receiving messages. The library is designed to be easy to use and flexible, allowing you to quickly build and deploy ZeroMQ-based programs for a variety of use cases.

With `zerobase`, you can focus on building the application logic, while the library takes care of the underlying ZeroMQ infrastructure.

That being said, it is still a work in progress, so don't hesitate to create an issue or start a PR!

Yours truly, <br>
Augusto M.P

## Getting Started

Below you'll find the necessary information to install and get started with `zerobase`. For in-depth documentation, check out the [docs](docs/index.md) folder.

### Installation

#### Semi-Automatic Installation (Recommended)

1. Download Python3.10 from your preferred source.
2. Download the latest ZeroBase release from the releases page.
3. Download the latest `requirements.txt` from the releases page.
4. Run `pip install -r <requirements_file>`.
5. Run `pip install <whl_file>`.
6. And import `zerobase` in your python scripts!

#### Manual Installation

1. Download Python3.10 from your preferred source.
2. Download/clone this repository.
3. Open a terminal inside of the repository folder.
4. Run `pip install -r <requirements_file>`.
5. Run `pip install .`
6. And import `zerobase` in your python scripts!

### Quickstart

Once you install the `zerobase` package (by following one of the above methods), take a look at [`docs/examples/basic.py`](docs/examples/basic.py) for a basic example on how to use the library.

The main function generates random messages and sends them on example topics "A", "B", and "C". The `on_msg_received` function is called whenever a message is received on one of the subscribed topics, and simply prints out the message and topic.

To customize the code for your own use case, you can modify the main function to generate and send messages on different topics, and modify the `on_msg_received` function to handle incoming messages according to the given topic. You can also modify the `pub_config` and `sub_configs` objects to change the addresses and topics used by the publisher and subscribers.

## License

This project is licensed under the GPLv3 license - see the [LICENSE](LICENSE) file for details.
