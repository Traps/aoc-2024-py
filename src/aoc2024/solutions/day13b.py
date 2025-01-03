from .day13a import parse_machines, get_prize_cost


PRIZE_OFFSET:int = 10_000_000_000_000


def solve(_input:str) -> int:
    machines = parse_machines(_input, prize_offset=PRIZE_OFFSET)

    prize_costs = filter(None, map(get_prize_cost, machines))

    return sum(prize_costs)