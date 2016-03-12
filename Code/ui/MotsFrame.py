#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkFont

from Case import Case
try:
    from Code.ui.UiMot import UiMot
except ImportError:
    import sys
    sys.path.append('./Code/ui/UiMot')

try:
    from tkinter import *
except ImportError:
    from Tkinter import *


class MotsFrame(Canvas):

    def __init__(self, *args, **kwargs):
        kwargs.pop('grille')
        Canvas.__init__(self, *args, **kwargs)
        self.f = Frame(master=self)
        '''
        myframe=Frame(root,relief=GROOVE,width=50,height=100,bd=1)
myframe.place(x=10,y=10)

canvas=Canvas(myframe)
frame=Frame(canvas)
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left")
        '''

    def set_Mots(self, listes):
        line = 0
        col = 0
        max = 0
        print listes
        for l in listes:
            for l2 in l:
                print(l2)
                for case in l2.caseD:
                    case.grid(row=line, column=col, ipady=10)
                    col += 1
                l2.button.grid(row=line, column=col+1, ipady=10)
                if col > max:
                    max = col
                col = 0
                line += 1
        line = 0
        for l in listes:
            for l2 in l:
                l2.button.grid(row=line, column=max+2, ipady=10)
                line += 1

