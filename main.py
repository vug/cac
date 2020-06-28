from typing import Set

from music21.pitch import Pitch
from music21.scale import MajorScale
import networkx as nx

from cac import construct_graph, Triplet
from discoversounds import (
    query_sound,
    Section,
    Instrument,
    Articulation,
)
import midi
from midi import Player
from visualization import plot_hierarchical_graph


def main1():
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


def main2():
    from fractions import Fraction
    from typing import List, Tuple

    from cac import Graph

    Pattern = Tuple[Fraction, ...]
    # class Pattern(Tuple[int, ...]):
    #     def __str__(self):
    #         return " ".join([str(x) for x in self])

    def split_notes(pat: Pattern) -> List[Pattern]:
        successors = []
        # rule 1: single item can be replace with two items with 1/2 length
        for i in range(len(pat)):
            one = pat[i : i + 1]
            if True:
                double = (one[0] / 2,) * 2
                # succ = Pattern(pat[:i] + double + pat[i + 1 :])
                succ = pat[:i] + double + pat[i + 1 :]
                successors.append(succ)
        for i in range(len(pat) - 1):
            two = pat[i : i + 2]
            if two[0] == two[1]:
                triplet = (two[0] / 3 * 2,) * 3
                succ = pat[:i] + triplet + pat[i + 2 :]
                successors.append(succ)
        for i in range(len(pat) - 3):
            four = pat[i : i + 4]
            if four[0] == four[1] == four[2] == four[3]:
                quintlet = (four[0] / 5 * 4,) * 5
                succ = pat[:i] + quintlet + pat[i + 4 :]
                successors.append(succ)
        return successors

    # traverse one step from selected child at a time
    g1 = Graph[Pattern](split_notes)
    g1.traverse(start=(Fraction(1, 1),), distance=1)
    g1.traverse(start=(Fraction(1, 2), Fraction(1, 2)), distance=1)
    results = g1.traverse(
        start=(Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)), distance=1
    )

    # traverse all children in given distance
    g2 = Graph[Pattern](split_notes)
    g2.traverse(start=(Fraction(1, 1),), distance=2)

    def f2s(frs):
        return " ".join([str(fr) for fr in frs])

    print([f2s(u) for u in results])

    for u, vs in g2.adjacency.items():
        print(
            f2s(u), [f2s(v) for v in vs],
        )

    # G = g.get_networkx_graph()
    # print([f2s(nd) for nd in G.nodes], [(f2s(u), f2s(v)) for u, v in G.edges])
    # print(list(G.adjacency()))


if __name__ == "__main__":
    main2()
