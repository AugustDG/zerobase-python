
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

if __name__ == "__main__":
    pub_config = ZeroBasePubConfig(addr="tcp://*:5555")
    sub_config_1 = ZeroBaseSubConfig(addr="tcp://localhost:5555", topics=["A"])
    sub_config_2 = ZeroBaseSubConfig(addr="tcp://localhost:5555", topics=["B"])

    base = ZeroBase(pub_config=pub_config, sub_configs=[sub_config_1, sub_config_2], main=main, msg_received=on_msg_received)
    base.run()