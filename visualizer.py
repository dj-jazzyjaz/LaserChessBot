import sys
# sys.path.append('/home/jasmine/.local/lib/python3.10/site-packages')

from game2dboard import Board
from pieces import PieceType, PieceColor, Rotation

def show_board(board):
    b = Board(8, 10)         # 8 rows, 10 columns, filled w/ None

    b.cell_size = 100       
    b.cell_color = "gray"
    #b.on_mouse_click = mouse_fn

    for r in range(8):
        for c in range(10):
            if not board.is_empty((r, c)):
                piece, color, rotation = board.get_piece_properties((r, c))
                
                piece_type_str = piece.name.lower()
                rotation_str = rotation.name.lower()
                img_name = f"{piece_type_str}_{rotation_str}"

                if color == PieceColor.SILVER:
                    img_name += "_s.png"
                else:
                    img_name += ".png"

                b[r][c] = img_name
    
    b.show()