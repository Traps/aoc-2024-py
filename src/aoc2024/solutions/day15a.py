import dataclasses
import enum
import typing


class MapSymbol(enum.StrEnum):
    ROBOT:str = '@'
    BOX:str = 'O'
    WALL:str = '#'


class XY(typing.NamedTuple):
    x:int
    y:int

    def __add__(self, other:tuple) -> 'XY':
        return XY(self.x + other[0], self.y + other[1])


class Direction(enum.StrEnum):
    NORTH:str = '^'
    EAST:str = '>'
    SOUTH:str = 'v'
    WEST:str = '<'

    def as_step(self:'Direction') -> XY:
        match self:
            case Direction.NORTH:
                return XY(0, -1)
            case Direction.EAST:
                return XY(1, 0)
            case Direction.SOUTH:
                return XY(0, 1)
            case Direction.WEST:
                return XY(-1, 0)
            

@dataclasses.dataclass(slots=True, init=False)
class Warehouse(object):
    width:int
    height:int

    robot_pos:XY

    walls:frozenset[XY]
    boxes:set[XY]

    def __init__(self, warehouse_map:str) -> None:
        rows = warehouse_map.splitlines()

        self.width = len(rows[0]) - 2
        self.height = len(rows) - 2

        walls = list()
        boxes = list()

        for y,row in enumerate(rows[1:-1]):
            for x,c in enumerate(row[1:-1]):
                match c:
                    case MapSymbol.ROBOT:
                        self.robot_pos = XY(x, y)
                    case MapSymbol.BOX:
                        boxes.append(XY(x, y))
                    case MapSymbol.WALL:
                        walls.append(XY(x, y))

        self.walls = frozenset(walls)
        self.boxes = set(boxes)

    def move_robot(self, direction:Direction) -> None:
        step = direction.as_step()

        shove_pos = self.robot_pos + step
        
        new_pos = shove_pos
        box_moved = False

        while new_pos in self.boxes:
            box_moved = True
            new_pos += step

        if not (0 <= new_pos.x < self.width and 0 <= new_pos.y < self.height):
            return None

        if new_pos in self.walls:
            return None
        
        if box_moved:
            self.boxes.remove(shove_pos)
            self.boxes.add(new_pos)
        
        self.robot_pos = shove_pos


def gps_coords(box:XY) -> int:
    return (box.x + 1) + (box.y + 1) * 100


def solve(_input:str) -> int:
    warehouse_map, moves = _input.split('\n\n')
    
    warehouse = Warehouse(warehouse_map)
    moves = ''.join(moves.splitlines())

    for move in moves:
        warehouse.move_robot(Direction(move))

    return sum(gps_coords(box) for box in warehouse.boxes)

