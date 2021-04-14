import PySimpleGUI as sg
import itertools
import numpy as np
import random 
from collections import deque


clue = {'size':(3,1), 'font':('Franklin Gothic Book', 30), 'readonly':True, 'disabled_readonly_background_color':"#F1EABC", 'justification':'center'}
corner = {'size':(3,1), 'font':('Franklin Gothic Book', 30), 'readonly':True, 'disabled_readonly_background_color':"#343434"}
inputs = {'size':(3,1), 'font':('Franklin Gothic Book', 30), 'background_color':"#15f1af", 'justification':'center'}


col1 = sg.Column(
    [[sg.Input(key=(0,0), **corner)]+[sg.Input(key=(0,i), **clue) for i in range(1,7)]+[sg.Input(key=(0,7), **corner)]], pad=(0,0)
    )
col2 = sg.Column(
    [[sg.Input(key=(i,0), **clue)] for i in range(1,7)], pad=(0,0)
)
col3 = sg.Column(
    [[sg.Input(key=(j,i), **inputs) for i in range(1,7)] for j in range(1,7)], pad=(0,0)
    )
col4 = sg.Column(
    [[sg.Input(key=(i,7), **clue)] for i in range(1,7)], pad=(0,0)
)
col5 = sg.Column(
    [[sg.Input(key=(7,0), **corner)]+ [sg.Input(key=(7,i), **clue) for i in range(1,7)]+[sg.Input(key=(7,7), **corner)]], pad=(0,0)
)
col7 = sg.Column(
    [[sg.Frame('Actions:',
         [[sg.Button('New Game'), sg.Button('Solve'), sg.Button('Clear'), sg.Button('Quit')]], size=(450,45), pad=(0,0)
         )
    ]], pad=(0,0)
)
col6 = sg.Text(key='Output', size=(40,1))

board = sg.Frame('Board', [[col1], [col2, col3, col4], [col5]], )
layout = [[board], [col6], [col7]]
window = sg.Window('6x6 Skyscrapers', layout, size=(900,600))


def solve_puzzle(clues):
    lista = list(itertools.permutations([1, 2, 3, 4, 5, 6]))
    def numSs(tupla):
        m = max(tupla)
        count = 1
        while len(tupla[:tupla.index(m)]) > 0:
            m = max(tupla[:tupla.index(m)])
            count += 1
        return count
    def useClues(a, b):
        if a != 0 and b != 0:
            return [i for i in lista if numSs(i) == a and numSs(tuple(reversed(i))) == b]
        elif a != 0 and b == 0:
            return [i for i in lista if numSs(i) == a]
        elif a == 0 and b != 0:
            return [i for i in lista if numSs(tuple(reversed(i))) == b]
        else:
            return lista
    v = [useClues(clues[i],clues[17-i]) for i in range(6)]
    h = [useClues(clues[i],clues[29-i]) for i in range(6,12)]
    def compX(tupla, index, lista):
        for k in range(6):
            a = [i for i in lista[k] if i[index] == tupla[k]] 
            if a == []:
                return False        
    def compX2(tupla, index, lista):
        for k in range(6):
            a = [i for i in lista[k] if i[index] == tupla[5-k]] 
            if a == []:
                return False
    while sum(len(h[i]) for i in range(6)) > 6:
        for i in range(6):
            v[i] = [j for j in v[i] if not compX(j,5-i,h) == False] 
        for i in range(6):
            h[i] = [j for j in h[i] if not compX2(j,i,v) == False]            
    return tuple(tuple(reversed(i)) for lista in h for i in lista)

tests_clues = {0:(3, 6, 0, 0, 0, 2, 3, 0, 3, 0, 0, 0, 0, 4, 2, 5, 0, 0, 0, 0, 1, 0, 0, 0),
               1:(3, 2, 2, 3, 2, 1, 1, 2, 3, 3, 2, 2, 5, 1, 2, 2, 4, 3, 3, 2, 1, 2, 2, 4), 
               2:(0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0),
               3:(0, 3, 0, 5, 3, 4, 0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 2, 3, 3, 2, 0, 3, 1, 0),
               4:(4, 3, 2, 5, 1, 5, 2, 2, 2, 2, 3, 1, 1, 3, 2, 3, 3, 3, 5, 4, 1, 2, 3, 4)}

def turn_clues(turn, clues): # rotate clues
    queue = deque(clues)
    queue.rotate(-6*turn)
    return tuple(queue)

def clear_inputs():
    for i in range(1,7):
        for j in range(1,7):
            window[(i,j)].update('', background_color = '#15f1af')
            values[(i,j)] = ''

def clear_clues():
    for i in range(1,7):
        window[(0,i)].update('')
        window[(i,7)].update('')
        window[(7,i)].update('')
        window[(i,0)].update('')


tests = list(range(4*4))

c = None

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED  or event == 'Quit':
        break
    if event == 'Clear':
        clear_inputs()
    if event == 'New Game':
        clear_clues()
        clear_inputs()
        x = random.sample(tests, 1)[0]
        tes = x % 5
        turn = x // 4
        c = turn_clues(turn, tests_clues[tes])
        for i in range(1,7):
            if c[i-1] != 0:
                window[(0,i)].update(c[i-1])
            if c[24-i] != 0:
                window[(i,0)].update(c[24-i])
            if c[i+5] != 0:
                window[(i,7)].update(c[i+5])
            if c[18-i] != 0:    
                window[(7,i)].update(c[18-i])
    if event == 'Solve':
        if c:
            x = solve_puzzle(c)
            for i in range(1,7):
                for j in range(1,7):
                    val = window[(i,j)].get()
                    if val != str(x[i-1][j-1]):
                        window[(i,j)].update(background_color = '#ff0000')
                    window[(i,j)].update(x[i-1][j-1])      
        else:
            window['Output'].update('To continue start a new game')
        
        

    #window['-OUTPUT-'].update('first value'+ str(values[(1,1)]) + ', second values' + str(values[(2,2)]))

    # Input verification
    """if len(values['-INPUT-']) and values['-INPUT-'][-1] not in ('0123456789'):
        # delete last char from input
        window['-INPUT-'].update(values['-INPUT-'][:-1])"""

window.close() 

