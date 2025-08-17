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

def find_unique_rectangle(board):
    # Buscar pares de candidatos en 4 celdas que forman un rectángulo
    for r1 in range(8):
        for c1 in range(8):
            for r2 in range(r1 + 1, 9):
                for c2 in range(c1 + 1, 9):
                    rect_cells = [(r1, c1), (r1, c2), (r2, c1), (r2, c2)]
                    values = [board.candidates[r][c] for r, c in rect_cells]
                    if all(board.grid[r][c] == 0 and 2 <= len(vals) <= 3 for (r, c), vals in zip(rect_cells, values)):
                        # Buscar si tres celdas tienen el mismo par y la cuarta tiene extras
                        pairs = [v for v in values if len(v) == 2]
                        if len(pairs) < 2:
                            continue
                        base_pair = next(iter(pairs), None)
                        if all(p == base_pair for p in pairs if len(p) == 2):
                            for i, v in enumerate(values):
                                if len(v) > 2 and base_pair.issubset(v):
                                    extras = v - base_pair
                                    if extras:
                                        r, c = rect_cells[i]
                                        return f"Rectángulo de unicidad tipo 1: en ({r+1},{chr(c+65)}), eliminar {extras} para evitar solución múltiple"
    return None


