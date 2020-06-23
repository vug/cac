import csv
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from matplotlib import pyplot as plt
from music21.pitch import Pitch
import rtmidi

from configuration import Configuration
from entities import Section, Instrument, Articulation


@dataclass
class Sound(object):
    long_name: str
    section: Section
    instrument: Instrument
    articulation: Articulation
    short_name: str
    low: str
    high: str
    low_no: int = field(init=False)
    high_no: int = field(init=False)
    # will be set by router
    port: rtmidi.MidiOut = None
    channel: int = None

    def __post_init__(self):
        self.low_no = Pitch(self.low).midi
        self.high_no = Pitch(self.high).midi


def read_sounds():
    with open(Configuration.ranges_file) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        next(reader)
        rows = list(reader)
        RANGES = {r[0]: (r[1], r[2]) for r in rows}

    sounds = []
    with open(Configuration.sounds_file) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        next(reader)
        for row in reader:
            ix, section, instrument, articulation, short_name = row
            long_name = f"{section} - {instrument} - {articulation}"
            low, high = RANGES[short_name]
            snd = Sound(
                long_name,
                Section(section),
                Instrument(instrument),
                Articulation(articulation),
                short_name,
                low,
                high,
            )
            sounds.append(snd)

    return sounds


def route_sounds(sounds, ports):
    cpp = Configuration.channels_per_port
    if len(ports) * cpp <= len(sounds):
        raise Exception(
            f"Not enough ports. There are {len(sounds)} sounds, and {len(ports)} ports."
            "One port has only {cpp} channels."
        )
    for ix, sound in enumerate(sounds):
        sound.channel = ix % cpp
        sound.port = ports[ix // cpp]


def plot_instrument_ranges(sounds):
    inst_info = {
        (snd.short_name, snd.low_no, snd.high_no, snd.section): None for snd in sounds
    }.keys()
    color_map = {
        Section.PERCUSSION: "orange",
        Section.WOODWINDS: "green",
        Section.BRASS: "red",
        Section.STRINGS: "blue",
    }
    names, lows, highs, sections = zip(*inst_info)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.barh(
        y=list(range(len(names))),
        left=lows,
        width=[high - low for (low, high) in zip(lows, highs)],
        tick_label=names,
        color=[color_map[sec] for sec in sections],
    )
    # grid at Cs and Gs
    xticks = sorted(list(range(24, 111, 12)) + list(range(19, 111, 12)))
    ax.set_xticks(xticks)
    ax.set_xticklabels([Pitch(no) for no in xticks], rotation=0)
    ax.grid(axis="x", which="major")
    ax.set_title("Instrument Ranges")
    plt.tight_layout()
    plt.show()
