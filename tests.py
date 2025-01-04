import unittest

from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_large_cells(self):
        num_cols = 12
        num_rows = 16
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertFalse(m1._cells[0][0].has_top_wall)
        self.assertFalse(m1._cells[num_cols - 1][num_rows - 1].has_bottom_wall)


class TestMaze(unittest.TestCase):

    def setUp(self):
        self.num_rows = 5
        self.num_cols = 5
        self.cell_size_x = 10
        self.cell_size_y = 10
        self.x1 = 0
        self.y1 = 0
        self.test_maze = Maze(self.num_rows, self.num_cols, self.cell_size_x, self.cell_size_y, self.x1, self.y1,
                              seed=0)

    def test_complete_maze_generation(self):
        self.test_maze._break_entrance_and_exit()
        self.test_maze._break_walls_r(0, 0)
        for row in self.test_maze._cells:
            for cell in row:
                self.assertTrue(cell._visited)

    def test_correct_pathway_carving(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if j < self.num_cols - 1:
                    right_cell = self.test_maze._cells[i][j + 1]
                    current_cell = self.test_maze._cells[i][j]
                    self.assertEqual(current_cell.has_right_wall, right_cell.has_left_wall,
                                     f"Mismatch in walls between ({i}, {j}) and ({i}, {j + 1})")

                if i < self.num_rows - 1:
                    bottom_cell = self.test_maze._cells[i + 1][j]
                    current_cell = self.test_maze._cells[i][j]
                    self.assertEqual(current_cell.has_bottom_wall, bottom_cell.has_top_wall,
                                     f"Mismatch in walls between ({i}, {j}) and ({i + 1}, {j})")

    def test_cell_is_visited_rest(self):

        for row in self.test_maze._cells:
            for cell in row:
                cell._visited = True

        self.test_maze._reset_cells_visited()

        for row in self.test_maze._cells:
            for cell in row:
                self.assertEqual(cell._visited, False)


if __name__ == "__main__":
    unittest.main()
