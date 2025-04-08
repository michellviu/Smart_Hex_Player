from player import MinimaxPlayer
from hex_board import HexBoard


game = HexBoard(size=4)  # Crea un tablero de 5x5

player = MinimaxPlayer(1)

game.board = [ 
    [1, 1, 0, 1],
    [0, 1, 0, 0],
    [0, 0, 2, 2],
    [0, 0, 2, 2]
]

# Probar el método count_connected para el jugador 1
connected_count_player_1 = player.evaluate_board(game, 1)
print(f"Jugador 1 - Evaluacion: {connected_count_player_1}")

# Probar el método count_connected para el jugador 2
connected_count_player_2 = player.evaluate_board(game, 2)
print(f"Jugador 2 - Evaluacion: {connected_count_player_2}")