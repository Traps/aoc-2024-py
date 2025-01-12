
from collections.abc import Sequence
from typing import Generator, Iterable

from .day16a import XY, parse_map

SHORTCUT_DIST_MAX:int = 2
SHORTCUT_GAIN_MIN:int = 100


def neighbours_of(pos:XY) -> Generator[XY, None, None]:
    yield pos + (1, 0)
    yield pos + (0, 1)
    yield pos + (-1, 0)
    yield pos + (0, -1)


def resolve_track(start_pos:XY, exit_pos:XY, track:Iterable[XY]) -> Generator[XY, None, None]:
    unvisited = set(track)

    pos = start_pos
    yield pos

    while pos != exit_pos:
        yield (pos := next(p for p in neighbours_of(pos) if p in unvisited))
        unvisited.remove(pos)


def distance(p0:XY, p1:XY) -> int:
    return abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])


def locate_shortcuts(track_path:Sequence[XY], min_gain:int, cheat_length:int
                     ) -> dict[tuple[XY, XY], int]:
    shortcuts = {}

    for i,p0 in enumerate(track_path[:-min_gain]):
        for j,p1 in enumerate(track_path[i + min_gain + 1:], min_gain + 1):
            if 2 <= (dist := distance(p0, p1)) <= cheat_length:
                if (gain := j - dist) >= min_gain:
                    shortcuts[(p0, p1)] = gain

    return shortcuts


def solve(_input:str) -> int:
    start_pos, exit_pos, track = parse_map(_input)

    path = tuple(resolve_track(start_pos, exit_pos, track))
    
    return len(locate_shortcuts(path, SHORTCUT_GAIN_MIN, SHORTCUT_DIST_MAX))