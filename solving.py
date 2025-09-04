class Solver:
    grid = None

    def __init__(self, grid):
        self.grid = grid

    def look_for_solvation(self):
        solvations = set()
        swaps = []

        for r in range(8):
            for c in range(8):
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if nr >= 8 or nc >= 8:
                        continue

                    grid_copy = self.grid.copy()
                    grid_copy[r, c], grid_copy[nr, nc] = grid_copy[nr, nc], grid_copy[r, c]

                    matched = self.__check_grid_matches(grid_copy)

                    if matched:
                        matched.add((r, c))
                        matched.add((nr, nc))
                        solvations.update(matched)
                        swaps.append(((r, c), (nr, nc)))

        return solvations, swaps

    # Проверяет поле на наличие плиток длиной >=3, возвращает список индексов по двум координатам
    def __check_grid_matches(self, grid):
        matched_positions = set()

        # Проверка по строкам
        for r in range(8):
            count = 1
            for c in range(1, 8):
                if grid[r, c] == grid[r, c - 1]:
                    count += 1
                else:
                    if count >= 3:
                        for k in range(c - count, c):
                            matched_positions.add((r, k))
                    count = 1
            if count >= 3:
                for k in range(8 - count, 8):
                    matched_positions.add((r, k))

        # Проверка по столбцам
        for c in range(8):
            count = 1
            for r in range(1, 8):
                if grid[r, c] == grid[r - 1, c]:
                    count += 1
                else:
                    if count >= 3:
                        for k in range(r - count, r):
                            matched_positions.add((k, c))
                    count = 1
            if count >= 3:
                for k in range(8 - count, 8):
                    matched_positions.add((k, c))

        return matched_positions

