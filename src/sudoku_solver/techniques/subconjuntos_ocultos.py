from itertools import combinations

def get_all_units():
    units = []
    for i in range(9):
        units.append([(i, j) for j in range(9)])  # filas
        units.append([(j, i) for j in range(9)])  # columnas
    for r in range(0, 9, 3):
        for c in range(0, 9, 3):
            units.append([(r + i, c + j) for i in range(3) for j in range(3)])
    return units

def find_hidden_subset(board, size=2):
    for unit in get_all_units():
        # Mapeo de candidato a posiciones donde aparece
        candidate_positions = {digit: [] for digit in range(1, 10)}
        for r, c in unit:
            if board.grid[r][c] == 0:
                for digit in board.candidates[r][c]:
                    candidate_positions[digit].append((r, c))
        # Buscar combinaciones de dígitos
        for digits in combinations(range(1, 10), size):
            positions = [set(candidate_positions[d]) for d in digits]
            if all(1 <= len(pos) <= size for pos in positions):
                combined = set.union(*positions)
                if len(combined) == size:
                    eliminations = []
                    for r, c in combined:
                        to_remove = board.candidates[r][c] - set(digits)
                        if to_remove:
                            eliminations.append((r, c, to_remove))
                    if eliminations:
                        label = {2: "Par", 3: "Trío", 4: "Cuarteto"}.get(size, f"{size}-subset")
                        return f"{label} oculto en {combined} con candidatos {digits}, eliminar otros candidatos: {eliminations}"
    return None
