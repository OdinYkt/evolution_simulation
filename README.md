# Evolution simulation

Small project 4fun.\
 World of bots which are controlled by the gen. Gen it's array of numbers [0..127]. 

## Command of bots
0..7 move \
8..15 eat\
16..23 watch\
24 photosynth\
25 if/else\
26 cell division\
other numbers (26..127)
```python
bots['UTK'] += num
```
## Display
Used standart library tkinter for display. \
Bots has color, which depends on where they get their energy from: \
green - photosynth, red - other bots, blue - minerals
```python 
def crt_cell(x, y):                   
    global cells, x_size, y_size
    x_size = x
    y_size = y
    cells = [[Label(window, text=f'', width=2, height=1, background='white') 
for j in range(y_size)] for i in range(x_size)]
    for j in range(y_size):
        for i in range(x_size):
            cells[i][j].grid(row=i, column=j)
```

## How to use

Run the code. Input number of start cells(ex. 500) \
```python
Введите количество организмов:500
```
In window use 'START\STOP' button to start\stop simulation. \
You can save interesting variants of evolution with button "copy to txt"
