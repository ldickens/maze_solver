import ui

app = ui.App()

num_cols = 14
num_rows = 14
m2 = ui.Maze(10, 10, num_rows, num_cols, 10, 10, win=app.maze)

app.wait_for_close()