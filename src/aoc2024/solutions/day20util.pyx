import cython

from cython.cimports.libc.stdlib import malloc, free # type: ignore
from cython.cimports.libc.stdlib import abs as iabs  # type: ignore

P_XY = cython.typedef(tuple[cython.int, cython.int])


cdef struct C_XY:
    long x
    long y


cdef long distance(p0:C_XY, p1:C_XY):
    return iabs(p0.x - p1.x) + iabs(p0.y - p1.y)


cdef long c_count_shortcuts(C_XY *track, long track_len, long min_gain, long cheat_len):
        cdef long dist, i, j
        cdef long shortcut_count = 0

        for i in range(track_len - min_gain):
            for j in range(i + min_gain + 1, track_len):
                dist = distance(track[i], track[j])

                if 2 <= dist <= cheat_len and (j - i - dist) >= min_gain:
                    shortcut_count += 1

        return shortcut_count

    
def count_shortcuts(track_path:list[P_XY], min_gain:cython.long,
                    cheat_length:cython.long) -> cython.long:
    cdef long track_length = len(track_path)
    cdef long shortcut_count

    cdef C_XY *track = <C_XY *>malloc(track_length * cython.sizeof(C_XY))

    for i,(x,y) in enumerate(track_path):
        track[i] = C_XY(<long>x, <long>y)

    try:
        shortcut_count = c_count_shortcuts(track, track_length, min_gain, cheat_length)
    finally:
        free(track)

    return shortcut_count