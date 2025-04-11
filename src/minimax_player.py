import time
import heapq
import random
from hex_board import HexBoard
from player import Player


class MinimaxPlayer(Player):
    
    def __init__(self, player_id: int, depth: int = 4):
        super().__init__(player_id)
        self.best_eval = -float("inf")
        self.best_move_global = None
        self.depth = depth
    
    def play(self, game: HexBoard, max_time: float=10.0) -> tuple:
        # Llamar al método minimax con una profundidad inicial, alpha y beta
        start_time = time.time()
        self.best_eval = -float("inf")
        self.best_move_global = None
        mejor_movimiento = None
        
        profundidad = 1
        while MinimaxPlayer.tiempo_restante(start_time, max_time):
            _, best_move = self.minimax(game, profundidad, -float("inf"), float("inf"), True,start_time,max_time)
            if MinimaxPlayer.tiempo_restante(start_time, max_time):
                mejor_movimiento = best_move
                profundidad += 1
            else:
                break
        if mejor_movimiento is None:
            return random.choice(game.get_possible_moves())
            #print(f"Mejor movimiento encontrado: {best_move} con evaluación: {self.best_eval}")
        return mejor_movimiento
    
    
    def ordenar_movimientos(game: HexBoard, jugador):
        def score(move):
            centro = game.size // 2
            return -((move[0] - centro) ** 2 + (move[1] - centro) ** 2)  # más cerca del centro = mejor
        return sorted(game.get_possible_moves(), key=score)
    
    def tiempo_restante(inicio, tiempo_maximo):
        return time.time() - inicio < tiempo_maximo

    def get_boxes(game: HexBoard,player_id: int):
        """Devuelve una lista de cajas (fila, columna) para el jugador dado."""
        boxes = []
        for row in range(game.size):
            for col in range(game.size):
                if game.board[row][col] == player_id:
                    boxes.append((row, col))
        return boxes
        
    
    def get_neighbors(row: int, col: int, game: HexBoard):
        """Devuelve una lista de vecinos (fila, columna) para la posición dada."""

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, -1)]

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < game.size and 0 <= nc < game.size:
                yield nr, nc
    
    
    def heuristic_1(game: HexBoard, player_id):
        
            visited = set()
            connected_components = 0
            descubierto = [[False for _ in range(len(game.board))] for _ in range(len(game.board))]
            boxes = MinimaxPlayer.get_boxes(game, player_id)
            
            for row, col in boxes:
                if (row, col) not in visited:
                    stack = [(row, col)]
                    connected_components += 1
                    while stack:
                        r, c = stack.pop()
                        if (r, c) not in visited:
                            visited.add((r, c))
                            for nr, nc in MinimaxPlayer.get_neighbors(r, c, game):
                                if not descubierto[nr][nc] and game.board[nr][nc] == player_id:
                                    stack.append((nr, nc))
                                    descubierto[nr][nc] = True
                                    
            return 0 if connected_components==0 else len(boxes)/connected_components
        
    def evaluar_expansion(game:HexBoard, jugador_id):
        n = len(game.board)
        centro = n // 2
        puntuacion = 0

        for i in range(n):
            for j in range(n):
                if game.board[i][j] == jugador_id:
                    for x, y in MinimaxPlayer.get_neighbors(i, j, game):
                        if game.board[x][y] == 0:
                            distancia = abs(x - centro) + abs(y - centro)
                            puntuacion += 1 / (1 + distancia)  # más cerca del centro = mayor puntuación

        return puntuacion
        
    
    def evaluate_board(self, game: HexBoard):
        # Si el jugador actual ha ganado, retorna un valor muy alto
        if game.check_connection(self.player_id):
            return 1000
        # Si el oponente ha ganado, retorna un valor muy bajo
        if game.check_connection(3 - self.player_id):
            return -1000
        
        # Heurística 1: Basada en la cantidad de componentes conectados
        h_componentes = MinimaxPlayer.heuristic_1(game, self.player_id)
        h_expansion = MinimaxPlayer.evaluar_expansion(game, self.player_id)
        # Heurística 2: Basada en la distancia más corta hacia la victoria
        player_distance = MinimaxPlayer.fichas_faltantes_hex(game.board, self.player_id)
        opponent_distance = MinimaxPlayer.fichas_faltantes_hex(game.board, 3 - self.player_id)
                           
        heuristic_2 = (opponent_distance - player_distance)

        # Combinar ambas heurísticas con pesos
        weight_1 = 1.0  # Peso para la heurística de componentes conectados
        weight_2 = 2 # Peso para la heurística de distancia
        weight_3 = 1.5  # Peso para el control del centro
        # weight_1*heuristic_1 +
        return weight_1* h_componentes + weight_2* heuristic_2 + weight_3*h_expansion

    def minimax(self, game: HexBoard, depth: int, alpha: float, beta: float, maximizing_player: bool, start_time: float, max_time: float) -> tuple[int, tuple[int, int]]:
        """
        Implementación del algoritmo Minimax con poda alfa-beta y control de tiempo.

        Args:
            game (HexBoard): El estado actual del tablero.
            depth (int): La profundidad máxima de búsqueda.
            alpha (float): El valor alfa para la poda.
            beta (float): El valor beta para la poda.
            maximizing_player (bool): True si es el turno del jugador actual, False si es el turno del oponente.
            start_time (float): Tiempo de inicio del turno del jugador.
            max_time (float): Tiempo máximo permitido para el turno (en segundos).

        Returns:
            tuple[int, tuple[int, int]]: La evaluación del tablero y el mejor movimiento (fila, columna).
        """

        # Verificar si se alcanzó el tiempo límite
        if time.time() - start_time > max_time:
            return self.best_eval, self.best_move_global
        
          # Verificar si se alcanza una condición terminal o la profundidad máxima
        if depth == 0 or game.check_connection(self.player_id) or game.check_connection(3 - self.player_id):
            return self.evaluate_board(game), None

        best_move = None

        if maximizing_player:
            max_eval = -float("inf")
            for move in MinimaxPlayer.ordenar_movimientos(game, self.player_id if maximizing_player else 3 - self.player_id):
                # Verificar si se alcanzó el tiempo límite
                if time.time() - start_time > max_time:
                    return self.best_eval, self.best_move_global

                # Clonar el tablero y realizar el movimiento
                cloned_game = game.clone()
                cloned_game.place_piece(move[0], move[1], self.player_id)

                # Llamada recursiva para el jugador minimizador
                eval, _ = self.minimax(cloned_game, depth - 1, alpha, beta, False, start_time, max_time)

                # Actualizar el mejor movimiento y la evaluación máxima
                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                    # Actualizar las variables globales
                    self.best_eval = max_eval
                    self.best_move_global = best_move

                # Actualizar alfa y realizar poda
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval, best_move

        else:
            min_eval = float("inf")
            for move in MinimaxPlayer.ordenar_movimientos(game, self.player_id if maximizing_player else 3 - self.player_id):
                # Verificar si se alcanzó el tiempo límite
                if time.time() - start_time > max_time:
                    return self.best_eval, self.best_move_global

                # Clonar el tablero y realizar el movimiento
                cloned_game = game.clone()
                cloned_game.place_piece(move[0], move[1], 3 - self.player_id)

                # Llamada recursiva para el jugador maximizador
                eval, _ = self.minimax(cloned_game, depth - 1, alpha, beta, True, start_time, max_time)

                # Actualizar el mejor movimiento y la evaluación mínima
                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                    # Actualizar las variables globales
                    self.best_eval = min_eval
                    self.best_move_global = best_move
                # Actualizar beta y realizar poda
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            
            return min_eval, best_move


    def fichas_faltantes_hex(tablero, jugador):
        n = len(tablero)
        # Direcciones de vecinos en HEX (6 vecinos)
        direcciones = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]
        
        if jugador == 1:
            fuente = [(x, 0) for x in range(n)]  
            es_receptor = lambda x, y: y == n - 1
        else:
            fuente = [(0, y) for y in range(n)]
            es_receptor = lambda x, y: x == n - 1
        
        distancia = [[float('inf')] * n for _ in range(n)]
        heap = []
        
        for x, y in fuente:
            if tablero[x][y] == jugador:
                distancia[x][y] = 0
                heapq.heappush(heap, (0, x, y))
            elif tablero[x][y] == 0:
                distancia[x][y] = 1
                heapq.heappush(heap, (1, x, y))
            # Si es del oponente, no se agrega (distancia permanece infinito)
        
        while heap:
            d, x, y = heapq.heappop(heap)
            if es_receptor(x, y):
                return d  # Llegamos al sumidero
            
            for dx, dy in direcciones:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n:
                    costo = 0 if tablero[nx][ny] == jugador else 1 if tablero[nx][ny] == 0 else float('inf')
                    nueva_distancia = d + costo
                    if nueva_distancia < distancia[nx][ny]:
                        distancia[nx][ny] = nueva_distancia
                        heapq.heappush(heap, (nueva_distancia, nx, ny))
        
        return n*n  # No hay camino posible

    