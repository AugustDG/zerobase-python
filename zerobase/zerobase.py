"""
Author: Augusto Mota Pinheiro
Date: 22/05/2023
Description: This file contains the ZeroBase class, which is the base class for all ZeroMQ-based programs for NanoStride. It handles all of the necessary setup and teardown for ZeroMQ, and provides a simple interface for sending and receiving messages.

Copyright 2023, NanoStride
Not licensed under any license. All rights reserved.
"""

import pickle
import sys
import threading
from attr import dataclass
import zmq
import signal

from typing import Any, Callable, List

@dataclass
class ZeroBasePubConfig:
    """
    This represents the configuration for a ZeroBase publisher socket.
    """

    addr: str

@dataclass
class ZeroBaseSubConfig:
    """
    This represents the configuration for a ZeroBase subscriber socket.
    """

    addr: str
    topics: List[str]

@dataclass
class ZeroBasePubSocket:
    """
    This represents a ZeroBase publisher socket.
    """

    socket: zmq.Socket
    config: ZeroBasePubConfig

@dataclass
class ZeroBaseSubSocket:
    """
    This represents a ZeroBase subscriber socket.
    """

    socket: zmq.Socket
    config: ZeroBaseSubConfig
    registered: bool = False

class ZeroBase():
    """
    This is the base class for all ZeroMQ-based programs for NanoStride. It handles all of the necessary setup and teardown for ZeroMQ, and provides a simple interface for sending and receiving messages.
    """
    
    def __init__(self, pub_config: ZeroBasePubConfig | None, sub_configs: List[ZeroBaseSubConfig] = [], main: Callable[[], bool] | None = None, msg_received: Callable[[str, Any], None] | None = None, logger: Callable[[Any], None] = print) -> None:
        signal.signal(signal.SIGINT, self._signal_handler)

        # assign socket configurations
        self.pub_config = pub_config
        self.sub_configs = sub_configs

        # assign callback properties
        self._main = main
        self._logger = logger
        self._msg_received = msg_received

        # initialize ZMQ properties
        self._ctx = zmq.Context()
        self.pub_sockets: List[ZeroBasePubSocket] = []
        self.sub_sockets: List[ZeroBaseSubSocket] = []
    
        # initialize necessary sockets
        if self.pub_config is not None:
            socket = self._ctx.socket(zmq.PUB)
            socket.bind(self.pub_config.addr)

            self.pub_socket = ZeroBasePubSocket(socket, self.pub_config)

        for config in self.sub_configs:
            self.comms_can_run = True

            socket = self._ctx.socket(zmq.SUB)
            socket.connect(config.addr)

            for topic in config.topics:
                socket.setsockopt_string(zmq.SUBSCRIBE, topic)
            
            self.sub_sockets.append(ZeroBaseSubSocket(socket, config))


    def run(self) -> None:
        """ 
        This function is the main entry point for the ZeroBase class (and it should be for the program as well)! It will assume that this is the main thread and run the flow in the appropriate order.

        However, if a main function has not been provided, it won't do anything and assume that the user will manually call start() and stop() outside of this class.
        """

        if self._main is None:
            return
        
        self.start()

        # run the main loop until it returns false (indicating that the program should stop)
        while True:
            if not self._main():
                break

        self.stop()

    
    def start(self) -> None:
        """
        Starts this instance's necessary threads. Must be called before sending or receiving messages.
        """

        self._logger("Starting ZeroBase...")
        
        # start the receive loop thread
        self._receive_loop_thread = threading.Thread(target=self._receive_loop)
        self._receive_loop_thread.start()
        

    def stop(self) -> None:
        """
        Stops and cleans up this instance. Must be called before the program exits!
        """

        self._logger("Stopping ZeroBase...")
        
        self.comms_can_run = False

        # wait for the receive loop thread to finish
        self._receive_loop_thread.join(timeout=2)

        self._ctx.destroy()
        
    def send(self, msg: Any, topic: str) -> None:
        """
        Sends a message to the specified topic.
        """

        self._logger("Sending message " + str(msg) + " on topic: \"" + topic + "\"")

        # send the message if the socket has been opened
        if self.pub_socket is not None:
            self.pub_socket.socket.send(bytes(topic, "utf-8"), zmq.SNDMORE)
            self.pub_socket.socket.send_pyobj(msg)

    # receive a message from the specified topic
    def _receive_loop(self) -> None:
        poller = zmq.Poller()

        self._logger("Registering sockets...")

        for sub_socket in self.sub_sockets:
            self._logger("Registering sub socket on address " + sub_socket.config.addr + " with topics: " + str(sub_socket.config.topics))
            
            poller.register(sub_socket.socket, zmq.POLLIN)
            sub_socket.registered = True
        
        registered_qty = len(self.sub_sockets)

        self._logger("Registered sockets: " + str(registered_qty))
        self._logger("ZeroBase receive loop started!")

        # run the comms loop
        while self.comms_can_run:
            # check if any sockets have been registered (otherwise, there's no point in trying to receive messages)
            if len(self.sub_sockets) == 0:
                continue

            # register any new sockets
            if registered_qty <= len(self.sub_sockets):
                for sub_socket in filter(lambda socket: (not socket.registered), self.sub_sockets):
                    poller.register(sub_socket.socket, zmq.POLLIN)
                    sub_socket.registered = True
                
                registered_qty = len(self.sub_sockets)

            # poll for any messages
            try:
                ready_sockets = dict(poller.poll())
                
                self._process_poll(ready_sockets)
            except:
                # if the message can't be received, just ignore it
                continue

    # processes the poll results
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
            if self._msg_received is not None:
                self._msg_received(recv_topic, recv_obj)


    # handle OS signals
    def _signal_handler(self, sig, frame) -> None:
        self.stop()
        sys.exit(sig)