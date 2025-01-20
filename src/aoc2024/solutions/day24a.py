import functools
import operator

from typing import Callable


GATE_OPS:dict[str, Callable[[bool, bool], bool]] = {
    'AND': operator.and_,
    'OR': operator.or_,
    'XOR': operator.xor
}


def parse_system(system:str) -> tuple[Callable[[str], int], set[str]]:
    wires, gates = system.replace(' ->', '').split('\n\n')

    wires = (line.split(': ') for line in wires.splitlines())

    wires = {gate:int(value) for gate,value in wires}

    gates = (gate.split(' ') for gate in gates.splitlines())
    
    gate_functions = {}
    for in0, op, in1, out in gates:
        gate_functions[out] = (GATE_OPS[op], in0, in1)

    @functools.cache
    def get_gate(gate:str) -> int:
        if gate in wires:
            return wires[gate]
        
        op, in0, in1 = gate_functions[gate]

        return op(get_gate(in0), get_gate(in1))
    
    return get_gate, set(gate_functions.keys()) | set(wires.keys())


def solve(_input:str) -> int:
    gate_function, outputs = parse_system(_input)

    z_outputs = sorted(g for g in outputs if g.startswith('z'))

    z_bits = [gate_function(g) for g in z_outputs]

    return sum(b<<i for i,b in enumerate(z_bits))