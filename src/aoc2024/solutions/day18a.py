from types import NoneType
from typing import Generator, Iterable

from .day16a import XY


FALLEN_COUNT_CHALLENGE:int = 1024
FALLEN_COUNT_SAMPLE:int = 12

WORLD_SIZE_CHALLENGE:int = 71
WORLD_SIZE_SAMPLE:int = 7


def parse_falling_bytes(_bytes:str) -> Generator[XY, None, None]:
    for byte in _bytes.splitlines():
        yield XY(*map(int, byte.split(',')))


def neighbours_of(pos:XY) -> Generator[XY, None, None]:
    yield pos + (1, 0)
    yield pos + (0, 1)
    yield pos + (-1, 0)
    yield pos + (0, -1)


def in_bounds(pos:XY, world_size:int) -> bool:
    return 0 <= pos.x < world_size and 0 <= pos.y < world_size


def find_exit_distance(fallen_bytes:Iterable[XY], world_size:int) -> int|NoneType:
    fallen_bytes = set(fallen_bytes)

    default_dist = world_size * world_size + 1

    pos_start = XY(0, 0)
    pos_exit = XY(world_size - 1, world_size - 1)

    to_visit = [(0, pos_start)]

    distances = {pos_start: 0}

    while to_visit:
        current_dist, current_pos = to_visit.pop()

        new_dist = current_dist + 1

        if new_dist > distances.get(pos_exit, default_dist):
            break

        for new_pos in neighbours_of(current_pos):
            if not in_bounds(new_pos, world_size) or new_pos in fallen_bytes:
                continue

            if distances.get(new_pos, default_dist) > new_dist:            
                distances[new_pos] = new_dist
                to_visit.append((new_dist, new_pos))

        to_visit.sort(key=lambda p: p[0], reverse=True)
    
    return distances.get(pos_exit, None)


def solve(_intput:str) -> int:
    falling_bytes = list(parse_falling_bytes(_intput))

    if len(falling_bytes) >= FALLEN_COUNT_CHALLENGE:
        world_size = WORLD_SIZE_CHALLENGE
        fallen_bytes = falling_bytes[:FALLEN_COUNT_CHALLENGE]
    else:
        world_size = WORLD_SIZE_SAMPLE
        fallen_bytes = falling_bytes[:FALLEN_COUNT_SAMPLE]

    return find_exit_distance(fallen_bytes, world_size)

    