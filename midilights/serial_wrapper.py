import serial
import serial.tools.list_ports


def get_available_ports():
    ports = serial.tools.list_ports.comports()
    ports_dir = {port: (desc, hwid) for port, desc, hwid in sorted(ports)}
    return ports_dir

class SerialWrapper(serial.Serial):
    def __init__(self, device="COM3", baudrate=115200):
        super(SerialWrapper, self).__init__(port=device, baudrate=baudrate)
        self.num_bytes = 0

    def bytes_sent(self):
        return self.num_bytes

    def send_data(self, data):
        bytes_data = (data + "\n").encode()
        self.num_bytes += len(bytes_data)
        self.write(bytes_data)
