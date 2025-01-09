from types import FunctionType
from typing import Generator, Iterable

from .day17a import parse_setup


def stringify_instruction(opcode:int, operand:int) -> tuple[str, str]:
    combo_val = lambda _op: '0123abc'[_op]

    match opcode:
        case 0: # adv
            return ('a', f'a >> {combo_val(operand)}')
        case 1: # bxl
            return ('b', f'b ^ {operand}')
        case 2: # bst
            return ('b', f'{combo_val(operand)} & {0b111}')
        case 3: # jnz
            assert operand == 0
            return ('RECURSE', f'{{FUNCTION_NAME}}(outputs, a)')
        case 4: # bxc
            return ('b', 'b ^ c')
        case 5: # out
            return ('OUTPUT', f'{combo_val(operand)} & {0b111}')
        case 6: # bdv
            return ('b', f'a >> {combo_val(operand)}')
        case 7: # cdv
            return ('c', f'a >> {combo_val(operand)}')


def reduce_program(instructions:list[tuple[str, str]]) -> str:
    var_exprs = {'a': 'a'}

    for instruction in instructions:
        (var, expr) = instruction

        for v,e in var_exprs.items():
            expr = expr.replace(v, f'({e})' if len(e) > 1 else e)

        var_exprs[var] = expr
    
    output_expr = var_exprs['OUTPUT']
    recursive_call = var_exprs['RECURSE'].replace('>>', '<<')

    return (
        f'def {{FUNCTION_NAME}}(outputs, _a):\n'
        f'    *outputs, next_output = outputs\n'

        f'    for a in range(_a, _a + 8):\n'
        f'        if {output_expr} != next_output:\n'
        f'            continue\n'
        
        f'        if outputs:\n'
        f'            yield from {recursive_call}\n'
        f'        else:\n'
        f'            yield a\n'
    )


def find_self_replicating_values(program:Iterable[int]) -> Generator[int, None, None]:
    GLOBAL_FUNCTION_ALIAS:str = 'reversed_chronospatial_program'

    program = tuple(program)
    
    assert sum(op == 3 for op in program[::2]) == 1
    assert program[-2:] == (3, 0)

    exprs = []
    for opcode,operand in zip(program[0::2], program[1::2]):
        exprs.append(stringify_instruction(opcode, operand))

    rev_def = reduce_program(exprs).format(FUNCTION_NAME=GLOBAL_FUNCTION_ALIAS)

    rev_code = compile(rev_def, "<string>", "exec")

    _globals = globals()

    rev_prog = FunctionType(rev_code.co_consts[0], _globals, GLOBAL_FUNCTION_ALIAS)
    
    _globals[GLOBAL_FUNCTION_ALIAS] = rev_prog
    
    yield from rev_prog(program, 0)

    _globals.pop(GLOBAL_FUNCTION_ALIAS)
    
        



# def reverse_program(outputs:list[int], a:int=0) -> Generator[int, None, None]:
#     if len(outputs) == 0:
#         yield a
#         return
    
#     next_out = outputs[-1]

#     for b in range(8):
#         _a = (a << 3) | b

#         if b ^ 0b110 ^ (_a >> (b ^ 0b011)) & 0b111 == next_out:
#             yield from reverse_program(outputs[:-1], _a)



def solve(_intput:str) -> str:
    registers, program = parse_setup(_intput)

    

    return min(find_self_replicating_values(program))
    

    # return list(rev_prog(*registers)) #min(reverse_program(program))












