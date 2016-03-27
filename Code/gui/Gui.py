#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import threading
import ttk
from Queue import Queue
from Tkinter import *

import time
from tkFileDialog import askopenfilename, asksaveasfilename

from grille.Algos import Algo
from grille.Grille import Grille
from gui.GrilleFrame import GrilleFrame
from gui.MainFrame import MainFrame

from grille.Dictionnaire import Dico

DICO_PATH = '../Data/mots/'
GRILLEVIDE_PATH = '../Data/grillesVides/'
GRILLEPLEIN_PATH = '../Data/grillePleines/'

class Gui(Frame):

    def __init__(self, master, algo=None):

        Frame.__init__(self, master)

        # Options pour l'ouverture/sauvegarde des fichiers
        self.openfileoptions = dict()
        self.openfileoptions['filetypes'] = [('Fichier Mots croisés', '.mc'), ('Tout les fichiers', '.*')]
        self.openfileoptions['initialfile'] = 'ma_grille.mc'
        #self.openfileoptions['initialdir'] = GRILLE_PATH
        self.openfileoptions['parent'] = master

        # Queue pour les Threads
        self.thread_queue = Queue()

        self.createMenu()

        self.algo = Algo(algoName="AC3")
        self.algo.setQueue(self.thread_queue)
        self.mainFrame = MainFrame(self, self.algo, self.thread_queue)
        self.mainFrame.pack(fill=BOTH, expand=True)
        self.filename = None



    def update_Algo(self, arg0):
        self.algo.setAlgoName(arg0)
        self.mainFrame.setAlgo()


    def update_Dico(self):
        start = time.time()
        self.dico = Dico(self.dliste[self.radio_dico.get()-1])
        end = time.time() - start
        self.mainFrame.send_To_Trace("Création du dictionnaire "+self.dliste[self.radio_dico.get()-1].split("/")[-1]+" :"+str(end) + "\n", "temps")
        if self.algo.grille:
            self.algo.grille.updateDico(self.dico)

    def file_chooser(self):
        self.filename = None
        self.openfileoptions['initialdir'] = GRILLEVIDE_PATH
        self.filename = askopenfilename(**self.openfileoptions)
        if self.filename:
            self.Ggrille(self.filename)

    def Ggrille(self, file):
        self.algo.setGrille(Grille(filePath=file))
        self.algo.grille.updateDico(self.dico)
        self.setGrille()

    def genere_Grille(self):
        Up = Toplevel()
        Up.title("Générer Grille")

        li = IntVar()
        li.set(10)
        Label(Up, text ="Nombre de ligne :").grid(row=1, column=0, sticky="w")
        w = Scale(Up, from_=5, to=20, orient=HORIZONTAL, var=li)
        w.grid(row=1, column=1, sticky="w")

        col = IntVar()
        col.set(10)
        Label(Up, text ="Nombre de colonne :").grid(row=2, column=0, sticky="w")
        w = Scale(Up, from_=5, to=20, orient=HORIZONTAL, var=col)
        w.grid(row=2, column=1, sticky="w")

        nbN = IntVar()
        nbN.set(30)
        Label(Up, text ="% de case noir :").grid(row=3, column=0, sticky="w")
        w = Scale(Up, from_=10, to=50, orient=HORIZONTAL, var=nbN)
        w.grid(row=3, column=1, sticky="w")


        button = Button(Up, text ="Créer la Grille", command = Up.destroy).grid(row =5,columnspan=2, sticky=N+S+E+W)

        Up.wait_window()
        self.algo.setGrille(Grille(taille=(li.get(),col.get()),alea=True, percent=nbN.get()))
        self.algo.grille.updateDico(self.dico)
        self.setGrille()

    def file_saver(self):
        self.openfileoptions['initialdir'] = GRILLEPLEIN_PATH
        if self.algo.grille:
            self.openfileoptions['initialfile'] = str(self.algo.grille.nomGrille)+"_"+str(self.algo.algoName)
        filename = asksaveasfilename(**self.openfileoptions)
        if filename and self.algo.grille:
            self.algo.grille.sauvegarder_grille(filename)

    def setGrille(self):
        self.mainFrame.open_grille()

    def createMenu(self):
        menubar = Menu(self.master)

        filemenu = Menu(menubar, tearoff=0)
        algomenu = Menu(menubar, tearoff=0)
        dicomenu = Menu(menubar, tearoff=0)

        newGrilleMenu = Menu(menubar, tearoff=0)
        newGrilleMenu.add_command(label="Ouvrir Grille", command=self.file_chooser)

        newGrilleMenu.add_command(label="Générer Grille", command=self.genere_Grille)

        filemenu.add_cascade(label="Nouvelle grille", menu=newGrilleMenu)
        filemenu.add_cascade(label="Sauver Grille", command=self.file_saver)
        filemenu.add_separator()
        filemenu.add_command(label="Quitter", command=self.master.quit)

        self.radio_algo = StringVar()
        algomenu.add_radiobutton(label="AC3", variable=self.radio_algo, value=1,
                                 command=lambda arg0="AC3": self.update_Algo(arg0))
        algomenu.add_radiobutton(label="Forward Checking", variable=self.radio_algo, value=2,
                                 command=lambda arg0="FC": self.update_Algo(arg0))
        algomenu.add_radiobutton(label="FC/AC3", variable=self.radio_algo, value=3,
                                 command=lambda arg0="FC_AC3": self.update_Algo(arg0))

        algomenu.add_radiobutton(label="CBJ", variable=self.radio_algo, value=4,
                                 command=lambda arg0="CJ": self.update_Algo(arg0))

        self.radio_algo.set(1)

        self.radio_dico = IntVar()
        self.listDico = []
        self.dliste = []
        for dirname, dirnames, filenames in os.walk(DICO_PATH):
            for filename in filenames:
                self.dliste += ["".join([DICO_PATH, filename])]
                self.listDico += [filename[:-4]]

        i = 1
        for l in self.listDico:
            dicomenu.add_radiobutton(label=l, variable=self.radio_dico, value=i, command=self.update_Dico)
            i += 1

        self.radio_dico.set(5)
        menubar.add_cascade(label="Fichier", menu=filemenu)
        menubar.add_cascade(label="Algorithme", menu=algomenu)
        menubar.add_cascade(label="Dictionnaire", menu=dicomenu)

        self.dico = Dico(self.dliste[self.radio_dico.get()-1])

        self.master.config(menu=menubar)

