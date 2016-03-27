from Tkinter import *

from grille import Mot


class MotFrame(Frame):
    def __init__(self, root):

        Frame.__init__(self, root)
        self.ff = Frame(root)
        self.canvas = Canvas(self.ff, borderwidth=0, background="#ffffff")
        self.frame = Frame(self.canvas, background="#ffffff")
        self.vsb = Scrollbar(self.ff, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)


        self.listes = []

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def set_Mots(self):
        print "HELLO"
        line = 0
        col = 0
        max = 0
        for l in self.listes:
            for l2 in l:
                l2.number.grid(row=line, column=col, ipady=10)
                col += 1
                for case in l2.caseMotFrame:
                    case.grid(row=line, column=col, ipady=10)
                    col += 1
                #l2.button.grid(row=line, column=col+1, ipady=10)
                if col > max:
                    max = col
                col = 0
                line += 1
        line = 0
        for l in self.listes:
            col = max+2
            for l2 in l:
                l2.value.grid(row=line, column=col, ipady=10)
                l2.button.grid(row=line, column=col+1, ipady=10)
                line += 1


