import collections

from typing import Iterable

from .day22a import EVOLUTION_ROUNDS
from .day22util import catalog_sequence_prices


def sum_sequence_prices(monkey_sequences:Iterable[dict[int, int]]) -> dict[int, int]:
    sequence_sums = collections.defaultdict(lambda: 0)

    for sequence_prices in monkey_sequences:
        for sequence, price in sequence_prices.items():
            if price == 0:
                continue

            sequence_sums[sequence] += price

    return sequence_sums


def solve(_input:str) -> int:
    secrets = map(int, _input.splitlines())

    sequence_prices = [
        catalog_sequence_prices(secret, EVOLUTION_ROUNDS) for secret in secrets
    ]

    sequence_sums = sum_sequence_prices(sequence_prices)

    return max(sequence_sums.values())