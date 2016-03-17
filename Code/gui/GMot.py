import tkFont
from Tkinter import *

from gui.Case import Case


class GMot:

    def __init__(self, mot, master, master2):

        self.xStart = mot.xStart
        self.yStart = mot.yStart
        self.taille = mot.taille
        self.mot = mot
        font = tkFont.Font(family="Helvetica", size=7)
        self.caseGrilleFrame = [Case(master, validate="key", textvariable=None, state=NORMAL, bg='white',
                                     font=font, width=5, justify=CENTER, m=mot, ui=self, pos=i)
                                for i in range(mot.taille)]
        self.caseMotFrame = [Case(master2, validate="key", textvariable=None, state=NORMAL, bg='white',
                                  font=font, width=5, justify=CENTER, m=mot, ui=self, pos=i)
                             for i in range(mot.taille)]
        self.button = Button(master2, text="Domaine", command=self.showDomaine)


    def update(self):
        # TODO: Update depuis les 3 entrees

        for i in range(self.taille):
            if self.caseGrilleFrame[i].get() != self.mot.lettres[i]:
               self.caseGrilleFrame[i].setLettre(self.mot.lettres[i])
            if self.caseMotFrame[i].get() != self.mot.lettres[i]:
                self.caseMotFrame[i].setLettre(self.mot.lettres[i])


    def printD(self):
        s = ""
        for m in self.mot.domaine:
            s += str(m)+" "
        print str(self.mot) + " ->" + s

    def showDomaine(self):
        s = ""
        for i in self.mot.domaine:
            s += str(i)+"\n"
        win = Toplevel()
        win.title("Domaine de " + str(self.mot.lettres))
        frame = Frame(win)
        scroll = Scrollbar(frame)
        text = Text(frame, yscrollcommand=scroll.set, height=5, width=self.mot.taille+10)
        # Config
        text.insert(END, ''.join(s))
        scroll.config(command=text.yview)
        # Packing
        text.pack(side='left', fill='both', expand=1)
        scroll.pack(side='right', fill='y')
        frame.pack(fill='both', expand=1)