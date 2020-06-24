import csv
from dataclasses import dataclass, field

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


def query_sound(sounds, section, instrument, articulation):
    def does_match(snd):
        return (
            snd.section == section
            and snd.instrument == instrument
            and snd.articulation == articulation
        )

    matches = [snd for snd in sounds if does_match(snd)]
    assert matches, "No Matching Instrument To Query"
    return matches[0]
