class Configuration(object):
    """Environment information such as virtual port names, CSV files."""

    virtual_ports = [
        "loopMIDI Port 1 1",
        "loopMIDI Port 2 2",
        "loopMIDI Port 3 3",
        "loopMIDI Port 4 4",
    ]
    enums_file = "sounds/BBC Symphony Discover Sounds Dataset - Enums.csv"
    ranges_file = "sounds/BBC Symphony Discover Sounds Dataset - Ranges.csv"
    sounds_file = "sounds/BBC Symphony Discover Sounds Dataset - Sounds.csv"
    channels_per_port = 16
