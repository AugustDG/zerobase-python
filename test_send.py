import time
import zmq

ctx = zmq.Context() 
socket = ctx.socket(zmq.PUB)
socket.bind("tcp://*:5555")

while True:
    socket.send(bytes("", "utf-8"), zmq.SNDMORE)
    print("Sending message: Hello, World!")
    socket.send_pyobj("Hello, World!")
    time.sleep(2)
    pass