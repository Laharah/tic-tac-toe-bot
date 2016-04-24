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

class Board:
    """tracks the game state of tic-tac-toe, has convienience functions"""
    def __init__(self, state=None):
        if state is None:
            state = tuple(('.') * 3 for _ in range(3))
        self.state = state
        xs = sum(row.count('X') for row in state)
        self.turn = xs % 2

    def __getitem__(self, index):
        if isinstance(index, tuple):
            a, b = index
            return self.state[a][b]
        else:
            return self.state[index]
