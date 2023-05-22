"""
Author: Augusto Mota Pinheiro
Date: 22/05/2023
Description: This file contains the ZeroBase class, which is the base class for all ZeroMQ-based programs for NanoStride. It handles all of the necessary setup and teardown for ZeroMQ, and provides a simple interface for sending and receiving messages.

Copyright 2023, NanoStride
Not licensed under any license. All rights reserved.
"""

import pickle
import sys
from typing import Any, Callable

import threading
import zmq
import signal

class ZeroBase():
    """
    This class is the base class for all ZeroMQ-based programs for NanoStride. It handles all of the necessary setup and teardown for ZeroMQ, and provides a simple interface for sending and receiving messages.
    """
    
    def __init__(self, send_addr: str | None = None, recv_addr: str | None = None, send_topic: str = "", recv_topic: str = "", main: Callable[[], bool] | None = None, msg_received: Callable[[str, Any], None] | None = None, logger: Callable[[Any], None] = print) -> None:
        signal.signal(signal.SIGINT, self._signal_handler)

        # assign topic properties
        self.send_topic = send_topic
        self.recv_topic = recv_topic

        # assign callback properties
        self._main = main
        self._logger = logger
        self._msg_received = msg_received

        # initialize ZMQ properties
        self._ctx = zmq.Context()
        self._send_socket = None
        self._recv_socket = None
    
        # initialize necessary sockets
        if send_addr is not None:
            self._send_socket = self._ctx.socket(zmq.PUB)
            self._send_socket.bind(send_addr)

        if recv_addr is not None:
            self.comms_can_run = True

            self._recv_socket = self._ctx.socket(zmq.SUB)
            self._recv_socket.connect(recv_addr)
            self._recv_socket.setsockopt_string(zmq.SUBSCRIBE, recv_topic)


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
        
    def send(self, msg: Any, topic: str | None = None) -> None:
        """
        Sends a message to the specified topic. If no topic is specified, the default topic for this instance will be used.
        """

        # send the message if the socket has been opened
        if self._send_socket is not None:
            self._send_socket.send(bytes(self.send_topic if topic is None else topic, "utf-8"), zmq.SNDMORE)
            self._send_socket.send_pyobj(msg)

    # receive a message from the specified topic
    def _receive_loop(self) -> None:
        # run the comms loop
        while self.comms_can_run:
            # check if the socket has been opened (otherwise, there's no point in trying to receive messages)
            if self._recv_socket is None:
                continue

            # tries to manually deserialize the received message (because the first frame is the topic)
            try:
                recv_msg = self._recv_socket.recv_multipart()
            except:
                # if the message can't be received, just ignore it
                continue

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

