import sys

import mido

from serial_wrapper import SerialWrapper

def display_input_ports():
    inports = mido.get_input_names()
    print("Please select the midi port to read from:")
    for ix, inport in enumerate(inports):
        print(f"{ix}: {inport}")

def bridge_midi_to_serial(in_port, device):
    srl = SerialWrapper(device)
    with mido.open_input(in_port) as inport:
        for msg in inport:
            control, value = msg.control, msg.value
            if value == 127:
                data = f"m{control}{value}"
                srl.send_data(data)


            

if __name__ == "__main__":
    display_input_ports()
    inport_ix = int(input())
    inport = mido.get_input_names()[inport_ix]
    bridge_midi_to_serial(inport, "")
