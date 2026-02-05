"""
Tic Tac Toe Player
"""

import math
import copy
from typing import Literal

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    turns_played = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY: turns_played += 1
    
    if turns_played % 2 == 0:  # Even number
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_actions = set()  # Initialise a possible actions set
    
    # Neseted for loop
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add( (i, j) )

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    i, j = action  # Destructure the tuple
    if board[i][j] != EMPTY: raise Exception('Invalid Action')
    if i not in (0, 1, 2) or j not in (0, 1, 2): raise Exception('Invalid Action')

    newState = copy.deepcopy(board)
    newState[i][j] = player(board)

    return newState


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for row in board:
        if row[0] != EMPTY and row[0] == row[1] == row[2]:
            return row[0]
        
    for col in range(3):
        if board[0][col] != EMPTY and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]
        
    if board[0][0] != EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    
    if board[0][2] != EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None  # No Winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board): return True
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY: return False  # Any empty field means game not over

    return True  # All fields occupied


type Utility = Literal[-1, 0, 1]

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    result = winner(board)

    if result == X: return 1
    if result == O: return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # if winner(board): return None
    maximising = player(board) == X

    best_action = None
    # best_value = -math.inf if maximising else math.inf
    best_value = -1 if maximising else 1

    for action in actions(board):
        result_board = result(board, action)
        action_value = min_value(result_board) if maximising else max_value(result_board)
        
        if maximising and action_value > best_value:
            best_value = action_value
            best_action = action
        elif not maximising and action_value < best_value:
            best_value = action_value
            best_action = action

    return best_action


def max_value(board) -> Utility:
    if terminal(board):
        return utility(board)

    v = -math.inf

    for action in actions(board):
        min_v = min_value(result(board, action))
        v = max(v, min_v)

        if v == 1: return 1  # already best result possible, skip the rest

    assert v in (-1, 0, 1), "v did not satisfy Utility type"  # Theoretically should never happen
    return v


def min_value(board) -> Utility:
    if terminal(board):
        return utility(board)

    v = math.inf

    for action in actions(board):
        min_v = max_value(result(board, action))
        v = min(v, min_v)

        if v == -1: return -1

    assert v in (-1, 0, 1), "v did not satisfy Utility type"
    return v