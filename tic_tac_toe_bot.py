# usr/bin/python

import re
import random
import warnings


class Board:
    """tracks the game state of tic-tac-toe, has convienience functions"""
    _EMPTY = '.'

    def __init__(self, state=None):
        if state is None:
            state = tuple((self._EMPTY, ) * 3 for _ in range(3))
        self.state = state
        xs = sum(row.count('X') for row in state)
        os = sum(row.count('O') for row in state)
        self.turn = 'X' if xs == os else 'O'

    @property
    def empty_squares(self):
        """attrubute that generates the cordinates of empty squares in the board"""
        return ((i, j)
                for i, row in enumerate(self) for j, value in enumerate(row)
                if value == self._EMPTY)

    def board_from_move(self, cord):
        """creates and returns a new board with the given square taken"""
        if self[cord] != self._EMPTY:
            raise IndexError("Square {} already Taken!".format(cord))
        mark = self.turn
        new_state = self._state_replace(cord, mark)
        return self.__class__(tuple(new_state))

    def _state_replace(self, cord, value):
        """returns new state with value at cord"""
        new_state = []
        r, c = cord
        for i, row in enumerate(self):
            if i == r:
                row = row[:c] + (value, ) + row[c + 1:]
            new_state.append(row)
        return tuple(new_state)

    def score(self):
        """return O, X, stalemate or None"""
        #  checks if a row is a run
        run = lambda row: row[0] != self._EMPTY and all(x == row[0] for x in row)
        #  extracts the left to right diagonal row from a state
        diagonal = lambda state: tuple(state[i][i] for i in range(len(state[0])))

        rotate = lambda state: tuple(map(tuple, zip(*reversed(state))))

        for state in (self.state, rotate(self.state)):
            for row in state + (diagonal(state), ):  # add diagonal as a 4th row
                if run(row):
                    return row[0]
        if not list(self.empty_squares):
            return 'stalemate'
        else:
            return None

    def __getitem__(self, index):
        """allows normal double indexing and numpy style tuple indexing"""
        if isinstance(index, tuple):
            a, b = index
            return self.state[a][b]
        else:
            return self.state[index]

    def __setitem__(self, index, value):
        """
        ONLY WORKS FOR TUPLE STYLE CORDINATES. FOR QUICK EDITS ONLY, PREFER
        'Board.board_from_move' TO MAINTAIN IMMUTABILITY
        """
        try:
            current_val = self[index]
        except IndexError:
            raise IndexError("index out of bounds")
        if value == current_val:
            return
        self.state = self._state_replace(index, value)

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return self.state == other.state

    def __iter__(self):
        """iterates by row"""
        return iter(self.state)

    def __str__(self):
        head = "  0   1   2\n"
        sep = '\n  ---------\n'
        r = '{} {} | {} | {}'
        rows = []
        for i, row in enumerate(self):
            row = (v if v != self._EMPTY else ' ' for v in row)
            rows.append(r.format(i, *row))
        rows = sep.join(rows)
        return ''.join((head, rows))

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.state)


class Bot:
    """min/max tic-tac-toe playing robot"""
    cache = {}

    def __init__(self):
        pass

    def util(self, board):
        if board in self.cache:
            return self.cache[board]
        score = board.score()
        if score is None:
            if board.turn == 'X':
                u = max(self.quality(move, board) for move in board.empty_squares)
            else:
                u = min(self.quality(move, board) for move in board.empty_squares)
            self.cache[board] = u
            return u
        elif score == 'stalemate':
            self.cache[board] = 0
            return 0
        elif score == 'X':
            self.cache[board] = 1
            return 1
        else:
            self.cache[board] = -1
            return -1

    def quality(self, action, board):
        return self.util(board.board_from_move(action))

    def __call__(self, board):
        op = max if board.turn == 'X' else min
        q = lambda action: self.quality(action, board)
        best_case = op(q(s) for s in board.empty_squares)
        moves = [cord for cord in board.empty_squares if q(cord) == best_case]
        return random.choice(moves)


def human_player(board):
    print(board)
    move = input("\nYou are {}s, what is your move?: ".format(board.turn))
    return tuple(int(x) for x in re.findall(r'\d', move))


def random_player(board):
    moves = list(board.empty_squares)
    return random.choice(moves)


def play(p1, p2, initial=None, verbose=False):
    """plays a game of tic-tac-toe using 2 strategy functions"""
    other = {p1: p2, p2: p1}
    board = Board() if not initial else initial
    current_player = p1
    while board.score() is None:
        try:
            board = board.board_from_move(current_player(board))
            current_player = other[current_player]
        except IndexError:
            warnings.warn('ILLEGAL MOVE, AUTOMATIC LOSS!')
            return 'X' if board.turn == 'O' else 'O'
        if verbose:
            print(board)
    return board.score()

if __name__ == '__main__':
    winner_table = ['X', 'O', 'stalemate']
    players = [Bot(), human_player]
    while True:
        random.shuffle(players)
        winner = play(*players)
        if winner_table.index(winner) == 2:
            print("\nStalemate, no winner!\n")
        elif players[winner_table.index(winner)] is human_player:
            print("\nYou Win! This should be impossible!\n")
        else:
            print("\nYou lose, better luck next time!\n")
