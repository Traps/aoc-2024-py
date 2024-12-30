import importlib

from ..inputs import get_sample_inputs, get_challenge_input

DAY_NAME:str = __file__.split('_')[-1].replace('.py','')

# Part 1 #
part1_module = importlib.import_module(f'.solutions.{DAY_NAME}a', 'aoc2024')

def test_part1_samples() -> None:
    samples = get_sample_inputs(DAY_NAME, 'a')

    assert part1_module.solve(samples[0]) == 14

def test_part1_challenge() -> None:
    challenge = get_challenge_input(DAY_NAME)

    assert part1_module.solve(challenge) == 344


# Part 2 #
part2_module = importlib.import_module(f'.solutions.{DAY_NAME}b', 'aoc2024')

def test_part2_samples() -> None:
    samples = get_sample_inputs(DAY_NAME, 'b')

    assert part2_module.solve(samples[0]) == 34

def test_part2_challenge() -> None:
    challenge = get_challenge_input(DAY_NAME)

    assert part2_module.solve(challenge) == 1182