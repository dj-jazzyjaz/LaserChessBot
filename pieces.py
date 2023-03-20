from dataclasses import dataclass
import numpy as np
import math
import itertools
import copy
from enum import Enum
from typing import List, Optional, Tuple

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

@dataclass
class Move:
    position: Tuple[int, int]
    rotation: Rotation
    
    is_position_new: bool = True # True if the position is new, false if the rotation is new
    is_swap: bool = False

def turn_180(rotation):
    return Rotation((rotation.value + 4) % 8)

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
    )  -> List[Move]:       
        curr_rotation = board.get_rotation(position)

        # Stored as ((r, c), rotation)
        moves = []

        # Add the rotation
        moves.append(Move(position, Rotation((curr_rotation.value + 2) % 8), False))
        moves.append(Move(position, Rotation((curr_rotation.value - 2) % 8), False))

        # TODO should we check for validity here or not
        # Try moving
        
        for move in TRANSLATE_MOVES:
            new_pos = add_move(position, move)
            
            if in_bounds(new_pos) and board.is_empty(new_pos):
                moves.append(Move(new_pos, curr_rotation))

        return moves

class Scarab(Piece):
    @staticmethod
    def get_moves(board, position) -> List[Tuple[Tuple[int, int], Rotation]]:
        assert board.get_piece(position) == PieceType.SCARAB

        curr_rotation = board.get_rotation(position)
 
        moves = []

        if curr_rotation == Rotation.NE:
            moves.append(Move(position, Rotation.NW, False))
        elif curr_rotation == Rotation.NW:
            moves.append(Move(position, Rotation.NE, False))
        else:
            raise ValueError(f"Scarab can only have rotation of NW or NE, this scarab is {curr_rotation}")

        # Add swap moves
        for move in TRANSLATE_MOVES:
            new_move = add_move(position, move)
            if in_bounds(new_move):
                if board.get_piece(new_move) != PieceType.SCARAB:
                    moves.append(Move(new_move, curr_rotation, True, is_swap=not board.is_empty(new_move)))

        return moves
    
    @staticmethod
    def hit(laser_rotation, piece_rotation) -> Tuple[bool, Optional[Rotation]]:
        """
        Returns:
            hit (bool): True if piece is hit and must be eliminated
            new_laser_rotation (Optional[Rotation]): The new laser rotation if reflected, None if piece is hit and eliminated
        -----> |<--
        """
        """
        If scarab is NE: N->W, W->N, S->E, E->S
        If scarab is NW: N->E, E->N, S->W, W->S
        """
        if piece_rotation == Rotation.NE:
            match laser_rotation:
                case Rotation.N:
                    return (False, Rotation.W)
                case Rotation.W:
                    return (False, Rotation.N)
                case Rotation.S:
                    return (False, Rotation.E)
                case Rotation.E:
                    return (False, Rotation.S)
                case _:
                    raise ValueError(f"Invalid laser rotation {laser_rotation}")
        elif piece_rotation == Rotation.NW:
            match laser_rotation:
                case Rotation.N:
                    return (False, Rotation.E)
                case Rotation.E:
                    return (False, Rotation.N)
                case Rotation.S:
                    return (False, Rotation.W)
                case Rotation.W:
                    return (False, Rotation.S)
                case _:
                    raise ValueError(f"Invalid laser rotation {laser_rotation}")
        else:
            raise ValueError(f"Scarab can only have rotation of NW or NE, this scarab is {piece_rotation}")
    

class Sphinx(Piece):
    @staticmethod
    def get_moves(board, position) -> List[Tuple[Tuple[int, int], Rotation]]:
        assert board.get_piece(position) == PieceType.SPHINX
        curr_rotation = board.get_rotation(position)

        ## Upper Sphinx
        if position == (0, 0):
            if curr_rotation == Rotation.S:
                return [Move(position, Rotation.E, False)]
            elif curr_rotation == Rotation.E:
                return [Move(position, Rotation.S, False)]
        ## Lower Sphinx
        elif position == (7, 9):
            if curr_rotation == Rotation.N:
                return [Move(position, Rotation.W, False)]
            elif curr_rotation == Rotation.W:
                return [Move(position, Rotation.N, False)]
        else:
            raise ValueError(f"Sphinx can only be in position (0, 0) or (7, 9). This sphinx position is {position}")
        
    @staticmethod
    def hit(laser_rotation, piece_rotation) -> Tuple[bool, Optional[Rotation]]:
        return False, None
            

class Anubis(Piece):
    @staticmethod
    def get_moves(board, position) -> List[Tuple[Tuple[int, int], Rotation]]:
        assert board.get_piece(position) == PieceType.ANUBIS

        return Piece.get_moves(board, position)
    
    @staticmethod
    def hit(laser_rotation, piece_rotation) -> Tuple[bool, Optional[Rotation]]:
        """
        If laser comes from 180 degrees of the piece rotation is blocked, otherwise it is hit
        """
        if turn_180(piece_rotation) == laser_rotation:
            return False, None
        else:
            return True, None
    
class Pharoah(Piece):
    @staticmethod
    def get_moves(board, position) -> List[Tuple[Tuple[int, int], Rotation]]:
        assert board.get_piece(position) == PieceType.PHAROAH

        # only allow the Pharoah to move since turning doesn't do anything
        return [move for move in Piece.get_moves(board, position) if not move.is_position_new]
    
    @staticmethod
    def hit(laser_rotation, piece_rotation) -> Tuple[bool, Optional[Rotation]]:
        return True, None

class Pyramid(Piece):
    @staticmethod
    def get_moves(board, position) -> List[Tuple[Tuple[int, int], Rotation]]:
        assert board.get_piece(position) == PieceType.PYRAMID

        return Piece.get_moves(board, position)        
    
    @staticmethod
    def hit(laser_rotation, piece_rotation) -> Tuple[bool, Optional[Rotation]]:
        """
        NE: S->E, W->N, N->hit, E->hit
        NW: S->W, E->N, N->hit, W->hit
        SE: N->E, W->S, S->hit, E->hit
        SW: N->W, E->S, S->hit, W->hit
        """
        if piece_rotation == Rotation.NE:
            match laser_rotation:
                case Rotation.S:
                    return (False, Rotation.E)
                case Rotation.W:
                    return (False, Rotation.N)
                case Rotation.N:
                    return (True, None)
                case Rotation.E:
                    return (True, None)
                case _:
                    raise ValueError(f"Invalid laser rotation {laser_rotation}")
        elif piece_rotation == Rotation.NW:
            match laser_rotation:
                case Rotation.S:
                    return (False, Rotation.W)
                case Rotation.E:
                    return (False, Rotation.N)
                case Rotation.N:
                    return (True, None)
                case Rotation.W:
                    return (True, None)
                case _:
                    raise ValueError(f"Invalid laser rotation {laser_rotation}")
        elif piece_rotation == Rotation.SE:
            match laser_rotation:
                case Rotation.N:
                    return (False, Rotation.E)
                case Rotation.W:
                    return (False, Rotation.S)
                case Rotation.S:
                    return (True, None)
                case Rotation.E:
                    return (True, None)
                case _:
                    raise ValueError(f"Invalid laser rotation {laser_rotation}")
        elif piece_rotation == Rotation.SW:
            match laser_rotation:
                case Rotation.N:
                    return (False, Rotation.W)
                case Rotation.E:
                    return (False, Rotation.S)
                case Rotation.S:
                    return (True, None)
                case Rotation.W:
                    return (True, None)
                case _:
                    raise ValueError(f"Invalid laser rotation {laser_rotation}")
        else:
            raise ValueError(f"Pyramid can only have rotation of NW, NE, SW, or SE, this pyramid is {piece_rotation}")
        
def get_piece_from_piece_type(piece_type):
    if piece_type == PieceType.ANUBIS:
        return Anubis
    elif piece_type == PieceType.PHAROAH:
        return Pharoah
    elif piece_type == PieceType.PYRAMID:
        return Pyramid
    elif piece_type == PieceType.SCARAB:
        return Scarab
    elif piece_type == PieceType.SPHINX:
        return Sphinx
    else:
        raise ValueError(f"Invalid piece type {piece_type}")