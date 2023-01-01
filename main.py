from tkinter import *
import time
from random import randrange, shuffle

background = '#9c9192'
d = {0: [1, 0], 1: [1, 1], 2: [1, -1], 3: [0, 1], 4: [0, -1], 5: [-1, 0], 6: [-1, 1], 7: [-1, -1]}

len_of_code = 64
start_hp = 10

window = Tk()
window.title("Симулирование эволюции")
window.geometry('1900x1600')


def crt_cell(x, y):                   #создание поля отображения
    global cells, x_size, y_size
    x_size = x
    y_size = y
    cells = [[Label(window, text=f'', width=2, height=1, background='white') for j in range(y_size)] for i in range(x_size)]
    for j in range(y_size):
        for i in range(x_size):
            cells[i][j].grid(row=i, column=j)


def crt_live(count=10):                                                    #создание организмов
    global live
    #live - список словарей для каждого организма
    n = count
    hp = 10
    for _ in range(count):
        flag = True
        while flag:
            xy = [randrange(0, x_size), randrange(0, y_size)]
            if cells[xy[0]][xy[1]]['background'] == 'white':
                flag = False
                color = 'red'
                cells[xy[0]][xy[1]]['background'] = color
        live.append({
            'gen': [randrange(0, 16) for i in range(len_of_code)],#[randrange(0, len_of_code) for i in range(len_of_code)],
            'hp': hp,
            'coord': xy,
            'color': color,
            'UTK': 0,
            'anticycle': 0
        })


def copy_live():            #0123 4567
    hp = 10
    _ = live.copy()
    new_live = _
    for bots in new_live:
        flag = True
        while flag:
            xy = [randrange(0, x_size), randrange(0, y_size)]
            if cells[xy[0]][xy[1]]['background'] == 'white':
                flag = False
                color = 'red'
                cells[xy[0]][xy[1]]['background'] = color
        bots['coord'] = xy
    live.extend(new_live)



#24..31
def cell_division(bot, side):
    coord = bot['coord'].copy()
    _ = d.get(side - 24)                                            #d = {0: [1, 0], 1: [1, 1], 2: [1, -1], 3: [0, 1], 4: [0, -1], 5: [-1, 0], 6: [-1, 1], 7: [-1, -1]}
    xy = _.copy()
    x, y = coord[0], coord[1]
    flag = True
    if xy[0] + x == x_size:
        x = 0
        flag = False
    elif xy[0] + x < 0:
        x = x_size - 1
        flag = False

    if xy[1] + y == y_size:                                       #ограничение верх-низ
        flag = False
    elif xy[1] + y < 0:
        flag = False

    if flag:
        x += xy[0]
        y += xy[1]

    if cells[x][y]['background'] == 'white':
        live.append(mutation(bot))
        cells[x][y].configure(background='red')                 #Доработать цвет


def mutation(old):
    #кол-во исходов из 100
    chance_of_mutation = 20
    #кол-во изменений
    power_of_mutation = 1
    new = old.copy()
    if randrange(0, 100) in range(chance_of_mutation):
        for i in range(power_of_mutation):
            index_of_mutation = randrange(0, 64)
            mut = randrange(0, 2)*(-1)
            if new['gen'][index_of_mutation] + mut < 0:
                new['gen'][index_of_mutation] = 64
            elif new['gen'][index_of_mutation] + mut > 63:
                new['gen'][index_of_mutation] = 0
            else:
                new['gen'][index_of_mutation] += randrange(0, 2)*(-1)
    new['hp'] = 5
    return new


def create_food(count_of_food):
    global food_coord
    if count_of_food == 'full':
        for j in range(y_size):
            for i in range(x_size):
                if cells[i][j]['background'] == 'white':
                    cells[i][j]['background'] = 'green'
    else:
        i = 0
        while i < count_of_food:
            xy = [randrange(0, x_size), randrange(0, y_size)]
            if cells[xy[0]][xy[1]]['background'] == 'white':
                cells[xy[0]][xy[1]].configure(background='green')
                i += 1

#0..7
def move(bot, side):                                  #для всех функций стороны перепутаны, но задействованы все
    coord = bot['coord'].copy()
    _ = d.get(side)                                            #d = {0: [1, 0], 1: [1, 1], 2: [1, -1], 3: [0, 1], 4: [0, -1], 5: [-1, 0], 6: [-1, 1], 7: [-1, -1]}
    xy = _.copy()
    x, y = coord[0], coord[1]
    flag = True
    if xy[0] + x == x_size:
        x = 0
        flag = False
    elif xy[0] + x < 0:
        x = x_size - 1
        flag = False

    if xy[1] + y == y_size:                                       #ограничение верх-низ
        flag = False
    elif xy[1] + y < 0:
        flag = False

    if flag:
        x += xy[0]
        y += xy[1]

    if cells[x][y]['background'] == 'white':
        cells[coord[0]][coord[1]]['background'] = 'white'
        bot['coord'] = [x, y]
        cells[x][y].configure(background='red')                 #тут доработать с цветом

#8..15
def eat(bot, side):
    coord = bot['coord'].copy()
    _ = d.get(side - 8)                                            #d = {0: [1, 0], 1: [1, 1], 2: [1, -1], 3: [0, 1], 4: [0, -1], 5: [-1, 0], 6: [-1, 1], 7: [-1, -1]}
    xy = _.copy()
    x, y = coord[0], coord[1]

    flag = True
    if xy[0] + x == x_size:
        x = 0
        flag = False
    elif xy[0] + x < 0:
        x = x_size - 1
        flag = False

    if xy[1] + y == y_size:                                       #ограничение верх-низ
        flag = False
    elif xy[1] + y < 0:
        flag = False

    if flag:
        x += xy[0]
        y += xy[1]

    if not (cells[x][y]['background'] == 'white'):

        if cells[x][y]['background'] == 'green':                            #поиск жертвы в виде еды
            bot['hp'] += 5
            cells[x][y]['background'] = 'white'

        else:                                                               #значит бот..
            for bots in live:
                if bots['coord'] == [x, y]:
                    cells[x][y]['background'] = 'white'
                    bot['hp'] += bots['hp']
                    live.remove(bots)
                    break

 #16..23
def watch(bot, side):
    coord = bot['coord'].copy()
    _ = d.get(side - 16)                                            #d = {0: [1, 0], 1: [1, 1], 2: [1, -1], 3: [0, 1], 4: [0, -1], 5: [-1, 0], 6: [-1, 1], 7: [-1, -1]}
    xy = _.copy()
    x, y = coord[0], coord[1]

    flag = True
    if xy[0] + x == x_size:
        x = 0
        flag = False
    elif xy[0] + x < 0:
        x = x_size - 1
        flag = False

    if xy[1] + y == y_size:                                       #ограничение верх-низ
        flag = False
    elif xy[1] + y < 0:
        flag = False

    if flag:
        x += xy[0]
        y += xy[1]

    ans = 1                                             # 0 - empty, 1 - enemy, 2 - food, 3 - poison
    if cells[x][y]['background'] == 'white':
        ans = 0
    elif cells[x][y]['background'] == 'green':
        ans = 2
    return ans


def step():
    global num_steps
    _ = live.copy()
    pull = _
    shuffle(pull)
    rdy = 0
    n = len(pull)

    for bots in pull:
        # bots['UTK'] = 0
        bots['anticycle'] = 0

    while rdy < n:
        n = len(pull)
        for bots in pull:                                #очередь
            if bots['anticycle'] >= 15:
                rdy += 1
                bots['hp'] += -1                         # 1хп в ход
                bots['UTK'] += 1
                pull.remove(bots)
                continue

            if bots['UTK'] > 63:                                 #не даём выходить из пула команд 0..63
                bots['UTK'] -= 63

            k = bots['UTK']

            if 0 <= bots['gen'][k] <= 7:                 #live[k] - список 0-64
                move(bots, bots['gen'][k])                  #движение
                rdy += 1
                bots['hp'] += -1                        #1хп в ход
                bots['UTK'] += 1
                pull.remove(bots)
            elif 8 <= bots['gen'][k] <= 15:              #есть
                eat(bots, bots['gen'][k])
                rdy += 1
                bots['hp'] += -1
                bots['UTK'] += 1
                pull.remove(bots)
            else:
                bots['anticycle'] += 1
                if 16 <= bots['gen'][k] <= 23:             #смотреть, УТК empty+=1 enemy+=2 eat+=3
                    _ = watch(bots, bots['gen'][k])
                    if _ == 0:
                        bots['UTK'] += 1
                    elif _ == 1:
                        bots['UTK'] += 2
                    elif _ == 2:
                        bots['UTK'] += 3
                elif 24 <= bots['gen'][k] <= 31:
                    cell_division(bots, bots['gen'][k])
                    rdy += 1
                    bots['hp'] += -2                        #-2хп за деление
                    pull.remove(bots)
                elif bots['gen'][k] == 32:                   #проверка хп + ветвление
                    if bots['hp'] > int((bots['gen'][k+1]+1)*start_hp/len_of_code):
                        bots['UTK'] += 1
                    else:
                        bots['UTK'] += 2
                else:                                       #значения выше 32 повышают УТК
                    bots['UTK'] += bots['gen'][k]

    for bots in live:
        if bots['hp'] < 0:
            x = bots['coord'][0]
            y = bots['coord'][1]
            cells[x][y].configure(background='white')
            live.remove(bots)
    num_steps += 1


def main():
    # create_food(20)
    flag = False

    if flag:
        flag = False
    else:
        flag = True

    while flag:
        if num_steps % 20 == 0 and num_steps > 0:
            create_food(5)
            flag = False
        step()
        step_lbl.configure(text=f"Count of steps:{num_steps-1}")
        live_lbl.configure(text=f'Count of lives:{len(live)}')
        time.sleep(0.1)
        window.update()




size = 36 # size x size count of cells
live = []

crt_cell(50, 80)
crt_live(int(input('Введите количество организмов:')))
create_food('full')
# create_food(10)

step_btn = Button(text='STEP', command=main)
step_btn.grid(row=51, column=81)
#
food_btn = Button(text='Create_Live', command=crt_live)
food_btn.grid(row=52, column=81)
food_btn = Button(text='copy', command=copy_live)
food_btn.grid(row=53, column=81)
num_steps = 0

step_lbl = Label(window, font=("Arial Bold", 14), text='start')
step_lbl.place(x=1600, y=200)
live_lbl = Label(window, font=("Arial Bold", 14), text=f'Count of lives:{len(live)}')
live_lbl.place(x=1600, y=400)

window.mainloop()



