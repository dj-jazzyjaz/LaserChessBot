from game_tree import GameTree
from pieces import PieceColor, PieceType, Rotation, get_piece_from_piece_type
from board import Board
import numpy as np
import visualizer

"""
board_config =  np.zeros((8, 10))
board_config[4, 4] = Board.get_encoding(PieceType.PHAROAH, PieceColor.SILVER, Rotation.N)
board_config[1, 1] = Board.get_encoding(PieceType.ANUBIS, PieceColor.SILVER, Rotation.W)
board_config[2, 2] = Board.get_encoding(PieceType.PYRAMID, PieceColor.SILVER, Rotation.NE)
board_config[3, 3] = Board.get_encoding(PieceType.SCARAB, PieceColor.SILVER, Rotation.NE)
board_config[0, 0] = Board.get_encoding(PieceType.SPHINX, PieceColor.SILVER, Rotation.S)
b = Board(board_config, [], PieceColor.SILVER)
moves = b.get_next_moves()
"""

def initialize_classic_board():
    # row, col, piece, color, rotation
    config = [
        (0, 0, PieceType.SPHINX, PieceColor.RED, Rotation.S),
        (0, 4, PieceType.ANUBIS, PieceColor.RED, Rotation.S),
        (0, 5, PieceType.PHAROAH, PieceColor.RED, Rotation.S),
        (0, 6, PieceType.ANUBIS, PieceColor.RED, Rotation.S),
        (0, 7, PieceType.PYRAMID, PieceColor.RED, Rotation.SE),
        (1, 2, PieceType.PYRAMID, PieceColor.RED, Rotation.SW),
        (3, 0, PieceType.PYRAMID, PieceColor.RED, Rotation.NE),
        (3, 4, PieceType.SCARAB, PieceColor.RED, Rotation.NE),
        (3, 5, PieceType.SCARAB, PieceColor.RED, Rotation.NW),
        (3, 7, PieceType.PYRAMID, PieceColor.RED, Rotation.SE),
        (4, 0, PieceType.PYRAMID, PieceColor.RED, Rotation.SE),
        (4, 7, PieceType.PYRAMID, PieceColor.RED, Rotation.NE),
        (5, 6, PieceType.PYRAMID, PieceColor.RED, Rotation.SE),
        (7, 9, PieceType.SPHINX, PieceColor.SILVER, Rotation.N),
        (7, 5, PieceType.ANUBIS, PieceColor.SILVER, Rotation.N),
        (7, 4, PieceType.PHAROAH, PieceColor.SILVER, Rotation.N),
        (7, 3, PieceType.ANUBIS, PieceColor.SILVER, Rotation.N),
        (7, 2, PieceType.PYRAMID, PieceColor.SILVER, Rotation.NW),
        (6, 7, PieceType.PYRAMID, PieceColor.SILVER, Rotation.SW),
        (4, 9, PieceType.PYRAMID, PieceColor.SILVER, Rotation.SW),
        (4, 5, PieceType.SCARAB, PieceColor.SILVER, Rotation.NE),
        (4, 4, PieceType.SCARAB, PieceColor.SILVER, Rotation.NW),
        (4, 2, PieceType.PYRAMID, PieceColor.SILVER, Rotation.NW),
        (3, 9, PieceType.PYRAMID, PieceColor.SILVER, Rotation.NW),
        (3, 2, PieceType.PYRAMID, PieceColor.SILVER, Rotation.SW),
        (2, 3, PieceType.PYRAMID, PieceColor.SILVER, Rotation.SE),
    ]
    return Board.from_config_list(config) 

b = initialize_classic_board()

"""
next_moves = b.get_next_moves()

position = (0, 7)
piece_type = b.get_piece(position)

moves = get_piece_from_piece_type(piece_type).get_moves(b, position)


print(moves)
new_b, eliminated_piece, eliminated_color = b.make_move(position, moves[0])
visualizer.show_board(new_b)
"""

game_tree = GameTree()

# print(game_tree.score_board(b))

game_tree.build_tree(b)