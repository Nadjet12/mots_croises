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




    def toggle(self):
        if self.show.get():
            self.motFrame.grid(row=0, column=1, sticky=N+E+S+W)
        else:
            self.motFrame.grid_forget()


    def set_Grille(self, grille):
        self.grille = grille

        l = 0
        self.grille2 = [
            [Case(self.gframe, validate="key", state=DISABLED,
                                disabledbackground='black', width=5, font=self.customFont)
                         for i in range(grille.taille[1])]
                for j in range(grille.taille[0])]


        self.motVert = [UiMot(mot, self.gframe, self.customFont) for mot in self.grille.mots_verticaux]
        self.motHori = [UiMot(mot, self.gframe, self.customFont) for mot in self.grille.mots_horizontaux]
        #
        # TODO: Attention les lettres qui sont dans deux mot !!!
        # la ne sont que dans hori !!!

        for mot in self.motVert:
            for i in range(mot.taille):
                self.grille2[mot.xStart+i][mot.yStart] = mot.caseG[i]

        for mot in self.motHori:
            for i in range(mot.taille):
                self.grille2[mot.xStart][mot.yStart+i] = mot.caseG[i]


        for line in range(len(self.grille2)):
            for case in range(len(self.grille2[line])):
                self.grille2[line][case].grid(row=line, column=case, ipady=10)

        for mot in self.motVert:
            for i in range(mot.taille):
                mot.update()

        for mot in self.motHori:
            for i in range(mot.taille):
                mot.update()

        # TODO : afficher les mots sur la droite