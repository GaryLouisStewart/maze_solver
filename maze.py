from cell import Cell
import time
import random


class Maze:
    def __init__(self,
                 x1,
                 y1,
                 num_rows,
                 num_cols,
                 cell_size_x,
                 cell_size_y,
                 win=None,
                 seed=None,
                 ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            cols = []
            for j in range(self._num_rows):
                cols.append(Cell(self._win))
            self._cells.append(cols)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return

        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j]._visited = True

        while True:
            to_visit = []

            # check left
            if i > 0 and not self._cells[i - 1][j]._visited:
                to_visit.append((i - 1, j))

            # check right
            if i < self._num_cols - 1 and not self._cells[i + 1][j]._visited:
                to_visit.append((i + 1, j))

            # check top
            if j > 0 and not self._cells[i][j - 1]._visited:
                to_visit.append((i, j - 1))
            # check bottom
            if j < self._num_rows - 1 and not self._cells[i][j + 1]._visited:
                to_visit.append((i, j + 1))

            if not to_visit:
                self._draw_cell(i, j)
                return

            next_i, next_j = random.choice(to_visit)

            if next_j > j:
                # right
                self._cells[i][j].has_right_wall = False
                self._cells[i][j + 1].has_left_wall = False
            if next_j < j:
                # left
                self._cells[i][j].has_left_wall = False
                self._cells[i][j - 1].has_right_wall = False
            if next_i > i:
                # down
                self._cells[i][j].has_bottom_wall = False
                self._cells[i + 1][j].has_top_wall = False
            if next_i < i:
                # up
                self._cells[i][j].has_top_wall = False
                self._cells[i - 1][j].has_bottom_wall = False

            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell._visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        # mark the current cell as visited.
        self._cells[i][j]._visited = True

        # check if we are at the end cell

        end_i = len(self._cells) - 1
        end_j = len(self._cells[0]) - 1

        if i == len(self._cells) - 1 and j == len(self._cells[0]) - 1:
            return True

        # directional checking

        # right
        if j + 1 < len(self._cells[0]):
            if not self._cells[i][j].has_right_wall:
                if not self._cells[i][j + 1]._visited:
                    self._cells[i][j].draw_move(self._cells[i][j + 1])
                    if self._solve_r(i, j + 1):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)
        # left
        if j - 1 >= 0:
            if not self._cells[i][j].has_left_wall:
                if not self._cells[i][j - 1]._visited:
                    self._cells[i][j].draw_move(self._cells[i][j - 1])
                    if self._solve_r(i, j - 1):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)

        # top
        if i - 1 >= 0:
            if not self._cells[i][j].has_top_wall:
                if not self._cells[i - 1][j]._visited:
                    self._cells[i][j].draw_move(self._cells[i - 1][j])
                    if self._solve_r(i - 1, j):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[i - 1][j], undo=True)

        # bottom

        if i + 1 < len(self._cells):
            if not self._cells[i][j].has_bottom_wall:
                if not self._cells[i + 1][j]._visited:
                    self._cells[i][j].draw_move(self._cells[i + 1][j])
                    if self._solve_r(i + 1, j):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True)

        return False
