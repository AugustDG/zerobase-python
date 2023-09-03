"""
Author: Augusto Mota Pinheiro
Date: 22/05/2023
Description: This file contains the ZeroBase class, which is the base class for all ZeroMQ-based programs for NanoStride. It handles all of the necessary setup and teardown for ZeroMQ, and provides a simple interface for sending and receiving messages.

Copyright 2023, NanoStride
GPLv3 License. All rights reserved.
"""

import pickle
import sys
import threading
import zmq
import signal

from typing import Any, Callable, List
from .configs import ZeroBasePubConfig, ZeroBaseSubConfig
from .sockets import ZeroBasePubSocket, ZeroBaseSubSocket


class ZeroBase():
    """
    This is the base class for all ZeroMQ-based programs for NanoStride. It handles all of the necessary setup and teardown for ZeroMQ, and provides a simple interface for sending and receiving messages.
    """

    def __init__(self, main: Callable[[], bool], msg_received: Callable[[str, Any], None], logger: Callable[[Any], None] = print) -> None:
        # assign callback properties
        self._main = main
        self._logger = logger
        self._msg_received = msg_received

        self.has_init = False

    def init(self, pub_configs: List[ZeroBasePubConfig] | None, sub_configs: List[ZeroBaseSubConfig] = []) -> None:
        """ 
        Initializes the ZeroBase instance. Must be called before anything else!
        """

        if self.has_init:
            return

        self._logger("Initializing ZeroBase...")

        # initialize ZMQ & ZeroBase properties
        self._ctx = zmq.Context()
        self.pub_sockets: List[ZeroBasePubSocket] = []
        self.sub_sockets: List[ZeroBaseSubSocket] = []

        # initialize PUB sockets
        for config in pub_configs:
            socket = self._ctx.socket(zmq.PUB)
            socket.bind(config.addr)

            self.pub_sockets.append(ZeroBasePubSocket(socket, config))

        # initialize SUB sockets
        for config in sub_configs:
            socket = self._ctx.socket(zmq.SUB)
            socket.connect(config.addr)

            for topic in config.topics:
                socket.setsockopt_string(zmq.SUBSCRIBE, topic)

            self.sub_sockets.append(ZeroBaseSubSocket(socket, config))

        # start the communication loop thread
        self._receive_loop_thread = threading.Thread(target=self._receive_loop)
        self._receive_loop_thread.start()

        self.has_init = True

    def run(self) -> None:
        """ 
        This function is the main entry point for the ZeroBase class (and it should be for the program as well)! It will assume that this is the main thread and run the flow in the appropriate order.

        However, if a main function has not been provided, it won't do anything and assume that the user will manually call start() and stop() outside of this class.
        """

        if self._main is None:
            return

        # run the main loop until it returns false (indicating that the program should stop) or the program is terminated
        while self.has_init:
            if not self._main():
                break

        self.uninit()

    def uninit(self) -> None:
        """
        Stops and cleans up this instance. Must be called before the program exits!
        """

        if not self.has_init:
            return

        self._logger("Stopping ZeroBase...")

        self.has_init = False

        # wait for the receive loop thread to finish, kill it if it's taking too long
        if self._receive_loop_thread is not None:
            self._receive_loop_thread.join(timeout=2)
        
        for pub_socket in self.pub_sockets:
            pub_socket.socket.close()

        for sub_socket in self.sub_sockets:
            sub_socket.socket.close()

        self.pub_sockets.clear()
        self.sub_sockets.clear()

        self._ctx.destroy()

    def send(self, topic: str, msg: Any) -> None:
        """
        Sends a message to the specified topic.
        """

        if not self.has_init:
            return

        self._logger("Sending message " + str(msg) + " on topic: \"" + topic + "\"")

        # send the same message, if the socket has been opened, through all supplied publishers
        for pub_socket in self.pub_sockets:
            pub_socket.socket.send(bytes(topic, "utf-8"), zmq.SNDMORE)
            pub_socket.socket.send_pyobj(msg)

    # receive a message from the specified topic

    def _receive_loop(self) -> None:
        poller = zmq.Poller()

        self._logger("Registering sockets...")

        for sub_socket in self.sub_sockets:
            self._logger("Registering sub socket on address " + sub_socket.config.addr +
                         " with topics: " + str(sub_socket.config.topics))

            poller.register(sub_socket.socket, zmq.POLLIN)
            sub_socket.registered = True

        self.registered_sub_qty = len(self.sub_sockets)

        self._logger("Registered sockets: " + str(self.registered_sub_qty))
        self._logger("ZeroBase receive loop started!")

        # run the comms loop
        while self.has_init:
            # check if any sockets have been registered (otherwise, there's no point in trying to receive messages)
            if len(poller.sockets) == 0:
                continue

            # register any new sockets
            if self.registered_sub_qty <= len(self.sub_sockets):
                for sub_socket in filter(lambda socket: (not socket.registered), self.sub_sockets):
                    poller.register(sub_socket.socket, zmq.POLLIN)
                    sub_socket.registered = True

                self.registered_sub_qty = len(self.sub_sockets)

            # poll for any messages
            try:
                ready_sockets = dict(poller.poll())

                self._process_poll(ready_sockets)
            except:
                # if the message can't be received, just ignore it
                continue

    # processes the ZMQ polling results
    def _process_poll(self, ready_sockets: dict[Any, int]) -> None:
        for sub_socket in self.sub_sockets:
            # not super sure why I can't use the socket that was returned by the poller, but it doesn't work for some reason
            # this is just following the example from the ZeroMQ guide
            if sub_socket.socket not in ready_sockets:
                continue

            recv_msg = sub_socket.socket.recv_multipart()

            # tries to manually deserialize the received message (because the first frame is the topic)
            # the first frame is the topic, and the second is the message
            recv_topic = recv_msg.pop(0).decode("utf-8")
            recv_obj = recv_msg.pop()
            recv_obj = pickle.loads(recv_obj)

            # call the callback if it exists
            self._msg_received(recv_topic, recv_obj)