import discoversounds
import midi
from midi import Player

try:
    from entities import Section, Instrument, Articulation
except ImportError:
    print("entities.py does not existing. Generating...")
    import codegen

    codegen.codegen_entities_py()


def initialize():
    sounds = discoversounds.read_sounds()
    output_ports = midi.open_ports()
    discoversounds.route_sounds(sounds, output_ports)
    return sounds


if __name__ == "__main__":
    sounds = initialize()

    basses = discoversounds.query_sound(
        sounds, Section.STRINGS, Instrument.BASSES, Articulation.SPICCATO
    )
    celli = discoversounds.query_sound(
        sounds, Section.STRINGS, Instrument.CELLI, Articulation.SPICCATO
    )
    violas = discoversounds.query_sound(
        sounds, Section.STRINGS, Instrument.VIOLAS, Articulation.SPICCATO
    )
    violins = discoversounds.query_sound(
        sounds, Section.STRINGS, Instrument.VIOLINS_1, Articulation.SPICCATO
    )

    p = Player()
    for i, snd in enumerate(sounds[:5]):
        midi_no = (snd.low_no + snd.high_no) // 2
        p.schedule(snd, midi_no, i * 0.2, 0.2, 100)
    p.play()
