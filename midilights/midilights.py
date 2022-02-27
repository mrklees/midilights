import sys
import time
import mido

from serial_wrapper import SerialWrapper, get_available_ports
from serial.serialutil import SerialException

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


def run_bridge():
    guess = display_input_ports()
    if guess:
        inport_ix = guess
    else:
        inport_ix = int(input("port:"))

    inport = mido.get_input_names()[inport_ix]
    for i in range(15):
        available_ports = get_available_ports()
        if available_ports:
            break
        print("Waiting for COM port to appear")
        time.sleep(1)
    else:
        assert False, "Never found COM port"

    first_port = list(available_ports.keys())[0]
    print(f"Sending Midi from {inport_ix} to {first_port}")
    bridge_midi_to_serial(inport, device=first_port)


if __name__ == "__main__":
    while True:
        try:
            run_bridge()
        except SerialException:
            print("Caught SerialException will restart in 2 second")
            time.sleep(2)
