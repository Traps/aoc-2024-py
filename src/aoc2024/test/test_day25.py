import importlib
import pytest

from ..inputs import get_sample_inputs, get_challenge_input

DAY_NAME:str = __file__.split('_')[-1].replace('.py','')

# Part 1 #
part1_module = importlib.import_module(f'.solutions.{DAY_NAME}a', 'aoc2024')
    
def test_part1_samples() -> None:
    samples = get_sample_inputs(DAY_NAME, 'a')

    assert part1_module.solve(samples[0]) == 3

def test_part1_challenge() -> None:
    challenge = get_challenge_input(DAY_NAME)

    assert part1_module.solve(challenge) == 3663