def find_pointing_line_region(board):
    for region_start_r in range(0, 9, 3):
        for region_start_c in range(0, 9, 3):
            region = [(region_start_r + i, region_start_c + j) for i in range(3) for j in range(3)]
            for digit in range(1, 10):
                locations = [(r, c) for (r, c) in region if digit in board.candidates[r][c]]
                if len(locations) >= 2:
                    rows = {r for r, _ in locations}
                    cols = {c for _, c in locations}
                    if len(rows) == 1:
                        row = next(iter(rows))
                        affected = [(row, c) for c in range(9) if (row, c) not in region and digit in board.candidates[row][c]]
                        if affected:
                            return f"Intersección región/fila: eliminar {digit} de {affected}"
                    if len(cols) == 1:
                        col = next(iter(cols))
                        affected = [(r, col) for r in range(9) if (r, col) not in region and digit in board.candidates[r][col]]
                        if affected:
                            return f"Intersección región/columna: eliminar {digit} de {affected}"
    return None