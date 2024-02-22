import ui

app = ui.App()

num_cols = 13
num_rows = 13
m2 = ui.Maze(10, 10, num_rows, num_cols, 40, 40, win=app.maze)

app.wait_for_close()