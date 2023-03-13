from pieces import PieceColor, PieceType, Rotation
from board import Board
import numpy as np

board_config =  np.zeros((8, 10))
board_config[4, 4] = Board.get_encoding(PieceType.PHAROAH, PieceColor.SILVER, Rotation.N)
board_config[1, 1] = Board.get_encoding(PieceType.ANUBIS, PieceColor.SILVER, Rotation.W)
board_config[2, 2] = Board.get_encoding(PieceType.PYRAMID, PieceColor.SILVER, Rotation.NE)
board_config[3, 3] = Board.get_encoding(PieceType.SCARAB, PieceColor.SILVER, Rotation.NE)
board_config[0, 0] = Board.get_encoding(PieceType.SPHINX, PieceColor.SILVER, Rotation.S)
b = Board(board_config, [], PieceColor.SILVER)
moves = b.get_next_moves()

