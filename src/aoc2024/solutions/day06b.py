import itertools

from enum import IntEnum
from typing import TypeAlias, Generator

from .day06a import LabMap, LabGuard, Position


class InfiniteLoopException(Exception):
    pass


class Direction(IntEnum):
    north:int = 0
    east:int = 1
    south:int = 2
    west:int = 3
    
    def __add__(self, other_value:int):
        return self.__class__((self.value + other_value) % 4)
    
    @staticmethod
    def from_move(pos0:Position, pos1:Position) -> 'Direction':
        match (pos1[0] - pos0[0], pos1[1] - pos0[1]):
            case 0,-1:
                return Direction.north
            case 0,1:
                return Direction.south
            case 1,0:
                return Direction.east
            case -1,0:
                return Direction.west
            
        return None


Step:TypeAlias = tuple[Position, Direction]


class CarelessLabGuard(object):
    lab:LabMap
    
    pos_x:int
    pos_y:int
    
    start_direction:int
    
    visited:set[Step]
    
    extra_obstruction:Position
    
    def __init__(self, lab_map:LabMap, start_step:Step, block_pos:Position) -> None:
        self.lab = lab_map

        (self.pos_x, self.pos_y), self.start_direction = start_step
        
        self.visited = set()
        
        self.extra_obstruction = block_pos

    def _commit_path(self, path:list[Position], direction:Direction) -> None:
        if self.extra_obstruction in path:
            path = path[:path.index(self.extra_obstruction)]
        
        if len(path) == 0:
            return True
            
        new_visited = [(pos, direction) for pos in path]
        
        if not self.visited.isdisjoint(new_visited):
            raise InfiniteLoopException()
        
        self.pos_x, self.pos_y = path[-1]
        
        self.visited.update(new_visited)
        
        return self.lab.contains(self.pos_x, self.pos_y)
            
    def _walk_north(self) -> bool:
        col = reversed(self.lab.col_obstructions[self.pos_x])
        
        stop_row = next((i for i in col if i < self.pos_y), - 2)
        
        visit_rows = range(self.pos_y, stop_row, - 1)
        
        path = [(self.pos_x, row) for row in visit_rows]

        return self._commit_path(path, Direction.north)
            
    def _walk_south(self) -> bool:
        col = self.lab.col_obstructions[self.pos_x]
        
        stop_row = next((i for i in col if i > self.pos_y), self.lab.height + 1)
        
        visit_rows = range(self.pos_y, stop_row)
        
        path = [(self.pos_x, row) for row in visit_rows]

        return self._commit_path(path, Direction.south)

    def _walk_east(self) -> bool:
        row = self.lab.row_obstructions[self.pos_y]
        
        stop_col = next((i for i in row if i > self.pos_x), self.lab.width + 1)
        
        visit_cols = range(self.pos_x, stop_col)
        
        path = [(col, self.pos_y) for col in visit_cols]
        
        return self._commit_path(path, Direction.east)
    
    def _walk_west(self) -> bool:
        row = reversed(self.lab.row_obstructions[self.pos_y])
        
        stop_col = next((i for i in row if i < self.pos_x), - 2)
        
        visit_cols = range(self.pos_x, stop_col, - 1)
        
        path = [(col, self.pos_y) for col in visit_cols]

        return self._commit_path(path, Direction.west)
    
    def wait_for_guard_to_leave(self) -> None:
        guard_moves = itertools.cycle([
            self._walk_north, self._walk_east, self._walk_south, self._walk_west
        ])
        
        for _ in range(self.start_direction):
            next(guard_moves)
        
        while next(guard_moves).__call__():
            pass


def locate_locking_obstructions(lab_map:LabMap) -> Generator[Position, None, None]:
    unobstructed_guard = LabGuard(lab_map)
    unobstructed_guard.wait_for_guard_to_leave()
    
    visited = set()
    
    for current_pos, next_pos in itertools.pairwise(unobstructed_guard.path):
        visited.add(current_pos)
        
        start_dir = Direction.from_move(current_pos, next_pos)
        
        if start_dir is None or next_pos in visited:
            continue
        
        start_step = (current_pos, start_dir)
        
        try:
            test_guard = CarelessLabGuard(lab_map, start_step, block_pos=next_pos)
            test_guard.wait_for_guard_to_leave()
        except InfiniteLoopException:
            yield next_pos


def solve(_input:str) -> int:
    lab_map = LabMap(_input)
    
    return sum(1 for _ in locate_locking_obstructions(lab_map))