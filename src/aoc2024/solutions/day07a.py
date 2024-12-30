import operator

from typing import Callable, TypeAlias

Operator:TypeAlias = Callable[[int, int], int]

OPERATORS:tuple[Operator, ...] = (operator.add, operator.mul)


def parse_equations(_input:str) -> list[tuple[int, ...]]:
    lines = (line.replace(':', '').strip() for line in _input.splitlines())

    return [tuple(map(int, line.split(' '))) for line in lines if line]


def has_solution(operators:tuple[Operator, ...], target:int, head:int,
                 *values:tuple[int, ...]) -> bool:
    for op in operators:
        new_head = op(head, values[0])

        if new_head == target and len(values) == 1:
            return True
        elif new_head <= target and len(values) > 1:
            if has_solution(operators, target, new_head, *values[1:]):
                return True
            
    return False


def solve(_input:str) -> int:
    calibration_eqs = parse_equations(_input)

    valid_eqs = (eq for eq in calibration_eqs if has_solution(OPERATORS, *eq))

    return sum(target for target,*_ in valid_eqs)