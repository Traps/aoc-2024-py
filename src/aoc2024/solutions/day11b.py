from .day11a import expanded_length

def solve(_input:str) -> int:
    stones = map(int, _input.split(' '))

    return sum(expanded_length(stone, 75) for stone in stones)