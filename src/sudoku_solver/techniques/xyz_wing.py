
def shares_unit(cell1, cell2):
    r1, c1 = cell1
    r2, c2 = cell2
    same_row = r1 == r2
    same_col = c1 == c2
    same_box = (r1 // 3 == r2 // 3) and (c1 // 3 == c2 // 3)
    return same_row or same_col or same_box


def get_shared_peers(cell1, cell2):
    r1, c1 = cell1
    r2, c2 = cell2
    shared = []
    for r in range(9):
        for c in range(9):
            if (r, c) != cell1 and (r, c) != cell2:
                if shares_unit((r, c), cell1) and shares_unit((r, c), cell2):
                    shared.append((r, c))
    return shared

def find_xyz_wing(board):
    # Buscar todas las celdas con exactamente 3 candidatos
    triple_value_cells = [(r, c, tuple(board.candidates[r][c])) for r in range(9) for c in range(9)
                          if board.grid[r][c] == 0 and len(board.candidates[r][c]) == 3]

    # Buscar alas con 2 candidatos que se crucen con la pivote de 3
    for r1, c1, triple in triple_value_cells:
        triple_set = set(triple)
        for (r2, c2), pair2 in bivalue_cells(board):
            if not shares_unit((r1, c1), (r2, c2)):
                continue
            if set(pair2).issubset(triple_set):
                for (r3, c3), pair3 in bivalue_cells(board):
                    if (r3, c3) in [(r1, c1), (r2, c2)] or not shares_unit((r1, c1), (r3, c3)):
                        continue
                    if set(pair3).issubset(triple_set):
                        # Intersección de influencia entre las alas
                        shared = get_shared_peers((r2, c2), (r3, c3))
                        if shared:
                            z_candidates = triple_set & set(pair2) & set(pair3)
                            if len(z_candidates) == 1:
                                z = next(iter(z_candidates))
                                return f"XYZ-Wing: pivote ({r1+1},{chr(c1+65)}) con {triple}, alas ({r2+1},{chr(c2+65)}) y ({r3+1},{chr(c3+65)}), eliminar {z} de {shared}"
    return None


def bivalue_cells(board):
    return [((r, c), tuple(board.candidates[r][c])) for r in range(9) for c in range(9)
            if board.grid[r][c] == 0 and len(board.candidates[r][c]) == 2]
