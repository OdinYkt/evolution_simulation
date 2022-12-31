from tkinter import *
window = Tk()
window.title("Симулирование эволюции")
window.geometry('1600x1600')
color = []
n = 30 #цветов
h = 10
for r in range(0, 256, int(255/h)):
    for g in range(0, 256, int(255/h)):
        for b in range(0, 256, int(255/h)):
            color.append([r, g, b])
            print([r, g, b])
print(len(color))