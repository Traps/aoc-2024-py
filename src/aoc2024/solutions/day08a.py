import dataclasses
import itertools

from collections import defaultdict
from typing import Generator


SYMBOL_NO_ANTENNA:str = '.'


@dataclasses.dataclass(frozen=True, slots=True)
class Vec2D(object):
    x:int
    y:int
    
    def __add__(self, other:'Vec2D') -> 'Vec2D':
        return Vec2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other:'Vec2D') -> 'Vec2D':
        return Vec2D(self.x - other.x, self.y - other.y)
    
    def in_bounds(self, map_width:int, map_height:int) -> bool:
        return 0 <= self.x < map_width and 0 <= self.y < map_height


def parse_antenna_groups(_input:str) -> list[list[Vec2D]]:
    antenna_locs = defaultdict(list)

    for y, line in enumerate(_input.splitlines()):
        for x, symbol in enumerate(line):
            if symbol == SYMBOL_NO_ANTENNA:
                continue
            
            antenna_locs[symbol].append(Vec2D(x, y))

    return list(antenna_locs.values())


def resolve_antinodes(antennas:list[Vec2D], bounds:tuple[int,int]) -> Generator[Vec2D, None, None]:
    for loc1, loc2 in itertools.combinations(antennas, 2):
        offset = loc2 - loc1
        
        if (antinode1 := loc2 + offset).in_bounds(*bounds):
            yield antinode1

        if (antinode2 := loc1 - offset).in_bounds(*bounds):
            yield antinode2
        

def solve(_input:str) -> int:
    map_bounds = (_input.index('\n'), len(_input.strip().splitlines()))

    antenna_groups = parse_antenna_groups(_input)

    antinodes = (resolve_antinodes(grp, map_bounds) for grp in antenna_groups)
    antinodes = set(itertools.chain(*antinodes))

    return len(antinodes)