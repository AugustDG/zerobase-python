
import random
import time
from zerobase import ZeroBase, ZeroBasePubConfig, ZeroBaseSubConfig

def main() -> bool:
    print("Main loop running...")

    msg = str((random.randint(1, 100), random.randint(1, 100)))
    base.send(topic="A", msg=msg)

    msg = str((random.randint(1, 100), random.randint(1, 100)))
    base.send(topic="B", msg=msg)

    msg = str((random.randint(1, 100), random.randint(1, 100)))
    base.send(topic="C", msg=msg)

    time.sleep(random.randint(1, 3))

    return True

def on_msg_received(topic, msg):
    print("Message received: " + msg + " on topic: \"" + topic + "\"")

def on_terminated():
    print("Program has terminated!")

if __name__ == "__main__":
    pub_config_1 = ZeroBasePubConfig(addr="tcp://*:5555")
    pub_config_2 = ZeroBasePubConfig(addr="tcp://*:5556")

    # IPC only works on linux for now, use tcp on localhost instead if on windows/mac, 
    # more info: https://github.com/zeromq/netmq/issues/331
    # pub_config_3 = ZeroBasePubConfig(addr="ipc:///tmp/test.ipc")
    
    # in the same process only, more info: http://api.zeromq.org/2-1:zmq-inproc
    pub_config_4 = ZeroBasePubConfig(addr="inproc://test") 

    sub_config_1 = ZeroBaseSubConfig(addr="tcp://localhost:5555", topics=["A", "B"])
    sub_config_2 = ZeroBaseSubConfig(addr="tcp://localhost:5556", topics=["B"])

    # IPC only works on linux for now, use tcp on localhost instead if on windows/mac, 
    # more info: https://github.com/zeromq/netmq/issues/331
    # sub_config_3 = ZeroBaseSubConfig(addr="ipc:///tmp/test.ipc", topics=["A"]) 
    
    # in the same process only, more info: http://api.zeromq.org/2-1:zmq-inproc
    sub_config_4 = ZeroBaseSubConfig(addr="inproc://test", topics=["A", "B"]) 

    base = ZeroBase(main=main, msg_received=on_msg_received)
    base.init(pub_configs=[pub_config_1, pub_config_2, pub_config_4], sub_configs=[sub_config_1, sub_config_2, sub_config_4])
    
    base.run()

    on_terminated()