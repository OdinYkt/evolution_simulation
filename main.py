from tkinter import *
import time
from datetime import datetime
from random import randrange, shuffle, choice
import pathlib
from pathlib import Path


def life_to_txt():                              #переделать
    name = str(datetime.now())
    for i in ':-.':
        name = name.replace(i, '')
    name = name.strip()
    name = name + '.txt'

    path = Path(pathlib.Path().absolute(), 'txt_live', name)
    with open(path, 'w') as file:
        for i in live:
            file.write(str(i) + '\n')

def txt_to_life(name):
    path = Path(pathlib.Path().absolute(), 'txt_live', name)
    live.clear()
    with open(path, 'r') as file:
        for lines in file:
            live.append(eval(lines))
    for bots in live:
        xy = bots['coord']
        cells[xy[0]][xy[1]]['background'] = bots['color']

def get_hex(rgb):
    return "#%02x%02x%02x" % rgb


def get_rgb(hex):
    h = hex.lstrip('#')
    ans = (tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)))
    return ans


def crt_cell(x, y):                   #создание поля отображения
    global x_size, y_size
    x_size = x
    y_size = y
    cells = [[Label(window, text=f'', width=2, height=1, background='white') for j in range(y_size)] for i in range(x_size)]
    for j in range(y_size):
        for i in range(x_size):
            cells[i][j].grid(row=i, column=j)
    return cells


def crt_live(count):                                                    #создание организмов
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
                start_color = get_hex((200, 200, 200))
                cells[xy[0]][xy[1]]['background'] = start_color
        live.append({
            'gen': [randrange(0, len_of_code) for i in range(len_of_code)],     #[randrange(0, len_of_code) for i in range(len_of_code)],
            'energy': energy,
            'coord': xy,
            'color': start_color,
            'UTK': 0,
            'anticycle': 0,
            'age': 0,
            'r': 200,
            'g': 200,
            'b': 200
        })


#24..31
def cell_division(bot, side, start_utk = 0,mutation_on = True):
    ans = 1
    coord = bot['coord'].copy()
    _ = d.get(side)                                            #d = {0: [1, 0], 1: [1, 1], 2: [1, -1], 3: [0, 1], 4: [0, -1], 5: [-1, 0], 6: [-1, 1], 7: [-1, -1]}
    xy = _.copy()
    x, y = coord[0], coord[1]
    flag = True
    ch_of_mut = 25
    ch_if_cell = 0

    x += xy[0]
    y += xy[1]

    if cells[x][y]['background'] == 'white' and bot['energy'] >= 20:
        if mutation_on:
            new_bot = mutation(bot, ch_of_mut)
        else:
            new_bot = mutation(bot, ch_if_cell)

        new_bot['coord'] = [x, y]
        new_bot['UTK'] = start_utk
        cells[x][y]['background'] = new_bot['color']
        live.append(new_bot)
        ans = 2
    return ans


def mutation(old, chance):
    #кол-во исходов из 100
    chance_of_mutation = chance
    #кол-во изменений
    power_of_mutation = 1
    if old['energy'] > 200:
        power_of_mutation = 3
        chance += 10
    new = old.copy()
    if randrange(0, 100) in range(chance_of_mutation):
        for i in range(power_of_mutation):
            index_of_mutation = randrange(0, len_of_code-1)
            mut = choice([-power_of_mutation, power_of_mutation])
            if new['gen'][index_of_mutation] + mut < 0:
                new['gen'][index_of_mutation] = 63
            elif new['gen'][index_of_mutation] + mut > 63:
                new['gen'][index_of_mutation] = 0
            else:
                new['gen'][index_of_mutation] += mut
        new['r'] = 180
        new['g'] = 180
        new['b'] = 180
        new['color'] = get_hex((180, 180, 180))
    else:
        new['r'] = 200
        new['g'] = 200
        new['b'] = 200
        new['color'] = get_hex((200, 200, 200))
    new['energy'] = 15
    new['age'] = 0
    return new


def create_food(count_of_food=10):
    food_coord = []
    if count_of_food == 'full':
        for j in range(y_size):
            for i in range(x_size):
                if i == 0 or j == 0 or i == 49 or j == 79:
                    cells[i][j]['background'] = food_color
                    cells[i][j]['text'] = '.'
                    food_coord.append([i,j])
    else:
        i = 0
        while i < count_of_food:
            xy = [randrange(0, x_size), randrange(0, y_size)]
            if cells[xy[0]][xy[1]]['background'] == 'white':
                cells[xy[0]][xy[1]]['background'] = food_color
                cells[xy[0]][xy[1]]['text'] = '.'
                i += 1
                food_coord.append([xy[0],xy[1]])
    return food_coord

def photosynth(bot):
    if 50 > bot['coord'][0] > 30 or 20 > bot['coord'][0] > 0:
        bot['energy'] += 30
        # bot['age'] -= 5
        ans = 1
    else:
        # bot['energy'] += 2
        ans = 2

    if ans == 1:
        change_g = 4
        if bot['r'] - change_g <= 30:
            bot['r'] = 30
        else:
            bot['r'] -= change_g
        if bot['b'] - change_g <= 30:
            bot['b'] = 30
        else:
            bot['b'] -= change_g
        if bot['g'] + change_g >= 255:
            bot['g'] = 255
        else:
            bot['g'] += change_g
        bot['color'] = get_hex((bot['r'], bot['g'], bot['b']))

    return ans


def move(bot, side):
    coord = bot['coord'].copy()
    _ = d.get(side)
    xy = _.copy()
    x, y = coord[0], coord[1]

    x += xy[0]
    y += xy[1]

    ans = 1
    if cells[x][y]['background'] == 'white':
        cells[coord[0]][coord[1]]['background'] = 'white'
        bot['coord'] = [x, y]
        cells[x][y]['background'] = bot['color']
    else:
        ans = watch(bot, side) + 1
    return ans


def eat(bot, side):
    global live
    coord = bot['coord'].copy()
    _ = d.get(side)
    xy = _.copy()
    x, y = coord[0], coord[1]
    result = 1

    x += xy[0]
    y += xy[1]

    if not (cells[x][y]['background'] == 'white'):
        if cells[x][y]['background'] == food_color:                            #поиск жертвы в виде еды
            result = 2
            bot['energy'] += 5
            # bot['age'] -= 1
            # if bot['age'] < 0:
            #     bot['age'] = 0

            change_b = 5
            if bot['b'] + change_b >= 255:
                bot['b'] = 255
            else:
                bot['b'] += change_b

        else:                                                               #значит бот..
            dif = []
            for bots in live:
                if bots['coord'] == [x, y]:

                    for i in range(len(bots['gen'])):
                        if bots['gen'][i] - bot['gen'][i] != 0:
                            dif.append(bots['gen'][i] - bot['gen'][i])
                    if dif == [1] or dif == [-1] or dif == []:
                        result = 3
                        break
                    cells[x][y]['background'] = 'white'
                    bot['energy'] += int(bots['energy']/10) + 20
                    # bot['age'] -= 1
                    live.remove(bots)
                    move(bot, side)
                    change_r = 50
                    if bot['g'] - change_r <= 30:
                        bot['g'] = 30
                    else:
                        bot['g'] -= change_r
                    if bot['b'] - change_r <= 30:
                        bot['b'] = 30
                    else:
                        bot['b'] -= change_r
                    if bot['r'] + change_r >= 255:
                        bot['r'] = 255
                    else:
                        bot['r'] += change_r

                    result = 4
                    break

    return result


def watch(bot, side):
    coord = bot['coord'].copy()
    _ = d.get(side)
    xy = _.copy()
    x, y = coord[0], coord[1]

    x += xy[0]
    y += xy[1]

    ans = 3                                       # 1 - empty, 2 - food, 3 - wall, 4 - enemy,  5 - ally

    if cells[x][y]['background'] == 'white':
        ans = 1
    elif cells[x][y]['background'] == food_color:
        ans = 2
    else:
        dif = []
        for bots in live:
            if bots['coord'] == [x, y]:
                for i in range(len(bots['gen'])):
                    if bots['gen'][i] - bot['gen'][i] != 0:
                        dif.append(bots['gen'][i] - bot['gen'][i])
                break
        if dif == [1] or dif == [-1] or dif == []:
            ans = 4

    return ans


def clear_cells(cells):
    global live, x_size, y_size
    colored_cells = []
    if live:
        for bots in live:
            colored_cells.append(bots['coord'])
    colored_cells.extend(food_coord)
    for j in range(y_size):
        for i in range(x_size):
            if [i, j] not in colored_cells:
                cells[i][j]['background'] = 'white'


def step():
    global num_steps
    _ = live.copy()
    pull = _
    shuffle(pull)

    rdy = 0         #counter for ready of bots
    n = len(pull)

    for bots in pull:           #сброс счётчика цикла
        bots['anticycle'] = 0

    while rdy < n:          #шаг кончается, когда все боты закончили команды
        n = len(pull)
        for bots in pull:
            if bots['anticycle'] >= 30:             #бот также может зависнуть в цикле, для этого проверяем счётчик
                rdy += 1
                bots['UTK'] += 1
                pull.remove(bots)
                continue

            if bots['UTK'] >= len_of_code:            #не даём выходить УТК из списка команд 0..63
                bots['UTK'] -= len_of_code

            k = bots['UTK']             #для удобства
            # bots['gen']  - список 0-64
            if 0 <= bots['gen'][k] <= 7:
                ans = move(bots, bots['gen'][k])

                rdy += 1
                bots['UTK'] += ans
                pull.remove(bots)
            elif 8 <= bots['gen'][k] <= 15:              #есть
                ans = eat(bots, bots['gen'][k] - 8)

                rdy += 1
                bots['UTK'] += ans
                pull.remove(bots)
            elif bots['gen'][k] == 24:
                ans = photosynth(bots)

                rdy += 1
                bots['UTK'] += ans
                pull.remove(bots)
            elif bots['gen'][k] == 26:
                k_next = k + 1
                k_next_ = k + 2
                if k_next >= len_of_code:
                    k_next -= len_of_code
                if k_next_ >= len_of_code:
                    k_next_ -= len_of_code
                ans = cell_division(bots, int(bots['gen'][k_next] % 8), bots['gen'][k_next_])

                rdy += 1
                if ans == 2:
                    bots['energy'] -= 20
                bots['UTK'] += ans
                pull.remove(bots)
            elif bots['gen'][k] == 27:
                bots['age'] -= 5
                rdy += 1
                bots['UTK'] += 1
                pull.remove(bots)
            else:
                bots['anticycle'] += 1
                if 16 <= bots['gen'][k] <= 23:             #смотреть, УТК empty+=1 enemy+=2 eat+=3
                    ans = watch(bots, bots['gen'][k] - 16)
                    bots['UTK'] += ans
                elif bots['gen'][k] == 25:                  #проверка хп
                    k_next = k + 1
                    if k_next > (len_of_code-1):
                        k_next -= (len_of_code-1)

                    if bots['energy'] > int(bots['gen'][k_next]*500/63):
                        bots['UTK'] += 2
                    else:
                        bots['UTK'] += 3
                elif bots['gen'][k] == 28:                  #проверка возраста
                    k_next = k + 1
                    if k_next > (len_of_code-1):
                        k_next -= (len_of_code-1)

                    if bots['age'] > int(bots['gen'][k_next]*100/63):
                        bots['UTK'] += 2
                    else:
                        bots['UTK'] += 3
                else:                                       #значения повышают УТК
                    bots['UTK'] += bots['gen'][k]

    for bots in live:
        if bots['age'] < 0:
            bots['age'] = 0

        bots['age'] += 1

        bots['energy'] -= step_energy
        x = bots['coord'][0]
        y = bots['coord'][1]
        if bots['energy'] >= 250:
            ans = cell_division(bots, randrange(0, 8), randrange(0, 127))
            if ans == 2:                              #принудительное деление в случайную сторону
                bots['energy'] -= 20

        if bots['energy'] <= 0 or bots['energy'] >= 500 or bots['age'] >= 200:
            cells[x][y]['background'] = 'white'
            live.remove(bots)
    for bots in live:
        x = bots['coord'][0]
        y = bots['coord'][1]
        bots['color'] = get_hex((bots['r'], bots['g'], bots['b']))
        cells[x][y]['background'] = bots['color']

    num_steps += 1

def statistic(_live):
    max_energy = 0
    avg_energy = 0
    max_age = 0
    min_age = 0
    summ_energy = 0
    if live:
        min_age = live[-1]['age']
        for bots in _live:
            if bots['energy'] > max_energy:
                max_energy = bots['energy']
            summ_energy += bots['energy']
            if bots['age'] > max_age:
                max_age = bots['age']
            if bots['age'] < min_age:
                min_age = bots['age']
        avg_energy = int(summ_energy/len(_live))
    stats = (max_energy, avg_energy, max_age,  min_age)
    return stats


def main():
    global num_steps, num_world
    step()
    stats = statistic(live)

    step_lbl.configure(text=f"Count of steps:{num_steps - 1}")
    live_lbl.configure(text=f'Count of lives:{len(live)}')
    max_energy_lbl['text'] = f'Max energy: {stats[0]}'
    avg_energy_lbl['text'] = f'Avg energy: {stats[1]}'
    max_age_lbl['text'] = f'Max age: {stats[2]}'
    min_age_lbl['text'] = f'Min age: {stats[3]}'
    if len(live) < 250:
        time.sleep(0.05)
    if num_steps % 150 == 0:
        clear_cells(cells)
    if len(live) == 0:
        crt_live(1500)
        num_steps = 0
        num_world += 1
        world_lbl.configure(text=f'# of world:{num_world}')
    window.update()


def new_world():
    global num_steps, num_world
    live.clear()
    clear_cells(cells)
    crt_live(1500)
    num_steps = 0
    num_world += 1
    world_lbl.configure(text=f'# of world:{num_world}')


def button():
    global start_simulation
    if start_simulation:
        start_simulation = False
    else:
        start_simulation = True

    while start_simulation:
        main()
        continue


#dict for move(), eat() and watch()
d = {0: [1, 0], 1: [1, 1], 2: [1, -1], 3: [0, 1], 4: [0, -1], 5: [-1, 0], 6: [-1, 1], 7: [-1, -1]}

#create window
window = Tk()
window.title("Симулирование эволюции")
window.geometry('1920x1600')
#create cell
cells = crt_cell(50, 80)
live = []
###############
#buttons and labels
step_btn = Button(text='START/STOP',
                  command=button
                  )


txt_btn = Button(text='copy to txt',
                 command=life_to_txt
                 )
new_world_btn = Button(text='new world',
                 command=new_world
                 )
###############
step_lbl = Label(window,
                 font=("Arial Bold", 14),
                 text='Count of steps'
                 )

world_lbl = Label(window,
                 font=("Arial Bold", 14),
                 text='# of world: 0'
                 )

max_energy_lbl = Label(window,
                 font=("Arial Bold", 12),
                 text='max_energy: 0'
                 )
avg_energy_lbl = Label(window,
                 font=("Arial Bold", 12),
                 text='avg_energy: 0'
                 )
max_age_lbl = Label(window,
                 font=("Arial Bold", 12),
                 text='max_age: 0'
                 )
min_age_lbl = Label(window,
                 font=("Arial Bold", 12),
                 text='min_age: 0'
                 )
live_lbl = Label(
    window,
    font=("Arial Bold", 14),
    text=f'Count of lives:{len(live)}'
    )
###############
step_btn.grid(row=51, column=81)
txt_btn.grid(row=52, column=81)
new_world_btn.grid(row=51, column=82)
world_lbl.place(x=1600, y=100)
step_lbl.place(x=1600, y=200)

live_lbl.place(x=1600, y=400)
max_energy_lbl.place(x=1600, y=440)
avg_energy_lbl.place(x=1600, y=465)
min_age_lbl.place(x=1600, y=490)
max_age_lbl.place(x=1600, y=515)
###############
#rules
step_energy = 1
food_color = get_hex((150, 150, 255))
len_of_code = 64
start_hp = 10

print('Добро пожаловать в симуляцию эволюции v0.1')

food_coord = create_food('full')
num_steps = 0
num_world = 0


crt_live(int(input('Введите количество организмов:')))
print('Создание окна отображения(5-10 сек)')

start_simulation = False
window.mainloop()





