# seems to be working ok. I created the next file to add "undo/redo" and the choice to play as white or black.

import pygame
import os
import chess
import chess.engine

pygame.init()

# Set up the Pygame window
WINDOW_SIZE = (640, 640)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chess")

# Set up the Chess engine
engine = chess.engine.SimpleEngine.popen_uci("D:\Mine\Python Projects\AIchess\Leela Chess Zero (LCZero) engine\lc0.exe")

# Set up the Chess board
board = chess.Board()

# Set up the Chess pieces
piece_images = {}
file_location = os.path.dirname(os.path.abspath(__file__))
for color in ("b", "w"):
    for piece_type in ("k", "q", "r", "n", "b", "p"):
        # image_path = os.path.join("pieces", f"{color}{piece_type}.png")
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pieces", f"{color}{piece_type}.png")
        # image_path = os.path.join(file_location, f"pieces\{color}{piece_type()}.png")
        piece_images[(color, piece_type)] = pygame.image.load(image_path)

# Draw the Chess board
def draw_board():
    # Draw the squares
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                square_color = (240, 217, 181)
            else:
                square_color = (181, 136, 99)
            # pygame.draw.rect(screen, square_color, (col * 80, row * 80, 80, 80))
            pygame.draw.rect(screen, square_color, (col * 80, row * 80, 80, 80))
    # Draw the pieces
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece:
                color = "b" if piece.color == chess.BLACK else "w"
                piece_type = piece.symbol().lower()
                image = piece_images[(color, piece_type)]
                screen.blit(image, (col * 80, row * 80))

# Make a move
def make_move(move):
    board.push(move)
    draw_board()

# Get the AI's move
def get_ai_move():
    result = engine.play(board, chess.engine.Limit(time=2.0))
    make_move(result.move)

def game_loop():
    running = True
    selected_square = None
    legal_moves = set()
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    col = x // 80
                    row = 7 - (y // 80)
                    square = chess.square(col, row)
                    piece = board.piece_at(square)
                    if piece and piece.color == chess.WHITE:
                        selected_square = square
                        legal_moves = set(
                            move.to_square for move in board.legal_moves if move.from_square == square
                        )
                    elif selected_square and square in legal_moves:
                        move = chess.Move(selected_square, square)
                        make_move(move)
                        if not board.is_game_over():
                            get_ai_move()
                        selected_square = None
                        legal_moves = set()
        # Draw the board
        draw_board()
        # Draw circles around the legal moves
        if selected_square is not None:
            for move_square in legal_moves:
                col = chess.square_file(move_square)
                row = 7 - chess.square_rank(move_square)
                pygame.draw.circle(screen, (0, 255, 0), (col * 80 + 40, row * 80 + 40), 20, 4)
        # Update the display
        pygame.display.update()
    pygame.quit()

game_loop()
