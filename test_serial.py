from time import sleep
from midilights.serial_wrapper import SerialWrapper, get_available_ports

def simulated_drum_loop(device, repeats=10, wait_time=0.5):
    serial = SerialWrapper(device)
    kick =  f'm{chr(0)}{chr(127)}'
    snare = f'm{chr(1)}{chr(127)}'
    chat = f'm{chr(2)}{chr(127)}'
    for rep in range(repeats):
        serial.send_data(kick)
        sleep(wait_time)
        serial.send_data(snare)
        sleep(wait_time)
        serial.send_data(chat)
        sleep(1)

if __name__ == "__main__":
    available_ports = get_available_ports()
    print(f"Devices: {available_ports}")
    first_port = list(available_ports.keys())[1]
    print(f"Using device: {first_port}")
    simulated_drum_loop(first_port)
