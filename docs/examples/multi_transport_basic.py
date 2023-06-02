
import random
import time
from zerobase import ZeroBase, ZeroBasePubConfig, ZeroBaseSubConfig

def main() -> bool:
    print("Main loop running...")

    msg = str((random.randint(1, 100), random.randint(1, 100)))
    base.send(msg, "A")

    msg = str((random.randint(1, 100), random.randint(1, 100)))
    base.send(msg, "B")

    msg = str((random.randint(1, 100), random.randint(1, 100)))
    base.send(msg, "C")

    time.sleep(random.randint(1, 3))

    return True

def on_msg_received(topic, msg):
    print("Message received: " + msg + " on topic: \"" + topic + "\"")

def on_terminated():
    print("Program is terminating...")

if __name__ == "__main__":
    pub_config_1 = ZeroBasePubConfig(addr="tcp://*:5555")
    pub_config_2 = ZeroBasePubConfig(addr="tcp://127.0.0.1:5556")

    sub_config_1 = ZeroBaseSubConfig(addr="tcp://127.0.0.1:5555", topics=["A"])
    sub_config_2 = ZeroBaseSubConfig(addr="tcp://localhost:5555", topics=["B"])
    sub_config_3 = ZeroBaseSubConfig(addr="tcp://127.0.0.1:5556", topics=["B"])

    base = ZeroBase(pub_configs=[pub_config_1, pub_config_2], sub_configs=[sub_config_1, sub_config_2, sub_config_3], main=main, terminated=on_terminated, msg_received=on_msg_received)
    base.run()