import numpy as np
import random
import pygame
import math
import sys

PLAYER = 0
AI = 1

EMPTY_PIECE = 0
PLAYER_PIECE = 1
AI_PIECE = 2

SQUARE_SIZE = 100
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

###################################################################Functions###################################################################
def create_board():
    board = np.zeros((6, 7))
    return board

def print_board(board):
    print(np.flip(board,0))

def drop_piece(board,row,col,piece):
    board[row][col] = piece

def is_valid_location(board,col):
    return board[5][col] == EMPTY_PIECE

def get_next_open_row(board,col):
    for row in range(6):
        if board[row][col] == EMPTY_PIECE:
            return row

def winning_move(board,piece):
    # Horizontal locations
    for col in range(7-3):
        for row in range(6):
            if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                return True

    # Vertical locations
    for row in range(6 - 3):
        for col in range(7):
            if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                return True

    # main diagonals
    for row in range(6 - 3):
        for col in range(7-3):
            if board[row][col] == piece and board[row + 1][col+1] == piece and board[row + 2][col+2] == piece and board[row + 3][col+3] == piece:
                return True

    # anti diagonals
    for row in range(3,6):
        for col in range(7-3):
            if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece and board[row - 3][col + 3] == piece:
                return True

def calc_window(window,piece):
    score = 0
    if (window.count(piece) == 4):
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY_PIECE) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY_PIECE) == 1:
        score += 2

    inv_piece = PLAYER_PIECE
    # if(piece == PLAYER_PIECE):
    #     inv_piece = AI_PIECE

    if window.count(inv_piece) == 3 and window.count(EMPTY_PIECE) == 1:
        score -= 4
    return score

def score_position(board,piece):
    score = 0
    # center column
    center_array = [int(i) for i in list(board[:,3])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Horizontal
    for row in range(6):
        row_array = [int(i) for i in list(board[row,:])]
        for col in range(7-3):
            window = row_array[col:col+4]
            score += calc_window(window,piece)

    # Vertical
    for col in range(7):
        col_array = [int(i) for i in list(board[:,col])]
        for row in range(6-3):
            window = col_array[row:row+4]
            score += calc_window(window,piece)

    # Main diagonals
    for row in range(6-3):
        for col in range(7-3):
            window = [board[row+i][col+i] for i in range(4)]
            score += calc_window(window,piece)

    # Anti diagonals
    for row in range(3,6):
        for col in range(7 - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += calc_window(window,piece)
    return score

def get_valid_locations(board):
    valid_locations = []
    for col in range(7):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def is_terminal_node(board):
    return winning_move(board,PLAYER_PIECE) or winning_move(board,AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board,depth,alpha,beta,maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if is_terminal:
        if winning_move(board,AI_PIECE):
            return None,math.inf
        elif winning_move(board,PLAYER_PIECE):
            return None,-math.inf
        else:# Game is Over
            return None,0
    if depth == 0:# return the heuristic value of node
        return None,score_position(board,AI_PIECE)

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board,col)
            temp_board = board.copy()
            drop_piece(temp_board,row,col,AI_PIECE)
            score = minimax(temp_board,depth-1,alpha,beta,False)[1]
            if score > value:
                value = score
                column = col
            alpha = max(value, alpha)
            if beta <= alpha:
                break
        return column,value
    else:# minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board,col)
            temp_board = board.copy()
            drop_piece(temp_board,row,col,PLAYER_PIECE)
            score = minimax(temp_board, depth - 1,alpha,beta, True)[1]
            if score < value:
                value = score
                column = col
            beta = min(value, beta)
            if beta <= alpha:
                break
        return column,value

def draw_board(board):
    for col in range(7):
        for row in range(6):
            pygame.draw.rect(screen,BLUE,(col*SQUARE_SIZE,row*SQUARE_SIZE+SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            pygame.draw.circle(screen,BLACK,(col*SQUARE_SIZE+SQUARE_SIZE/2,row*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2),RADIUS)

    for col in range(7):
        for row in range(6):
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE / 2, height - (row * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE / 2, height - (row * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
        pygame.display.update()


###################################################################Main Game###################################################################
pygame.init()
FONT = pygame.font.SysFont('comicsans', 45)

width = 7 * SQUARE_SIZE
height = (6 + 1) * SQUARE_SIZE
RADIUS = int(SQUARE_SIZE // 2 - 5)
size = (width, height)
screen = pygame.display.set_mode(size)
board = create_board()
draw_board(board)
print_board(board)
pygame.display.update()

current_player = random.randint(PLAYER,AI)
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            #0 → x - position(starts from left)
            #0 → y-position (starts from top)
            #width → rectangle’s width (full screen width)
            #SQUARE_SIZE → rectangle’s height 100px
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE))
            posX = event.pos[0]
            if current_player == PLAYER:
                #posX → x-position (where your mouse is).
                #int(SQUARE_SIZE/2) → y-position (it's vertically centered inside the top rectangle).
                pygame.draw.circle(screen,RED,(posX, int(SQUARE_SIZE/2)),RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))

            # Player turn
            if current_player == PLAYER:
                posX = event.pos[0]
                col = int(math.floor(posX // SQUARE_SIZE))
                if (is_valid_location(board, col)):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    print_board(board)

                    if (winning_move(board, PLAYER_PIECE)):
                        label = FONT.render("You wins!!! Mabroooooook!!!", True, RED)
                        screen.blit(label,(15,10))
                        game_over = True

                    current_player ^= 1
                    draw_board(board)

    # AI turn
    if current_player == AI and not game_over:
        pygame.time.wait(300)
        col,minimaxScore = minimax(board,2,-math.inf,math.inf,True)
        if (is_valid_location(board, col)):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            print_board(board)

            if (winning_move(board, AI_PIECE)):
                label = FONT.render("AI wins!!!", True, YELLOW)
                screen.blit(label, (15, 10))
                game_over = True

            current_player ^= 1
            draw_board(board)

    if (len(get_valid_locations(board)) == 0):
        pygame.time.wait(300)
        label = FONT.render("GAME OVER", True, RED)
        game_over = True

    if game_over:
        pygame.time.wait(3000)