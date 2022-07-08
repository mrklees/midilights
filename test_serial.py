from time import sleep
from midilights.serial_wrapper import SerialWrapper, get_available_ports

def simulated_drum_loop(device, repeats=10, wait_time=0.5):
    kick =  f'm{chr(0)}{chr(127)}'
    snare = f'm{chr(1)}{chr(127)}'
    chat = f'm{chr(2)}{chr(127)}'

    with SerialWrapper(device) as serial:
        serial.send_data("m{chr(5)}{chr(2)}")
        for rep in range(repeats):
            print("iteration:", rep)
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
