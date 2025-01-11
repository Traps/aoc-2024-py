import functools

from .day19a import parse_towel_patterns


@functools.cache
def count_ways_to_make(towel:str, patterns:tuple[str]) -> bool:
    if towel == '':
        return 1

    count = 0
    for pattern in patterns:
        if not towel.startswith(pattern):
            continue

        count += count_ways_to_make(towel[len(pattern):], patterns)

    return count


def solve(_input:str) -> int:
    patterns, towels = map(tuple, parse_towel_patterns(_input))

    return sum(count_ways_to_make(towel, patterns) for towel in towels)
