import functools


@functools.cache
def blink(value:int) -> tuple[int, ...]:
    if value == 0:
        return (1,)
    
    number = str(value)
    
    if (n_digit := len(number)) % 2 == 0:
        return (int(number[:n_digit//2]), int(number[n_digit//2:]))
    
    return (value * 2024,)


@functools.cache
def expanded_length(value:int, count:int) -> int:
    if count == 0:
        return 1
    
    return sum(expanded_length(val, count-1) for val in blink(value))


def solve(_input:str) -> int:
    stones = map(int, _input.split(' '))

    return sum(expanded_length(stone, 25) for stone in stones)