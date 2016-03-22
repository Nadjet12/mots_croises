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

DICO_PATH = './mots/'

class Gui(Frame):

    def __init__(self, master, root, algo=None):

        Frame.__init__(self, master)

        # Options pour l'ouverture/sauvegarde des fichiers
        self.openfileoptions = dict()
        self.openfileoptions['filetypes'] = [('Fichier Mots croisés', '.mc'), ('Tout les fichiers', '.*')]
        self.openfileoptions['initialfile'] = 'ma_grille.mc'
        self.openfileoptions['parent'] = root

        # Queue pour les Threads
        self.thread_queue = Queue()


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
                                 command=lambda arg0="AC3": self.update_Algo(arg0))
        algomenu.add_radiobutton(label="Forward Checking", variable=self.radio_algo, value=2,
                                 command=lambda arg0="FC": self.update_Algo(arg0))
        algomenu.add_radiobutton(label="FC/AC3", variable=self.radio_algo, value=3,
                                 command=lambda arg0="FC_AC3": self.update_Algo(arg0))

        algomenu.add_radiobutton(label="BCJ", variable=self.radio_algo, value=4,
                                 command=lambda arg0="BCJ": self.update_Algo(arg0))

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

        self.radio_dico.set(2)
        menubar.add_cascade(label="Fichier", menu=filemenu)
        menubar.add_cascade(label="Algorithme", menu=algomenu)
        menubar.add_cascade(label="Dictionnaire", menu=dicomenu)

        self.dico = self.dliste[self.radio_dico.get()-1]

        master.config(menu=menubar)
        self.algo = algo
        self.grille = None
        self.algo.queue = self.thread_queue
        self.mainFrame = MainFrame(self, self.algo, self.thread_queue)
        self.mainFrame.pack()



    def update_Algo(self, arg0):
        self.algo.algo = arg0

    def update_Dico(self):
        print "update dico :" + str(self.dliste[self.radio_dico.get()-1])
        self.dico = self.dliste[self.radio_dico.get()-1]
        if self.grille:
            self.grille.updateDico(self.dico)
        print "a faire update_dico"

    def file_chooser(self):
        filename = askopenfilename(**self.openfileoptions)
        self.grille = Grille(filePath=filename, dictionnaire=self.dico)
        self.algo.grille = self.grille
        print "a faire file_chooser"
        self.setGrille()


    def genere_Grille(self):
        print "a faire genere_Grille"
        self.grille =  Grille(taille=(10,10),alea=True, dictionnaire=self.dico)
        self.algo.grille = self.grille
        self.setGrille()

    def file_saver(self):
        filename = asksaveasfilename(**self.openfileoptions)
        print "a faire genere_Grille"

    def setGrille(self):
        self.mainFrame.open_grille(self.grille)
        
    '''
    def __init__(self, master):
        self.master = master
        self.test_button = Button(self.master, command=self.tb_click)
        self.test_button.configure(
            text="Start", background="Grey",
            padx=50
            )
        self.test_button.pack(side=TOP)

    def progress(self):
        self.prog_bar = ttk.Progressbar(
            self.master, orient="horizontal",
            length=200, mode="indeterminate"
            )
        self.prog_bar.pack(side=TOP)

    def tb_click(self):
        self.progress()
        self.prog_bar.start()
        self.queue = Queue.Queue()
        ThreadedTask(self.queue).start()
        self.master.after(100, self.process_queue)

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            print msg
            # Show result of the task if needed
            self.prog_bar.stop()
        except Queue.Empty:
            self.master.after(100, self.process_queue)


class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        time.sleep(5)  # Simulate long running process
        s
        print "guiFrame"elf.queue.put("Task finished")
    '''

