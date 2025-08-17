from itertools import combinations

def find_fish_patterns(board, fish_size=2):
    """
    Generaliza X-Wing (2), Swordfish (3) y Medusa (4)
    Busca patrones en filas o columnas donde un candidato aparece en exactamente fish_size columnas (o filas)
    """
    for digit in range(1, 10):
        # Buscar en filas
        row_cands = []
        for r in range(9):
            cols = [c for c in range(9) if digit in board.candidates[r][c]]
            if 1 <= len(cols) <= fish_size:
                row_cands.append((r, cols))
        for row_combo in combinations(row_cands, fish_size):
            all_cols = set(c for _, cols in row_combo for c in cols)
            if len(all_cols) == fish_size:
                # Eliminación en columnas fuera de las filas seleccionadas
                eliminations = []
                for col in all_cols:
                    for row in range(9):
                        if row not in [r for r, _ in row_combo] and digit in board.candidates[row][col]:
                            eliminations.append((row, col))
                if eliminations:
                    name = {2: "X-Wing", 3: "Swordfish", 4: "Medusa"}.get(fish_size, f"{fish_size}-Fish")
                    rows_used = [r for r, _ in row_combo]
                    return f"{name} fila/columna con candidato {digit}, en filas {rows_used} y columnas {sorted(all_cols)} → eliminar de {eliminations}"

        # Buscar en columnas
        col_cands = []
        for c in range(9):
            rows = [r for r in range(9) if digit in board.candidates[r][c]]
            if 1 <= len(rows) <= fish_size:
                col_cands.append((c, rows))
        for col_combo in combinations(col_cands, fish_size):
            all_rows = set(r for _, rows in col_combo for r in rows)
            if len(all_rows) == fish_size:
                eliminations = []
                for row in all_rows:
                    for col in range(9):
                        if col not in [c for c, _ in col_combo] and digit in board.candidates[row][col]:
                            eliminations.append((row, col))
                if eliminations:
                    name = {2: "X-Wing", 3: "Swordfish", 4: "Medusa"}.get(fish_size, f"{fish_size}-Fish")
                    cols_used = [c for c, _ in col_combo]
                    return f"{name} columna/fila con candidato {digit}, en columnas {cols_used} y filas {sorted(all_rows)} → eliminar de {eliminations}"
    return None
