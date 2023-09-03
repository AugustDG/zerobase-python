# Documentation (v0.6.0)

## Table of Contents

- [Documentation](#documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Usage](#usage)
    - [Working Examples](#examples)
  - [API Reference](#api-reference)
  - [License](#license)

## Introduction

This document should serve as a reference for the `zerobase` library. It is intended to be used as a reference for the library's API, and as a indirect-guide for how to use the library.

## Usage

For the simplest use case, take a look at the [Quickstart](../README.md#quickstart) section of the README. For more in-depth usage, take a look at the [Examples](#examples) section of this document. And for a complete reference of the library's API, take a look at the [API Reference](#api-reference) section.

### Working Examples

A series of examples to demonstrate how to use the library.

---

[`docs/examples/basic.py`](basic.py)

Quick and dirty example on how to use the library (the same one used by the **Quickstart**), with some comments to explain what's going on.

---

[`docs/examples/multi_transport_basic.py`](multi_transport_basic.py)

Very similar to the basic example, but using multiple publisher addresses.

---

[`docs/examples/multi_transport_advanced.py`](multi_transport_advanced.py)

Very similar to both basic examples, but mixing different transports. For IPC and INPROC transports, check out the links in the comments.

---

## API Reference

This section is organized by module, and contains a reference page for each module and class in the library.

- [ZeroBase](reference/zerobase.md)
- [Configs](reference/configs)
  - [ZeroBasePubConfig](reference/configs/zerobasepubconfig.md)
  - [ZeroBaseSubConfig](reference/configs/zerobasesubconfig.md)
- [Sockets](reference/sockets)
  - [ZeroBasePubSocket](reference/sockets/zerobasepubsocket.md)
  - [ZeroBaseSubSocket](reference/sockets/zerobasesubsocket.md)

## License

This project is licensed under the GPLv3 license - see the [LICENSE](../LICENSE) file for details.
