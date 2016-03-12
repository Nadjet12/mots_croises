from Code.ui.Case import Case
import tkFont

try:
    from tkinter import *
    import tkinter as ttk
except ImportError:
    from Tkinter import *

class UiMot:

    def __init__(self, mot, master, master2, font):

        self.xStart = mot.xStart
        self.yStart = mot.yStart
        self.taille = mot.taille
        self.mot = mot
        self.caseG = [Case(master, validate="key", textvariable=None, state=NORMAL, bg='white',
                           font=font, width=5, justify=CENTER, m=mot, ui=self, pos=i) for i in range(mot.taille)]
        self.caseD = [Case(master2, validate="key", textvariable=None, state=NORMAL, bg='white',
                           font=font, width=5, justify=CENTER, m=mot, ui=self, pos=i) for i in range(mot.taille)]
        self.button = Button(master2, text="Domaine", command=self.showDomaine)


    def update(self):
        # TODO: Update depuis les 3 entrees

        for i in range(self.taille):
            if self.caseG[i].get() != self.mot.lettres[i]:
               self.caseG[i].setLettre(self.mot.lettres[i])
            if self.caseD[i].get() != self.mot.lettres[i]:
                self.caseD[i].setLettre(self.mot.lettres[i])
    def change(self, param, param1):
        pass

    def printD(self):
        s = ""
        for m in self.mot.domaine:
            s += str(m)+" "
        print str(self.mot) + " ->" + s

    def showDomaine(self):
        s = ""
        top = Toplevel()
        top.title("Domaine de " + str(self.mot.lettres))
        for i in self.mot.domaine:
            s+= str(i)+"\n"
        msg = Message(top, text=s)
        msg.pack()
