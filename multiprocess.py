from main import *

zones = [[0, 10], [10, 20], [20, 30], [30, 40], [40, 50], [50, 60], [60, 70], [70, 79]]
def step(zone):
    current_zone = zones[zone]
    start_y = current_zone[0]
    end_y = current_zone[1]
    _ = live.copy()
    pull = _
    for bots in pull:
        if bots['coord'][1] not in range(start_y, end_y+1):
            pull.remove(bots)
        if bots['rdy'] == 1:
            pull.remove(bots)

    shuffle(pull)
    n = len(pull)
    rdy = 0
    for bots in pull:                               #сброс счётчика цикла
        bots['anticycle'] = 0

    while rdy < n:                                  #шаг кончается, когда все боты закончили команды
        n = len(pull)
        for bots in pull:
            if bots['anticycle'] >= 15:             #бот также может зависнуть в цикле, для этого проверяем счётчик
                rdy += 1
                bots['energy'] -= step_energy       # 1хп в ход
                bots['UTK'] += 1
                pull.remove(bots)
                continue

            if bots['UTK'] > 63:                    #не даём выходить УТК из списка команд 0..63
                bots['UTK'] -= 64

            k = bots['UTK']                         #для удобства
            # bots['gen']  - список 0-64
            if 0 <= bots['gen'][k] <= 7:
                ans = move(bots, bots['gen'][k])

                rdy += 1
                bots['energy'] -= step_energy
                bots['UTK'] += ans
                pull.remove(bots)
            elif 8 <= bots['gen'][k] <= 15:              #есть
                ans = eat(bots, bots['gen'][k] - 8)

                rdy += 1
                bots['energy'] -= step_energy
                bots['UTK'] += ans
                pull.remove(bots)
            elif bots['gen'][k] == 24:
                ans = photosynth(bots)

                rdy += 1
                bots['energy'] -= step_energy
                bots['UTK'] += ans
                pull.remove(bots)
            elif bots['gen'][k] == 26:
                k_next = k + 1
                k_next_ = k + 2
                if k_next > 63:
                    k_next -= 63
                if k_next_ > 63:
                    k_next_ -= 63
                ans = cell_division(bots, int(bots['gen'][k_next] % 8), bots['gen'][k_next_])

                rdy += 1
                bots['energy'] += -10
                bots['UTK'] += ans
                pull.remove(bots)
            else:
                bots['anticycle'] += 1
                if 16 <= bots['gen'][k] <= 23:             #смотреть, УТК empty+=1 enemy+=2 eat+=3
                    ans = watch(bots, bots['gen'][k] - 16)
                    bots['UTK'] += ans
                elif bots['gen'][k] == 25:                  #проверка хп
                    k_next = k + 1
                    if k_next > 63:
                        k_next -= 63

                    if bots['energy'] >= bots['gen'][k_next]:
                        bots['UTK'] += 2
                    else:
                        bots['UTK'] += 3
                else:                                       #значения повышают УТК
                    bots['UTK'] += bots['gen'][k]

    # for bots in live:                                       #условия выживания бота
    #     bots['age'] += 1
    #     x = bots['coord'][0]
    #     y = bots['coord'][1]

    #     if bots['energy'] <= 0 or bots['age'] >= 100:
    #         cells[x][y]['background'] = 'white'
    #         live.remove(bots)
    #     elif bots['energy'] >= 60:              #принудительное деление в случайную сторону
    #         bots['energy'] -= 20
    #         cell_division(bots, randrange(0, 8))
    #     else:
    #         bots['color'] = get_hex((bots['r'], bots['g'], bots['b']))
    #         cells[x][y]['background'] = bots['color']
    # num_steps += 1
