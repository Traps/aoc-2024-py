from typing import Iterable, TypeAlias
from collections import defaultdict

from ..util.parsing import to_rows

RuleSet:TypeAlias = dict[int, set[int]]
Update:TypeAlias = tuple[int, ...]


def parse_pages(_input:str) -> tuple[RuleSet, tuple[Update, ...]]:
    rules_section, updates = _input.split('\n\n')

    rules = defaultdict(set)
    for earlier_page, later_page in to_rows(rules_section, int, '|'):
        rules[earlier_page].add(later_page)
    
    return dict(rules), to_rows(updates, int, ',')


def update_is_valid(update_pages:Iterable[int], rules:RuleSet) -> bool:
    seen_pages = []
    
    for next_page in update_pages:
        later_pages = rules.get(next_page, set())
        
        if any(page in later_pages for page in seen_pages):
            return False
        
        seen_pages.append(next_page)
            
    return True


def solve(_input:str) -> int:
    rules, updates = parse_pages(_input)
    
    valid_updates = (
        upd for upd in updates if update_is_valid(upd, rules)
    )
    
    return sum(upd[len(upd)//2] for upd in valid_updates)
    
    
    