import tkinter as tk
import numpy as np
from tkinter import messagebox  # 导入提示窗口包

go_bang = '五子棋'
grid = 8  # number of grid of chessboard
boundary = 32
width_of_chessboard = 424
width_of_block = 45
r_of_mp = 4
width_of_chess = 12

my_turn = 0  # black chess first
player = 0  # black chess
colors = ['black', 'white']
max_depth = 1  # important parameter - max step we can predict

black_chess = []
white_chess = []

def x2index(x):
    return int((x - boundary) / width_of_block)


def index2x(index):
    return index * width_of_block + boundary


def gui(root, canvas):
    root.title(go_bang)
    root.geometry("424x424")

    canvas.grid(row=0, column=0, rowspan=6)
    canvas.bind("<Button-1>", put_chess)  # bind mouse event

    for i in range(grid + 1):  # draw line
        canvas.create_line(boundary, (width_of_block * i + boundary), width_of_block * grid + boundary,
                           (width_of_block * i + boundary))
        canvas.create_line((width_of_block * i + boundary), boundary, (width_of_block * i + boundary),
                           width_of_block * grid + boundary)

    point_x = [2, 4, 6, 6, 2]  # draw marked point
    point_y = [2, 4, 6, 2, 6]
    for i in range(5):
        loc_x = width_of_block * point_x[i] + boundary
        loc_y = width_of_block * point_y[i] + boundary
        canvas.create_oval(loc_x - r_of_mp, loc_y - r_of_mp,
                           loc_x + r_of_mp, loc_y + r_of_mp, fill="black")


def is_win(x, y, temp_turn):
    index_x = x2index(x)
    index_y = x2index(y)
    # if left to right
    count = 1
    temp_x = index_x - 1
    while 0 <= temp_x <= grid and 0 <= index_y <= grid and loc[temp_x][index_y] == temp_turn:
        count += 1
        temp_x -= 1
    temp_x = index_x + 1
    while 0 <= temp_x <= grid and 0 <= index_y <= grid and loc[temp_x][index_y] == temp_turn:
        count += 1
        temp_x += 1
    if count >= 5:
        return True
    # if up to down
    count = 1
    temp_y = index_y - 1
    while 0 <= index_x <= grid and 0 <= temp_y <= grid and loc[index_x][temp_y] == temp_turn:
        count += 1
        temp_y -= 1
    temp_y = index_y + 1
    while 0 <= index_x <= grid and 0 <= temp_y <= grid and loc[index_x][temp_y] == temp_turn:
        count += 1
        temp_y += 1
    if count >= 5:
        return True
    # if left up to right down
    count = 1
    temp_x = index_x - 1
    temp_y = index_y - 1
    while 0 <= temp_x <= grid and 0 <= temp_y <= grid and loc[temp_x][temp_y] == temp_turn:
        count += 1
        temp_x -= 1
        temp_y -= 1
    temp_x = index_x + 1
    temp_y = index_y + 1
    while 0 <= temp_x <= grid and 0 <= temp_y <= grid and loc[temp_x][temp_y] == temp_turn:
        count += 1
        temp_x += 1
        temp_y += 1
    if count >= 5:
        return True
    # if left down to right up
    count = 1
    temp_x = index_x - 1
    temp_y = index_y + 1
    while 0 <= temp_x <= grid and 0 <= temp_y <= grid and loc[temp_x][temp_y] == temp_turn:
        count += 1
        temp_x -= 1
        temp_y += 1
    temp_x = index_x + 1
    temp_y = index_y - 1
    while 0 <= temp_x <= grid and 0 <= temp_y <= grid and loc[temp_x][temp_y] == temp_turn:
        count += 1
        temp_x += 1
        temp_y -= 1
    if count >= 5:
        return True
    return False


def draw_chess(color, x, y):
    c.create_oval(x - width_of_chess, y - width_of_chess, x + width_of_chess, y + width_of_chess, fill=color)


# put chess to the chessboard
def put_chess(event):
    global my_turn
    if my_turn == player:
        # it is player's turn
        click_x = event.x
        click_y = event.y

        overflow_x = (click_x - boundary) % width_of_block  # find nearest location
        overflow_y = (click_y - boundary) % width_of_block
        if overflow_x < width_of_block / 2:
            x = click_x - overflow_x
        else:
            x = click_x - overflow_x + width_of_block
        if overflow_y < width_of_block / 2:
            y = click_y - overflow_y
        else:
            y = click_y - overflow_y + width_of_block

        draw_chess(colors[player], x, y)
        loc[x2index(x)][x2index(y)] = my_turn

        if not is_win(x, y, player):  # it is computer's turn
            my_turn = (my_turn + 1) % 2
            best_score, best_loc = max_min((player + 1) % 2, max_depth, float('-Inf'), float('Inf'))
            best_i, best_j = best_loc
            loc[best_i][best_j] = (player + 1) % 2
            draw_chess(colors[(player + 1) % 2], index2x(best_i), index2x(best_j))
            if is_win(best_i, best_j, (player+1) % 2):
                messagebox.showerror("showerror", "Computer win！")
            my_turn = (my_turn + 1) % 2
        else:
            messagebox.showinfo("showinfo", "You win！")


# give score of chess
def give_chess_score(number, empty):
    if number >= 5:
        return 500000
    elif number == 4:
        if empty == 2:
            return 50000
        elif empty == 1:
            return 5000
    elif number == 3:
        if empty == 2:
            return 5000
        elif empty == 1:
            return 500
    elif number == 2:
        if empty == 2:
            return 100
        elif empty == 1:
            return 10
    elif number == 1 and empty == 2:
        return 10
    return 0


def give_line_score(line, chess):
    empty = 0  # live or dead chess
    number = 0  # number of consequent chess
    score = 0  # score of chess
    if line[0] == -1:
        empty = 1
    elif line[0] == chess:
        number += 1
    for i in range(1, len(line)):
        if line[i] == chess:
            number += 1
        elif line[i] == -1:
            if number == 0:
                empty = 1
            else:
                score += give_chess_score(number, empty+1)
                empty = 1
                number = 0
        else:
            score += give_chess_score(number, empty)
            empty = 0
            number = 0
    score += give_chess_score(number, empty)
    return score


def give_score(chess):
    score = 0
    # from left to right
    for i in range(grid + 1):
        score += give_line_score(loc[i], chess)
    # from up to down
    for j in range(grid + 1):
        line = []
        for i in range(grid + 1):
            line.append(loc[i][j])
        score += give_line_score(line, chess)
    # from left up to right down
    for j in range(grid + 1):
        i = 0
        line = []
        while i <= grid and j <= grid:
            line.append(loc[i][j])
            i += 1
            j += 1
        score += give_line_score(line, chess)
    for i in range(1, grid + 1):
        j = 0
        line = []
        while i <= grid and j <= grid:
            line.append(loc[i][j])
            i += 1
            j += 1
        score += give_line_score(line, chess)
    # from left down to right up
    for i in range(grid + 1):
        j = 0
        while i >= 0 and j <= grid:
            line.append(loc[i][j])
            i -= 1
            j += 1
        score += give_line_score(line, chess)
    for j in range(1, grid + 1):
        i = grid
        while i >= 0 and j <= grid:
            line.append(loc[i][j])
            i -= 1
            j += 1
        score += give_line_score(line, chess)
    return score


# max min algorithm with Alpha-Beta pruning
def max_min(temp_turn, depth, alpha, beta):
    if depth == 1:
        if temp_turn == player:  # if it is player's turn, we need min score of computer
            best = float('inf')
            best_loc = (-1, -1)
            for i in range(grid + 1):
                for j in range(grid + 1):
                    if loc[i][j] == -1:
                        loc[i][j] = temp_turn
                        score = give_score((player+1) % 2) - give_score(player)
                        loc[i][j] = -1
                        if score < best:
                            best = score
                            best_loc = (i, j)
            return best, best_loc
        else:  # if it is computer's turn, we need max score of computer
            best = float('-inf')
            best_loc = (-1, -1)
            for i in range(grid + 1):
                for j in range(grid + 1):
                    if loc[i][j] == -1:
                        loc[i][j] = temp_turn
                        score = give_score((player+1) % 2) - give_score(player)
                        loc[i][j] = -1
                        if score > best:
                            best = score
                            best_loc = (i, j)
            return best, best_loc
    if temp_turn == player:  # if it is player's turn, we need min score of computer
        best = float('inf')
        best_loc = (-1, -1)
        for i in range(grid + 1):
            for j in range(grid + 1):
                if loc[i][j] == -1:
                    loc[i][j] = temp_turn
                    next_score, next_loc = max_min((temp_turn + 1) % 2, depth - 1, alpha, beta)
                    loc[i][j] = -1
                    if next_score < best:
                        best = next_score
                        best_loc = (i, j)
                    if beta > next_score:
                        beta = next_score
                    if alpha > beta:
                        return best, best_loc
        return best, best_loc
    else:
        best = float('-inf')
        best_loc = (-1, -1)
        for i in range(grid + 1):
            for j in range(grid + 1):
                if loc[i][j] == -1:
                    loc[i][j] = temp_turn
                    next_score, next_loc = max_min((temp_turn + 1) % 2, depth - 1, alpha, beta)
                    loc[i][j] = -1
                    if next_score > best:
                        best = next_score
                        best_loc = (i, j)
                    if alpha < next_score:
                        alpha = next_score
                    if alpha > beta:
                        return best, best_loc
        return best, best_loc


if __name__ == '__main__':
    r = tk.Tk()
    # background
    c = tk.Canvas(r, bg="saddlebrown", width=width_of_chessboard, height=width_of_chessboard)
    # init map
    loc = np.array([-1] * ((grid + 1) * (grid + 1))).reshape([(grid + 1), (grid + 1)])
    # GUI
    gui(r, c)
    # run game
    r.mainloop()

