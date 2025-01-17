import cython


PY_UInt32 = cython.typedef(cython.int)

ctypedef unsigned int C_UInt32


cdef C_UInt32 evolve_once(C_UInt32 secret):
    secret = (secret ^ secret << 6) & 16777215
    secret = (secret ^ secret >> 5)
    return (secret ^ secret << 11) & 16777215


def evolve(secret:PY_UInt32, rounds:PY_UInt32) -> PY_UInt32:
    cdef C_UInt32 c_secret = secret

    for _ in range(rounds):
        c_secret = evolve_once(c_secret)

    return c_secret


def catalog_sequence_prices(secret:PY_UInt32, rounds:PY_UInt32) -> dict[PY_UInt32, PY_UInt32]:
    cdef C_UInt32 c_secret = secret

    cdef C_UInt32 c_price0 = c_secret % 10
    cdef C_UInt32 c_price1

    cdef C_UInt32 c_sequence = c_price0

    sequence_prices:dict = {}

    for i in range(rounds):
        c_price1 = (c_secret := evolve_once(c_secret)) % 10

        c_sequence = (c_sequence << 5) + c_price1 + 9 - c_price0 & 1048575

        c_price0 = c_price1

        if i < 3:
            continue

        if c_sequence not in sequence_prices:
            sequence_prices[c_sequence] = c_price1

    return sequence_prices
    