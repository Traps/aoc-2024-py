from typing import Iterable

from .day16a import XY
from .day18a import (parse_falling_bytes, neighbours_of, in_bounds, 
                     WORLD_SIZE_CHALLENGE, WORLD_SIZE_SAMPLE,
                     FALLEN_COUNT_CHALLENGE, FALLEN_COUNT_SAMPLE)


def can_reach_exit(fallen_bytes:Iterable[XY], world_size:int) -> bool:
    fallen_bytes = set(fallen_bytes)

    pos_exit = XY(world_size - 1, world_size - 1)

    to_visit = [XY(0, 0)]

    while to_visit:
        current_pos = to_visit.pop()

        for pos in neighbours_of(current_pos):
            if pos == pos_exit:
                return True
            
            if not in_bounds(pos, world_size) or pos in fallen_bytes:
                continue

            fallen_bytes.add(pos)
            to_visit.append(pos)

        to_visit.sort(key=sum, reverse=False)

    return False


def solve(_intput:str) -> str:
    falling_bytes = list(parse_falling_bytes(_intput))

    if len(falling_bytes) >= FALLEN_COUNT_CHALLENGE:
        world_size = WORLD_SIZE_CHALLENGE
        fallen_count = FALLEN_COUNT_CHALLENGE
    else:
        world_size = WORLD_SIZE_SAMPLE
        fallen_count = FALLEN_COUNT_SAMPLE

    step_size = len(falling_bytes) - fallen_count
    last_reachable = fallen_count

    while True:
        step_size = max(step_size // 2, 1)
        fallen_count += step_size

        if can_reach_exit(falling_bytes[:fallen_count], world_size):
            last_reachable = fallen_count
            continue
    
        if last_reachable == fallen_count - 1:
            return ','.join(map(str, falling_bytes[last_reachable]))
        
        fallen_count = last_reachable