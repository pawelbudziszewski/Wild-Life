"""Species to be used by Wild Life app.
Each life form should be provided as a list of strings (one string per
line), with '#' character representing life cell, any other character
representing background.
All life forms must be converted to Numpy array of floats using 
convert_species()
"""
import numpy as np

def convert_species(species):
    """Convert str-based life form to np array of floats.
    """
    return np.array([[1.0*(c=='#') for c in ln] for ln in species])

GOSPER_GLIDER_GUN = [
    '........................#...........',
    '......................#.#...........',
    '............##......##............##',
    '...........#...#....##............##',
    '##........#.....#...##..............',
    '##........#...#.##....#.#...........',
    '..........#.....#.......#...........',
    '...........#...#....................',
    '............##......................',
    ]
GOSPER_GLIDER_GUN = convert_species(GOSPER_GLIDER_GUN)

PULSAR = [
    '..###...###..',
    '.............',
    '#....#.#....#',
    '#....#.#....#',
    '#....#.#....#',
    '..###...###..',
    '.............',
    '..###...###..',
    '#....#.#....#',
    '#....#.#....#',
    '#....#.#....#',
    '.............',
    '..###...###..',
    ]
PULSAR = convert_species(PULSAR)

GLIDERS = [
    '..##.##..',
    '.#.#.#.#.',
    '#..#.#..#',
    '.#.#.#.#.',
    '..##.##..',
    ]
GLIDERS = convert_species(GLIDERS)

KOKS_GALAXY = [
    '......##...',
    '.......#...',
    '..###..##..',
    '###.#...#..',
    '#....#.##..',
    '....#.#....',
    '..##.#....#',
    '..#...#.###',
    '..##..###..',
    '...#.......',
    '...##......',
    ]
KOK_GALAXY = convert_species(KOKS_GALAXY)

TURTLE_L = [
    '.###.......#',
    '.##..#.##.##',
    '...###....#.',
    '.#..#.#...#.',
    '#....#....#.',
    '#....#....#.',
    '.#..#.#...#.',
    '...###....#.',
    '.##..#.##.##',
    '.###.......#',
    ]
TURTLE_L = convert_species(TURTLE_L)
TURTLE_R = np.flip(TURTLE_L, 1)

BLIMKER_PUFFER = [
    '.............###.',
    '............#####',
    '...........##.###',
    '............##...',
    '.................',
    '.................',
    '.........#.#.....',
    '..#.....#..#.....',
    '.#####...#.#.....',
    '##...##.##.......',
    '.#.......#.......',
    '..##..#..#.......',
    '..........#......',
    '..##..#..#.......',
    '.#.......#.......',
    '##...##.##.......',
    '.#####...#.#.....',
    '..#.....#..#.....',
    '.........#.#.....',
    '.................',
    '.................',
    '............##...',
    '...........##.###',
    '............#####',
    '.............###.',
    ]
BLIMKER_PUFFER = convert_species(BLIMKER_PUFFER)

# This is just a blank "stamp" - may be used to clean the life arena.
BLANK = np.zeros((13,13))
