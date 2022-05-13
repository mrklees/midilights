import mido
from midilights.midilights import display_input_ports

def test_bridge(inport_ix=1):
    inport = mido.get_input_names()[inport_ix]

    with mido.open_input(inport) as inport:
        for ix, msg in enumerate(inport):
            print(msg)
            if ix == 100: 
                break

if __name__ == "__main__":
    display_input_ports()
    inport_ix = int(input("port:"))
    test_bridge(inport_ix)