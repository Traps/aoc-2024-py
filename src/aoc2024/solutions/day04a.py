import dataclasses

from typing import Final


@dataclasses.dataclass(slots=True, frozen=True)
class XY(object):
    x:int
    y:int

    def __add__(self, other:'XY') -> 'XY':
        return XY(self.x + other.x, self.y + other.y)


DIRECTIONS:Final[tuple[XY]] = tuple(
        XY(x,y) for x in range(-1,2) for y in range(-1,2) if x!=0 or y!=0
    )


def index_board(letter_board:str, word:str) -> tuple[set[XY], ...]:
    board_lines = letter_board.splitlines()
    board_width = len(board_lines[0])

    letter_board = ''.join(board_lines)

    board_index = []
    for letter in word:
        letter_index = (i for i,c in enumerate(letter_board) if c==letter)

        board_index.append(set(XY(*divmod(i, board_width)) for i in letter_index))

    return tuple(board_index)


def count_word(pos:XY, board_index:tuple[set[XY], ...], direction:XY=None) -> int:
    if direction is None:
        if pos not in board_index[0]:
            return 0

        return sum(count_word(pos + d, board_index[1:], d) for d in DIRECTIONS)
    
    for letter_index in board_index:
        if pos not in letter_index:
            return 0

        pos += direction

    return 1


def solve(_input:str) -> int:
    board_index = index_board(_input, word='XMAS')

    return sum(count_word(pos, board_index) for pos in board_index[0]) 