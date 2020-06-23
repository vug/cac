import sched
import time

import discoversounds
import midi
from midi import NOTE_ON, NOTE_OFF, abidin

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


def get_sound(sounds, section, instrument, articulation):
    def does_match(snd):
        return (
            snd.section == section
            and snd.instrument == instrument
            and snd.articulation == articulation
        )

    matches = [snd for snd in SOUNDS if does_match(snd)]
    assert matches, "No Matching Instrument To Query"
    return matches[0]


def schedule_note(scheduler, port, channel, midi_no, time, duration, volume):
    #     print(OUTS.index(port) + 1, channel + 1, midi_no, time, duration, volume)
    scheduler.enter(
        time + duration - 0.01,
        1,
        port.send_message,
        argument=([NOTE_OFF | channel, midi_no, 0],),
    )
    scheduler.enter(
        time, 10, port.send_message, argument=([NOTE_ON | channel, midi_no, volume],)
    )


if __name__ == "__main__":
    sounds = initialize()
    # snd = sounds[0]
    # print(sounds[:2])

    s = sched.scheduler(time.time, time.sleep)
    for i, snd in enumerate(sounds[:5]):
        mid_no = (snd.low_no + snd.high_no) // 2
        # print(i, OUTS.index(snd.port) + 1, snd.channel + 1, snd.long_name)
        schedule_note(s, snd.port, snd.channel, mid_no, i * 0.2, 0.19, 100)
    s.run()
