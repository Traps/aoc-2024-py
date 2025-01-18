import itertools
import numpy


def create_adjacency_matrix(network_map:str) -> tuple[numpy.ndarray, list[str]]:
    connections = [line.split('-') for line in network_map.splitlines()]

    unique_ids = sorted(set(itertools.chain(*connections)))
    
    adjacency_matrix = numpy.full((len(unique_ids),) * 2, 0, dtype=int)

    for id0,id1 in connections:
        adjacency_matrix[unique_ids.index(id0), unique_ids.index(id1)] = 1

    return (adjacency_matrix + adjacency_matrix.T), unique_ids


def solve(_input:str) -> int:
    adjacency, unique_ids = create_adjacency_matrix(_input)

    starts_with_t = [id.startswith('t') for id in unique_ids]

    for idx,v in numpy.ndenumerate(adjacency):
        if v != 0 and any(starts_with_t[i] is False for i in idx):
            adjacency[idx] = 2
    
    a3 = numpy.linalg.matrix_power(adjacency, 3)

    t_trace = sum(a3.diagonal()[starts_with_t])

    return t_trace // 16