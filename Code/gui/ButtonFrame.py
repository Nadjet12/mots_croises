#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
from Tkinter import *

import time

from grille.Algos import Algo


class ButtonFrame(Frame):

    def __init__(self, master, queue, algo=None, traceFrame=None, motFrame=None):

        Frame.__init__(self, master)
        self.showMot = IntVar()
        self.showMot.set(0)
        self.showTrace = IntVar()
        self.showTrace.set(0)


        self.playButton = Button(self, text="Lancer l'algo", command=self.play)
        self.playButton.grid(row=0, column=0)
        self.playButton.configure(state="disabled")
        self.continueButton = Button(self, text="Continuer l'algo", command=self.continueAlgo)
        self.continueButton.configure(state="disabled")
        self.continueButton.grid(row=0, column=1)


        self.advanceButton = Checkbutton(self, text="Voir les mots",
                                         variable=self.showMot, command=self.toggle_Mot)
        self.advanceButton.configure(state="disabled")

        self.resetButton = Button(self, text="Remise à zero",
                                         command=self.raz)
        self.resetButton.grid(row=0, column=2)
        self.resetButton.configure(state="disabled")

        self.advanceButton.grid(row=0, column=5, sticky=E)
        self.traceButton = Checkbutton(self, text="Trace algo",
                                      variable=self.showTrace, command=self.toggle_Trace)
        self.traceButton.grid(row=0, column=3, sticky=E)

        self.cleartraceButton = Button(self, text="Clear Trace",
                                      command=self.clearTrace)
        self.cleartraceButton.configure(state="disabled")
        self.cleartraceButton .grid(row=0, column=4, sticky=E)
        self.queue = queue
        self.algo = algo
        self.traceFrame = traceFrame
        self.motFrame = motFrame



    def play(self):
        self.resetButton.configure(state="normal")
        if self.algo.hasRun:
            self.algo.stop()
            self.algo = Algo(queue=self.queue, grille=self.algo.grille, traceframe=self.traceFrame, algoName=self.algo.algoName, heuristique=self.algo.heur)

            self.master.send_To_Trace("nombre de mot sur la grille :" + str(len(self.algo.grille.mots_horizontaux + self.algo.grille.mots_verticaux))+"\n", "curr")
            self.master.send_To_Trace("nombre de mot dans les Domaines :" + str(self.algo.grille.get_Domaines_Sizes())+"\n", "curr")

            self.algo.start()
            self.after(1000, self.process_queue)
        else:

            self.master.send_To_Trace("nombre de mot sur la grille :" + str(len(self.algo.grille.mots_horizontaux + self.algo.grille.mots_verticaux))+"\n", "curr")
            self.master.send_To_Trace("nombre de mot dans les Domaines :" + str(self.algo.grille.get_Domaines_Sizes())+"\n", "curr")
            self.algo.start()

            self.after(1000, self.process_queue)

    def raz(self):
        self.master.Ggrille(self.algo.grille.filePath)
        self.resetButton.configure(state="disabled")

    def process_queue(self):
        try:
            #print "try " + str(self.queue.get(0))
            result = self.queue.get(0)
            self.show(result)
        except Queue.Empty:
            #print "empty"
            self.after(1000, self.process_queue)


    def toggle_Mot(self):
        if self.showMot.get() and self.motFrame:
            self.master.toggle_Mot(True)
            #self.motFrame.grid(row=0, column=1,rowspan=100, sticky=N+E+S+W)
        else:
            self.master.toggle_Mot(False)
            #self.c.grid_forget()

    def toggle_Trace(self):
        if self.showTrace.get() and self.traceFrame:
            self.master.toggle_Trace(True)
            self.cleartraceButton.configure(state="normal")
            #self.traceFrame.grid(row=2, column=0, sticky=N+E+S+W)
        else:
            self.master.toggle_Trace(False)
            self.cleartraceButton.configure(state="disabled")
            #self.traceFrame.grid_forget()
    def clearTrace(self):
        if self.traceFrame:
            self.master.clearTrace()
    def show(self, result):

        if self.algo.algoName is 'AC3':
            mess = 'Non Arc-Consistant'
            if result:
                mess = 'Arc-Consistant'
            top = Toplevel()
            top.title("Resultat")

            msg = Message(top, text=mess)
            msg.pack()
            self.algo.stop()

        elif result:
            self.continueButton.configure(state="normal")
            self.algo.grille.setResultat(result)
            self.master.updateGrille()
            for m in self.algo.grille.mots_horizontaux + self.algo.grille.mots_verticaux:
                self.master.send_To_Trace(str(m)+'\n', "curr")


            pass
        else:
            self.continueButton.configure(state="disabled")
            mess = 'Pas/plus de résultat'
            top = Toplevel()
            top.title("Resultat")

            msg = Message(top, text=mess)
            msg.pack()
            self.algo.stop()
        self.after(1000, self.process_queue)


    def continueAlgo(self):
        self.algo.resume()
        self.continueButton.configure(state="disabled")
        self.after(1000, self.process_queue)

    def enableMot(self, bool):
        if bool:
            self.playButton.configure(state="normal")
            self.advanceButton.configure(state="normal")
        else:
            self.advanceButton.configure(state="disabled")
            self.playButton.configure(state="disabled")