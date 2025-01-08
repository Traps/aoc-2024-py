import itertools
from .day17a import parse_setup, ChronospatialComputer

def solve(_intput:str) -> str:
    registers, program = parse_setup(_intput)
    
    for a in itertools.count():
        computer = ChronospatialComputer(a, *registers[1:])
    
        output = tuple(computer.run_program(program))
        
        if a == 100_000:
            return