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
                           font=font, width=5, justify=CENTER) for i in range(mot.taille)]
        self.caseD = [Case(master, validate="key", textvariable=None, state=NORMAL, bg='white',
                           font=font, width=5, justify=CENTER) for i in range(mot.taille)]



    def update(self):
        for i in range(self.taille):
            self.caseG[i].setLettre(self.mot.lettres[i])
            self.caseD[i].setLettre(self.mot.lettres[i])
