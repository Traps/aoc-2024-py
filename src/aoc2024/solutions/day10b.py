from .day04a import XY
from .day10a import ElevationIndex, find_trail_ends, parse_elevation_map


def score_trailhead(pos:XY, elevation_index:ElevationIndex) -> int:
    if pos not in elevation_index[0]:
        return 0
    
    return sum(1 for _ in find_trail_ends(0, pos, elevation_index))


def solve(_input:str) -> int:
    elevation_index = parse_elevation_map(_input)

    return sum(score_trailhead(pos, elevation_index) for pos in elevation_index[0])