import copy  #Used to deep-copy the board when simulating moves

#Constants for different types of pieces
#Regular pieces
EMPTY, RED, BLACK = '.', 'r', 'b'     
#King pieces          
RED_KING, BLACK_KING = 'R', 'B'                

BOARD_SIZE = 8  #Checkers board is 8x8

def create_board():
    #Create 8x8 empty board
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  
    for row in range(3):  #Top three rows for BLACK pieces
        #This puts the pieces in the 'dark' squares where there isnt a '.'
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:  
                board[row][col] = BLACK
    for row in range(5, 8):  #Bottom three rows for RED pieces
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = RED
    return board

#Prints the board to the terminal
def print_board(board):
    print("  " + " ".join(str(i) for i in range(BOARD_SIZE)))  #Print column headers
    #Enumerate associates a tuple with an associated number
    for i, row in enumerate(board):
        print(chr(65 + i), " ".join(row))  #Print row index and row contents

#Tracker for king pieces
def is_king(piece):
    return piece in (RED_KING, BLACK_KING)

#Checks for board bounds
def is_valid_position(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

#Returns all possible valid moves for a given players pieces
def get_all_moves(board, player):
    moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            #Check if the piece belongs to the player
            if board[r][c].lower() == player:  
                piece_moves = get_piece_moves(board, r, c)
                moves.extend(piece_moves)
    return moves

#Returns valid moves for a specific piece at any row and column
def get_piece_moves(board, r, c):
    moves = []
    piece = board[r][c]
    directions = []

    #RED or KING can move up (toward smaller row numbers)
    if piece.lower() == 'r' or is_king(piece):
        directions.extend([(-1, -1), (-1, 1)])
    #BLACK or KING can move down (toward larger row numbers)
    if piece.lower() == 'b' or is_king(piece):
        directions.extend([(1, -1), (1, 1)])
    
    for dr, dc in directions:
        nr, nc = r + dr, c + dc  #Next regular move position
        if is_valid_position(nr, nc) and board[nr][nc] == EMPTY:
            moves.append(((r, c), (nr, nc)))  #Normal move
        elif is_valid_position(nr, nc) and board[nr][nc].lower() != piece.lower():
            #Jumping over opponent piece
            jump_r = nr + dr
            jump_c = nc + dc
            if is_valid_position(jump_r, jump_c) and board[jump_r][jump_c] == EMPTY:
                moves.append(((r, c), (jump_r, jump_c)))  #Capture move
    return moves

#Applies a move to the board and returns a new board state
def make_move(board, move):
    new_board = copy.deepcopy(board)  #Copy board to avoid modifying the original
    (r1, c1), (r2, c2) = move  #Extract move coordinates
    piece = new_board[r1][c1]
    new_board[r1][c1] = EMPTY  #Remove piece from old spot
    new_board[r2][c2] = piece  #Place piece in new spot

    #If the move is a jump, remove the captured piece
    if abs(r2 - r1) == 2:
        #Floor operation to remove captured piece
        new_board[(r1 + r2)//2][(c1 + c2)//2] = EMPTY

    #Promote to king if piece reaches the end of the board
    if piece == RED and r2 == 0:
        new_board[r2][c2] = RED_KING
    elif piece == BLACK and r2 == BOARD_SIZE - 1:
        new_board[r2][c2] = BLACK_KING

    return new_board

#Evaluates the board from REDs perspective (+ means RED is winning)
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

#The fun part: Minimax algorithm with fixed depth
def minimax(board, depth, maximizing):
    if depth == 0:
        return evaluate_board(board), None  #Return evaluation score and no move

    player = 'r' if maximizing else 'b'
    moves = get_all_moves(board, player)

    if not moves:
        return evaluate_board(board), None  #No moves = lose condition

    best_move = None
    if maximizing:
        #Check for best move for itself
        max_eval = float('-inf')
        for move in moves:
            #We do not care about the move, we instead want the evaluated score
            eval, _ = minimax(make_move(board, move), depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        #Check for best move against opponet
        min_eval = float('inf')
        for move in moves:
            eval, _ = minimax(make_move(board, move), depth - 1, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move

#Main game loop for human vs AI
def play_game():
    board = create_board()
    human_player = 'r'
    current_player = 'r'

    try:
        while True:
            print_board(board)
            winner = check_winner(board)
            if winner:
                print(f"{'Human' if winner == human_player else 'AI'} wins!")
                break
            if current_player == human_player:
                while True:
                    try:
                        print("Choose the piece you want to grab (e.g., F 0), or 'b' to go back:")
                        piece_input = input().strip().upper()
                        if piece_input == 'B':
                            # 'b' input lets the user cancel and reselect
                            print("Returning to piece selection.")
                            continue
                        row_col = piece_input.split()
                        if len(row_col) != 2:     # If container has more than 2 elements, raise ValueErr
                            raise ValueError
                        r1 = ord(row_col[0]) - 65 # Convert row letter to row index
                        c1 = int(row_col[1])      # Convert to int

                        print("Where do you want to place the piece (e.g., E 1), or 'b' to go back:")
                        dest_input = input().strip().upper()
                        if dest_input == 'B':
                            # Another cancel block
                            print("Move cancelled. Start over.")
                            continue
                        row_col = dest_input.split()
                        if len(row_col) != 2:     # If container has more than 2 elements, raise ValueErr
                            raise ValueError
                        r2 = ord(row_col[0]) - 65 # Convert row letter to row index
                        c2 = int(row_col[1])      # Convert to int

                        # Check to see if this move is actually valid
                        move = ((r1, c1), (r2, c2))
                        if move in get_all_moves(board, human_player):
                            # If that move is actually valid, make the move and break the loop
                            board = make_move(board, move)
                            break
                        else:
                            print("Invalid move. Try again.")
                    except ValueError:
                        # 
                        print("Invalid input. Please use the format 'Row Column': (F 0) ")

            else:
                print("AI is thinking...")
                _, move = minimax(board, 3, False)
                if move:
                    board = make_move(board, move)
                    print(f"AI moves from {move[0]} to {move[1]}")
            current_player = 'b' if current_player == 'r' else 'r'

    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")  #Graceful exit on Ctrl+C

#Checks for game over conditions (one color has no pieces)
def check_winner(board):
    red_exists = any(piece.lower() == 'r' for row in board for piece in row)
    black_exists = any(piece.lower() == 'b' for row in board for piece in row)
    if not red_exists:
        return 'b'  #Black wins
    elif not black_exists:
        return 'r'  #Red wins
    return None  #Game continues

if __name__ == '__main__':
    play_game()
