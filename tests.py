import unittest
from ui import Maze, Cell

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows
        )

    def test_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m2 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m2._cells[0][0].has_left_wall,
            False
        )
        self.assertEqual(
            m2._cells[0][0].has_right_wall,
            False
        )
        self.assertEqual(
            m2._cells[0][0].has_top_wall,
            False
        )
        self.assertEqual(
            m2._cells[0][0].has_bottom_wall,
            False
        )

    def test_break_neighbour_wall(self):
        num_cols = 7
        num_rows = 6
        m2 = Maze(10, 10, num_rows, num_cols, 80, 80, seed=1)
        self.assertEqual(
            m2._cells[2][0].has_left_wall,
            False
        )
        self.assertEqual(
            m2._cells[3][4].has_left_wall,
            False
        )
        self.assertEqual(
            m2._cells[3][4].has_bottom_wall,
            False
        )

    def test_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10
        m2 = Maze(0, 0, num_rows, num_cols, 10, 10)
        for j in m2._cells:
            for i in j:
                self.assertEqual(
                    i.visited,
                    False
                )

if __name__ == "__main__":
    unittest.main()