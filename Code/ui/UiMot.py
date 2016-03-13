from Tkinter import *

from ui.Case import Case


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
        for i in self.mot.domaine:
            s+= str(i)+"\n"
        win    = Toplevel()
        win.title("Domaine de " + str(self.mot.lettres))
        frame  = Frame(win)
        scroll = Scrollbar(frame)
        text   = Text(frame, yscrollcommand=scroll.set, height=5, width=self.mot.taille+10)
        # Config
        text.insert(END, ''.join(s))
        scroll.config(command=text.yview)
        # Packing
        text.pack(side='left', fill='both', expand=1)
        scroll.pack(side='right', fill='y')
        frame.pack(fill='both', expand=1)
