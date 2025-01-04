import re
import numpy

from typing import NamedTuple, Generator, TypeAlias

class Vec2D(NamedTuple):
    x:int
    y:int
    
    def __add__(self, other:'Vec2D') -> 'Vec2D':
        return Vec2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other:'Vec2D') -> 'Vec2D':
        return Vec2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, factor:int):
        return Vec2D(self.x * factor, self.y * factor)


def parse_robots(robots:str) -> Generator[tuple[int, ...], None, None]:
    for robot in robots.splitlines():
        yield tuple(map(int, re.findall(r'\-?\d+', robot)))


def simulate_robot(pos:Vec2D, vel:Vec2D, sim_sec:int, world_size:Vec2D) -> Vec2D:
    new_pos = pos + vel * sim_sec
    
    return Vec2D(new_pos.x % world_size.x, new_pos.y % world_size.y)
    
    

def solve(_input:str) -> int:
    world_size = [11, 7]
    
    robots = numpy.asarray(list(parse_robots(_input)), dtype=int)
    
    pos, vel = numpy.split(robots, 2, axis=-1)
    

    new_pos = numpy.mod(pos + vel * 100, [world_size] * len(robots))
    
    return new_pos
    
    for robot in parse_robots(_input):
        new_pos = simulate_robot(*robot, 100, world_size)
        
        print(new_pos)