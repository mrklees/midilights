import serial
import serial.tools.list_ports


def get_available_ports():
    ports = serial.tools.list_ports.comports()
    ports_dir = {port: (desc, hwid) for port, desc, hwid in sorted(ports)}
    return ports_dir

class SerialWrapper:
    def __init__(self, device="COM3"):
        self.ser = serial.Serial(device, 115200)
        self.num_bytes = 0

    def bytes_sent(self):
        return self.num_bytes

    def send_data(self, data):
        bytes_data = (data + "\n").encode()
        self.ser.write(bytes_data)
        self.num_bytes += len(bytes_data)
