import pytest
import tic_tac_toe_bot as bot

example_state = (('X', 'O', 'X'), ('X', '.', 'O'), ('X', 'O', '.'), )
o_win = (('O', 'O', 'O'), ('X', '.', 'X'), ('X', '.', '.'), )
diag_win = (('X', 'O', 'O'), ('O', 'X', '.'), ('.', '.', 'X'), )
l_diag_win = (('.', 'O', 'X'), ('.', 'X', 'O'), ('X', '.', 'O'), )
stalemate = (('X', 'O', 'X'), ('X', 'O', 'X'), ('O', 'X', 'O'), )


def test_board():
    board = bot.Board()
    assert board.state == tuple(('.', ) * 3 for _ in range(3))
    new_state = example_state
    board = bot.Board(new_state)
    assert board.state == new_state


def test_board_get_item():
    new_state = example_state
    board = bot.Board(new_state)
    assert board[1][2] == 'O'
    assert board[1, 2] == 'O'
    assert board[1, 0] == 'X'
    assert board[0] == ('X', 'O', 'X')
    with pytest.raises(IndexError):
        board[0, 4]


def test_board_set_item():
    board = bot.Board()
    board[0, 0] = 'X'
    assert board[0, 0] == 'X'
    board[0, 0] = 'O'
    assert board[0][0] == 'O'
    with pytest.raises(IndexError):
        board[0, 5] = 'X'
    with pytest.raises(TypeError):
        board[1][1] = 'X'


def test_board_iter():
    board = bot.Board(example_state)
    for row_board, row_example in zip(board, example_state):
        assert row_board == row_example


def test_board_empty_squares():
    board = bot.Board(example_state)
    assert list(board.empty_squares) == [(1, 1), (2, 2)]
    assert all(board[cord] == board._EMPTY for cord in board.empty_squares)
    cords = {(a, b) for a in range(3) for b in range(3)}
    non_empty = cords - set(board.empty_squares)
    assert not any(board[cord] == board._EMPTY for cord in non_empty)


def test_board_from_move():
    board = bot.Board()
    new_board = board.board_from_move((2, 1))
    assert new_board[2, 1] == 'X'
    new_board = new_board.board_from_move((1, 1))
    assert new_board[1, 1] == 'O'
    assert new_board.turn == 'X'
    assert board[1, 1] == board._EMPTY
    assert new_board is not board
    with pytest.raises(IndexError):
        n = new_board.board_from_move((1, 1))


def test_board_score():
    assert bot.Board().score() == None
    assert bot.Board(example_state).score() == "X"
    assert bot.Board(o_win).score() == "O"
    assert bot.Board(diag_win).score() == "X"
    assert bot.Board(stalemate).score() == "stalemate"
    assert bot.Board(l_diag_win).score() == 'X'


def test_board_hash():
    board_a = bot.Board(example_state)
    board_b = bot.Board(example_state)
    assert board_a is not board_b
    s = {board_a, board_b}  # must be hashable to be added to a set
    assert hash(board_a) == hash(board_b)


def test_board_eq():
    a = bot.Board(example_state)
    b = bot.Board(example_state)
    c = bot.Board()
    assert a == b != c
    s = {a, b, c}
    assert len(s) == 2
    assert all(x in s for x in (a, b, c))


def test_board_str():
    # regression only
    board = bot.Board(example_state)
    s = ('  0   1   2',
         '0 X | O | X',
         '  ---------',
         '1 X |   | O',
         '  ---------',
         '2 X | O |  ', )
    assert str(board) == '\n'.join(s)


def test_bot_repr():
    # regression only
    board = bot.Board(example_state)
    assert repr(board) == "Board((('X', 'O', 'X'), ('X', '.', 'O'), ('X', 'O', '.')))"


def test_bot():
    robot = bot.Bot()


def test_bot_util():
    robot = bot.Bot()
    assert robot.util(bot.Board(example_state)) == 1
    assert robot.util(bot.Board(o_win)) == -1
    assert robot.util(bot.Board(stalemate)) == 0
    assert robot.util(bot.Board()) == 0  # the only winning move is not to play.
    board = bot.Board().board_from_move((0, 0)).board_from_move((0, 2))
    assert robot.util(board) == 1


def test_bot_quality():
    robot = bot.Bot()
    board = bot.Board().board_from_move((0, 0)).board_from_move((0, 2))
    assert robot.quality((1, 1), board) == 0
    assert robot.quality((0, 1), board) == -1
    assert robot.quality((1, 0), board) == 1


def test_bot_call():
    robot = bot.Bot()
    board = bot.Board()
    assert isinstance(robot(board), tuple)
    board = board.board_from_move(robot(board))
    assert isinstance(robot(board), tuple)


if __name__ == '__main__':
    pytest.main('-v -s')
