from dataclasses import dataclass, field

from typing import Callable, Iterable


@dataclass(slots=True)
class ChronospatialComputer(object):
    a:int
    b:int
    c:int
    
    _instruction_set:tuple[Callable[[int], None]] = field(init=False)
    
    i_ptr:int = field(init=False, default=0)

    output:list[int] = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        self._instruction_set = (
            self.inst0_adv, self.inst1_bxl, self.inst2_bst,
            self.inst3_jnz, self.inst4_bxc, self.inst5_out,
            self.inst6_bdv, self.inst7_cdv
        )
    
    def combo_val(self, op:int) -> int:
        match op:
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
        
        return op
    
    def inst0_adv(self, operand:int) -> None:
        self.a //= (1 << self.combo_val(operand))
    
    def inst1_bxl(self, operand:int) -> None:
        self.b ^= operand
        
    def inst2_bst(self, operand:int) -> None:
        self.b = self.combo_val(operand) & 0b111
    
    def inst3_jnz(self, operand:int) -> None:
        if self.a != 0:
            self.i_ptr = operand - 2
        
    def inst4_bxc(self, operand:int) -> None:
        self.b ^= self.c

    def inst5_out(self, operand:int) -> None:
        self.output.append(self.combo_val(operand) & 0b111)
    
    def inst6_bdv(self, operand:int) -> None:
        self.b = self.a // (1 << self.combo_val(operand))
    
    def inst7_cdv(self, operand:int) -> None:
        self.c = self.a // (1 << self.combo_val(operand))
        
    def run_instruction(self, opcode:int, operand:int) -> None:
        self._instruction_set[opcode](operand)
        self.i_ptr += 2
            
    def run_program(self, program:Iterable[int]) -> list[int]:
        program = tuple(program)
        
        program_length = len(program)
        
        while 0 <= self.i_ptr < program_length:
            self.run_instruction(program[self.i_ptr], program[self.i_ptr+1])
            
        return self.output
        

def parse_setup(setup:str) -> tuple[tuple[int, ...], tuple[int, ...]]:
    line_values = (line.split(' ')[-1] for line in setup.splitlines())
    
    *registers, program = filter(None, line_values)
    
    return tuple(map(int, registers)), tuple(map(int, program.split(',')))


def solve(_intput:str) -> str:
    registers, program = parse_setup(_intput)
    
    computer = ChronospatialComputer(*registers)
    
    output = computer.run_program(program)
    
    return ','.join(map(str, output))