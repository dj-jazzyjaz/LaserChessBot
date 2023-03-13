import numpy as np
import math
import itertools
import copy
from enum import Enum
from typing import Tuple

class PieceType(Enum):
    NONE = 0
    PHAROAH = 1
    SCARAB = 2
    PYRAMID = 3
    ANUBIS = 4
    SPHINX = 5

class PieceColor(Enum):
    RED = -1
    SILVER = 1

class Rotation(Enum):
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7

TRANSLATE_MOVES = list(itertools.product(
            [-1, 0, 1],
            [-1, 0, 1]
    ))
TRANSLATE_MOVES.remove((0, 0))

def in_bounds(position):
    return 0 <= position[0] and position[0] < 8 and 0 <= position[1] and position[1] < 10

def add_move(position, move):
    return (position[0] + move[0], position[1] + move[1])

class Piece:
    # Get all valid moves
    @staticmethod
    def get_moves(
        board,
        position,
    ):       
        curr_rotation = board.get_rotation(position)

        # Stored as ((r, c), rotation)
        moves = []

        # Add the rotation
        moves.append((position, Rotation((curr_rotation.value + 2) % 8)))
        moves.append((position, Rotation((curr_rotation.value - 2) % 8)))

        # TODO should we check for validity here or not
        # Try moving
        
        for move in TRANSLATE_MOVES:
            new_pos = add_move(position, move)
            
            if in_bounds(new_pos) and board.is_empty(new_pos):
                moves.append((new_pos, curr_rotation))

        return moves

class Scarab(Piece):
    @staticmethod
    def get_moves(board, position):
        assert board.get_piece(position) == PieceType.SCARAB

        curr_rotation = board.get_rotation(position)
 
        moves = []

        if curr_rotation == Rotation.NE:
            moves.append((position, Rotation.NW))
        elif curr_rotation == Rotation.NW:
            moves.append((position, Rotation.NE))
        else:
            raise ValueError(f"Scarab can only have rotation of NW or NE, this scarab is {curr_rotation}")

        # Add swap moves
        for move in TRANSLATE_MOVES:
            new_move = add_move(position, move)
            if in_bounds(new_move):
                if board.get_piece(new_move) != PieceType.SCARAB:
                    moves.append((new_move, curr_rotation))

        return moves

class Sphinx(Piece):
    @staticmethod
    def get_moves(board, position):
        assert board.get_piece(position) == PieceType.SPHINX
        curr_rotation = board.get_rotation(position)

        ## Upper Sphinx
        if position == (0, 0):
            if curr_rotation == Rotation.S:
                return((position, Rotation.E))
            elif curr_rotation == Rotation.E:
                return((position, Rotation.S))
        ## Lower Sphinx
        elif position == (7, 9):
            if curr_rotation == Rotation.N:
                return((position, Rotation.W))
            elif curr_rotation == Rotation.W:
                return((position, Rotation.N))
        else:
            raise ValueError(f"Sphinx can only be in position (0, 0) or (7, 9). This sphinx position is {position}")
            

class Anubis(Piece):
    @staticmethod
    def get_moves(board, position):
        assert board.get_piece(position) == PieceType.ANUBIS

        return Piece.get_moves(board, position)
    
class Pharoah(Piece):
    @staticmethod
    def get_moves(board, position):
        assert board.get_piece(position) == PieceType.PHAROAH

        return Piece.get_moves(board, position)

class Pyramid(Piece):
    @staticmethod
    def get_moves(board, position):
        assert board.get_piece(position) == PieceType.PYRAMID

        return Piece.get_moves(board, position)        