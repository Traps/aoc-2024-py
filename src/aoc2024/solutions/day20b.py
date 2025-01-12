from .day20a import parse_map, resolve_track, locate_shortcuts


SHORTCUT_DIST_MAX:int = 20
SHORTCUT_GAIN_MIN:int = 100


def solve(_input:str) -> int:
    start_pos, exit_pos, track = parse_map(_input)

    path = tuple(resolve_track(start_pos, exit_pos, track))

    return len(locate_shortcuts(path, SHORTCUT_GAIN_MIN, SHORTCUT_DIST_MAX))