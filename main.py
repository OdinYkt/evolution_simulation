from tkinter import *
import time
from random import randrange, shuffle

def crt_cell(): #создание сетки отображения
    global cells
    cells = [[Label(text=f'     ', width= 2, height= 1, background= '#9c9192') for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            cells[i][j].place(x=indent+i*21, y=indent+j*22)

def crt_live(count): #создание организмов
    global live, c_live, n_live, n
    n = count
    live = [[randrange(0, 64) for i in range(64)] for j in range(n)]
    c_live = [[randrange(0, 32) for i in range(2)] for j in range(n)] #возможно два бота на одной позиции
    n_live = [i for i in range(n)]
    for i in range(n):
        x, y = c_live[i][0], c_live[i][1]
        cells[x][y].configure(background='red')


def move(side,n):
    x, y = c_live[n][0], c_live[n][1]
    if side == 0 and not([x, y + 1] in c_live): #вниз
        cells[x][y].configure(background='#9c9192')
        x += 0
        y += 1
        c_live[n] = [x, y]
        cells[x][y].configure(background='red')
    elif side == 1 and not([x + 1, y + 1] in c_live):
        cells[x][y].configure(background='#9c9192')
        x += 1
        y += 1
        c_live[n] = [x, y]
        cells[x][y].configure(background='red')
    elif side == 2 and not ([x - 1, y] in c_live):
        cells[x][y].configure(background='#9c9192')
        x += -1
        y += 0
        c_live[n] = [x, y]
        cells[x][y].configure(background='red')
    elif side == 3 and not ([x - 1, y - 1] in c_live):
        cells[x][y].configure(background='#9c9192')
        x += -1
        y += -1
        c_live[n] = [x, y]
        cells[x][y].configure(background='red')
    elif side == 4 and not ([x - 1, y] in c_live):
        cells[x][y].configure(background='#9c9192')
        x += -1
        y += 0
        c_live[n] = [x, y]
        cells[x][y].configure(background='red')
    elif side == 5 and not ([x - 1, y + 1] in c_live):
        cells[x][y].configure(background='#9c9192')
        x += -1
        y += 1
        c_live[n] = [x, y]
        cells[x][y].configure(background='red')
    elif side == 6 and not ([x, y + 1] in c_live):
        cells[x][y].configure(background='#9c9192')
        x += 0
        y += 1
        c_live[n] = [x, y]
        cells[x][y].configure(background='red')
    elif side == 7 and not ([x + 1, y + 1] in c_live):
        cells[x][y].configure(background='#9c9192')
        x += 1
        y += 1
        c_live[n] = [x, y]
        cells[x][y].configure(background='red')

def step():
    shuffle(n_live)
    rdy = 0
    k = 0 # очередь
    c = 0 # команды
    while rdy<n:
        if 0<=live[n_live[k]][c]<=7: #live[n_live[k]] - список 0-64
            move(live[n_live[k]][c])



def start_color(): #test
    for i in range(size):
        cells[i][0].configure(background='black')
        cells[i][size-1].configure(background='black')
        cells[0][i].configure(background='black')
        cells[size-1][i].configure(background='black')

window = Tk()
window.title("Симулирование эволюции")
window.geometry('1600x1600')

size = 36  # 100x100 count of cells
indent = 50

crt_cell()
start_color()
crt_live(int(input('Введите количество организмов:')))

window.mainloop()
