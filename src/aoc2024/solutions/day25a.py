import itertools

from typing import TypeAlias

Key:TypeAlias = tuple[int, ...]
Lock:TypeAlias = tuple[int, ...]


def parse_schematics(schematics:str) -> tuple[list[Key], list[Lock]]:
    keys, lock = [], []
    
    for schematic in schematics.split('\n\n'):
        columns = zip(*schematic.splitlines())

        heights = tuple(col.count('#') - 1 for col in columns)

        if schematic.startswith('.'):
            keys.append(heights)
        else:
            lock.append(heights)

    return keys, lock


def key_fits_lock(key:Key, lock:Lock) -> bool:
    return all(k <= (5 - l) for k,l in zip(key, lock))


def solve(_input:str) -> int:
    keys, locks = parse_schematics((_input))

    key_lock_pairs = itertools.product(keys, locks)

    return sum(key_fits_lock(*pair) for pair in key_lock_pairs)