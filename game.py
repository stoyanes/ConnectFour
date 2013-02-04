'''
Standart Connect four game. Here, the game is implemented with python and pygame library. For artificial intelligence is used
minimax algorithm.


Note: The game is not implemented with object-oriented way, because of simplicity and performance.
'''

import random
import copy
import sys
import pygame
from constants import *
from functions import *
from pygame.locals import *


'''
    main() function inits images of the game and run the main loop.
    
'''
def main():
    
    pygame.init()
    pygame.display.set_caption('Connect Four')
    init_system_game_data()
    init_human_player_data()
    init_computer_player_data()

    draw_welcome_mess(screen)
    user_option = get_start_option(screen)
    
    # This here is a little tricky. I needed a pointer to track difficulty level (to be easy changed by the user)
    # and array with one element is doing a perfect job for me :)
    difficulty = [2]
    
    while True:

        if user_option == QUIT_GAME:
            pygame.quit()
            sys.exit()
        
        turn = HUMAN
        main_board = new_board()
        choice = None
        
        while True:
        # Human player logic is here:
            if turn == HUMAN:
                get_human_move(main_board, difficulty)
                if is_winner(main_board, RED):
                    draw_human_player_win_mess(screen)
                    choice = get_continue_play_choice(screen)
                    if choice == CONTINUE_PLAY_YES:
                        main_board = new_board()
                    else:
                        pygame.quit()
                        sys.exit()
                turn = COMPUTER
            else:

                col = bestMove(difficulty[0], main_board)
                make_move(main_board, YELLOW, col[0])
                #(state, column, color):
                #makeMove(main_board, col[0], YELLOW)
                if is_winner(main_board, YELLOW):
                    draw_computer_player_win_mess(screen)
                    choice = get_continue_play_choice(screen)
                    print(choice)
                    if choice == CONTINUE_PLAY_YES:
                        main_board = new_board()  
                    else:
                        pygame.quit()
                        sys.exit()
                turn = HUMAN

            # Draw state goes here:
            if is_board_full(main_board):
                draw_mess(screen)
                choice = get_continue_play_choice(screen)
                if choice == CONTINUE_PLAY_YES:
                    main_board = new_board()
                else:
                    pygame.quit()
                    sys.exit()

            # To clear some bad effects of multiple clicking of user
            pygame.event.clear()


'''
    This function draws the board, the position of players and difficulty mode. 
    First parameter is the board on which everythong is going to be drawn
    Second parameter is the difficulty level. This is just for drawing the correct image, noting more.
'''
def draw_board(board, diff):
    screen.blit(background_img, (0, 0))
    rect = pygame.Rect(0, 0, SPACE_SIZE, SPACE_SIZE)
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            rect.topleft = (X_DISTANCE + (x * SPACE_SIZE), Y_DISTANCE + (y * SPACE_SIZE))
            if board[x][y] == RED:
                screen.blit(human_player_img, rect)
            elif board[x][y] == YELLOW:
                screen.blit(computer_player_img, rect)
    
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_WIDTH):
            rect.topleft = (X_DISTANCE + (x * SPACE_SIZE), Y_DISTANCE + (y * SPACE_SIZE))
            screen.blit(board_img, rect)
    
    # Some kind of stupid implementation but will be improved later
    if diff[0] == 1:   
        screen.blit(easy_diff, (0, WINDOW_HEIGHT - 50))

    if diff[0] == 2:
        screen.blit(medium_diff, (0, WINDOW_HEIGHT - 50))

    if diff[0] == 3:
        screen.blit(hard_diff, (0, WINDOW_HEIGHT - 50))

'''
Get next position on which human player will place his tile. Also this function listens to event to change the 
difficult level. I know this is not good, do more than one thing but I promise this will be improved soon. :)
'''
def get_human_move(board, diff):
    coord_x, coord_y = None, None
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_q:
                pygame.quit()
                sys.exit()

            # Here we are listening to eventually change the difficulty level
            # harder:
            elif event.type == KEYDOWN and event.key == K_d:
                if diff[0] == 3:
                    diff[0] = 2
                    draw_board(board, diff)
                    continue
                if diff[0] == 2:
                    diff[0] = 1
                draw_board(board, diff)
            # easier: 
            elif event.type == KEYDOWN and event.key == K_u:
                if diff[0] == 1:
                    diff[0] = 2
                    draw_board(board, diff)
                    continue
                if diff[0] == 2:
                    diff[0] += 1
                draw_board(board, diff)
            # Just picking the positon of mouse click and evaluate the proper column to place 
            # player tile
            elif event.type == MOUSEBUTTONDOWN:
                coord_x, coord_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                column = int((coord_x - X_DISTANCE) / SPACE_SIZE)
                if is_valid_move(board, column):
                    board[column][get_empty_space(board, column)] = RED
                    draw_board(board, diff)
                    pygame.display.update()
                    return
                coord_x, coord_y = None, None

        draw_board(board, diff)
        pygame.display.update()

def init_system_game_data():
    global screen, board_img, background_img, another_game_img, easy_diff, medium_diff, hard_diff
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    board_img = pygame.image.load('images/board.png')
    board_img = pygame.transform.smoothscale(board_img, (SPACE_SIZE, SPACE_SIZE))
    background_img = pygame.image.load('images/background.png')
    another_game_img = pygame.image.load('images/another_game_mess.png')
    easy_diff = pygame.image.load('images/diff_easy.png')
    medium_diff = pygame.image.load('images/diff_medium.png')
    hard_diff = pygame.image.load('images/diff_hard.png')
    
def init_human_player_data():
    global human_player_rect, human_player_img
    human_player_rect = pygame.Rect(int(SPACE_SIZE / 2), WINDOW_HEIGHT - int(3 * SPACE_SIZE / 2), SPACE_SIZE, SPACE_SIZE)
    human_player_img = pygame.image.load('images/red_player.png')
    human_player_img = pygame.transform.smoothscale(human_player_img, (SPACE_SIZE, SPACE_SIZE))
    
    
def init_computer_player_data():
    global computer_player_rect, computer_player_img, computer_player_win_img
    computer_player_rect = pygame.Rect(WINDOW_WIDTH - int(3 * SPACE_SIZE / 2), WINDOW_HEIGHT - int(3 * SPACE_SIZE / 2), SPACE_SIZE, SPACE_SIZE)
    computer_player_img = pygame.image.load('images/yellow_player.png')
    computer_player_img = pygame.transform.smoothscale(computer_player_img, (SPACE_SIZE, SPACE_SIZE))
    computer_player_win_img = pygame.image.load('images/computer_player_win.png')

    
def bestMove(depth, board):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """
        
        # determine opponent's color

        opp_player = RED
        
        # enumerate all legal moves
        legal_moves = {} # will map legal move states to their alpha values
        for col in range(BOARD_WIDTH):
            # if column i is a legal move...
            if is_valid_move(board, col):
                board_copy = copy.deepcopy(board)
                make_move(board_copy, YELLOW, col)
                legal_moves[col] = -search(depth-1, board_copy, opp_player)
        
        best_alpha = -99999999
        best_move = None

        moves = list(legal_moves.items())

        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move
        
        return best_move, best_alpha

               
def search(depth, board, curr_player):
    """ Searches the tree at depth 'depth'
        By default, the state is the board, and curr_player is whomever 
        called this search
        
        Returns the alpha value
    """
    
    # enumerate all legal moves from this state
    legal_moves = []
    for i in range(BOARD_WIDTH):
        # if column i is a legal move...
        #if self.isLegalMove(i, board):
        if is_valid_move(board, i):
            board_copy = copy.deepcopy(board)
            make_move(board_copy, curr_player, i)
            legal_moves.append(board_copy)
    
    # if this node (state) is a terminal node or depth == 0...
    if depth == 0 or len(legal_moves) == 0 or gameIsOver(board_copy):
        # return the heuristic value of node
        return value(board_copy, curr_player)
    
    # determine opponent's color
    if curr_player == RED:
        opp_player = YELLOW
    else:
        opp_player = RED

    alpha = -99999999
    for child in legal_moves:
        if child == None:
            print("child == None (search)")
        alpha = max(alpha, -search(depth-1, child, opp_player))
    return alpha


def gameIsOver(state):
    if checkForStreak(state, RED, 4) >= 1:
        return True
    elif checkForStreak(state, YELLOW, 4) >= 1:
        return True
    else:
        return False
    



def value(state, color):
    """ Simple heuristic to evaluate board configurations
        Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 + 
        (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
        3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
    """
    if color == RED:
        o_color = YELLOW
    else:
        o_color = RED
    
    my_fours = checkForStreak(state, color, 4)
    my_threes = checkForStreak(state, color, 3)
    my_twos = checkForStreak(state, color, 2)
    opp_fours = checkForStreak(state, o_color, 4)
    #opp_threes = self.checkForStreak(state, o_color, 3)
    #opp_twos = self.checkForStreak(state, o_color, 2)
    if opp_fours > 0:
        return -100000
    else:
        return my_fours*100000 + my_threes*100 + my_twos
        
def checkForStreak(state, player, streak):
    count = 0
    # for each piece in the board...
    for i in range(BOARD_WIDTH):
        for j in range(BOARD_HEIGHT):
            # ...that is of the color we're looking for...
            if state[i][j] == player:
                # check if a vertical streak starts at (i, j)
                count += verticalStreak(i, j, state, streak)
                
                # check if a horizontal four-in-a-row starts at (i, j)
                count += horizontalStreak(i, j, state, streak)
                
                # check if a diagonal (either way) four-in-a-row starts at (i, j)
                count += diagonalCheck(i, j, state, streak)
    # return the sum of streaks of length 'streak'
    return count
        
def verticalStreak(row, col, state, streak):
    consecutiveCount = 0
    for i in range(row, BOARD_WIDTH):
        if state[i][col] == state[row][col]:
            consecutiveCount += 1
        else:
            break

    if consecutiveCount >= streak:
        return 1
    else:
        return 0

def horizontalStreak(row, col, state, streak):
    consecutiveCount = 0
    for j in range(col, BOARD_WIDTH):
        if state[row][j] == state[row][col]:
            consecutiveCount += 1
        else:
            break

    if consecutiveCount >= streak:
        return 1
    else:
        return 0

def diagonalCheck(row, col, state, streak):

    total = 0
    # check for diagonals with positive slope
    consecutiveCount = 0
    j = col
    for i in range(row, BOARD_WIDTH):
        if j > BOARD_WIDTH - 1:
            break
        elif state[i][j] == state[row][col]:
            consecutiveCount += 1
        else:
            break
        j += 1 # increment column when row is incremented
        
    if consecutiveCount >= streak:
        total += 1

    # check for diagonals with negative slope
    consecutiveCount = 0
    j = col
    for i in range(row, -1, -1):
        if j > BOARD_WIDTH - 1:
            break
        elif state[i][j] == state[row][col]:
            consecutiveCount += 1
        else:
            break
        j += 1 # increment column when row is incremented

    if consecutiveCount >= streak:
        total += 1

    return total

if __name__ == '__main__':
    main()