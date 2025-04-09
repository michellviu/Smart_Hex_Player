# **MinimaxPlayer: Implementación del Jugador Basado en Minimax**

Este archivo contiene la implementación de un jugador para el juego de Hex basado en el algoritmo **Minimax con poda alfa-beta**.

---

## **Clases**

### **`Player`**
Clase base para los jugadores. Define la estructura básica que deben seguir los jugadores en el juego de Hex.

#### **Métodos**
- **`__init__(self, player_id: int)`**:
  - Inicializa el jugador con un identificador único (`player_id`), que puede ser `1` o `2`.

- **`play(self, board: HexBoard, max_time: float) -> tuple`**:
  - Define cómo el jugador decide su movimiento en el tablero.

---

### **`MinimaxPlayer`**
Clase que implementa un jugador basado en el algoritmo **Minimax con poda alfa-beta**.

#### **Métodos**
- **`__init__(self, player_id: int)`**:
  - Inicializa el jugador con un identificador único (`player_id`).

- **`play(self, game: HexBoard, max_time: float) -> tuple[int, int]`**:
  - Decide el mejor movimiento utilizando el algoritmo Minimax.
  - Controla el tiempo máximo permitido para calcular la jugada (`max_time`).

- **`get_boxes(self, game: HexBoard, player_id: int) -> list[tuple[int, int]]`**:
  - Devuelve una lista de todas las casillas ocupadas por el jugador (`player_id`) en el tablero.

- **`get_neighbors(self, row: int, col: int, game: HexBoard) -> list[tuple[int, int]]`**:
  - Devuelve una lista de las celdas vecinas de una posición `(row, col)` en el tablero.


- **`evaluate_board(self, game: HexBoard) -> int`**:
  - Evalúa el estado actual del tablero para el jugador.
  - Utiliza una heurística basada en el número de componentes conectados y las casillas ocupadas por el jugador.
  - Retorna un valor numérico que representa la calidad del estado del tablero.

- **`minimax(self, game: HexBoard, depth: int, alpha: float, beta: float, maximizing_player: bool, start_time: float, max_time: float) -> tuple[int, tuple[int, int]]`**:
  - Implementa el algoritmo Minimax con poda alfa-beta y control de tiempo.
  - Explora recursivamente los posibles movimientos hasta una profundidad máxima (`depth`) o hasta que se alcance el tiempo límite (`max_time`).
  - Retorna la evaluación del tablero y el mejor movimiento encontrado.

---

## **Estrategia del Jugador**

El jugador `MinimaxPlayer` utiliza el algoritmo **Minimax con poda alfa-beta** para tomar decisiones estratégicas en el juego de Hex. A continuación, se describe la estrategia en detalle:

### **1. Evaluación del Tablero**
La función `evaluate_board` evalúa el estado del tablero para el jugador actual. La heurística utilizada considera:
- **Casillas ocupadas (`boxes`)**:
  - Se cuentan todas las casillas ocupadas por el jugador actual.
- **Componentes conectados (`connected_components`)**:
  - Se calcula el número de grupos de casillas conectadas del jugador actual.
- **Fórmula de evaluación**:
  ```python
  len(boxes) / connected_components
  ```

### **2. Algoritmo Minimax**
El algoritmo Minimax explora recursivamente los posibles movimientos en el tablero para encontrar el mejor movimiento. Se utiliza poda alfa-beta para reducir el número de nodos explorados y mejorar la eficiencia.

#### **Características del Minimax**:
- **Maximizador y minimizador**:
  - El jugador actual intenta maximizar su evaluación del tablero.
  - El oponente intenta minimizar la evaluación del tablero.
- **Control de tiempo**:
  - Si el tiempo transcurrido excede el límite (`max_time`), el algoritmo devuelve el mejor movimiento encontrado hasta ese momento.
- **Condiciones de parada**:
  - Profundidad máxima alcanzada (`depth == 0`).
  - El jugador actual o el oponente ha ganado (`game.check_connection`).

### **3. Control de Tiempo**
El jugador respeta un tiempo máximo permitido para cada jugada (`max_time`). Si el tiempo límite se alcanza durante la ejecución del algoritmo Minimax:
- El algoritmo devuelve el mejor movimiento encontrado hasta ese momento.
- Esto asegura que el jugador siempre realice un movimiento dentro del tiempo permitido.

### **4. Vecinos y Conexiones**
El método `get_neighbors` identifica las celdas vecinas de una posición en el tablero. Esto es fundamental para:
- Evaluar las conexiones entre las casillas ocupadas por el jugador.
- Determinar los componentes conectados en el tablero.

---

