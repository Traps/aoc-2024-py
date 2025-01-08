import importlib
import pytest

from ..inputs import get_sample_inputs, get_challenge_input

DAY_NAME:str = __file__.split('_')[-1].replace('.py','')

# Part 1 #
part1_module = importlib.import_module(f'.solutions.{DAY_NAME}a', 'aoc2024')

def test_part1_sample_setups() -> None:
    c1 = part1_module.ChronospatialComputer(0, 0, 9)
    c1.run_program([2, 6])
    assert c1.b == 1

    c2 = part1_module.ChronospatialComputer(10, 0, 0)
    c2.run_program([5, 0, 5, 1, 5, 4])
    assert c2.output == [0, 1, 2]

    c3 = part1_module.ChronospatialComputer(2024, 0, 0)
    c3.run_program([0, 1, 5, 4, 3, 0]) 
    assert c3.output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert c3.a == 0

    c4 = part1_module.ChronospatialComputer(0, 29, 0)
    c4.run_program([1, 7])
    assert c4.b == 26
    
    c5 = part1_module.ChronospatialComputer(0, 2024, 43690)
    c5.run_program([4, 0])
    assert c5.b == 44354
    
def test_part1_samples() -> None:
    samples = get_sample_inputs(DAY_NAME, 'a')

    assert part1_module.solve(samples[0]) == '4,6,3,5,6,3,5,2,1,0'

def test_part1_challenge() -> None:
    challenge = get_challenge_input(DAY_NAME)

    assert part1_module.solve(challenge) == '6,2,7,2,3,1,6,0,5'


# # Part 2 #
# part2_module = importlib.import_module(f'.solutions.{DAY_NAME}b', 'aoc2024')

# def test_part2_samples() -> None:
#     samples = get_sample_inputs(DAY_NAME, 'b')

#     assert part2_module.solve(samples[0]) == 117440

# def test_part2_challenge() -> None:
#     challenge = get_challenge_input(DAY_NAME)

#     assert part2_module.solve(challenge) == 524