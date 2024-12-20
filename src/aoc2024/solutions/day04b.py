from collections import defaultdict

from typing import Final

from .day04a import index_board, XY


STEP_NE:Final[XY] = XY( 1,  1)
STEP_SE:Final[XY] = XY( 1, -1)
STEP_NW:Final[XY] = XY(-1,  1)
STEP_SW:Final[XY] = XY(-1, -1)


def is_x_mas(pos:XY, board:dict[XY, str]) -> bool:
    if board[pos] != 'A':
        return False

    diag1 = set([board[pos + STEP_NE], board[pos + STEP_SW]])
    diag2 = set([board[pos + STEP_NW], board[pos + STEP_SE]])

    return diag1 == {'M', 'S'} and diag1 == diag2


def parse_board(text_board:str) -> dict[XY, str]:
    word = 'MAS'
    
    board = defaultdict(lambda: '.')
    for letter,loci in zip(word, index_board(text_board, word)):
        board.update({xy:letter for xy in loci})

    return board


def solve(_input:str) -> int:
    board = parse_board(_input)

    a_loci = [p for p,c in board.items() if c == 'A']

    return sum(is_x_mas(p, board) for p in a_loci)