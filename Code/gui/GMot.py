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
        self.number = Entry(master2, validate="key", state=NORMAL, bg='grey',
                                     font=font, width=5, justify=CENTER)
        self.number.insert(0, self.mot.id)
        self.value = Entry(master2, validate="key", state=NORMAL, bg='grey',
                                     font=font, width=5, justify=CENTER)
        self.value.insert(0, self.mot.value)


    def update(self, From):

        for i in range(self.taille):
            if self.caseGrilleFrame[i].get() != self.mot.lettres[i] and From != self.caseGrilleFrame[i]:
               self.caseGrilleFrame[i].setLettre(self.mot.lettres[i])
            if self.caseMotFrame[i].get() != self.mot.lettres[i] and From != self.caseMotFrame[i]:
                self.caseMotFrame[i].setLettre(self.mot.lettres[i])
        self.value.delete(0, 'end')
        self.value.insert('end', self.mot.value)


    def showDomaine(self):
        s = ""
        for i in self.mot.getDomaine():
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

    def focusMot(self, case):
        for i in range(self.mot.taille):
            if self.caseGrilleFrame[i] is case or self.caseMotFrame[i] is case:
                self.caseGrilleFrame[i].setFocus(True)
                self.caseMotFrame[i].setFocus(True)
            else :
                self.caseGrilleFrame[i].setFocus()
                self.caseMotFrame[i].setFocus()

    def unfocusMot(self):
        for c in self.caseGrilleFrame +  self.caseMotFrame:
            c.setUnfocus()