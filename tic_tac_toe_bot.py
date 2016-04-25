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

    @property
    def squares(self):
        """returns a generator of the values of all squares"""
        return itertools.chain(*self.state)

    @property
    def empty_squares(self):
        """attrubute that generates the cordinates of empty squares in the board"""
        return ((i, j)
                for i, row in enumerate(self) for j, value in enumerate(row)
                if value == self._EMPTY)

    @property
    def filled_squares(self):
        """attrubute that generates the cordinates of filled squares in the board"""
        return ((i, j)
                for i, row in enumerate(self) for j, value in enumerate(row)
                if value != self._EMPTY)

    def board_from_move(self, cord):
        if self[cord] != self._EMPTY:
            raise ValueError("Square {} already Taken!".format(cord))
        mark = 'X' if self.turn == 0 else 'O'
        new_state = []
        r, c = cord
        for i, row in enumerate(self):
            if i == r:
                row = row[:c] + (mark, ) + row[c + 1:]
            new_state.append(row)
        return self.__class__(tuple(new_state))

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

    def __str__(self):
        head = "  0   1   2\n"
        sep =   '  ---------\n'
        r = '{} {} | {} | {}\n'
        rows = []
        for i, row in enumerate(self):
            row = (v if v != self._EMPTY else ' ' for v in row)
            rows.append(r.format(i, *row))
        rows = sep.join(rows)
        return ''.join((head, rows))

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.state)
