from ..util.parsing import to_columns


def solve(_input:str) -> int:
    columns = to_columns(_input, int)

    return sum(a*columns[1].count(a) for a in columns[0])