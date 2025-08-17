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

def find_naked_subset(board, size=3):
    for unit in get_all_units():
        cells = [(r, c) for (r, c) in unit if board.grid[r][c] == 0 and 2 <= len(board.candidates[r][c]) <= size]
        for combo in combinations(cells, size):
            union = set()
            for (r, c) in combo:
                union |= board.candidates[r][c]
            if len(union) == size:
                eliminables = []
                for (r, c) in unit:
                    if (r, c) not in combo and any(x in board.candidates[r][c] for x in union):
                        eliminables.append((r, c))
                if eliminables:
                    label = {2: "Par", 3: "Trío", 4: "Cuarteto"}.get(size, f"{size}-subset")
                    return f"{label} desnudo en {combo}, eliminar {union} de {eliminables}"
    return None