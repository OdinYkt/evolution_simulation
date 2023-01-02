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
    energy = 10
    for _ in range(count):
        flag = True
        while flag:
            xy = [randrange(0, x_size), randrange(0, y_size)]
            if cells[xy[0]][xy[1]]['background'] == 'white':
                flag = False
                color = 'red'
                cells[xy[0]][xy[1]]['background'] = color
                print(f'{xy} new red cell')
        live.append({
            'gen': [24 for i in range(len_of_code)],     #[randrange(0, len_of_code) for i in range(len_of_code)],
            'energy': energy,
            'coord': xy,
            'color': color,
            'UTK': 0,
            'anticycle': 0,
            'age': 0
        })


def copy_live():            #0123 4567
    global live
    energy = 10
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
                print(f'{xy} new red cell')
        bots['coord'] = xy
        bots['energy'] = energy
        bots['age'] = 0
    live.extend(new_live)



#24..31
def cell_division(bot, side):
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
        new_bot = mutation(bot)
        new_bot['coord'] = [x, y]
        live.append(new_bot)
        cells[x][y].configure(background='red')                 #Доработать цвет
        print(f'{[x, y]} new red cell, {num_steps}')


def mutation(old):
    #кол-во исходов из 100
    chance_of_mutation = 50
    #кол-во изменений
    power_of_mutation = 2
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
    new['energy'] = 10
    new['age'] = 0
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


def photosynth(bot):
    # coord = bot['coord'].copy()
    bot['energy'] += 2


#0..7
def move(bot, side):                                  #для всех функций стороны перепутаны, но задействованы все
    coord = bot['coord'].copy()
    _ = d.get(side)                                            #d = {0: [1, 0], 1: [1, 1], 2: [1, -1], 3: [0, 1], 4: [0, -1], 5: [-1, 0], 6: [-1, 1], 7: [-1, -1]}
    xy = _.copy()
    x, y = coord[0], coord[1]
    x_flag = True
    y_flag = True
    if xy[0] + x == x_size:
        x = 0
        x_flag = False
    elif xy[0] + x < 0:
        x = x_size - 1
        x_flag = False

    if xy[1] + y == y_size:                                       #ограничение верх-низ
        y_flag = False
    elif xy[1] + y < 0:
        y_flag = False

    if x_flag and y_flag:
        x += xy[0]
        y += xy[1]

    ans = watch(bot, side)
    if cells[x][y]['background'] == 'white' and y_flag:
        cells[coord[0]][coord[1]]['background'] = 'white'
        bot['coord'] = [x, y]
        cells[x][y].configure(background='red')                 #тут доработать с цветом
        # print(f'{[x,y]} new red cell')
    return ans


#8..15
def eat(bot, side):
    coord = bot['coord'].copy()
    _ = d.get(side)                                            #d = {0: [1, 0], 1: [1, 1], 2: [1, -1], 3: [0, 1], 4: [0, -1], 5: [-1, 0], 6: [-1, 1], 7: [-1, -1]}
    xy = _.copy()
    x, y = coord[0], coord[1]
    result = 1
    x_flag = True
    y_flag = True
    if xy[0] + x == x_size:
        x = 0
        x_flag = False
    elif xy[0] + x < 0:
        x = x_size - 1
        x_flag = False

    if xy[1] + y == y_size:                                       #ограничение верх-низ
        y_flag = False
    elif xy[1] + y < 0:
        y_flag = False

    if y_flag and x_flag:
        x += xy[0]
        y += xy[1]

    if not (cells[x][y]['background'] == 'white') and y_flag:
        result = 2
        if cells[x][y]['background'] == 'green':                            #поиск жертвы в виде еды
            bot['energy'] += 5
            cells[x][y]['background'] = 'white'

        else:                                                               #значит бот..
            for bots in live:
                if bots['coord'] == [x, y]:
                    cells[x][y]['background'] = 'white'
                    bot['energy'] += bots['energy']
                    live.remove(bots)
                    break

    return result


 #16..23
def watch(bot, side):
    coord = bot['coord'].copy()
    _ = d.get(side)                                            #d = {0: [1, 0], 1: [1, 1], 2: [1, -1], 3: [0, 1], 4: [0, -1], 5: [-1, 0], 6: [-1, 1], 7: [-1, -1]}
    xy = _.copy()
    x, y = coord[0], coord[1]

    x_flag = True
    y_flag = True
    if xy[0] + x == x_size:
        x = 0
        x_flag = False
    elif xy[0] + x < 0:
        x = x_size - 1
        x_flag = False

    if xy[1] + y == y_size:                                       #ограничение верх-низ
        y_flag = False
    elif xy[1] + y < 0:
        y_flag = False

    if x_flag and y_flag:
        x += xy[0]
        y += xy[1]

    ans = 2                                             # 1 - empty, 2 - enemy, 3 - food, 4 - wall

    if cells[x][y]['background'] == 'white' and y_flag:
        ans = 1
    elif cells[x][y]['background'] == 'green' and y_flag:
        ans = 3
    elif not y_flag:
        ans = 4
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
                bots['energy'] += -step_energy                         # 1хп в ход
                bots['UTK'] += 1
                pull.remove(bots)
                continue

            if bots['UTK'] > 63:                                 #не даём выходить из пула команд 0..63
                bots['UTK'] -= 64

            k = bots['UTK']

            if 0 <= bots['gen'][k] <= 7:                 #live[k] - список 0-64
                ans = move(bots, bots['gen'][k])                  #движение

                rdy += 1
                bots['energy'] += -1                        #1хп в ход
                bots['UTK'] += ans
                pull.remove(bots)
            elif 8 <= bots['gen'][k] <= 15:              #есть
                ans = eat(bots, bots['gen'][k] - 8)

                rdy += 1
                bots['energy'] += -1
                bots['UTK'] += ans
                pull.remove(bots)
            elif bots['gen'][k] == 24:
                photosynth(bots)

                rdy += 1
                bots['energy'] += -1
                bots['UTK'] += 1
                pull.remove(bots)
            else:
                bots['anticycle'] += 1
                if 16 <= bots['gen'][k] <= 23:             #смотреть, УТК empty+=1 enemy+=2 eat+=3
                    ans = watch(bots, bots['gen'][k] - 16)
                    bots['UTK'] += ans
                elif bots['gen'][k] == 25:
                    k_next = k + 1
                    if k+1 > 63:
                        k_next -= 63

                    if bots['energy'] >= (bots['gen'][k_next]+1/64)*10:
                        bots['UTK'] += 1
                    else:
                        bots['UTK'] += 2
                else:                                       #значения выше 26(!) повышают УТК
                    bots['UTK'] += bots['gen'][k]

    for bots in live:
        bots['age'] += 1
        if bots['energy'] <= 0 or bots['age'] >= 80:
            x = bots['coord'][0]
            y = bots['coord'][1]
            cells[x][y].configure(background='white')
            live.remove(bots)
        elif bots['energy'] >= 40:
            bots['energy'] -= 20
            cell_division(bots, randrange(0, 8))
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
step_energy = 1

crt_cell(50, 80)
crt_live(int(input('Введите количество организмов:')))
create_food(40)
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



