

from dataclasses import dataclass
from typing import List, Optional
from board import Board
from pieces import PieceColor, PieceType, get_piece_from_piece_type

piece_to_value = {
    PieceType.PYRAMID: 1,
    PieceType.PHAROAH: 1000,
    PieceType.SCARAB: 3,
    PieceType.ANUBIS: 2,
    PieceType.SPHINX: 0,
}

@dataclass
class GameNode:
    board: Board
    turn: PieceColor
    parent: "GameNode"
    children: Optional[List["GameNode"]]
    score: int
    depth: int

class GameTree:
    def __init__(self):
        pass

    def score_board(self, board):
        # Lower score is better for Red, higher score is better for Silver
        num_points = 0
        for position in board.get_piece_positions():
            piece_type, color, _ = board.get_piece_properties(position)
            if color == PieceColor.RED:
                num_points += piece_to_value[piece_type]
            else:
                num_points -= piece_to_value[piece_type]
        
        return num_points

    def build_tree(self, board):
        root = GameNode(board, PieceColor.RED, None, None, self.score_board(board), 0)

        self.build_tree_helper(root)


        
    def build_tree_helper(self, node):
        if node.depth == 5:
            return
        next_boards = node.board.get_next_moves()
        node.children = []
        
        for new_board in next_boards:
            score = self.score_board(new_board)
            new_node = GameNode(new_board, node.board.next_turn, node, None, score, node.depth + 1)
            node.children.append(new_node)

        children = node.children
        if node.turn == PieceColor.RED:
            children.sort(key=lambda x: x.score)
        else:
            children.sort(key=lambda x: x.score, reverse=True)
        
        for child in children[:5]:
            self.build_tree_helper(child)

        if node.turn == PieceColor.RED:
            node.score = max(child.score for child in children[:5])
        else:
            node.score = min(child.score for child in children[:5])

        if node.depth < 2:
            print(f"Completed search. Depth: {node.depth} Score: {node.score}")
    
