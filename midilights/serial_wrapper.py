import serial

class SerialWrapper:
    def __init__(self, device):
        #self.ser = serial.Serial(device, 115200)
        pass

    def send_data(self, data):
        #data += "\r\n"
        data += "\n"
        bytes_data = data.encode()
        print(bytes_data)
        #self.ser.write(bytes_data)