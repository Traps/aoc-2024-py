from typing import Final, Generator

from ..solutions.day03a import (get_products,
                                MUL_STATEMENT_HEAD,
                                MUL_STATEMENT_TAIL)

ENABLE_STATEMENT:Final[str] = 'do()'
DISABLE_STATEMENT:Final[str] = 'don\'t()'

def get_enabled_products(memory:str) -> Generator[int, None, None]:
    segments = memory.split(ENABLE_STATEMENT)

    segments = [seg.split(DISABLE_STATEMENT)[0] for seg in segments]

    for segment in segments:
        yield sum(get_products(segment))

def solve(_input:str) -> int:
    return sum(get_enabled_products(_input))