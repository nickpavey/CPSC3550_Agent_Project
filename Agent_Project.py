
EMPTY, RED, BLACK = '.', 'r', 'b'
RED_KING, BLACK_KING = 'R', 'B'

BOARD_SIZE = 8

def create_board():
    #This creates an 8x8 board filled with the EMPTY symbol: '.'.
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    #The top 3 rows (0–2) get black pieces: 'b' on alternating dark squares
    for row in range(3):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = BLACK
    #The bottom 3 rows (5–7) get Red pieces ('r') in the same pattern.
    for row in range(5, 8):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = RED
    return board
def print_board(board):
    print("  " + " ".join(str(i) for i in range(BOARD_SIZE)))
    for i, row in enumerate(board):
        print(i, " ".join(row))

def is_king(piece):
    return piece in (RED_KING, BLACK_KING)

def is_valid_position(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

#Setting up a numerical system to help the AI determine the best takes.
def evaluate_board(board):
    score = 0
    for row in board:
        for piece in row:
            if piece == RED:
                score += 1
            elif piece == RED_KING:
                score += 2
            elif piece == BLACK:
                score -= 1
            elif piece == BLACK_KING:
                score -= 2
    return score

def play_game():
    board = create_board()
    human_player = 'r'
    ai_player = 'b'
    current_player = 'r'

    #while True:
    print_board(board)
    winner = check_winner(board)
    if winner:
        print(f"{'Human' if winner == human_player else 'AI'} wins!")
        #break


def check_winner(board):
    #Lower helps avoid adding extra lines checking for king pieces
    red_exists = any(piece.lower() == 'r' for row in board for piece in row)
    black_exists = any(piece.lower() == 'b' for row in board for piece in row)
    #If b, AI wins. If r, Man wins.
    if not red_exists:
        return 'b'
    elif not black_exists:
        return 'r'
    return None

#Nothing happens here so far besides printing the board
if __name__ == '__main__':
    play_game()