from time import time
from midilights.midilights import run_bridge
from serial.serialutil import SerialException

if __name__ == "__main__":
    while True:
        try:
            run_bridge()
        except SerialException:
            print("Caught SerialException will restart in 2 second")
            time.sleep(2)