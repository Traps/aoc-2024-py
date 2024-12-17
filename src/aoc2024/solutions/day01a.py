from ..util.parsing import to_columns


def solve(_input:str) -> int:
    columns = to_columns(_input, int)

    return sum(abs(a-b) for a,b in zip(*map(sorted, columns)))