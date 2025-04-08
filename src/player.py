from hex_board import HexBoard
class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard) -> tuple:
        raise NotImplementedError("¡Implementa este método!")
    
    

class MinimaxPlayer(Player):
    
    def __init__(self, player_id: int):
        super().__init__(player_id)
    
    def play(self, game: HexBoard) -> tuple:
        # Llamar al método minimax con una profundidad inicial, alpha y beta
        _, best_move = self.minimax(game, depth=3, alpha=-float("inf"), beta=float("inf"), maximizing_player=True)
        # Devolver el mejor movimiento encontrado
        return best_move
    
   
    def get_boxes(self,game: HexBoard,player_id: int) -> list:
        """Devuelve una lista de cajas (fila, columna) para el jugador dado."""
        boxes = []
        for row in range(game.size):
            for col in range(game.size):
                if game.board[row][col] == player_id:
                    boxes.append((row, col))
        return boxes
    

    def get_neighbors(self,row: int, col: int, game: HexBoard) -> list:
        """Devuelve una lista de vecinos (fila, columna) para la posición dada."""

        neighbors = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, -1)]

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < game.size and 0 <= nc < game.size:
                neighbors.append((nr, nc))
                
        return neighbors
    
    
    def evaluate_board(self,game: HexBoard, player_id) -> int:
      
        visited = set()
        connected_components = 0
        descubierto = [[False for _ in range(len(game.board))] for _ in range(len(game.board))]
        boxes = self.get_boxes(game, player_id)
        
        for row, col in boxes:
            if (row, col) not in visited:
                stack = [(row, col)]
                connected_components += 1
                while stack:
                    r, c = stack.pop()
                    if (r, c) not in visited:
                        visited.add((r, c))
                        for nr, nc in self.get_neighbors(r, c, game):
                            if not descubierto[nr][nc] and game.board[nr][nc] == player_id:
                                stack.append((nr, nc))
                                descubierto[nr][nc] = True
                               
                                
        return  len(boxes)/connected_components


    def minimax(self, game: HexBoard, depth: int, alpha: float, beta: float, maximizing_player: bool) -> tuple[int, tuple[int, int]]:
       
        # Verificar si se alcanza una condición terminal o la profundidad máxima
        if depth == 0 or game.check_connection(self.player_id) or game.check_connection(3 - self.player_id):
            return self.evaluate_board(game), None

        best_move = None

        if maximizing_player:
            max_eval = -float("inf")
            for move in game.get_possible_moves():
                # Clonar el tablero y realizar el movimiento
                cloned_game = game.clone()
                cloned_game.place_piece(move[0], move[1], self.player_id)

                # Llamada recursiva para el jugador minimizador
                eval, _ = self.minimax(cloned_game, depth - 1, alpha, beta, False)

                # Actualizar el mejor movimiento y la evaluación máxima
                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                # Actualizar alfa y realizar poda
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval, best_move

        else:
            min_eval = float("inf")
            for move in game.get_possible_moves():
                # Clonar el tablero y realizar el movimiento
                cloned_game = game.clone()
                cloned_game.place_piece(move[0], move[1], 3 - self.player_id)

                # Llamada recursiva para el jugador maximizador
                eval, _ = self.minimax(cloned_game, depth - 1, alpha, beta, True)

                # Actualizar el mejor movimiento y la evaluación mínima
                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                # Actualizar beta y realizar poda
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval, best_move




