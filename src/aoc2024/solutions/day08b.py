import itertools

from typing import Generator

from .day08a import Vec2D, parse_antenna_groups


def resolve_antinodes(antennas:list[Vec2D], bounds:tuple[int,int]) -> Generator[Vec2D, None, None]:
    for loc1, loc2 in itertools.combinations(antennas, 2):
        offset = loc2 - loc1

        while loc1.in_bounds(*bounds):
            yield loc1
            loc1 -= offset

        while loc2.in_bounds(*bounds):
            yield loc2
            loc2 += offset
        

def solve(_input:str) -> int:
    map_bounds = (_input.index('\n'), len(_input.strip().splitlines()))

    antenna_groups = parse_antenna_groups(_input)

    antinodes = (resolve_antinodes(grp, map_bounds) for grp in antenna_groups)
    antinodes = set(itertools.chain(*antinodes))

    return len(antinodes)