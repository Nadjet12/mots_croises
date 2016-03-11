#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from Code.Grille import Grille
except ImportError:
    import sys
    sys.path.append('./Code/Grille')

from GrilleFrame import GrilleFrame

try:
    from tkinter import *
except ImportError:
    from Tkinter import *
    from tkFileDialog import askopenfilename, asksaveasfilename

import os

grille = [['.', '.', '.', '.', None, '.', '.', '.', '.'],
          ['.', None, '.', None, None, None, '.', None, '.'],
          ['.', '.', '.', '.', None, '.', '.', '.', '.'],
          [None, '.', None, '.', '.', '.', None, '.', None],
          ['.', '.', '.', '.', None, '.', '.', '.', '.'],
          [None, '.', None, '.', '.', '.', None, '.', None],
          ['.', '.', '.', '.', None, '.', '.', '.', '.'],
          ['.', None, '.', None, None, None, '.', None, '.'],
          ['.', '.', '.', '.', None, '.', '.', '.', '.']]

class MainFrame(Frame):

    def __init__(self, master=None):

        Frame.__init__(self, master)

        self.options = dict()
        self.options['filetypes'] = [('Fichier Mots croisés', '.mc'), ('Tout les fichiers', '.*')]
        self.options['initialfile'] = 'ma_grille.mc'
        self.options['parent'] = root

        self.grille = grille
        self.frameMot = Frame(self, width=100, height=100, bg="yellow")
        self.frameGrille = GrilleFrame(self.frameMot, grille=self.grille, master=self)

        self.frameGrille.grid(row=0, column=0, sticky=N+E+S+W)


        menubar = Menu(master)

        filemenu = Menu(menubar, tearoff=0)
        algomenu = Menu(menubar, tearoff=0)
        dicomenu = Menu(menubar, tearoff=0)

        newGrilleMenu = Menu(menubar, tearoff=0)
        newGrilleMenu.add_command(label="Ouvrir Grille", command=self.file_chooser)
        newGrilleMenu.add_command(label="Sauver Grille", command=self.file_saver)
        newGrilleMenu.add_command(label="Générer Grille", command=self.genere_Grille)

        filemenu.add_cascade(label="Nouvelle grille", menu=newGrilleMenu)
        filemenu.add_separator()
        filemenu.add_command(label="Quitter", command=master.quit)

        self.radio_algo = StringVar()
        algomenu.add_radiobutton(label="AC3", variable=self.radio_algo, value=1,
                                 command=lambda arg0="Algo1": self.test(arg0))
        algomenu.add_radiobutton(label="Algo2", variable=self.radio_algo, value=2,
                                 command=lambda arg0="Algo2": self.test(arg0))
        algomenu.add_radiobutton(label="Algo3", variable=self.radio_algo, value=3,
                                 command=lambda arg0="Algo3": self.test(arg0))
        self.radio_algo.set(1)

        self.radio_dico = StringVar()
        self.listDico = []
        for dirname, dirnames, filenames in os.walk('../mots'):
            # print path to all filenames.
            for filename in filenames:
                filename = filename[:-4]
                print(filename)
                self.listDico += [filename]

        i = 1
        for l in self.listDico:
            dicomenu.add_radiobutton(label=l, variable=self.radio_dico, value=i, command=lambda arg0=l: self.test(arg0))
            i += 1

        self.radio_dico.set(2)
        menubar.add_cascade(label="Fichier", menu=filemenu)
        menubar.add_cascade(label="Algorithme", menu=algomenu)
        menubar.add_cascade(label="Dictionnaire", menu=dicomenu)

        master.config(menu=menubar)

    @staticmethod
    def test(arg0):
        print arg0

    def file_chooser(self):
        filename = askopenfilename(**self.options)
        self.grille = Grille(filename)
        self.frameGrille.set_Grille(self.grille)
        print(filename)

    def genere_Grille(self):
        self.grille =  Grille(taille=(10,10),alea=True)
        self.frameGrille.set_Grille(self.grille)

    def file_saver(self):
        filename = asksaveasfilename(**self.options)
        print(filename)


if __name__ == "__main__":
    root = Tk()

    interface = MainFrame(master=root)
    interface.master.title("Mots Croisés")
    # interface.master.geometry('{}x{}'.format(800, 600))
    interface.pack(fill="both", expand=True)

    interface.mainloop()
