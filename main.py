from tkinter import *
import time
from random import randrange, shuffle

background = '#9c9192'
d = {0: [1, 0], 1: [1, 1], 2: [1, -1], 3: [0, 1], 4: [0, -1], 5: [-1, 0], 6: [-1, 1], 7: [-1, -1]}

def crt_cell(): #создание сетки отображения
    global cells
    cells = [[Label(text=f'     ', width=2, height=1, background=background) for i in range(size)] for j in range(size)]
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
    x, y = c_live[index_of_bot][0], c_live[index_of_bot][1]
    xy = d.get(side)                                           #d = {0: [1, 0], 1: [1, 1], 2: [1, -1], 3: [0, 1], 4: [0, -1], 5: [-1, 0], 6: [-1, 1], 7: [-1, -1]}
    xy[0] += x
    xy[1] += y
    if xy not in c_live:
        cells[x][y].configure(background='#9c9192')
        c_live[index_of_bot] = xy
        cells[xy[0]][xy[1]].configure(background='red')


def eat(side, index_of_bot):
    x, y = c_live[index_of_bot][0], c_live[index_of_bot][1]
    xy = d.get(side - 8)
    xy[0] += x
    xy[1] += y
    if xy in c_live:                                            #поиск жертвы в виде бота
        index_of_victim = c_live.index(xy)

        live[index_of_bot][64] += live[index_of_victim][64]     # забирает жизнь жертвы
        c_live.pop(index_of_victim)                             # удаляем жертву из координат
        cells[xy[0]][xy[1]].configure(background=background)
        live.pop(index_of_victim)
    elif xy in food_coord:                                      #поиск жертвы в виде еды
        index_of_victim = food_coord.index(xy)

        live[index_of_bot][64] += 10
        food_coord.pop(index_of_victim)                         # удаляем жертву из координат
        cells[xy[0]][xy[1]].configure(background=background)


def watch(side, index_of_bot):
    x, y = c_live[index_of_bot][0], c_live[index_of_bot][1]
    xy = d.get(side-15)
    xy[0] += x
    xy[1] += y
    ans = 0                         # 0 - empty, 1 - enemy, 2 - food, 3 - poison
    if xy in c_live:
        ans = 1
    elif xy in food_coord:
        ans = 2
    return ans


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


