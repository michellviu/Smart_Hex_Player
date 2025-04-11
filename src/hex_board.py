class HexBoard:
    
        def __init__(self, size: int):
            self.size = size  # Tamaño N del tablero (NxN)
            self.board = [[0 for _ in range(size)] for _ in range(size)]  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)
            self.ds = [-1] * (size * size + 4)
            
        def clone(self) -> "HexBoard":
            """
            Devuelve una copia del tablero actual.
            """
            new_board = HexBoard(self.size)
            new_board.board = [row[:] for row in self.board]  # Copia profunda de la matriz del tablero
            new_board.ds = self.ds[:]  # Copia del arreglo Union-Find
            return new_board

        def place_piece(self, row: int, col: int, player_id: int) -> bool:
            """
            Coloca una ficha si la casilla está vacía y realiza las uniones necesarias.

            Args:
                row (int): Fila de la celda.
                col (int): Columna de la celda.
                player_id (int): Identificador del jugador (1 o 2).

            Returns:
                bool: True si la ficha se colocó correctamente, False en caso contrario.
            """
            if 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == 0:
                # Colocar la ficha en el tablero
                self.board[row][col] = player_id

                # Obtener la posición lineal de la celda en el arreglo Union-Find
                pos = self.position(row, col)
                
                # Conectar la celda a los bordes virtuales si está en un borde del tablero
                if player_id == 1:  # Jugador 1 (bordes izquierdo y derecho)
                    if col == 0:
                        self.join(0, pos)  # Conectar al borde izquierdo
                    if col == self.size - 1:
                        self.join(1, pos)  # Conectar al borde derecho
                elif player_id == 2:  # Jugador 2 (bordes superior e inferior)
                    if row == 0:
                        self.join(2, pos)  # Conectar al borde superior
                    if row == self.size - 1:
                        self.join(3, pos)  # Conectar al borde inferior

                # Conectar la celda a sus vecinos adyacentes del mismo jugador
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == player_id:
                        neighbor_pos = self.position(nr, nc)
                        self.join(pos, neighbor_pos)

                return True
            return False

        def get_possible_moves(self) -> list[tuple[int, int]]:
            """
            Devuelve todas las casillas vacías como tuplas (fila, columna).

            Returns:
                list[tuple[int, int]]: Lista de posiciones vacías en el tablero.
            """
            return [(row, col) for row in range(self.size) for col in range(self.size) if self.board[row][col] == 0]
        
        def check_connection(self, player_id: int) -> bool:
            """
            Verifica si el jugador ha conectado sus dos lados opuestos.

            Args:
                player_id (int): El identificador del jugador (1 o 2).

            Returns:
                bool: True si el jugador ha conectado sus lados opuestos, False en caso contrario.
            """
            if player_id == 1:
                # Jugador 1 (conecta el lado izquierdo con el derecho)
                return self.root(0) == self.root(1)
            elif player_id == 2:
                # Jugador 2 (conecta el lado superior con el inferior)
                return self.root(2) == self.root(3)
            return False
        
        # Disjoint set

        def root(self, a):
            if self.ds[a] < 0:
                return a
            else:
                self.ds[a] = self.root(self.ds[a])
                return self.ds[a]

        def join(self, a, b):
            a, b = self.root(a), self.root(b)
            if a == b:
                return False
            if self.ds[a] < self.ds[b]:
                a, b = b, a
            self.ds[b] += self.ds[a]
            self.ds[a] = b
            return True

        def position(self, row: int, col: int) -> int:
            """
            Convierte las coordenadas (fila, columna) en una posición lineal en el arreglo Union-Find.

            Args:
                row (int): Fila de la celda.
                col (int): Columna de la celda.

            Returns:
                int: Posición lineal en el arreglo Union-Find.
            """
            return 4 + row * self.size + col

	    # End disjoint set
     
        def print_board(self):
            space = ""
            print(space , end="     ")
            for i in range(self.size):
                print(f"\033[31m{i}  \033[0m", end=" ")
            print("\n")
            for i in range(self.size):
                print(space , end=" ")
                print(f"\033[34m{i}  \033[0m",end=" ")
                for j in range(self.size):
                    if self.board[i][j] == 0:
                        print("⬜ ",end=" ")
                    if self.board[i][j] == 1:
                        print("🟥 ",end=" ")
                    if self.board[i][j] == 2:
                        print("🟦 ",end=" ")
                    if j == self.size -1:
                        print(f"\033[34m {i} \033[0m",end=" ")
                space += "  "
                print("\n")
            print(space,end="    ")
            for i in range(self.size):
                print(f"\033[31m{i}  \033[0m", end=" ")