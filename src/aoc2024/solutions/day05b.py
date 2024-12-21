from .day05a import (RuleSet,
                     Update,
                     parse_pages,
                     update_is_valid)


def get_loose_pages(rules:RuleSet) -> list[int]:
    locked_pages = set().union(*rules.values())
    
    return [page for page in rules.keys() if page not in locked_pages]


def order_pages(update:Update, rules:RuleSet) -> list[int]:
    update_rules = {p:rules.get(p, set()) for p in update}
    ordered_pages = []
    
    while loose_pages := get_loose_pages(update_rules):
        ordered_pages.extend(loose_pages)
        
        for page in loose_pages:
            update_rules.pop(page)

    return ordered_pages

        
def solve(_input:str) -> int:
    rules, updates = parse_pages(_input)
    
    invalid_updates = (upd for upd in updates if not update_is_valid(upd, rules))
    
    reordered_updates = (order_pages(upd, rules) for upd in invalid_updates)
    
    return sum(upd[len(upd)//2] for upd in reordered_updates)
    


