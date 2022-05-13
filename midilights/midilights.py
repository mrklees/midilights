import os
import sys
import time
import mido

from midilights.serial_wrapper import SerialWrapper, get_available_ports
from serial.serialutil import SerialException

user_commands = []

def user_input():
    global user_commands
    while True:
        try:
            command = input()
            values = tuple(map(int, command.split(" ")))
            if len(command) == 2:
                user_commands.append(values)
        except KeyboardInterupt:
            break
        except:
            continue

def display_input_ports():
    inports = mido.get_input_names()
    guess = None
    print("Please select the midi port to read from:")
    for ix, inport in enumerate(inports):
        print(f"{ix}: {inport}")
        if "loopMIDI" in inport:
            print("guessed!")
            guess = ix
    return guess

def bridge_midi_to_serial(in_port, device="COM3"):
    global user_commands
    srl = SerialWrapper(device)
    with mido.open_input(in_port) as inport:
        for msg in inport:
            while user_commands:
                c, v = user_commands.pop(0)
                data = f"m{chr(c)}{chr(v)}"
                srl.send_data(data)

            control, value = msg.control, msg.value
            if value > 0:
                data = f"m{chr(control)}{chr(value)}"
                print(control, value)
                srl.send_data(data)
                time.sleep(0.01)


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
    print(os.listdir("."))
    while True:
        try:
            run_bridge()
        except SerialException:
            print("Caught SerialException will restart in 2 second")
            time.sleep(2)
