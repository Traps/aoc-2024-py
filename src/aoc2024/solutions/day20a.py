
from typing import Generator, Iterable

from .day16a import XY, parse_map

from .day20util import count_shortcuts

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


def solve(_input:str) -> int:
    start_pos, exit_pos, track = parse_map(_input)

    path = list(resolve_track(start_pos, exit_pos, track))
    
    return count_shortcuts(path, SHORTCUT_GAIN_MIN, SHORTCUT_DIST_MAX)