from tkinter import *
import time
from random import randrange, shuffle

def crt_cell():                                                         #создание сетки отображения
    global cells
    cells = [[Label(text=f'     ', width=2, height=1, background=background) for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            cells[i][j].place(x=indent+i*21, y=indent+j*22)


def crt_live(count):                                                    #создание организмов
    global live, c_live, n_live, n
    n = count
    live = [[randrange(0, len_of_code) for i in range(len_of_code)] for j in range(n)]      #[0..63]

    for j in range(n):                                                  #добавление хп в 65е значение в списке генома
        live[j].append(start_hp)

    c_live = []                                                         #координаты живых клеток
    j = 0
    while j < n:
        xy = [randrange(0, size), randrange(0, size)]
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
    while i < count_of_food:
        xy = [randrange(0, size), randrange(0, size)]
        if not(xy in c_live) and not(xy in food_coord):
            food_coord.append(xy)
            i += 1
            cells[xy[0]][xy[1]].configure(background='green')


def move(side, index_of_bot):                                   #для всех функций стороны перепутаны, но задействованы все
    x, y = c_live[index_of_bot][0], c_live[index_of_bot][1]
    _ = d.get(side)                                            #d = {0: [1, 0], 1: [1, 1], 2: [1, -1], 3: [0, 1], 4: [0, -1], 5: [-1, 0], 6: [-1, 1], 7: [-1, -1]}
    xy = _.copy()
    old_x, old_y = x, y
    flag = True
    if xy[0] + x >= size:
        x = 0
        flag = False
    elif xy[0] + x < 0:
        x = size - 1
        flag = False

    if xy[1] + y >= size:                                       #ограничение верх-низ
        flag = False
    elif xy[1] + y < 0:
        flag = False

    if flag:
        x += xy[0]
        y += xy[1]

    if xy not in c_live:
        cells[old_x][old_y].configure(background=background)
        c_live[index_of_bot] = [x, y]
        cells[x][y].configure(background='red')


def eat(side, index_of_bot):
    x, y = c_live[index_of_bot][0], c_live[index_of_bot][1]
    _ = d.get(side - 8)                                            #d = {0: [1, 0], 1: [1, 1], 2: [1, -1], 3: [0, 1], 4: [0, -1], 5: [-1, 0], 6: [-1, 1], 7: [-1, -1]}
    xy = _.copy()
    xy_of_victim = [x+xy[0], y+xy[1]]
    if xy_of_victim in c_live:                                                      #поиск жертвы в виде бота
        index_of_victim = c_live.index(xy_of_victim)
        live[index_of_bot][len_of_code] += live[index_of_victim][len_of_code]       # забирает жизнь жертвы
        c_live.pop(index_of_victim)                                                 # удаляем жертву из координат
        cells[xy_of_victim[0]][xy_of_victim[1]].configure(background=background)
        live.pop(index_of_victim)
    elif xy_of_victim in food_coord:                                                #поиск жертвы в виде еды
        index_of_victim = food_coord.index(xy_of_victim)
        live[index_of_bot][len_of_code + 1] += 10
        food_coord.pop(index_of_victim)                                             # удаляем жертву из координат
        cells[xy_of_victim[0]][xy_of_victim[1]].configure(background=background)


def watch(side, index_of_bot):
    x, y = c_live[index_of_bot][0], c_live[index_of_bot][1]
    _ = d.get(side - 16)
    xy = _.copy()
    xy_check = [x+xy[0], y+xy[1]]
    ans = 0                                             # 0 - empty, 1 - enemy, 2 - food, 3 - poison
    if xy_check in c_live:
        ans = 1
    elif xy_check in food_coord:
        ans = 2
    return ans


def step():
    pull = n_live                                       #очередь из индексов ботов
    shuffle(pull)
    rdy = 0                                             #счётчик готовности  while rdy<n
    c = [0 for _ in range(len(n_live))]                 #УТК для каждого бота
    while rdy < n:
        for k in pull:                                  #очередь
            if c[k]>63:                                 #не даём выходить из пула команд 0..63
                c[k] -= 63
            if 0 <= live[k][c[k]] <= 7:                 #live[k] - список 0-64
                move(live[k][c[k]], k)                  #движение
                rdy += 1
                live[k][64] -= 1                        #1хп в ход
                pull.pop(k)
            elif 8 <= live[k][c[k]] <= 15:              #есть
                eat(live[k][c[k]], k)
                rdy += 1
                live[k][len_of_code] -= 1
                pull.pop(k)
            elif 16 <= live[k][c[k]] <= 23:
                if watch(live[k][c[k]], k) == 0:
                    c[k] += 1
                elif watch(live[k][c[k]], k) == 1:
                    c[k] += 2
                elif watch(live[k][c[k]], k) == 2:
                    c[k] += 3
            elif 24 <= live[k][c[k]] <= 31:
                None #деление

background = '#9c9192'
d = {0: [1, 0], 1: [1, 1], 2: [1, -1], 3: [0, 1], 4: [0, -1], 5: [-1, 0], 6: [-1, 1], 7: [-1, -1]}

len_of_code = 64
start_hp = 10

window = Tk()
window.title("Симулирование эволюции")
window.geometry('1600x1600')

size = 36                       # size x size count of cells
indent = 50

crt_cell()
crt_live(int(input('Введите количество организмов:')))
create_food(10)

while True:                     #test move
    for i in range(8):
        time.sleep(0.33)
        move(1, 1)
        window.update()


