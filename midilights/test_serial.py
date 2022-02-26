from time import sleep
from serial_wrapper import SerialWrapper

def simulated_drum_loop(repeats=10, wait_time=0.5):
    serial = SerialWrapper("")
    kick = 'm0127'
    snare = 'm1127'
    chat = 'm2127'
    for rep in range(repeats):
        serial.send_data(kick)
        sleep(wait_time)
        serial.send_data(snare)
        sleep(wait_time)
        serial.send_data(chat)
        sleep(1)

if __name__ == "__main__":
    simulated_drum_loop()