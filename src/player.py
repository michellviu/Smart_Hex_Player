import time
from hex_board import HexBoard
from collections import deque

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard, max_time: float) -> tuple:
        raise NotImplementedError("¡Implementa este método!")
    
    

