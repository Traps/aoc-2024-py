import importlib
import pytest

from ..inputs import get_sample_inputs, get_challenge_input

DAY_NAME:str = __file__.split('_')[-1].replace('.py','')

# Part 1 #
part1_module = importlib.import_module(f'.solutions.{DAY_NAME}a', 'aoc2024')
    
def test_part1_samples() -> None:
    samples = get_sample_inputs(DAY_NAME, 'a')

    path = part1_module.resolve_track(*part1_module.parse_map(samples[0]))

    assert part1_module.count_shortcuts(list(path), 2, 2) == 44

    assert part1_module.solve(samples[0]) == 0

def test_part1_challenge() -> None:
    challenge = get_challenge_input(DAY_NAME)

    assert part1_module.solve(challenge) == 1530


# Part 2 #
part2_module = importlib.import_module(f'.solutions.{DAY_NAME}b', 'aoc2024')

def test_part2_samples() -> None:
    samples = get_sample_inputs(DAY_NAME, 'b')

    path = part2_module.resolve_track(*part2_module.parse_map(samples[0]))

    assert part2_module.count_shortcuts(list(path), 50, 20) == 285

    assert part2_module.solve(samples[0]) == 0

def test_part2_challenge() -> None:
    challenge = get_challenge_input(DAY_NAME)

    assert part2_module.solve(challenge) == 1033983
