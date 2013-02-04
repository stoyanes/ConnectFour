import pygame
from pygame.locals import *
from constants import *
import random
import sys

def print_array(board):
    for i in range(len(board)):
        print (board[i])
    print('--------')
    
def get_max(moves):
    max = 0.0
    index_of_max = 0
    for i in range(len(moves)):
        if max < moves[i]:
            max = moves[i]
            index_of_max = i
    return max
    
def get_start_option(screen):
    image = pygame.image.load('images/connect-four-choice.png')
    screen.blit(image, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_s:
                return START_GAME
            if event.type == KEYDOWN and event.key == K_q:
                return QUIT_GAME
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def get_random_element(moves):
    random_number = random.randint(0, len(moves) - 1)
    return moves[random_number]

    
def draw_welcome_mess(screen):
    image = pygame.image.load('images/connect-four.png')
    screen.blit(image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(2000)


def draw_human_player_win_mess(screen):
    image = pygame.image.load('images/human_player_win.png')
    screen.blit(image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(2000)


def draw_computer_player_win_mess(screen):
    image = pygame.image.load('images/computer_player_win.png')
    screen.blit(image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(2000)
    

def draw_mess(screen):
    image = pygame.image.load('images/draw_mess.png')
    screen.blit(image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(2000)
    
def get_continue_play_choice(screen):
    image = pygame.image.load('images/another_game_mess.png')
    screen.blit(image, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_y:
                return CONTINUE_PLAY_YES
            if event.type == KEYDOWN and event.key == K_n:
                return CONTINUE_PLAY_NO
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    
def new_board():
    board = []
    for i in range(BOARD_WIDTH):
        board.append([None] * BOARD_HEIGHT)
    return board

def get_best_of_potential(board, potential_moves):
    tmp_best_move = INT_MIN_VALUE
    for i in range(0, BOARD_WIDTH):
            if potential_moves[i] > tmp_best_move and is_valid_move(board, i):
                tmp_best_move = potential_moves[i]
    return tmp_best_move
                
def get_list_of_best_moves(board, best_move, moves):
    best_moves = []
    for i in range(len(moves)):
        if moves[i] == best_move and is_valid_move(board, i):
            best_moves.append(i)
    return best_moves

def get_random_player():
    if random.randint(0, 1) == 0:
        return COMPUTER
    else:
        return HUMAN

def is_board_full(board):
    for i in range(BOARD_WIDTH):
        for j in range(BOARD_HEIGHT):
            if board[i][j] == None:
                return False
    return True

def get_empty_space(board, column):
    for y in range(BOARD_HEIGHT-1, -1, -1):
        if board[column][y] == None:
            return y
    return -1
    

def is_valid_move(board, column):
    if column < 0 or column >= BOARD_WIDTH or board[column][0] != None:
        return False
    return True
    
def is_winner(board, player):
    # check horizontal spaces
    for x in range(BOARD_WIDTH - 3):
        for y in range(BOARD_HEIGHT):
            if board[x][y] == player and board[x+1][y] == player and board[x+2][y] == player and board[x+3][y] == player:
                return True
    # check vertical spaces
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT - 3):
            if board[x][y] == player and board[x][y+1] == player and board[x][y+2] == player and board[x][y+3] == player:
                return True
    # check / diagonal spaces
    for x in range(BOARD_WIDTH - 3):
        for y in range(3, BOARD_HEIGHT):
            if board[x][y] == player and board[x+1][y-1] == player and board[x+2][y-2] == player and board[x+3][y-3] == player:
                return True
    # check \ diagonal spaces
    for x in range(BOARD_WIDTH - 3):
        for y in range(BOARD_HEIGHT - 3):
            if board[x][y] == player and board[x+1][y+1] == player and board[x+2][y+2] == player and board[x+3][y+3] == player:
                return True
    return False

def make_move(board, player, column):
    low = get_empty_space(board, column)
    if low != -1:
        board[column][low] = player
    #to be deleted
    
