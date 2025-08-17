
def get_all_units():
    units = []
    for i in range(9):
        units.append([(i, j) for j in range(9)])  # filas
        units.append([(j, i) for j in range(9)])  # columnas
    for r in range(0, 9, 3):
        for c in range(0, 9, 3):
            units.append([(r + i, c + j) for i in range(3) for j in range(3)])
    return units


def find_naked_single(board):
    for r in range(9):
        for c in range(9):
            if board.grid[r][c] == 0 and len(board.candidates[r][c]) == 1:
                value = next(iter(board.candidates[r][c]))
                return f"Naked Single: colocar {value} en columna {chr(c+65)}, fila {r+1}"
    return None


def find_hidden_single(board):
    for unit in get_all_units():
        for digit in range(1, 10):
            places = [(r, c) for (r, c) in unit if digit in board.candidates[r][c]]
            if len(places) == 1:
                r, c = places[0]
                return f"Hidden Single: colocar {digit} en columna {chr(c+65)}, fila {r+1}"
    return None


def find_naked_pair(board):
    for unit in get_all_units():
        candidate_map = {}
        for (r, c) in unit:
            if board.grid[r][c] == 0 and len(board.candidates[r][c]) == 2:
                key = tuple(sorted(board.candidates[r][c]))
                candidate_map.setdefault(key, []).append((r, c))
        for candidates, positions in candidate_map.items():
            if len(positions) == 2:
                return f"Naked Pair {candidates} en {positions}"
    return None
