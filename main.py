from discoversounds import (
    query_sound,
    Section,
    Instrument,
    Articulation,
)
import midi
from midi import Player


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
