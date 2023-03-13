import numpy as np
import math
import itertools
import copy
import enum
from typing import Tuple

from pieces import PieceColor, PieceType, Rotation, Piece, Sphinx, Scarab, Anubis, Pyramid, Pharoah
# Board

# 10 wide, 8 tall

# Representing the pieces by an enum, with the rotation 
# Special squares that only one of a color can enter

# Initial configurations

"""
Rotations

Pharoah, Anubis, Laser Direction:
Up: 0
Right: 0.25
Down: 0.5
Left: 0.75


Pyramid:
|_ : 0
|-- : 0.25
--| : 0.5
_| : 0.75

Scarab: 
\ : 0
/ : 0.5

Sphinx:
facing column: 0
facing row: 0.5
"""
        
# TODO Make a board named tuple that stores config, pieces, next turn seperately from an object
class Board:
    def __init__(self, board_config, eliminated_pieces, next_turn):
        # self.board_config = np.array((8, 10))
        # self.elimnated_pieces = []
        # self.next_turn = PieceColor.RED
        self.board_config = board_config
        self.eliminated_pieces = eliminated_pieces
        self.next_turn = next_turn

    def _is_valid(self):
        # check correct number of pieces
        # check peices not on incorrect colored squares
        pass

    def make_move(self, position, new_position) -> "Board":
        # Make move, compute if any pieces got eliminated, generate a new board
        new_board = copy.deepcopy(self.board_config)

        piece, color, rotation = self.get_piece_properties(position)
        assert(color == self.next_turn)

        if not self.is_empty(new_position):
            if piece != PieceType.SCARAB:
                raise ValueError(f"Cannot swap type {piece} with another piece")
            new_board[position] = Board.get_encoding(*self.get_piece_properties(new_position))
        else:
            new_board[position] = 0
        new_board[new_position] = Board.get_encoding(piece, color, rotation)

        new_board_obj = Board(new_board, self.eliminated_pieces, PieceColor(-1 * self.next_turn.value))

        # Check if anything gets lasered!
        off_board = False
        if self.next_turn == PieceColor.RED:
            laser_position = (0, 0)
            laser_rotaton = 0.5
        else:
            laser_position = (7, 9)
            laser_rotation = 0
        
        while True:
            # Get the next item it lands on
            if laser_rotation == 0:
                # Pointing north
                col = new_board[:, laser_position[1]]
                # If no non-zero the laser is off the board
                if len(np.nonzero(col)) == 0:
                    break
                # Get the largest idx of non-zero value, since that is the lowest piece getting hit
                row = np.max(np.nonzero(col))
                # If row below current piece, then the laser if off board
                if row < laser_position[0]:
                    break

                # Otherwise we have hit a piece!
                hit_position = (row, col)

                piece, color, rotation = new_board_obj.get_piece_properties(hit_position)

                if piece == PieceType.PHAROAH:
                    # TODO: GAME OVER
                    break
                elif piece == PieceType.ANUBIS:
                    if rotation != Rotation.S:
                        new_board_obj.eliminated_pieces.append((piece, color))
                        new_board_obj
                        self.board_config[hit_position] = 0
                        break
                elif piece == PieceType.PYRAMID:
                    if rotation == Rotation.SE:
                        # Reflects the laser right
                        laser_position = hit_position
                        laser_rotation = Rotation.E
                    elif rotation == Rotation.SW:
                        # Reflects the laser left
                        laser_position = hit_position
                        laser_rotation = Rotation.W
                    else:
                        # Hit!
                        new_board_obj.eliminated_pieces.append((piece, color))
                        new_board_obj.board_config[hit_position] = 0
                elif piece == PieceType.SCARAB:
                    if rotation == Rotation.NE:
                        # Reflects the laser left
                        laser_position = hit_position
                        laser_rotation = Rotation.W
                    else:
                        # Reflects the laser right
                        laser_position = hit_position
                        laser_rotation = Rotation.E
                elif piece == PieceType.SPHINX:
                    break
            else:
                # TODO other rotations
                pass

    @staticmethod
    def get_encoding(piece, color, rotation):
        return piece.value * color.value + (rotation.value/8.0)


    def in_bounds(self, position) -> bool:
        return position[0] >= 0 and position[0] <= 8 and \
            position[1] >= 0 and position[1] <= 10

    def get_piece(self, position: Tuple[int, int]):
        """
        Given a (r, c) return piece type
        """
        assert(self.in_bounds(position))
        val = self.board_config[position]
        piece = abs(int(np.floor(val)))
        return PieceType(piece)
    
    def get_color(self, position):
        assert(self.in_bounds(position))
        val = self.board_config[position]
        color = PieceColor.SILVER if val > 0 else PieceColor.RED
        return color

    def get_rotation(self, position: Tuple[int, int]):
        assert(self.in_bounds(position))
        val = abs(self.board_config[position])
        # TODO do some validation to make sure rotation is valid
        return Rotation( int( 8 * (val % 1)))
    
    def get_piece_properties(self, position):
        assert(self.in_bounds(position))
        val = self.board_config[position]
        piece = PieceType(abs(int(np.floor(val))))
        color = PieceColor.SILVER if val > 0 else PieceColor.RED

        val = abs(val)
        rotation = Rotation( int( 8 * (val % 1)))
        return piece, color, rotation

    def is_empty(self, position):
        val = self.board_config[position]
        return val == 0

    def get_next_moves(self):
        B = self.board_config
        filter_B = B < 0 if self.next_turn == PieceColor.RED else B > 0
        pieces_idxs = np.nonzero(filter_B)

        next_board_positions = []

        for i in range(np.shape(pieces_idxs)[1]):
            position = (pieces_idxs[0][i], pieces_idxs[1][i])
            piece_type = self.get_piece(position)

            if piece_type == PieceType.SPHINX:
                moves = Sphinx.get_moves(self, position)
            elif piece_type == PieceType.SCARAB:
                moves = Scarab.get_moves(self, position)
            elif piece_type == PieceType.ANUBIS:
                moves = Anubis.get_moves(self, position)
            elif piece_type == PieceType.PYRAMID:
                moves = Pyramid.get_moves(self, position)
            elif piece_type == PieceType.PHAROAH:
                moves = Pharoah.get_moves(self, position)

            print(f"Piece: {piece_type} Moves: {moves}")
            """
            next_board_positions.extend(
                [self.make_move(move) for move in moves]
            )
            """
            




