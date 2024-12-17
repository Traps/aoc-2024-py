from typing import Callable, Optional, TypeVar

T = TypeVar('T')

def to_columns(_input:str, fparse:Optional[Callable[[str], T]]=None, delim:str=' ') -> tuple[list[T|str], ...]:
    lines = filter(None, (line.strip() for line in _input.splitlines()))

    cols = zip(*(filter(None, line.split(delim)) for line in lines))

    return tuple(list(c if fparse is None else map(fparse, c)) for c in cols)


def to_rows(_input:str, fparse:Optional[Callable[[str], T]]=None, delim:str=' ') -> tuple[list[T|str], ...]:
    lines = filter(None, (line.strip() for line in _input.splitlines()))

    rows = (filter(None, line.split(delim)) for line in lines)

    return tuple(list(row if fparse is None else map(fparse, row)) for row in rows)
