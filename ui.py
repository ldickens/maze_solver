from tkinter import Tk, BOTH, Canvas
from time import sleep
import random
 
class App(Tk):
    def __init__(self,):
        super().__init__()

        w = 800
        h = 600

        self.running = False

        self.geometry(f'{w}x{h}')
        self.title('Maze Solver')
        self.protocol('WM_DELETE_WINDOW', self.close)

        self.maze = MazeDrawing(self)
        self.maze.pack(fill=BOTH, expand=True)

    def redraw(self):
        self.update_idletasks()
        self.update()
    
    def wait_for_close(self):
        self.running = True
        while self.running == True:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill_colour):
        line.draw(self.maze, fill_colour)


class MazeDrawing(Canvas):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(background='white')
        
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, p1, p2):
        self.p1  = p1
        self.p2 = p2

    def draw(self, canvas, fill_colour):
        if canvas is not None:
            canvas.create_line(
                self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_colour, width=2
            )
            canvas.pack(fill=BOTH, expand=True)

class Cell():
    def __init__(self, x1, y1, x2, y2, win = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win
        self.visited = False

    def draw(self):
        top_right = Point(self._x2, self._y1)
        bot_right = Point(self._x2, self._y2)
        top_left = Point(self._x1, self._y1)
        bot_left = Point(self._x1, self._y2)

        left_line = Line(top_left, bot_left)
        top_line = Line(top_left, top_right)
        right_line = Line(top_right, bot_right)
        bottom_line = Line(bot_left, bot_right)

        if self.has_left_wall:
            left_line.draw(self._win, "black")
        else:
            left_line.draw(self._win, "white")

        if self.has_right_wall:
            right_line.draw(self._win, "black")
        else:
            right_line.draw(self._win, "white")

        if self.has_top_wall:
            top_line.draw(self._win, "black")
        else:
            top_line.draw(self._win, "white")
        
        if self.has_bottom_wall:
            bottom_line.draw(self._win, "black")
        else:
            bottom_line.draw(self._win, "white")

    def draw_move(self, to_cell, undo=False):
        colour = 'red'
        if undo:
            colour = 'grey'
        this_mx = (self._x1 + self._x2) // 2
        this_my = (self._y1 + self._y2) // 2
        this_point = Point(this_mx, this_my)

        to_cell_mx = (to_cell._x1 + to_cell._x2) // 2
        to_cell_my = (to_cell._y1 + to_cell._y2) // 2
        to_cell_point = Point(to_cell_mx, to_cell_my)

        line = Line(this_point, to_cell_point)
        line.draw(self._win, colour)


class Maze():
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win = None,
            seed = None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        if seed is not None:
           random.seed(seed)

        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        for e, col in enumerate(range(self.num_cols)):
            self._cells.append([])
            for a, row in enumerate(range(self.num_rows)):
                self._cells[e].append(Cell(
                    self.x1 + (self.cell_size_x * e), #x1
                    self.y1 + (self.cell_size_y * a), #y1
                    self.x1 + (self.cell_size_x * (e + 1)), #x2
                    self.y1 + (self.cell_size_y * (a + 1)), #y2
                    win = self._win
                    ))
                
    def _draw_cell(self):
        for col in self._cells:
            for cell in col:
                cell.draw()

    def _animate(self):
        self._win.redraw()
        sleep(0.05)

    def _break_entrance_and_exit(self):
        maze_entrance = self._cells[0][0]
        maze_entrance.has_left_wall = False
        maze_entrance.has_right_wall = False
        maze_entrance.has_top_wall = False
        maze_entrance.has_bottom_wall = False

        maze_exit = self._cells[self.num_cols - 1][self.num_rows - 1]
        maze_exit.has_left_wall = False
        maze_exit.has_right_wall = False
        maze_exit.has_top_wall = False
        maze_exit.has_bottom_wall = False

        self._draw_cell()

    
    def _break_walls_r(self, i , j):
        self._cells[j][i].visited = True

        if i == self.num_rows-1 and j == self.num_cols-1:
            return

        while True:
            to_visit = []
            neighbours = 0
            # check neighbours
            for x in range(j-1, j+2):
                if x > 0 and x <= self.num_cols-1:
                    if self._cells[x][i].visited == False:
                        to_visit.append([i,x])
                        neighbours += 1
            for y in range(i-1, i+2):
                if y > 0 and y <= self.num_rows-1:
                    if self._cells[j][y].visited == False:
                        to_visit.append([y, j])
                        neighbours += 1

            if neighbours != 0:
                # find next random direction, break walls and recursively call next cell
                next_cell_idx = random.randint(0, neighbours - 1)
                next_cell = to_visit[next_cell_idx]
                self.break_neighbour_wall((i, j), next_cell)
                self._break_walls_r(*next_cell)
            else:
                self._draw_cell()
                return

    def break_neighbour_wall(self, cur_cell, neighbour_cell):
        y1, x1  = cur_cell
        yt, xt = neighbour_cell

        if x1 - xt != 0:
            if x1 - xt == 1:
                self._cells[x1][y1].has_left_wall = False
                self._cells[xt][yt].has_right_wall = False
            else:
                self._cells[x1][y1].has_right_wall = False
                self._cells[xt][yt].has_left_wall = False
        else:
            if y1 - yt == 1:
                self._cells[x1][y1].has_top_wall = False
                self._cells[xt][yt].has_bottom_wall = False
            else:
                self._cells[x1][y1].has_bottom_wall = False
                self._cells[xt][yt].has_top_wall = False

    def _reset_cells_visited(self):
        for j in self._cells:
            for i in j:
                i.visited = False