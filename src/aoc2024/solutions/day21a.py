import functools
import itertools

from typing import Generator, NamedTuple


class KeyPos(NamedTuple):
    row:int
    col:int

    def __add__(self, other:'KeyPos') -> 'KeyPos':
        return KeyPos(self.row + other[0], self.col + other[1])
    
    def __sub__(self, other:'KeyPos') -> 'KeyPos':
        return KeyPos(self.row - other[0], self.col - other[1])
    
    @property
    def moves(self) -> str:
        lat_moves = ('v' if self.row > 0 else '^') * abs(self.row) 
        hor_moves = ('>' if self.col > 0 else '<') * abs(self.col)

        return lat_moves + hor_moves
    
    @staticmethod
    def from_key(key:str) -> 'KeyPos':
        if key == '^':
            key = '0'

        i_key = '789456123 0A<v>'.index(key) - 12

        return KeyPos(*divmod(i_key, 3))
        

def path_is_safe(pos:KeyPos, steps:str) -> bool:
    for c in steps:
        match c:
            case '<':
                pos += (0, -1)
            case '>':
                pos += (0, 1)
            case '^':
                pos += (-1, 0)
            case 'v':
                pos += (1, 0)

        if pos == KeyPos.from_key(' '):
            return False
        
    return True


def key2key_paths(key0:str, key1:str) -> Generator[str, None, None]:
    p0 = KeyPos.from_key(key0)

    diff = KeyPos.from_key(key1) - p0

    paths = [diff.moves, diff.moves[::-1]]

    return (path + 'A' for path in paths if path_is_safe(p0, path))


def shortest(s0:str, s1:str) -> str:
    return s0 if len(s0) < len(s1) else s1


@functools.cache
def resolve_input_sequence(sequence:str, keypad_layers:int) -> str:
    if keypad_layers == 0:
        return sequence
    
    key_moves = itertools.pairwise('A' + sequence)
 
    section_options = itertools.starmap(key2key_paths, key_moves)

    shortest_sections = []
    for options in section_options:
        options = (resolve_input_sequence(p, keypad_layers - 1) for p in options)

        shortest_sections.append(functools.reduce(shortest, options))

    return ''.join(shortest_sections)


def get_code_complexity(code:str, keypad_layers:int) -> int:
    num_val = int(''.join(c for c in code if c.isnumeric()))

    input_sequence = resolve_input_sequence(code, keypad_layers)

    return num_val * len(input_sequence)


def solve(_input:str) -> int:
    codes = _input.splitlines()

    return sum(get_code_complexity(code, 3) for code in codes)

