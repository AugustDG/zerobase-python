import pickle
import zmq
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

ctx = zmq.Context() 
socket = ctx.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
socket.setsockopt_string(zmq.SUBSCRIBE, "")

while True:
    print("Message received: " + str(pickle.loads(socket.recv_multipart().pop())))
    pass