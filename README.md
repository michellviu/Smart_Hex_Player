# **MinimaxPlayer: Implementación del Jugador Basado en Minimax**

Esta solución contiene la implementación de un jugador para el juego de Hex basado en el algoritmo **Minimax con poda alfa-beta**.

---

## **`MinimaxPlayer`**

Clase que implementa un jugador basado en el algoritmo **Minimax con poda alfa-beta**.

## 🎯 Estrategia General

El enfoque general del jugador se basa en:

- **Iterative Deepening**: Se inicia la búsqueda con una profundidad de 1 y se incrementa mientras el tiempo lo permita.

- **Ordenamiento de Movimientos**: Antes de explorar los movimientos, estos se ordenan heurísticamente para maximizar la eficiencia de la poda.

---

## ⚙️ Ordenamiento de Movimientos

Antes de evaluar cada movimiento posible, se utiliza un criterio de orden basado en la **distancia al centro del tablero**. La intuición es que las posiciones cercanas al centro tienen mayor potencial estratégico al estar más conectadas con múltiples rutas posibles.

```python
def ordenar_movimientos(game: HexBoard, jugador):
    def score(move):
        centro = game.size // 2
        return -((move[0] - centro) ** 2 + (move[1] - centro) ** 2)
    return sorted(game.get_possible_moves(), key=score)
```

Esto guía al algoritmo para que primero explore movimientos centrales.

---

## 🧠 Evaluación Heurística

La función de evaluación del estado del tablero se compone de tres heurísticas principales, combinadas con pesos configurables:

1. 🔗 Heurística de Conectividad

Evalúa la eficiencia de conexión entre piezas propias. Se calcula dividiendo la cantidad total de piezas del jugador por el número de componentes conectados que forman, penalizando distribuciones dispersas y premiando formaciones más cohesivas.

```python
heuristic_1 = piezas / componentes_conectados
```

2. 🚣️ Heurística de Distancia a la Victoria

Utiliza un algoritmo de búsqueda similar a Dijkstra para estimar el número mínimo de movimientos necesarios para conectar los lados del tablero. Se calcula tanto para el jugador como para el oponente, y se considera la diferencia entre ambos:

```python
heuristic_2 = distancia_oponente - distancia_jugador
```

Esto permite penalizar los movimientos en los que el oponente está más cerca del objetivo.

3. 🌱 Heurística de Expansión Ponderada

Evalúa el número de celdas vacías adyacentes a piezas propias, ponderadas por su cercanía al centro del tablero. Se asume que las posiciones centrales tienen mayor valor estratégico.

```python
puntaje += 1 / (1 + distancia_al_centro)
```

Esto incentiva al jugador a construir estructuras expansibles en regiones clave del tablero.

### ⚖️ Combinación de Heurísticas

Cada heurística se combina con un peso determinado para formar la evaluación total del tablero:

```python
evaluacion = (1.0 * h_conectividad) + (2.0 * h_distancia) + (1.5 * h_expansion)
```

Estos pesos pueden ser ajustados para modificar el comportamiento estratégico del jugador según se requiera.

---
