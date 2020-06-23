import rtmidi
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF

from configuration import Configuration


def open_ports():
    available_ports = rtmidi.MidiOut().get_ports()
    ports = []
    for vpname in Configuration.virtual_ports:
        if vpname not in available_ports:
            raise ValueError(
                f"Virtual Port {vpname} is not an available MIDI Out Port. Make virtual ports are open."
            )
    for vpname in Configuration.virtual_ports:
        midi_out = rtmidi.MidiOut()
        ix = available_ports.index(vpname)
        midi_out.open_port(ix)
        ports.append(midi_out)
    return ports
