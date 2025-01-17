from .day22util import evolve

EVOLUTION_ROUNDS:int = 2000

def solve(_input:str) -> int:
    secrets = map(int, _input.splitlines())
    
    return sum(evolve(secret, EVOLUTION_ROUNDS) for secret in secrets)