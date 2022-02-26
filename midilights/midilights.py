import sys
import mido

def display_input_ports():
    inports = mido.get_input_names()
    print("Please select the midi port to read from:")
    for ix, inport in enumerate(inports):
        print(f"{ix}: {inport}")

def open_inputs(in_port):
    with mido.open_input(in_port) as inport:
        for msg in inport:
            try:
                print(msg)
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    display_input_ports()
    inport_ix = int(input())
    open_inputs(mido.get_input_names()[inport_ix])
