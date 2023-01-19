### (C) 2023 neutrogic
###
### This is a general script for programs I make using tkinter/ttkbootstrap. It's just general functions.
###

import os
import yaml
from tkinter import *
import ttkbootstrap as ttkb

#Centers the screen... would like for this to work with dynamic sizes...
def center(root, w, h):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    
    return ('%dx%d+%d+%d' % (w, h, x, y))

#idk why i made a function for this
def destroy(root):
	root.destroy()

#verifies input as interger and prevents entry of non-numeric characters
def verify_int(event):
    v = event.char
    try:
        v = int(v)
    except ValueError:
        if v != '\x08' and v != '':
            return 'break'

#verifies input as float and prevents entry of non-numeric characters
def verify_float(event):
    v = event.char
    try:
        v = float(v)
    except ValueError:
        if v != '\x08' and v != '':
            return 'break'

#turns a given yaml file, in the cwd, into a dictionary file. 
#i use this to keep my scripts looking cleaner.
def yaml_dict(name):
    with open(os.path.join(os.getcwd(), name + '.yaml'), 'r', encoding='utf-8') as dicky:
        dictionary = yaml.safe_load(dicky)

    return dictionary