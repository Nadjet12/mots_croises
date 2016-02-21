#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkFont

from Code.ui.Case import Case

try:
    from tkinter import *
except ImportError:
    from Tkinter import *


class GrilleFrame(Frame):

    def __init__(self, motFrame, grille=None, master=None):

        Frame.__init__(self, master)
        self.customFont = tkFont.Font(family="Helvetica", size=12)
        self.show = IntVar()
        self.show.set(0)
        self.gframe = Frame(self, width=100, height=100, bg="red")
        self.motFrame = motFrame
        self.buttonsFrame =Frame(self, width=100, height=100)

        self.playButton = Button(self.buttonsFrame, text="Play", command=None)
        self.playButton.grid(row=0, column=0, sticky=W)

        self.stepButton = Button(self.buttonsFrame, text="Step by Step", command=None)
        self.stepButton.grid(row=0, column=2, sticky=W)

        self.advanceButton = Checkbutton(self.buttonsFrame, text="Voir les mots",
                                         variable=self.show, command=self.toggle)
        self.advanceButton.grid(row=0, column=5, sticky=E)

        self.buttonsFrame.grid(row=0, column=0, sticky=N+E+S+W)
        self.gframe.grid(row=1, column=0, sticky=N+E+S+W)
        self.var = 'f'
        l = 0
        self.grille2 = []
        for line in grille:
            col = 0
            g = []
            for c in line:
                if c is None:
                    g += [Case(self.gframe, validate="key", state=DISABLED,
                                disabledbackground='black', width=5, font=self.customFont)]
                    g[-1].grid(row=l, column=col, ipady=10)
                else:

                    g += [Case(self.gframe, validate="key",
                                textvariable=None,
                                state=NORMAL,
                                # state="readonly",
                                bg='white',
                                font=self.customFont,
                                width=5,
                                justify=CENTER)]
                    g[-1].grid(row=l, column=col, ipady=10)

                col += 1
            l += 1
            self.grille2 += [g]



    def toggle(self):
        if self.show.get():
            self.motFrame.grid(row=0, column=1, sticky=N+E+S+W)
        else:
            self.motFrame.grid_forget()


