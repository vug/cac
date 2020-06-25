from matplotlib import pyplot as plt
from music21.pitch import Pitch
import networkx as nx

from entities import Section


def plot_instrument_ranges(sounds):
    inst_info = {
        (snd.short_name, snd.low_no, snd.high_no, snd.section): None for snd in sounds
    }.keys()
    color_map = {
        Section.PERCUSSION: "orange",
        Section.WOODWINDS: "green",
        Section.BRASS: "red",
        Section.STRINGS: "blue",
    }
    names, lows, highs, sections = zip(*inst_info)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.barh(
        y=list(range(len(names))),
        left=lows,
        width=[high - low for (low, high) in zip(lows, highs)],
        tick_label=names,
        color=[color_map[sec] for sec in sections],
    )
    # grid at Cs and Gs
    xticks = sorted(list(range(24, 111, 12)) + list(range(19, 111, 12)))
    ax.set_xticks(xticks)
    ax.set_xticklabels([Pitch(no) for no in xticks], rotation=0)
    ax.grid(axis="x", which="major")
    ax.set_title("Instrument Ranges")
    plt.tight_layout()
    plt.show()


def plot_hierarchical_graph(G):
    fig, ax = plt.subplots(figsize=(15, 15))
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    nx.draw(
        G,
        pos,
        with_labels=True,
        arrows=False,
        width=0.2,
        ax=ax,
        node_size=10,
        alpha=0.5,
        font_size=4,
    )
    plt.tight_layout()
    plt.show()
