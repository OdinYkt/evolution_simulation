from tkinter import *
import time
import random
import numpy
import pandas


def crt_cell():
    global cells
    cells = [[Label(text=f'     ', width= 2, height= 1, background= '#9c9192') for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            cells[i][j].place(x=indent+i*21,y=indent+j*22)


def start_color():
    for i in range(size):
        cells[i][0].configure(background='black')
        cells[i][size-1].configure(background='black')
        cells[0][i].configure(background='black')
        cells[size-1][i].configure(background='black')

window = Tk()
window.title("Симулирование эволюции")
window.geometry('1600x1600')


# a = [Label(text=i) for i in range(10)]
# j = 0
# for i in a:
#     i.place(x=j*10,y=10)
#     j += 10

size = 36  # 100x100 count of cells
indent = 50
crt_cell()
start_color()
# tst = Label(text=f'|=|', width= 10, height= 5, background= '#9c9192')
# tst.place(x=100, y=100)

window.mainloop()
