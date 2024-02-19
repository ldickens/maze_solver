import ui

app = ui.App()

num_cols = 7
num_rows = 6
m2 = ui.Maze(10, 10, num_rows, num_cols, 80, 80, win=app.maze)

app.wait_for_close()