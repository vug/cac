"""Do not modify manually. Autogenerated."""


from enum import auto, Enum


class Section(Enum):
    STRINGS = "Strings"
    BRASS = "Brass"
    WOODWINDS = "Woodwinds"
    PERCUSSION = "Percussion"


class Instrument(Enum):
    VIOLINS_1 = "Violins 1"
    VIOLINS_2 = "Violins 2"
    VIOLAS = "Violas"
    CELLI = "Celli"
    BASSES = "Basses"
    HORNS_A4 = "Horns a4"
    TRUMPETS_A3 = "Trumpets a3"
    TENOR_TROMBONES_A3 = "Tenor Trombones a3"
    BASS_TROMBONES_A2 = "Bass Trombones a2"
    TUBA = "Tuba"
    FLUTES_A3 = "Flutes a3"
    PICCOLO = "Piccolo"
    OBOES_A3 = "Oboes a3"
    CLARINETS_A3 = "Clarinets a3"
    BASSOONS_A3 = "Bassoons a3"
    HARP_AND_CELESTE = "Harp and Celeste"
    PERCUSSION = "Percussion"
    TUNED_PERCUSSION = "Tuned Percussion"


class Articulation(Enum):
    LONG = "Long"
    SPICCATO = "Spiccato"
    PIZZICATO = "Pizzicato"
    TREMOLO = "Tremolo"
    STACCATISSIMO = "Staccatissimo"
    HARP_PLUCKS = "Harp Plucks"
    CELESTE = "Celeste"
    TIMPANI_HITS = "Timpani Hits"
    UNTUNED_PERCUSSION = "Untuned Percussion"
    TUBULAR_BELLS = "Tubular Bells"
    MARIMBA = "Marimba"
    XYLOPHONE = "Xylophone"
    GLOCKENSPIEL = "Glockenspiel"
