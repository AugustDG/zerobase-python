
import random
import time
from zerobase.zerobase import ZeroBase

def main() -> bool:
    print("Main loop running...")

    msg = str((random.randint(1, 100), random.randint(1, 100)))
    print("Sending message: " + msg)
    base.send(msg)

    time.sleep(random.randint(1, 5))

    return True

def on_msg_received(msg):
    print("Message received: " + msg)

if __name__ == "__main__":
    base = ZeroBase(send_addr="tcp://*:5556", recv_addr="tcp://localhost:5555", main=main, msg_received=on_msg_received)
    base.run()