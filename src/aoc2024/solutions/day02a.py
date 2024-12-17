
from collections.abc import Sequence
from itertools import pairwise

from ..util.parsing import to_rows


def report_is_safe(report:Sequence[int]) -> bool:
    level_diffs = [b-a for a,b in pairwise(report)]

    if all(diff < 0 for diff in level_diffs) or all(diff > 0 for diff in level_diffs):
        return max(abs(diff) for diff in level_diffs) <= 3
    
    return False


def solve(_input:str) -> int:
    reports = to_rows(_input, int)

    return sum(report_is_safe(report) for report in reports)