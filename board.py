import numpy as np
import math
import itertools
import copy
import enum
from typing import Tuple

from pieces import PieceColor, PieceType, Rotation, get_piece_from_piece_type, turn_180

class Board:
    # TODO: support special squares that only one of a color can enter
    n_rows = 8
    n_cols = 10
    def __init__(self, board_config, eliminated_pieces_red, eliminated_pieces_silver, next_turn):
        self.board_config = board_config
        self.eliminated_pieces_red = eliminated_pieces_red
        self.eliminated_pieces_silver = eliminated_pieces_silver
        self.next_turn = next_turn

    @staticmethod
    def from_config_list(config_list, get_mirrored=False):
        board_config = np.zeros((Board.n_rows, Board.n_cols))
        for config in config_list:
            r, c, piece, color, rotation = config
            board_config[r, c] = Board.get_encoding(piece, color, rotation)
            
            board_config[Board.n_rows - r - 1, Board.n_cols - c - 1] = Board.get_encoding(
                piece,
                PieceColor(-1 * color.value),
                turn_180(rotation) if piece != PieceType.SCARAB else rotation)

            if get_mirrored:
                print(f"({Board.n_rows-r-1}, {Board.n_cols-c-1}, {piece}, {PieceColor.SILVER}, { turn_180(rotation) if piece != PieceType.SCARAB else rotation}),")

        return Board(board_config, [], [], PieceColor.RED)
    
    def _is_valid(self):
        # TODO: check correct number of pieces
        # TODO: check peices not on incorrect colored squares
        pass

    def eliminate_piece(self, position) -> Tuple[PieceType, PieceColor]:
        """
        Returns the piece and color of the piece that was eliminated
        """
        assert not self.is_empty(position)
        piece, color, _ = self.get_piece_properties(position)
        if color == PieceColor.RED:
            self.eliminated_pieces_red.append(piece)
        else:
            self.eliminated_pieces_silver.append(piece)
        
        return piece, color

    def make_move(self, position, move) -> "Board":
        """
        Make move, compute if any pieces got eliminated, generate a new board
        """
        new_board = copy.deepcopy(self.board_config)

        piece, color, _ = self.get_piece_properties(position)
        assert(color == self.next_turn)

        if move.is_position_new and not self.is_empty(move.position):
            if piece != PieceType.SCARAB:
                raise ValueError(f"Cannot swap type {piece} with another piece")
            new_board[position] = Board.get_encoding(*self.get_piece_properties(move.position))
        else:
            new_board[position] = 0
        new_board[move.position] = Board.get_encoding(piece, color, move.rotation)

        new_board_obj = Board(new_board, self.eliminated_pieces_red, self.eliminated_pieces_silver, PieceColor(-1 * self.next_turn.value))

        if self.next_turn == PieceColor.RED:
            laser_position = (0, 0)
        else:
            laser_position = (7, 9)
        
        laser_direction = new_board_obj.get_rotation(laser_position)
        eliminated_piece, eliminated_color = (None, None)
        while True:
            next_hit = new_board_obj.get_next_hit(laser_position, laser_direction)
            if next_hit is None:
                break
            piece, piece_color, piece_rotation = new_board_obj.get_piece_properties(next_hit)
            got_hit, new_laser_direction = get_piece_from_piece_type(piece).hit(laser_direction, piece_rotation)

            if got_hit:
                eliminated_piece, eliminated_color = new_board_obj.eliminate_piece(next_hit)
                break

            if new_laser_direction is None:
                # Laser is blocked
                break

            laser_direction = new_laser_direction
            laser_position = next_hit

        return new_board_obj #, eliminated_piece, eliminated_color


    def get_next_hit(self, laser_position, laser_direction):
        def _get_next_nonzero_idx(row_or_col, curr_idx, greater_than=True):
            nonzero_idxs = np.nonzero(row_or_col)[0]
            if greater_than:
                nonzero_idxs = nonzero_idxs[nonzero_idxs > curr_idx]
                if len(nonzero_idxs) == 0:
                    return None
                return np.min(nonzero_idxs)
            else:
                nonzero_idxs = nonzero_idxs[nonzero_idxs < curr_idx]
                if len(nonzero_idxs) == 0:
                    return None
                return np.max(nonzero_idxs)
            

        if laser_direction == Rotation.N or laser_direction == Rotation.S:
            col = self.board_config[:, laser_position[1]]
            idx = _get_next_nonzero_idx(col, laser_position[0], greater_than=laser_direction == Rotation.S)
            if idx is None:
                return None
            return (idx, laser_position[1])
        elif laser_direction == Rotation.E or laser_direction == Rotation.W:
            row = self.board_config[laser_position[0], :]
            idx = _get_next_nonzero_idx(row, laser_position[1], greater_than=laser_direction == Rotation.E)
            if idx is None:
                return None
            return (laser_position[0], idx)

    @staticmethod
    def get_encoding(piece, color, rotation):
        return color.value * (piece.value + (rotation.value/8.0))


    def in_bounds(self, position) -> bool:
        return position[0] >= 0 and position[0] <= 8 and \
            position[1] >= 0 and position[1] <= 10

    def get_piece(self, position: Tuple[int, int]):
        """
        Given a (r, c) return piece type
        """
        assert(self.in_bounds(position))
        val = self.board_config[position]
        piece = int(np.floor(abs(val)))
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
        piece = PieceType(int(np.floor(abs(val))))
        color = PieceColor.SILVER if val > 0 else PieceColor.RED

        val = abs(val)
        rotation = Rotation( int( 8 * (val % 1)))

        return piece, color, rotation

    def is_empty(self, position):
        val = self.board_config[position]
        return val == 0

    def get_next_moves(self):
        new_boards = []
        # TODO: don't move Pharoah/Anubis in early game since it doesn't really help

        piece_positions = self.get_piece_positions(filter_by_color=True)
        for position in piece_positions:
            piece_type, color, _ = self.get_piece_properties(position)

            moves = get_piece_from_piece_type(piece_type).get_moves(self, position)

            new_boards.extend([self.make_move(position, move) for move in moves])

        return new_boards

    def get_piece_positions(self, filter_by_color=False):
        B = self.board_config
        if filter_by_color:
            B = B < 0 if self.next_turn == PieceColor.RED else B > 0
        pieces_idxs = np.nonzero(B)

        positions = []

        for i in range(np.shape(pieces_idxs)[1]):
            positions.append((pieces_idxs[0][i], pieces_idxs[1][i]))
        
        return positions

        
            




