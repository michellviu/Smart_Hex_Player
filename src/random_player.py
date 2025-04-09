import random
from hex_board import HexBoard
from player import Player

class RandomPlayer(Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)

    def play(self, game: HexBoard, max_time : float) -> tuple[int, int]:
        
        possible_moves = game.get_possible_moves()
        return random.choice(possible_moves) if possible_moves else None