import serial
import serial.tools.list_ports


def get_available_ports():
    ports = serial.tools.list_ports.comports()
    ports_dir = {port: (desc, hwid) for port, desc, hwid in sorted(ports)}
    return ports_dir

class SerialWrapper:
    def __init__(self, device="COM3"):
        self.ser = serial.Serial(device, 115200)

    def send_data(self, data):
        data += "\n"
        bytes_data = data.encode()
        print(bytes_data)
        self.ser.write(bytes_data)