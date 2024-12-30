from . import day07a


def iconcat(a:int, b:int) -> int:
    _b = b
    while _b := _b // 10:
        a *= 10

    return a * 10 + b


OPERATORS:tuple[day07a.Operator, ...] = (*day07a.OPERATORS, iconcat)


def solve(_input:str) -> int:
    calibration_eqs = day07a.parse_equations(_input)

    valid_eqs = (eq for eq in calibration_eqs if day07a.has_solution(OPERATORS, *eq))

    return sum(target for target,*_ in valid_eqs)