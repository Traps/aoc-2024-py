
from collections.abc import Sequence

from ..util.parsing import to_rows
from .day02a import report_is_safe


def report_is_safe_enough(report:Sequence[int]) -> bool:
    if report_is_safe(report):
        return True
    
    for i_drop in range(len(report)):
        if report_is_safe((lvl for i,lvl in enumerate(report) if i != i_drop)):
            return True
        
    return False
    

def solve(_input:str) -> int:
    reports = to_rows(_input, int)

    return sum(report_is_safe_enough(report) for report in reports)