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

def find_xy_wing(board):
    # Buscar todas las casillas con exactamente 2 candidatos
    bivalue_cells = [(r, c, tuple(board.candidates[r][c])) for r in range(9) for c in range(9)
                     if board.grid[r][c] == 0 and len(board.candidates[r][c]) == 2]

    for r1, c1, (x, y) in bivalue_cells:
        for r2, c2, pair2 in bivalue_cells:
            if (r1, c1) == (r2, c2):
                continue
            if x in pair2 and len(set((x, y)).intersection(pair2)) == 1:
                z = (set(pair2) - {x}).pop()
                for r3, c3, pair3 in bivalue_cells:
                    if (r3, c3) in [(r1, c1), (r2, c2)]:
                        continue
                    if y in pair3 and z in pair3 and len(pair3) == 2:
                        # Verificar intersección de influencia entre c2 y c3
                        shared_peers = get_shared_peers((r2, c2), (r3, c3))
                        if shared_peers:
                            return f"XY-Wing con pivote ({r1+1},{chr(c1+65)}) usando {x,y}, alas en ({r2+1},{chr(c2+65)}) y ({r3+1},{chr(c3+65)}), eliminar {z} de {shared_peers}"
    return None