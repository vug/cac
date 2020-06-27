from collections import deque
from typing import Any, Callable, Set, List, Tuple, Hashable, Generic, TypeVar, cast

from music21.pitch import Pitch

class Triplet(object):
    """A container of 3 Pitches.

    Two different triplets with same pitches have different ids
    but have same hashes and are equal."""

    def __init__(self, pitches: Tuple[Pitch, Pitch, Pitch]):
        # maybe compare their midi numbers.
        if not pitches[0] <= pitches[1] <= pitches[2]:
            pitches = cast(Tuple[Pitch, Pitch, Pitch], tuple(sorted(pitches)))
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

