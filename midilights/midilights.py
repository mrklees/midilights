import sys

import mido

from serial_wrapper import SerialWrapper, get_available_ports

def display_input_ports():
    inports = mido.get_input_names()
    guess = None
    print("Please select the midi port to read from:")
    for ix, inport in enumerate(inports):
        print(f"{ix}: {inport}")
        if "loopMIDI" in inport:
            guess = ix
    return guess

def bridge_midi_to_serial(in_port, device="COM3"):
    srl = SerialWrapper(device)
    with mido.open_input(in_port) as inport:
        for msg in inport:
            control, value = msg.control, msg.value
            if value == 127:
                data = f"m{chr(control)}{chr(value)}"
                srl.send_data(data)


            

if __name__ == "__main__":
    guess = display_input_ports()
    if guess:
        inport_ix = guess
    else:
        inport_ix = int(input("port:"))
    inport = mido.get_input_names()[inport_ix]
    available_ports = get_available_ports()
    first_port = list(available_ports.keys())[0]
    print(f"Sending Midi to {first_port}")
    bridge_midi_to_serial(inport, device=first_port)
