import functools
import itertools

from types import NoneType
from typing import Callable, Generator, NamedTuple, Optional


class Gate(NamedTuple):
    operator:str|NoneType
    operands:frozenset['Gate|str']

    @staticmethod
    def factory(in0:'Gate|str', op:Optional[str]=None,
                in1:Optional['Gate|str']=None) -> 'Gate':
        return Gate(op, frozenset([in0] if in1 is None else [in0, in1]))


def locate_gate_mismatch(gate0:Gate, gate1:Gate) -> Optional[tuple[Gate, Gate]]:
    if gate0.operator != gate1.operator:
        return (gate0, gate1)

    gate1_extra = gate1.operands - gate0.operands

    if len(gate1_extra) == 0:
        return None

    if len(gate1_extra) == 2:
        return (gate0, gate1)
    
    gate0_extra, = gate0.operands - gate1.operands
    gate1_extra, = gate1_extra

    return locate_gate_mismatch(gate0_extra, gate1_extra)


@functools.cache
def zbit_add_overflow(i:int) -> Gate:
    z_and = Gate.factory(f'x{i:02d}', 'AND', f'y{i:02d}')

    if i == 0:
        return z_and
    
    z_xor = Gate.factory(f'x{i:02d}', 'XOR', f'y{i:02d}')

    subz_xor = Gate.factory(z_xor, 'AND', zbit_add_overflow(i-1))

    return Gate.factory(z_and, 'OR', subz_xor)


@functools.cache
def zbit_model_add(i_bit:int, input_bit_count:int) -> Gate:
    z_xor = Gate.factory(f'x{i_bit:02d}', 'XOR', f'y{i_bit:02d}')
    
    if i_bit == 0:
        return z_xor
    
    if i_bit >= input_bit_count:
        return zbit_add_overflow(i_bit-1)
    
    return Gate.factory(z_xor, 'XOR', zbit_add_overflow(i_bit-1))


def zbit_model_and(i_bit:int, _:int) -> Gate:
    return Gate.factory(f'x{i_bit:02d}', 'AND', f'y{i_bit:02d}')


def swap_gate_outputs(name0:str, name1:str, system:str) -> str:
    name0 = f'-> {name0}'
    name1 = f'-> {name1}'
    
    return system.replace(name0, '#').replace(name1, name0).replace('#', name1)


def parse_system(system:str) -> tuple[set[str], dict[str, Gate]]:
    input_wires, system_gates = system.replace(' -> ', ' ').split('\n\n')

    input_wires = {wire.split(':')[0] for wire in input_wires.splitlines()}

    system_gates = (gate.split(' ') for gate in system_gates.splitlines())
    system_gates = {out:(in0,op,in1) for in0,op,in1,out in system_gates}
    
    gates = dict(zip(input_wires, input_wires))

    while system_gates:
        for output in list(system_gates.keys()):
            (in0,op,in1) = system_gates[output]

            if in0 not in gates or in1 not in gates:
                continue

            gates[output] = Gate.factory(gates[in0], op, gates[in1])
            
            system_gates.pop(output)

    gates = {n:g for n,g in gates.items() if isinstance(g, Gate)}

    return input_wires, gates


def find_swapped_gates(system_setup:str, system_model:Callable[[int, int], Gate]
                       ) -> Generator[tuple[str, str], None, None]:
    input_wires, gates_by_name = parse_system(system_setup)
    names_by_gate = {g:n for n,g in gates_by_name.items()}

    input_bit_count = sum(w.startswith('x') for w in input_wires)

    z_gates = sorted(name for name in gates_by_name.keys() if name.startswith('z'))

    gate_mismatch = None
    for gate_name in z_gates:
        gate_number = int(gate_name.lstrip('z'))

        gate_found = gates_by_name[gate_name]
        gate_expected = system_model(gate_number, input_bit_count)

        if gate_found != gate_expected:
            gate_mismatch = locate_gate_mismatch(gate_expected, gate_found)
            break
    
    if gate_mismatch is None:
        return

    swapped_names = tuple(map(names_by_gate.get, gate_mismatch))

    yield swapped_names

    new_system = swap_gate_outputs(*swapped_names, system_setup)

    yield from find_swapped_gates(new_system, system_model)


def solve(_input:str) -> str:
    system_model = zbit_model_add if 'OR' in _input else zbit_model_and

    swapped_gates = find_swapped_gates(_input, system_model)
    
    return ','.join(sorted(itertools.chain(*swapped_gates)))