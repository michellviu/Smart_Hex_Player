import random
from hex_board import HexBoard
from minimax_player import MinimaxPlayer
from random_player import RandomPlayer

def play_game(sizeB=5, starting_player=1) -> tuple[list[list[int]], int]:
    """
    Simula un juego entre MinimaxPlayer y RandomPlayer.

    Args:
        size (int): Tamaño del tablero (NxN).
        starting_player (int): Jugador que comienza (1 o 2).

    Returns:
        tuple[list[list[int]], int]: El estado final del tablero y el jugador ganador (1 o 2, o 0 si es empate).
    """
    # Crear un tablero de tamaño `size`
    game = HexBoard(size=sizeB)

    # Crear un jugador Minimax y un jugador aleatorio
    minimax_player = MinimaxPlayer(player_id=1)
    random_player = RandomPlayer(player_id=2)

    # Inicializar el jugador actual según el jugador que comienza
    current_player = minimax_player if starting_player == 1 else random_player

    # Bucle para jugar el juego
    while True:
        # Obtener el movimiento del jugador actual
        move = current_player.play(game, max_time=2.0)

        # Verificar si hay movimientos válidos
        if move is None:
            return game.board, 0  # Empate

        # Realizar el movimiento en el tablero
        game.place_piece(move[0], move[1], current_player.player_id)

        # Verificar si el jugador actual ha ganado
        if game.check_connection(current_player.player_id):
            return game.board, current_player.player_id  # Retornar el tablero y el ganador

        # Cambiar al siguiente jugador
        current_player = minimax_player if current_player == random_player else random_player


def play_multiple_games(num_games=100, size=5):
    """
    Juega múltiples partidas entre MinimaxPlayer y RandomPlayer, alternando quién comienza.

    Args:
        num_games (int): Número de partidas a jugar.
        size (int): Tamaño del tablero (NxN).

    Returns:
        None
    """
    results = {1: 0, 2: 0, 0: 0}  # Contador de victorias para cada jugador y empates

    for i in range(num_games):
        # Elegir aleatoriamente quién comienza (1 o 2)
        starting= random.choice([1, 2])

        # Jugar una partida
        final_board, winner = play_game(sizeB=size, starting_player=starting)

        # Actualizar los resultados
        results[winner] += 1

        # Imprimir el estado final del tablero
        print(f"Partida {i + 1}:")
        for row in final_board:
            print(row)
        print(f"Ganador: {'Jugador 1' if winner == 1 else 'Jugador 2' if winner == 2 else 'Empate'}\n")

    # Imprimir el resumen de resultados
    print("Resumen de resultados:")
    print(f"Jugador 1 ganó {results[1]} partidas.")
    print(f"Jugador 2 ganó {results[2]} partidas.")
    print(f"Empates: {results[0]} partidas.")

# Ejecutar múltiples partidas
if __name__ == "__main__":
    play_multiple_games(num_games=100, size=5)