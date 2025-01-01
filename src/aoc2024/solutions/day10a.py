from typing import Generator, TypeAlias

from .day04a import XY


ElevationIndex:TypeAlias = tuple[tuple[XY, ...], ...]

DIRECTIONS:tuple[XY, ...] = (XY(1,0), XY(0,-1), XY(-1,0), XY(0,1))


def parse_elevation_map(text_map:str) -> ElevationIndex:
    elevation_index = [[] for _ in range(10)]

    for y,line in enumerate(text_map.splitlines()):
        for x,c in enumerate(line):
            elevation_index[int(c)].append(XY(x, y))

    return elevation_index


def find_trail_ends(elev:int, pos:XY, elevation_index:ElevationIndex) -> Generator[XY, None, None]:
    if elev > 9 or pos not in elevation_index[elev]:
        return

    if elev == 9:
        yield pos
    
    for step in DIRECTIONS:
        yield from find_trail_ends(elev + 1, pos + step, elevation_index)


def score_trailhead(pos:XY, elevation_index:ElevationIndex) -> int:
    if pos not in elevation_index[0]:
        return 0
    
    return len(set(find_trail_ends(0, pos, elevation_index)))


def solve(_input:str) -> int:
    elevation_index = parse_elevation_map(_input)

    return sum(score_trailhead(pos, elevation_index) for pos in elevation_index[0])