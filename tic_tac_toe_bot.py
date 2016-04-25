# usr/bin/python
"""A perfect tic tac toe player. written in python"""
"""
  0   1   2
0 X | O | X
  ---------
1 O | X | X
  ---------
2 X | O | O
"""
"""
Concepts:
    board (state) - custom class: indexing, printing, turn, filled, HASHABLE and IMMUTABLE
    player - functon, bot with strat, human with input
    who's turn - stored in board? integer
    score - function 0, 1, None
"""
import itertools


class Board:
    """tracks the game state of tic-tac-toe, has convienience functions"""
    _EMPTY = '.'

    def __init__(self, state=None):
        if state is None:
            state = tuple((self._EMPTY, ) * 3 for _ in range(3))
        self.state = state
        xs = sum(row.count('X') for row in state)
        self.turn = xs % 2

    def __getitem__(self, index):
        if isinstance(index, tuple):
            a, b = index
            return self.state[a][b]
        else:
            return self.state[index]

    def __contains__(self, item):
        return item in itertools.chain(*self.state)

    def __iter__(self):
        """iterates by row"""
        return iter(self.state)
