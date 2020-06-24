"""
Module responsible of initialization (read sounds, open ports, route them)
and playing sounds via Player class.
"""
import sched
import time
from typing import List

import rtmidi
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF

from configuration import Configuration
from discoversounds import Sound, read_sounds


def _open_ports() -> List[rtmidi.MidiOut]:
    """Open MIDI Output Ports given in Configuration."""
    available_ports = rtmidi.MidiOut().get_ports()
    ports = []
    for vpname in Configuration.virtual_ports:
        if vpname not in available_ports:
            raise ValueError(
                f"Virtual Port {vpname} is not an available MIDI Out Port. "
                "Make virtual ports are open."
            )
    for vpname in Configuration.virtual_ports:
        midi_out = rtmidi.MidiOut()
        ix = available_ports.index(vpname)
        midi_out.open_port(ix)
        ports.append(midi_out)
    return ports


def _route_sounds(sounds, ports) -> None:
    """Set destinations of MIDI messages per sound."""
    cpp = Configuration.channels_per_port
    if len(ports) * cpp <= len(sounds):
        raise Exception(
            f"Not enough ports. There are {len(sounds)} sounds, and {len(ports)} ports."
            "One port has only {cpp} channels."
        )
    for ix, sound in enumerate(sounds):
        sound.channel = ix % cpp
        sound.port = ports[ix // cpp]


def initialize() -> (List[Sound], List[rtmidi.MidiOut]):
    sounds = read_sounds()
    output_ports = _open_ports()
    _route_sounds(sounds, output_ports)
    return sounds, output_ports


class Player(object):
    """Schedule notes and play them."""

    EPSILON = 0.01

    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def schedule(
        self, sound: Sound, midi_no: int, time: float, duration: float, volume: int
    ) -> None:
        Player.schedule_note(
            self.scheduler, sound.port, sound.channel, midi_no, time, duration, volume
        )

    def play(self) -> None:
        self.scheduler.run()

    @staticmethod
    def schedule_note(
        scheduler: sched.scheduler,
        port: rtmidi.MidiOut,
        channel: int,
        midi_no: int,
        time: float,
        duration: float,
        volume: int,
    ) -> None:
        # print(OUTS.index(port) + 1, channel + 1, midi_no, time, duration, volume)
        scheduler.enter(
            delay=time + duration - Player.EPSILON,
            priority=1,
            action=port.send_message,
            argument=([NOTE_OFF | channel, midi_no, 0],),
        )
        scheduler.enter(
            delay=time,
            priority=10,
            action=port.send_message,
            argument=([NOTE_ON | channel, midi_no, volume],),
        )
