from collections import deque
from typing import Callable, List, Tuple

from music21.pitch import Pitch
from music21.scale import MajorScale

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


def get_next_triplets1(curr: Triplet) -> List[Triplet]:
    pitches = (curr.pitches[0], curr.pitches[1], curr.pitches[2].transpose(2))
    succ = Triplet(pitches)
    if succ.pitches[2] < Pitch("C4"):
        return [succ]
    else:
        return []


def get_next_triplets(triplet: Triplet) -> List[Triplet]:
    all_pitches = MajorScale(tonic="C").getPitches("C1", "C8")
    next_triplets = set()
    for i, pitch in enumerate(triplet.pitches):
        # TODO: improve construct_graph to accept negative values here
        for diff in [1]:
            # TODO: make this a utility function
            moved_pitch = all_pitches[all_pitches.index(pitch) + diff]
            if moved_pitch in triplet.pitches:
                continue
            next_pitches = list(triplet.pitches).copy()
            next_pitches[i] = moved_pitch
            next_pitches = tuple(next_pitches)
            if not Pitch("C2") <= next_pitches[0] <= Pitch("C4"):
                continue
            if not Pitch("C3") <= next_pitches[1] <= Pitch("C5"):
                continue
            if not Pitch("C4") <= next_pitches[2] <= Pitch("C6"):
                continue
            next_triplets.add(Triplet(next_pitches))
    return list(next_triplets)


def construct_graph(init: Triplet, next_states_func: Callable, steps: int):
    q = deque([init])
    vertices = set()
    edges = set()
    while q and steps > 0:
        for _ in range(len(q)):
            curr = q.pop()
            vertices.add(curr)
            for succ in next_states_func(curr):
                edges.add((curr, succ))
                if succ not in vertices and succ not in q:
                    q.appendleft(succ)
        steps -= 1
    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G


def main3():
    init_pitches = (Pitch("C2"), Pitch("C3"), Pitch("G3"))
    init_triplet = Triplet(init_pitches)
    successors = get_next_triplets(init_triplet)
    print(init_triplet, successors)
    G = construct_graph(init_triplet, get_next_triplets1, 2)
    print(G.edges)


if __name__ == "__main__":
    main3()


def main1():
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
