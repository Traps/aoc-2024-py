from .day22util import evolve

def solve(_input:str) -> int:
    secrets = map(int, _input.splitlines())
    
    return sum(evolve(s, 2000) for s in secrets)