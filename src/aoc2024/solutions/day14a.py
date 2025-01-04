import numpy
import re

from typing import Generator

WORLD_SIZE_SAMPLE:tuple[int, int] = (11, 7) 
WORLD_SIZE_CHALLENGE:tuple[int, int] = (101, 103)

ROBOT_COUNT_CHALLENGE:int = 500


def parse_robots(robots:str) -> Generator[tuple[int, ...], None, None]:
    for robot in robots.splitlines():
        yield tuple(map(int, re.findall(r'\-?\d+', robot)))


def calculate_safety_factor(robot_pos:numpy.ndarray, world_size:tuple[int, int]
                          ) -> Generator[int, None, None]:
    
    mid_x, mid_y = numpy.array(world_size) // 2
    pos_x, pos_y = numpy.split(robot_pos, 2, axis=-1)

    safety_factor = numpy.prod([
        ((pos_x < mid_x) & (pos_y < mid_y)).sum(),
        ((pos_x > mid_x) & (pos_y < mid_y)).sum(),
        ((pos_x > mid_x) & (pos_y > mid_y)).sum(),
        ((pos_x < mid_x) & (pos_y > mid_y)).sum()
    ])

    return int(safety_factor)


def solve(_input:str) -> int:
    robots = numpy.array(list(parse_robots(_input)), dtype=int)
    
    if len(robots) == ROBOT_COUNT_CHALLENGE:
        world_size = WORLD_SIZE_CHALLENGE
    else:
        world_size = WORLD_SIZE_SAMPLE
     
    start_pos, vel = numpy.split(robots, 2, axis=-1)
    
    end_pos = numpy.mod(start_pos + vel * 100, [world_size] * len(robots))
    
    return calculate_safety_factor(end_pos, world_size)