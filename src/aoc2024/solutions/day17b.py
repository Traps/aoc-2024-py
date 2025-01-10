from typing import Callable, Generator, Iterable

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
            return ('RECURSE', f'a')
        case 4: # bxc
            return ('b', 'b ^ c')
        case 5: # out
            return ('OUTPUT', f'{combo_val(operand)} & {0b111}')
        case 6: # bdv
            return ('b', f'a >> {combo_val(operand)}')
        case 7: # cdv
            return ('c', f'a >> {combo_val(operand)}')


def reduce_program(instructions:list[tuple[str, str]]
                   ) -> tuple[Callable[[int], int], Callable[[int], int]]:
    var_exprs = {'a': 'a'}

    for instruction in instructions:
        (var, expr) = instruction

        for v,e in var_exprs.items():
            expr = expr.replace(v, f'({e})' if len(e) > 1 else e)

        var_exprs[var] = expr
    
    output_expr = var_exprs['OUTPUT']
    recurse_expr = var_exprs['RECURSE'].replace('>>', '<<')

    f_output = eval(f'lambda a: {output_expr}')
    f_recurse = eval(f'lambda a: {recurse_expr}')

    return f_output, f_recurse


def find_self_replicating_values(program:Iterable[int]
                                 ) -> Generator[int, None, None]:
    program = tuple(program)
    
    assert sum(op == 3 for op in program[::2]) == 1
    assert program[-2:] == (3, 0)

    exprs = []
    for opcode,operand in zip(program[0::2], program[1::2]):
        exprs.append(stringify_instruction(opcode, operand))

    f_output, f_recurse = reduce_program(exprs)

    def reversed_program(outputs:tuple[int, ...],
                         _a:int=0) -> Generator[int, None, None]:
        *outputs, next_output = outputs

        for a in range(_a, _a + 8):
            if f_output(a) != next_output:
                continue
                
            if outputs:
                yield from reversed_program(outputs, f_recurse(a))
            else:
                yield a

    yield from reversed_program(program)


def solve(_intput:str) -> str:
    _, program = parse_setup(_intput)

    return min(find_self_replicating_values(program))