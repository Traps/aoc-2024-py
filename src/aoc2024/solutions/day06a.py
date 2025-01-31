import itertools

from typing import Final, TypeAlias


SYMBOL_GUARD:Final[str] = '^'
SYMBOL_OBSTRUCTION:Final[str] = '#'

Position:TypeAlias = tuple[int, int]


def locate_obstructions(map_slice:str) -> tuple[int, ...]:
    return tuple(i for i,c in enumerate(map_slice) if c == SYMBOL_OBSTRUCTION)


class LabMap(object):
    row_obstructions:tuple[tuple[int, ...], ...]
    col_obstructions:tuple[tuple[int, ...], ...]
    
    guard_x:int
    guard_y:int
    
    width:int
    height:int
    
    def __init__(self, text_map:str):
        text_rows = tuple(text_map.splitlines())
        text_cols = tuple(''.join(c) for c in zip(*text_rows))
        
        self.row_obstructions = tuple(map(locate_obstructions, text_rows))
        self.col_obstructions = tuple(map(locate_obstructions, text_cols))
    
        self.width = len(self.col_obstructions)
        self.height = len(self.row_obstructions)
    
        self.guard_y = next(i for i,row in enumerate(text_rows) if SYMBOL_GUARD in row)
        self.guard_x = text_rows[self.guard_y].index(SYMBOL_GUARD)
        
    def contains(self, x:int, y:int) -> bool:
        return (0 <= x < self.width) and (0 <= y < self.height)


class LabGuard(object):
    lab:LabMap
    
    pos_x:int
    pos_y:int
    
    path:list[Position]
    
    def __init__(self, lab_map:LabMap) -> None:
        self.lab = lab_map
        
        self.pos_x = lab_map.guard_x
        self.pos_y = lab_map.guard_y
        
        self.path = list()
            
    def _commit_path(self, path:list[Position]) -> bool:
        if len(path) == 0:
            return True
        
        self.pos_x, self.pos_y = path[-1]

        if not (guard_on_map := self.lab.contains(self.pos_x, self.pos_y)):
            path.pop()
        
        self.path.extend(path)
        
        return guard_on_map
            
    def _walk_north(self) -> bool:
        col = reversed(self.lab.col_obstructions[self.pos_x])
        
        stop_row = next((i for i in col if i < self.pos_y), - 2)
        
        visit_rows = range(self.pos_y, stop_row, - 1)

        return self._commit_path([(self.pos_x, row) for row in visit_rows])
            
    def _walk_south(self) -> bool:
        col = self.lab.col_obstructions[self.pos_x]
        
        stop_row = next((i for i in col if i > self.pos_y), self.lab.height + 1)
        
        visit_rows = range(self.pos_y, stop_row)

        return self._commit_path([(self.pos_x, row) for row in visit_rows])

    def _walk_east(self) -> bool:
        row = self.lab.row_obstructions[self.pos_y]
        
        stop_col = next((i for i in row if i > self.pos_x), self.lab.width + 1)
        
        visit_cols = range(self.pos_x, stop_col)
        
        return self._commit_path([(col, self.pos_y) for col in visit_cols])
    
    def _walk_west(self) -> bool:
        row = reversed(self.lab.row_obstructions[self.pos_y])
        
        stop_col = next((i for i in row if i < self.pos_x), - 2)
        
        visit_cols = range(self.pos_x, stop_col, - 1)

        return self._commit_path([(col, self.pos_y) for col in visit_cols])
    
    def wait_for_guard_to_leave(self) -> None:
        guard_moves = itertools.cycle([
            self._walk_north, self._walk_east, self._walk_south, self._walk_west
        ])
        
        while next(guard_moves).__call__():
            pass


def solve(_input:str) -> int:
    lab = LabMap(_input)

    guard = LabGuard(lab)
    guard.wait_for_guard_to_leave()

    return len(set(guard.path))