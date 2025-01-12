import importlib
import pytest

from ..inputs import get_sample_inputs, get_challenge_input

DAY_NAME:str = __file__.split('_')[-1].replace('.py','')

# Part 1 #
part1_module = importlib.import_module(f'.solutions.{DAY_NAME}a', 'aoc2024')
    
def test_part1_samples() -> None:
    samples = get_sample_inputs(DAY_NAME, 'a')

    path = part1_module.resolve_track(*part1_module.parse_map(samples[0]))

    shortcuts = part1_module.locate_shortcuts(tuple(path), 2, 2)

    assert sum(dist ==  2 for dist in shortcuts.values()) == 14
    assert sum(dist ==  4 for dist in shortcuts.values()) == 14
    assert sum(dist ==  6 for dist in shortcuts.values()) == 2
    assert sum(dist ==  8 for dist in shortcuts.values()) == 4
    assert sum(dist == 10 for dist in shortcuts.values()) == 2
    assert sum(dist == 12 for dist in shortcuts.values()) == 3
    assert sum(dist == 20 for dist in shortcuts.values()) == 1
    assert sum(dist == 36 for dist in shortcuts.values()) == 1
    assert sum(dist == 38 for dist in shortcuts.values()) == 1
    assert sum(dist == 40 for dist in shortcuts.values()) == 1
    assert sum(dist == 64 for dist in shortcuts.values()) == 1

    assert part1_module.solve(samples[0]) == 0

def test_part1_challenge() -> None:
    challenge = get_challenge_input(DAY_NAME)

    assert part1_module.solve(challenge) == 1530


# Part 2 #
part2_module = importlib.import_module(f'.solutions.{DAY_NAME}b', 'aoc2024')

def test_part2_samples() -> None:
    samples = get_sample_inputs(DAY_NAME, 'b')

    path = part2_module.resolve_track(*part2_module.parse_map(samples[0]))

    shortcuts = part2_module.locate_shortcuts(tuple(path), 50, 20)

    assert sum(dist == 50 for dist in shortcuts.values()) == 32
    assert sum(dist == 52 for dist in shortcuts.values()) == 31
    assert sum(dist == 54 for dist in shortcuts.values()) == 29
    assert sum(dist == 56 for dist in shortcuts.values()) == 39
    assert sum(dist == 58 for dist in shortcuts.values()) == 25
    assert sum(dist == 60 for dist in shortcuts.values()) == 23
    assert sum(dist == 62 for dist in shortcuts.values()) == 20
    assert sum(dist == 64 for dist in shortcuts.values()) == 19
    assert sum(dist == 66 for dist in shortcuts.values()) == 12
    assert sum(dist == 68 for dist in shortcuts.values()) == 14
    assert sum(dist == 70 for dist in shortcuts.values()) == 12
    assert sum(dist == 72 for dist in shortcuts.values()) == 22
    assert sum(dist == 74 for dist in shortcuts.values()) == 4
    assert sum(dist == 76 for dist in shortcuts.values()) == 3

    assert part2_module.solve(samples[0]) == 0

def test_part2_challenge() -> None:
    challenge = get_challenge_input(DAY_NAME)

    assert part2_module.solve(challenge) == 1033983