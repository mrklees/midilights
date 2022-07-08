from time import sleep, time
from tqdm import tqdm
from midilights.serial_wrapper import SerialWrapper, get_available_ports

def benchmark(serial, iterations=100):
    kick =  f'm{chr(0)}{chr(127)}'

    T0 = time()
    for i in tqdm(range(iterations)):
        serial.send_data(kick)

    while True:
        queued = serial.ser.out_waiting
        print(f"Waiting on {queued} ({time() - T0:.2f})")
        if queued == 0:
            break
        sleep(0.01)

    # Should happen instantly
    serial.ser.flush()

    T1 = time()
    num_bytes = serial.bytes_sent()
    duration = T1 - T0

    bandwidth = num_bytes / duration
    print(f"\tsent {num_bytes} in {duration:.2f} -> {bandwidth:.1f} Bps")


if __name__ == "__main__":
    available_ports = get_available_ports()
    print(f"Devices: {available_ports}")
    first_port = list(available_ports.keys())[1]
    print(f"Using device: {first_port}")
    serial = SerialWrapper(first_port)

    benchmark(serial, iterations=10000)
    serial.ser.close()
