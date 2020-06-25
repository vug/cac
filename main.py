from collections import deque
from typing import Callable, Tuple, Set

from music21.pitch import Pitch
from music21.scale import MajorScale
import networkx as nx

from discoversounds import (
    query_sound,
    Section,
    Instrument,
    Articulation,
)
import midi
from midi import Player
from visualization import plot_hierarchical_graph


class Triplet(object):
    """A container of 3 Pitches.

    Two different triplets with same pitches have different ids
    but have same hashes and are equal."""

    def __init__(self, pitches: Tuple[Pitch, Pitch, Pitch]):
        # maybe compare their midi numbers.
        if not pitches[0] <= pitches[1] <= pitches[2]:
            pitches = tuple(sorted(pitches))
        self.pitches = pitches
        self.midi_nos = tuple(p.midi for p in pitches)

    def __hash__(self):
        return hash(self.midi_nos)

    def __eq__(self, other):
        return self.midi_nos == other.midi_nos

    def __str__(self):
        pitch_names = [str(p) for p in self.pitches]
        return f"({' '.join(pitch_names)})"

    def __repr__(self):
        return self.__str__()


all_pitches = MajorScale(tonic="C").getPitches("C1", "C8")
pitch2index = {p: ix for ix, p in enumerate(all_pitches)}
C2 = Pitch("C2")
C3 = Pitch("C3")
C4 = Pitch("C4")
C5 = Pitch("C5")
C6 = Pitch("C6")


def get_next_triplets(triplet: Triplet) -> Set[Triplet]:
    next_triplets = set()
    for i, pitch in enumerate(triplet.pitches):
        # TODO: improve construct_graph to accept negative values here
        for diff in [1]:
            # TODO: make this a utility function
            moved_pitch = all_pitches[pitch2index[pitch] + diff]
            if moved_pitch in triplet.pitches:
                continue
            next_pitches = tuple(
                p if i != j else moved_pitch for j, p in enumerate(triplet.pitches)
            )
            if (
                not C2 <= next_pitches[0] <= C4
                or not C3 <= next_pitches[1] <= C5
                or not C4 <= next_pitches[2] <= C6
            ):
                continue
            next_triplets.add(Triplet(next_pitches))
    return next_triplets


def filter_triplets(curr, successors):
    pass


def construct_graph(
    init: Triplet, next_states_func: Callable, steps: int
) -> Tuple[Set[Triplet], Set[Tuple[Triplet, Triplet]]]:
    q = deque([init])
    vertices = set()
    edges = set()
    while q and steps > 0:
        for _ in range(len(q)):
            curr = q.pop()
            vertices.add(curr)
            successors = next_states_func(curr)
            for succ in successors:
                edges.add((curr, succ))
                if succ not in vertices and succ not in q:
                    q.appendleft(succ)
        steps -= 1
    return vertices, edges


def main():
    init_pitches = (Pitch("C2"), Pitch("C3"), Pitch("C4"))
    init_triplet = Triplet(init_pitches)
    _, edges = construct_graph(init_triplet, get_next_triplets, 48)
    G = nx.DiGraph()
    G.add_edges_from(edges)
    plot_hierarchical_graph(G)  # blocking

    progression = []
    chord = init_triplet
    while chord:
        progression.append(chord)
        successors = list(G.successors(chord))
        if successors:
            chord = successors[len(successors) // 2]
        else:
            chord = None
    print(progression)

    sounds, _ = midi.initialize()

    _ = query_sound(sounds, Section.STRINGS, Instrument.BASSES, Articulation.SPICCATO)
    celli = query_sound(
        sounds, Section.STRINGS, Instrument.CELLI, Articulation.SPICCATO
    )
    violas = query_sound(
        sounds, Section.STRINGS, Instrument.VIOLAS, Articulation.SPICCATO
    )
    violins = query_sound(
        sounds, Section.STRINGS, Instrument.VIOLINS_1, Articulation.SPICCATO
    )

    _ = query_sound(sounds, Section.BRASS, Instrument.TUBA, Articulation.STACCATISSIMO)
    trombones = query_sound(
        sounds, Section.BRASS, Instrument.TENOR_TROMBONES_A3, Articulation.STACCATISSIMO
    )
    trumpets = query_sound(
        sounds, Section.BRASS, Instrument.TRUMPETS_A3, Articulation.STACCATISSIMO
    )
    horns = query_sound(
        sounds, Section.BRASS, Instrument.HORNS_A4, Articulation.STACCATISSIMO
    )

    strings = (celli, violas, violins)
    brass = (trombones, trumpets, horns)
    dt = 0.175
    dur = 0.125

    p = Player()
    for measure, triplet in enumerate(progression):
        for beat in range(4):
            for note, snd in zip(triplet.pitches, strings):
                p.schedule(snd, Pitch(note).midi, (beat + measure * 4) * dt, dur, 100)
        for note, snd in zip(triplet.pitches, brass):
            p.schedule(snd, Pitch(note).midi, measure * 4 * dt, dur * 2, 100)
            p.schedule(snd, Pitch(note).midi, (measure * 4 + 3.25) * dt, dur * 0.5, 100)
    p.play()


if __name__ == "__main__":
    main()
