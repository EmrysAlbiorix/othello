# Team members who contributed to this project:
#

INITIAL_STATE = ('........',) * 3 + ('...XO...', '...OX...') + ('........',) * 3

DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


def flips(board, player, location):
    """
    :param board: A sequence of strings
    :param player: 'X' or 'O'
    :param location: A pair (r, c) with 0 <= r < 8 and 0 <= c < 8
    :return: A collection of pairs of locations of opponent's pieces that would be flipped by this move
    """
    def f(r, c, dr, dc):  # Find flips starting at (r, c) and looking in direction (dr, dc)
        line = []
        while True:
            r, c = (r + dr, c + dc)
            if not (0 <= r < 8 and 0 <= c < 8):
                return []  # Edge of board -- no capture
            if board[r][c] == '.':
                return []  # Empty space -- no capture
            if board[r][c] == player:
                return line  # Friendly piece -- capture all opposing pieces seen so far
            line.append((r, c))
    result = []
    for d in DIRECTIONS:
        result.extend(f(*location, *d))
    return result


def successor(board, player, move):
    """
    :param board: A sequence of strings
    :param player: 'X' or 'O'
    :param move: Either 'pass' or a pair (r, c) with 0 <= r < 8 and 0 <= c < 8
    :return: The board that would result if player played move
    """
    if move == 'pass':
        return board
    mutable_board = [list(row) for row in board]  # Copy to a list of lists
    for r, c in flips(board, player, move):
        mutable_board[r][c] = player
    r, c = move
    mutable_board[r][c] = player
    return tuple(''.join(row) for row in mutable_board)


def legal_moves(board, player):
    """
    :param board: A sequence of strings
    :param player: 'X' or 'O'
    :return: A collection of legal moves for player from board; each is (r, c). Returns an empty collection if neither
    player has a legal move or ['pass'] if player cannot make a capturing move.
    """
    result = []
    game_over = True
    for r in range(8):
        for c in range(8):
            if board[r][c] == '.':
                here = (r, c)
                if flips(board, player, here):
                    game_over = False
                    result.append(here)
                # The inclusion of game_over in the condition below is for efficiency:
                # If it has already been determined that the game is not over, there's no need to check
                # for opposing legal moves
                elif game_over and flips(board, opposite(player), here):
                    game_over = False
    if result or game_over:
        return result
    return ['pass']


def score(board):
    """
    :param board: A sequence of strings
    :return: The difference between the number of pieces 'X' has and the number 'O' has. This is therefore positive if
    'X' is winning, negative if 'O' is winning, and 0 if the score is tied.
    """
    s = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'X':
                s += 1
            if board[r][c] == 'O':
                s -= 1
    return s


def opposite(player):
    if player == 'X':
        return 'O'
    return 'X'


def value(board, player, depth):
    """
    :param board: A string
    :param player: 'X' or 'O'
    :param depth: At least 1; greater depth is slower but smarter
    :return: The value of board if it is player's turn
    """
    if legal_moves(board, 'X') == legal_moves(board, 'O') == 'pass':
        return score(board)
    if depth == 0:
        return score(board)
    best_value = 0
    if player == 'X':
        best_value = -100
    if player == 'O':
        best_value = 100
    for m in legal_moves(board, player):
        s = successor(board, player, m)
        if player == 'X':
            v = value(s, 'O', depth - 1)
            if v > best_value:
                best_value = v
        if player == 'O':
            v = value(s, 'X', depth - 1)
            if v < best_value:
                best_value = v
    return best_value



def less(x, y):
    return x < y


def greater(x, y):
    return x > y


def best_move(board, player, depth):
    """
    :param board: A string
    :param player: 'X' or 'O'
    :param depth: At least 1; greater depth is slower but smarter
    :return: The best move (index) for player
    """
    best_move = None
    best_value = 0
    if player == 'X':
        best_value = -100
    if player == 'O':
        best_value = 100
    for m in legal_moves(board, player):
        s = successor(board, player, m)
        if player == 'X':
            v = value(s, 'O', depth - 1)
            if v > best_value:
                best_value = v
                best_move = m
        if player == 'O':
            v = value(s, 'X', depth - 1)
            if v < best_value:
                best_value = v
                best_move = m
    return best_move


def print_board(board):
    print(' 01234567')
    for i in range(8):
        print(str(i) + board[i] + str(i))
    print(' 01234567')
    print()


def main():
    board = INITIAL_STATE
    player = 'X'
    while True:
        moves = legal_moves(board, player)
        if not moves:
            break
        if moves == ['pass']:
            move = 'pass'
        elif player == 'X':
            move = best_move(board, player, 5)  # Adjust this number for a stronger, slower player
        else:
            print('Your move.')
            r = int(input('Row: '))
            c = int(input('Column: '))
            move = (r, c)
        board = successor(board, player, move)
        print_board(board)
        player = opposite(player)
    w = score(board)
    if w > 0:
        print('X wins!')
    elif w < 0:
        print('O wins!')
    else:
        print('Tie.')


if __name__ == '__main__':
    main()