import re
import sympy

from types import NoneType
from typing import Generator, NamedTuple


BUTTON_PRICES:sympy.Matrix = sympy.Matrix([3, 1]).T


class Machine(NamedTuple):
    dx_da:int; dy_da:int
    dx_db:int; dy_db:int
    prize_x:int; prize_y:int


def parse_machines(machine_rules:str, prize_offset:int=0) -> Generator[Machine, None, None]:
    offsets = (0,) * 4 + (prize_offset,) * 2

    for machine in re.split(r'\n\n', machine_rules):
        values = map(int, re.findall(r'(?<=[\=\+])\d+', machine))

        yield Machine(*map(sum, zip(values, offsets)))


def get_prize_cost(machine:Machine) -> int|NoneType:
    button_moves = sympy.Matrix((
        [machine.dx_da, machine.dx_db],
        [machine.dy_da, machine.dy_db]
    ))

    prize_pos = sympy.Matrix([machine.prize_x, machine.prize_y])

    button_presses = button_moves.solve(prize_pos)

    if not all(n.is_integer for n in button_presses):
        return None

    return int((BUTTON_PRICES * button_presses)[0])


def solve(_input:str) -> int:
    machines = parse_machines(_input)
    
    prize_costs = filter(None, map(get_prize_cost, machines))

    return sum(prize_costs)