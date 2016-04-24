import pytest
import tic_tac_toe_bot as bot


def test_board():
    board = bot.Board()
    assert board.state == tuple(('.') * 3 for _ in range(3))
    new_state = (
        ('X', 'O', 'X'),
        ('X', '.', 'O'),
        ('X', 'O', '.'),
    )
    board = bot.Board(new_state)
    assert board.state == new_state


def test_board_get_item():
    new_state = (
        ('X', 'O', 'X'),
        ('X', '.', 'O'),
        ('X', 'O', '.'),
    )
    board = bot.Board(new_state)
    assert board[1][2] == 'O'
    assert board[1, 2] == 'O'
    assert board[1, 0] == 'X'
    assert board[0] == ('X', 'O', 'X')
    with pytest.raises(IndexError):
        board[0, 4]


if __name__ == '__main__':
    pytest.main('-v')
