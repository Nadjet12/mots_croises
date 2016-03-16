import tkFont
from Tkinter import Frame


class GrilleFrame(Frame):

    def __init__(self, master, grille=None):
        Frame.__init__(self, master)
        self.grille = grille

