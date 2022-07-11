import datetime
import mido
import os
import sys
import threading
import time

from collections import defaultdict

from midilights.serial_wrapper import SerialWrapper, get_available_ports
from serial.serialutil import SerialException

user_commands = []

def user_input():
    print("Starting User Input processor")
    global user_commands
    while True:
        try:
            command = input("command:")
            values = tuple(map(int, command.split(" ")))
            if len(values) == 2:
                print("\tadded command:", values)
                user_commands.append(values)
        except KeyboardInterrupt:
            print("Caught ^C Exiting")
            exit(0)
        except:
            print("Caught error")
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

    # To print every once in a while
    events = 0
    last_print_time = time.time()
    last_print_count = 0
    updates = defaultdict(int)
    last_values = defaultdict(int)

    last = [time.time()]
    skipped = 0


    with SerialWrapper(device) as srl, mido.open_input(in_port) as inport:
        for msg in inport:
            while user_commands:
                c, v = user_commands.pop(0)
                print(f"\tSending user command {c} {v}")
                data = f"m{chr(c)}{chr(v)}"
                srl.send_data(data)

            try:
                control, value = msg.control, msg.value
            except AttributeError:
                print("Caught a midi val with no cc")
            if value > 0:
                data = f"m{chr(control)}{chr(value)}"
                events += 1
                updates[control] += 1
                last_values[control] = value

                if srl.out_waiting > 20:
                    delta = time.time() - last[0]
                    skipped += 1
                    updates["Skip"] += 1
                    print(f"Skip #{skipped:<3} | {control:3} {value:3} | last {len(last)} updates in {delta:.3f} seconds")
                else:
                    if skipped:
                        print("previously skipped:", skipped)
                        skipped = 0

                    if events % 100 == 0 or (last_print_count > events and (time.time() - last_print_time) > 1):
                        now = datetime.datetime.now().replace(microsecond=0).isoformat()
                        # Sorted
                        last_values = [v for k, v in sorted(last_values.items())]
                        print(f"{now} {events} events - {skipped} skipped | Sending {control} {value} | last values: {last_values} updates: {dict(sorted(updates.items()))}")

                        last_print_time = time.time()
                        last_print_count = events

                    srl.send_data(data)

                    last.append(time.time())
                    if len(last) > 10:
                        last.pop(0)


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

    # Start thread waiting for user input
    user_thread = threading.Thread(target=user_input)
    user_thread.start()
    bridge_midi_to_serial(inport, device=first_port)

if __name__ == "__main__":
    print(os.listdir("."))
    while True:
        try:
            run_bridge()
        except SerialException:
            print("Caught SerialException will restart in 2 second")
            time.sleep(2)
        except KeyboardInterrupt:
            print("Caught ^C Exiting")
            exit(0)
