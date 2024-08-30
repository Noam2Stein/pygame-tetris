import sys

import pygame
from pygame.locals import *

from piece import *

# parameters

fps = 60

surface_width = 800
surface_height = 500
board_cells = (10, 24)

background_color = (10, 10, 10)
board_background_color = (25, 25, 25)
piece_color = (222, 22, 22)
filled_cell_color = (222, 222, 222)

piece_fall_frequency = 2
piece_drop_fall_frequency = 40
piece_fast_move_wait = 0.125
piece_fast_move_frequency = 40
piece_fast_rotate_wait = 0.25
piece_fast_rotate_frequency = 8

# influenced parameters

delta_time = 1 / fps

surface_aspect = surface_width / surface_height
board_aspect = board_cells[0] / board_cells[1]
board_width = board_aspect / surface_aspect * surface_width
board_x = (surface_width - board_width) / 2
board_rect = pygame.Rect(board_x, 0, board_width, surface_height)
cell_size = board_width / board_cells[0]
border_width = (surface_width - board_width) / 2
next_pieces_x = border_width + board_width + border_width / 2 - cell_size * 1.5
next_pieces_y = round(board_cells[1] / 2 - 2) * cell_size

# behavioural fns

def detect_collision(offset_x: int, offset_y: int) -> bool:
    global piece, filled_cells, board_cells

    for rect in piece.rects():
        for x in range(rect[2]):
            for y in range(rect[3]):
                if (rect[0] + x + offset_x, rect[1] + y + offset_y) in filled_cells:
                    return True
                
    return piece.right() + offset_x > board_cells[0] or piece.left() + offset_x < 0 or piece.bottom() + offset_y > board_cells[1]

def dodge_collision() -> bool:
    global piece

    for x in [0, 1, -1]:
        for y in [0, 1, -1]:
            if not detect_collision(x, y):
                piece.x += x
                piece.y += y
                return False
    
    return True

def row_is_filled(row: int) -> bool:
    global filled_cells, board_cells

    for x in range(board_cells[0]):
        if not (x, row) in filled_cells:
            return False
        
    return True

def clear_lines():
    global filled_cells, board_cells

    while True:
        any = False
        for row in range(board_cells[1] - 1, -1, -1):
            if row_is_filled(row):
                any = True
                for x in range(board_cells[0]):
                    filled_cells.remove((x, row))
            
                for y in range(row, 1, -1):
                    for x in range(board_cells[0]):
                        if (x, y) in filled_cells:
                            filled_cells[filled_cells.index((x, y))] = (x, y + 1)
        if not any:
            return


def fill_piece():
    global piece, filled_cells

    for rect in piece.rects():
        for x in range(rect[2]):
            for y in range(rect[3]):
                filled_cells.append((rect[0] + x, rect[1] + y))
    
    clear_lines()

def use_next_piece():
    global piece, board_cells, next_pieces

    piece = Piece(round(board_cells[0] / 2), 0, next_pieces.next(), 0)
    piece.y = piece.y + round(piece.size()[1] / 2 - 0.49)

    if dodge_collision():
        pygame.quit()
        sys.exit()

def move_piece():
    global piece, piece_move_dir, board_cells

    if 0 <= piece.right() + piece_move_dir <= board_cells[0] and 0 <= piece.left() + piece_move_dir <= board_cells[0] and not detect_collision(piece_move_dir, 0):
        piece.x += piece_move_dir

def drop_piece() -> bool:
    global piece

    if detect_collision(0, 1):
        return True

    piece.y += 1

    return False

def rotate_piece():
    global piece

    piece.rotation += 1
    if piece.rotation == 4:
        piece.rotation = 0

    if dodge_collision():
        piece.rotation -= 1
        if piece.rotation == -1:
            piece.rotation = 3

# game loop

pygame.init()
pygame.display.set_caption("Tetris")
surface = pygame.display.set_mode((surface_width, surface_height))

next_pieces = PieceQueue()

filled_cells = []

piece = None
use_next_piece()
piece_fall_timer = 0
piece_drop = False
piece_move_dir = 0
piece_move_timer = 0
piece_rotate = False
piece_rotate_timer = 0

while True:
    #
    # event handling
    #
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                piece_move_dir = 1
                move_piece()
                piece_move_timer = piece_fast_move_wait

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                piece_move_dir = -1
                move_piece()
                piece_move_timer = piece_fast_move_wait

            if event.key == pygame.K_UP or event.key == pygame.K_w:
                rotate_piece()
                piece_rotate = True
                piece_rotate_timer = piece_fast_rotate_wait

            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                piece_drop = True
                piece_fall_timer = min(piece_fall_timer, 1 / piece_drop_fall_frequency)

        if event.type == KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if piece_move_dir == 1:
                    piece_move_dir = 0

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if piece_move_dir == -1:
                    piece_move_dir = 0

            if event.key == pygame.K_UP or event.key == pygame.K_w:
                piece_rotate = False

            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                piece_drop = False

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #
    # *** event handling
    #

    #
    # update
    #

    piece_move_timer -= delta_time
    if piece_move_timer <= 0 and piece_move_dir != 0:
        piece_move_timer = 1 / piece_fast_move_frequency
        move_piece()

    piece_rotate_timer -= delta_time
    if piece_rotate_timer <= 0 and piece_rotate:
        piece_rotate_timer = 1 / piece_fast_rotate_frequency
        rotate_piece()

    piece_fall_timer -= delta_time
    if piece_fall_timer <= 0:
        piece_fall_timer = 1 / (piece_drop_fall_frequency if piece_drop else piece_fall_frequency)
        if drop_piece():
            fill_piece()
            use_next_piece()
    
    #
    # *** update
    #

    #
    # draw
    #
    surface.fill(background_color)
    surface.fill(board_background_color, board_rect)

    piece.fill(surface, piece_color, (board_x, 0, cell_size, cell_size))

    for cell in filled_cells:
        surface.fill(filled_cell_color, (board_x + cell[0] * cell_size, cell[1] * cell_size, cell_size, cell_size))

    next_piece_y = next_pieces_y
    for next_piece in next_pieces.queue:
        next_piece.fill(surface, piece_color, (next_pieces_x, next_piece_y, cell_size, cell_size))
        next_piece_y += next_piece.size()[1] + cell_size

    #
    # *** draw
    #

    pygame.display.update()
    pygame.time.Clock().tick(fps)