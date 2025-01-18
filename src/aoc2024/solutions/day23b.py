import itertools
import numpy

from .day23a import create_adjacency_matrix


def solve(_input:str) -> str:
    adjacency, unique_ids = create_adjacency_matrix(_input)

    numpy.fill_diagonal(adjacency, 1)

    a2 = numpy.linalg.matrix_power(adjacency, 2)

    group_size = numpy.max(a2) - 1

    is_member = numpy.sum(a2 == group_size, axis=0) == (group_size - 1)

    member_ids = itertools.compress(unique_ids, is_member)

    return ','.join(sorted(member_ids))
