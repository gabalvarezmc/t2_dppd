import numpy as np
from .techniques import basic_techniques, interseccion_linearegion, naked_subset, \
    subconjuntos_ocultos, xy_wing, xyz_wing, xy_chain, rectangulo_unicidad, fish_patterns, cadenas_coloreadas

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


# Actualizamos suggest_technique para incluir subconjuntos ocultos
def suggest_technique(board):
    techniques = [
        basic_techniques.find_naked_single,
        basic_techniques.find_hidden_single,
        basic_techniques.find_naked_pair,
        lambda b: naked_subset.find_naked_subset(b, 3),
        lambda b: naked_subset.find_naked_subset(b, 4),
        lambda b: subconjuntos_ocultos.find_hidden_subset(b, 2),
        lambda b: subconjuntos_ocultos.find_hidden_subset(b, 3),
        lambda b: subconjuntos_ocultos.find_hidden_subset(b, 4),
        interseccion_linearegion.find_pointing_line_region,
        xy_wing.find_xy_wing,
        xyz_wing.find_xyz_wing,
        xy_chain.find_xy_chain,
        cadenas_coloreadas.find_colored_chains,
        rectangulo_unicidad.find_unique_rectangle,
        lambda b: fish_patterns.find_fish_patterns(b, 2),
        lambda b: fish_patterns.find_fish_patterns(b, 3),
        lambda b: fish_patterns.find_fish_patterns(b, 4),
    ]
    list_of_techniques = []
    for tech in techniques:
        result = tech(board)
        if result:
            # print("Sugerencia de técnica:", result)
            list_of_techniques.append(result)
            return result
    # if list_of_techniques:
    #     return list_of_techniques
    return "No se encontró ninguna técnica aplicable de las implementadas."


sudoku_code = "030040002020035100089020030000310070000580300008467290000094020260050007800270040"
example_grid = [
    [int(sudoku_code[i * 9 + j]) for j in range(9)] for i in range(9)
]
board = SudokuBoard(example_grid)
suggestion = suggest_technique(board)
