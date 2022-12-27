from tkinter import *
import time
from random import randrange, shuffle

def crt_cell(): #создание сетки отображения
    global cells
    cells = [[Label(text=f'     ', width= 2, height= 1, background= '#9c9192') for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            cells[i][j].place(x=indent+i*21, y=indent+j*22)


def crt_live(count):                                                    #создание организмов
    global live, c_live, n_live, n
    n = count
    live = [[randrange(0, 64) for i in range(64)] for j in range(n)]

    for j in range(n):                                                  #добавление хп в 65е значение в списке генома
        live[j].append(10)

    c_live = []                                                         #координаты живых клеток
    j = 0
    while j<n:
            xy = [randrange(0, 32), randrange(0, 32)]
            if not(xy in c_live):
                c_live.append(xy)
                j += 1

    n_live = [i for i in range(n)]                                      #сбор количества живых клеток

    for i in range(n):                                                  #покрас живых клеток
        x, y = c_live[i][0], c_live[i][1]
        cells[x][y].configure(background='red')


def create_food(count_of_food):
    global food_coord
    food_coord = []
    i = 0
    while i<count_of_food:
        xy = [randrange(0, 32), randrange(0, 32)]
        if not(xy in c_live) and not(xy in food_coord):
            food_coord.append(xy)
            i += 1
            cells[xy[0]][xy[1]].configure(background='green')


def move(side,index_of_bot):       #стороны перепутаны, но задействованы все
    c = index_of_bot
    x, y = c_live[c][0], c_live[c][1]
    if side == 0 and not([x - 1, y - 1] in c_live):
        cells[x][y].configure(background='#9c9192')
        x += -1
        y += -1
        c_live[c] = [x, y]
        cells[x][y].configure(background='red')
    elif side == 1 and not([x - 1, y + 1] in c_live):
        cells[x][y].configure(background='#9c9192')
        x += -1
        y += 1
        c_live[c] = [x, y]
        cells[x][y].configure(background='red')
    elif side == 2 and not ([x - 1, y] in c_live):
        cells[x][y].configure(background='#9c9192')
        x += -1
        c_live[c] = [x, y]
        cells[x][y].configure(background='red')
    elif side == 3 and not ([x, y - 1] in c_live):
        cells[x][y].configure(background='#9c9192')
        y += -1
        c_live[c] = [x, y]
        cells[x][y].configure(background='red')
    elif side == 4 and not ([x, y + 1] in c_live): #
        cells[x][y].configure(background='#9c9192')
        y += 1
        c_live[c] = [x, y]
        cells[x][y].configure(background='red')
    elif side == 5 and not ([x + 1, y - 1] in c_live):
        cells[x][y].configure(background='#9c9192')
        x += 1
        y += -1
        c_live[c] = [x, y]
        cells[x][y].configure(background='red')
    elif side == 6 and not ([x, y + 1] in c_live): #
        cells[x][y].configure(background='#9c9192')
        x += 1
        y += 1
        c_live[c] = [x, y]
        cells[x][y].configure(background='red')
    elif side == 7 and not ([x + 1, y] in c_live):
        cells[x][y].configure(background='#9c9192')
        x += 1
        c_live[c] = [x, y]
        cells[x][y].configure(background='red')


def eat(side, index_of_bot):
    x, y = c_live[index_of_bot][0], c_live[index_of_bot][1]
    flag = False
    if side == 8 and [x - 1, y - 1] in c_live:
        index_of_victim = c_live.index([x - 1, y - 1])
        flag = True
    elif side == 9 and [x - 1, y + 1] in c_live:
        index_of_victim = c_live.index([x - 1, y + 1])
        flag = True
    elif side == 10 and [x - 1, y] in c_live:
        index_of_victim = c_live.index([x - 1, y])
        flag = True
    elif side == 11 and [x, y - 1] in c_live:
        index_of_victim = c_live.index([x, y - 1])
        flag = True
    elif side == 12 and [x, y + 1] in c_live:
        index_of_victim = c_live.index([x, y + 1])
        flag = True
    elif side == 13 and [x + 1, y - 1] in c_live:
        index_of_victim = c_live.index([x + 1, y - 1])
        flag = True
    elif side == 14 and [x + 1, y + 1] in c_live:
        index_of_victim = c_live.index([x + 1, y + 1])
        flag = True
    elif side == 15 and [x + 1, y] in c_live:
        index_of_victim = c_live.index([x + 1, y])
        flag = True

    if flag:
        live[index_of_bot][64] += live[index_of_victim][64]  # забирает жизнь жертвы
        c_live.pop(index_of_victim)  # удаляем жертву из координат
        live.pop(index_of_bot)

# def watch(side, n):
#     ans = 1                         # 1 - empty, 2 - enemy, 3 - food, 4 - poison
#     if side == 16:
#         if [x - 1, y - 1] in c_live:
#             ans = 2
#         elif
#     elif side == 17 and [x - 1, y + 1] in c_live:
#         index_of_victim = c_live.index([x - 1, y + 1])
#         flag = True
#     elif side == 18 and [x - 1, y] in c_live:
#         index_of_victim = c_live.index([x - 1, y])
#         flag = True
#     elif side == 19 and [x, y - 1] in c_live:
#         index_of_victim = c_live.index([x, y - 1])
#         flag = True
#     elif side == 20 and [x, y + 1] in c_live:
#         index_of_victim = c_live.index([x, y + 1])
#         flag = True
#     elif side == 21 and [x + 1, y - 1] in c_live:
#         index_of_victim = c_live.index([x + 1, y - 1])
#         flag = True
#     elif side == 22 and [x + 1, y + 1] in c_live:
#         index_of_victim = c_live.index([x + 1, y + 1])
#         flag = True
#     elif side == 23 and [x + 1, y] in c_live:
#         index_of_victim = c_live.index([x + 1, y])
#         flag = True


def step():
    n_step = n_live
    shuffle(n_step)
    rdy = 0
    c = [0 for _ in range(n_live.count())]   # команды
    while rdy<n:
        for k in n_step:                               # очередь
            if 0<=live[k][c[k]]<=7:     #live[k] - список 0-64
                move(live[k][c[k]], k)  #движение
                rdy+=1
                live[k][64]-=1          #1хп в ход
                n_step.pop(k)
            elif 8<=live[k][c[k]]<=15:  #есть
                eat(live[k][c[k]], k)
                rdy+=1
                live[k][64]-=1
                n_step.pop(k)
            # elif 16<=live[k][c[k]]<=23:
            #     if watch(live[k][c[k]], k):


def start_color():                                      #test
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
create_food(10)

while True: #test move
    for i in range(8):
        time.sleep(2)
        move(i, 1)
        window.update()


