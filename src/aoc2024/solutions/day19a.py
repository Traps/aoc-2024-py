from collections.abc import Sequence


def parse_towel_patterns(towel_patterns:str) -> tuple[list[str], list[str]]:
    patterns, towels = towel_patterns.split('\n\n')

    return patterns.split(', '), towels.splitlines()


def can_make(towel:str, patterns:Sequence[str]) -> bool:
    if towel == '':
        return True

    for pattern in patterns:
        if not towel.startswith(pattern):
            continue

        if can_make(towel[len(pattern):], patterns):
            return True
    
    return False


def solve(_input:str) -> int:
    patterns, towels = parse_towel_patterns(_input)

    return sum(can_make(towel, patterns) for towel in towels)