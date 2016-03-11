from Code.ui.Case import Case
import tkFont

try:
    from tkinter import *
except ImportError:
    from Tkinter import *

class UiMot:

    def __init__(self, mot, master, font):
        self.xStart = mot.xStart
        self.yStart = mot.yStart
        self.taille = mot.taille
        self.mot = mot
        self.caseG = [Case(master, validate="key", textvariable=None, state=NORMAL, bg='white',
                           font=font, width=5, justify=CENTER, m=mot, ui=self, pos=i) for i in range(mot.taille)]
        self.caseD = [Case(master, validate="key", textvariable=None, state=NORMAL, bg='white',
                           font=font, width=5, justify=CENTER, m=mot, ui=self, pos=i) for i in range(mot.taille)]



    def update(self):
        # TODO: Update depuis les 3 entrees

        # update depuis les mots
        for i in range(self.taille):
            self.caseG[i].setLettre(self.mot.lettres[i])
            self.caseD[i].setLettre(self.mot.lettres[i])

    def change(self, param, param1):
        pass
