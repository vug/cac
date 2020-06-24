from discoversounds import (
    query_sound,
    Section,
    Instrument,
    Articulation,
)
import midi
from midi import Player


class Triplet(object):
    """A container of 3 Pitches.

    Two different triplets with same pitches have different ids
    but have same hashes and are equal."""

    def __init__(self, pitches: Tuple[Pitch, Pitch, Pitch]):
        if not pitches[0] <= pitches[1] <= pitches[2]:
            pitches = tuple(sorted(pitches))
        self.pitches = pitches

    def __hash__(self):
        return hash(self.pitches)

    def __eq__(self, other):
        return self.pitches == other.pitches

    def __str__(self):
        pitch_names = [str(p) for p in self.pitches]
        return f"({' '.join(pitch_names)})"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    sounds, _ = midi.initialize()

    basses = query_sound(
        sounds, Section.STRINGS, Instrument.BASSES, Articulation.SPICCATO
    )
    celli = query_sound(
        sounds, Section.STRINGS, Instrument.CELLI, Articulation.SPICCATO
    )
    violas = query_sound(
        sounds, Section.STRINGS, Instrument.VIOLAS, Articulation.SPICCATO
    )
    violins = query_sound(
        sounds, Section.STRINGS, Instrument.VIOLINS_1, Articulation.SPICCATO
    )

    p = Player()
    for i, snd in enumerate(sounds[:5]):
        midi_no = (snd.low_no + snd.high_no) // 2
        p.schedule(snd, midi_no, i * 0.2, 0.2, 100)
    p.play()
