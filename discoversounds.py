import csv
from dataclasses import dataclass, field

from music21.pitch import Pitch
import rtmidi

from configuration import Configuration

try:
    from entities import Section, Instrument, Articulation
except ModuleNotFoundError:
    print("entities.py does not existing. Generating...")
    import codegen

    codegen.codegen_entities_py()
    from entities import Section, Instrument, Articulation


@dataclass
class Sound(object):
    """Represents a BBC Symphony Orchestra Preset.

    Also knows MIDI port and channel to send MIDI messages
    to play that preset.
    """

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
    """Read from CSV file and create Sound objects."""
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


def query_sound(sounds, section, instrument, articulation):
    """Search a sound with given attributes."""

    def does_match(snd):
        return (
            snd.section == section
            and snd.instrument == instrument
            and snd.articulation == articulation
        )

    matches = [snd for snd in sounds if does_match(snd)]
    assert matches, "No Matching Instrument To Query"
    return matches[0]
