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

def find_colored_chains(board):
    from collections import defaultdict, deque

    def get_candidate_map():
        # Diccionario: dígito → lista de pares conjugados (dos celdas por grupo)
        candidate_map = defaultdict(list)
        for digit in range(1, 10):
            for unit in get_all_units():
                positions = [(r, c) for (r, c) in unit if digit in board.candidates[r][c]]
                if len(positions) == 2:
                    candidate_map[digit].append(tuple(positions))
        return candidate_map

    def build_color_graph(pairs):
        graph = defaultdict(list)
        for a, b in pairs:
            graph[a].append(b)
            graph[b].append(a)
        return graph

    def color_chain(graph):
        color = {}
        for node in graph:
            if node not in color:
                queue = deque([(node, 0)])
                while queue:
                    current, c = queue.popleft()
                    color[current] = c
                    for neighbor in graph[current]:
                        if neighbor not in color:
                            queue.append((neighbor, 1 - c))
                        elif color[neighbor] == color[current]:
                            return None  # conflicto, no es bipartito
        return color

    def find_type1(color, digit):
        # Casilla no en la cadena que ve dos colores opuestos del mismo dígito
        marked = list(color.items())
        for r in range(9):
            for c in range(9):
                if board.grid[r][c] != 0 or digit not in board.candidates[r][c]:
                    continue
                sees = [parity for (r2, c2), parity in marked if shares_unit((r, c), (r2, c2))]
                if 0 in sees and 1 in sees:
                    return f"Cadena coloreada tipo 1: eliminar candidato {digit} de ({r+1},{chr(c+65)})"
        return None

    def find_type2(color, digit):
        # Dos celdas de igual color que se vean mutuamente
        for (r1, c1), p1 in color.items():
            for (r2, c2), p2 in color.items():
                if p1 == p2 and (r1, c1) != (r2, c2) and shares_unit((r1, c1), (r2, c2)):
                    return f"Cadena coloreada tipo 2: eliminar candidato {digit} de todas las celdas de color {p1}"
        return None

    # Procedimiento general
    candidate_map = get_candidate_map()
    for digit, pairs in candidate_map.items():
        graph = build_color_graph(pairs)
        color = color_chain(graph)
        if color:
            result1 = find_type1(color, digit)
            if result1:
                return result1
            result2 = find_type2(color, digit)
            if result2:
                return result2
    return None
