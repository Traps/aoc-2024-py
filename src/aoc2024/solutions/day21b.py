import functools
import itertools

from .day21a import key2key_paths


@functools.cache
def resolve_input_length(sequence:str, keypad_layers:int) -> int:
    if keypad_layers == 0:
        return len(sequence)
    
    key_moves = itertools.pairwise('A' + sequence)
 
    section_options = itertools.starmap(key2key_paths, key_moves)

    length = 0
    for options in section_options:
        length += min(resolve_input_length(p, keypad_layers-1) for p in options)

    return length


def get_code_complexity(code:str, keypad_layers:int) -> int:
    num_val = int(''.join(c for c in code if c.isnumeric()))

    return num_val * resolve_input_length(code, keypad_layers)


def solve(_input:str) -> int:
    codes = _input.splitlines()

    return sum(get_code_complexity(code, 26) for code in codes)
