from typing import Generator

from .day16a import (
    Direction,
    XY,
    State,
    parse_map,
    resolve_state_distances
)


def preceeding_states(current_state:State, state_distances:dict[State, int]
                      ) -> Generator[State, None, None]:
    current_distance = state_distances[current_state]
    
    reverse_state = State(current_state.pos, current_state.facing + 2)
    
    for (prior_pos, _), _ in reverse_state.get_move_options():
        for prior_state in (State(prior_pos, direction) for direction in Direction):
            if prior_state not in state_distances:
                continue
            
            expected_cost = current_distance - state_distances[prior_state]
            
            if (current_state, expected_cost) in prior_state.get_move_options():
                yield prior_state


def backtrack_to_start(current_state:State, start_state:State,
                       state_distances:dict[State, int]) -> Generator[XY, None, None]:
    yield current_state.pos
    
    if current_state == start_state:
        return
    
    for state in preceeding_states(current_state, state_distances):
        yield from backtrack_to_start(state, start_state, state_distances)


def solve(_input:str) -> int:
    start_pos, exit_pos, accessible_pos = parse_map(_input)
    
    state_distances = resolve_state_distances(start_pos, exit_pos, accessible_pos)
    
    start_state = next(s for s,d in state_distances.items() if d == 0)
    
    exit_dist = min(d for s,d in state_distances.items() if s.pos == exit_pos)
    
    exit_states = [s for s,d in state_distances.items()
                   if s.pos == exit_pos and d == exit_dist]

    visited = set()
    
    for exit_state in exit_states:
        visited.update(backtrack_to_start(exit_state, start_state, state_distances))
    
    return len(visited)