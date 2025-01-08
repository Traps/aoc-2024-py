import dataclasses
import typing

from .day15a import Direction, MapSymbol, XY


class ImmovableObjectShoved(Exception):
    pass


@dataclasses.dataclass(slots=True, init=False)
class Warehouse(object):
    width:int
    height:int

    robot_pos:XY

    walls:frozenset[XY]
    boxes:set[XY]

    def __init__(self, warehouse_map:str) -> None:
        warehouse_map = (warehouse_map.replace('#', '##')
                                      .replace('.', '..')
                                      .replace('O', 'O.')
                                      .replace('@', '@.'))

        rows = warehouse_map.splitlines()

        self.width = len(rows[0]) - 4
        self.height = len(rows) - 2

        walls = list()
        boxes = list()

        for y,row in enumerate(rows[1:-1]):
            for x,c in enumerate(row[2:-2]):
                match c:
                    case MapSymbol.ROBOT:
                        self.robot_pos = XY(x, y)
                    case MapSymbol.BOX:
                        boxes.append(XY(x, y))
                    case MapSymbol.WALL:
                        walls.append(XY(x, y))

        self.walls = frozenset(walls)
        self.boxes = set(boxes)

    def resolve_moved_boxes(self, base_pos:XY, direction:Direction) -> typing.Generator[XY, None, None]:
        if base_pos in self.boxes and direction is not Direction.WEST:
            yield from self.resolve_moved_boxes(base_pos + (1, 0), direction)

        shoved = [base_pos + direction.as_step()]
        
        if direction is not Direction.EAST:
            shoved.append(shoved[0] + Direction.WEST.as_step())

        shoved_main = shoved[0]

        if not (0 <= shoved_main.x < self.width and 0 <= shoved_main.y < self.height):
            raise ImmovableObjectShoved("Can't shove stuff outside of the map.")

        if shoved_main in self.walls:
            raise ImmovableObjectShoved("Can't shove walls.")
            
        for shoved_box in self.boxes.intersection(shoved):
            yield shoved_box
            yield from self.resolve_moved_boxes(shoved_box, direction)


    def move_robot(self, direction:Direction) -> None:
        try:
            moved_boxes = set(self.resolve_moved_boxes(self.robot_pos, direction))
        except ImmovableObjectShoved:
            return
        
        step = direction.as_step()
        
        new_boxes = {box + step for box in moved_boxes}

        self.boxes.difference_update(moved_boxes - new_boxes)
        self.boxes.update(new_boxes)

        self.robot_pos += step


def gps_coords(box:XY) -> int:
    return (box.x + 2) + (box.y + 1) * 100


def solve(_input:str) -> int:
    warehouse_map, moves = _input.split('\n\n')

    warehouse = Warehouse(warehouse_map)
    moves = ''.join(moves.splitlines())

    for move in moves:
        warehouse.move_robot(Direction(move))

    return sum(gps_coords(box) for box in warehouse.boxes)

