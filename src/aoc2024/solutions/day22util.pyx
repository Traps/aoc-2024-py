import cython

from typing import Generator


cdef unsigned long evolve_once(unsigned long secret):
    secret = (secret ^ (secret << 6)) & 16777215
    secret = (secret ^ (secret >> 5)) # & 16777215
    return (secret ^ (secret << 11)) & 16777215


def evolve(secret:cython.int, rounds:cython.int=0) -> int:
    cdef unsigned long c_secret = secret

    for _ in range(rounds):
        c_secret = evolve_once(c_secret)

    return c_secret


def unfold_evolution(secret:cython.int, rounds:cython.int=0) -> Generator[int, None, None]:
    cdef unsigned long c_secret = secret

    yield c_secret
    for _ in range(rounds):
        yield (c_secret := evolve_once(c_secret))