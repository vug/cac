from collections import deque
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    List,
    Generic,
    Hashable,
    Set,
    Tuple,
    TypeVar,
)

from music21.pitch import Pitch
import networkx as nx
from networkx import convert


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


TVertex = TypeVar("TVertex", bound=Hashable)


class Graph(Generic[TVertex]):
    def __init__(
        self,
        compute_successors: Callable[[TVertex], List[TVertex]],
        pre_process: Callable[[TVertex], Any] = None,
        post_process: Callable[[TVertex], Any] = None,
        process_edge: Callable[[TVertex, TVertex], Any] = None,
    ):
        self._compute_successors = compute_successors
        self.vertices: Set[TVertex] = set()
        self.pre_process = pre_process
        self.post_process = post_process
        self.process_edge = process_edge
        self.adjacency: Dict[TVertex, List[TVertex]] = {}

    def get_successors(self, u: TVertex) -> List[TVertex]:
        """Get successors in memoized manner.

        If they are already computed, retrieve them from self.adjacency cache.
        Otherwise, compute and cache them.
        """
        if u not in self.adjacency:
            self.adjacency[u] = self._compute_successors(u)
        return self.adjacency[u]

    def traverse(self, start: TVertex, distance: int = 0) -> List[TVertex]:
        """Get the list of all vertices that are within distance away from start.

        While traversing caches edges in self.adjacency.
        distance = 0 returns vertex itself, however, outgoing edges are cached.
        distance = 1 returns vertex itself and its neighbors. Again outgoing
        edges from neighbors are cached.
        """
        traversed = []
        seen: Set[TVertex] = set([start])
        processed: Set[TVertex] = set()

        q = deque([start])
        while q and distance >= 0:
            for i in range(len(q)):  # trick to keep track of distance
                u = q.pop()
                traversed.append(u)
                if self.pre_process:
                    self.pre_process(u)
                successors = self.get_successors(u)
                processed.add(u)
                for v in successors:
                    if self.process_edge and v not in processed:
                        self.process_edge(u, v)
                    if v not in seen:
                        q.appendleft(v)
                        seen.add(v)
                if self.post_process:
                    self.post_process(u)
            distance -= 1
        return traversed

    def get_networkx_graph(self) -> nx.DiGraph:
        """make a nx graph from processed vertices/edges."""
        return convert.from_dict_of_lists(self.adjacency)
