import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
MENU_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# Fonts
font = pygame.font.SysFont(None, 40)

# Board
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]

# Game States
MENU = 0
GAME = 1
game_state = MENU

# Difficulty Levels
EASY = 0
MEDIUM = 1
HARD = 2
difficulty = EASY


# Draw lines
def draw_lines():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (0, row * SQUARE_SIZE),
            (WIDTH, row * SQUARE_SIZE),
            LINE_WIDTH,
        )
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (row * SQUARE_SIZE, 0),
            (row * SQUARE_SIZE, HEIGHT),
            LINE_WIDTH,
        )


draw_lines()


# Draw figures
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "O":
                pygame.draw.circle(
                    screen,
                    CIRCLE_COLOR,
                    (
                        int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                        int(row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    ),
                    CIRCLE_RADIUS,
                    CIRCLE_WIDTH,
                )
            elif board[row][col] == "X":
                pygame.draw.line(
                    screen,
                    CROSS_COLOR,
                    (
                        col * SQUARE_SIZE + SPACE,
                        row * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                    ),
                    (
                        col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                        row * SQUARE_SIZE + SPACE,
                    ),
                    CROSS_WIDTH,
                )
                pygame.draw.line(
                    screen,
                    CROSS_COLOR,
                    (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                    (
                        col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                        row * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                    ),
                    CROSS_WIDTH,
                )


# Check win
def check_win(player):
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[2][0] == board[1][1] == board[0][2] == player:
        return True
    return False


# Check draw
def check_draw():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True


# Evaluate the board state
def evaluate(board):
    if check_win("O"):
        return 1
    if check_win("X"):
        return -1
    return 0


# Minimax algorithm
def minimax(board, depth, is_maximizing):
    score = evaluate(board)

    if score == 1:
        return score
    if score == -1:
        return score
    if check_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = None
                    best_score = min(score, best_score)
        return best_score


# AI move
def ai_move():
    if difficulty == EASY:
        make_random_move()
    elif difficulty == MEDIUM:
        if random.random() < 0.5:
            make_random_move()
        else:
            make_minimax_move()
    else:
        make_minimax_move()


def make_random_move():
    empty_squares = [
        (row, col)
        for row in range(BOARD_ROWS)
        for col in range(BOARD_COLS)
        if board[row][col] is None
    ]
    row, col = random.choice(empty_squares)
    board[row][col] = "O"


def make_minimax_move():
    best_score = -math.inf
    best_move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                board[row][col] = "O"
                score = minimax(board, 0, False)
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    if best_move:
        board[best_move[0]][best_move[1]] = "O"


# Main menu
def draw_main_menu():
    screen.fill(MENU_COLOR)
    easy_button = pygame.Rect(50, 50, 200, 50)
    medium_button = pygame.Rect(50, 125, 200, 50)
    hard_button = pygame.Rect(50, 200, 200, 50)

    pygame.draw.rect(screen, BG_COLOR, easy_button)
    pygame.draw.rect(screen, BG_COLOR, medium_button)
    pygame.draw.rect(screen, BG_COLOR, hard_button)

    easy_text = font.render("Easy", True, TEXT_COLOR)
    medium_text = font.render("Medium", True, TEXT_COLOR)
    hard_text = font.render("Hard", True, TEXT_COLOR)

    screen.blit(easy_text, (easy_button.x + 50, easy_button.y + 10))
    screen.blit(medium_text, (medium_button.x + 30, medium_button.y + 10))
    screen.blit(hard_text, (hard_button.x + 50, hard_button.y + 10))

    return easy_button, medium_button, hard_button


def handle_main_menu_click(pos):
    global game_state, difficulty
    easy_button, medium_button, hard_button = draw_main_menu()
    if easy_button.collidepoint(pos):
        difficulty = EASY
        start_game()
    elif medium_button.collidepoint(pos):
        difficulty = MEDIUM
        start_game()
    elif hard_button.collidepoint(pos):
        difficulty = HARD
        start_game()


def start_game():
    global game_state, board, player, game_over
    board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
    player = "X"
    game_over = False
    game_state = GAME
    screen.fill(BG_COLOR)
    draw_lines()


# Main loop
player = "X"
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_main_menu_click(event.pos)
        elif game_state == GAME:
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if board[clicked_row][clicked_col] is None:
                    board[clicked_row][clicked_col] = player
                    if check_win(player):
                        game_over = True
                    elif check_draw():
                        game_over = True
                    else:
                        player = "O"
                        ai_move()
                        if check_win("O"):
                            game_over = True
                        elif check_draw():
                            game_over = True
                        player = "X"

            screen.fill(BG_COLOR)
            draw_lines()
            draw_figures()
            pygame.display.update()

    if game_state == MENU:
        draw_main_menu()
        pygame.display.update()
