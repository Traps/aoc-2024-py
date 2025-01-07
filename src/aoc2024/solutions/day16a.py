import enum
import typing


class Direction(enum.IntEnum):
    EAST:int = 0
    SOUTH:int = 1
    WEST:int = 2
    NORTH:int = 3
    
    def __add__(self, value:int) -> 'Direction':
        return self.__class__((self.value + value) % 4)
    
    def __sub__(self, value:int) -> 'Direction':
        return self.__class__((self.value - value) % 4)


class MapSymbol(enum.StrEnum):
    WALL:str = '#'
    PATH:str = '.'
    START:str = 'S'
    EXIT:str = 'E'
    

class XY(typing.NamedTuple):
    x:int
    y:int
    
    def __add__(self, other:tuple) -> 'XY':
        return XY(self.x + other[0], self.y + other[1])
    

class State(typing.NamedTuple):
    pos:XY
    facing:Direction
    
    def move(self, direction:Direction) -> 'State':
        match direction:
            case Direction.EAST:
                return State(self.pos + (1, 0), direction)
            case Direction.SOUTH:
                return State(self.pos + (0, 1), direction)
            case Direction.WEST:
                return State(self.pos + (-1, 0), direction)
            case Direction.NORTH:
                return State(self.pos + (0, -1), direction)
    
    def get_move_options(self) -> typing.Generator[tuple['State', int], None, None]:
        yield (self.move(self.facing), 1)
        yield (self.move(self.facing - 1), 1001)
        yield (self.move(self.facing + 1), 1001)


def parse_map(maze_map:str) -> tuple[XY, XY, set[XY]]:
    rows = maze_map.splitlines()
    
    start_pos = None
    exit_pos = None
    
    accessible = []
    
    for y,row in enumerate(rows[1:-1]):
        for x,c in enumerate(row[1:-1]):
            match c:
                case MapSymbol.PATH:
                    accessible.append(XY(x, y))
                case MapSymbol.START:
                    start_pos = XY(x, y)
                case MapSymbol.EXIT:
                    accessible.append(XY(x, y))
                    exit_pos = XY(x, y)

    return start_pos, exit_pos, set(accessible)


def resolve_state_distances(start_pos:XY, exit_pos:XY, accessible_pos:set[XY]) -> dict[State, int]:
    start_state = State(start_pos, Direction.EAST)
    
    state_distances = {start_state: 0}
    
    to_visit = [(start_state, 0)]
    
    exit_distance = 1<<32
    
    while to_visit:
        current_state, current_distance = to_visit.pop()
        
        if current_distance >= exit_distance:
            continue
        
        for new_state, move_cost in current_state.get_move_options():
            if new_state.pos not in accessible_pos:
                continue
            
            new_distance = current_distance + move_cost
            
            if state_distances.get(new_state, 1<<32) > new_distance:
                state_distances[new_state] = new_distance
                to_visit.append((new_state, new_distance))
                
                if new_state.pos == exit_pos:
                    exit_distance = new_distance
                
        to_visit.sort(key=lambda p: p[1], reverse=True)

    return state_distances


def solve(_input:str) -> int:
    start_pos, exit_pos, accessible_pos = parse_map(_input)
    
    state_distances = resolve_state_distances(start_pos, exit_pos, accessible_pos)
    
    return min(d for s,d in state_distances.items() if s.pos == exit_pos)