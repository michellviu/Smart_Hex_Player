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
        raise NotImplementedError("¡Implementa este método!")
    
    
    def get_boxes(game: HexBoard,player_id: int) -> list:
        """Devuelve una lista de cajas (fila, columna) para el jugador dado."""
        boxes = []
        for row in range(game.size):
            for col in range(game.size):
                if game.board[row][col] == player_id:
                    boxes.append((row, col))
        return boxes
    
    
    def get_neighbors(self, row: int, col: int, game: HexBoard) -> list:
        """Devuelve una lista de vecinos (fila, columna) para la posición dada."""
        directions_even = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]  # Vecinos para filas pares
        directions_odd = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]  # Vecinos para filas impares

        neighbors = []
        directions = directions_even if row % 2 == 0 else directions_odd

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < game.size and 0 <= nc < game.size:
                neighbors.append((nr, nc))
                
        return neighbors
    
    
    def count_connected(self,game, player_id) -> int:
      
        visited = set()
        connected_count = 0
        descubierto = [[False for _ in range(len(game))] for _ in range(len(game))]
        boxes = self.get_boxes(game, player_id)
        
        for row, col in boxes:
            if (row, col) not in visited:
                stack = [(row, col)]
                while stack:
                    r, c = stack.pop()
                    if (r, c) not in visited:
                        visited.add((r, c))
                        for nr, nc in self.get_neighbors(r, c, game):
                            if not descubierto[nr][nc] and game[nr][nc] == player_id:
                                stack.append((nr, nc))
                                descubierto[nr][nc] = True
                                connected_count += 1
                                
        return connected_count
    

    # def evaluate_board(self, game: HexBoard) -> int:
    #     """Heuristic to evaluate the board state."""
    #     score = 0
        
    #     boxes = self.get_boxes(game, self.player_id)
    #     mask = [[False for _ in range(game.size)] for _ in range(game.size)]
    #     queue = queue()

        