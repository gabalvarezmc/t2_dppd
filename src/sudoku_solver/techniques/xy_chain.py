import numpy as np
from itertools import combinations


class SudokuBoard:
    def __init__(self, grid):
        self.grid = np.array(grid)
        self.candidates = self.generate_candidates()

    def generate_candidates(self):
        candidates = [[set(range(1, 10)) if self.grid[r][c] == 0 else set()
                       for c in range(9)] for r in range(9)]
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] != 0:
                    self.eliminate_candidates(r, c, self.grid[r][c], candidates)
        return candidates

    def eliminate_candidates(self, row, col, value, candidates):
        for i in range(9):
            candidates[row][i].discard(value)
            candidates[i][col].discard(value)
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                candidates[r][c].discard(value)


def get_all_units():
    units = []
    for i in range(9):
        units.append([(i, j) for j in range(9)])  # filas
        units.append([(j, i) for j in range(9)])  # columnas
    for r in range(0, 9, 3):
        for c in range(0, 9, 3):
            units.append([(r + i, c + j) for i in range(3) for j in range(3)])
    return units


def shares_unit(cell1, cell2):
    r1, c1 = cell1
    r2, c2 = cell2
    same_row = r1 == r2
    same_col = c1 == c2
    same_box = (r1 // 3 == r2 // 3) and (c1 // 3 == c2 // 3)
    return same_row or same_col or same_box


def get_bivalue_cells(board):
    return [((r, c), tuple(board.candidates[r][c])) for r in range(9) for c in range(9)
            if board.grid[r][c] == 0 and len(board.candidates[r][c]) == 2]


def build_xy_chains(board):
    # Construir grafo donde nodos son celdas bivalue y aristas son pares conjugados
    edges = {}
    bivalue = get_bivalue_cells(board)
    for (r1, c1), (a, b) in bivalue:
        for (r2, c2), (x, y) in bivalue:
            if (r1, c1) == (r2, c2):
                continue
            if shares_unit((r1, c1), (r2, c2)):
                shared = set((a, b)).intersection((x, y))
                if len(shared) == 1:
                    edges.setdefault((r1, c1), []).append((r2, c2))
    return edges


def find_xy_chain(board):
    graph = build_xy_chains(board)
    bivalue = get_bivalue_cells(board)

    for (start, pair) in bivalue:
        visited = set()
        chain = []

        def dfs(path, values):
            current = path[-1]
            visited.add(current)
            if len(path) > 1 and values[0] == values[-1]:
                # Validar que extremos ven una misma casilla
                common_seen = []
                for r in range(9):
                    for c in range(9):
                        if board.grid[r][c] == 0 and values[0] in board.candidates[r][c]:
                            if shares_unit((r, c), path[0]) and shares_unit((r, c), path[-1]):
                                common_seen.append((r, c))
                if common_seen:
                    return f"Cadena XY entre {path[0]} y {path[-1]} con valor común {values[0]}, eliminarlo de {common_seen}"

            for neighbor in graph.get(current, []):
                if neighbor not in visited:
                    next_candidates = tuple(board.candidates[neighbor[0]][neighbor[1]])
                    if len(next_candidates) == 2:
                        shared = set(values[-1:]).intersection(next_candidates)
                        if shared:
                            other = next_candidates[0] if next_candidates[1] == shared.pop() else next_candidates[1]
                            result = dfs(path + [neighbor], values + [other])
                            if result:
                                return result
            visited.remove(current)
            return None

        result = dfs([start], list(pair))
        if result:
            return result
    return None
