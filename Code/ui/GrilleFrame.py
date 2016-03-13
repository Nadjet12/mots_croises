#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import tkFont

from Case import Case
try:
    from Code import Algos
except ImportError:
    import sys
    sys.path.append('./Code/Algos')
from Code import Algos
from Code.ui.MotsFrame import MotsFrame

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

    def __init__(self, traceFrame, grille=None, master=None):

        Frame.__init__(self, master)
        self.customFont = tkFont.Font(family="Helvetica", size=7)
        self.showadv = IntVar()
        self.showadv.set(0)
        self.showtr= IntVar()
        self.showtr.set(0)
        #self.gframe = Frame(self, width=100, height=100, bg="red")
        self.vsb = Scrollbar(self, orient=VERTICAL)
        self.vsb.grid(row=0, column=2,rowspan=10,  sticky=N+S)
        self.c = Canvas(self,yscrollcommand=self.vsb.set)
        self.vsb.config(command=self.c.yview)
        self.gframe = Frame(self)
        self.motFrame = MotsFrame(self.c, grille=None)
        self.motFrame.pack()
        self.traceFrame = traceFrame





        self.buttonsFrame =Frame(self, width=100, height=100)

        self.playButton = Button(self.buttonsFrame, text="Play", command=self.printt)
        self.playButton.grid(row=0, column=0, sticky=W)

        self.stepButton = Button(self.buttonsFrame, text="Step by Step", command=None)
        self.stepButton.grid(row=0, column=2, sticky=W)

        self.advanceButton = Checkbutton(self.buttonsFrame, text="Voir les mots",
                                         variable=self.showadv, command=self.toggle_Advance)
        self.advanceButton.grid(row=0, column=5, sticky=E)

        self.taceButton = Checkbutton(self.buttonsFrame, text="Trace Algo",
                                         variable=self.showtr, command=self.toggle_Trace)
        self.taceButton.grid(row=0, column=6, sticky=E)

        self.buttonsFrame.grid(row=0, column=0, sticky=N+E+S+W)
        self.gframe.grid(row=1, column=0, sticky=N+E+S+W)
        self.var = 'f'

    def printt(self):
        print "AVANT"
        threading.Thread(target=Algos.ac3(self.grille, self.traceFrame)).start()

        print "apres"
        for m in self.motHori:
            m.update()
        for m in self.motVert:
            m.update()
        for m in self.motHori:
            m.printD()
        for m in self.motVert:
            m.printD()


        print "MOT VERT"
        for mot in self.motVert:
            print mot.mot
        print "MOT HORI"
        for mot in self.motHori:
            print mot.mot



    def toggle_Advance(self):
        if self.showadv.get():
            self.c.grid(row=0, column=1,rowspan=100, sticky=N+E+S+W)
        else:
            self.c.grid_forget()

    def toggle_Trace(self):
        if self.showtr.get():
            self.traceFrame.grid(row=2, column=0, sticky=N+E+S+W)
        else:
            self.traceFrame.grid_forget()


    def set_Grille(self, grille):

        self.grille = grille

        self.grille2 = [
            [None for i in range(grille.taille[1])]
                for j in range(grille.taille[0])]


        self.motVert = [UiMot(self.grille.mots_verticaux[mot], self.gframe, self.motFrame, self.customFont) for mot in range(len(self.grille.mots_verticaux))]
        self.motHori = [UiMot(self.grille.mots_horizontaux[mot], self.gframe, self.motFrame, self.customFont) for mot in range(len(self.grille.mots_horizontaux))]

        for mot in self.motVert:
            for i in range(mot.taille):
                self.grille2[mot.xStart+i][mot.yStart] = mot.caseG[i]

        for mot in self.motHori:
            for i in range(mot.taille):
                self.grille2[mot.xStart][mot.yStart+i] = mot.caseG[i]

        for mot in self.motVert:
            for mot2 in self.motHori:
                c1, c2 = mot.mot.get_Contrainte(mot2.mot)
                if c1 and c2:
                    mot.caseG[c1[1]].add_ui(mot2.caseG[c2[1]].uis)
                    mot2.caseG[c2[1]].add_ui(mot.caseG[c1[1]].uis)
                    mot.caseG[c1[1]] = mot2.caseG[c2[1]]


        for i in range(len(self.grille2)):
            for j in range(len(self.grille2[i])):
                if not self.grille2[i][j]:
                    self.grille2[i][j] = Case(self.gframe, validate="key", state=DISABLED,
                                disabledbackground='black', width=5, font=self.customFont)
        for line in range(len(self.grille2)):
            for case in range(len(self.grille2[line])):
                self.grille2[line][case].grid(row=line, column=case, ipady=10)

        for mot in self.motVert:
            mot.update()

        for mot in self.motHori:
            mot.update()

        # TODO : afficher les mots sur la droite
        self.motFrame.set_Mots([self.motVert, self.motHori ])
        return [self.motVert, self.motHori ]