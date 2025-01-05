import numpy

from typing import Generator

from .day14a import parse_robots, WORLD_SIZE_CHALLENGE


def measure_spread(robot_pos:numpy.ndarray) -> numpy.float64:
    offset = robot_pos - numpy.mean(robot_pos, axis=0)

    return numpy.pow(offset, 2).sum()


def generate_robot_positions(start_pos:numpy.ndarray, vel:numpy.ndarray,
                             world_size:tuple[int, int]
                             ) -> Generator[numpy.ndarray, None, None]:
    t_max = numpy.prod(world_size)

    pos = start_pos.copy()

    world_wrap = numpy.array([world_size] * len(start_pos))

    for _ in range(t_max):
        yield numpy.mod(pos + vel, world_wrap, out=pos)


def solve(_input:str) -> int:
    robots = numpy.array(list(parse_robots(_input)), dtype=int)

    pos, vel = numpy.split(robots, 2, axis=-1)

    round_pos = generate_robot_positions(pos, vel, WORLD_SIZE_CHALLENGE)

    round_spread = (measure_spread(p_round) for p_round in round_pos)

    return min(enumerate(round_spread), key=lambda r: r[1])[0]
    