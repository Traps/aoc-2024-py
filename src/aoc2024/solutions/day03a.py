
from typing import Generator, Final

MUL_STATEMENT_HEAD:Final[str] = 'mul('
MUL_STATEMENT_TAIL:Final[str] = ')'


def parse_term(term:str) -> int:
    if term.isdecimal() and len(term) <= 3:
        return int(term)
    
    return 0


def evaluate_segment(segment:str) -> int:
    if segment.count(',') != 1:
        return 0
    
    term1, term2 = segment.split(',')

    return parse_term(term1) * parse_term(term2)


def get_products(memory:str) -> Generator[int, None, None]:
    _, *segments = memory.split(MUL_STATEMENT_HEAD)

    segments = [seg.split(MUL_STATEMENT_TAIL, 1)[0] for seg in segments]

    for segment in segments:
        yield evaluate_segment(segment)


def solve(_input:str) -> int:
    return sum(get_products(_input))